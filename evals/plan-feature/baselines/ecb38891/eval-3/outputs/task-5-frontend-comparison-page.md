## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page at `/sbom/compare` with the full UI layout from the Figma design: a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown, followed by six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). The page supports URL-shareable comparisons via query parameters and handles empty, loading, and populated states.

Also includes unit tests (Vitest + React Testing Library), E2E tests (Playwright), and MSW mock fixtures.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` with lazy-loaded page component

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with state management, URL sync, and layout
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component with count badge and data table
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for comparison page
- `tests/mocks/fixtures/comparison.json` — mock comparison API response fixture
- `tests/mocks/handlers.ts` — add MSW handler for `GET /api/v2/sbom/compare` (modify existing file)
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests for comparison workflow

## Implementation Notes
- **Page structure**: follow the established page directory pattern (see `src/pages/SbomListPage/` and `src/pages/SbomDetailPage/` for reference). Each page gets its own directory with a main component and optional `components/` subdirectory.

- **URL state management**: the page reads `left` and `right` query parameters from the URL using React Router's `useSearchParams`. When the user clicks "Compare", update the URL search params so the comparison is bookmark/shareable. On page load with query params, auto-trigger the comparison.

- **Header Toolbar (CompareToolbar.tsx)**:
  - Two PatternFly `Select` (single, typeahead) dropdowns for SBOM selection. Fetch the SBOM list using the existing `useSboms` hook (`src/hooks/useSboms.ts`). Display SBOM name and version (e.g., "my-product-sbom v2.3.1").
  - "Compare" button: PatternFly primary `Button`, disabled until both selectors have values. On click, calls `useSbomComparison` with selected IDs (from Task 4).
  - "Export" dropdown: PatternFly `Dropdown` with two items — "Export JSON" and "Export CSV". Disabled until comparison data is loaded. Export is non-MVP but the UI element should be present per the Figma design. Implement client-side download: serialize `SbomComparisonResult` as JSON or convert to CSV and trigger browser file download via `Blob` + `URL.createObjectURL`.
  - Disable the entire toolbar during loading.

- **Diff Sections (DiffSection.tsx)**:
  - Reusable component accepting: title, count, badge color, column definitions, and row data.
  - Use PatternFly `ExpandableSection` for each section. Default expanded when count > 0.
  - Use PatternFly `Badge` for count with color per section:
    - Added Packages: green
    - Removed Packages: red
    - Version Changes: blue
    - New Vulnerabilities: red
    - Resolved Vulnerabilities: green
    - License Changes: yellow
  - Use PatternFly composable `Table` with sortable columns inside each section.
  - For New Vulnerabilities section: rows with severity "Critical" must have a highlighted background. Use the existing `SeverityBadge` component (`src/components/SeverityBadge.tsx`) for the Severity column.
  - **Virtualized lists**: when a diff section has >100 rows, use virtualization (e.g., `react-window` or PatternFly's built-in virtualization) to prevent browser freezing per the non-functional requirements.

- **Empty state**: when no comparison has been performed (page load without query params or without clicking Compare), show PatternFly `EmptyState` with:
  - Icon: `CodeBranchIcon` from PatternFly icons
  - Title: "Select two SBOMs to compare"
  - Body: "Choose an SBOM for each side and click Compare to see what changed."
  - Use the existing `EmptyStateCard` component pattern from `src/components/EmptyStateCard.tsx`.

- **Loading state**: while the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Use the existing `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` as a reference for loading patterns.

- **Section order**: sections render in this fixed order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.

- **Route registration**: add the route in `src/routes.tsx` BEFORE the `/sbom/:id` route to avoid path conflicts. Use lazy loading consistent with existing routes (`React.lazy` or dynamic import).

- **Mutation pattern note**: this page is read-only (no mutations), but if Export triggers any server-side action in the future, follow the React Query mutation pattern with `onSuccess` + `queryClient.invalidateQueries()` per project conventions.

- **Testing**:
  - Unit tests: render `SbomComparePage` with MSW mocking the comparison endpoint. Test empty state, loading state, populated state with diff sections, URL parameter sync.
  - E2E tests: navigate to `/sbom/compare`, select two SBOMs, click Compare, verify diff sections appear with correct data.
  - Add MSW handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare`.
  - Add mock fixture in `tests/mocks/fixtures/comparison.json` following the pattern of existing fixtures (`sboms.json`, `advisories.json`).

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page structure with table, filters, and state management
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page with tabs and sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for table component with package data columns
- `src/components/SeverityBadge.tsx` — existing shared component for severity display; use directly in New Vulnerabilities table
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern
- `src/components/LoadingSpinner.tsx` — existing loading indicator pattern
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar patterns (though this page uses selectors, not filters)
- `src/hooks/useSboms.ts` — existing hook for SBOM list; use for selector dropdowns
- `tests/mocks/handlers.ts` — existing MSW handlers; extend with comparison endpoint handler
- `tests/mocks/fixtures/sboms.json` — existing mock SBOM data pattern; follow for comparison fixture
- `tests/e2e/sbom-list.spec.ts` — reference for Playwright E2E test patterns

## Acceptance Criteria
- [ ] Page is accessible at `/sbom/compare` route
- [ ] Two SBOM selector dropdowns load and display available SBOMs from the existing SBOM list endpoint
- [ ] "Compare" button is disabled until both selectors have values
- [ ] Clicking "Compare" calls the comparison API and displays results in six collapsible diff sections
- [ ] URL updates with `left` and `right` query parameters when comparison is performed
- [ ] Loading the page with `left` and `right` query params auto-triggers comparison (URL-shareable)
- [ ] Added Packages section shows packages present in right but not in left with correct columns (Package Name, Version, License, Advisories count)
- [ ] Removed Packages section shows packages present in left but not in right
- [ ] Version Changes section shows packages with different versions and upgrade/downgrade direction
- [ ] New Vulnerabilities section shows new advisories with severity badge; Critical rows are highlighted
- [ ] Resolved Vulnerabilities section shows resolved advisories
- [ ] License Changes section shows packages with changed licenses
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows skeleton placeholders during API call
- [ ] Diff sections with >100 rows use virtualized rendering without browser freezing
- [ ] "Export" dropdown is present with JSON and CSV options (non-MVP — implement client-side download)
- [ ] Unit tests pass
- [ ] E2E tests pass

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are provided
- [ ] Unit test: page auto-triggers comparison when left and right query params are present
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: diff sections render correct data from comparison API response
- [ ] Unit test: Critical vulnerabilities have highlighted row styling
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] E2E test: select two SBOMs, click Compare, verify diff sections appear
- [ ] E2E test: copy URL with query params, navigate to it, verify comparison loads automatically

## Verification Commands
- `npx vitest run src/pages/SbomComparePage/` — run unit tests for comparison page
- `npx playwright test tests/e2e/sbom-compare.spec.ts` — run E2E tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Frontend comparison API layer (types, client, hook)
