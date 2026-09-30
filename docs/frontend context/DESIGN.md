# DESIGN.md — CivicBrain Canonical Design System (v2)

> Single source of truth for every visual decision in CivicBrain. Components and
> Antigravity prompts cite this document by section; they do not restate it.
> Product/backend facts live in `FRONTEND_CONTEXT.md`. Screen detail lives in
> `SCREEN_SPECS.md`. This file only changes when a real design decision changes.
>
> **v2 changelog** (supersedes v1 in full): the brand/action color moved off orange
> entirely — orange is now status-only (urgent/critical). One deep teal ("Ledger") is
> the product's single brand/interactive color everywhere except Karmi Sahayak's
> functionally-justified hi-vis exception. Neutrals cooled from warm cream to a
> cooler stone-paper. Display serif changed Fraunces → Newsreader. Responsive rules
> tightened: no screen may ship a "mobile stack, just centered" desktop layout — every
> screen needs a real composition at ≥1024px (§11 now names this violation explicitly).

---

## DESIGN DNA (read this first, every session)

**Concept — The Benchmark**, unchanged: a surveyor's benchmark is a fixed, verified
reference point everything else is checked against. CivicBrain does the same to civic
reports — uncertain complaints become verified, located, appealable records. Things
that are *verified* look stamped; things that are *uncertain* look provisional; things
that are *located* are tied to a coordinate, a map, a ward.

**One brand color, strictly separated from status.** `Ledger` — a deep, quiet teal — is
the product's *only* interactive/brand color: buttons, links, focus rings, the wordmark
accent, everywhere, in every workspace but one. `Brick` (orange-red), `Turmeric`
(amber), `Moss` (green), and `Slate` (blue-grey) exist *only* for status, confidence,
and priority — never for chrome, never for decoration. This is the single most
important rule in the palette: **if a component is using Brick/Turmeric/Moss/Slate
anywhere other than a status/priority/confidence indicator, that's a bug.** The one
sanctioned exception is Karmi Sahayak, which trades the teal brand for a high-contrast
amber chrome — justified purely by outdoor sunlight legibility, not decoration.

**Neutrals are cool stone-paper, not warm cream.** `Paper` (surface) and `Ink`
(text/dark chrome) both lean cool teal-charcoal, never pure black, never a beige that
reads "generic government form."

**Type is IBM Plex Sans (UI) + IBM Plex Mono (data) + IBM Plex Sans Devanagari (Hindi)
+ Newsreader (the one rare editorial accent — Transparency Board, ward report cards,
key Nagrik Setu moments; never body copy, never buttons).**

**Every screen gets a real desktop composition — never a centered mobile column.**
Stacking content and centering it on a wide viewport is the single most common way this
system quietly degrades into "shrink-to-fit." If a screen has more than one primary
element (e.g. a primary action plus supporting/recent content), ≥1024px gets a genuine
multi-column layout, not the mobile stack with more whitespace around it.

**Tokens are four layers**: primitive → semantic → component → workspace-theme.
Components touch semantic tokens only. Because semantic token *names* never change
(only what they map to), a palette correction like this one only ever touches
`tokens/primitives.css` and `tokens/semantic.css` — never a component file.

**One product, seven registers**, driven by density/typography-scale/motion/component
grammar — not by swapping the brand hue per workspace anymore. Nagrik Setu (warm,
spacious) → Command Deck (dense, quiet-motion, table-first) → Ops Board (dense,
departmental) → City Pulse (spatial, GSAP-eased map reveals, teal map-data layer
distinct from the teal brand color) → Karmi Sahayak (tactile, hi-vis amber, offline-
aware — the one brand-color exception) → Control Room (flat, zero accent at all, not
even Ledger) → Transparency Board (editorial, stamped-ledger, Lenis scroll).

**Motion has three levels**: Quiet (operational), Responsive (interaction feedback),
Expressive (public/read-once surfaces only).

**Confidence and evidence are never decorative.** No fake AI confidence, no decorative
charts, no loading animation implying work the backend isn't doing.

**Banned by default**: Inter, blue-purple gradients, glassmorphism, neon glow,
floating blobs, icon-in-square-above-heading grids, generic rounded-card walls,
meaningless parallax, stock photography, and — new in v2 — any screen whose ≥1024px
layout is just its mobile layout centered with more margin. Full list §14.

---

## 1. Art direction — The Benchmark

Unchanged from v1: CivicBrain converts uncertain, multi-channel civic noise into a
verified, located, appealable record. Provisional content looks like a field sketch;
confirmed content looks like a survey stamp. Rejected directions: generic gov-portal
(bland-as-trust, wrong for a product people should *want* to check), smart-city
futurism (implies sensor/AI capability the product doesn't have). Chosen direction:
editorial/documentary — a serious newsroom or ordnance-survey office's relationship to
a public record. v2 sharpens the palette toward that specifically: a real municipal
ledger book is bound in dark cloth or leather with cream pages, not a bright orange
folder — the deep `Ledger` teal reads as *that binding*, not as a call-to-action color
borrowed from a checkout button.

## 2. Visual variation by workspace

Same shared DNA, seven contextual expressions — now via density/typography/motion/
component grammar rather than a different brand hue per workspace.

| Workspace | Density | Typography behavior | Imagery | Interaction style | Motion | Surface treatment | Hierarchy | Spatial metaphor |
|---|---|---|---|---|---|---|---|---|
| **Nagrik Setu** | Low, spacious; two-column on desktop (primary actions left, recent activity right — never a centered mobile stack past 1024px) | Plex Sans body, Newsreader for the 2–3 highest-trust moments | Citizen's own evidence photos, full-bleed | Large touch targets, one primary action per screen | Expressive at key moments only | Paper surface, `Ledger`-teal primary buttons/links | One task at a time, status always visible | The tracking token *is* the artifact — a field waybill stub |
| **Command Deck** | High, table-dense, 1280px+ | Plex Sans UI, Plex Mono for every score/ID/timestamp | Evidence thumbnails inline, full view on demand | Keyboard-navigable queue, inline expand | Quiet, <150ms | Ink chrome, `Ledger`-teal for the one primary action per view, optional dark night-ops mode | Priority score is the primary sort axis, always itemized | A stamped ledger line per incident |
| **Ops Board** | High, departmental | Same as Command Deck, dept-color chips use `Slate` variants, never brand hue | Work-order evidence, before/after | Assign/claim from the queue row | Quiet | Lighter Paper than Command Deck | SLA timer dominant, color-coded via status tokens only | A clipboard — subtle top-binding rule motif |
| **City Pulse** | Medium, map-first | Plex Sans panels, Plex Mono coordinates | The map itself; no other photography | Click/hover map interaction | Expressive for the map only — GSAP cluster reveal | Paper chrome, `Ledger`-teal UI buttons, `Channel` (a distinct lighter teal) for map data layers only — never the same teal as the buttons | Spatial pattern first, list second | Coordinate-ruler ticks along the map frame |
| **Karmi Sahayak** | Low, single-task, full-screen | Plex Sans only, larger scale | Camera capture is the interaction | One thumb, bottom-anchored action | Minimal, fast | Near-black Ink surface, **high-contrast amber chrome — the one sanctioned brand-color exception**, justified by outdoor sunlight legibility | Current task fills the screen | A hi-vis vest, not a dashboard |
| **Control Room** | High, form-dense | Plex Sans + Plex Mono | None | Explicit save/confirm, typed confirmation for destructive actions | None beyond native | Flat Paper, **zero accent color at all — not even `Ledger`** | Every field labeled | A registry ledger book |
| **Transparency Board** | Low, editorial, 720px column | Newsreader headlines over Plex Sans body, Plex Mono for hashes/IDs | City-wide aggregate imagery only | Read-mostly, scroll-driven | Expressive — Lenis smooth scroll | Paper with a `Moss`-green stamp motif on verified entries | The ledger entry is the unit | A public notice board / stamped audit trail |

## 3. Design tokens — four layers

```
tokens/primitives.css        raw scales, no meaning
tokens/semantic.css          meaning, workspace-agnostic
tokens/components/*.css      component-scoped tokens, reference semantic only
tokens/themes/*.css          per-workspace overrides of semantic tokens only
```

Semantic token *names* are stable across v1 → v2 — only their values changed. If a
component was built correctly against semantic tokens (never a raw hex), this palette
correction requires **zero component-file edits** — that's what the layer system is for.

### 3.1 Primitive palette

| Family | Role | Anchor value(s) |
|---|---|---|
| `--paper-*` | Cool stone-paper neutrals, surfaces | `--paper-0: #F6F5EF` (card) · `--paper-50: #EDEBE3` (base bg) · `--paper-300: #C9CBBC` (border) |
| `--ink-*` | Teal-charcoal dark scale — text, dark chrome, Control Room/night-ops dark mode | `--ink-900: #1C2B28` (primary text) · `--ink-600: #4B5D57` (secondary text) · `--ink-950: #141F1D` (dark-mode base) |
| `--ledger-*` | **The one brand/interactive color, everywhere except Karmi Sahayak** | `--ledger-600: #1F4E49` (light-mode primary) · `--ledger-700: #163936` (hover/pressed) · `--ledger-300: #6FB3A6` (dark-mode primary) |
| `--channel-*` | Spatial/GIS map-data layers only — deliberately distinct from `Ledger` so map data never reads as a clickable action | `--channel-500: #3E8C8A` |
| `--brick-*` | Status: urgent/critical/danger — **status only, never chrome** | `--brick-500: #A6432E` |
| `--turmeric-*` | Status: medium/warning/low-confidence — **status only** | `--turmeric-500: #A87423` |
| `--moss-*` | Status: success/resolved/verified — **status only** | `--moss-500: #3E6B4F` |
| `--slate-*` | Status: neutral/informational — **status only** | `--slate-500: #55606B` |
| `--hivis-amber-*` | Karmi Sahayak's chrome exception only, never used elsewhere | `--hivis-amber-500: #E0A83D` |

### 3.2 Semantic tokens (full mapping in `tokens/semantic.css`; representative set)

```css
--color-background          var(--paper-50)
--color-surface              var(--paper-100)
--color-surface-raised        var(--paper-0)
--color-border               var(--paper-300)
--color-border-strong        var(--ink-500)
--color-text-primary         var(--ink-900)
--color-text-secondary       var(--ink-600)
--color-text-inverse         var(--paper-50)
--color-action-primary       var(--ledger-600)   /* was Marker-orange in v1 — now unified teal */
--color-action-secondary     var(--ink-700)
--color-focus                var(--ledger-600)
--color-status-success       var(--moss-500)
--color-status-warning       var(--turmeric-500)
--color-status-danger        var(--brick-500)
--color-status-info          var(--slate-500)    /* was Channel in v1 — Channel is now spatial-only */
--color-confidence-low       var(--turmeric-500) /* "still calibrating" */
--color-confidence-medium    var(--slate-500)    /* neutral, not alarming */
--color-confidence-high      var(--moss-500)     /* reassuring */
--color-verified-seal        var(--moss-600)
--color-priority-low         var(--slate-500)
--color-priority-medium      var(--turmeric-500)
--color-priority-high        var(--brick-500)    /* priority intentionally shares the status
   hue family now — a priority level IS an urgency signal, so this is earned reuse, not
   decoration. Disambiguated from a plain status pill by content, not color: a priority
   chip always carries its numeric score + "Priority" label; a status pill never does. */
--color-gis-incident-point   var(--channel-500)
--color-gis-cluster-fill     var(--channel-500)
--color-gis-ward-boundary    var(--ink-500)
--color-gis-causal-edge      var(--channel-600)
--color-gis-selected-ring    var(--moss-500)
```

### 3.3 Typography, spacing, radius, borders, shadows, elevation, opacity, motion, z-index

```css
/* type scale — mobile → desktop pair, fluid via clamp() */
--font-family-ui        "IBM Plex Sans", "Segoe UI", sans-serif
--font-family-mono      "IBM Plex Mono", ui-monospace, monospace
--font-family-devanagari "IBM Plex Sans Devanagari", sans-serif
--font-family-display   "Newsreader", Georgia, serif       /* rare — §6, changed from Fraunces */

--text-xs:   clamp(0.75rem, 0.72rem + 0.1vw, 0.8125rem)
--text-sm:   clamp(0.8125rem, 0.78rem + 0.12vw, 0.875rem)
--text-base: clamp(0.9375rem, 0.9rem + 0.15vw, 1rem)
--text-lg:   clamp(1.0625rem, 1rem + 0.25vw, 1.1875rem)
--text-xl:   clamp(1.25rem, 1.15rem + 0.4vw, 1.5rem)
--text-2xl:  clamp(1.625rem, 1.4rem + 0.9vw, 2.25rem)
--text-3xl:  clamp(2.125rem, 1.7rem + 1.8vw, 3.25rem)   /* Newsreader display only */

--space-1: 4px  --space-2: 8px  --space-3: 12px  --space-4: 16px
--space-5: 20px --space-6: 24px --space-8: 32px  --space-10: 40px
--space-12: 48px --space-16: 64px --space-20: 80px --space-24: 96px --space-32: 128px

--radius-sm: 4px    /* inputs, chips */
--radius-md: 8px    /* cards, buttons */
--radius-lg: 12px   /* modals, sheets */
--radius-xl: 16px   /* full-screen mobile sheets only */
--radius-full: 999px  /* status chips ONLY — the one pill exception */

--shadow-flat: none
--shadow-lifted: 0 8px 24px -12px rgba(20,31,29,0.18)
--shadow-overlay: 0 16px 48px -16px rgba(20,31,29,0.28)   /* modals/sheets only */

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

--content-width-narrow: 720px   /* single-column reading content — Track Report, ledger entries */
--content-width-form: 560px
--content-width-dashboard: 960px  /* NEW in v2 — multi-column landing/dashboard screens
   (Nagrik Setu Home, etc.) that are NOT continuous prose and shouldn't be squeezed into
   the narrow reading column just because they're on a "citizen" app */
--content-width-console: none   /* fluid, min 1280px */
```

### 3.4 Map-specific tokens

```css
--map-point-radius-incident: 6px
--map-point-radius-cluster: clamp(8px, calc(8px + sqrt(var(--cluster-count)) * 1.5px), 28px)
--map-line-ward-boundary: 1.5px dashed var(--color-gis-ward-boundary)
--map-basemap-style: "civicbrain-field"   /* custom muted vector style, Paper/Ink palette
   — never a default bright OSM/Mapbox style. Provider UNKNOWN, see
   UI_ARCHITECTURE.md §10. */
```
Cluster radius is a real function of point count — never a decorative fixed size.

## 4. Theme-swap architecture

Unchanged principle, now proven by this exact revision: a full re-theme means editing
`tokens/primitives.css`/`tokens/semantic.css` (global) or a specific
`tokens/themes/<workspace>.css` (scoped) — never a component. This v1→v2 palette
correction touched only those two files plus the two font tokens. If any component was
found hardcoding `#C1592B` or similar instead of `var(--color-action-primary)`, that's
logged as a violation in the retrofit pass (`ANTIGRAVITY_PROMPTS.md` §RETROFIT), not
silently fixed inline.

## 5. Color — every color has a job

| Token | Job | Never used for |
|---|---|---|
| `color-action-primary` (`Ledger`) | The one primary action per screen, everywhere except Karmi Sahayak | Decoration, large background fills, anything status-related |
| `color-action-secondary` (`Ink`) | Secondary/staff actions | Citizen primary CTAs |
| `color-status-success/warning/danger/info` (`Moss`/`Turmeric`/`Brick`/`Slate`) | System-state feedback, confidence bands, priority bands | Brand chrome, buttons, links, decoration |
| `color-gis-*` (`Channel`) | Map data layers only | UI chrome outside the map — including buttons that happen to live on a map screen, which still use `Ledger` |
| `color-verified-seal` (`Moss`) | The verification/stamped mark specifically | General success toasts — visually distinct via the `SealMark` shape, not a different hue |

Contrast: body text on background/surface ≥ 7:1; UI labels ≥ 4.5:1 minimum; Karmi
Sahayak overrides to ≥ 7:1 unconditionally. No status/priority/confidence meaning is
ever color-only — always paired with a label, icon, or the numeric value itself (§12).

**The one rule that matters most**: grep the codebase periodically for any component
using `Brick`/`Turmeric`/`Moss`/`Slate` outside an actual status/priority/confidence
indicator. That is the single most common way this system quietly degrades back into
"orange = brand" — it must never happen again after the v1 mistake.

## 6. Typography

**System**: IBM Plex Sans (UI/body) + IBM Plex Mono (data) + IBM Plex Sans Devanagari
(Hindi companion) — one open-source multi-script family. Plus **Newsreader** (changed
from Fraunces in v2) as the single rare display accent — a literary/gazette-quality
variable serif (optical size + italic), used only for Transparency Board headlines,
ward report card titles, and the 2–3 highest-trust Nagrik Setu moments. Never body copy,
never buttons, never more than one Newsreader element per screen.

| Role | Family | Weights | Notes |
|---|---|---|---|
| UI/body | IBM Plex Sans | 400, 500, 600 | Default everywhere |
| Data/coordinates/IDs/timestamps/scores | IBM Plex Mono | 400, 500 | Tabular figures always on |
| Hindi UI/body | IBM Plex Sans Devanagari | 400, 500, 600 | Weight-matched pairing |
| Editorial display (rare) | Newsreader (variable: opsz, wght, ital) | 400–600 | Transparency Board, ward report cards, Nagrik Setu key moments only |

Scale, line-height, tracking, numerals: unchanged from v1 (§3.3). Paragraph width still
capped at `content-width-narrow` (720px) for continuous prose specifically — dashboard/
landing screens that aren't prose may use `content-width-dashboard` (960px, new in v2,
§3.3) instead.

## 7. Imagery

Unchanged from v1 — real evidence and real geography only, never stock photography, no
decoration. See v1 spec in full: evidence photography 4:3/native aspect, GPS/timestamp
mono caption strip below (never overlaid), redaction badge, before/after pairs equal
size, custom muted basemap for maps, responsive `srcset`, real-pixel blur-up placeholder.

## 8. Component language

Unchanged from v1 — structure follows content, not every surface is a rounded card.
Buttons/inputs/tables/timelines/evidence galleries/score breakdowns etc. all keep their
v1 grammar (`radius-md`, two elevation levels, table-first for staff consoles, etc.).
The only functional change: every component that previously referenced
`color-action-primary` expecting orange now renders `Ledger` teal automatically — no
component code changes required.

## 9. Motion system

Unchanged from v1 — Quiet/Responsive/Expressive tiers, `prefers-reduced-motion`
fallbacks, GSAP/Lenis as route-level dynamic imports only. See v1 spec.

## 10. Loading — honest, specific, never generic theater

Unchanged from v1 — never depict a process the backend isn't actually performing. See
v1 spec in full (operation-specific loading patterns table).

## 11. Responsive system

Unchanged breakpoint table from v1 (§11), **plus one new hard rule**: a screen with more
than one primary element (a main action plus supporting/secondary content — recent
items, related data, context) must get a genuine multi-column composition at ≥1024px.
"Centering the mobile stack with more margin around it" is not a desktop layout — it is
the exact mistake this v2 revision exists to correct (see Nagrik Setu Home,
`SCREEN_SPECS.md` §2.1, fixed as the reference case). A single-purpose linear flow
(the New Report Flow's step-by-step capture, for instance) is allowed to stay single-
column at every breakpoint — that's a genuine design decision, not the anti-pattern.
The test: could a wide viewport show something useful *beside* the primary content
instead of just empty margin? If yes, it must.

## 12. Accessibility — part of the design, not QA

Unchanged from v1 — WCAG 2.1 AA minimum, Karmi Sahayak ≥7:1 unconditionally,
status/confidence/priority never color-only, visible focus ring, full keyboard nav on
staff consoles, ≥48px touch targets on citizen/field apps. See v1 spec in full.

## 13. Performance

Unchanged from v1 — image/lazy-load strategy, route-level code splitting, GSAP/Lenis/
MapLibre as dynamic imports only, Lighthouse ≥90 targets. See v1 spec in full.

## 14. AI-slop pre-flight — permanent banned-pattern list

Everything from v1's list still applies (Inter, blue-purple gradients, glassmorphism,
neon glow, gradient text, hero blobs, excessive pills, icon-in-square-above-heading,
arbitrary shadows, meaningless parallax, fake AI confidence, decorative charts,
fabricated statistics, generic stock photography, unearned brutalism/glassmorphism).

**New in v2**:
- **A screen whose ≥1024px layout is its mobile layout, just centered with wider
  margins.** Every multi-element screen needs a real desktop composition (§11).
- **Any use of `Brick`/`Turmeric`/`Moss`/`Slate`/`Channel` as brand/chrome color**
  instead of `Ledger` — these are status/spatial tokens, not decoration, ever.
- **A warm-cream or beige surface color** — neutrals are cool stone-paper (`Paper`),
  not cream, per §3.1.

**Rule, unchanged**: *do not reject a pattern because it is trendy — reject it because
it is unearned.* The test is always: does this choice come from the product (Benchmark
concept, workspace personality, real content) or from a template default?

## 15. Implementation contract — every future Antigravity prompt must include

Unchanged from v1 (13-point list — reference this file's section numbers, name the
workspace/user/backend capability, describe layout/interaction/responsive/states/a11y/
performance, specify what NOT to do, specify acceptance criteria). See v1 spec in full.
Claude makes the design decisions. Antigravity implements against a fully-specified
prompt — it never invents visual direction, color, typography, or layout structure.
