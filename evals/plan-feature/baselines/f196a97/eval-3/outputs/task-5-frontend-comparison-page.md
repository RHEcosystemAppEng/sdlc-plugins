# Task 5 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` with a header toolbar containing two SBOM selector dropdowns, a Compare button, and an Export dropdown. Below the toolbar, render six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) each with a count badge and data table. The page reads `left` and `right` query parameters from the URL for shareable comparisons. Support empty state, loading state, and virtualized lists for large diffs (>100 rows).

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to SbomComparePage

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section with count badge and data table
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown

## Implementation Notes
- Follow the page structure pattern from `src/pages/SbomDetailPage/`: main page component with page-specific sub-components in a `components/` subdirectory.
- **SBOM selectors:** Use PatternFly `Select` (single, typeahead) components. Populate them using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version as the option label.
- **URL-shareable comparison:** Read `left` and `right` query params from the URL using React Router's `useSearchParams()`. When both are present on page load, auto-trigger the comparison. Update the URL when the user clicks Compare.
- **Compare button:** PatternFly primary `Button`, disabled until both selectors have values. On click, call the `useSbomComparison` hook with the selected IDs.
- **Export dropdown:** PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. This is not MVP but include the UI shell with disabled state.
- **Diff sections:** Use PatternFly `ExpandableSection` for each category. Default expanded for sections with >0 items, collapsed for empty sections. Each section title includes a PatternFly `Badge` with count. Badge colors: Added Packages = green, Removed Packages = red, Version Changes = blue, New Vulnerabilities = red, Resolved Vulnerabilities = green, License Changes = yellow.
- **Data tables:** Use PatternFly composable `Table` with sortable columns. Column definitions per section:
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction
  - New Vulnerabilities: Advisory ID, Severity (use existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- **Critical vulnerability highlighting:** Rows in the New Vulnerabilities section with severity "Critical" should have a highlighted/warning background using PatternFly's `isHoverable` or custom row className.
- **Empty state:** When no comparison has been performed (no query params and no Compare clicked), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state:** While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable the toolbar during loading.
- **Virtualization:** For sections with >100 rows, use virtualized list rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization support.
- Use the existing `LoadingSpinner` from `src/components/LoadingSpinner.tsx` and `EmptyStateCard` from `src/components/EmptyStateCard.tsx` as references for loading/empty patterns.
- Route should be lazy-loaded following the pattern in `src/routes.tsx`.

## Reuse Candidates
- `src/hooks/useSboms.ts` — existing hook for loading the SBOM list used to populate the selector dropdowns
- `src/components/SeverityBadge.tsx` — existing shared component for rendering severity levels in the New/Resolved Vulnerabilities sections
- `src/components/FilterToolbar.tsx` — reusable PatternFly filter toolbar pattern, reference for toolbar layout
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern
- `src/components/LoadingSpinner.tsx` — existing loading indicator component
- `src/utils/severityUtils.ts` — severity level ordering and color mapping, useful for critical vulnerability row highlighting
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component, reference for table column definitions and sorting
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component, reference for advisory display pattern

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and loads the comparison page
- [ ] Both SBOM selector dropdowns are populated with available SBOMs
- [ ] Compare button is disabled when fewer than two SBOMs are selected
- [ ] Clicking Compare triggers the comparison API call and renders diff sections
- [ ] URL is updated with `left` and `right` query params for shareability
- [ ] Opening a URL with both query params auto-loads the comparison
- [ ] All six diff sections render with correct columns and count badges
- [ ] Badge colors match the spec (green/red/blue/yellow per section)
- [ ] Critical vulnerabilities have highlighted rows in New Vulnerabilities section
- [ ] Empty state shows when no comparison has been performed
- [ ] Loading state shows skeleton placeholders during API call
- [ ] Export dropdown is present but disabled (non-MVP placeholder)

## Test Requirements
- [ ] Unit test: renders empty state when no comparison is active
- [ ] Unit test: renders loading skeletons when comparison is in progress
- [ ] Unit test: renders all six diff sections with correct data when comparison completes
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: URL query params trigger auto-comparison on page load
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add comparison fixture data in `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison API types, client function, and React Query hook
