## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page at `/sbom/compare` with the header toolbar (SBOM selectors, Compare button, Export dropdown) and vertically stacked collapsible diff sections, following the Figma design. The page reads `left` and `right` query parameters from the URL for shareable comparisons, and uses the `useSbomComparison` hook from Task 5 to fetch diff data.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to `SbomComparePage`

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM Select dropdowns, Compare button, and Export Dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable expandable section component with count badge and data table

## Implementation Notes
- Follow the page structure pattern from `src/pages/SbomListPage/SbomListPage.tsx`: page directory with main component, test file, and `components/` subdirectory.
- Register the route in `src/routes.tsx` following the existing route definition pattern (lazy-loaded page component).

**Figma design — PatternFly component mapping:**
- **SBOM selectors**: use PatternFly `Select` (single, typeahead variant). Fetch SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version (e.g., "my-product-sbom v2.3.1").
- **Compare button**: PatternFly `Button` (primary variant). Disabled until both selectors have values. On click, update URL query params and trigger comparison fetch.
- **Export dropdown**: PatternFly `Dropdown` (secondary). Two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded.
- **Diff sections**: PatternFly `ExpandableSection` for each diff category. Default expanded for sections with >0 items, collapsed for empty sections.
- **Count badges**: PatternFly `Badge` in each section title. Colors: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- **Data tables**: PatternFly composable `Table` inside each section with sortable columns. Use virtualization (e.g., `react-window` or PatternFly virtualized table) for sections with >100 rows per NFR.
- **Severity indicators**: reuse existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` in the New Vulnerabilities and Resolved Vulnerabilities sections.
- **Empty state**: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Show when no comparison has been performed (page load without query params).
- **Loading state**: PatternFly `Skeleton` placeholders in each diff section while the API call is in progress. Disable the toolbar during loading.

**Diff section table columns (from Figma):**
1. Added Packages: Package Name, Version, License, Advisories (count)
2. Removed Packages: Package Name, Version, License, Advisories (count)
3. Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
4. New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package — rows with severity "Critical" get highlighted background
5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
6. License Changes: Package Name, Left License, Right License

**URL-shareable comparison**: read `left` and `right` from `useSearchParams()`. When both are present on page load, auto-trigger the comparison. When the user clicks Compare, update the URL search params so the comparison is bookmarkable.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — reuse directly for severity display in vulnerability diff sections
- `src/components/EmptyStateCard.tsx` — reference pattern for empty state, though this page uses PatternFly EmptyState directly with custom icon and text
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar layout patterns
- `src/hooks/useSboms.ts` — reuse to populate the SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly Table composable pattern with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for rendering advisory data with severity badges

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] SBOM selectors load and display available SBOMs from the existing `useSboms` hook
- [ ] Compare button triggers comparison API call and displays results in diff sections
- [ ] Each diff category renders in its own collapsible `ExpandableSection` with correct count badge color
- [ ] Data tables display correct columns per section as specified in the Figma design
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading skeleton displays while comparison API call is in progress
- [ ] URL query params (`left`, `right`) are read on page load and updated on Compare click for shareable URLs
- [ ] Export dropdown is present and disabled until comparison is loaded

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders diff sections with correct data after comparison API returns
- [ ] Unit test: Compare button is disabled when fewer than two SBOMs are selected
- [ ] Unit test: URL search params are updated when Compare is clicked
- [ ] Unit test: Critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] E2E test in `tests/e2e/`: full comparison workflow — select two SBOMs, click Compare, verify diff sections appear

## Dependencies
- Depends on: Task 5 — Add SBOM comparison API types and client (trustify-ui)

[sdlc-workflow] Description digest: sha256:25d244d7005a2bd84b38a9cd806c05f580c7b6d57f0787f0149b858c4a9d629e
