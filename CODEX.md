# Project Context For Codex

## What This Repository Is

This repository contains a static HTML adaptation project based on the Boxcar automotive template.

There are two layers:

1. The original multi-page HTML template in `1.HTML_Template/`
2. APC Shop content and page-mapping inputs in `data_source/`

The practical goal is not to build a new app from scratch, but to reshape an existing automotive dealer template into a presentation and e-shop site for ALFA PRO CONCEPT / APC Shop.

## Key Directories

- `1.HTML_Template/`
  Static source template with all page variants, CSS, JS, fonts, and images.
- `2.Documentation/`
  Vendor documentation for the Boxcar template.
- `3.Licensing/`
  License files for the purchased/distributed template.
- `data_source/`
  Business content and mapping rules for the APC conversion.

## Template Characteristics

- Static HTML, not WordPress and not a component-based frontend app
- Bootstrap-based styling
- jQuery-based behavior
- Main editable assets:
  - `1.HTML_Template/css/style.css`
  - `1.HTML_Template/js/main.js`
- Large set of ready-made pages:
  homepages, inventory, blog, shop, dealer, dashboard, contact, about, cart, checkout, and detail pages

## APC Business Context

The target business is APC Shop / ALFA PRO CONCEPT in Bardejov.

Known business inputs from `data_source/presentation/content.md`:

- Founded in 2008
- Focus on ATVs and powersports
- Authorized service for Polaris, CFMOTO, and Indian Motorcycle
- Offers rental, financing, service, and moto school
- Sells higher-end vehicles and machines from brands such as CFMOTO, Indian Motorcycle, Kawasaki, GOES, and Vanderhall

## E-shop Scope

Known categories from `data_source/eshop/categories.md`:

- Machines
- Clothing
- Helmets
- Parts and accessories

This suggests the final site should combine brand/dealer presentation with standard e-shop flows.

## Page Mapping

`data_source/mapping.json` defines how APC content should be placed onto the template pages.

Presentation mapping:

- `home` -> `index.html`
- `about_us` -> `about.html`
- `contact` -> `contact.html`
- `services` -> `ui-elements.html`
- `rental` -> `inventory-list-01.html`
- `financing` -> `faq.html`
- `high_end_products` -> `inventory-sidebar-cards.html`
- `product_detail` -> `inventory-page-single.html`
- `moto_school` -> `blog-list-01.html`

E-shop mapping:

- `home` -> `index-10.html`
- `category_list` -> `shop-list.html`
- `product_detail` -> `shop-single.html`
- `cart` -> `cart.html`
- `checkout` -> `checkout.html`
- `user_dashboard` -> `dashboard.html`
- `inventory` -> `inventory-sidebar-rows.html`

## How To Work In This Repo

- Treat `1.HTML_Template/` as the editable frontend source
- Treat `data_source/` as the source of truth for APC-specific content and structure
- Reuse existing template pages before inventing new page structures
- Prefer adapting static markup and content over introducing build tooling
- When making APC changes, keep template asset paths and global structure intact

## Working Assumption

Unless the user says otherwise, this repository should be approached as a template-customization project:

- replace generic automotive dealer content with APC content
- keep the static HTML architecture
- preserve the original template systems where possible
- use the mapping file as the primary routing/content placement guide
