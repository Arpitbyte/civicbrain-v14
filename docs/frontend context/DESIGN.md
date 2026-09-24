# DESIGN.md — CivicBrain Canonical Design System

> Single source of truth for every visual decision in CivicBrain. Components and
> Antigravity prompts cite this document by section; they do not restate it.
> Product/backend facts live in `FRONTEND_CONTEXT.md`. Screen inventory lives in
> `SCREEN_SPECS.md`. This file only changes when a real design decision changes.

---

## DESIGN DNA (read this first, every session)

**Concept — The Benchmark.** A surveyor's benchmark is a fixed, verified reference
point that every other measurement is checked against. CivicBrain does the same thing
to civic reports: it takes uncertain, scattered citizen complaints and turns them into
a verified, located, appealable point of record. Every visual decision reinforces this:
things that are *verified* look stamped/sealed; things that are *uncertain* look
provisional/pending; things that are *located* are tied to a coordinate, a map, a ward.

**Palette vocabulary is fieldwork, not SaaS**: `Field` (paper/daylight neutrals),
`Station` (survey-ink dark), `Marker` (survey-orange, primary action), `Channel`
(river-teal, spatial/GIS), `Seal` (verification green), `Flag` (amber/red, hazard).
No blue-purple AI gradient anywhere in the product.

**Type is one coherent multi-script family, plus one rare accent.** IBM Plex Sans (UI),
IBM Plex Mono (data/coordinates/IDs), IBM Plex Sans Devanagari (Hindi companion) — one
designed system, one foundry, genuinely multi-script. Fraunces is the single accent
serif, used only for the highest-trust editorial moments (Transparency Board, ward
report cards) — rare on purpose, never a body font.

**Tokens are four layers**: primitive → semantic → component → workspace-theme.
Components touch semantic tokens only. A full re-theme = editing files in
`tokens/themes/`, nothing else.

**One product, seven registers**: Nagrik Setu (warm, spacious, low density) → Command
Deck (dense, quiet-motion, table-first) → Ops Board (dense, departmental) → City Pulse
(spatial, GSAP-eased map reveals) → Karmi Sahayak (tactile, hi-vis, offline-aware) →
Control Room (flat, administrative, zero decoration) → Transparency Board (editorial,
stamped-ledger, Lenis scroll). Same tokens, same components, different theme file and
different motion budget per workspace.

**Motion has three levels**: Quiet (operational tools, near-zero decoration), Responsive
(interaction feedback, everywhere), Expressive (public/read-once surfaces only —
Nagrik Setu key moments, City Pulse spatial reveal, Transparency Board scroll).

**Confidence and evidence are never decorative.** No fake AI confidence, no decorative
charts, no loading animation implying work the backend isn't actually doing.

**Banned by default**: Inter, blue-purple gradients, glassmorphism, neon glow, floating
blobs, icon-in-square-above-heading grids, generic rounded-card walls, meaningless
parallax, stock photography. Full list in §14. Rule: *reject a pattern because it's
unearned, not because it's trendy.*

---

## 1. Art direction — The Benchmark

CivicBrain's job is to convert **uncertain, multi-channel civic noise into a verified,
located, appealable record.** That is the entire emotional and visual thesis. Everything
in the product exists on a spectrum from *unverified field note* to *stamped public
record*, and the UI should make that spectrum legible at a glance — not through a badge
system bolted on afterward, but through surface treatment itself: provisional content
looks like a field sketch (thin borders, mono captions, muted); confirmed content looks
like a survey stamp (a sealed edge, a green mark, a permanent-feeling border weight).

This is stronger than a generic "civic tech" or "smart city" look because it's derived
from what the product actually *does* (establish verified reference points from
uncertain reports) rather than what it looks like (maps, dashboards). Competing
directions considered and rejected:
- **Generic gov-portal (GOV.UK-style)** — communicates trust through blandness. Correct
  for a regulator, wrong for a product that wants people to *want* to check their ward's
  ledger. Rejected.
- **Smart-city futurism (dark dashboards, glowing data)** — implies sensor/AI capability
  CivicBrain explicitly doesn't have yet (Bootstrap Principle). Would misrepresent the
  product. Rejected.
- **Editorial/documentary (chosen, evolved)** — treats civic data the way a serious
  newsroom or an ordnance survey office treats a public record: legible, sourced,
  confident, slightly tactile. This is the direction, and Benchmark is its name.

Target feel: contemporary, editorial, spatially literate, quietly tactile, civic without
looking governmental, premium without looking like a luxury brand, technical without
looking cyberpunk.

## 2. Visual variation by workspace

One shared DNA, seven contextual expressions. All seven use the same token layers and
component library — only the theme file, density defaults, and motion budget change.

| Workspace | Density | Typography behavior | Imagery | Interaction style | Motion | Surface treatment | Hierarchy | Spatial metaphor |
|---|---|---|---|---|---|---|---|---|
| **Nagrik Setu** | Low, spacious, 720px reading column | Plex Sans body, Fraunces for the 2–3 highest-trust moments (report confirmed, ledger entry created) | Citizen's own evidence photos, full-bleed evidence cards | Large touch targets, one primary action per screen, step-by-step flow | Expressive at key moments only (submission success, status change) | Field paper surfaces, soft single-elevation cards | One task at a time, status always visible | The tracking token *is* the artifact — styled as a field waybill stub |
| **Command Deck** | High, table-dense, 1280px+ | Plex Sans UI, Plex Mono for every score/ID/timestamp | Evidence thumbnails inline in rows, full view on demand | Keyboard-navigable queue, inline expand for score breakdown | Quiet — instant state swaps, <150ms | Station-ink chrome, optional dark "night ops" mode | Priority score is the primary sort axis, always itemized | A stamped ledger line per incident |
| **Ops Board** | High, departmental | Same as Command Deck, dept-color chip accents | Work-order evidence, before/after pairs | Assign/claim actions from the queue row | Quiet | Field paper (lighter than Command Deck — one department, less alarm) | SLA timer is the dominant visual weight | A clipboard — subtle top-binding rule motif on queue cards |
| **City Pulse** | Medium, map-first | Plex Sans for panels, Plex Mono for coordinates/cluster stats | The map itself is the imagery; no other photography | Click/hover map interaction, cross-filter panels | Expressive for map only — GSAP cluster reveal, layer cross-fade | Channel-teal chrome around a Field-paper map frame | Spatial pattern first, list second | Coordinate ruler ticks along the map frame edge |
| **Karmi Sahayak** | Low, single-task, full-screen steps | Plex Sans only, larger scale (outdoor legibility) | Camera capture is the primary interaction, not a gallery | One thumb, bottom-anchored primary action, large targets (≥48px) | Minimal, fast, no easing flourish | Near-black Station surface, Marker-amber accents (hi-vis) | Current task fills the screen; nothing else competes | A hi-vis vest, not a dashboard |
| **Control Room** | High, form-dense | Plex Sans + Plex Mono for config values | None — administrative screens don't need imagery | Explicit save/confirm, no destructive action without a typed confirmation | None beyond native focus/hover | Flat Field-paper, zero accent color, monochrome Station text | Every field labeled, no icon-only controls | A registry ledger book, not a dashboard |
| **Transparency Board** | Low, editorial, 720px column | Fraunces headlines over Plex Sans body; Plex Mono for ledger hashes/IDs | City-wide aggregate imagery (maps, ward outlines) only — never staged photography | Read-mostly, scroll-driven, search as the one input-heavy surface | Expressive — Lenis smooth scroll, restrained scroll reveals | Field paper with a Seal-green stamp motif on verified entries | The ledger entry is the unit, always chronological | A public notice board / stamped audit trail |

## 3. Design tokens — four layers

```
tokens/primitives.css        raw scales, no meaning
tokens/semantic.css          meaning, workspace-agnostic
tokens/components/*.css      component-scoped tokens, reference semantic only
tokens/themes/*.css          per-workspace overrides of semantic tokens only
```

Rule, absolute: **components reference semantic tokens only.** A component file never
contains a hex value, a raw font name, or a raw pixel shadow. If a value is truly local
to one component and will never be reused or reskinned (e.g. a 1px hairline inside a
specific icon), it may be hardcoded — document why in a comment.

### 3.1 Primitive palette

| Family | Role | Scale | Anchor value |
|---|---|---|---|
| `--field-*` | Paper/daylight neutrals | 0–950 | `--field-50: #F7F4EE` (base bg) · `--field-950: #17140F` |
| `--station-*` | Survey-ink dark, staff chrome / night-ops dark mode | 0–950 | `--station-900: #1B2024` · `--station-500: #4A555C` |
| `--marker-*` | Survey/field orange — primary action, citizen accent | 100–900 | `--marker-500: #C1592B` |
| `--channel-*` | River-teal — spatial/GIS accent | 100–900 | `--channel-500: #2E6E6B` |
| `--seal-*` | Verification green | 100–900 | `--seal-500: #3C7A4B` |
| `--flag-amber-*` / `--flag-red-*` | Hazard/warning/danger (flagging-tape colors) | 100–900 | `--flag-amber-500: #D98E04` · `--flag-red-500: #B3311F` |

### 3.2 Semantic tokens (full mapping in `tokens/semantic.css`; representative set)

```css
--color-background          var(--field-50)
--color-surface              var(--field-100)
--color-surface-raised       var(--field-0)
--color-border               var(--field-300)
--color-border-strong        var(--station-500)
--color-text-primary         var(--station-900)
--color-text-secondary       var(--station-600)
--color-text-inverse         var(--field-50)
--color-action-primary       var(--marker-500)   /* citizen apps default */
--color-action-secondary     var(--station-700)
--color-focus                var(--channel-600)
--color-status-success       var(--seal-500)
--color-status-warning       var(--flag-amber-500)
--color-status-danger        var(--flag-red-500)
--color-status-info          var(--channel-500)
--color-confidence-low       var(--flag-amber-500)   /* never red — low confidence isn't an error */
--color-confidence-medium    var(--marker-400)
--color-confidence-high      var(--seal-500)
--color-verified-seal        var(--seal-600)
--color-priority-1           var(--marker-200)   /* low */
--color-priority-2           var(--marker-400)
--color-priority-3           var(--marker-600)
--color-priority-4           var(--marker-800)   /* critical */
--color-gis-incident-point   var(--marker-500)
--color-gis-cluster-fill     var(--marker-500)   /* opacity scales with density, see §3.4 */
--color-gis-ward-boundary    var(--station-500)
--color-gis-causal-edge      var(--channel-600)
--color-gis-selected-ring    var(--seal-500)
```

### 3.3 Typography, spacing, radius, borders, shadows, elevation, opacity, motion, z-index

```css
/* type scale — mobile → desktop pair, fluid via clamp() */
--font-family-ui        "IBM Plex Sans", "Segoe UI", sans-serif
--font-family-mono      "IBM Plex Mono", ui-monospace, monospace
--font-family-devanagari "IBM Plex Sans Devanagari", sans-serif
--font-family-display   "Fraunces", Georgia, serif       /* rare — §6 */

--text-xs:   clamp(0.75rem, 0.72rem + 0.1vw, 0.8125rem)
--text-sm:   clamp(0.8125rem, 0.78rem + 0.12vw, 0.875rem)
--text-base: clamp(0.9375rem, 0.9rem + 0.15vw, 1rem)
--text-lg:   clamp(1.0625rem, 1rem + 0.25vw, 1.1875rem)
--text-xl:   clamp(1.25rem, 1.15rem + 0.4vw, 1.5rem)
--text-2xl:  clamp(1.625rem, 1.4rem + 0.9vw, 2.25rem)
--text-3xl:  clamp(2.125rem, 1.7rem + 1.8vw, 3.25rem)   /* Fraunces display only */

--space-1: 4px  --space-2: 8px  --space-3: 12px  --space-4: 16px
--space-5: 20px --space-6: 24px --space-8: 32px  --space-10: 40px
--space-12: 48px --space-16: 64px --space-20: 80px --space-24: 96px --space-32: 128px

--radius-sm: 4px    /* inputs, chips */
--radius-md: 8px    /* cards, buttons */
--radius-lg: 12px   /* modals, sheets */
--radius-xl: 16px   /* full-screen mobile sheets only */
--radius-full: 999px  /* status chips ONLY — the one pill exception */

--shadow-flat: none
--shadow-lifted: 0 8px 24px -12px rgba(23,20,15,0.18)
--shadow-overlay: 0 16px 48px -16px rgba(23,20,15,0.28)   /* modals/sheets only */

--z-base: 0 --z-sticky: 10 --z-dropdown: 20 --z-scrim: 30 --z-modal: 40
--z-toast: 50 --z-tooltip: 60

--opacity-disabled: 0.4 --opacity-muted: 0.65 --opacity-scrim: 0.5
--opacity-hover-tint: 0.08 --opacity-press-tint: 0.14

--duration-instant: 100ms --duration-fast: 150ms --duration-base: 220ms
--duration-slow: 360ms --duration-deliberate: 600ms
--ease-standard: cubic-bezier(.2,0,0,1)
--ease-decelerate: cubic-bezier(0,0,0,1)
--ease-accelerate: cubic-bezier(.4,0,1,1)
--ease-spatial: cubic-bezier(.16,1,.3,1)   /* GSAP map/expressive moments only */

--control-height-sm: 32px --control-height-md: 40px --control-height-lg: 48px
--icon-size-sm: 16px --icon-size-md: 20px --icon-size-lg: 24px --icon-size-xl: 32px

--content-width-narrow: 720px   /* Nagrik Setu, Transparency Board reading column */
--content-width-form: 560px
--content-width-console: none   /* fluid, min 1280px */
```

### 3.4 Map-specific tokens

```css
--map-point-radius-incident: 6px
--map-point-radius-cluster: clamp(8px, calc(8px + sqrt(var(--cluster-count)) * 1.5px), 28px)
--map-line-ward-boundary: 1.5px dashed var(--color-gis-ward-boundary)
--map-basemap-style: "civicbrain-field"   /* custom muted vector style, Field/Station
   palette — never a default bright OSM/Mapbox style. Provider UNKNOWN, see
   UI_ARCHITECTURE.md §10; style spec can be finalized independent of provider. */
```
Cluster radius is a real function of point count — never a decorative fixed size.

## 4. Theme-swap architecture

A full re-theme means editing files in `tokens/themes/` only:
`tokens/themes/nagrik-setu.css`, `command-deck.css`, `city-pulse.css`, etc. — each
overrides a subset of §3.2 semantic tokens (accent, surface warmth, border weight) and
nothing else. Primitives (§3.1) rarely change; component tokens (radius, height, shadow
shape) almost never change per-theme — only per global redesign.

**Business logic never reads a token.** A component checks `incident.status ===
'resolved'` to decide *what* to render (a `StatusTimeline` step, a `ScoreBreakdown`
value); it never checks a token to decide business behavior. Conversely, no component
hardcodes `if (workspace === 'karmi-sahayak') fontSize = 18` — that belongs in
`tokens/themes/karmi-sahayak.css` as a semantic-token override, applied automatically by
theme context. This separation is what makes "change a few files, whole product
re-skins" true.

## 5. Color — every color has a job

| Token | Job | Never used for |
|---|---|---|
| `color-action-primary` (Marker) | The one primary action per screen | Decoration, large background fills |
| `color-action-secondary` (Station) | Secondary/staff actions | Citizen primary CTAs |
| `color-status-success/warning/danger/info` | System-state feedback only | Priority ranking, brand decoration |
| `color-confidence-*` | Confidence bands, always paired with the numeric Z value and a text label | Standalone meaning — color is never the only signal (§12) |
| `color-priority-1..4` (single-hue Marker scale) | Priority rank only — deliberately *not* red/amber/green so it never reads as good/bad | Status or confidence |
| `color-verified-seal` (Seal green) | The verification/stamped mark specifically | General success toasts (use `color-status-success`, same hue family but distinct token so verification always reads as structurally different from a transient toast) |
| `color-gis-*` | Map layers only | UI chrome outside the map |

Contrast: body text on `color-background`/`color-surface` ≥ 7:1 (exceeds AA); UI labels
≥ 4.5:1 minimum; Karmi Sahayak overrides all text/control contrast to ≥ 7:1 unconditionally
for outdoor use. No status or priority meaning is ever color-only — always paired with a
label, icon, or position (see §12).

## 6. Typography

**System**: IBM Plex Sans (UI/body) + IBM Plex Mono (data) + IBM Plex Sans Devanagari
(Hindi companion) — one open-source (OFL) multi-script family, chosen specifically over
a patchwork of separate foundries because CivicBrain is genuinely multilingual and needs
its Latin and Devanagari type to share one design language, not just a similar x-height.
Plus **Fraunces** as a single rare display accent (§2 table — Nagrik Setu key moments,
Transparency Board headlines, ward report card titles only; never body copy, never
buttons, never more than one Fraunces element per screen).

| Role | Family | Weights used | Notes |
|---|---|---|---|
| UI/body | IBM Plex Sans | 400, 500, 600 | Default everywhere |
| Data/coordinates/IDs/timestamps/scores | IBM Plex Mono | 400, 500 | Tabular figures on, always — a score column must align |
| Hindi UI/body | IBM Plex Sans Devanagari | 400, 500, 600 | Weight-matched pairing with Plex Sans |
| Editorial display (rare) | Fraunces (variable, opsz+wght+SOFT axes) | 400–600, opsz 72+ at display sizes | Ward report card titles, ledger section headers, Nagar Pragati headline number's *label* (the number itself is always Plex Mono) |

Scale: see `--text-*` tokens §3.3, fluid via `clamp()` so mobile and desktop share one
declaration. Paragraph width capped at `--content-width-narrow` (720px, ~68–75 characters
per line). Line-height: 1.5 for body, 1.2 for UI labels/buttons, 1.1 for Fraunces
display. Tracking: 0 for body, +0.01em for all-caps micro-labels (used sparingly — status
chips only, never section headers). Numerals: tabular lining figures (Plex Mono) in every
table, score, timestamp, and coordinate — proportional oldstyle never used for data.

## 7. Imagery

Every image in the product is real evidence or real geography — never decoration.

- **Evidence photography** (citizen/field-worker submitted): 4:3 or native aspect,
  never force-cropped to a square; shown full width within a bordered evidence card, not
  a rounded thumbnail; GPS + timestamp burned into a Plex Mono caption strip *below* the
  photo, never overlaid on top of it; a redaction badge (small Seal-outline icon) when
  face/plate blurring was applied; before/after pairs shown at equal size, side by side
  on tablet+, stacked on mobile.
- **Maps**: the only other imagery class. Custom-styled muted vector basemap (`--map-
  basemap-style`) — never a default bright basemap; ward boundaries, incident points,
  and clusters are the "photography" of City Pulse and the Transparency Board.
- **No stock photography anywhere in the product.** If a screen needs an image and no
  real evidence/map data exists for it (e.g. an empty state), use a typographic or
  line-icon treatment from the custom icon set (§DESIGN §8), never a placeholder photo.
- **Loading/fallback**: evidence photos use a blurred low-res placeholder generated from
  the actual uploaded image (never a generic gray box or a skeleton shimmer standing in
  for content that has real pixels to show); below-the-fold evidence lazy-loads;
  responsive `srcset` at 3 widths (thumbnail/card/full).

## 8. Component language

Structure follows content — not every surface is a rounded card.

| Component | Grammar |
|---|---|
| Buttons | `radius-md`, height sm/md/lg per §3.3; primary = filled `action-primary`; secondary = 1px border, transparent fill; destructive requires typed confirmation for irreversible actions (Control Room) |
| Links | Underline on hover only in body copy; nav links use weight change, not underline |
| Inputs/Select/Search | `radius-sm`, 1px `color-border`, focus = 2px `color-focus` ring offset 2px, never a color-only invalid state (icon + message) |
| Navigation | Staff consoles: persistent left rail, icon+label, current workspace always visible; Nagrik Setu: bottom tab bar (mobile-first); Transparency Board: simple top nav, no mega-menu |
| Tabs | Underline-indicator style, not pill/segmented-control unless genuinely 2-option toggle |
| Cards | Used only for discrete, comparable items (a work-order summary, a ward tile) — never as a generic content wrapper. `radius-md`, `shadow-flat` default, `shadow-lifted` on focus/active only |
| Tables | The primary pattern for Command Deck/Ops Board/Control Room — not cards-pretending-to-be-tables. Sticky header, mono numerals, row-level keyboard nav |
| List rows | Transparency Board ledger, work-order queues on mobile — hairline divider, no card shadow |
| Drawers | Right-side, for "more detail without leaving the list" (incident quick-view from Command Deck queue) |
| Dialogs | Center-modal, `shadow-overlay`, `radius-lg`, used only for genuinely blocking decisions (adjudication, destructive confirm) |
| Sheets | Bottom sheet on mobile (`radius-xl` top corners), replaces dialogs on Nagrik Setu/Karmi Sahayak |
| Maps/Markers | See §3.4. Markers scale by real count/severity, never decorative |
| Badges/Status indicators | Text + icon + color always together, never color chip alone |
| Timelines | `StatusTimeline` — the 11-state lifecycle, one instance per observation, never collapsed (§FRONTEND_CONTEXT §4) |
| Evidence galleries | Full-width evidence cards per §7, stacked, not a cropped thumbnail grid |
| Score breakdowns | `ScoreBreakdown` — expandable, itemized AHP criteria + equity boost + confidence Z, mono numerals, always |
| Charts | Real data only, axis-labeled, mono numerals; no chart exists without a fetched dataset behind it |
| Tooltips | Instant on focus, 150ms delay on hover, never carry information unavailable elsewhere (a11y) |
| Toast/Notifications | Bottom-center on mobile, bottom-right on desktop, `duration-slow` auto-dismiss for info, manual dismiss for anything actionable |
| Empty states | Specific to what's missing ("No incidents in this ward yet" not "No data"), never a generic illustration |
| Loading states | See §10 — never a bare generic spinner if a more honest pattern exists |
| Errors | Plain language + the actual next step, never a raw API error string surfaced to citizens |
| Confirmation states | A `Seal`-styled confirmation for verified/committed actions, distinct from a generic success toast |

## 9. Motion system

| Level | Where | Duration/easing | Examples |
|---|---|---|---|
| **Quiet** | Command Deck, Ops Board, Control Room, Karmi Sahayak — tools touched all day | `duration-instant`/`fast`, `ease-standard` only | Row expand, tab switch, status update — opacity/height change, no slide/bounce |
| **Responsive** | Everywhere, all workspaces | `duration-fast`, `ease-standard` | Button press (scale 0.98), hover tint, focus ring (instant), input validation feedback |
| **Expressive** | Nagrik Setu key moments, City Pulse map, Transparency Board scroll | `duration-slow`/`deliberate`, `ease-spatial`, GSAP/Lenis | Report-submitted confirmation, DBSCAN cluster reveal, causal-graph edge draw-in, ledger-page scroll reveal |

Every animated component ships a `prefers-reduced-motion` fallback that swaps to an
instant state change — never a degraded-but-still-animated version. GSAP and Lenis are
route-level dynamic imports, never global bundle dependencies (§13).

## 10. Loading — honest, specific, never generic theater

Rule: **never depict a process the backend isn't actually performing.** A loading state
may only reference a real operation.

| Real backend operation | Honest loading pattern |
|---|---|
| Photo upload + redaction (`POST /v1/intake/reports/photo`) | Progress bar tied to real upload bytes, then a redaction-badge placeholder until the response returns — no fake "scanning" sweep unless upload is genuinely streaming |
| AHP re-run (`POST /v1/prioritization/evaluate`) | If the API returns all 5 criteria together (likely), reveal them with a `duration-fast` stagger for legibility once the response lands — this is a legibility aid on real data, not a simulation of computation happening live |
| Dedup/Fellegi-Sunter matching | Plain skeleton rows — no "matching..." narrative unless the API streams progress |
| GIS cluster load | Muted basemap skeleton, points fade in on data arrival |
| Offline sync (`POST /v1/dispatch/sync`) | Determinate "X of Y mutations synced" — real countable data, show it |
| Ledger chain fetch | Plain skeleton list — no fake "verifying cryptographic proof" spinner unless that step is genuinely observable from the API |

Default fallback when no operation-specific pattern applies: a plain skeleton in the
shape of the real content, `opacity` pulse only (`duration-slow`), never a spinner
icon as the primary pattern (skeletons communicate *what's coming*; spinners don't).

## 11. Responsive system

| Breakpoint | Range | Nav | Maps | Tables | Sidebars | Drawers | Evidence | Forms | Charts |
|---|---|---|---|---|---|---|---|---|---|
| Mobile | 0–639px | Bottom tab bar (citizen) / hamburger→full sheet (staff, rare) | Full-screen, controls collapse to a bottom sheet | Become stacked list rows, not scrolled tables | Become a bottom sheet | Become full-screen sheets | Full-width, stacked before/after | Single column, `content-width-form` capped | Simplified, 1 series default, swipe between |
| Tablet | 640–1023px | Persistent bottom tab (citizen) / collapsible rail (staff) | Inline, controls as a floating panel | Horizontal-scroll table with sticky first column | Collapsible rail | Right-side drawer | Two-up grid | Two-column where natural | Full detail |
| Laptop | 1024–1439px | Persistent left rail (staff) | Inline with a docked side panel | Full table, sticky header | Persistent, collapsible | Right-side drawer | Grid, before/after side by side | Two-column | Full detail, multi-series |
| Desktop | 1440–1919px | Persistent left rail | Inline, side panel + minimap | Full table + inline expand rows | Persistent | Right-side drawer | Grid | Two-column, generous margin | Full detail |
| Large desktop | 1920px+ | Persistent left rail, content stays capped at `content-width-console`/`narrow` — never stretches full width | Same, more map real estate | Same, more visible rows | Persistent | Right-side drawer | Grid, capped columns | Content stays capped, doesn't stretch | Full detail |

Not a shrink-desktop-to-fit approach: mobile Command Deck/Ops Board (if ever accessed on
a phone) becomes a list-row pattern, not a horizontally-scrolled miniature table.

## 12. Accessibility — part of the design, not QA

- WCAG 2.1 AA minimum everywhere; Karmi Sahayak targets ≥7:1 contrast unconditionally.
- **Status/confidence/priority is never color-only** — always paired with a text label
  and/or icon (§5, §8 badges).
- Focus ring: `2px solid var(--color-focus)`, `2px` offset, visible on every interactive
  element, never suppressed.
- Full keyboard navigation on staff consoles — arrow-key row navigation on Command Deck/
  Ops Board queues, `Tab`/`Shift+Tab` through forms in logical order, `Esc` closes
  drawers/dialogs/sheets.
- Touch targets ≥ 48px on Nagrik Setu and Karmi Sahayak (`control-height-lg`).
- Evidence photo alt text: citizen-declared category + location, never "photo" or
  filename.
- Error messaging: plain language, states what happened and the next step, never a raw
  API/exception string.
- `prefers-reduced-motion` respected by every animated component (§9).

## 13. Performance

- Image strategy per §7: responsive `srcset`, lazy-load below fold, real-pixel blur-up
  placeholders, never a generic asset standing in for content that exists.
- Route-level code splitting per workspace — Control Room code never loads for a
  dispatcher, Karmi Sahayak never loads staff-console map code.
- GSAP, Lenis, MapLibre are dynamic imports on the routes that use them — never in the
  main bundle of any app.
- Budgets: `nagrik-setu`/`transparency-board` — Lighthouse Performance ≥90 on simulated
  Moto G4/Slow 4G; `karmi-sahayak` — core shell ≤200KB gzipped; `staff-console` — route-
  split per workspace, no cross-workspace bundle bleed.
- Animation budget: Expressive-tier motion (§9) never runs on more than one element
  simultaneously per view, and never on Karmi Sahayak regardless of context (battery/
  data cost on field devices).

## 14. AI-slop pre-flight — permanent banned-pattern list

Inter-as-default · purple-blue gradients · generic SaaS dashboard look · three/six-card
feature grids · identical rounded cards repeated as the only structural pattern ·
glassmorphism · neon glow · gradient text · hero blobs · excessive pills (only status
chips get `radius-full`) · icon-in-square-above-heading pattern · arbitrary/inconsistent
shadows (only the two tokens in §3.3 exist) · a grey 1px border around every element by
default · meaningless parallax · animation with no functional reason · fake AI
confidence language · decorative charts with no real data · fabricated statistics ·
generic stock photography · random handwritten/display typography with no stated reason
· brutalism or glassmorphism applied because it's currently fashionable rather than
because it serves this specific product.

**Rule**: *do not reject a pattern because it is trendy — reject it because it is
unearned.* A rounded card is fine when content is genuinely discrete and comparable
(§8). A shadow is fine when it's one of the two defined elevation tokens used for its
defined purpose. The test is always: does this choice come from the product (Benchmark
concept, workspace personality, real content) or from a template default?

## 15. Implementation contract — every future Antigravity prompt must include

1. Reference this file (`DESIGN.md`) and the relevant section numbers — never restate
   the whole system inline.
2. Name the workspace (§2) and its theme file.
3. Name the user/role building this screen for (`FRONTEND_CONTEXT.md` §5).
4. Name the actual backend capability/endpoint(s) involved (`FRONTEND_CONTEXT.md` §6,
   `SCREEN_SPECS.md`).
5. State the exact visual intent in Benchmark terms (verified vs. provisional, etc).
6. Describe layout using the structural pattern from §8 (table/timeline/split-pane/
   evidence board/command surface — not "a card").
7. Describe interaction behavior per §8/§9 motion level for that workspace.
8. Describe responsive behavior per §11 for the breakpoints that matter for this screen.
9. Describe every required state: loading (§10), empty, error, success, offline where
   relevant, confidence/evidence states where relevant.
10. Describe accessibility requirements per §12 specific to this screen's controls.
11. Describe performance constraints per §13 specific to this screen (image count, map
    presence, animation use).
12. Specify what NOT to do — the relevant subset of §14, plus any screen-specific
    backend-truth traps (e.g. "do not show a confidence percentage for CV categorization
    — it doesn't exist yet").
13. Specify acceptance criteria as a short checklist Antigravity must self-verify against
    before considering the screen done.

Claude makes the design decisions. Antigravity implements against a fully-specified
prompt — it never invents visual direction, color, typography, or layout structure.
