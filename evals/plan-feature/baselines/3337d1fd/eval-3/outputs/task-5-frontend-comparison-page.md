## Repository
trustify-ui

## Target Branch
main

## Description
Build the SBOM comparison page with a header toolbar for SBOM selection and vertically stacked collapsible diff sections. This is the core UI component of the feature, rendering the structured diff returned by the comparison API into an interactive, navigable view following the Figma design specifications.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with SBOM selectors, compare button, and diff sections
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with left/right SBOM Select dropdowns, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable expandable diff section with count badge and data table
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page

## Implementation Notes
**Page layout (SbomComparePage.tsx):**
Use the Figma design context for the full-page layout. The page has a header toolbar (`ComparisonToolbar`) followed by six vertically stacked `DiffSection` components. Read URL query params `left` and `right` using React Router's `useSearchParams` to pre-populate selectors. Call `useSbomComparison(leftId, rightId)` from `src/hooks/useSbomComparison.ts` when both IDs are set and the user clicks Compare. Render a PatternFly `EmptyState` when no comparison has been performed, using `CodeBranchIcon` with title "Select two SBOMs to compare" and body "Choose an SBOM for each side and click Compare to see what changed."

**ComparisonToolbar component:**
- Two PatternFly `Select` components (single, typeahead variant) for left and right SBOM selection. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in each option.
- A primary PatternFly `Button` labeled "Compare", disabled until both selectors have values. On click, updates URL query params and triggers the comparison API call.
- A secondary PatternFly `Dropdown` labeled "Export" with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded.
- Entire toolbar is disabled during loading state.

**DiffSection component:**
- Wraps PatternFly `ExpandableSection` with a title and PatternFly `Badge` showing the item count. Badge color varies by section: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- Default expanded when item count > 0, collapsed when empty.
- Contains a PatternFly `Table` (composable variant) with sortable columns. Column definitions are passed as props since each section has different columns.
- For the New Vulnerabilities section, rows with severity "Critical" should have a highlighted background row style.
- The Severity column in vulnerability sections uses the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`.

**Loading state:**
While the comparison API call is in progress, render PatternFly `Skeleton` placeholders inside each diff section area.

**Section order and columns per Figma design:**
1. Added Packages: Package Name, Version, License, Advisories (count) — green badge
2. Removed Packages: Package Name, Version, License, Advisories (count) — red badge
3. Version Changes: Package Name, Left Version, Right Version, Direction — blue badge
4. New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package — red badge
5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package — green badge
6. License Changes: Package Name, Left License, Right License — yellow badge

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing severity badge component for vulnerability rows
- `src/components/EmptyStateCard.tsx` — Reference for empty state pattern (use PatternFly EmptyState directly per Figma)
- `src/components/LoadingSpinner.tsx` — Reference for loading state pattern
- `src/hooks/useSboms.ts` — Existing hook for populating SBOM selector options
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Reference for PatternFly Table usage with sortable columns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Reference for advisory display patterns

## Acceptance Criteria
- [ ] Comparison page renders with header toolbar and empty state on initial load
- [ ] SBOM selectors are populated from the existing SBOM list API
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] Clicking Compare triggers the comparison API call and renders diff sections
- [ ] All six diff sections render with correct columns per Figma design
- [ ] Each section shows a count badge with the correct color
- [ ] Sections with items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Severity column uses the existing SeverityBadge component
- [ ] Loading state shows Skeleton placeholders
- [ ] Empty state shows CodeBranchIcon with correct title and body text
- [ ] Export dropdown is disabled until comparison data is loaded
- [ ] URL query params `left` and `right` pre-populate selectors on page load

## Test Requirements
- [ ] Unit test: renders empty state when no comparison data exists
- [ ] Unit test: renders all six diff sections with correct data after comparison
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: DiffSection expands when count > 0, collapses when count is 0
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted styling

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run --reporter=verbose -- SbomComparePage` — component tests pass

## Dependencies
- Depends on: Task 4 — Frontend SBOM comparison API types, client function, and hook
