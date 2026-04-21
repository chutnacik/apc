const fs = await import("node:fs/promises");
const path = await import("node:path");
const { Presentation, PresentationFile } = await import("@oai/artifact-tool");

const W = 1280;
const H = 720;

const ROOT = "/Users/jakubchutnak/Sites/apc-html/apc";
const OUT_DIR = path.join(ROOT, "outputs", "apc-eshop-bardejov");
const SCRATCH_DIR = path.join(ROOT, "tmp", "slides", "apc-eshop-bardejov");
const PREVIEW_DIR = path.join(SCRATCH_DIR, "preview");

const HERO_PATH = path.join(ROOT, "images", "APC", "cforce-1000-touring-25-copy-title-copy-1920x938.jpeg");
const COLORS = {
  bg: "#0D0F12",
  panel: "#12161C",
  panelSoft: "#161C24",
  ink: "#F6F1E8",
  muted: "#C7C1B8",
  mutedSoft: "#9AA3AE",
  accent: "#F97316",
  accentSoft: "#FDBA74",
  line: "#2B3440",
  card: "#131920E6",
  white: "#FFFFFF",
};

async function ensureDirs() {
  await fs.mkdir(OUT_DIR, { recursive: true });
  await fs.mkdir(PREVIEW_DIR, { recursive: true });
}

async function readImageBlob(filePath) {
  const bytes = await fs.readFile(filePath);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

function addShape(slide, geometry, position, fill, line = { width: 0, fill: fill || COLORS.bg }) {
  return slide.shapes.add({
    geometry,
    position,
    fill,
    line,
  });
}

function addText(slide, text, position, options = {}) {
  const box = addShape(
    slide,
    "rect",
    position,
    options.fill || "#00000000",
    options.line || { width: 0, fill: "#00000000" },
  );
  box.text = text;
  box.text.fontSize = options.fontSize ?? 20;
  box.text.color = options.color ?? COLORS.ink;
  box.text.bold = Boolean(options.bold);
  box.text.typeface = options.typeface ?? "Lato";
  box.text.alignment = options.align ?? "left";
  box.text.verticalAlignment = options.valign ?? "top";
  box.text.insets = options.insets ?? { left: 0, right: 0, top: 0, bottom: 0 };
  if (options.autoFit) {
    box.text.autoFit = options.autoFit;
  }
  return box;
}

async function addImage(slide, filePath, position, fit = "cover", geometry = undefined) {
  const image = slide.images.add({
    blob: await readImageBlob(filePath),
    alt: path.basename(filePath),
    fit,
    geometry,
  });
  image.position = position;
  return image;
}

function addBulletRow(slide, title, body, x, y, iconText) {
  addShape(
    slide,
    "roundRect",
    { left: x, top: y, width: 356, height: 80 },
    COLORS.card,
    { width: 1, fill: COLORS.line, style: "solid" },
  );
  addShape(
    slide,
    "ellipse",
    { left: x + 18, top: y + 18, width: 42, height: 42 },
    COLORS.accent,
    { width: 0, fill: COLORS.accent },
  );
  addText(slide, iconText, { left: x + 30, top: y + 27, width: 20, height: 20 }, {
    fontSize: 13,
    color: COLORS.white,
    bold: true,
    typeface: "Poppins",
    align: "center",
    valign: "middle",
  });
  addText(slide, title, { left: x + 78, top: y + 16, width: 250, height: 22 }, {
    fontSize: 16,
    color: COLORS.white,
    bold: true,
    typeface: "Poppins",
  });
  addText(slide, body, { left: x + 78, top: y + 40, width: 250, height: 28 }, {
    fontSize: 12,
    color: COLORS.muted,
    typeface: "Lato",
  });
}

function addTag(slide, text, left, top, width) {
  addShape(
    slide,
    "roundRect",
    { left, top, width, height: 34 },
    "#1B232CF0",
    { width: 1, fill: "#32404F", style: "solid" },
  );
  addText(slide, text, { left: left + 16, top: top + 8, width: width - 32, height: 18 }, {
    fontSize: 12,
    color: COLORS.accentSoft,
    bold: true,
    typeface: "Poppins",
    align: "center",
    valign: "middle",
  });
}

async function buildSlide() {
  const presentation = Presentation.create({ slideSize: { width: W, height: H } });
  const slide = presentation.slides.add();

  slide.background.fill = COLORS.bg;

  await addImage(slide, HERO_PATH, { left: 566, top: 0, width: 714, height: 720 }, "cover");

  addShape(slide, "rect", { left: 0, top: 0, width: 1280, height: 720 }, "#090B0ECC", { width: 0, fill: "#090B0ECC" });
  addShape(slide, "rect", { left: 0, top: 0, width: 660, height: 720 }, "#0A0D11F2", { width: 0, fill: "#0A0D11F2" });
  addShape(slide, "rect", { left: 566, top: 0, width: 200, height: 720 }, "#0A0D11AA", { width: 0, fill: "#0A0D11AA" });

  addShape(
    slide,
    "roundRect",
    { left: 46, top: 42, width: 1188, height: 636 },
    "#0E1319AA",
    { width: 1, fill: "#222B35", style: "solid" },
  );

  addShape(slide, "rect", { left: 76, top: 88, width: 4, height: 478 }, COLORS.accent, { width: 0, fill: COLORS.accent });
  addText(slide, "APC SHOP", { left: 88, top: 60, width: 180, height: 30 }, {
    fontSize: 22,
    color: COLORS.white,
    bold: true,
    typeface: "Poppins",
    autoFit: "shrinkText",
  });

  addTag(slide, "SHOWROOM + SERVIS + E-SHOP", 88, 154, 272);

  addText(slide, "Showroom, servis a e-shop v Bardejove", { left: 88, top: 210, width: 430, height: 116 }, {
    fontSize: 31,
    color: COLORS.ink,
    bold: true,
    typeface: "Poppins",
  });

  addText(slide, "Všetko pre jazdcov na jednom mieste", { left: 88, top: 336, width: 410, height: 66 }, {
    fontSize: 24,
    color: COLORS.accentSoft,
    bold: true,
    typeface: "Poppins",
  });

  addText(
    slide,
    "Od strojov a výbavy až po servisné zázemie. APC v Bardejove spája fyzický showroom s online ponukou, aby si mal nákup aj podporu na jednom mieste.",
    { left: 88, top: 410, width: 430, height: 72 },
    {
      fontSize: 15,
      color: COLORS.muted,
      typeface: "Lato",
    },
  );

  addShape(
    slide,
    "roundRect",
    { left: 88, top: 508, width: 224, height: 52 },
    COLORS.accent,
    { width: 0, fill: COLORS.accent },
  );
  addText(slide, "Prezrieť ponuku", { left: 88, top: 522, width: 224, height: 20 }, {
    fontSize: 17,
    color: COLORS.white,
    bold: true,
    typeface: "Poppins",
    align: "center",
    valign: "middle",
  });

  addShape(
    slide,
    "roundRect",
    { left: 770, top: 74, width: 414, height: 196 },
    "#10151CDD",
    { width: 1, fill: "#2A333E", style: "solid" },
  );
  addText(slide, "E-shop pre jazdcov", { left: 802, top: 102, width: 220, height: 28 }, {
    fontSize: 20,
    color: COLORS.white,
    bold: true,
    typeface: "Poppins",
  });
  addText(slide, "Prilby, oblečenie, doplnky, diely a mazivá", { left: 802, top: 138, width: 300, height: 40 }, {
    fontSize: 14,
    color: COLORS.muted,
    typeface: "Lato",
  });

  addTag(slide, "Prilby", 802, 196, 92);
  addTag(slide, "Oblečenie", 904, 196, 118);
  addTag(slide, "Diely", 1032, 196, 84);
  addTag(slide, "Doplnky", 802, 238, 106);
  addTag(slide, "Mazivá", 918, 238, 92);
  addTag(slide, "Servis", 1020, 238, 96);

  addBulletRow(slide, "Showroom", "Stroje, výbava a poradenstvo priamo na predajni.", 74, 576, "01");
  addBulletRow(slide, "Servis", "Objednanie servisu a zázemie pre ďalšiu starostlivosť.", 454, 576, "02");
  addBulletRow(slide, "E-shop", "Rýchla cesta k ponuke aj mimo showroomu.", 834, 576, "03");

  slide.speakerNotes.setText(
    [
      "APC e-shop / showroom slide",
      "",
      "Sources:",
      "- /Users/jakubchutnak/Sites/apc-html/apc/apc-homepage.html",
      "- /Users/jakubchutnak/Sites/apc-html/apc/images/APC/cforce-1000-touring-25-copy-title-copy-1920x938.jpeg",
    ].join("\n"),
  );

  return presentation;
}

async function saveBlob(blob, filePath) {
  const bytes = new Uint8Array(await blob.arrayBuffer());
  await fs.writeFile(filePath, bytes);
}

async function main() {
  await ensureDirs();
  const presentation = await buildSlide();
  const preview = await presentation.export({ slide: presentation.slides.items[0], format: "png", scale: 1 });
  await saveBlob(preview, path.join(PREVIEW_DIR, "slide-01.png"));
  const pptxBlob = await PresentationFile.exportPptx(presentation);
  await pptxBlob.save(path.join(OUT_DIR, "output.pptx"));
  console.log(path.join(OUT_DIR, "output.pptx"));
}

await main();
