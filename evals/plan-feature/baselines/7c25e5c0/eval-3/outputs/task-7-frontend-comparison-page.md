## Repository
trustify-ui

## Target Branch
main

## Description
Create the SBOM comparison page at `/sbom/compare` with a PatternFly-based layout matching the Figma design. The page features a header toolbar with two SBOM selectors, a "Compare" action button, and vertically stacked collapsible diff sections — each with a data table displaying the comparison results. Includes URL-shareable comparisons via query parameters and proper empty/loading states.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable expandable diff section with count badge and data table
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — SBOM selector dropdown component wrapping PatternFly Select

## Files to Modify
- `src/routes.tsx` — add `/sbom/compare` route pointing to `SbomComparePage`

## Implementation Notes
Build the page from PatternFly 5 components as specified in the Figma design context:

**Header toolbar:**
- Two SBOM selectors using PatternFly `Select` (single, typeahead) — each fetches the SBOM list via the existing `useSboms` hook from `src/hooks/useSboms.ts`
- Pre-populate selectors from URL query params `left` and `right` using React Router's `useSearchParams`
- "Compare" button: PatternFly primary `Button`, disabled until both selectors have values
- "Export" dropdown: PatternFly `Dropdown` with "Export JSON" and "Export CSV" options, disabled until comparison result is loaded (export implementation is deferred — non-MVP)

**Diff sections (6 sections, each using DiffSection component):**
1. **Added Packages** — PatternFly `ExpandableSection`, green `Badge` count, `Table` with columns: Package Name, Version, License, Advisories (count)
2. **Removed Packages** — red `Badge`, same column structure as Added Packages
3. **Version Changes** — blue `Badge`, `Table` columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
4. **New Vulnerabilities** — red `Badge`, `Table` columns: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have highlighted background
5. **Resolved Vulnerabilities** — green `Badge`, `Table` columns: Advisory ID, Severity, Title, Previously Affected Package
6. **License Changes** — yellow `Badge`, `Table` columns: Package Name, Left License, Right License

**Empty state:** PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body text "Choose an SBOM for each side and click Compare to see what changed."

**Loading state:** PatternFly `Skeleton` placeholders in each diff section while the comparison API call is in progress; header toolbar disabled during loading.

**Virtualization:** For diff sections with >100 rows, use virtualized list rendering to prevent browser freezing (per NFR).

**Routing:** Register `/sbom/compare` in `src/routes.tsx` following the existing lazy-loaded page pattern using React Router v6.

Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's React component scope.

Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's route definition scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity level display, used in the New Vulnerabilities and Resolved Vulnerabilities diff sections
- `src/components/EmptyStateCard.tsx` — existing empty state component, reference for PatternFly EmptyState pattern
- `src/components/LoadingSpinner.tsx` — existing loading indicator, reference for loading state pattern
- `src/components/FilterToolbar.tsx` — existing filter toolbar using PatternFly, reference for toolbar layout patterns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component, reference for PatternFly Table with package data
- `src/hooks/useSboms.ts` — existing hook for SBOM list, used by the SBOM selector dropdowns

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selector dropdowns load SBOM list and allow selection
- [ ] URL query params `left` and `right` pre-populate selectors and are updated on selection
- [ ] "Compare" button triggers comparison and displays results
- [ ] All six diff sections render with correct data tables and column layouts
- [ ] Each diff section has a colored count badge matching the Figma spec (green, red, blue, yellow)
- [ ] Sections with 0 items are collapsed by default; sections with >0 items are expanded
- [ ] Empty state shows when no comparison has been performed
- [ ] Loading skeletons show during API call
- [ ] Critical vulnerability rows have highlighted background in New Vulnerabilities section
- [ ] Route is registered in `src/routes.tsx`

## Test Requirements
- [ ] Component renders empty state on initial load (no query params)
- [ ] Component renders comparison results after clicking Compare
- [ ] URL query params are correctly read and written
- [ ] Each diff section renders the correct number of items
- [ ] Critical vulnerability rows have highlighted styling

## Dependencies
- Depends on: Task 6 — Frontend comparison hook
