## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SbomComparePage component implementing the comparison UI from the Figma design. The page includes a header toolbar with SBOM selectors, a Compare button, and an Export dropdown, plus six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) each containing a data table. Includes empty state and loading state handling.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM Select dropdowns, Compare button, and Export Dropdown

## Implementation Notes
- **PatternFly components** (per Figma design):
  - SBOM selectors: use PatternFly `Select` (single, typeahead variant) — fetch SBOM list via existing `useSboms` hook from `src/hooks/useSboms.ts`.
  - Diff sections: use PatternFly `ExpandableSection` with `isExpanded` defaulting to `true` for sections with items > 0.
  - Count badges: use PatternFly `Badge` — green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow/gold for License Changes.
  - Data tables: use PatternFly composable `Table` (`Thead`, `Tbody`, `Tr`, `Th`, `Td`) with sortable columns. For sections with >100 rows, implement virtualized rendering (e.g., `react-window` or PatternFly's built-in virtualization).
  - Severity indicator: reuse existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` in the New Vulnerabilities and Resolved Vulnerabilities tables.
  - Empty state: use PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Export button: use PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded.
  - Loading state: use PatternFly `Skeleton` placeholders in each diff section while the comparison API call is in progress. Disable the header toolbar during loading.
- **Table columns per section** (from Figma):
  - Added/Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package — rows with "Critical" severity have highlighted background
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- **DiffSection component**: accepts `title`, `count`, `badgeColor`, `columns`, `rows`, and `isExpanded` props. Renders `ExpandableSection` > `Table`.
- Follow page structure convention: each page in its own directory under `src/pages/` with optional `components/` subdirectory.
- Use `useSbomComparison` hook from Task 6 for data fetching.

**Data component rendering scope:**
- All six diff section tables inside the comparison page render **aggregated** data — they display the complete diff result across all categories, not scoped to a sub-context.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity display in vulnerability tables
- `src/components/FilterToolbar.tsx` — existing reusable toolbar pattern (reference for toolbar layout)
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern
- `src/components/LoadingSpinner.tsx` — existing loading indicator (reference, though Skeleton is preferred per Figma)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component demonstrating PatternFly Table usage with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list showing advisory rendering patterns
- `src/hooks/useSboms.ts` — existing hook for populating SBOM selector dropdowns

## Acceptance Criteria
- [ ] SbomComparePage renders with header toolbar containing two SBOM selectors, Compare button, and Export dropdown
- [ ] Compare button is disabled until both selectors have values
- [ ] Six collapsible diff sections render with correct titles and count badges
- [ ] Each diff section contains a sortable data table with correct columns per Figma design
- [ ] Rows in New Vulnerabilities with Critical severity have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] Export dropdown is disabled until comparison data is loaded
- [ ] Virtualized rendering is used for diff sections with >100 rows

## Test Requirements
- [ ] Unit test: empty state renders when no comparison data exists
- [ ] Unit test: diff sections render with correct item counts and badge colors
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted styling
- [ ] Unit test: Export dropdown is disabled when no comparison data is loaded

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add comparison React Query hook

## Description Digest
sha256-md:271e20e7fd1b0f92ebcfb8c67c8a7364942a60586253d2085bf86835e6c054f8
