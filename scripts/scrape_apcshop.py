#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import time
import xml.etree.ElementTree as ET
from collections import deque
from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests


BASE_URL = "https://apcshop.eu/"
OUTPUT_DIR = Path("data_source/scraped/apcshop")
USER_AGENT = "Mozilla/5.0 (compatible; Codex APC scraper/1.0; +https://apcshop.eu/)"
PRESENTATION_PATHS = [
    "/",
    "/kontakt",
    "/motoskola",
    "/pozicovna",
    "/servis",
    "/obchodne-podmienky",
]
SKIP_PREFIXES = (
    "/pub/",
    "/static/",
    "/customer/",
    "/checkout/",
    "/wishlist/",
    "/catalogsearch/",
    "/newsletter_popup/",
    "/theme_options/",
)
SKIP_EXACT = {
    "/",
    "/blog",
    "/blog/",
    "/kontakt",
}
URL_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)
TAG_RE = re.compile(r"<[^>]+>")


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data:
            self.parts.append(data)

    def get_text(self) -> str:
        text = " ".join(part.strip() for part in self.parts if part.strip())
        return re.sub(r"\s+", " ", unescape(text)).strip()


def strip_tags(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment)
    return parser.get_text()


def search(pattern: str, text: str, flags: int = re.I | re.S) -> str | None:
    match = re.search(pattern, text, flags)
    return unescape(match.group(1)).strip() if match else None


def search_all(pattern: str, text: str, flags: int = re.I | re.S) -> list[str]:
    return [unescape(item).strip() for item in re.findall(pattern, text, flags)]


def normalize_url(url: str) -> str:
    parsed = urlparse(urljoin(BASE_URL, url))
    scheme = "https"
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    query = f"?{parsed.query}" if parsed.query else ""
    return f"{scheme}://{netloc}{path}{query}"


def is_internal(url: str) -> bool:
    return urlparse(url).netloc.endswith("apcshop.eu")


def should_skip(url: str) -> bool:
    parsed = urlparse(url)
    if not is_internal(url):
        return True
    if parsed.path in SKIP_EXACT:
        return False
    return parsed.path.startswith(SKIP_PREFIXES)


def slug(url: str) -> str:
    parsed = urlparse(url)
    value = parsed.path.strip("/").replace("/", "__") or "home"
    if parsed.query:
        value += "__" + re.sub(r"[^a-zA-Z0-9]+", "_", parsed.query).strip("_")
    return value


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def extract_internal_links(html: str, current_url: str) -> list[str]:
    links: list[str] = []
    for href in URL_RE.findall(html):
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        normalized = normalize_url(urljoin(current_url, href))
        if is_internal(normalized) and not should_skip(normalized):
            links.append(normalized)
    return dedupe(links)


def extract_meta(html: str, name: str) -> str | None:
    return search(
        rf'<meta[^>]+(?:name|property)=["\']{re.escape(name)}["\'][^>]+content=["\']([^"\']+)["\']',
        html,
    )


def extract_breadcrumbs(html: str) -> list[str]:
    values = search_all(r'<li class="item[^"]*">\s*<a[^>]*>\s*<span>(.*?)</span>', html)
    active = search(r'<li class="item current">\s*<strong>(.*?)</strong>', html)
    if active:
        values.append(active)
    return dedupe([strip_tags(item) for item in values if strip_tags(item)])


def remove_blocks(html: str) -> str:
    cleaned = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    cleaned = re.sub(r"<style\b[^>]*>.*?</style>", " ", cleaned, flags=re.I | re.S)
    cleaned = re.sub(r"<!--.*?-->", " ", cleaned, flags=re.S)
    cleaned = re.sub(r"<noscript\b[^>]*>.*?</noscript>", " ", cleaned, flags=re.I | re.S)
    return cleaned


def extract_main_section(html: str) -> str | None:
    cleaned = remove_blocks(html)
    for pattern in [
        r'<main id="maincontent" class="page-main">(.*?)</main>',
        r'<div class="category-view">(.*?)</main>',
        r'<div class="columns"><div class="column main">(.*?)</main>',
    ]:
        match = re.search(pattern, cleaned, re.I | re.S)
        if match:
            return match.group(1)
    return None


def extract_headings(html: str) -> dict[str, list[str]]:
    return {
        "h1": dedupe(strip_tags(item) for item in search_all(r"<h1[^>]*>(.*?)</h1>", html)),
        "h2": dedupe(strip_tags(item) for item in search_all(r"<h2[^>]*>(.*?)</h2>", html)),
        "h3": dedupe(strip_tags(item) for item in search_all(r"<h3[^>]*>(.*?)</h3>", html)),
    }


def compact_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_presentation_page(url: str, html: str) -> dict:
    main_section = extract_main_section(html) or html
    text = compact_text(strip_tags(main_section))
    paragraphs = [
        compact_text(strip_tags(item))
        for item in search_all(r"<p\b[^>]*>(.*?)</p>", main_section)
    ]
    paragraphs = [item for item in paragraphs if item and item not in {"&nbsp;"}]
    return {
        "url": url,
        "title": search(r"<title>(.*?)</title>", html),
        "meta_description": extract_meta(html, "description"),
        "breadcrumbs": extract_breadcrumbs(html),
        "headings": extract_headings(main_section),
        "paragraphs": paragraphs,
        "text_excerpt": text[:5000],
        "internal_links": extract_internal_links(main_section, url)[:200],
    }


def classify_page(url: str, html: str) -> str:
    parsed = urlparse(url)
    if parsed.path in ("/", ""):
        return "home"
    if parsed.path.rstrip("/") == "/kontakt":
        return "contact"
    if parsed.path.rstrip("/") == "/blog":
        return "blog_index"
    if parsed.path.startswith("/blog/"):
        return "blog_post"
    if 'class="product-info-main"' in html and 'itemprop="sku"' in html:
        return "product"
    if "product-item-link" in html or "category-view" in html:
        return "category"
    return "page"


def extract_json_text(fragment: str) -> str:
    cleaned = TAG_RE.sub(" ", fragment)
    return re.sub(r"\s+", " ", unescape(cleaned)).strip()


def extract_product(url: str, html: str) -> dict:
    description_html = search(
        r'<div class="product attribute description">.*?<div class="value"[^>]*>(.*?)</div>\s*</div>',
        html,
    )
    short_description_html = search(
        r'<div class="product attribute overview">.*?<div class="value"[^>]*>(.*?)</div>\s*</div>',
        html,
    )
    return {
        "url": url,
        "type": "product",
        "title": search(r'<span class="base"[^>]*itemprop="name">(.*?)</span>', html)
        or extract_meta(html, "title"),
        "meta_description": extract_meta(html, "description"),
        "sku": search(r'<div class="value" itemprop="sku">(.*?)</div>', html),
        "availability": search(r'<div class="stock [^"]+">.*?<span>(.*?)</span>', html),
        "price_with_tax": search(
            r'id="product-price-\d+"[^>]*class="price-wrapper[^"]*">\s*<span class="price">(.*?)</span>',
            html,
        ),
        "price_without_tax": search(
            r'id="price-excluding-tax-product-price-\d+"[^>]*>\s*<span class="price">(.*?)</span>',
            html,
        ),
        "brand": search(r'<meta itemprop="brand" content="([^"]+)"', html)
        or search(r'<h4 class="product-brand-name">\s*<a[^>]*>(.*?)</a>', html),
        "breadcrumbs": extract_breadcrumbs(html),
        "main_image": search(
            r'<div class="gallery-placeholder[^"]*"[^>]*>.*?<img[^>]+src="([^"]+)"',
            html,
        ),
        "gallery_images": dedupe(
            search_all(r'"full":"(https:\\/\\/[^"]+)"', html)
            + search_all(r'<img[^>]+data-src="([^"]+/catalog/product/[^"]+)"', html)
            + search_all(r'<img[^>]+src="([^"]+/catalog/product/[^"]+)"', html)
        ),
        "description_html": description_html,
        "description_text": strip_tags(description_html) if description_html else None,
        "short_description_html": short_description_html,
        "short_description_text": strip_tags(short_description_html) if short_description_html else None,
    }


def extract_category(url: str, html: str) -> dict:
    title = search(r"<title>(.*?)</title>", html)
    product_links = dedupe(
        normalize_url(item) for item in search_all(r'class="product-item-link"[^>]+href="([^"]+)"', html)
    )
    product_links = [item for item in product_links if classify_product_candidate(item)]
    pagination_links = dedupe(
        normalize_url(item)
        for item in search_all(r'href="([^"]+\?p=\d+[^"]*)"', html)
        if is_internal(normalize_url(item))
    )
    return {
        "url": url,
        "type": "category",
        "title": title,
        "meta_description": extract_meta(html, "description"),
        "breadcrumbs": extract_breadcrumbs(html),
        "product_links": product_links,
        "pagination_links": pagination_links,
    }


def classify_product_candidate(url: str) -> bool:
    path = urlparse(url).path.strip("/")
    if not path:
        return False
    if any(path.startswith(prefix.strip("/")) for prefix in ("blog/", "customer/", "checkout/")):
        return False
    if path in {"kontakt"}:
        return False
    return len(path.split("/")) == 1


def extract_contact(url: str, html: str) -> dict:
    body_text = strip_tags(html)
    phones = dedupe(search_all(r'href="tel:([^"]+)"', html))
    emails = dedupe(search_all(r'href="mailto:([^"]+)"', html))
    address_candidates = dedupe(
        re.findall(
            r"(Duklianska[^,.<\n]*[, ]+\d+[A-Za-z/]*[, ]+[0-9]{3}\s?[0-9]{2}\s+[A-Za-zÁ-Žá-ž ]+)",
            body_text,
        )
    )
    opening_hours = dedupe(
        re.findall(r"(Po.*?(?:Sobota|Nedeľa).*?(?:[0-9]{1,2}:[0-9]{2}|Zatvorené))", body_text)
    )
    return {
        "url": url,
        "type": "contact",
        "title": search(r"<title>(.*?)</title>", html),
        "meta_description": extract_meta(html, "description"),
        "phones": phones,
        "emails": emails,
        "addresses": address_candidates,
        "opening_hours": opening_hours,
        "text_excerpt": body_text[:2000],
    }


def extract_blog_post(url: str, html: str) -> dict:
    content_html = search(r'<div class="post-content">(.*?)<div class="post-data">', html)
    if not content_html:
        content_html = search(r'<div class="post-content">(.*?)</article>', html)
    return {
        "url": url,
        "type": "blog_post",
        "title": search(r"<title>(.*?)\s*\|\s*APC Shop</title>", html) or search(r"<title>(.*?)</title>", html),
        "meta_description": extract_meta(html, "description"),
        "published_at": search(r'<time[^>]+datetime="([^"]+)"', html),
        "hero_images": dedupe(search_all(r'<img[^>]+src="([^"]+)"', content_html or "")),
        "content_html": content_html,
        "content_text": strip_tags(content_html) if content_html else None,
    }


def extract_home(url: str, html: str) -> dict:
    return {
        "url": url,
        "type": "home",
        "title": search(r"<title>(.*?)</title>", html),
        "meta_description": extract_meta(html, "description"),
        "meta_keywords": extract_meta(html, "keywords"),
        "top_internal_links": extract_internal_links(html, url)[:200],
    }


def read_sitemap(session: requests.Session) -> list[str]:
    response = session.get(urljoin(BASE_URL, "sitemap.xml"), timeout=30)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text.strip() for node in root.findall("sm:url/sm:loc", ns) if node.text]
    return [normalize_url(item) for item in urls if "apcshop.eu" in item]


@dataclass
class CrawlResult:
    pages: dict[str, dict] = field(default_factory=dict)
    categories: dict[str, dict] = field(default_factory=dict)
    products: dict[str, dict] = field(default_factory=dict)
    blog_posts: dict[str, dict] = field(default_factory=dict)
    contacts: dict[str, dict] = field(default_factory=dict)
    presentation_pages: dict[str, dict] = field(default_factory=dict)
    errors: list[dict] = field(default_factory=list)


class ApcShopScraper:
    def __init__(self, delay: float, max_urls: int, timeout: int) -> None:
        self.delay = delay
        self.max_urls = max_urls
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.result = CrawlResult()

    def fetch(self, url: str) -> str:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def crawl(self) -> CrawlResult:
        seeds = dedupe(
            [
                normalize_url(BASE_URL),
                normalize_url(urljoin(BASE_URL, "/kontakt")),
                normalize_url(urljoin(BASE_URL, "/blog/")),
            ]
        )
        seeds.extend(normalize_url(urljoin(BASE_URL, path)) for path in PRESENTATION_PATHS)

        try:
            homepage = self.fetch(BASE_URL)
            seeds.extend(extract_internal_links(homepage, BASE_URL))
            self.result.pages[normalize_url(BASE_URL)] = extract_home(normalize_url(BASE_URL), homepage)
            self.result.presentation_pages[normalize_url(BASE_URL)] = extract_presentation_page(
                normalize_url(BASE_URL), homepage
            )
        except Exception as exc:
            self.result.errors.append({"url": BASE_URL, "error": str(exc)})
            homepage = ""

        try:
            seeds.extend(read_sitemap(self.session))
        except Exception as exc:
            self.result.errors.append({"url": urljoin(BASE_URL, "sitemap.xml"), "error": str(exc)})

        queue = deque(dedupe(item for item in seeds if is_internal(item) and not should_skip(item)))
        visited: set[str] = set()

        while queue and len(visited) < self.max_urls:
            url = queue.popleft()
            if url in visited:
                continue
            visited.add(url)
            try:
                html = self.fetch(url)
                page_type = classify_page(url, html)
                if urlparse(url).path in PRESENTATION_PATHS:
                    self.result.presentation_pages[url] = extract_presentation_page(url, html)
                if page_type == "category":
                    payload = extract_category(url, html)
                    self.result.categories[url] = payload
                    for next_url in reversed(payload["pagination_links"]):
                        if next_url not in visited:
                            queue.append(next_url)
                    for next_url in reversed(payload["product_links"]):
                        if next_url not in visited:
                            queue.appendleft(next_url)
                elif page_type == "product":
                    self.result.products[url] = extract_product(url, html)
                elif page_type == "contact":
                    self.result.contacts[url] = extract_contact(url, html)
                    self.result.presentation_pages[url] = extract_presentation_page(url, html)
                elif page_type == "blog_index":
                    blog_urls = [
                        next_url
                        for next_url in extract_internal_links(html, url)
                        if next_url.startswith(normalize_url(urljoin(BASE_URL, "/blog/")))
                        and next_url != normalize_url(urljoin(BASE_URL, "/blog/"))
                    ]
                    for next_url in reversed(blog_urls):
                        if next_url.startswith(normalize_url(urljoin(BASE_URL, "/blog/"))) and next_url != normalize_url(
                            urljoin(BASE_URL, "/blog/")
                        ):
                            queue.appendleft(next_url)
                elif page_type == "blog_post":
                    self.result.blog_posts[url] = extract_blog_post(url, html)
                else:
                    self.result.pages[url] = {
                        "url": url,
                        "type": page_type,
                        "title": search(r"<title>(.*?)</title>", html),
                        "meta_description": extract_meta(html, "description"),
                    }
            except Exception as exc:
                self.result.errors.append({"url": url, "error": str(exc)})
            if self.delay:
                time.sleep(self.delay)

        self.result.pages["crawl_summary"] = {
            "visited_urls": len(visited),
            "captured_categories": len(self.result.categories),
            "captured_products": len(self.result.products),
            "captured_blog_posts": len(self.result.blog_posts),
            "captured_contacts": len(self.result.contacts),
            "captured_presentation_pages": len(self.result.presentation_pages),
            "errors": len(self.result.errors),
        }
        return self.result


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape important business and catalog data from apcshop.eu")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between HTTP requests in seconds")
    parser.add_argument("--max-urls", type=int, default=250, help="Maximum number of URLs to crawl")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR, help="Directory for JSON output")
    args = parser.parse_args()

    scraper = ApcShopScraper(delay=args.delay, max_urls=args.max_urls, timeout=args.timeout)
    result = scraper.crawl()

    output_dir = args.output_dir
    write_json(output_dir / "pages.json", result.pages)
    write_json(output_dir / "categories.json", sorted(result.categories.values(), key=lambda item: item["url"]))
    write_json(output_dir / "products.json", sorted(result.products.values(), key=lambda item: item["url"]))
    write_json(output_dir / "blog_posts.json", sorted(result.blog_posts.values(), key=lambda item: item["url"]))
    write_json(output_dir / "contacts.json", sorted(result.contacts.values(), key=lambda item: item["url"]))
    write_json(
        output_dir / "presentation_pages.json",
        sorted(result.presentation_pages.values(), key=lambda item: item["url"]),
    )
    write_json(output_dir / "errors.json", result.errors)
    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "categories": len(result.categories),
                "products": len(result.products),
                "blog_posts": len(result.blog_posts),
                "contacts": len(result.contacts),
                "presentation_pages": len(result.presentation_pages),
                "errors": len(result.errors),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
