# UI_ARCHITECTURE.md — CivicBrain Frontend Architecture

## 1. Deployable apps (not one monolith)

The 7 workspaces split into **4 deployables** by auth model, connectivity assumption,
and performance profile — sharing a common package layer.

| App | Workspaces | Stack | Why separate |
|---|---|---|---|
| `apps/nagrik-setu` | Citizen Portal | React 18 + Vite, installable PWA | Public, anon-auth (Phone OTP), needs offline draft persistence for photo/voice reports mid-submission on poor mobile networks |
| `apps/staff-console` | Command Deck, Ops Board, City Pulse, Control Room | React 18 + Vite, SPA | Shared authenticated session (Supabase JWT), role-gated nav within one app — same login, same shell, differs by `staff_role_enum` |
| `apps/karmi-sahayak` | Field Companion | React 18 + Vite, offline-first PWA, IndexedDB queue | Separate deploy so the bundle stays minimal (low-end Android, low bandwidth); has its own offline sync engine and cannot share staff-console's heavier map/table code |
| `apps/transparency-board` | Transparency Board / Jan Sunwai | **Astro** (islands, SSG/SSR) | Public, SEO-relevant, must be fast on low-end devices; mostly read-only content — ships far less JS than a full SPA; React islands only for the ledger search and the read-only assistant |

## 2. Shared packages

```
packages/design-tokens   — tokens/{primitives,semantic,themes}.css, exported as CSS vars
                            + a generated Tailwind theme (Tailwind v4 @theme import)
packages/ui              — component library: primitives (Button, Field, Card, Chip,
                            EvidencePhoto, ConfidenceBadge, ScoreBreakdown) built on
                            Radix primitives for behavior, fully restyled — never
                            shipped with default shadcn visuals
packages/api-client       — typed client generated from /v1/openapi.json (openapi-
                            typescript + a thin fetch wrapper); regenerate on backend
                            change, never hand-write endpoint URLs in app code
packages/i18n             — react-i18next config + shared string catalog (en, hi, +
                            room for other vernaculars per §Nagrik Setu requirement)
```

## 3. Styling implementation

Tailwind CSS v4, tokens wired in via `@theme` referencing the CSS custom properties in
`design-tokens` (not Tailwind's default palette). Components never use raw Tailwind
color/spacing utilities that bypass tokens (e.g. no `bg-blue-500`) — only semantic
utility classes generated from the token set (e.g. `bg-surface`, `text-primary`,
`border-default`). Enforce via a lint rule (see `AUDIT.md` category 1) once code exists.

## 4. State & data

- **Server state**: TanStack Query throughout — every `api-client` call is wrapped in a
  query/mutation hook. No manual `useEffect` fetch chains.
- **Local/UI state**: Zustand, scoped per app (filter panels, map viewport, draft form
  state in Nagrik Setu before submit).
- **Forms**: React Hook Form + Zod schemas mirrored from backend Pydantic models —
  validation errors match backend error shapes exactly.
- **Routing**: React Router v6 (data routers) for the three SPA apps; Astro's file-based
  routing + React islands for `transparency-board`.

## 5. Offline & sync (Karmi Sahayak + Nagrik Setu draft persistence)

- Karmi Sahayak: IndexedDB mutation queue mirrors the backend's own `sync_mutation_log`
  concept — every local action (start, resolve, photo capture) is queued as a mutation
  object, replayed via `POST /v1/dispatch/sync` on reconnect. UI must show a persistent
  offline/queued-count badge (§DESIGN.md workspace table) — never silently queue.
  Conflict results (`dispatch_conflict_review`) surface to the worker as "pending
  supervisor review," not as a silent failure.
- Nagrik Setu: in-progress report drafts (photo/voice/text not yet submitted) persist to
  IndexedDB so a citizen on a flaky connection doesn't lose a half-filled report.

## 6. Maps / GIS

**MapLibre GL JS** (open-source, no vendor key required — matches the Bootstrap
Principle's zero-dependency ethos) for City Pulse (`/v1/gis/incidents/geojson`,
`/v1/gis/wards/geojson`, `/v1/gis/clusters`) and for the lightweight location pickers in
Nagrik Setu and Ops Board. Vector tile basemap from a self-hostable/OSM-derived source —
finalize provider during implementation (mark as UNKNOWN pending infra decision, do not
block design on it).

## 7. Accessibility baseline (non-negotiable, all apps)

WCAG 2.1 AA minimum. Every evidence photo has alt text describing what was reported
(citizen-entered category + location), not "photo". Every confidence/score element is
readable by screen reader with its numeric value and plain-language band ("low
confidence"), not color alone. Karmi Sahayak specifically: outdoor contrast ratio ≥7:1
(exceeds AA) because of direct-sunlight use. Full checklist lives in `AUDIT.md`.

## 8. Performance budgets

- `nagrik-setu` & `transparency-board`: target Lighthouse Performance ≥90 on a simulated
  Moto G4 / Slow 4G profile (matches likely citizen device profile in Kanpur).
- `karmi-sahayak`: JS bundle ≤200KB gzipped for the core shell (map/heavy libs
  code-split, loaded only if a screen needs them).
- `staff-console`: less constrained (desktop, office network) but still route-based
  code-splitting per workspace so Control Room code never loads for a dispatcher.

## 9. i18n

Nagrik Setu is the primary multilingual surface (per reference doc, "multilingual
intake"). English + Hindi at launch via `react-i18next`, string catalog structured to
add more vernaculars without code changes. Devanagari type pairing per `DESIGN.md` §1.
Staff apps (Command Deck/Ops Board/City Pulse/Control Room) are English-first; confirm
with product whether staff need Hindi UI — marked **UNKNOWN**, not assumed.

## 10. What's confirmed vs. what needs verification

**Confirmed from reference doc**: full API surface, DB schema, role model, lifecycle
states, auth model (Supabase JWT + RLS).

**UNKNOWN — verify before locking implementation**:
- Vector tile basemap provider/hosting for MapLibre.
- Whether staff consoles need Hindi/vernacular UI or are English-only.
- Exact CSV field spec for admin bulk staff import (affects Control Room import screen).
- Whether push notifications exist for citizens (tracking updates) — not in the API list
  above; do not design a notification center until confirmed.
