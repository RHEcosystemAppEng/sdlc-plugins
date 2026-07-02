## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page with a header toolbar (two SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections, following the Figma design specifications. Each diff section uses PatternFly ExpandableSection with a Table inside displaying category-specific columns. The page reads left/right SBOM IDs from URL query parameters for shareable comparisons and uses the useSbomComparison hook from Task 4 for data fetching.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM Select dropdowns, Compare button, and Export Dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable expandable diff section component wrapping ExpandableSection + Badge + Table
- `src/pages/SbomComparePage/components/DiffSection.test.tsx` — Unit tests for DiffSection component

## Implementation Notes
- **PatternFly component mapping per Figma design:**
  - SBOM selectors: PatternFly `Select` (single, typeahead) — pre-populate from URL query params `left` and `right`, fetch SBOM list via existing `useSboms` hook from `src/hooks/useSboms.ts`
  - Diff sections: PatternFly `ExpandableSection` — default expanded for sections with count > 0, collapsed for empty sections
  - Count badges: PatternFly `Badge` — green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes
  - Data tables: PatternFly `Table` (composable) — sortable columns, no pagination; use virtualized rendering for >100 rows per non-functional requirement
  - Severity indicators: use existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Export button: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV" — disabled until comparison result is loaded
  - Loading state: PatternFly `Skeleton` placeholders in each diff section while API call is in progress; header toolbar disabled during loading

- **Diff section table columns per Figma:**
  1. Added Packages: Package Name, Version, License, Advisories (count)
  2. Removed Packages: Package Name, Version, License, Advisories (count)
  3. Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  4. New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package — rows with severity "Critical" have a highlighted background
  5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  6. License Changes: Package Name, Left License, Right License

- **URL query parameters:** read `left` and `right` from `useSearchParams()` (React Router). When user selects SBOMs and clicks Compare, update URL params so the comparison is shareable/bookmarkable.
- **DiffSection component:** generic reusable component accepting props: title, count, badgeColor, columns, rows, isExpanded (default true when count > 0). This avoids duplicating ExpandableSection + Badge + Table boilerplate six times.
- **Critical vulnerability highlighting:** in the New Vulnerabilities table, apply a CSS class or PatternFly `isRowHighlighted` for rows where severity is "Critical".

**Data component rendering scope:**
- Each diff section table renders data scoped to its own category from the SbomComparisonResult — the tables are NOT aggregated across all categories. Each section receives its specific array (e.g., Added Packages section receives only `result.added_packages`).

**Convention references:**
- Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's React component scope.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; MSW for API mocking.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's test file scope.
- Per CONVENTIONS.md §Naming: PascalCase for components, camelCase for hooks and utilities.
  Applies: task creates `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's component naming scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity level display in vulnerability tables
- `src/components/FilterToolbar.tsx` — reusable filter toolbar pattern with PatternFly (for toolbar layout reference)
- `src/components/EmptyStateCard.tsx` — existing empty state component (may serve as pattern reference, though Figma specifies custom empty state content)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (though Skeleton is used per Figma for section-level loading)
- `src/hooks/useSboms.ts` — existing hook to fetch SBOM list for the selector dropdowns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability table sorting

## Acceptance Criteria
- [ ] SbomComparePage renders with header toolbar containing two SBOM Select dropdowns, Compare button, and Export dropdown
- [ ] Compare button is disabled until both SBOM selectors have values
- [ ] Clicking Compare triggers the comparison API call via useSbomComparison hook
- [ ] Six diff sections render with correct titles, count badges, and table columns per Figma design
- [ ] Diff sections are expanded by default when they have items, collapsed when empty
- [ ] Badge colors match Figma: green (added/resolved), red (removed/new vulns), blue (version changes), yellow (license changes)
- [ ] New Vulnerability rows with "Critical" severity have highlighted background
- [ ] Empty state with CodeBranchIcon displays when no comparison has been performed
- [ ] Skeleton loading states display while comparison API call is in progress
- [ ] URL query params (left, right) are read on mount and written on Compare click
- [ ] Export dropdown is disabled until comparison result is loaded

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no query params are present
- [ ] Unit test: SbomComparePage renders diff sections with correct data when comparison result is loaded (MSW mock)
- [ ] Unit test: Compare button is disabled when only one SBOM selector has a value
- [ ] Unit test: DiffSection renders ExpandableSection with Badge showing correct count and color
- [ ] Unit test: DiffSection table renders correct columns for each diff category
- [ ] Unit test: Critical vulnerability rows are highlighted in New Vulnerabilities section
- [ ] Unit test: Export dropdown is disabled when no comparison result is present

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook

[sdlc-workflow] Description digest: sha256-md:5cf990fd9186cc906984f029fff53082dcc9aeadb3ba1723c7d8c31e65885f09
