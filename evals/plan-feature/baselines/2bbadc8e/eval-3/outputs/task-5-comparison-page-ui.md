## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page at `/sbom/compare` with a header toolbar and vertically stacked collapsible diff sections, following the Figma design specifications. The page allows users to select two SBOMs, trigger a comparison, and view the structured diff across six categories. The URL encodes both SBOM IDs as query parameters for shareability and bookmarking.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component with count badge and data table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown placeholder
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison API response data for tests

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)
- `src/App.tsx` — add route entry if needed by the router setup pattern

## Implementation Notes
**Figma design reference (from figma-context.md):**

**Header Toolbar:**
- Left SBOM selector: PatternFly `Select` (single, typeahead) showing SBOM name and version. Pre-populated from URL query param `left`. Fetches SBOM list via existing `useSboms` hook.
- Right SBOM selector: identical `Select` dropdown for the second SBOM. Pre-populated from URL query param `right`.
- "Compare" button: PatternFly primary `Button`, disabled until both selectors have values. Triggers the comparison API call.
- "Export" dropdown: placeholder for Task 6 (non-MVP). Render as disabled PatternFly `Dropdown` with "Export JSON" and "Export CSV" items.

**Diff Sections (PatternFly `ExpandableSection`):**
1. Added Packages — green `Badge` count; columns: Package Name, Version, License, Advisories (count)
2. Removed Packages — red `Badge` count; columns: Package Name, Version, License, Advisories (count)
3. Version Changes — blue `Badge` count; columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
4. New Vulnerabilities — red `Badge` count; columns: Advisory ID, Severity (using existing `SeverityBadge` component), Title, Affected Package. Rows with severity "Critical" have a highlighted background.
5. Resolved Vulnerabilities — green `Badge` count; columns: Advisory ID, Severity, Title, Previously Affected Package
6. License Changes — yellow `Badge` count; columns: Package Name, Left License, Right License

Default expanded for sections with > 0 items.

**Empty State (no comparison performed yet):**
PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Loading State:**
PatternFly `Skeleton` placeholders in each diff section while API call is in progress. Header toolbar disabled during loading.

**URL-shareable comparison:**
Use React Router `useSearchParams` to read/write `left` and `right` query parameters. When both are present on page load, auto-trigger the comparison. When the user clicks Compare, update the URL query parameters so the comparison is bookmarkable.

**Virtualized lists:**
For diff sections with > 100 rows, use virtualized rendering to prevent browser freezing. Use `react-window` or PatternFly's built-in virtualization support for the `Table` component.

**PatternFly component mapping (from Figma):**

| Figma Element | PatternFly Component |
|---|---|
| SBOM selector | `Select` (single, typeahead) |
| Diff section | `ExpandableSection` |
| Count badge | `Badge` |
| Data table | `Table` (composable, sortable) |
| Severity indicator | `SeverityBadge` (existing `src/components/SeverityBadge.tsx`) |
| Empty state | `EmptyState` |
| Compare button | `Button` (primary) |
| Export button | `Dropdown` (disabled placeholder for Task 6) |

Follow the existing page structure pattern: each page has its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory for page-specific components. See `src/pages/SbomDetailPage/` for the established pattern.

Per CONVENTIONS.md: use PatternFly 5 components for all UI elements; use React Query hooks for data fetching; follow PascalCase naming for components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity level display; reuse directly in the New Vulnerabilities and Resolved Vulnerabilities diff sections
- `src/components/EmptyStateCard.tsx` — existing empty state component; consider reusing or adapting for the comparison empty state
- `src/components/FilterToolbar.tsx` — existing filter toolbar pattern; reference for toolbar layout conventions
- `src/components/LoadingSpinner.tsx` — existing loading indicator; consider for loading state alongside Skeleton placeholders
- `src/hooks/useSboms.ts` — existing hook for SBOM list; reuse for populating the SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference for table column patterns and PatternFly Table usage
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component; reference for advisory display patterns

## Acceptance Criteria
- [ ] Page renders at `/sbom/compare` route
- [ ] Two SBOM selector dropdowns fetch and display the SBOM list using `useSboms` hook
- [ ] "Compare" button is disabled until both selectors have values
- [ ] Clicking "Compare" calls the comparison API and displays results in collapsible diff sections
- [ ] Each diff section shows the correct data table columns as specified in the Figma design
- [ ] Each diff section has a count badge with the correct color (green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes)
- [ ] Sections with > 0 items are expanded by default; sections with 0 items are collapsed
- [ ] New Vulnerability rows with severity "Critical" have a highlighted background
- [ ] URL query params `left` and `right` are updated when Compare is clicked
- [ ] Loading the page with `left` and `right` query params auto-triggers the comparison
- [ ] Empty state displays when no comparison has been performed (no query params)
- [ ] Loading state shows Skeleton placeholders while comparison API call is in progress
- [ ] Diff sections with > 100 rows use virtualized rendering

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: SBOM selectors fetch and display SBOM list
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button triggers API call and displays diff sections with data
- [ ] Unit test: critical vulnerability rows have highlighted background styling
- [ ] Unit test: page auto-triggers comparison when loaded with both query params in URL
- [ ] Unit test: loading state shows skeleton placeholders during API call
- [ ] MSW mock handler returns valid SbomComparison fixture for comparison endpoint

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add API client and React Query hook for SBOM comparison
