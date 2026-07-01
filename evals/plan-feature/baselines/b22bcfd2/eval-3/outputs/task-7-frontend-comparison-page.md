## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI at /sbom/compare following the Figma design context. The page includes a header toolbar with SBOM selector dropdowns and a Compare button, collapsible diff sections with data tables for each change category, empty state, and loading skeleton states. This is the primary user-facing component for the feature.

## Files to Modify
- `src/routes.tsx` — add route for /sbom/compare pointing to the new SbomComparePage
- `src/App.tsx` — add lazy import for SbomComparePage if routes use lazy loading

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section with count badge and data table
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — table for added packages diff section
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — table for removed packages diff section
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — table for version changes diff section
- `src/pages/SbomComparePage/components/VulnerabilityTable.tsx` — table for new/resolved vulnerabilities diff sections
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — table for license changes diff section

## Implementation Notes
**Page structure** (per Figma design context):

The page follows the existing page structure pattern from `src/pages/SbomDetailPage/SbomDetailPage.tsx` — a directory under `src/pages/` with a main component and a `components/` subdirectory.

**Header Toolbar (CompareToolbar.tsx)**:
- Two PatternFly `Select` components (single, typeahead variant) for left and right SBOM selection. Pre-populate from URL query params `left` and `right`. Fetch SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`.
- A primary PatternFly `Button` labeled "Compare" — disabled until both selectors have values. On click, update URL query params and trigger the comparison via `useSbomComparison` hook.
- A secondary PatternFly `Dropdown` for export with items "Export JSON" and "Export CSV" — disabled until comparison result is loaded.

**Diff Sections (DiffSection.tsx)**:
- Each section is a PatternFly `ExpandableSection` with a title and a PatternFly `Badge` showing the item count. Badge colors per Figma: green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes.
- Sections default to expanded when they have >0 items.
- Inside each section, render a PatternFly composable `Table` with sortable columns. For sections with >100 rows, use virtualized rendering to prevent browser freezing (per non-functional requirements).

**Diff section order** (per Figma):
1. Added Packages — columns: Package Name, Version, License, Advisories (count). Badge: green.
2. Removed Packages — columns: Package Name, Version, License, Advisories (count). Badge: red.
3. Version Changes — columns: Package Name, Left Version, Right Version, Direction. Badge: blue.
4. New Vulnerabilities — columns: Advisory ID, Severity (using `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Badge: red. Rows with severity "Critical" have highlighted background.
5. Resolved Vulnerabilities — columns: Advisory ID, Severity, Title, Previously Affected Package. Badge: green.
6. License Changes — columns: Package Name, Left License, Right License. Badge: yellow.

**Empty State**:
When no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Reference the existing `src/components/EmptyStateCard.tsx` for the empty state pattern.

**Loading State**:
While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading. Reference `src/components/LoadingSpinner.tsx` for existing loading patterns.

**URL sharing**:
Encode both SBOM IDs in URL query params (`?left={id1}&right={id2}`) so comparisons are bookmarkable and shareable. Use React Router's `useSearchParams` to read/write query params.

## Reuse Candidates
- `src/hooks/useSboms.ts` — fetch SBOM list for the selector dropdowns
- `src/components/SeverityBadge.tsx` — severity display in vulnerability tables
- `src/components/EmptyStateCard.tsx` — empty state pattern
- `src/components/LoadingSpinner.tsx` — loading state pattern
- `src/components/FilterToolbar.tsx` — PatternFly toolbar integration pattern reference
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — page structure pattern with components/ subdirectory
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — table component pattern for package data
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability rows

## Acceptance Criteria
- [ ] Comparison page renders at /sbom/compare route
- [ ] Left and right SBOM selectors use PatternFly Select with typeahead
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] All six diff sections render as PatternFly ExpandableSection with correct Badge colors
- [ ] Data tables display correct columns per Figma spec for each section
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] SeverityBadge component is used for vulnerability severity display
- [ ] Empty state shows when no comparison is loaded (PatternFly EmptyState with CodeBranchIcon)
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL encodes both SBOM IDs for bookmarking and sharing
- [ ] Export dropdown offers JSON and CSV options

## Test Requirements
- [ ] Unit test: renders empty state when no SBOM IDs are in URL params
- [ ] Unit test: selectors populate with SBOM list from useSboms hook
- [ ] Unit test: Compare button is disabled until both selectors have values
- [ ] Unit test: renders all six diff sections with correct data from comparison result
- [ ] Unit test: Critical vulnerability rows have highlighted styling
- [ ] Unit test: Export dropdown is disabled until comparison is loaded

## Dependencies
- Depends on: Task 6 — Frontend API types and hooks
