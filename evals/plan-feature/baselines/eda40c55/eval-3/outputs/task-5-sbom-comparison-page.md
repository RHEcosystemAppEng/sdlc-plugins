## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page component at `/sbom/compare` that renders a side-by-side diff between two SBOMs. The page includes a header toolbar with SBOM selectors, a Compare button, and an Export dropdown, followed by six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). The page reads SBOM IDs from URL query parameters for shareable URLs. For diffs with more than 100 changed packages, virtualized lists prevent browser freezing.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section with count badge and data table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` -- header toolbar with SBOM selectors, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` -- add route for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)

## Implementation Notes
- **Page layout** (per Figma design):
  - Header toolbar at the top with two PatternFly `Select` components (single, typeahead) for left and right SBOM selection, a primary `Button` ("Compare"), and a secondary `Dropdown` ("Export" with "Export JSON" and "Export CSV" items).
  - Below the toolbar, six `ExpandableSection` components, one per diff category, each containing a composable `Table` with sortable columns.
  - SBOM selectors fetch the SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version (e.g., "my-product-sbom v2.3.1").
  - Compare button is disabled until both selectors have values. Export dropdown is disabled until comparison data is loaded.
- **URL-shareable comparison**:
  - Read `left` and `right` query parameters from the URL using React Router's `useSearchParams`.
  - Pre-populate selectors from URL params on page load.
  - When the user clicks Compare, update the URL query params so the comparison is bookmarkable.
- **Diff sections** (per Figma design -- each section uses PatternFly `ExpandableSection` with `Badge`):
  1. **Added Packages** -- Badge color: green. Table columns: Package Name, Version, License, Advisories (count).
  2. **Removed Packages** -- Badge color: red. Table columns: Package Name, Version, License, Advisories (count).
  3. **Version Changes** -- Badge color: blue. Table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
  4. **New Vulnerabilities** -- Badge color: red. Table columns: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have a highlighted background (use PatternFly `isRowSelected` or custom row class with `--pf-v5-global--danger-color--100`).
  5. **Resolved Vulnerabilities** -- Badge color: green. Table columns: Advisory ID, Severity, Title, Previously Affected Package.
  6. **License Changes** -- Badge color: yellow. Table columns: Package Name, Left License, Right License.
  - Sections with >0 items are expanded by default; sections with 0 items are collapsed.
- **Empty state** (per Figma design):
  - When no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state** (per Figma design):
  - While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading.
- **Virtualization**:
  - For diff sections with >100 rows, use a virtualized table (e.g., `react-window` or PatternFly's built-in virtualization) to prevent browser freezing per the non-functional requirement.
- **Export functionality** (non-MVP but included per Figma):
  - Export JSON: serialize the `SbomComparison` data as a downloadable `.json` file using `URL.createObjectURL` and a Blob.
  - Export CSV: convert each diff section into CSV rows and trigger a download.
- Per CONVENTIONS.md §Page Structure: create the comparison page in its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.
- Per CONVENTIONS.md §Component Library: use PatternFly 5 components for all UI elements (`Select`, `ExpandableSection`, `Badge`, `Table`, `EmptyState`, `Skeleton`, `Button`, `Dropdown`). Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md §Naming: use PascalCase for component files and camelCase for utility functions. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's naming scope.
- Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests with MSW for API mocking. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's test file scope.
- Route registration: add a lazy-loaded route in `src/routes.tsx` following the pattern of existing page routes (e.g., `SbomListPage`, `SbomDetailPage`).

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- existing shared component for rendering severity levels; use in the New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` -- existing empty state component; may be usable for the comparison empty state or as a pattern reference
- `src/components/LoadingSpinner.tsx` -- existing loading indicator; reference for loading state patterns
- `src/components/FilterToolbar.tsx` -- existing toolbar component; reference for toolbar layout patterns
- `src/hooks/useSboms.ts` -- existing hook for fetching SBOM list; used by the SBOM selectors
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- existing package table component; reference for table column patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` -- existing advisory list component; reference for advisory display patterns

## Acceptance Criteria
- [ ] SbomComparePage renders at `/sbom/compare` with header toolbar and diff sections
- [ ] Left and right SBOM selectors use PatternFly `Select` (single, typeahead) and load SBOM list from the existing `useSboms` hook
- [ ] Compare button triggers the comparison API call and displays results in collapsible diff sections
- [ ] URL query parameters (`left`, `right`) are read on page load and updated when Compare is clicked
- [ ] Each diff section uses PatternFly `ExpandableSection` with a `Badge` showing the count
- [ ] New Vulnerabilities section highlights rows with "Critical" severity
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows `Skeleton` placeholders during API call
- [ ] Large diffs (>100 rows per section) use virtualized rendering

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders comparison results when mock API returns data
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: New Vulnerabilities section highlights Critical severity rows
- [ ] Unit test: URL query params are updated after clicking Compare
- [ ] Add MSW mock handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add mock comparison fixture data in `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 4 -- Add SBOM comparison API types, client function, and React Query hook
