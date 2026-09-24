# ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts

> Paste-ready prompts for Antigravity, in build order. Each prompt is standalone — it
> can be pasted alone into a fresh Antigravity session. Design system detail lives in
> `DESIGN.md`; screen detail lives in `SCREEN_SPECS.md`; product/backend truth lives in
> `FRONTEND_CONTEXT.md`; architecture lives in `UI_ARCHITECTURE.md`. Every prompt
> references these by section instead of repeating them.
>
> **Read this once before running anything**: all of the above files (plus this one and
> `IMPLEMENTATION_LOG.md`) live in the project's frontend-context docs folder. Confirm
> the exact path in the repo first — reference them by filename in every prompt below.

## Standard clauses (included in full inside every prompt — do not skip when pasting)

**FILES TO READ (standard):** `DESIGN.md`, `FRONTEND_CONTEXT.md`, `UI_ARCHITECTURE.md`,
`SCREEN_SPECS.md` (relevant §), `IMPLEMENTATION_LOG.md` — from the frontend-context docs
folder, before writing any code.

**DOCUMENTATION (standard, mandatory, every prompt):** After finishing this task, append
a new dated entry to `IMPLEMENTATION_LOG.md` (never overwrite prior entries) using its
template: files created/modified, components/tokens introduced or changed, deviations
from this prompt with reasons, known gaps, which states were actually implemented, and a
pass/fail self-check against this prompt's Acceptance Criteria and against `DESIGN.md`
§14 (anti-slop). This is not optional — the audit phase depends on it being current.

---

## Implementation order

1. **Foundation** — PROMPT 0
2. **Shared shells** — PROMPT 1
3. **Navigation & routing** — PROMPT 2
4. **Primitives** — PROMPT 3 (Tier 0), PROMPT 4 (Tier 1 civic-specific)
5. **First representative screen per workspace** — PROMPT 5–11
6. **Remaining screens** — PROMPT 12–33
7. **Responsive refinement pass** — PROMPT 34
8. **Motion pass** — PROMPT 35
9. **Accessibility pass** — PROMPT 36
10. **Visual polish / anti-slop pass** — PROMPT 37

---

## PROMPT 0 — Foundation: Tokens & Repo Scaffold

PROJECT CONTEXT: CivicBrain, greenfield frontend against a live, stable backend. No
frontend code exists yet.
WORKSPACE: none (cross-cutting foundation).
USER: n/a — infrastructure only.
SCREEN: n/a.
GOAL: stand up the monorepo and the token system so every later prompt has something to
build on.
FILES TO READ: standard, plus `UI_ARCHITECTURE.md` §1–3 in full.
BACKEND/API SOURCES: none directly — this is pure frontend infra.
LAYOUT: n/a.
COMPONENTS: n/a.
TYPOGRAPHY: load IBM Plex Sans, IBM Plex Mono, IBM Plex Sans Devanagari (self-hosted
woff2, not a CDN dependency for the primary UI faces — Fraunces may load from Google
Fonts per `DESIGN.md` publishing constraints if this becomes a published artifact later,
but for the app itself, self-host all four families).
COLOR TOKENS: implement the full four-layer system from `DESIGN.md` §3 exactly —
`tokens/primitives.css`, `tokens/semantic.css`, `tokens/components/*.css` (empty
scaffolds, filled per-component later), `tokens/themes/*.css` (one file per workspace,
even if mostly empty at this stage — the files must exist so later prompts only ever
edit them, never create new theme files ad hoc). Wire into Tailwind v4 via `@theme`
pointing at the CSS custom properties — never Tailwind's default palette.
IMAGERY: n/a.
INTERACTIONS: n/a.
MOTION: n/a.
RESPONSIVE BEHAVIOR: implement the breakpoint tokens from `DESIGN.md` §3.3/§11.
LOADING/EMPTY/ERROR/SUCCESS: n/a.
ACCESSIBILITY: n/a at this stage.
PERFORMANCE: fonts subset to Latin+Devanagari only, `font-display: swap`.
DO NOT: do not invent additional primitive color families beyond Field/Station/Marker/
Channel/Seal/Flag (`DESIGN.md` §3.1). Do not add Inter or any fallback that isn't in the
approved stacks. Do not skip creating the per-workspace theme file scaffolds even if
empty.
ACCEPTANCE CRITERIA:
- [ ] Repo builds and runs with zero visual output (this prompt ships plumbing only)
- [ ] All four token layers exist as separate files matching `DESIGN.md` §3 structure
- [ ] All four typefaces load and are verified in a throwaway test page, then that test
      page is deleted before committing
- [ ] Report back the confirmed repo/monorepo structure and package manager used, since
      this was flagged UNKNOWN in `SCREEN_SPECS.md` §3
DOCUMENTATION: standard (see top of this file).

---

## PROMPT 1 — Shared App Shells

PROJECT CONTEXT: CivicBrain.
WORKSPACE: all four deployables (`UI_ARCHITECTURE.md` §1).
USER: n/a — structural.
SCREEN: n/a — shells only, no real screen content yet.
GOAL: build `StaffConsoleShell`, `CitizenShell`, `FieldShell`, `EditorialShell` per
`SCREEN_SPECS.md` §1 Tier 2, empty of real content but structurally complete and
themeable.
FILES TO READ: standard, plus `DESIGN.md` §2 (workspace personality table) and §3.3.
BACKEND/API SOURCES: none.
LAYOUT: `StaffConsoleShell` = 280px left rail + fluid main, min-width 1280px.
`CitizenShell` = bottom tab bar + `content-width-narrow` column, mobile-first.
`FieldShell` = single column, bottom-anchored action slot, no top chrome beyond a
persistent `OfflineSyncBadge` slot. `EditorialShell` = top nav + `content-width-narrow`
column (Astro layout component).
COMPONENTS: each shell is a layout component taking a `children` slot; no page content.
TYPOGRAPHY/COLOR TOKENS: each shell applies its workspace's theme token file
(`tokens/themes/*.css`) at the root — this is the one place theme selection happens.
IMAGERY: none.
INTERACTIONS: none yet beyond shell chrome (nav real links come in PROMPT 2).
MOTION: none.
RESPONSIVE BEHAVIOR: per `DESIGN.md` §11 table for each shell's nav element specifically.
LOADING/EMPTY/ERROR/SUCCESS: n/a.
ACCESSIBILITY: shells include a skip-to-content link (staff console especially), correct
landmark roles (`nav`, `main`).
PERFORMANCE: shells are the app's persistent chrome — must not themselves trigger route
code-splitting boundaries in a way that duplicates shell code per route.
DO NOT: do not add any workspace-specific visual flourish inside these shells beyond the
theme token swap — personality comes from tokens and later screen content, not from
one-off styling inside the shell component itself.
ACCEPTANCE CRITERIA:
- [ ] All four shells render with placeholder content and visibly different theming
      purely from their theme token file
- [ ] Switching a value in one `tokens/themes/*.css` file visibly changes only that
      shell, nothing else
DOCUMENTATION: standard.

---

## PROMPT 2 — Navigation & Role-Gated Routing

PROJECT CONTEXT: CivicBrain.
WORKSPACE: `staff-console` primarily (role-gating is its core complexity); also wires
real routes for the other three apps.
USER: all 7 roles (`FRONTEND_CONTEXT.md` §5).
SCREEN: n/a — routing/nav only.
GOAL: implement the full route table from `SCREEN_SPECS.md` §0, with `staff-console`
navigation gated by `staff_role_enum` so a `dispatcher` never sees a Control Room nav
item, etc.
FILES TO READ: standard, plus `SCREEN_SPECS.md` §0 in full and `FRONTEND_CONTEXT.md` §5.
BACKEND/API SOURCES: `GET /v1/auth/me` — decode role/scope on load, gate nav accordingly.
LAYOUT: left rail (staff console) gets one nav item per workspace the current role can
access, in the order listed in `DESIGN.md` §2's table; bottom tab bar (citizen) gets
Home/Track only (2 items, not more); field app gets no persistent nav beyond the shell's
offline badge (single-purpose app).
COMPONENTS: `NavRail`, `NavTabBar`, route-level `RoleGate` wrapper.
INTERACTIONS: attempting a route the current role can't access redirects to that role's
default workspace, never a raw 403 page.
MOTION: Quiet — nav active-state change is instant.
RESPONSIVE BEHAVIOR: staff console rail collapses to icon-only ≥1024px<1280px if that
range is ever hit, full hamburger only below 1024px (rare for this role per
`DESIGN.md`§11).
ACCESSIBILITY: nav is fully keyboard-reachable, current route indicated with
`aria-current`.
DO NOT: do not build a generic "you don't have permission" dead-end screen — route to
somewhere useful instead (§Interactions above). Do not hardcode role checks scattered
across components — centralize in `RoleGate`.
ACCEPTANCE CRITERIA:
- [ ] Every route in `SCREEN_SPECS.md` §0 resolves to a real (even if empty) page
- [ ] A `corporator` account, when logged in, sees only Transparency Board nav; an
      `admin` sees everything
DOCUMENTATION: standard.

---

## PROMPT 3 — Tier 0 Primitives

PROJECT CONTEXT: CivicBrain.
WORKSPACE: shared (`packages/ui`).
GOAL: build the generic primitive set from `SCREEN_SPECS.md` §1 Tier 0: `Button`,
`IconButton`, `Field`/`Input`/`Select`/`Textarea`, `Checkbox`/`Radio`/`Switch`, `Tabs`,
`Tooltip`, `Toast`, `Dialog`, `Sheet`, `Drawer`, `Badge`/`Chip`, `Skeleton`,
`EmptyState`, `ErrorState` — on Radix primitives for behavior, fully restyled per
`DESIGN.md` §8, never shipped with default shadcn visuals.
FILES TO READ: standard, plus `DESIGN.md` §3.3 (component tokens) and §8 in full.
COMPONENTS/TYPOGRAPHY/COLOR: every visual property sourced from semantic tokens only —
no raw hex, no raw px shadow, per `DESIGN.md` §4's absolute rule.
INTERACTIONS: each primitive supports the full state set relevant to it (hover, press,
focus, disabled; `Input` additionally supports invalid-with-message per `DESIGN.md`§8).
MOTION: `Button` press = scale 0.98 `duration-fast`; `Dialog`/`Sheet` entrance/exit per
`DESIGN.md` §9 Responsive tier; `Toast` per §8.
RESPONSIVE BEHAVIOR: `Dialog`→`Sheet` swap is a workspace/breakpoint decision made by the
*caller*, not baked into one component — build both, document which to use when.
ACCESSIBILITY: full keyboard support and ARIA per Radix defaults, verify nothing was
broken by restyling; `EmptyState`/`ErrorState` take a required, specific message prop —
no default generic text allowed to ship.
DO NOT: no `rounded-full` outside `Badge`/`Chip` (`DESIGN.md` §3.3). No component
hardcodes a workspace theme — theming happens entirely via the semantic tokens it
inherits from context.
ACCEPTANCE CRITERIA:
- [ ] Every primitive has a Storybook-style isolated demo (or equivalent) showing all
      its states
- [ ] Swapping the active theme token file visibly restyles every primitive with zero
      component code changes
DOCUMENTATION: standard.

---

## PROMPT 4 — Tier 1 Civic-Specific Components

PROJECT CONTEXT: CivicBrain.
WORKSPACE: shared (`packages/ui`), built on PROMPT 3's primitives.
GOAL: build `ConfidenceBadge`, `ScoreBreakdown`, `EvidencePhotoCard`, `BeforeAfterPair`,
`StatusTimeline`, `TrackingTokenDisplay`, `OfflineSyncBadge`, `PriorityChip`, `SealMark`,
and the MapLibre layer wrappers (`WardBoundaryMapLayer`, `IncidentPointLayer`,
`ClusterLayer`) — per `SCREEN_SPECS.md` §1 Tier 1, this is CivicBrain's actual visual
vocabulary and the highest-leverage component work in the whole build.
FILES TO READ: standard, plus `PROJECT_REFERENCE_FOR_FRONTEND.md` §2.2/§3.3 for the
exact score formula and confidence semantics, and `DESIGN.md` §3.4 for map tokens.
BACKEND/API SOURCES: these components take typed props matching the actual API response
shapes for `priority_score`/`raw_priority_score`/`equity_boost`/`confidence_score` and
`incident_status_enum` — build against real field names from `/v1/openapi.json`, not
invented prop names.
COMPONENTS: `ScoreBreakdown` must render the exact formula from `FRONTEND_CONTEXT.md`§3
as an expandable itemization (collapsed = final score + confidence only; expanded = each
weighted criterion + equity boost, mono numerals). `StatusTimeline` must implement the
least-advanced-child aggregation rule (`FRONTEND_CONTEXT.md` §4) when given multiple
child observations, and a plain single-lifecycle rendering when given one.
IMAGERY: `EvidencePhotoCard` exactly per `DESIGN.md` §7 (aspect preserved, mono caption
strip below not overlaid, redaction badge, responsive `srcset`, real-pixel blur-up
placeholder while loading — never a generic gray box).
INTERACTIONS: `ScoreBreakdown` expand/collapse; `TrackingTokenDisplay` copy-to-clipboard
with a toast confirmation.
MOTION: Quiet tier for all of these by default (they're used everywhere, including
operational surfaces) — expand/collapse is an instant height change.
LOADING/EMPTY/ERROR: each ships a skeleton variant matching its real shape (not a
generic box) and a defined empty case (`StatusTimeline` with zero observations should
not render at all — that's a data bug upstream, fail loudly in dev).
ACCESSIBILITY: `ConfidenceBadge`/`PriorityChip`/`StatusTimeline` step states are all
readable by screen reader as text + numeric value, never conveyed by color/position
alone (`DESIGN.md` §12).
PERFORMANCE: MapLibre layer wrappers are the one place a heavy dependency is genuinely
justified — confirm it's dynamically imported, not in the shared bundle (`UI_ARCHITECTURE.md`§13/`DESIGN.md`§13).
DO NOT: do not let `ConfidenceBadge` ever render a percentage for something the CV
pipeline hasn't actually scored — if the field is null/cold-start, render the honest
"Citizen Declared" / "Pending Automated Triage" state instead, per
`FRONTEND_CONTEXT.md` §7 point 1 — this is the single most important rule in the entire
system and this component is where it's enforced first.
ACCEPTANCE CRITERIA:
- [ ] `ScoreBreakdown` renders correctly against a real sample API response
- [ ] `StatusTimeline` correctly computes least-advanced-child status from a 2+
      observation fixture, matching the rank table in `FRONTEND_CONTEXT.md` §4
- [ ] No component in this prompt has a code path that fabricates a confidence value
DOCUMENTATION: standard.

---

## PROMPT 5 — Representative Screen: Nagrik Setu · Track Report

PROJECT CONTEXT: CivicBrain.
WORKSPACE: Nagrik Setu (Citizen Portal).
USER: `citizen` (anon/OTP).
SCREEN: Track Report — lookup + detail, per `SCREEN_SPECS.md` §2.3.
GOAL: ship the screen that most directly proves the product's core honesty principle —
per-observation, never-collapsed status.
FILES TO READ: standard, plus `SCREEN_SPECS.md` §2.3 in full.
BACKEND/API SOURCES: `GET /v1/intake/reports/track`.
LAYOUT/COMPONENTS/IMAGERY/INTERACTIONS/MOTION: exactly as specified in
`SCREEN_SPECS.md` §2.3 — do not deviate on the least-advanced-child rendering, that is
the one non-negotiable part of this screen.
RESPONSIVE BEHAVIOR: mobile-first, this screen has no meaningful desktop-specific layout
beyond centering within `content-width-narrow`.
LOADING/EMPTY/ERROR/SUCCESS: per `SCREEN_SPECS.md` §2.3 states list.
ACCESSIBILITY: per `DESIGN.md` §12; token lookup and per-observation cards must be
independently announced by screen readers as separate items.
PERFORMANCE: this is a public, likely-mobile, likely-slow-network screen — budget per
`UI_ARCHITECTURE.md` §8/`DESIGN.md` §13.
DO NOT: do not show a single collapsed progress bar under any circumstance, even as a
"simplified" fallback. Do not pre-collapse status server-side assumptions — compute the
parent status client-side from the fetched children as specified.
ACCEPTANCE CRITERIA:
- [ ] A fixture with 2 observations in different departments at different statuses
      renders 2 independent `StatusTimeline`s and the correct least-advanced parent
      banner text
- [ ] Token-not-found state tested and matches spec
DOCUMENTATION: standard.

---

## PROMPT 6 — Representative Screen: Command Deck · Incident Detail

PROJECT CONTEXT: CivicBrain.
WORKSPACE: Command Deck.
USER: `dispatcher`, `admin`.
SCREEN: Incident Detail, per `SCREEN_SPECS.md` §2.6.
GOAL: ship the "case file" pattern — evidence-forward, score-explained — that Ops
Board's Work Order Detail (PROMPT 22) will explicitly reuse.
FILES TO READ: standard, plus `SCREEN_SPECS.md` §2.6, `FRONTEND_CONTEXT.md` §3/§4.
BACKEND/API SOURCES: `GET /v1/incidents/{id}`, `GET .../observations`, `GET
/v1/causal/links`, `PATCH .../status`.
LAYOUT: 280px rail + main; sticky 64px context strip; **60/40 evidence/score split** on
desktop, 100/100 stacked (evidence first) below 1024px — exact composition per
`SCREEN_SPECS.md` §2.6.
COMPONENTS: `EvidencePhotoCard` stack, `ScoreBreakdown` (expanded by default here),
`StatusTimeline` with staff-only valid-next-state transition buttons only — never a
free-form status dropdown.
INTERACTIONS/MOTION/RESPONSIVE/STATES: exactly per `SCREEN_SPECS.md` §2.6.
ACCESSIBILITY: full keyboard operability of the status-transition controls specifically —
this is the highest-consequence interactive element on the page.
PERFORMANCE: evidence images lazy-load below the fold even on this content-dense staff
screen.
DO NOT: do not offer a status transition that isn't valid from the incident's current
state per the 11-state machine (`FRONTEND_CONTEXT.md` §4) — compute valid-next-states
client-side from current status, don't hardcode a static button set.
ACCEPTANCE CRITERIA:
- [ ] Status buttons shown always exactly match the valid transitions for the current
      `incident_status_enum` value across all 11 states, tested against each
- [ ] Score breakdown numbers match the formula in `FRONTEND_CONTEXT.md` §3 exactly
DOCUMENTATION: standard.

---

## PROMPT 7 — Representative Screen: Ops Board · Department Queue

PROJECT CONTEXT: CivicBrain.
WORKSPACE: Ops Board.
USER: `department_staff`.
SCREEN: Department Queue, per `SCREEN_SPECS.md` §2.10.
GOAL: the department supervisor's primary daily surface — reuse Command Deck's table
grammar (PROMPT 6 sets the case-file pattern; this reuses its table pattern from
`SCREEN_SPECS.md` §2.5's grammar, department-scoped).
FILES TO READ: standard, plus `SCREEN_SPECS.md` §2.10, §2.5 (table grammar reference).
BACKEND/API SOURCES: `GET /v1/dispatch/work-orders` (RLS dept-scoped — no client-side
department filter needed, but show the active department in the rail).
LAYOUT/COMPONENTS: table grammar per `DESIGN.md` §8, SLA-timer column visually dominant
and color-coded per `DESIGN.md` §5 rules (never bare text, always paired with a label).
INTERACTIONS/MOTION: Quiet tier, same pattern as Command Deck's queue.
STATES: empty/loading/error per `SCREEN_SPECS.md` §2.10, matching §2.5's pattern.
ACCESSIBILITY/PERFORMANCE: same standards as PROMPT 6.
DO NOT: do not add a department column (redundant — this queue is already scoped). Do
not duplicate Command Deck's component code — import and reuse the shared table/queue
components, apply the Ops Board theme token override only.
ACCEPTANCE CRITERIA:
- [ ] Visually distinct from Command Deck (top-binding-rule motif, lighter accent) while
      using the identical underlying table component
DOCUMENTATION: standard.

---

## PROMPT 8 — Representative Screen: City Pulse · Heatmap / Cluster View

PROJECT CONTEXT: CivicBrain.
WORKSPACE: City Pulse.
USER: `zonal_supervisor`, `admin`.
SCREEN: Heatmap/Cluster View, per `SCREEN_SPECS.md` §2.12.
GOAL: the one screen where GSAP earns its cost — spatial cluster reveal.
FILES TO READ: standard, plus `SCREEN_SPECS.md` §2.12, `DESIGN.md` §3.4/§9/§10.
BACKEND/API SOURCES: `GET /v1/gis/incidents/geojson`, `GET /v1/gis/clusters`, `GET
/v1/gis/wards/geojson`.
LAYOUT: 280px rail (layer toggles) + full-bleed MapLibre canvas; floating (not modal)
stats panel top-right on cluster select; mobile = full-screen map, toggles/stats as
bottom sheets — exact behavior per `SCREEN_SPECS.md` §2.12.
DATA VIZ: cluster circle radius from the real `--map-point-radius-cluster` formula
(`DESIGN.md` §3.4) — verify this against actual returned cluster sizes, never a fixed
decorative radius.
MOTION: GSAP cluster reveal, `duration-deliberate`/`ease-spatial`, radius 0→target on
data load/zoom change; layer toggle cross-fade `duration-base`. Reduced-motion: instant
final state, no animation, verified with `prefers-reduced-motion` forced on in testing.
LOADING/EMPTY/ERROR: basemap skeleton, "zoom out" hint at empty-cluster zoom levels,
data-layer retry banner that doesn't fail the whole map — per `SCREEN_SPECS.md` §2.12.
PERFORMANCE: MapLibre dynamically imported on this route only; GSAP dynamically imported
on this route only — confirm neither appears in any other app's bundle.
ACCESSIBILITY: cluster stats panel content is available to screen readers independent of
the map canvas (map itself is inherently limited for a11y — the data must be reachable
another way, e.g. a toggleable list view of the same cluster data).
DO NOT: do not use a default bright basemap style — use `--map-basemap-style` per
`DESIGN.md` §3.4 (confirm tile provider per `SCREEN_SPECS.md` §3 point 2 if not yet
resolved — proceed with a placeholder self-hosted/OSM style and flag it in the log if so).
ACCEPTANCE CRITERIA:
- [ ] Cluster radii verified to scale with real point counts across at least 3 different
      cluster sizes in test data
- [ ] Motion fully disabled and replaced with instant states under
      `prefers-reduced-motion: reduce`
DOCUMENTATION: standard.

---

## PROMPT 9 — Representative Screen: Karmi Sahayak · Work Order Action

PROJECT CONTEXT: CivicBrain.
WORKSPACE: Karmi Sahayak.
USER: `field_worker`.
SCREEN: Work Order Action (start/navigate/resolve), per `SCREEN_SPECS.md` §2.16.
GOAL: the core field task screen — offline-safe, one-thumb, outdoor-legible.
FILES TO READ: standard, plus `SCREEN_SPECS.md` §2.16, `UI_ARCHITECTURE.md` §5.
BACKEND/API SOURCES: `POST .../start`, `POST .../resolve` (photo + notes), queued via
IndexedDB and replayed through `POST /v1/dispatch/sync` when offline.
LAYOUT: full-screen single task, context strip top, map/navigate or photo-capture middle,
one large (≥48px, full-width) bottom-anchored primary action — exact behavior per
`SCREEN_SPECS.md` §2.16.
INTERACTIONS: `resolve` primary button stays disabled until a completion photo is
attached — no silent-skip path, enforced in the UI not just the backend.
MOTION: minimal, button press feedback only.
STATES: offline (queues locally, button shows "Saved — will sync" not a false "Done"),
upload-in-progress, conflict-pending (if this work order already has an open
`dispatch_conflict_review`, show that plainly) — per `SCREEN_SPECS.md` §2.16.
ACCESSIBILITY: contrast ≥7:1 unconditionally (`DESIGN.md` §5/§12), all controls ≥48px.
PERFORMANCE: this app's core bundle budget is 200KB gzipped (`UI_ARCHITECTURE.md` §8) —
this screen is the bulk of that budget, keep it lean.
DO NOT: do not ever show "Done"/"Completed" language for an action that's actually still
queued offline — that's a trust-breaking lie to a field worker who needs to know their
work really landed.
ACCEPTANCE CRITERIA:
- [ ] Full flow tested with network disabled: action queues, badge updates, no false
      success state shown
- [ ] Resolve blocked without a photo, tested explicitly
DOCUMENTATION: standard.

---

## PROMPT 10 — Representative Screen: Control Room · AHP Weight Calibration

PROJECT CONTEXT: CivicBrain.
WORKSPACE: Control Room.
USER: `admin`.
SCREEN: AHP Weight Calibration, per `SCREEN_SPECS.md` §2.22.
GOAL: the highest-stakes config screen in the product — get the hard-block-on-invalid
behavior exactly right.
FILES TO READ: standard, plus `SCREEN_SPECS.md` §2.22, `PROJECT_REFERENCE_FOR_FRONTEND.md`
§3.3/§5.5 (AHP matrix endpoints and consistency validation).
BACKEND/API SOURCES: `GET /v1/prioritization/ahp/matrix`, `GET .../active`, `PUT
/v1/prioritization/ahp/matrix`.
LAYOUT: `content-width-form`-capped 5×5 pairwise matrix editor, mono numerals, clear
S/R/E/C/U row/column labels, live-recalculated Consistency Ratio visually dominant, the
currently-active comparison shown alongside the editable draft — exact composition per
`SCREEN_SPECS.md` §2.22.
INTERACTIONS: save button is **disabled**, not merely warned, whenever CR exceeds the
backend's consistency threshold — recalculate CR client-side on every cell edit for
immediate feedback, but the backend `PUT` remains the source of truth for the actual
validation (client-side check is a UX aid, never a substitute for server validation).
MOTION: Quiet; save success gets the `SealMark` treatment (this is a real, consequential
commit — mark it as such).
STATES: CR-invalid (save blocked, inline guidance on which specific comparison to
revisit), save success, save error (server rejects for a reason the client check
missed — surface the server's actual validation message, don't paper over it).
ACCESSIBILITY: matrix cells are keyboard-navigable in a logical grid order, CR value is
announced on every recalculation via an `aria-live` region.
DO NOT: do not let the client-side CR check silently diverge from the backend's — if the
backend rejects a save the client thought was valid, treat that as a bug to log loudly
in `IMPLEMENTATION_LOG.md`, not something to hide from the admin.
ACCEPTANCE CRITERIA:
- [ ] Save genuinely blocked (not just visually discouraged) when CR exceeds threshold
- [ ] A deliberately inconsistent matrix fixture tested end to end
DOCUMENTATION: standard.

---

## PROMPT 11 — Representative Screen: Transparency Board · Nagar Pragati

PROJECT CONTEXT: CivicBrain.
WORKSPACE: Transparency Board (Astro).
USER: public, media.
SCREEN: Nagar Pragati City Feed, per `SCREEN_SPECS.md` §2.24.
GOAL: the public's front page — sets the editorial Fraunces + Lenis-scroll pattern that
Ward Report Card (PROMPT 30) reuses.
FILES TO READ: standard, plus `SCREEN_SPECS.md` §2.24, `DESIGN.md` §6/§9.
BACKEND/API SOURCES: `GET /v1/transparency/pragati`.
LAYOUT: hero metric block (one real headline number, Fraunces label + Plex Mono
numeral) → short editorial framing paragraph → grid of secondary real metrics, each
linking to its source (ward report cards, the ledger) → recent notable ledger entries —
exact composition per `SCREEN_SPECS.md` §2.24.
MOTION: Expressive — Lenis smooth scroll, `duration-slow`/`ease-spatial` section
reveals, one reveal per section not per element, reduced-motion disables all of it
cleanly.
PERFORMANCE: this is THE public/SEO page — Lighthouse ≥90 on simulated Moto G4/Slow 4G
is a hard requirement here specifically (`UI_ARCHITECTURE.md` §8); ship this as a mostly-
static Astro page with React islands only where genuinely interactive.
ACCESSIBILITY: Fraunces headline number still has a plain-text numeric equivalent
readable by screen reader (large display type sometimes renders oddly for some SR/
font-rendering combos — verify).
DO NOT: do not fabricate or round metrics in a way that isn't traceable to the API
response. Do not add a decorative chart without a real dataset behind it (`DESIGN.md`
§14).
ACCEPTANCE CRITERIA:
- [ ] Lighthouse Performance ≥90 verified on a throttled profile before this prompt is
      marked complete
- [ ] Every number on the page traces to a field in the `/v1/transparency/pragati`
      response
DOCUMENTATION: standard.

---

## PROMPTS 12–33 — Remaining Screens (compact form)

Each follows the same contract as PROMPTS 5–11 (standalone, same standard FILES TO READ
and DOCUMENTATION clauses apply — include them in full when pasting any of these into
Antigravity) but points entirely at the already-complete design in `SCREEN_SPECS.md` for
layout/imagery/motion/states, since that detail is not repeated here. Backend sources
are the endpoint(s) named; DO NOT items beyond the global `DESIGN.md` §14 list are only
called out where a screen has a specific trap.

| # | Screen | Workspace | User | Screen spec § | Endpoint(s) | Specific DO NOT |
|---|---|---|---|---|---|---|
| 12 | Home / Report an Issue | Nagrik Setu | citizen | 2.1 | local cache only | Don't build a "my reports" API-backed list — no such endpoint exists |
| 13 | New Report Flow | Nagrik Setu | citizen | 2.2 | `POST /v1/intake/reports`, `.../photo`, `/v1/nlp/analyze` | Category step must read "citizen-declared," never imply AI detection |
| 14 | Resolution Confirm/Dispute | Nagrik Setu | citizen | 2.4 | `POST .../confirm`, `.../dispute` | — |
| 15 | Incident Queue | Command Deck | dispatcher, admin | 2.5 | `GET /v1/incidents` | Never blank the table on a background refetch error — keep last-good data |
| 16 | Prioritization Re-run | Command Deck | dispatcher, admin | 2.7 | `POST /v1/prioritization/evaluate` | Don't fake a "calculating" delay if the response is already fast |
| 17 | Conflict Adjudication Queue | Command Deck | dispatcher, admin | 2.8 | `GET /v1/dispatch/conflicts`, `POST .../adjudicate` | No default-selected decision — force an explicit choice |
| 18 | Work Order Dispatch | Command Deck | dispatcher, dept staff | 2.9 | `POST /v1/dispatch/work-orders` | Empty field-worker list needs a real next step, not a dead end |
| 19 | Work Order Detail | Ops Board | department_staff | 2.11 | (confirm exact shape vs live OpenAPI) | Reuse Incident Detail's split-pane component; do not reimplement it. Use the 5-state `work_order_status_enum` timeline, not the 11-state incident one |
| 20 | Causal Graph View | City Pulse | zonal_supervisor, admin | 2.13 | `GET /v1/causal/links`, `.../downstream`, `POST /v1/causal/links` | Not a literal corkboard — clean directed graph |
| 21 | ETA / Confidence Panel | City Pulse | zonal_supervisor, admin | 2.14 | `GET /v1/analytics/incidents/{id}/eta` | Low confidence must be visually prominent, not fine print |
| 22 | My Work Orders | Karmi Sahayak | field_worker | 2.15 | `GET /v1/dispatch/work-orders/my` | Must render from cache before any network call resolves |
| 23 | Sync Status | Karmi Sahayak | field_worker | 2.17 | local queue + `GET /v1/dispatch/sync/conflicts` | Per-mutation retry, never a blanket silent failure |
| 24 | Staff Directory | Control Room | admin | 2.18 | `GET/POST /v1/admin/users` | Zero accent color per Control Room theme — resist adding one |
| 25 | Bulk Import | Control Room | admin | 2.19 | `POST /v1/admin/users/import` | Row-level errors, never one aggregate count; confirm dry-run vs commit param shape against live OpenAPI first |
| 26 | Org Hierarchy | Control Room | admin | 2.20 | `GET /v1/orgs/{id}/hierarchy`, `POST .../departments`, `.../representative` | Indentation-based tree, not a decorative box-and-connector org chart |
| 27 | Taxonomy Governance | Control Room | admin | 2.21 | `GET/POST /v1/taxonomy/categories`, `POST .../approve` | Proposed vs. approved must be visually distinct (dashed vs. `SealMark`) |
| 28 | Service-Time Priors | Control Room | admin | 2.23 | `GET/POST /v1/analytics/priors` | Same instrument-panel register as AHP, don't under-build it as an afterthought |
| 29 | Public Ledger | Transparency Board | public, media | 2.25 | `GET /v1/transparency/ledger` | Stamped/perforated visual treatment, not a generic search-results list |
| 30 | Case Provenance Chain | Transparency Board | public, media | 2.26 | `GET .../ledger/incidents/{id}/chain` | Plain-language transition is primary; hashes are secondary/mono/small |
| 31 | Ward Report Card | Transparency Board | public, corporator | 2.27 | `GET /v1/analytics/wards/{id}/report-card` | Clean data table, not a card-grid dashboard |
| 32 | Councilor Digest | Transparency Board | corporator | 2.28 | `GET /v1/analytics/corporator/digest` | Auth-scoped to own ward only — verify RLS is actually enforced client-side too (don't rely on the API alone if a stray route param could leak another ward's data in the UI) |
| 33 | Read-only Civic Assistant | Transparency Board | public | 2.29 | `POST /v1/transparency/assistant/query` | Must visually disclose it's deterministic/templated, never presented as a general chatbot |

---

## PROMPT 34 — Responsive Refinement Pass

PROJECT CONTEXT: CivicBrain, all screens from PROMPTS 5–33 now exist.
WORKSPACE: all.
GOAL: verify and fix every screen against the full breakpoint table in `DESIGN.md` §11 —
this is a dedicated pass, not a per-screen afterthought.
FILES TO READ: standard, plus `DESIGN.md` §11 in full.
DO NOT: do not simply shrink desktop layouts — verify each screen actually uses its
specified breakpoint-specific pattern (list-row vs. table, sheet vs. dialog, etc.) per
`DESIGN.md` §11 and `SCREEN_SPECS.md`.
ACCEPTANCE CRITERIA:
- [ ] Every screen tested at all 5 breakpoints from `DESIGN.md` §11
- [ ] Any screen found deviating gets a fix, logged individually in
      `IMPLEMENTATION_LOG.md` (one entry per screen fixed, not one combined entry)
DOCUMENTATION: standard.

---

## PROMPT 35 — Motion Pass

PROJECT CONTEXT: CivicBrain, all screens now functionally complete.
WORKSPACE: all.
GOAL: verify every animated element matches its assigned motion tier (`DESIGN.md` §9)
and that `prefers-reduced-motion` is honored everywhere without exception.
FILES TO READ: standard, plus `DESIGN.md` §9/§10 in full.
DO NOT: do not add any new decorative motion during this pass — this is a verification
and correction pass, not a chance to add flourish.
ACCEPTANCE CRITERIA:
- [ ] Every Expressive-tier moment (City Pulse cluster reveal, Nagar Pragati scroll
      reveal, Nagrik Setu submit/confirm `SealMark`) verified against its spec
- [ ] Every Quiet-tier surface (Command Deck, Ops Board, Control Room, Karmi Sahayak)
      verified to have zero decorative motion
- [ ] `prefers-reduced-motion: reduce` tested globally, confirmed every animation
      degrades to an instant state change
DOCUMENTATION: standard.

---

## PROMPT 36 — Accessibility Pass

PROJECT CONTEXT: CivicBrain, all screens functionally complete.
WORKSPACE: all.
GOAL: run the full `DESIGN.md` §12 checklist against every screen and fix violations.
FILES TO READ: standard, plus `DESIGN.md` §12 in full, `AUDIT.md` category 5.
ACCEPTANCE CRITERIA:
- [ ] Keyboard-only pass completed on Command Deck queue and Control Room forms
      specifically (highest-complexity interactive surfaces)
- [ ] Contrast verified ≥7:1 on all Karmi Sahayak screens unconditionally
- [ ] No status/confidence/priority element found relying on color alone
- [ ] Every violation found gets its own `IMPLEMENTATION_LOG.md` entry
DOCUMENTATION: standard.

---

## PROMPT 37 — Visual Polish / Anti-Slop Pass

PROJECT CONTEXT: CivicBrain, all screens functionally complete and responsive/motion/
a11y-verified.
WORKSPACE: all.
GOAL: run the `DESIGN.md` §14 banned-pattern checklist and the `AUDIT.md` §7 checklist
against every screen; this is the final pass before the product is considered v1-ready.
FILES TO READ: standard, plus `DESIGN.md` §14 and `AUDIT.md` in full.
DO NOT: anything on the `DESIGN.md` §14 list. Reject a pattern because it's unearned,
not because it's trendy — don't strip something intentional (e.g. the one Fraunces
headline per Transparency Board page) in an overcorrection.
ACCEPTANCE CRITERIA:
- [ ] Every item in `DESIGN.md` §14 explicitly checked against every screen
- [ ] Every item in `AUDIT.md` §1–7 checked, with findings written into `AUDIT.md`'s
      "Findings log" section (not just `IMPLEMENTATION_LOG.md` — this is the one prompt
      that also updates `AUDIT.md` directly, since it IS the audit)
- [ ] Any remaining gap gets a prioritized repair note in `AUDIT.md` per its "Repair-
      prompt priority convention" section
DOCUMENTATION: standard, plus the `AUDIT.md` update above.
