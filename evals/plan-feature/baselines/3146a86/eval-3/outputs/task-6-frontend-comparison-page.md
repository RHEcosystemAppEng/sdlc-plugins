# Task 6 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page must handle three states: empty state (no comparison yet), loading state (comparison in progress), and results state (comparison complete).

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to the new page component

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar, SBOM selectors, Compare button, Export dropdown, and diff section layout
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section wrapper using PatternFly `ExpandableSection` with count badge
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — table for added packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — table for removed packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — table for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — table for new vulnerabilities (columns: Advisory ID, Severity, Title, Affected Package) with critical row highlighting
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — table for resolved vulnerabilities (columns: Advisory ID, Severity, Title, Previously Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — table for license changes (columns: Package Name, Left License, Right License)
- `tests/mocks/fixtures/comparison.json` — mock comparison response data for tests

## Implementation Notes
- Per the frontend key conventions (Component library): all UI components must use PatternFly 5. The Figma design maps to these PF5 components:
  - SBOM selectors: `Select` (single, typeahead) — fetches SBOM list via existing `useSboms` hook
  - Diff sections: `ExpandableSection` — default expanded for sections with >0 items, collapsed for empty sections
  - Count badges: `Badge` — green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes
  - Data tables: `Table` (composable) — sortable columns, no pagination
  - Empty state: `EmptyState` with `CodeBranchIcon` as the icon, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Export button: `Dropdown` with two items: "Export JSON" and "Export CSV"
  - Loading state: `Skeleton` placeholders in each diff section while the API call is in progress
- Per the frontend key conventions (Page structure): each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory.
- Per the frontend key conventions (Routing): use React Router v6 with lazy-loaded page component. Add the route to `src/routes.tsx` following the existing pattern.
- URL-shareable comparison: the page must read `left` and `right` query parameters from the URL. When the Compare button is clicked, update the URL query parameters using `useSearchParams` from React Router so the comparison is bookmarkable.
- **New Vulnerabilities table**: rows with severity "Critical" must have a highlighted background (use PF5 danger/warning row variant or custom CSS class). Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display.
- Per the non-functional requirements: use virtualized lists for >100 changed packages to prevent browser freezing. Consider `react-window` or PF5's built-in virtualization for large tables.
- The Export dropdown should be disabled until a comparison result is loaded. Export JSON downloads the raw comparison response as a `.json` file. Export CSV converts the comparison to CSV format (one section per sheet or concatenated with section headers).
- Per constraint 5.3: follow the patterns referenced in Implementation Notes.
- Per constraint 5.4: reuse the existing `SeverityBadge`, `EmptyStateCard`, `LoadingSpinner`, and `FilterToolbar` components where applicable.

**Data component rendering scope:**
- All diff section tables render per-comparison data — each table displays results from a single `SbomComparisonResult`, scoped to its specific diff category (e.g., `AddedPackagesTable` renders only `comparison.added_packages`).

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — reuse for severity display in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — reference for empty state pattern (adapt for comparison-specific empty state)
- `src/components/LoadingSpinner.tsx` — reuse for loading states
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly table implementation with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for advisory list display patterns
- `src/hooks/useSboms.ts` — reuse for SBOM selector dropdown data
- `src/utils/severityUtils.ts` — reuse severity level ordering and color mapping for badge colors

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with the header toolbar and diff sections
- [ ] SBOM selectors fetch and display the SBOM list using the existing `useSboms` hook
- [ ] Compare button triggers the comparison API call and displays results in the diff sections
- [ ] URL query parameters `left` and `right` are updated when Compare is clicked, making the comparison shareable
- [ ] Page loads with pre-populated selectors when `left` and `right` query parameters are present in the URL
- [ ] Empty state is displayed when no comparison has been performed
- [ ] Loading state with skeleton placeholders is displayed during the API call
- [ ] Each diff section shows a count badge with the correct color
- [ ] Diff sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities table highlights rows with Critical severity
- [ ] Export dropdown offers JSON and CSV download options
- [ ] Tables handle >100 rows without browser freezing (virtualization)

## Test Requirements
- [ ] Unit test: comparison page renders empty state when no query parameters are present
- [ ] Unit test: comparison page renders loading state when comparison is in progress
- [ ] Unit test: comparison page renders diff sections with correct data from the API response
- [ ] Unit test: Compare button is disabled until both SBOM selectors have values
- [ ] Unit test: URL query parameters are updated when Compare is clicked
- [ ] Unit test: New Vulnerabilities table highlights Critical severity rows
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts` returning fixture data from `tests/mocks/fixtures/comparison.json`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add frontend API layer for SBOM comparison
