## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page UI at `/sbom/compare` based on Figma design specifications. The page includes SBOM selector dropdowns, a Compare button, and six collapsible diff sections displaying added/removed packages, version changes, new/resolved vulnerabilities, and license changes. This is the primary user-facing deliverable for TC-9003.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` -- Header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count `Badge`
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` -- Table component for added/removed packages and version changes
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` -- Table component for new/resolved vulnerabilities with `SeverityBadge`
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` -- Table component for license changes

## Files to Modify
- `src/routes.tsx` -- Add route entry for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)
- `src/pages/SbomListPage/SbomListPage.tsx` -- Add multi-select checkbox column and "Compare selected" button to navigate to comparison page with selected SBOM IDs

## Implementation Notes
**Figma design mapping** (per figma-context.md):

**ComparisonToolbar.tsx**: Use PatternFly `Select` component (single, typeahead variant) for both SBOM selectors. The selectors fetch the SBOM list via the existing `useSboms` hook from `src/hooks/useSboms.ts`. The "Compare" button is a PatternFly primary `Button`, disabled until both selectors have values. The "Export" button is a PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV", disabled until comparison data is loaded.

**DiffSection.tsx**: Use PatternFly `ExpandableSection` for each diff category. Each section title includes a PatternFly `Badge` showing the item count. Badge colors per Figma: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes. Sections default to expanded when they contain items (count > 0).

**PackageDiffTable.tsx**: Use PatternFly composable `Table` with sortable columns. For added/removed packages: columns are Package Name, Version, License, Advisories (count). For version changes: columns are Package Name, Left Version, Right Version, Direction (upgrade/downgrade).

**VulnerabilityDiffTable.tsx**: Use PatternFly composable `Table`. Columns: Advisory ID, Severity (rendered with existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" should have a highlighted background row style. Use severity ordering utilities from `src/utils/severityUtils.ts`.

**LicenseChangeTable.tsx**: Use PatternFly composable `Table`. Columns: Package Name, Left License, Right License.

**Empty state**: When no comparison has been performed (page load without query params), render PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Reuse the `EmptyStateCard` pattern from `src/components/EmptyStateCard.tsx`.

**Loading state**: While the comparison API call is in progress, render PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading.

**URL sync**: Read `left` and `right` query parameters from the URL using React Router's `useSearchParams`. Update URL when Compare is clicked so comparisons are bookmarkable and shareable (UC-2).

**Large diffs**: For sections with >100 items, use virtualized rendering to prevent browser freezing per non-functional requirements.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- Existing severity badge component for vulnerability tables
- `src/components/EmptyStateCard.tsx` -- Existing empty state component pattern
- `src/components/FilterToolbar.tsx` -- Pattern reference for toolbar layout with PatternFly
- `src/components/LoadingSpinner.tsx` -- Loading indicator pattern (though Skeleton is preferred per Figma)
- `src/hooks/useSboms.ts` -- Existing hook for loading SBOM list in selectors
- `src/utils/severityUtils.ts` -- Severity level ordering and color mapping for vulnerability tables
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- Pattern reference for package data table with PatternFly composable Table

## Acceptance Criteria
- [ ] Comparison page is accessible at `/sbom/compare`
- [ ] SBOM selectors load available SBOMs and support typeahead search
- [ ] Compare button triggers API call and renders all six diff sections
- [ ] Each diff section is collapsible with correct count badge and color
- [ ] New Vulnerabilities table highlights Critical severity rows
- [ ] Severity badges render correctly using existing `SeverityBadge` component
- [ ] Empty state displays when no comparison is active
- [ ] Skeleton loading state displays during API call
- [ ] URL encodes both SBOM IDs for bookmarking and sharing
- [ ] SBOM list page allows selecting two SBOMs and navigating to comparison

## Test Requirements
- [ ] Unit test: empty state renders when no SBOM IDs are in URL
- [ ] Unit test: selectors populate with SBOM list data
- [ ] Unit test: diff sections render with correct data and count badges
- [ ] Unit test: Critical severity rows have highlighted styling

## Dependencies
- Depends on: Task 4 -- Add API types, client function, and React Query hook

[sdlc-workflow] Description digest: sha256-md:e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7
