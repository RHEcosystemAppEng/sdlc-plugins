## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page component at `src/pages/SbomComparePage/` with a header toolbar (SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections. The page reads `left` and `right` SBOM IDs from URL query parameters, fetches comparison data using the hook from Task 4, and renders the structured diff. This is the primary UI for the SBOM comparison feature. The page must handle large diffs (>100 changed packages) using virtualized lists to prevent browser freezing.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar with SBOM Select dropdowns, Compare button, and Export Dropdown
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page

## Implementation Notes
1. **Page layout**: the page is a full-page layout with a header toolbar and vertically stacked collapsible diff sections. Follow the page structure pattern of `src/pages/SbomDetailPage/SbomDetailPage.tsx` which uses a similar tabs/sections layout.

2. **Header toolbar** (`ComparisonToolbar.tsx`):
   - Two PatternFly `Select` dropdowns (single, typeahead) for left and right SBOM selection. Fetch the SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populate from URL query params `left` and `right`.
   - A primary PatternFly `Button` labeled "Compare", disabled until both selectors have values. On click, update URL query params and trigger the comparison API call.
   - A secondary PatternFly `Dropdown` labeled "Export" with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. On select, serialize the comparison result to the chosen format and trigger a browser download.

3. **Diff sections** (`DiffSection.tsx`): each section is a PatternFly `ExpandableSection` containing:
   - Title with a PatternFly `Badge` showing the count of items. Badge colors by section: green (Added Packages, Resolved Vulnerabilities), red (Removed Packages, New Vulnerabilities), blue (Version Changes), yellow (License Changes).
   - A PatternFly composable `Table` with sortable columns. For sections with >100 rows, use virtualized rendering (e.g., `react-window` or PatternFly's virtualized table pattern) to prevent browser freezing.
   - Sections default to expanded when they have >0 items, collapsed when empty.

4. **Section-specific table columns** (from Figma design):
   - **Added Packages**: Package Name, Version, License, Advisories (count)
   - **Removed Packages**: Package Name, Version, License, Advisories (count)
   - **Version Changes**: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
   - **New Vulnerabilities**: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have a highlighted background (use PatternFly `isHoverable` row variant or custom CSS with `--pf-v5-global--danger-color--100`).
   - **Resolved Vulnerabilities**: Advisory ID, Severity, Title, Previously Affected Package
   - **License Changes**: Package Name, Left License, Right License

5. **Empty state**: when no comparison has been performed (page load without query params), render a PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed." Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` as a reference pattern.

6. **Loading state**: while the comparison API call is in progress, render PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.

7. **URL-shareable comparison**: the page URL must encode both SBOM IDs as query parameters (`/sbom/compare?left={id1}&right={id2}`). When the page loads with both params present, auto-trigger the comparison. Use React Router's `useSearchParams` to read/write query params.

8. **Export functionality** (non-MVP): implement JSON export by serializing the `SbomComparisonResult` to a JSON file download. CSV export should flatten the comparison into a single CSV with columns: Category, Package Name, Details. Use `Blob` + `URL.createObjectURL` for browser download.

Per CONVENTIONS.md §Component Library: all UI elements must use PatternFly 5 components (Select, ExpandableSection, Badge, Table, EmptyState, Button, Dropdown, Skeleton).
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory structure scope.

Per CONVENTIONS.md §Naming: PascalCase for components (SbomComparePage, DiffSection, ComparisonToolbar).
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's PascalCase component naming scope.

Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests with MSW for API mocking.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.test.tsx` test file scope.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference page with tabs/sections layout; follow its structure for the comparison page
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing table component for packages; reference for PatternFly Table usage with sortable columns
- `src/components/SeverityBadge.tsx` — existing component for rendering severity levels; reuse in the New Vulnerabilities and Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` — existing empty state component; reference for the comparison empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; reference for loading state patterns
- `src/components/FilterToolbar.tsx` — existing toolbar component; reference for PatternFly toolbar patterns
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list; reuse for populating the SBOM selector dropdowns

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] Left and right SBOM selectors load SBOM list via `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and renders results
- [ ] All six diff sections render with correct table columns per Figma design
- [ ] Diff sections use PatternFly ExpandableSection, expanded by default when count > 0
- [ ] Count badges show correct colors per section (green, red, blue, yellow)
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Severity values render using the existing SeverityBadge component
- [ ] Empty state renders when no comparison is performed (no query params)
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL encodes both SBOM IDs as query parameters for shareability
- [ ] Page auto-triggers comparison when loaded with both query params
- [ ] Export dropdown is disabled until comparison data is loaded
- [ ] Large diffs (>100 items) use virtualized rendering

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders loading state while API call is in progress
- [ ] Unit test: page renders all six diff sections with correct data after API response
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button triggers API call with selected SBOM IDs
- [ ] Unit test: diff sections are expanded by default when they have items
- [ ] Unit test: diff sections are collapsed when they have zero items
- [ ] Unit test: SeverityBadge renders correctly in vulnerability sections
- [ ] Unit test: Critical severity rows have highlighted styling

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison API types, client function, and React Query hook
