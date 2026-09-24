# SCREEN_SPECS.md — CivicBrain Complete Frontend Architecture & Screen Design

> Full sitemap, shared component architecture, and per-screen design (layout,
> composition, visual storytelling, imagery, motion, states, real backend data mapping)
> for all 7 workspaces. This is where "what to build" lives. `ANTIGRAVITY_PROMPTS.md`
> converts this into paste-ready implementation prompts and references this file's
> section numbers instead of repeating them. Visual system rules (tokens, type, color,
> motion levels, component grammar) live in `DESIGN.md` — this file only adds
> screen-specific decisions on top of that system.

---

## 0. Complete sitemap (4 deployables, per `UI_ARCHITECTURE.md` §1)

### 0.1 `apps/nagrik-setu` (public, anon + Phone OTP)
| Route | Screen | Primary user | Primary goal |
|---|---|---|---|
| `/` | Home / Report an Issue | Citizen | Start a report or track an existing one |
| `/report/new/capture` → `/location` → `/category` → `/review` | New Report Flow | Citizen | Submit photo/voice/text + GPS report |
| `/track` | Track lookup | Citizen | Find a report by token or phone |
| `/track/:token` | Track Report detail | Citizen | See per-observation status |
| `/track/:token/confirm` | Resolution Confirm | Citizen | Confirm satisfactory resolution |
| `/track/:token/dispute` | Resolution Dispute | Citizen | Dispute a premature/unsatisfactory closure |

### 0.2 `apps/staff-console` (authenticated, role-gated — Command Deck / Ops Board / City Pulse / Control Room)
| Route | Screen | Role(s) | Primary goal |
|---|---|---|---|
| `/deck` | Incident Queue | `dispatcher`, `admin` | City-wide triage |
| `/deck/incidents/:id` | Incident Detail | `dispatcher`, `admin` | Full case view, status control |
| `/deck/prioritize/:id` | Prioritization Re-run | `dispatcher`, `admin` | Re-score, see diff |
| `/deck/conflicts` | Conflict Adjudication Queue | `dispatcher`, `admin` | Resolve offline sync collisions |
| `/deck/dispatch/new` | Work Order Dispatch | `dispatcher`, `department_staff` | Create/assign a work order |
| `/ops` | Department Queue | `department_staff` | Dept-scoped queue |
| `/ops/work-orders/:id` | Work Order Detail | `department_staff` | SLA, evidence, assignment |
| `/pulse` | Heatmap / Cluster View | `zonal_supervisor`, `admin` | Spatial hotspot analysis |
| `/pulse/causal` | Causal Graph View | `zonal_supervisor`, `admin` | Root-cause/symptom mapping |
| `/pulse/eta/:incidentId` | ETA / Confidence Panel | `zonal_supervisor`, `admin` | Completion estimate + interval |
| `/control/staff` | Staff Directory | `admin` | List/manage staff accounts |
| `/control/staff/import` | Bulk Import | `admin` | CSV batch onboarding |
| `/control/hierarchy` | Org Hierarchy | `admin` | Org → Zone → Ward → Dept tree |
| `/control/taxonomy` | Taxonomy Governance | `admin` | Category propose/approve |
| `/control/ahp` | AHP Weight Calibration | `admin` | Pairwise matrix, Consistency Ratio |
| `/control/priors` | Service-Time Priors | `admin` | Recalibrate repair-time baselines |

### 0.3 `apps/karmi-sahayak` (field_worker, offline-first PWA)
| Route | Screen | Primary goal |
|---|---|---|
| `/my-orders` | My Work Orders | See assigned tasks, offline-cached |
| `/orders/:id` | Work Order Action | Start / navigate / resolve with photo proof |
| `/sync` | Sync Status | Queued mutation count, disputed items |

### 0.4 `apps/transparency-board` (Astro, public + corporator auth)
| Route | Screen | Primary user | Primary goal |
|---|---|---|---|
| `/` | Nagar Pragati City Feed | Public, media | City-wide progress at a glance |
| `/ledger` | Public Ledger | Public, media, corporators | Search the audit trail |
| `/ledger/:incidentId` | Case Provenance Chain | Public, media | Full history of one case |
| `/wards/:wardId/report-card` | Ward Report Card | Public, corporators | One ward's performance |
| `/corporator/digest` | Councilor Digest | `corporator` (auth) | Weekly summary for own ward |
| `/assistant` | Read-only Civic Assistant | Public | Templated civic Q&A |

---

## 1. Shared component architecture (`packages/ui`)

Build once, theme per workspace (`DESIGN.md` §4). Grouped by build priority — matches
`ANTIGRAVITY_PROMPTS.md` implementation order.

**Tier 0 — primitives** (generic, Radix-based, fully restyled): `Button`, `IconButton`,
`Field`/`Input`/`Select`/`Textarea`, `Checkbox`/`Radio`/`Switch`, `Tabs`, `Tooltip`,
`Toast`, `Dialog`, `Sheet`, `Drawer`, `Badge`/`Chip`, `Skeleton`, `EmptyState`,
`ErrorState`.

**Tier 1 — civic-specific** (the product's actual visual vocabulary):
- `ConfidenceBadge` — numeric Z value + text band + icon, never color-only.
- `ScoreBreakdown` — expandable AHP (S/R/E/C/U weighted) + equity boost + confidence,
  mono numerals, itemized per `PROJECT_REFERENCE_FOR_FRONTEND.md` §3.3 formula.
- `EvidencePhotoCard` — full-width photo, mono GPS/timestamp caption strip below,
  redaction badge, per `DESIGN.md` §7.
- `BeforeAfterPair` — two `EvidencePhotoCard`s, equal size, side-by-side ≥ tablet.
- `StatusTimeline` — the 11-state lifecycle (`FRONTEND_CONTEXT.md` §4), one instance per
  observation, renders the least-advanced-child rule at the parent level.
- `TrackingTokenDisplay` — waybill-stub styled, mono, copy-to-clipboard.
- `OfflineSyncBadge` — persistent, shows queued-mutation count, tap for `Sync Status`.
- `PriorityChip` — single-hue Marker scale per `DESIGN.md` §5, always with numeric value.
- `WardBoundaryMapLayer` / `IncidentPointLayer` / `ClusterLayer` — MapLibre layer
  wrappers, tokens from `DESIGN.md` §3.4.
- `SealMark` — the verification stamp visual for confirmed/verified states.

**Tier 2 — layout shells**: `StaffConsoleShell` (280px left rail + main), `CitizenShell`
(bottom tab bar + narrow column), `FieldShell` (single-column, bottom action bar),
`EditorialShell` (Transparency Board — top nav + 720px column).

Every Tier 0/1 component ships with `loading`/`empty`/`error` variants baked in — not
bolted on per-screen.

---

## 2. Screen specifications

Legend for **Data mapping**: `Endpoint → key response fields used → local state →
mutation (if any) → error condition handled`.

### NAGRIK SETU

#### 2.1 Home / Report an Issue
- **Purpose**: single fork — start a report, or track one you already made.
- **Visual idea**: the tracking token *is* the artifact — a field waybill stub sits
  visually at the center, not a generic hero banner.
- **Layout (mobile, default)**: full-bleed `CitizenShell`. Top: workspace wordmark +
  language switch. Center: one large primary CTA card ("Report an issue" — camera icon,
  Marker-filled) stacked above a secondary flat card ("Track my report"). Bottom tab bar
  fixed.
- **Layout (tablet+)**: same stack, capped at `content-width-narrow`, centered.
- **Imagery**: none decorative — if the citizen has past reports, show up to 2 recent
  `TrackingTokenDisplay` stubs inline as quick-access, real data only.
- **Interaction**: tap CTA → `/report/new/capture`. Tap track → `/track`.
- **Motion**: Expressive-tier — CTA card has a `duration-base` press-scale only; no
  entrance animation on load (first paint must be instant).
- **States**: empty (no past reports → CTA-only), loading (fetching recent tokens from
  local cache), error (cache read fails → CTA-only, silent).
- **Data mapping**: recent tokens read from local IndexedDB draft/history store, not an
  API call — no endpoint for "my reports list" exists (citizen auth is OTP/token-based,
  not session-listing) — **do not build a "my reports" list backed by an API call that
  doesn't exist.**

#### 2.2 New Report Flow (`capture` → `location` → `category` → `review`)
- **Purpose**: submit photo/voice/text + GPS.
- **Visual idea**: a field notebook — one page (step) at a time, a visible page-count
  indicator, not a generic progress bar.
- **Layout (mobile)**: full-screen single step, large capture button (camera/mic/text
  toggle) centered, step indicator top, "back" as a text link not an icon-only control.
  `location` step shows a MapLibre pin-drop mini-map, GPS auto-detected with manual
  override. `category` step shows taxonomy chips fetched from `/v1/taxonomy/categories`
  — **labeled "What kind of issue is this?" — citizen-declared, never "AI suggests..."**
  `review` step shows the assembled `EvidencePhotoCard` + location + category before
  submit.
- **Imagery**: the citizen's own capture only, shown immediately after capture in the
  same aspect ratio it will appear in tracking later (no crop surprise).
- **Interaction**: swipe or button to advance; each step independently validated before
  "Next" enables.
- **Motion**: step transition = horizontal slide, `duration-base`, `ease-standard`
  (Responsive tier, not Expressive — this is a workflow, not a moment); the final submit
  confirmation *is* Expressive (`ease-spatial`, `duration-deliberate` — a `SealMark`
  animates in) because it's the one moment worth marking.
- **States**: capture-permission-denied (explicit re-prompt UI, not a silent failure),
  upload-in-progress (real byte-progress bar per `DESIGN.md` §10), offline (draft saved
  locally, banner: "Saved — will submit when you're back online"), submit error (retry
  affordance, draft preserved).
- **Data mapping**: `POST /v1/intake/reports` (assemble) + `POST
  /v1/intake/reports/photo` (multipart, per photo) + `POST /v1/nlp/analyze` (if voice/
  text) → response includes `tracking_token` → shown on a success screen with
  `TrackingTokenDisplay` → mutation queued to IndexedDB if offline, replayed on
  reconnect → error: 4xx validation shown inline per field, 5xx shows a plain retry.

#### 2.3 Track Report (lookup + detail)
- **Purpose**: show real, per-observation, least-advanced-child status — the screen that
  most directly embodies the product's honesty principle.
- **Visual idea**: the field waybill stub, expanded into a full status ledger.
- **Layout (lookup)**: single input (token or phone), `content-width-form`.
- **Layout (detail, mobile-first, all breakpoints)**: `TrackingTokenDisplay` at top.
  Below it, **one `StatusTimeline` per observation**, each in its own bordered card
  labeled by department + category, never merged into one bar. Parent-level banner text
  reads the least-advanced status in plain language ("Still in progress — 1 of 2 issues
  resolved"), not a technical enum value.
- **Imagery**: each observation's own evidence photo(s) shown inside its card.
- **Interaction**: tap an observation card to expand full evidence gallery for that one
  issue only.
- **Motion**: Quiet — timeline step fill is an instant/`duration-fast` state change, not
  an animated progress bar (it's not a live process, it's a fetched state).
- **States**: token-not-found (plain message + link back to `/track`), loading
  (skeleton timeline shape), multi-department split (the core case — must be default-
  tested, not an edge case), resolved-but-not-confirmed (shows the confirm/dispute CTA).
- **Data mapping**: `GET /v1/intake/reports/track` → `observations[]` with per-obs
  `status`, `department`, `evidence` → parent status computed client-side via the
  least-advanced-child rule table (`FRONTEND_CONTEXT.md` §4) from the fetched child
  statuses — **never trust a pre-collapsed parent status if the API also returns child
  detail; compute it from children so the rule is visibly correct.**

#### 2.4 Resolution Confirm / Dispute
- **Purpose**: citizen judges the work, evidence-first.
- **Visual idea**: a verification desk — before/after side by side, the decision is the
  only action on the page.
- **Layout**: `BeforeAfterPair` full-width, then two clear buttons ("Confirm resolved" /
  "Dispute this"), dispute opens a short reason field (required, plain text).
- **Motion**: confirm → `SealMark` Expressive moment, same treatment as report-submit
  success, reinforcing "this is a real seal."
- **States**: already-confirmed/already-disputed (read-only view if revisited), submit
  error (retry, input preserved).
- **Data mapping**: `POST .../confirm` or `POST .../dispute` → success updates the
  `StatusTimeline` to `confirmed` or `appealed` optimistically, reconciled on refetch.

---

### COMMAND DECK

#### 2.5 Incident Queue
- **Purpose**: city-wide triage — the dispatcher's main surface, touched dozens of times
  a day. Density and speed matter more than delight here.
- **Visual idea**: a stamped ledger — each row reads like a line in a physical logbook.
- **Layout (desktop, 1280px+)**: `StaffConsoleShell` 280px left rail (workspace switcher
  + saved filters) + fluid main. Main: a filter/search strip (sticky, 56px) → a dense
  table. Columns: Priority (`PriorityChip`, sortable, default sort), Category, Ward,
  Department, Status (`Badge`), Age, Confidence (`ConfidenceBadge`, compact). Row click
  expands an inline `ScoreBreakdown` drawer (not navigation away) OR opens `/deck/
  incidents/:id` on a dedicated "open full case" icon — **both must exist; quick-glance
  inline, full detail on demand.**
- **Layout (tablet/mobile, rare for this role but must not break)**: table collapses to
  stacked list rows (`DESIGN.md` §11), priority and status remain the two visible fields
  per row, tap to open full detail (no inline drawer on small screens).
- **Interaction**: keyboard row navigation (arrow keys + Enter to open), multi-select for
  bulk department handoff.
- **Motion**: Quiet tier only — row expand is an instant height change, no slide/bounce.
- **States**: empty ("No incidents match these filters" + clear-filters action, never
  "No data"), loading (skeleton rows matching real row height), error (inline banner,
  table retains last-good data if a refetch fails — never blank the screen on a
  background refetch error).
- **Data mapping**: `GET /v1/incidents` (filtered/paged) → table rows → row expand reads
  cached detail or triggers `GET /v1/incidents/{id}` lazily → `PATCH .../status` for
  inline status changes with optimistic update + rollback on error.

#### 2.6 Incident Detail
- **Purpose**: full case view — the "case file."
- **Visual idea**: split evidence-and-score composition — evidence is the left/primary
  argument, score is the right/supporting rationale.
- **Layout (desktop)**: 280px rail + main. Main opens with a location/context strip
  (64px, sticky: ward, category, tracking token, age). Below: a **60/40 split** —
  left 60% = observation list + evidence gallery (`EvidencePhotoCard` stack, one per
  child observation) + causal links if any; right 40% = `ScoreBreakdown` (expanded by
  default here, unlike the queue) + status control (`StatusTimeline` with staff-only
  transition buttons) + dispatch action.
- **Layout (mobile/tablet)**: stacks to evidence-then-score (100/100), score section
  collapses to a summary chip that expands on tap.
- **Imagery**: every observation's evidence, full `EvidencePhotoCard` treatment — this
  is the one staff screen where photography is large and central, not thumbnailed.
- **Interaction**: status transition buttons only show the *valid next states* from the
  11-state machine (`FRONTEND_CONTEXT.md` §4) — never a free-form status dropdown.
- **Motion**: Quiet.
- **States**: loading (skeleton split layout), error (per-section — evidence can fail to
  load independently of score data), success (status change confirmed inline, no full
  page reload).
- **Data mapping**: `GET /v1/incidents/{id}`, `GET .../observations`, `GET
  /v1/causal/links` (filtered to this incident) → `PATCH .../status` mutation with the
  valid-transitions list derived client-side from current status.

#### 2.7 Prioritization Re-run
- **Purpose**: manually re-score, see exactly what changed and why.
- **Visual idea**: a before/after ledger correction — struck-through old values, new
  values beside them, not a silent overwrite.
- **Layout**: `content-width-form`-capped panel within the Incident Detail context (a
  drawer or dedicated route). Two `ScoreBreakdown` instances side by side (before/after)
  ≥ tablet, stacked on mobile, with a diff highlight on the criterion(s) that moved.
- **Motion**: Quiet — the diff appears once data returns, no fake "calculating" delay
  (§DESIGN.md §10) unless the request genuinely takes long enough to need a skeleton.
- **States**: loading (skeleton for the "after" side only — "before" is already known),
  error (retry, "before" state untouched), no-change result (explicitly shown as "Score
  unchanged," not left ambiguous).
- **Data mapping**: `POST /v1/prioritization/evaluate` → response new score → diffed
  client-side against the currently-displayed score.

#### 2.8 Conflict Adjudication Queue
- **Purpose**: resolve offline sync collisions — a real decision with evidence on both
  sides.
- **Visual idea**: two competing claims laid side by side, like comparing two witness
  statements.
- **Layout**: list of `dispatch_conflict_review` items (list-row pattern, not a table —
  each item needs more vertical room than a table row allows). Each item expands to a
  **split pane**: left = server state at time of conflict, right = worker's offline
  claim (with the worker's evidence photo if the mutation included one). Two buttons:
  "Accept worker's change" / "Dismiss." No default selection — a real decision.
- **Motion**: Quiet.
- **States**: empty ("No pending conflicts" — a genuinely good state, phrase it that
  way, not neutrally), loading, error, success (item removed from queue with a
  `duration-fast` collapse, not a jarring instant removal).
- **Data mapping**: `GET /v1/dispatch/conflicts` → `POST .../adjudicate` with
  `decision: "accept" | "dismiss"` → optimistic removal, rollback on error.

#### 2.9 Work Order Dispatch
- **Purpose**: create/assign a new work order from an incident.
- **Visual idea**: a dispatch slip — a simple, fast form, not a wizard.
- **Layout**: `content-width-form` dialog or drawer from Incident Detail — department
  (pre-filled from incident), field-worker select (scoped to that department), SLA
  target (from `category_service_time_prior`, shown read-only with its confidence),
  notes.
- **Motion**: Quiet.
- **States**: no available field workers in this department (explicit empty state with
  a link to Control Room staff directory, not a dead-end), submit error.
- **Data mapping**: `POST /v1/dispatch/work-orders` → success closes the dialog and adds
  the row to the incident's work-order list optimistically.

---

### OPS BOARD

#### 2.10 Department Queue
- **Purpose**: this department's own work, nothing else — a lighter Command Deck.
- **Visual idea**: a clipboard — a subtle top-binding rule motif on the queue container
  distinguishes it from Command Deck's ledger-line rows even though the table grammar
  is shared.
- **Layout (desktop)**: same table grammar as 2.5, department-scoped (no department
  column — it's redundant here), SLA-timer column is the dominant visual weight
  (color-coded by `DESIGN.md` §5 confidence/status rules, never bare text).
- **Motion**: Quiet.
- **States**: same pattern as 2.5.
- **Data mapping**: `GET /v1/dispatch/work-orders` (RLS-scoped to the staff member's
  department automatically — the frontend does not need to add a department filter, but
  should still show which department is active in the rail for clarity).

#### 2.11 Work Order Detail
- **Purpose**: one work order's full picture for a supervisor.
- **Visual idea**: same evidence-forward split as Incident Detail (2.6), reused
  component-for-component — this is intentional, it's the same "case file" pattern.
- **Layout**: 60/40 evidence/meta split (desktop), stacked (mobile). Meta side: SLA
  timer (large, prominent), assigned worker, status (`work_order_status_enum` — a
  simpler 5-state `StatusTimeline` variant, not the 11-state incident one — **do not
  reuse the incident lifecycle labels here, this is a different state machine**).
- **Data mapping**: derived from `GET /v1/dispatch/work-orders` detail (or embedded in
  incident detail response — confirm exact shape against live OpenAPI before building).

---

### CITY PULSE

#### 2.12 Heatmap / Cluster View
- **Purpose**: where are the systemic hotspots, and how confident is that read.
- **Visual idea**: the coordinate-ruler map frame — City Pulse's signature: tick marks
  along the map edges reinforce "this is a surveyed space," not a generic map widget.
- **Layout (desktop)**: 280px rail (layer toggles: incidents / clusters / ward
  boundaries) + full-bleed MapLibre canvas. A floating panel (top-right, not a modal)
  shows the selected cluster's stats (`ConfidenceBadge`, sample size, category mix) when
  a cluster is clicked.
- **Layout (mobile)**: map full-screen, layer toggles collapse into a bottom sheet,
  cluster stats appear as a bottom sheet on selection.
- **Imagery**: none beyond the map itself.
- **Data viz**: cluster circles sized by real point count (`--map-point-radius-cluster`
  formula, §3.4 in DESIGN.md — never a fixed decorative size), colored by density not
  by arbitrary hue.
- **Motion**: **Expressive tier, the one place GSAP earns its cost** — cluster reveal on
  zoom/data load animates radius from 0 → target over `duration-deliberate` with
  `ease-spatial`; layer toggle cross-fades `duration-base`. Reduced-motion: clusters
  appear at final size instantly, no animation.
- **States**: loading (basemap skeleton per `DESIGN.md` §10), no clusters at current
  zoom (explicit "Zoom out to see clusters" hint, not a blank map), error (map loads,
  data layer shows a retry banner rather than failing the whole map).
- **Data mapping**: `GET /v1/gis/incidents/geojson`, `GET /v1/gis/clusters`, `GET
  /v1/gis/wards/geojson` → MapLibre GeoJSON sources → click handlers read feature
  properties into the floating stats panel.

#### 2.13 Causal Graph View
- **Purpose**: see and manually confirm root-cause → symptom relationships.
- **Visual idea**: an evidence board with string between pins — but rendered as a clean
  directed graph, not a literal corkboard cliché.
- **Layout**: 280px rail (an incident search/select to center the graph on) + main graph
  canvas (SVG or a lightweight graph lib — MapLibre is not used here, this isn't
  spatial). Selected incident centered, upstream causes to the left, downstream symptoms
  to the right, `--color-gis-causal-edge` (Channel) directional arrows.
- **Interaction**: click a node to re-center; a "link a new cause" action opens a
  `content-width-form` dialog with an incident search.
- **Motion**: Expressive — edge draw-in on graph load (`ease-spatial`,
  `duration-deliberate`), Quiet thereafter for node re-centering (instant re-layout, not
  a physics-sim reflow that would feel gimmicky).
- **States**: no causal links for this incident (explicit empty state, not a blank
  canvas), loading, error.
- **Data mapping**: `GET /v1/causal/links`, `GET /v1/causal/incidents/{id}/downstream`
  → graph nodes/edges → `POST /v1/causal/links` mutation for manual linking.

#### 2.14 ETA / Confidence Panel
- **Purpose**: show a completion estimate honestly, with its interval and its Z factor.
- **Visual idea**: not a single number — a range on a simple axis, with the confidence
  band as the axis's own visual weight (thin line at low Z, solid band at high Z).
- **Layout**: a panel within Incident Detail (2.6) or standalone route — `ScoreBreakdown`-
  adjacent styling, mono numerals for the date range, `ConfidenceBadge` explicit.
- **States**: low-confidence prominent warning language ("Calibrating on city-wide
  priors — limited local history"), not hidden in fine print.
- **Data mapping**: `GET /v1/analytics/incidents/{id}/eta` → `estimate`, `interval`,
  `confidence`/`Z` fields.

---

### KARMI SAHAYAK

#### 2.15 My Work Orders
- **Purpose**: what do I do next — nothing else competes for attention.
- **Visual idea**: a hi-vis vest, not a dashboard — near-black Station background,
  Marker-amber accents, large everything.
- **Layout (mobile only — this app is not built for tablet/desktop)**: single column,
  cards not a table, each card: category + location (large), SLA countdown (large,
  color-coded), tap-to-open. `OfflineSyncBadge` persistent at the very top, always
  visible, never collapsible.
- **Motion**: Minimal — no entrance animation, list appears instantly (offline-cached
  data should already be present before any network call resolves).
- **States**: offline (full list still usable from cache, badge shows queued count if
  any pending actions exist), empty ("No work orders assigned" — genuinely calm, not
  alarming), loading (only on first-ever launch before cache exists).
- **Data mapping**: `GET /v1/dispatch/work-orders/my` → cached to IndexedDB on every
  successful fetch so the list survives offline.

#### 2.16 Work Order Action (start / navigate / resolve)
- **Purpose**: one task, one screen, bottom-anchored primary action.
- **Visual idea**: field notebook page, same DNA as the citizen's New Report Flow (2.2)
  — deliberate echo, since both are "capture evidence in the field."
- **Layout**: full-screen single task. Top: category/location context strip. Middle:
  either a map/navigate view (before `start`) or a photo-capture view (at `resolve`).
  Bottom: one large primary button (≥48px, full-width), fixed.
- **Interaction**: `resolve` requires a completion photo — the primary button stays
  disabled until a photo is attached, no silent-skip path.
- **Motion**: Minimal — button press feedback only.
- **States**: offline (action queues locally, button shows "Saved — will sync" instead
  of a false "Done"), upload-in-progress, conflict-pending (if this exact work order has
  a `dispatch_conflict_review` open, show that plainly rather than letting the worker
  re-submit blind).
- **Data mapping**: `POST .../start`, `POST .../resolve` (photo + notes) → queued as a
  mutation object if offline, replayed via `POST /v1/dispatch/sync` on reconnect.

#### 2.17 Sync Status
- **Purpose**: transparency on what's queued and what's disputed — trust the app enough
  to work offline all day.
- **Visual idea**: a manifest — a plain list, mono timestamps, nothing decorative.
- **Layout**: list of queued mutations (type + target + queued-at) + a "Sync now"
  action + a separate section for `dispatch_conflict_review` items awaiting supervisor
  decision.
- **States**: all-synced (calm confirmation, `SealMark`), syncing (determinate progress,
  `DESIGN.md` §10), sync error (per-mutation retry, never a blanket silent failure).
- **Data mapping**: local IndexedDB queue (source of truth for "queued") + `GET
  /v1/dispatch/sync/conflicts` for disputed items.

---

### CONTROL ROOM

#### 2.18 Staff Directory
- **Purpose**: see and manage staff accounts.
- **Visual idea**: a registry ledger book — plain table, zero accent color (per
  `DESIGN.md` §2 Control Room row), every field labeled.
- **Layout**: table — name, role, scope (dept/zone/ward), status, last active. Row
  click opens edit drawer.
- **Motion**: none beyond native focus/hover.
- **Data mapping**: `GET /v1/admin/users`, `POST /v1/admin/users`.

#### 2.19 Bulk Import
- **Purpose**: CSV batch onboarding, safely.
- **Visual idea**: a dry-run preview *is* the design — the whole screen is built around
  "show me what will happen before it happens."
- **Layout**: upload zone → dry-run result table (row-by-row: will-create / will-skip /
  error, with the specific reason per row) → explicit "Confirm import" action, separate
  from upload.
- **States**: dry-run validation errors shown per-row, never as a single aggregate
  count; import-in-progress (determinate, real row count); import complete (summary +
  link to the new staff in the Directory).
- **Data mapping**: `POST /v1/admin/users/import` (dry-run mode, then confirm mode —
  confirm exact API param for dry-run vs. commit against live OpenAPI).

#### 2.20 Org Hierarchy
- **Purpose**: see and edit the Org → Zone → Ward → Department tree.
- **Visual idea**: a registry tree, indentation-based, not a decorative org chart with
  boxes and connectors.
- **Layout**: expandable tree list, department-creation and ward-corporator-assignment
  as inline actions per node, not separate pages.
- **Data mapping**: `GET /v1/orgs/{org_id}/hierarchy`, `POST .../departments`, `GET/POST
  .../wards/{id}/representative`.

#### 2.21 Taxonomy Governance
- **Purpose**: propose and approve civic categories with their severity rubric.
- **Visual idea**: a "living taxonomy" register — proposed items visually distinct
  (dashed border, provisional) from approved ones (`SealMark`).
- **Layout**: two-section list — Proposed (with approve/reject actions) and Approved
  (read-mostly, edit rubric). Category detail shows severity rubric fields explicitly.
- **Data mapping**: `GET/POST /v1/taxonomy/categories`, `POST .../{id}/approve`.

#### 2.22 AHP Weight Calibration
- **Purpose**: the highest-stakes config screen in the product — edit the pairwise
  comparison matrix that drives every priority score city-wide.
- **Visual idea**: an instrument calibration panel — the Consistency Ratio is the single
  most important number on the screen and must be visually dominant, not a footnote.
- **Layout**: `content-width-form`-capped, a 5×5 pairwise matrix editor (mono numerals,
  clear row/column labels for S/R/E/C/U), live-recalculated Consistency Ratio shown
  prominently, save button **disabled** (not just warned) when CR exceeds the
  consistency threshold — this must be a hard block, matching the backend's "strictly
  validated for consistency."
- **States**: CR-invalid (save blocked, explicit inline guidance on which comparison to
  revisit), save success (`SealMark`), view-only "currently active" comparison shown
  alongside the editable draft so the change is never silent.
- **Data mapping**: `GET /v1/prioritization/ahp/matrix`, `GET .../active`, `PUT
  /v1/prioritization/ahp/matrix`.

#### 2.23 Service-Time Priors
- **Purpose**: recalibrate city-wide baseline repair-duration priors.
- **Visual idea**: same instrument-panel register as AHP calibration, lighter stakes.
- **Layout**: table of categories with current prior (mono, with sample size/confidence)
  + an editable recalibration action.
- **Data mapping**: `GET /v1/analytics/priors`, `POST /v1/analytics/priors`.

---

### TRANSPARENCY BOARD / JAN SUNWAI LEDGER

#### 2.24 Nagar Pragati (City Feed)
- **Purpose**: the public's first impression of city-wide progress.
- **Visual idea**: an editorial front page — Fraunces headline number (the one
  legitimate use of large display type), real aggregate metrics only, Lenis scroll
  reveal as sections come into view.
- **Layout**: hero metric block (one real headline number, e.g. resolution rate, in
  Fraunces + Plex Mono for the numeral) → a short editorial framing paragraph → a grid
  of secondary real metrics (not decorative — each links to its source: ward report
  cards, the ledger) → recent notable ledger entries as a short list.
- **Motion**: Expressive — Lenis smooth scroll, section reveals `duration-slow`
  `ease-spatial`, restrained (one reveal per section, not per element).
- **Data mapping**: `GET /v1/transparency/pragati`.

#### 2.25 Public Ledger
- **Purpose**: search the immutable audit trail.
- **Visual idea**: the stamped audit trail — each entry styled with a perforated-edge/
  stamp visual treatment reinforcing "this is a permanent record," list-row pattern.
- **Layout**: search/filter strip (720px column) + chronological list rows, each row:
  timestamp (mono), incident ref, transition, `SealMark` if applicable.
- **Data mapping**: `GET /v1/transparency/ledger` (search/filter params).

#### 2.26 Case Provenance Chain
- **Purpose**: full cryptographic history for one case, readable by a non-technical
  citizen.
- **Visual idea**: the ledger entry expanded into a vertical stamped chain — each link
  a `StatusTimeline`-adjacent visual, not raw hash dumps (hashes shown in mono, small,
  secondary — the plain-language transition is primary).
- **Data mapping**: `GET /v1/transparency/ledger/incidents/{id}/chain`.

#### 2.27 Ward Report Card
- **Purpose**: one ward's performance, public and corporator-facing.
- **Visual idea**: an actual report card register — Fraunces ward name as the one
  headline, metrics below in a clean data table, not a dashboard of cards.
- **Data mapping**: `GET /v1/analytics/wards/{id}/report-card`.

#### 2.28 Councilor Digest
- **Purpose**: auth'd corporator's weekly executive summary for their ward only.
- **Visual idea**: a briefing memo — denser than the public Ward Report Card, same
  editorial register, no public-facing framing language.
- **Data mapping**: `GET /v1/analytics/corporator/digest` (auth-scoped to the
  corporator's own ward via RLS).

#### 2.29 Read-only Civic Assistant
- **Purpose**: templated multilingual civic Q&A — **must be visually labeled as
  deterministic/templated, never presented as a general-purpose chatbot** (backend is
  local deterministic templates, not an LLM — per `PROJECT_REFERENCE_FOR_FRONTEND.md`
  §5.6).
- **Layout**: simple Q&A input + response card, an explicit "How this works" disclosure
  link near the input (not hidden in a footer).
- **Data mapping**: `POST /v1/transparency/assistant/query`.

---

## 3. Missing information — smallest possible questions

These block precise implementation and cannot be guessed. See `UI_ARCHITECTURE.md` §10
for the full list; the two that block the *first* prompts in `ANTIGRAVITY_PROMPTS.md`:

1. **Repo/monorepo structure**: does the actual repo already have a package manager and
   workspace layout (pnpm/turborepo/nx), or is Antigravity creating one from scratch?
   Confirm by having Antigravity run `cat package.json` (or equivalent) at repo root and
   report back before PROMPT 0 executes.
2. **MapLibre basemap tile source**: is there a self-hosted tile server, or should
   Antigravity use a free public vector tile source (e.g. OSM-derived) for development,
   swappable later? Needed before PROMPT 9/City Pulse work — every other prompt can
   proceed without this answer.
