# Task 5 — Build SBOM comparison page at /sbom/compare

**Summary:** Add /sbom/compare comparison page with collapsible diff sections and shareable URL
**Issue type:** Task | **Parent (Epic):** Epic B — TC-9003: Comparison UI and navigation
**Labels:** ai-generated-jira | **Priority:** Critical | **Fix Versions:** RHTPA 1.5.0

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the comparison view from the Figma design (SBOMCompare / Comparison View): a header toolbar with left/right SBOM selectors and a Compare button, followed by six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), plus empty and loading states. The selected SBOM ids are encoded in the URL (`/sbom/compare?left={id1}&right={id2}`) so a copied URL reloads the same comparison directly (UC-2). Rows for new vulnerabilities with Critical severity are visually highlighted. Large diffs (>100 rows in a section) are virtualized to avoid freezing the browser.

The Export dropdown is rendered in the toolbar by this task in a disabled state; its behaviour is implemented in Task 7.

## Files to Modify
- `src/routes.tsx` — register lazy-loaded route `/sbom/compare` → `SbomComparePage`
- `package.json` — add a virtualization dependency for large tables if none is present (e.g., `@patternfly/react-virtualized-extension` or `react-window`; verify what is already installed first)

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — page component: toolbar, URL query-param sync, empty/loading/error states, renders the six sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests (Vitest + RTL + MSW)
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — PF5 typeahead `Select` backed by `useSboms`
- `src/pages/SbomComparePage/components/DiffSection.tsx` — `ExpandableSection` with title + colored count `Badge`, wraps a table; default expanded when count > 0
- `src/pages/SbomComparePage/components/DiffTable.tsx` — composable PF5 `Table` with sortable columns, virtualized when rows > 100, optional row highlight predicate
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E: open shared URL, sections render

## Implementation Notes
- **Backend API contracts** (consumed through Task 4's `useSbomComparison` — do not call Axios directly from the page):
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` → `SbomComparison` (`added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`) — see trustify-backend `modules/fundamental/src/sbom/endpoints/compare.rs`. `404` for unknown ids → show a PF error/empty state, not empty sections.
  - `GET /api/v2/sbom` → `{ items: SbomSummary[], total: number }` (`modules/fundamental/src/sbom/endpoints/list.rs`) via existing `useSboms` for selector options.
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.
- **URL state (shareable comparisons):** use React Router v6 `useSearchParams`; selectors are initialized from `left`/`right`. Clicking **Compare** writes both ids to the query string; the query string (not local state) drives `useSbomComparison(left, right)`, so opening a shared URL triggers the comparison without re-selecting.
- **Toolbar behaviour (Figma):** Compare is primary and disabled until both selectors have values; Export `Dropdown` (items "Export JSON", "Export CSV") disabled until a result is loaded; the whole toolbar is disabled while loading.
- **States (Figma):** no query params → PF `EmptyState`, icon `CodeBranchIcon` (fallback for `ComparisonIcon`), title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Loading → each section shows a PF `Skeleton`.
- **Section/column spec (Figma, in order):**
  1. Added Packages — Package Name, Version, License, Advisories (count) — badge green
  2. Removed Packages — Package Name, Version, License, Advisories (count) — badge red
  3. Version Changes — Package Name, Left Version, Right Version, Direction — badge blue
  4. New Vulnerabilities — Advisory ID, Severity (`SeverityBadge`), Title, Affected Package — badge red; Critical rows highlighted
  5. Resolved Vulnerabilities — Advisory ID, Severity (`SeverityBadge`), Title, Previously Affected Package — badge green
  6. License Changes — Package Name, Left License, Right License — badge yellow
- **Custom sub-component specifications:**
  - Diff count badge: PF `Badge` (pill, PF default size) with per-section color — green = `--pf-v5-global--success-color--100`, red = `--pf-v5-global--danger-color--100`, blue = `--pf-v5-global--info-color--100`, yellow = `--pf-v5-global--warning-color--100`; white text (dark text on yellow for contrast). Figma provided color names only (no hex/tokens) — tokens above are the nearest PF5 mapping; confirm with design.
  - Critical vulnerability row highlight: full-row background `--pf-v5-global--danger-color--200`-tinted / PF `danger` light background (nearest token; Figma specifies "highlighted background" without a value), text unchanged; applies only to `new_vulnerabilities` rows whose severity is critical.
- **Data component rendering scope:**
  - Each `DiffTable` inside its `DiffSection` → **per-context** — the Added Packages table renders only `comparison.added_packages`, Removed only `comparison.removed_packages`, etc.; never merge/`flatMap` arrays across sections. Count badge = length of that section's array.
  - Critical highlighting → **per-context** to the New Vulnerabilities section only (not Resolved Vulnerabilities).
- **Display text vs API value mismatches:**
  - `new_vulnerabilities[].severity` / `resolved_vulnerabilities[].severity`: Figma shows "Critical"/"High"/… but the API returns lowercase (`"critical"`) — **frontend mapping needed**; pass through `SeverityBadge`, which uses `src/utils/severityUtils.ts` for level ordering/labels. Ensure the mapping is case-insensitive (normalize to the key format `severityUtils` expects) and the Critical-row predicate compares normalized values.
  - `version_changes[].direction`: API returns `upgrade` / `downgrade`; display as "Upgrade" / "Downgrade" — **frontend mapping needed**: `{ upgrade: "Upgrade", downgrade: "Downgrade" }` (optionally with an arrow-up/arrow-down PF icon).
  - Section titles and column headers are static UI chrome — no mapping needed. Package names, versions, licenses, advisory ids/titles are displayed as returned — no mismatch.
- **Virtualization:** sections with > 100 rows render via a virtualized table body (NFR: no browser freezing on large diffs); ≤ 100 rows render the plain composable `Table`. Sorting must work in both modes. No pagination (per Figma component mapping).
- Per CONVENTIONS.md §Page structure: create `src/pages/SbomComparePage/` with `SbomComparePage.tsx`, `SbomComparePage.test.tsx` and a `components/` subdirectory for page-specific components, as in `src/pages/SbomDetailPage/`.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `src/pages/<Page>/` scope.
- Per CONVENTIONS.md §Component library: build all UI from PF5 (`Select`, `ExpandableSection`, `Badge`, composable `Table`, `EmptyState`, `Skeleton`, `Dropdown`) — no custom replacements.
  Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's React component (`.tsx`) scope.
- Per CONVENTIONS.md §Routing: add `/sbom/compare` as a React Router v6 lazy-loaded page in `src/routes.tsx`, following existing page routes.
  Applies: task modifies `src/routes.tsx` matching the convention's route-definition scope.
- Per CONVENTIONS.md §Shared components: reuse `src/components/SeverityBadge.tsx`, `src/components/EmptyStateCard.tsx`/`LoadingSpinner.tsx` where they fit; keep the new components page-specific under `SbomComparePage/components/` unless reused elsewhere.
  Applies: task creates `src/pages/SbomComparePage/components/DiffTable.tsx` matching the convention's React component (`.tsx`) scope.
- Per CONVENTIONS.md §Naming: PascalCase component files (`DiffSection.tsx`); the directory follows the existing `src/pages/` naming (existing pages use PascalCase directories such as `SbomDetailPage/`, so follow that precedent over the kebab-case rule).
  Applies: task creates `src/pages/SbomComparePage/components/SbomSelector.tsx` matching the convention's TypeScript (`.tsx`) naming scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW (`tests/mocks/handlers.ts`, fixture from Task 4) for unit tests; Playwright for E2E following `tests/e2e/sbom-list.spec.ts`.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's Vitest/RTL test scope.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.3 `--base TC-9003`; §5.1–5.8 scope, reuse, data-flow tracing (URL → hook → sections), sibling parity with `SbomDetailPage` (loading/error handling).

## Reuse Candidates
- `src/hooks/useSboms.ts` — SBOM list for both selectors (Figma: "Fetches SBOM list via existing `useSboms` hook")
- `src/hooks/useSbomComparison.ts` — comparison data (Task 4)
- `src/components/SeverityBadge.tsx` — severity column in both vulnerability sections
- `src/utils/severityUtils.ts` — severity ordering for sortable Severity column and critical detection
- `src/components/EmptyStateCard.tsx` — existing empty-state placeholder; reuse/extend for the "Select two SBOMs to compare" state
- `src/components/LoadingSpinner.tsx` — loading indicator pattern (sections use `Skeleton` per Figma)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table (columns name/version/license); reuse its column/sort setup for package diff tables
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory rendering for vulnerability sections
- `tests/e2e/sbom-list.spec.ts` — Playwright pattern

## Acceptance Criteria
- [ ] `/sbom/compare` route renders `SbomComparePage` (lazy loaded)
- [ ] With no query params the empty state ("Select two SBOMs to compare") is shown
- [ ] Both selectors list SBOMs (name + version) from `useSboms`; Compare is disabled until both are selected
- [ ] Clicking Compare updates the URL to `?left={id1}&right={id2}` and loads the diff
- [ ] Opening `/sbom/compare?left={id1}&right={id2}` directly pre-populates both selectors and renders the comparison without user interaction
- [ ] Six sections render in the Figma order with the specified columns, colored count badges, and default expanded only when count > 0
- [ ] Each section shows only its own array's rows (per-context rendering)
- [ ] New Vulnerabilities rows with critical severity have the highlighted background; Resolved rows do not
- [ ] Severity values render via `SeverityBadge` with correct labels for lowercase API values; Direction shows "Upgrade"/"Downgrade"
- [ ] Sections with > 100 rows are virtualized and remain responsive
- [ ] Loading shows `Skeleton` per section and disables the toolbar; a `404`/error shows an error state (not empty sections)
- [ ] Export dropdown is present and disabled until results load

## Test Requirements
- [ ] Unit: empty state shown with no query params
- [ ] Unit: query params pre-populate selectors and trigger the comparison (MSW fixture)
- [ ] Unit: Compare button disabled until both selected; click writes params to URL
- [ ] Unit: each section shows correct count and rows from the fixture; zero-count sections are collapsed
- [ ] Unit: critical row in New Vulnerabilities has the highlight class; non-critical rows do not
- [ ] Unit: severity `"critical"` renders the Critical `SeverityBadge`; `direction: "downgrade"` renders "Downgrade"
- [ ] Unit: error state rendered when MSW returns `404`
- [ ] Unit: a section with 150 rows renders through the virtualized table (only a window of rows in the DOM)
- [ ] E2E (Playwright): navigate to a shared compare URL and verify sections render

## Verification Commands
- `npx vitest run src/pages/SbomComparePage` — tests pass
- `npx playwright test tests/e2e/sbom-compare.spec.ts` — E2E passes
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison API types, REST function and React Query hook
