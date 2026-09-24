# AUDIT.md — CivicBrain Frontend Audit Framework (template)

> **Status: no frontend code exists yet.** This file defines the categories and pass
> criteria used to audit each Antigravity implementation batch. Populate the "Findings"
> section under each category as real screens land — do not pre-fill fake findings.

## Audit categories & pass criteria

### 1. Design-system compliance
- Only semantic token classes used (no raw Tailwind palette/spacing bypassing tokens)
- Only the 5 approved typefaces (`DESIGN.md` §1)
- Only the 2 elevation levels / 3 radius tokens (`DESIGN.md` §2.3)
- Workspace accent matches its assigned theme token file, not hardcoded

### 2. Backend-truth compliance
- No screen references an endpoint not in the live 46-path surface
- No fake AI confidence language; CV/NLP cold-start states rendered honestly
- No UI for specified-but-unbuilt features (Proactive Inspection, Cross-Domain Signal Correlation)
- Priority score always itemized (AHP breakdown + equity boost + confidence Z), never a bare number

### 3. UX / lifecycle correctness
- Least-advanced-child status aggregation implemented correctly on all citizen-facing status views
- Per-observation status shown independently, never collapsed
- Evidence photos treated as primary content, not attachments
- Offline states (Karmi Sahayak, Nagrik Setu drafts) never fail silently

### 4. Responsiveness
- Karmi Sahayak: single-hand, thumb-zone reachable, tested at common low-end Android widths
- Staff console: usable down to 1280px, graceful beyond
- Nagrik Setu / Transparency Board: mobile-first, tested 360px–414px

### 5. Accessibility (WCAG 2.1 AA)
- Color never the sole carrier of status/confidence meaning
- Evidence photo alt text present and descriptive
- Karmi Sahayak contrast ≥7:1
- Full keyboard navigation on staff console (table/queue screens especially)

### 6. Performance
- Budgets from `UI_ARCHITECTURE.md` §8 met per app
- Route-based code splitting per workspace confirmed (no cross-workspace bundle bleed)

### 7. Anti-AI-slop
- Full checklist from `DESIGN.md` §7 run against each new screen

## Findings log

*(empty — first entries added after first Antigravity implementation batch is reviewed)*

## Repair-prompt priority convention

When findings exist, repair prompts to Antigravity are generated in this order:
**backend-truth violations → lifecycle correctness → accessibility → design-system
compliance → anti-slop → performance → polish.** Never let a cosmetic fix precede a
factual/backend-truth fix.
