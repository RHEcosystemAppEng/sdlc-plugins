## Repository
trustify-ui

## Target Branch
main

## Description
Build the SBOM comparison page at `/sbom/compare` (TC-9003) from the Figma design "SBOMCompare — Comparison View". The page has a header toolbar with two SBOM selectors and a Compare button, and six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). Both SBOM IDs are encoded in the URL (`?left={id1}&right={id2}`) so comparisons are bookmarkable and shareable (UC-2). Rows for new vulnerabilities with Critical severity are visually highlighted. Large diffs (>100 rows in a section) use virtualized tables to avoid freezing the browser.

The Export dropdown is rendered in the toolbar as part of the layout but its behaviour is delivered in Task 6; in this task it is present and disabled.

## Files to Modify
- `src/routes.tsx` — register lazy-loaded route `/sbom/compare` → `SbomComparePage`

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — page component: reads/writes `left`/`right` URL params, composes toolbar, empty/loading/error states and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Vitest + RTL tests
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — two SBOM `Select` typeaheads, Compare button, Export dropdown placeholder
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable `ExpandableSection` with title + colored count badge + table slot
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — table for Added/Removed packages
- `src/pages/SbomComparePage/components/VersionChangeTable.tsx` — table for Version Changes
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — table for New/Resolved vulnerabilities (with critical-row highlight)
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` — table for License Changes

## Implementation Notes
- **Figma layout (SBOMCompare / Comparison View):** full-page layout, header toolbar on top, six vertically stacked collapsible diff sections in this exact order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
- **Header toolbar (PatternFly 5):**
  - Left and right SBOM selectors: PF `Select` (single, typeahead) showing "<sbom name> v<version>" (e.g., "my-product-sbom v2.3.1"); options loaded via the existing `src/hooks/useSboms.ts` hook. Pre-populated from URL params `left` / `right`.
  - "Compare" button: PF `Button variant="primary"`, disabled until both selectors have values. Clicking it writes `?left=&right=` via React Router `useSearchParams` (this is what triggers `useSbomComparison` — the URL is the single source of truth, so pasting a shared URL loads the comparison directly per UC-2).
  - "Export" button: PF `Dropdown` with a secondary toggle and items "Export JSON", "Export CSV"; disabled until a comparison result is loaded (wired up in Task 6).
  - The whole toolbar is disabled while the comparison request is loading.
- **Diff sections:** each is a PF `ExpandableSection` whose toggle shows the title plus a PF `Badge` count. Default `isExpanded` = true when the section has >0 items, false when empty.
- **Table columns (PF composable `Table`, sortable columns, no pagination):**
  1. Added Packages — Package Name, Version, License, Advisories (count) — badge green
  2. Removed Packages — Package Name, Version, License, Advisories (count) — badge red
  3. Version Changes — Package Name, Left Version, Right Version, Direction (upgrade/downgrade) — badge blue
  4. New Vulnerabilities — Advisory ID, Severity (`SeverityBadge`), Title, Affected Package — badge red; rows with severity Critical get a highlighted background
  5. Resolved Vulnerabilities — Advisory ID, Severity (`SeverityBadge`), Title, Previously Affected Package — badge green
  6. License Changes — Package Name, Left License, Right License — badge yellow
- **Custom sub-component specifications:**
  - Count badge: PF `Badge` is not color-variant; implement the colored count as PF `Label` (`isCompact`) with `color` = `green` (Added, Resolved), `red` (Removed, New Vulnerabilities), `blue` (Version Changes), `gold` (License Changes — PF5 maps Figma "yellow" to `gold`); text = item count. Alternatively wrap `Badge` with a CSS class using `--pf-v5-global--palette--green-100` / `red-100` / `blue-100` / `gold-100` backgrounds — pick one approach and use it for all six sections.
  - Critical row highlight: apply a row modifier class on `<Tr>` when `severity` is critical, background `--pf-v5-global--palette--red-50` (map Figma highlight hex to the nearest PF5 danger token), keeping text color default for contrast.
  - Direction cell: text "Upgrade" / "Downgrade" with PF `ArrowUpIcon` (success color) / `ArrowDownIcon` (warning color).
- **Empty state (no URL params):** PF `EmptyState` with icon `CodeBranchIcon` (fallback for the Figma "ComparisonIcon", which is not in PF icons), title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Reuse `src/components/EmptyStateCard.tsx` if it accepts icon/title/body props; otherwise compose PF `EmptyState` directly.
- **Loading state:** each diff section renders a PF `Skeleton` placeholder while `useSbomComparison` is loading (do not use the single full-page `src/components/LoadingSpinner.tsx` here — Figma specifies per-section skeletons).
- **Error state (fail-closed):** when the hook reports an error (e.g., 404 for an unknown SBOM ID from a stale shared URL), show a PF `Alert variant="danger"` naming the failure; never render six empty sections, which would falsely indicate "no changes".
- **Virtualization (NFR):** sections with >100 rows render virtualized rows (e.g., `@patternfly/react-virtualized-extension` or `react-window` — check `package.json` for an existing dependency before adding one). Sections ≤100 rows render a plain composable `Table`.
- **Data component rendering scope:**
  - Added Packages table inside section "Added Packages" → **per-context** — render only `comparison.added_packages`
  - Removed Packages table → **per-context** — `comparison.removed_packages`
  - Version Changes table → **per-context** — `comparison.version_changes`
  - New Vulnerabilities table → **per-context** — `comparison.new_vulnerabilities`
  - Resolved Vulnerabilities table → **per-context** — `comparison.resolved_vulnerabilities`
  - License Changes table → **per-context** — `comparison.license_changes`
  - Do not merge/flatten arrays across sections; each section's count badge = length of its own array.
- **Display text vs API value mismatches:**
  - Field `severity` in New/Resolved Vulnerabilities: Figma shows "Critical" (title case) but the API returns lowercase `critical` — **frontend mapping needed**: pass the value through the existing normalization in `src/utils/severityUtils.ts` before rendering `SeverityBadge` and before the critical-row check (compare case-insensitively): `{ critical: "Critical", high: "High", medium: "Medium", low: "Low" }`.
  - Field `direction` in Version Changes: Figma column shows upgrade/downgrade; API returns `upgrade` / `downgrade` — **frontend mapping needed** for display labels: `{ upgrade: "Upgrade", downgrade: "Downgrade" }`.
  - Selector labels: Figma shows "my-product-sbom v2.3.1"; the SBOM list API returns name and version as separate fields — compose `${name} v${version}` in the frontend.
  - Package names, licenses, advisory IDs and titles are displayed as returned — **no mismatch**.
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` → `SbomComparison` (see Task 3 / trustify-backend `modules/fundamental/src/sbom/endpoints/compare.rs`); consumed only via `src/hooks/useSbomComparison.ts` from Task 3.
  - `GET /api/v2/sbom` → SBOM list, consumed via `src/hooks/useSboms.ts`.
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.
- **Per CONVENTIONS.md §Component library:** use PF5 components exclusively (`Select`, `ExpandableSection`, `Badge`/`Label`, composable `Table`, `EmptyState`, `Skeleton`, `Dropdown`, `Alert`), as in `src/pages/SbomListPage/SbomListPage.tsx`.
  Applies: task modifies src/pages/SbomComparePage/SbomComparePage.tsx matching the convention's React `.tsx` UI component scope.
- **Per CONVENTIONS.md §Page structure:** create `src/pages/SbomComparePage/` with the main component, a test file and a `components/` subdirectory, mirroring `src/pages/SbomDetailPage/` (`SbomDetailPage.tsx`, `SbomDetailPage.test.tsx`, `components/PackageTable.tsx`).
  Applies: task modifies src/pages/SbomComparePage/components/DiffSection.tsx matching the convention's `src/pages/<Page>/components/` scope.
- **Per CONVENTIONS.md §Routing:** register the page as a lazy-loaded React Router v6 route in `src/routes.tsx`, like the existing page routes.
  Applies: task modifies src/routes.tsx matching the convention's React Router route-definition scope.
- **Per CONVENTIONS.md §Naming:** PascalCase component files (`CompareToolbar.tsx`, `DiffSection.tsx`).
  Applies: task modifies src/pages/SbomComparePage/components/CompareToolbar.tsx matching the convention's TypeScript component naming scope.
- **Per CONVENTIONS.md §Testing:** Vitest + React Testing Library with MSW mocks from `tests/setup.ts` / `tests/mocks/handlers.ts`, as in `src/pages/SbomListPage/SbomListPage.test.tsx`.
  Applies: task modifies src/pages/SbomComparePage/SbomComparePage.test.tsx matching the convention's Vitest/RTL `.test.tsx` scope.
- **Constraints (docs/constraints.md):** §2 commits (Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer); §3 PRs (`--base main`, PR link on Jira task); §5 code changes (scoped to listed files, inspect first, reuse `SeverityBadge`/`severityUtils`/`EmptyStateCard` rather than duplicating, data-flow trace URL → hook → sections); §1.4/1.5 implement-task scope rules.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge required by Figma for the Severity column
- `src/utils/severityUtils.ts` — severity ordering/color mapping; use for case normalization, critical detection and sorting the Severity column
- `src/hooks/useSboms.ts` — SBOM list for the selectors
- `src/hooks/useSbomComparison.ts` (Task 3) — comparison data
- `src/components/EmptyStateCard.tsx` — existing empty state placeholder
- `src/components/LoadingSpinner.tsx` — only if a global fallback is needed for the lazy route `Suspense`
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table; reuse column/cell patterns for `PackageDiffTable`
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory rendering patterns for `VulnerabilityDiffTable`

## Acceptance Criteria
- [ ] `/sbom/compare` renders the comparison page (lazy-loaded route in `src/routes.tsx`)
- [ ] Without URL params the empty state shows `CodeBranchIcon`, "Select two SBOMs to compare" and the specified body text
- [ ] Compare button is disabled until both selectors have a value; clicking it updates the URL to `?left={id1}&right={id2}`
- [ ] Opening `/sbom/compare?left={id1}&right={id2}` directly pre-populates both selectors and loads the comparison without further interaction (UC-2)
- [ ] Six sections render in Figma order with the specified columns and badge colors (green, red, blue, red, green, yellow/gold)
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with Critical severity have a highlighted background
- [ ] Severity renders through `SeverityBadge` with correct title-case labels from lowercase API values
- [ ] Per-section `Skeleton` placeholders show while loading and the toolbar is disabled
- [ ] An API error (e.g., 404) shows a danger alert, not empty sections
- [ ] Sections with >100 rows are virtualized and remain responsive with 2000 rows
- [ ] Export dropdown is visible with "Export JSON" / "Export CSV" items and disabled (behaviour in Task 6)

## Test Requirements
- [ ] Renders empty state when no URL params are present
- [ ] Compare button disabled state toggles with selector values
- [ ] With URL params, renders all six sections with counts from the MSW fixture
- [ ] Critical new-vulnerability row has the highlight class; non-critical rows do not
- [ ] Loading state renders skeletons in each section and disables the toolbar
- [ ] MSW 404 response renders the error alert and no diff sections (fail-closed path)
- [ ] Section with >100 rows renders a virtualized list (only a subset of rows in the DOM)

## Verification Commands
- `npx vitest run src/pages/SbomComparePage` — page tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/compare endpoint (trustify-backend)
- Depends on: Task 3 — Add SBOM comparison API client, types and React Query hook
