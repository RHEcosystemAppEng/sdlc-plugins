## Repository
trustify-ui

## Target Branch
main

## Description
Create the SBOM comparison page component at `/sbom/compare` with a header toolbar for SBOM selection and six collapsible diff sections displaying the comparison results. The page implements the Figma design specifications using PatternFly 5 components, including SBOM selectors, a Compare action button, an Export dropdown, and data tables within expandable sections for each diff category.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- Main comparison page component with toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` -- Header toolbar with left/right SBOM PatternFly Select dropdowns, Compare Button, and Export Dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- Reusable collapsible diff section component with PatternFly ExpandableSection, Badge count, and composable Table

## Implementation Notes
- **Figma design reference -- Header Toolbar:**
  - Left and right SBOM selectors: PatternFly `Select` component (single selection, typeahead variant) showing SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populate selector values from URL query params `left` and `right` using React Router's `useSearchParams`. Fetch the SBOM list for selector options using the existing `useSboms` hook from `src/hooks/useSboms.ts`.
  - "Compare" button: PatternFly `Button` component (primary variant). Disabled until both selectors have values. On click, update URL query params and trigger the comparison API call via `useSbomComparison` hook from `src/hooks/useSbomComparison.ts`.
  - "Export" dropdown: PatternFly `Dropdown` component (secondary variant) with two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded. Export generates a downloadable file from the comparison result data.

- **Figma design reference -- Diff Sections:**
  Each section is a PatternFly `ExpandableSection` with a title, a PatternFly `Badge` showing the item count, and a PatternFly composable `Table` inside. Sections with >0 items default to expanded; sections with 0 items default to collapsed. Section order and specifications:
  1. **Added Packages** -- green `Badge`. Table columns: Package Name, Version, License, Advisories (count).
  2. **Removed Packages** -- red `Badge`. Table columns: Package Name, Version, License, Advisories (count).
  3. **Version Changes** -- blue `Badge`. Table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
  4. **New Vulnerabilities** -- red `Badge`. Table columns: Advisory ID, Severity (render using existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows where severity is "Critical" must have a highlighted background (use PatternFly `isHoverable` or custom CSS class for the critical row highlight).
  5. **Resolved Vulnerabilities** -- green `Badge`. Table columns: Advisory ID, Severity, Title, Previously Affected Package.
  6. **License Changes** -- yellow `Badge`. Table columns: Package Name, Left License, Right License.

- **Figma design reference -- Empty State:**
  When no comparison has been performed (page loaded without `left` and `right` query params), render a PatternFly `EmptyState` component with: `CodeBranchIcon` as the icon, title text "Select two SBOMs to compare", body text "Choose an SBOM for each side and click Compare to see what changed."

- **Figma design reference -- Loading State:**
  While the comparison API call is in progress (`isLoading` from `useSbomComparison`), render PatternFly `Skeleton` placeholders in place of each diff section's table content. The header toolbar controls (selectors, buttons) should be disabled during loading.

- Create `DiffSection` as a reusable component that accepts props: `title: string`, `count: number`, `badgeColor: string`, `columns: TableColumn[]`, `rows: TableRow[]`. Use PatternFly composable `Table` (`Thead`, `Tbody`, `Tr`, `Th`, `Td`) with sortable columns. For sections with >100 rows, implement virtualized rendering (react-window or equivalent) per the NFR requirement to prevent browser freezing on large diffs.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the severity column in the New Vulnerabilities and Resolved Vulnerabilities sections.
- Reference the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` for the empty state implementation pattern, but customize content for the comparison-specific design.
- Use `src/utils/severityUtils.ts` for severity level ordering when sorting the vulnerabilities table by severity column.
- URL must encode both SBOM IDs as query parameters (`?left={id1}&right={id2}`) for shareability (UC-2). Use `useSearchParams` from React Router v6 to read and update URL params. When a user selects SBOMs and clicks Compare, update the URL params so the comparison is bookmarkable and shareable.
- Per CONVENTIONS.md section Component library: all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.
- Per CONVENTIONS.md section Page structure: each page gets its own directory under `src/pages/` with a main component and a `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` page directory scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- Existing severity badge component; reuse directly in New Vulnerabilities and Resolved Vulnerabilities diff section tables
- `src/components/EmptyStateCard.tsx` -- Existing empty state component; reference for PatternFly EmptyState usage pattern
- `src/components/FilterToolbar.tsx` -- Existing PatternFly filter toolbar; reference for toolbar layout and Select component usage patterns
- `src/components/LoadingSpinner.tsx` -- Existing loading indicator; reference for loading patterns (though the Figma design specifies Skeleton for this page)
- `src/utils/severityUtils.ts` -- Severity level ordering and color mapping utilities; reuse for sorting vulnerability tables by severity
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- Existing package table component; reference for PatternFly composable Table usage with package data columns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` -- Existing advisory list component; reference for advisory display and PatternFly Table patterns
- `src/hooks/useSboms.ts` -- Existing hook for fetching SBOM list; reuse for populating SBOM selector dropdowns

## Acceptance Criteria
- [ ] `SbomComparePage` renders with a header toolbar containing two PatternFly Select (typeahead) SBOM selectors, a primary Compare button, and a secondary Export dropdown
- [ ] SBOM selectors are populated with SBOM list data from the existing `useSboms` hook, displaying name and version
- [ ] Compare button is disabled until both selectors have valid SBOM values
- [ ] Export dropdown has "Export JSON" and "Export CSV" items, disabled until comparison results are loaded
- [ ] Six diff sections render as PatternFly `ExpandableSection` components with correct titles and colored `Badge` counts (green, red, blue, red, green, yellow)
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed by default
- [ ] New Vulnerabilities section highlights rows with Critical severity using a visually distinct background color
- [ ] Severity column in vulnerability sections uses the existing `SeverityBadge` component
- [ ] Empty state renders with `CodeBranchIcon`, title "Select two SBOMs to compare", and body text when no query params are present
- [ ] Loading state shows PatternFly `Skeleton` placeholders during API call, with toolbar controls disabled
- [ ] URL query params (`left`, `right`) are read on page load and pre-populate the SBOM selectors
- [ ] Selecting SBOMs and clicking Compare updates URL query params for shareability and bookmarking

## Test Requirements
- [ ] Unit test: page renders empty state with correct icon, title, and body text when no query params are present
- [ ] Unit test: page renders all six diff sections with correct data when comparison result is provided
- [ ] Unit test: Compare button is disabled when only one SBOM selector has a value
- [ ] Unit test: Critical severity rows in New Vulnerabilities section have highlighted background styling
- [ ] Unit test: sections with 0 items render in collapsed state
- [ ] Unit test: Export dropdown is disabled when no comparison result is loaded

## Dependencies
- Depends on: Task 3 -- Add API types, client function, and hook for SBOM comparison

---
sha256-md:17cc703b478404762d5d5f7fc63692be6268a54773a0d992700a1b00d693afd7
