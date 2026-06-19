## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selector dropdowns and a Compare button, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), an empty state when no comparison is active, and loading skeletons during API calls. URL query parameters encode both SBOM IDs for shareability.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable expandable diff section with count badge and data table

## Implementation Notes
**Header Toolbar** (per Figma design):
- Two PatternFly `Select` components (single, typeahead) for SBOM selection. Pre-populate from URL query params `left` and `right`. Fetch SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`.
- A primary "Compare" button, disabled until both selectors have values. On click, update URL query params and trigger the comparison via `useSbomComparison` hook (task 8).
- A secondary "Export" `Dropdown` with "Export JSON" and "Export CSV" options. Disabled until comparison data is loaded.

**Diff Sections** (per Figma design):
Each section uses a PatternFly `ExpandableSection` with:
- Title and a `Badge` showing item count (color: green for added/resolved, red for removed/new-vulns, blue for version changes, yellow for license changes)
- A PatternFly composable `Table` inside with sortable columns
- Default expanded when section has >0 items

Section order and columns per Figma:
1. Added Packages: Package Name, Version, License, Advisories (count). Badge: green.
2. Removed Packages: Package Name, Version, License, Advisories (count). Badge: red.
3. Version Changes: Package Name, Left Version, Right Version, Direction. Badge: blue.
4. New Vulnerabilities: Advisory ID, Severity (use existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Badge: red. Rows with severity "Critical" get highlighted background.
5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package. Badge: green.
6. License Changes: Package Name, Left License, Right License. Badge: yellow.

**DiffSection component**: Extract a reusable `DiffSection` component that accepts a title, badge color, count, column definitions, and row data. This avoids repeating the ExpandableSection + Badge + Table pattern six times.

**Empty State** (per Figma design): When no comparison is active (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Loading State** (per Figma design): While comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable header toolbar during loading.

**URL shareability**: Read `left` and `right` from URL search params on mount. Update URL params when Compare is clicked. This enables bookmarking and sharing.

Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` and `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` and `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's `.tsx` page scope.

Per CONVENTIONS.md §Naming: PascalCase for components, camelCase for hooks and utilities, kebab-case for directories. Applies: convention has no file-type restriction (broadly applicable).

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity display in New/Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` — existing empty state component (adapt for comparison-specific messaging)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (may supplement Skeleton placeholders)
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar layout patterns
- `src/hooks/useSboms.ts` — existing hook to populate SBOM selector dropdowns
- `src/hooks/useSbomComparison.ts` — comparison data hook (from task 8)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly Table usage with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for advisory display patterns

## Dependencies
- Depends on: Task 8 — Frontend comparison hook (uses `useSbomComparison` hook)

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] SBOM selectors load SBOM list and allow typeahead selection
- [ ] Compare button triggers comparison API call and displays results
- [ ] All six diff sections display with correct columns, count badges, and badge colors per Figma
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Empty state displays when no comparison is active
- [ ] Skeleton loading state shows during API call
- [ ] URL query params `left` and `right` are read on mount and updated on Compare
- [ ] Export dropdown has JSON and CSV options (disabled until data loads)

## Test Requirements
- [ ] Unit test: renders empty state when no query params are present
- [ ] Unit test: renders SBOM selectors populated with SBOM list data
- [ ] Unit test: Compare button is disabled when fewer than two SBOMs are selected
- [ ] Unit test: renders all six diff sections with correct data after comparison
- [ ] Unit test: DiffSection component renders expandable section with badge and table
