# Project Overview: Boxcar HTML Template

This is a comprehensive Automotive & Car Dealer HTML5 template. It is built using standard web technologies (HTML, CSS, JS) and follows a multi-page architecture.

## Directory Structure

- `1.HTML_Template/`: The main source code for the template.
  - `css/`: Stylesheets including Bootstrap, Slick, and the main `style.css`.
  - `js/`: JavaScript files including jQuery, Bootstrap plugins, and the main `main.js`.
  - `images/`: All image assets (icons, backgrounds, resource images).
  - `fonts/`: Icon fonts and local font files.
  - `*.html`: Individual pages of the template (Home variations, Inventory, Blog, Shop, etc.).
- `2.Documentation/`: User guide and technical documentation for the template.
- `3.Licensing/`: License information.

## Core Technologies & Libraries

- **Framework:** Bootstrap (v5.x based on the documentation/structure).
- **Core Library:** jQuery.
- **Sliders:** Slick Slider.
- **Animations:** WOW.js (using `data-wow` attributes) and Animate.css.
- **Icons:** Font Awesome, Flaticon, Linearicons, Feather Icons (in documentation).
- **Navigation:** Mmenu (for mobile/sidebar navigation).
- **Gallery/Lightbox:** Fancybox.
- **Filtering:** MixItUp (likely for inventory/shop filtering).

## Development Guidelines

### 1. Modifying Styles
- The primary stylesheet is `1.HTML_Template/css/style.css`.
- Although the documentation mentioned SASS/Gulp source files, they are not present in this distribution. Edit `style.css` directly for any custom styling.
- Use Bootstrap utility classes whenever possible to maintain consistency.
- Helper classes for margins (`mt-20`), paddings (`pt-20`), and typography (`text-16`) are available and documented in `2.Documentation/index.html`.

### 2. Modifying Logic
- Custom JavaScript functionality is located in `1.HTML_Template/js/main.js`.
- Most components (sliders, animations) are initialized here.
- When adding new components, follow the existing initialization patterns in `main.js`.

### 3. Adding New Pages
- Use `index.html` or `about.html` as a starting point for new pages to ensure correct header/footer and asset linking.
- Ensure the `boxcar-wrapper` div is present as the main container.

### 4. Animations
- Use `data-wow-delay` and `wow fadeInUp` (or other WOW.js classes) for scroll-triggered animations.
- The documentation also mentions `data-anim` attributes for a custom animation system; check `main.js` to see which is actively used in the current version.

### 5. Images and Assets
- Place new images in `1.HTML_Template/images/resource/` or relevant subfolders.
- Use SVGs for icons where possible (already heavily used in the header).

## Important Notes
- This is a **static HTML template**, not a WordPress theme.
- Images in the preview are often placeholders; check `images/resource` for available assets.
- Responsive design is handled by Bootstrap and custom media queries in `style.css`.
