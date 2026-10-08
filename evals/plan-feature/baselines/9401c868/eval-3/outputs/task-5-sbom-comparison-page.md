## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page UI at `/sbom/compare` following the Figma design. The page includes a header toolbar with SBOM selectors and action buttons, vertically stacked collapsible diff sections with data tables, empty state when no comparison is loaded, and loading skeletons during API calls. The URL encodes both SBOM IDs as query parameters for shareable bookmarks.

## Files to Modify
- `src/routes.tsx` -- add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main comparison page component with SBOM selectors, compare button, export dropdown, and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section component with count badge and data table
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` -- header toolbar with SBOM Select dropdowns, Compare button, and Export dropdown
- `tests/mocks/fixtures/sbom-comparison.json` -- mock comparison response data for tests

## Implementation Notes
- **Figma design reference**: The comparison view is a full-page layout with a header toolbar and vertically stacked collapsible diff sections.

- **Header toolbar (ComparisonToolbar component)**:
  - Left SBOM selector: PatternFly `Select` (single, typeahead) showing SBOM name and version. Pre-populated from URL query param `left`. Fetches SBOM list via existing `useSboms` hook.
  - Right SBOM selector: identical PatternFly `Select` for the second SBOM. Pre-populated from URL query param `right`.
  - "Compare" button: PatternFly `Button` (primary variant), disabled until both selectors have values. Triggers the comparison API call by updating URL query params.
  - "Export" dropdown: PatternFly `Dropdown` (secondary variant) with two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded. (Non-MVP but included per Figma design.)

- **Diff sections (DiffSection component)**: Each section is a PatternFly `ExpandableSection` with:
  - Title and count `Badge` (color varies: green for added/resolved, red for removed/new vulns, blue for version changes, yellow for license changes)
  - PatternFly composable `Table` with sortable columns. Use virtualized rendering for sections with >100 rows (NFR).
  - Sections default to expanded when item count > 0.
  - Section order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
  - New Vulnerabilities table: use existing `SeverityBadge` component for the severity column. Rows with severity "Critical" have a highlighted background (e.g., `--pf-v5-global--danger-color--100` background).

- **Diff section table columns**:
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License

- **Empty state**: When no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Use existing `EmptyStateCard` component as reference.

- **Loading state**: While comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading.

- **URL-shareable comparison**: Read `left` and `right` from URL search params on mount. When the user clicks "Compare", update the URL search params via React Router's `useSearchParams`. This makes the comparison URL bookmarkable and shareable (UC-2).

- Per CONVENTIONS.md §Page structure: create dedicated directory under `src/pages/` with main component, test file, and `components/` subdirectory.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` page component scope.
- Per CONVENTIONS.md §Component library: use PatternFly 5 components for all UI elements.
  Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` routing file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- existing severity badge component; use in the New Vulnerabilities and Resolved Vulnerabilities diff sections
- `src/components/EmptyStateCard.tsx` -- existing empty state pattern; reference for the "no comparison" empty state
- `src/components/LoadingSpinner.tsx` -- existing loading indicator; reference for loading state pattern (use Skeleton instead per Figma)
- `src/hooks/useSboms.ts` -- existing hook for fetching SBOM list; use for populating the SBOM selector dropdowns
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` -- existing page with tabs; reference for page structure with sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- existing package table component; reference for table rendering patterns with PatternFly Table
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping; use for sorting vulnerabilities by severity

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Left and right SBOM selectors use PatternFly `Select` (single, typeahead) and populate from the SBOM list
- [ ] "Compare" button is disabled until both selectors have values
- [ ] Clicking "Compare" calls the comparison API and renders diff sections
- [ ] URL query params `left` and `right` are updated when comparison is triggered
- [ ] Page pre-populates selectors from URL query params on mount (shareable URL)
- [ ] Six diff sections render as PatternFly `ExpandableSection` components in the correct order
- [ ] Each section shows a count `Badge` with the correct color (green/red/blue/yellow)
- [ ] Sections with >0 items default to expanded; empty sections default to collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] SeverityBadge component is used for severity display in vulnerability sections
- [ ] Empty state displays when no comparison is active (no query params)
- [ ] Loading skeletons display while comparison API call is in progress
- [ ] Export dropdown shows "Export JSON" and "Export CSV" options (disabled until comparison loads)
- [ ] Large diffs (>100 items) use virtualized rendering

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page pre-populates selectors from URL query params
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button triggers API call when both SBOMs are selected
- [ ] Unit test: diff sections render with correct data from mock comparison response
- [ ] Unit test: Critical severity rows have highlighted background
- [ ] Unit test: Export dropdown is disabled when no comparison result is loaded
- [ ] MSW handler for `GET /api/v2/sbom/compare` returns mock fixture data

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 4 -- Add SBOM comparison API types, client function, and React Query hook
