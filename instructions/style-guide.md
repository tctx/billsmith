# BillSmith UI & UX Style Guide

**Version**: v1.0 — 30 May 2025

This document codifies everything an autonomous AI engineer must know to reproduce a polished, cohesive interface for the entire BillSmith application. It incorporates the requirements, flows, and tasks already defined in the PRD and Development Checklist.

## 0. How to Use This Guide

- **Read top-down**: Earlier sections define branding primitives consumed by later component rules.
- **Never deviate** from tokens, spacing scales, or naming patterns unless this guide explicitly allows overrides.
- **Cross-check** every screen you ship against the Page-by-Page Cues in §11.
- **Lint styles**: run a CSS-formatter with the declared ordering (see §7.2).
- **Accessibility is not optional**: failing WCAG AA is considered a blocking defect (§9).

## 1. Brand Identity

### Core Brand Elements

| Token | Value | Rationale / Usage |
|-------|-------|-------------------|
| **Product Name** | "BillSmith" | Title-case, no spaces. |
| **Voice & Tone** | Clear, concise, quietly confident. Similar to Ramp's understated professionalism. | Avoid exclamation points, marketing fluff, or jokes inside the product UI. |

### Color Palette

#### Primary Palette
- **#222222 (Ink)** - headings & body text
- **#666666 (Graphite)** - secondary text / labels  
- **#F8F9FA (Paper)** - background surfaces

*Rationale: High contrast yet neutral; ideal for document-heavy UI.*

#### Accent Palette (Categories)
- **Dynamically derived** from user-chosen `color_hex`
- **Default**: #2222FF if unspecified
- **Usage**: Only for category badges, chart strokes, and small UI affordances—never for large blocks of text

#### Status Colors
- **Error**: Red #C62828
- **Warning**: Yellow #F9A825  
- **Success**: Green #2E7D32

*Limited to status states & toasts.*

### Typography

**System Font Stack**: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`

*Matches Airbnb's system-font strategy—crisp on every OS.*

### Logo
- Simple word-mark in Ink
- 16 px left margin in header
- Reserve 24 px clear-space on all sides
- No glyphs or mascots until a future marketing refresh

## 2. Spatial System

### 2.1 Grid

#### Desktop
- 12-column CSS Grid
- 72 px max content width per column
- 24 px gutters

#### Tablet  
- 8-column
- 16 px gutters

#### Mobile
- Single column
- 16 px body padding

### 2.2 Spacing Scale

| Token | Rem | Usage |
|-------|-----|-------|
| `--space-0` | 0 | hairline divider offset |
| `--space-1` | 0.25 rem | icon padding, chip gaps |
| `--space-2` | 0.5 rem | small component padding |
| `--space-3` | 0.75 rem | label ↔ input gap |
| `--space-4` | 1 rem | default card padding |
| `--space-6` | 1.5 rem | section separation |
| `--space-8` | 2 rem | major block separation |

### 2.3 Elevation

Replicate Ramp's subtle shadow language:

```css
/* Shadow-100 */
box-shadow: 0 1px 3px rgba(0,0,0,.08);

/* Shadow-200 (hover) */
box-shadow: 0 4px 12px rgba(0,0,0,.10);
```

**Rules**:
- Cards never exceed Shadow-200
- Dialogs use a backdrop blur instead of larger shadows

## 3. Typography

| Role | Weight | Size (rem) | Line-height | Letter-spacing |
|------|--------|------------|-------------|----------------|
| **H1** | 600 | 2.0 | 1.1 | -.01em |
| **H2** | 600 | 1.5 | 1.2 | -.01em |
| **H3** | 600 | 1.25 | 1.25 | -.005em |
| **Body 1** | 400 | 1.0 | 1.5 | 0 |
| **Body 2** (small) | 400 | 0.875 | 1.5 | 0 |
| **Caption** | 400 | 0.75 | 1.4 | 0.02em |
| **Mono** | 500 | 0.875 | 1.4 | 0 |

### Typography Rules
- **Capitalize** buttons and chips sentence-case only (never all caps)
- **Ellipsize** long vendor names at 1 line with `text-overflow: ellipsis;`

## 4. Component Library

### 4.1 Buttons

#### Primary Variant
- **Background**: Ink (#222)
- **Text**: Paper (#FFF)
- **Border-radius**: 6 px
- **Padding**: 0.5 rem 1 rem
- **Hover**: lighten Ink to #333
- **Disabled**: opacity 0.5, cursor not-allowed

#### Secondary Variant  
- **Border**: 1 px Ink
- **Text**: Ink
- **Fill**: transparent
- **Hover**: background rgba(0,0,0,.04)

#### Danger Variant
- **Background**: Error red
- **Text**: #FFF
- **Hover**: Same rule as Primary

### 4.2 Cards
- **Padding**: `var(--space-4)` all around
- **Border**: 1 px #E0E0E0 on Light mode
- **Content ordering**: Title → Supporting text → Actions

### 4.3 Sidebar Category Item

```html
<li class="sidebar__item sidebar__item--active">
  <span class="swatch" style="background:#2222FF"></span>
  <span class="label">Rent</span>
</li>
```

**Active state**: 
- Background #F0F2F5
- Text Ink bold
- 4 px accent bar on left

### 4.4 Badges & Chips
- **Border-radius**: 12 px
- **Padding**: 12 px horizontal
- **Height**: 20 px
- **Background**: accent color at 8% opacity with 1 px solid accent line

### 4.5 Form Inputs
- **Border**: 1 px solid #CCC
- **Radius**: 6 px
- **Focus ring**: 2 px accent color inset shadow (`box-shadow: 0 0 0 2px var(--accent)`)
- **Label**: sits 4 px above input, Body-2 style

### 4.6 Tables
- **Header row**: uses H3 weight 600
- **Row height**: 48 px desktop / 40 px mobile
- **Hover**: row background #FAFAFA
- **Zebra striping**: only for dense search result tables (not on Dashboard docs list)

### 4.7 Modals & Drawers
- **Width**: `min(560 px, 90 vw)`
- **Border-radius**: 12 px
- **Positioning**: vertical centering at 10 vh offset for large screens
- **Close icon**: 24 px clickable area

### 4.8 Toast Notifications
- **Position**: bottom-left corner (mobile: bottom-center)
- **Auto-dismiss**: 5 s
- **Content**: include icon (check, exclamation, x) + short body2 message

## 5. Data Visualization (D3.js)

### Chart Styling
- **Color**: Use category accent for main stroke, 2 px thick
- **Secondary lines**: toned Ink #777 for comparison or future MoM lines
- **Gridlines**: light #EEEEEE, 1 px, vertical lines hidden by default
- **Area Fills**: only for selected category; 4% opacity accent to match screenshot aesthetic

### Interaction
- **Hover**: tooltip with Date & Amount; anchored 12 px above point
- **Mobile**: tap highlights point for 3 s

### Responsiveness
- **Chart container**: maintains 16:9 ratio
- **Tick labels**: auto-rotate to 45° below 500 px width

## 6. Iconography

- **Icon Library**: Lucide icons (MIT-licensed; Feather successor)
- **Stroke width**: 1.5 px to harmonize with Ink typography weight
- **Minimum tap target**: 36 × 36 px even when visual glyph is 16 px
- **Recoloring**: Never recolor icons except for semantic Error/Success contexts

## 7. CSS & Code Standards

### 7.1 File Structure

```
/src
  /css
    styles.css
    tokens.css      /* root :root variables */
    components/
  /js
    api.js
    charts.js
    components/
  index.html
```

### 7.2 CSS Ordering

1. @imports / custom properties
2. Reset / normalization
3. Layout (grid & flex helpers)
4. Components (alphabetical)
5. Utilities

### 7.3 BEM Rules

- **Block**: `.card`
- **Element**: `.card__title`  
- **Modifier**: `.card--compact`

### 7.4 JavaScript

- **ES2022 modules**, top-level import/export
- **Always use** `const` then `let`
- **Arrow functions** preferred for callbacks
- **Utility helpers** live in `/js/utils/`

## 8. Motion & Micro-Interactions

| Interaction | Duration | Easing |
|-------------|----------|---------|
| **Button press** | 120 ms | `cubic-bezier(.4,0,.2,1)` |
| **Modal enter/exit** | 240 ms | same easing |
| **Sidebar expand/collapse** | 180 ms | `ease-out` |
| **Chart point hover grow** | 100 ms | `linear` |

**Animation Rules**:
- Never animate color or letter-spacing
- Animate transform & opacity only to preserve text crispness

## 9. Accessibility Checklist

- ✅ **Color contrast** ≥ 4.5:1 for text < 18 pt
- ✅ **Interactive elements** get `aria-label` or visible text
- ✅ **Custom focusable divs** use `tabindex="0"`
- ✅ **Focus order** follows visual order
- ✅ **Toasts** announced via `aria-live="polite"`
- ✅ **PDF viewer** provides "Download" link (screen-reader discoverable)

## 10. Responsive Rules

| Breakpoint | Sidebar Behaviour | Grid Columns | Font Scaling |
|------------|-------------------|--------------|--------------|
| **≥ 1024 px** | Fixed 240 px rail | 12 | Base scale 1.0 |
| **600–1023 px** | Collapsible rail (burger icon) | 8 | Scale 0.95 |
| **< 600 px** | Dropdown category selector | 1 | Scale 0.9 |

## 11. Page-by-Page Cues

*Below each cue you'll see references to PRD feature IDs (F-xx) and Checklist tasks. Implement screens sequentially to satisfy those specs.*

### 11.1 Login Page (/login)

#### Layout
- Center card max-width 400 px, Shadow-200
- Logo word-mark top-center (`margin-bottom: var(--space-4)`)

#### Interactions
- Validate email on blur
- Shake card 4 px horizontally on invalid submit

**Checklist Alignment** → "Authentication UI" group tasks.

### 11.2 Dashboard Home (/)

- **Header** fixed; use 64 px height. "Add Bill" button = Primary variant + plus icon
- **Left Rail** matches Sidebar Category Item spec; active state syncs with chosen category (F-04)
- **Chart container** 100% width minus 48 px horizontal padding; implement tooltip as described in §5
- **Documents List** uses Table spec row height; "View" triggers inline PDF modal

**Checklist Alignment** → "Dashboard Home Page" & "File Upload Interface".

### 11.3 Bill Detail (/bill/:id)

- **PDF viewer** in right column must maintain 16:21 aspect ratio placeholder skeleton while loading
- **Edit Mode** transitions form fields with opacity fade (120 ms)

**Checklist Alignment** → "Bill Detail Page".

### 11.4 Category Modal

- Use Drawer pattern on mobile (slide up from bottom)
- Save button is disabled until valid name & hex entered

### 11.5 Search Results

- Place sticky sub-header showing current query and result count
- Rows are selectable with space key

### 11.6 Settings

- Accordion chevrons rotate 90° on open
- Sensitive keys (LLM API) hide characters until "Show" clicked

### 11.7 Paywall

- Marketing copy set in H2, body1
- Pricing card floats with Shadow-200
- Stripe button uses hosted checkout style

### 11.8 404

- Illustration 200 px square centered
- "Go Home" Secondary button under message

*(For future Insights page, reuse Dashboard header + left rail; chart grid will follow D3 spec.)*

## 12. Deliverables for Engineering

- ✅ **tokens.css** – All color, spacing, typography custom properties
- ✅ **styles.css** – Core, components, utilities as per ordering (§7.2)
- ✅ **Starter HTML files** with correct semantic structure and BEM classes
- ✅ **D3 helper module** with default theme + tooltip utility
- ✅ **SVG icon sprites** generated from Lucide subset (24 px art-board)