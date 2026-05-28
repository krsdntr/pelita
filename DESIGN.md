# Design System Specification: The Sacred Library

## 1. Overview & Creative North Star: "The Digital Sanctuary"
This design system is built upon the North Star of **"The Digital Sanctuary."** Unlike standard utility-first apps, this system prioritizes the "Sanctity of Space." It rejects the cluttered, boxy nature of modern web interfaces in favor of an editorial, high-end experience that feels like a physical library transition—moving from the rich, tactile warmth of a study (The Bookshelf) to the pure, silent focus of a reading room (The Reader).

To achieve this, we employ **Intentional Asymmetry** and **Tonal Depth**. Navigation elements are offset to allow the scripture to breathe, and we utilize a "No-Line" philosophy to ensure the interface never feels like a grid of constraints, but rather a flow of wisdom.

---

## 2. Colors: Tonal Transitions
The palette is rooted in Earth-tones and organic transitions. We move from deep, "Primary" wood tones to "Surface" tones that mimic fine vellum and parchment.

### The Color Tokens
*   **Primary (#442a22):** The "Mahogany" base. Used for the most significant actions and the weight of the bookshelf.
*   **Surface (#faf9f8):** The "Parchment" base. A warm off-white that reduces eye strain compared to pure hex white.
*   **Tertiary (#373023):** The "Ink" base. Used for deep contrast in "Dark" modes or high-importance typography.

### Layout Rules
*   **The "No-Line" Rule:** 1px solid borders are strictly prohibited for sectioning. Use background shifts: a `surface-container-low` component should sit on a `surface` background to define its bounds.
*   **Surface Hierarchy:** Use `surface-container-lowest` for the main reading canvas and `surface-container-high` for elevated UI elements like floating navigation bars.
*   **The "Glass & Gradient" Rule:** Floating customization menus must use Glassmorphism. Apply `surface-variant` at 70% opacity with a `24px` backdrop blur. Use a subtle linear gradient (from `primary` to `primary-container`) on progress bars to give them a liquid, organic feel.

---

## 3. Typography: The Editorial Voice
We utilize a high-contrast pairing: **Newsreader** (Serif) for the timelessness of scripture and **Inter** (Sans-serif) for the precision of the UI.

*   **Display-LG (Newsreader, 3.5rem):** For book titles and chapter headers. Use with `-0.02em` letter spacing for a "Custom Press" look.
*   **Title-LG (Newsreader, 1.375rem):** For verse highlights. This is the "Voice of Authority."
*   **Body-LG (Newsreader, 1rem):** The standard reading size. Line height must be set to `1.6` to ensure the "Sanctuary" feels spacious.
*   **Label-MD (Inter, 0.75rem):** For UI metadata, progress percentages, and navigation labels. All-caps with `0.05em` letter spacing.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are too aggressive for a spiritual context. We use "Ambient Light" principles.

*   **The Layering Principle:** Stack your containers. A card (Surface-Container-Lowest) sits on a section (Surface-Container-Low), which sits on the Page (Surface). This creates a "Natural Lift."
*   **Ambient Shadows:** For floating elements like the "Verse Share" modal, use a shadow with `0px 20px 40px` blur at 6% opacity using the `on-surface` color. It should feel like a cloud casting a shadow, not a plastic box.
*   **The Ghost Border:** If a boundary is required for accessibility (e.g., in Dark Mode), use `outline-variant` at 15% opacity. Never use 100% opacity.

---

## 5. Components: Custom Interaction

### The Bookshelf Card
*   **Structure:** No borders. Use `surface-container` with a `xl (0.75rem)` corner radius. 
*   **Visual:** Apply a subtle vertical gradient to mimic the spine of a book. The "Progress" is a 4px line at the very bottom of the card using the `primary` color.

### Instagram-Style Progress Bars
*   **Implementation:** Segmented bars for daily reading streaks.
*   **Styling:** Use `surface-variant` for the track and a gradient of `primary` to `secondary` for the fill. Roundedness must be `full`.

### Customization Sliders
*   **The Track:** 4px height, `surface-container-highest`.
*   **The Thumb:** A 20px circle in `primary`. No shadow; instead, use a 4px "halo" of `primary` at 10% opacity.

### Gamification Badges
*   **Style:** Minimalist linework. Avoid "game-like" bright colors. Use `tertiary` for the icon and `tertiary-fixed-dim` for the badge container. 
*   **Shape:** Use an "Organic Circle" (slightly irregular border-radius) to feel hand-stamped rather than factory-made.

### Input Fields
*   **Style:** Forbid the 4-sided box. Use a "Bottom-Only" line approach or a soft-filled `surface-container-low` with no border. Focus state is indicated by the line expanding from the center.

---

## 6. Do’s and Don’ts

### Do:
*   **Embrace Negative Space:** If a screen feels "empty," leave it. Space is a feature of focus.
*   **Verticality:** Allow scripture to flow vertically. Avoid horizontal paginated swiping which breaks the editorial "scroll" feel.
*   **Tonal Consistency:** Ensure the "Pastel Mode" uses the same `surface-container` logic, just swapped for soft hues (e.g., `primary-fixed-dim`).

### Don’t:
*   **Don’t use Dividers:** Never use a horizontal line to separate verses or menu items. Use `24px` of vertical white space instead.
*   **Don’t use Pure Black:** In Dark Mode, use `inverse-surface` as the deepest tone. Pure black (#000) feels "hollow" and tech-focused; we want "deep ink."
*   **Don’t use Standard Shadows:** Avoid the `0px 2px 4px` default. It looks "Bootstrap" and cheapens the premium feel.