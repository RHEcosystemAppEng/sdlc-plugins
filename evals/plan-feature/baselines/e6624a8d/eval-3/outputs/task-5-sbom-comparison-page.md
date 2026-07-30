## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` per the Figma design. The page provides a side-by-side comparison view where users select two SBOMs and see structured diffs across six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The page supports URL-shareable comparisons via query parameters and client-side export to JSON and CSV.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section component (wraps ExpandableSection + Badge + Table)
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` -- header toolbar with SBOM selectors, Compare button, and Export dropdown

## Implementation Notes
Per CONVENTIONS.md PatternFly 5: all UI components must use PatternFly 5 equivalents. The comparison page uses these PatternFly components per the Figma design.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md Page structure: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` page scope.

Per CONVENTIONS.md Naming conventions: PascalCase for components, camelCase for hooks, kebab-case for directories.
Applies: convention has no file-type restriction (broadly applicable).

**Figma design implementation -- Header Toolbar (CompareToolbar.tsx):**
- **Left SBOM selector**: PatternFly `Select` component (single, typeahead variant). Fetches SBOM list via existing `useSboms` hook. Displays SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populated from URL query param `left`.
- **Right SBOM selector**: identical `Select` component for the second SBOM. Pre-populated from URL query param `right`.
- **"Compare" button**: PatternFly `Button` (primary variant), disabled until both selectors have values. Triggers the comparison API call by updating URL query params (enabling URL-shareable comparisons).
- **"Export" dropdown**: PatternFly `Dropdown` component (secondary variant) with two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded.

**Figma design implementation -- Diff Sections (DiffSection.tsx):**
Each section is a PatternFly `ExpandableSection` with a title, count `Badge`, and a composable `Table` inside. Sections default to expanded when they have >0 items. Use virtualized rendering for sections with >100 rows (per non-functional requirements).

| Section | Badge Color | Table Columns |
|---|---|---|
| Added Packages | green | Package Name, Version, License, Advisories (count) |
| Removed Packages | red | Package Name, Version, License, Advisories (count) |
| Version Changes | blue | Package Name, Left Version, Right Version, Direction (upgrade/downgrade) |
| New Vulnerabilities | red | Advisory ID, Severity (SeverityBadge), Title, Affected Package |
| Resolved Vulnerabilities | green | Advisory ID, Severity, Title, Previously Affected Package |
| License Changes | yellow | Package Name, Left License, Right License |

- Rows in "New Vulnerabilities" with severity "Critical" must have a highlighted/warning background.
- All tables use sortable columns.

**Figma design implementation -- Empty State:**
When no comparison has been performed (page load without query params), render PatternFly `EmptyState` with:
- Icon: PatternFly `CodeBranchIcon`
- Title: "Select two SBOMs to compare"
- Body: "Choose an SBOM for each side and click Compare to see what changed."

**Figma design implementation -- Loading State:**
While the comparison API call is in progress, each diff section shows a PatternFly `Skeleton` placeholder. The header toolbar is disabled during loading.

**URL-shareable comparison:**
Use React Router's `useSearchParams` to read and write `left` and `right` query parameters. When both params are present on page load, auto-trigger the comparison. When the user clicks "Compare", update the URL params to enable bookmarking/sharing.

**Export implementation:**
- Export JSON: serialize the `SbomComparisonResult` object to a JSON file and trigger browser download
- Export CSV: flatten each diff section into CSV rows with section headers and trigger browser download

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- existing severity badge component; use in New Vulnerabilities and Resolved Vulnerabilities table columns
- `src/components/EmptyStateCard.tsx` -- existing empty state component; reference pattern for the comparison empty state (may need custom variant with CodeBranchIcon)
- `src/components/LoadingSpinner.tsx` -- existing loading indicator; reference for loading patterns
- `src/hooks/useSboms.ts` -- existing hook for fetching SBOM list; use for populating the SBOM selector dropdowns
- `src/utils/severityUtils.ts` -- existing severity level ordering and color mapping; use for severity badge rendering and critical row highlighting
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- existing package table component; reference for PatternFly Table patterns with package data

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections per Figma design
- [ ] SBOM selectors load available SBOMs and allow typeahead selection
- [ ] Compare button triggers API call and renders diff sections with correct data
- [ ] Each diff section shows correct count badge with section-specific color
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Empty state renders with CodeBranchIcon when no comparison is active
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL query params (`left`, `right`) enable shareable comparisons -- pre-populate selectors and auto-compare on page load
- [ ] Export JSON downloads the comparison result as a .json file
- [ ] Export CSV downloads the comparison result as a .csv file
- [ ] Large diffs (>100 changed packages) render without browser freezing (virtualized lists)

## Test Requirements
- [ ] Unit test: comparison page renders empty state when no query params are present
- [ ] Unit test: comparison page renders diff sections with mock comparison data
- [ ] Unit test: severity badges render correctly in vulnerability sections
- [ ] Unit test: critical severity rows have highlighted background
- [ ] Unit test: Compare button is disabled until both selectors have values
- [ ] Unit test: Export dropdown is disabled until comparison result is loaded
- [ ] Unit test: URL query params pre-populate selectors and trigger comparison
- [ ] Unit test: DiffSection component renders with correct badge color and expanded state

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 4 -- Add comparison API types, client function, and React Query hook
