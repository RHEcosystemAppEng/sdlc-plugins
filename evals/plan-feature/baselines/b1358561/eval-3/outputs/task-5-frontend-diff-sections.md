# Task 5 — Render comparison diff sections with critical-vulnerability highlighting

**Summary:** TC-9003: Render collapsible diff sections, count badges and critical highlighting
**Issue type:** Task
**Parent (Epic):** Epic 2 — TC-9003: SBOM comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
main

## Description
Render the six diff categories of an `SbomComparison` on the comparison page (TC-9003) as
vertically stacked, collapsible PatternFly `ExpandableSection`s, each with a title, a colored
count badge and a sortable composable `Table`. Rows in "New Vulnerabilities" with severity
Critical get a highlighted background (MVP requirement "Highlight packages with new critical
vulnerabilities"). Tables with more than 100 rows are virtualized so large diffs do not freeze
the browser (NFR).

## Files to Modify
- `src/pages/sbom-compare-page/SbomComparePage.tsx` — render `<ComparisonResults comparison={data} isLoading={isLoading} />` in place of the Task 4 placeholder
- `package.json` — add a list-virtualization dependency (e.g. `@patternfly/react-virtualized-extension` or `react-window`) if none is present

## Files to Create
- `src/pages/sbom-compare-page/components/ComparisonResults.tsx` — renders the six sections in Figma order
- `src/pages/sbom-compare-page/components/DiffSection.tsx` — generic `ExpandableSection` + title + colored `Badge` + `Skeleton` loading state + table slot
- `src/pages/sbom-compare-page/components/DiffTable.tsx` — sortable composable PatternFly `Table`, virtualized when rows > 100, supports a per-row highlight predicate
- `src/pages/sbom-compare-page/components/ComparisonResults.test.tsx` — component tests
- `src/utils/comparisonLabels.ts` — display-label mapping for API enum values (direction, severity fallback)

## Implementation Notes
- **Sections, columns and badge colors (Figma, in this order):**
  1. Added Packages — Package Name, Version, License, Advisories (count) — badge green — data `comparison.added_packages`
  2. Removed Packages — Package Name, Version, License, Advisories (count) — badge red — data `comparison.removed_packages`
  3. Version Changes — Package Name, Left Version, Right Version, Direction — badge blue — data `comparison.version_changes`
  4. New Vulnerabilities — Advisory ID, Severity (`SeverityBadge`), Title, Affected Package — badge red; Critical rows highlighted — data `comparison.new_vulnerabilities`
  5. Resolved Vulnerabilities — Advisory ID, Severity, Title, Previously Affected Package — badge green — data `comparison.resolved_vulnerabilities`
  6. License Changes — Package Name, Left License, Right License — badge yellow — data `comparison.license_changes`
- `ExpandableSection` is expanded by default when the section has > 0 items, collapsed when empty (Figma component mapping).
- **Custom sub-component specifications:**
  - Count badge: PatternFly `Badge` (pill, PF default size) with section-specific fill — green = `--pf-v5-global--success-color--100`, red = `--pf-v5-global--danger-color--100`, blue = `--pf-v5-global--info-color--100`, yellow = `--pf-v5-global--warning-color--100`; white text (dark text `--pf-v5-global--Color--dark-100` on yellow for contrast). PF5 `Badge` has no color prop — apply via a className/CSS variable override, or use PF `Label` `isCompact` with `color="green|red|blue|gold"` if the reviewer prefers built-in variants.
  - Critical row highlight: full-row background `--pf-v5-global--palette--red-50` (light red; Figma gives no exact token — map to nearest PF token) on New Vulnerabilities rows whose severity is critical; keep `SeverityBadge` rendering unchanged.
- **Data component rendering scope:**
  - Each table inside its `ExpandableSection` → **per-context** — render only that section's array (e.g. New Vulnerabilities table renders `comparison.new_vulnerabilities` only); do not merge or `flatMap` categories into a single list.
  - Section count badge → **per-context** — `comparison.<category>.length` for that section only.
  - Critical highlighting → **per-context** to New Vulnerabilities only; Resolved Vulnerabilities rows with critical severity are not highlighted (resolved risk is not high-risk change).
- **Display text vs API value mismatches:**
  - Field `severity` (new/resolved vulnerabilities): Figma shows "Critical" (title case via `SeverityBadge`) but the API returns lowercase `critical` — **frontend mapping needed**; use existing `src/utils/severityUtils.ts` normalization so `SeverityBadge` receives the value it expects (verify whether it expects `Critical` or `critical`). Highlight predicate must compare case-insensitively: `severity.toLowerCase() === "critical"`.
  - Field `direction` (version changes): Figma column "Direction (upgrade/downgrade)" — API returns `upgrade` / `downgrade` — **frontend mapping needed** for display: `{ upgrade: "Upgrade", downgrade: "Downgrade" }` (optionally with PF `ArrowUpIcon` / `ArrowDownIcon`), placed in `src/utils/comparisonLabels.ts`.
  - Field `advisory_count`: Figma header "Advisories (count)" — API returns a number — **no mismatch**; render the number.
  - Package names, versions, licenses, advisory IDs and titles are rendered as returned — **no mismatch**.
- **Sorting:** all columns sortable (composable `Table` `sort` props); default sort: New Vulnerabilities by severity descending using `severityUtils` ordering, others by package name / advisory ID ascending.
- **Virtualization (NFR):** when a section has > 100 rows, render through the virtualized body (fixed row height, bounded table height); ≤ 100 rows render normally. No pagination (Figma). Sorting must operate on the full array before virtualization.
- **Loading:** when `isLoading`, each `DiffSection` renders a PatternFly `Skeleton` instead of the table.
- Per CONVENTIONS.md §Page structure: page-specific components go in the page's `components/` subdirectory; see `src/pages/SbomDetailPage/components/PackageTable.tsx` and `AdvisoryList.tsx` for table patterns.
  Applies: task creates `src/pages/sbom-compare-page/components/DiffTable.tsx` matching the convention's `src/pages/<page>/components/*.tsx` scope.
- Per CONVENTIONS.md §Shared components: reuse `src/components/SeverityBadge.tsx` (do not re-implement severity rendering).
  Applies: task creates `src/pages/sbom-compare-page/components/ComparisonResults.tsx` matching the convention's React `.tsx` component scope.
- Per CONVENTIONS.md §Component library: use PF5 `ExpandableSection`, `Badge`, `Table` (composable), `Skeleton`.
  Applies: task creates `src/pages/sbom-compare-page/components/DiffSection.tsx` matching the convention's React `.tsx` component scope.
- Per CONVENTIONS.md §Naming: camelCase for utilities (`comparisonLabels.ts`), PascalCase for components.
  Applies: task creates `src/utils/comparisonLabels.ts` matching the convention's utility `.ts` naming scope.
- Constraints (docs/constraints.md): §5.1 scope; §5.4 reuse `SeverityBadge`, `severityUtils`, `PackageTable` patterns; §2.1–2.3 commit rules; §3.3 PR `--base main`.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity rendering for vulnerability rows
- `src/utils/severityUtils.ts` — severity ordering (sorting) and normalization/color mapping
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table (columns name/version/license)
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list rendering
- `tests/mocks/fixtures/sbom-compare.json` — fixture from Task 3

## Acceptance Criteria
- [ ] Six sections render in the Figma order with the specified titles and columns
- [ ] Each section shows a count badge equal to the length of its own array, in the specified color
- [ ] Sections with > 0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with severity critical (case-insensitive) have the highlighted background; other rows do not
- [ ] Severity renders through `SeverityBadge`; direction renders as "Upgrade"/"Downgrade"
- [ ] Columns are sortable
- [ ] Sections with > 100 rows are virtualized (DOM row count bounded) and the page stays responsive with 2000 rows
- [ ] Skeletons render per section while loading

## Test Requirements
- [ ] Render test with fixture: each section title, column headers and badge count correct
- [ ] Test: only the critical New Vulnerabilities row has the highlight class; a critical row in Resolved Vulnerabilities does not
- [ ] Test: empty category → section collapsed with badge 0
- [ ] Test: 500-row Added Packages section renders fewer than 500 row elements (virtualized)
- [ ] Test: `comparisonLabels` maps `upgrade`/`downgrade` correctly
- [ ] Test: per-context rendering — Removed Packages table does not contain entries from `added_packages`

## Verification Commands
- `npm run test -- ComparisonResults` — component tests pass
- `npm run build` — build succeeds

## Dependencies
- Depends on: Task 4 — Add /sbom/compare page with SBOM selectors and URL-shareable state
