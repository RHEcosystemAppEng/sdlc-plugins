# Task 8 — Implement SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the full SBOM comparison page at `/sbom/compare` following the Figma design specifications. The page includes a header toolbar with two SBOM selectors (PatternFly `Select` with typeahead), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results using PatternFly `ExpandableSection` components with data tables inside. The page supports URL-shareable comparisons via query parameters and handles empty, loading, and error states.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with toolbar and diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component (PatternFly ExpandableSection + Badge + Table)
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, Export dropdown

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection and "Compare selected" button to enable comparison workflow from the SBOM list

## Implementation Notes
- **Figma component mapping**: Follow the design context exactly:
  - SBOM selectors: PatternFly `Select` component (single, typeahead variant). Fetches SBOM list via existing `useSboms` hook. Pre-populated from URL query params `left` and `right`.
  - Compare button: PatternFly primary action button, disabled until both selectors have values.
  - Export dropdown: PatternFly `Dropdown` component with two items ("Export JSON", "Export CSV"). Disabled until comparison result is loaded.
  - Diff sections: PatternFly `ExpandableSection` with title, count `Badge`, and composable `Table` inside. Sections default expanded when item count > 0.
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Loading state: PatternFly `Skeleton` placeholders in each diff section while the API call is in progress. Header toolbar disabled during loading.
- **Diff section details from Figma**:
  1. Added Packages — columns: Package Name, Version, License, Advisories (count). Badge color: green.
  2. Removed Packages — columns: Package Name, Version, License, Advisories (count). Badge color: red.
  3. Version Changes — columns: Package Name, Left Version, Right Version, Direction. Badge color: blue.
  4. New Vulnerabilities — columns: Advisory ID, Severity (using `SeverityBadge`), Title, Affected Package. Badge color: red. Rows with severity "Critical" have highlighted background.
  5. Resolved Vulnerabilities — columns: Advisory ID, Severity, Title, Previously Affected Package. Badge color: green.
  6. License Changes — columns: Package Name, Left License, Right License. Badge color: yellow.
- **URL-shareable comparison**: Use React Router `useSearchParams` to read and write `left` and `right` query parameters. When the page loads with both parameters, auto-trigger the comparison.
- **Virtualized lists**: For diff sections with >100 rows, use virtualized rendering to prevent browser freezing per the non-functional requirement. Consider `react-window` or PatternFly's built-in virtualization.
- **Page structure**: Follow the existing page pattern from `src/pages/SbomDetailPage/` — main page component in the page directory root, sub-components in a `components/` subdirectory.
- **Routing**: Follow the lazy-loading pattern from `src/routes.tsx` using React Router v6.
- Use the `useSbomComparison` hook from Task 7 for data fetching.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for vulnerability severity display.
- Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` as reference for empty state patterns.
- Use the existing `LoadingSpinner` from `src/components/LoadingSpinner.tsx` as reference, but prefer PatternFly `Skeleton` for diff sections per the Figma spec.
- Per docs/constraints.md §5.4: Reuse existing components (SeverityBadge, EmptyStateCard) rather than creating new equivalents.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Reuse directly for severity display in vulnerability tables
- `src/components/EmptyStateCard.tsx` — Reference for empty state pattern; may need customization for comparison-specific empty state
- `src/components/FilterToolbar.tsx` — Reference for toolbar layout patterns with PatternFly
- `src/hooks/useSboms.ts` — Reuse for populating SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Reference for package table column structure
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Reference for advisory display patterns
- `src/utils/severityUtils.ts` — Reuse severity ordering and color mapping for critical vulnerability highlighting

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Two SBOM selectors allow searching and selecting SBOMs by name/version
- [ ] Compare button triggers comparison API call when both SBOMs are selected
- [ ] All six diff sections render with correct columns per Figma design
- [ ] Each diff section shows a count badge with the specified color
- [ ] Sections with items default to expanded; sections with zero items default to collapsed
- [ ] Critical vulnerabilities have highlighted row background in the New Vulnerabilities section
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL encodes both SBOM IDs as query parameters for bookmarking/sharing
- [ ] Page loads comparison directly when opened with left and right query params

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: SBOM selectors display SBOM list from useSboms hook
- [ ] Unit test: Compare button is disabled until both selectors have values
- [ ] Unit test: diff sections render with correct data from comparison API response
- [ ] Unit test: critical vulnerability rows have highlighted styling

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 7 — Add React Query hook for SBOM comparison

sha256-md:1246f41ec6228a1e1e865c6d09ab5689be36843b51a747a54f29d3d04688d44c
