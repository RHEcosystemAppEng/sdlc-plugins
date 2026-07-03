## Repository

trustify-ui

## Target Branch

main

## Priority

Critical

## Fix Versions

RHTPA 1.5.0

## Description

Build the SBOM comparison page at `/sbom/compare` following the Figma design specifications. The page consists of a header toolbar with two SBOM selector dropdowns (PatternFly `Select` with typeahead), a "Compare" button, and an "Export" dropdown, followed by vertically stacked collapsible diff sections. Each diff section is a PatternFly `ExpandableSection` containing a data table with sortable columns. The page reads `left` and `right` query parameters from the URL to pre-populate the selectors and automatically trigger comparison. An empty state is shown when no SBOMs are selected. Loading state uses PatternFly `Skeleton` placeholders within each section.

## Acceptance Criteria

- [ ] Page component is accessible at `/sbom/compare` via React Router
- [ ] Header toolbar contains two PatternFly `Select` (single, typeahead) dropdowns that load SBOM options via the existing `useSboms` hook
- [ ] A primary "Compare" button triggers the comparison API call; it is disabled until both selectors have values
- [ ] An "Export" dropdown (PatternFly `Dropdown`) with "Export JSON" and "Export CSV" options is disabled until comparison results are loaded
- [ ] Six collapsible diff sections render in order: Added Packages (green badge), Removed Packages (red badge), Version Changes (blue badge), New Vulnerabilities (red badge), Resolved Vulnerabilities (green badge), License Changes (yellow badge)
- [ ] Each section uses PatternFly `ExpandableSection` with a `Badge` showing the item count; sections with >0 items are expanded by default
- [ ] Each section contains a PatternFly composable `Table` with sortable columns matching the Figma column specifications
- [ ] New Vulnerabilities section rows with severity "Critical" have a highlighted background
- [ ] The existing `SeverityBadge` shared component is used for severity display in vulnerability sections
- [ ] Empty state (PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare") is shown when no query params are present
- [ ] Loading state shows `Skeleton` placeholders in each section while the API call is in progress; the toolbar is disabled during loading
- [ ] URL query parameters `left` and `right` are kept in sync with selector values for URL-shareable comparisons
- [ ] Tables use virtualized rendering for sections with more than 100 rows to prevent browser freezing

## Test Requirements

- [ ] Unit test: page renders empty state when no query params are provided
- [ ] Unit test: page renders comparison results with correct section counts and table data
- [ ] Unit test: "Compare" button is disabled when only one SBOM is selected
- [ ] Unit test: critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] E2E test: select two SBOMs, click Compare, verify diff sections appear with correct data

## Dependencies

- Task 3 (sbom-comparison-api-types-and-hook) -- provides `useSbomComparison` hook and TypeScript types

## Figma Design Context

- **SBOM selectors**: PatternFly `Select` (single, typeahead) pre-populated from URL query params `left` and `right`
- **Diff sections**: PatternFly `ExpandableSection` with `Badge` count indicators; color-coded badges (green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes)
- **Data tables**: PatternFly composable `Table` with sortable columns; virtualized for >100 rows
- **Severity display**: Reuse existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`
- **Empty state**: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: PatternFly `Skeleton` placeholders in each section; toolbar disabled during loading
- **Export button**: PatternFly `Dropdown` with "Export JSON" and "Export CSV" items

## Files to Modify

- `src/routes.tsx` -- add route for `/sbom/compare` pointing to `SbomComparePage`

## Files to Create

- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- unit tests
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` -- header toolbar with selectors, compare button, and export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section with badge and table

## Implementation Notes

- Follow the existing page structure pattern in `src/pages/SbomDetailPage/` with a main page component and a `components/` subdirectory for page-specific components.
- Use React Router `useSearchParams` to read and write `left` and `right` query parameters, keeping URL in sync with selector state.
- Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the SBOM selector dropdowns.
- Use the `useSbomComparison` hook from Task 3 for fetching comparison results.
- Reuse `SeverityBadge` from `src/components/SeverityBadge.tsx` in the vulnerability diff sections.
- Reuse `EmptyStateCard` from `src/components/EmptyStateCard.tsx` for the empty state (adapt icon and text).
- Use PatternFly 5 components: `Select`, `ExpandableSection`, `Badge`, `Table`, `EmptyState`, `Skeleton`, `Dropdown`.
- For virtualized tables with >100 rows, use `react-window` or equivalent virtualization library.
- Lazy-load the page component in `src/routes.tsx` using `React.lazy()` consistent with other route definitions.

## Conventions

- **Component library**: PatternFly 5 -- all UI components use PF5 equivalents. Applies: task creates `src/pages/SbomComparePage/` components matching the convention's component library scope.
- **Page structure**: Each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory. Applies: task creates `src/pages/SbomComparePage/` matching the convention's file organization scope.
- **Routing**: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's routing scope.
- **Naming**: PascalCase for components. Applies: task creates `SbomComparePage.tsx`, `ComparisonToolbar.tsx`, `DiffSection.tsx` matching the convention's naming scope.
