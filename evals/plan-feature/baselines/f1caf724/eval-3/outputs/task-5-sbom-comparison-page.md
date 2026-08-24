## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with SBOM selectors and a Compare button, and vertically stacked collapsible diff sections showing added/removed packages, version changes, new/resolved vulnerabilities, and license changes. Each section uses a PatternFly `ExpandableSection` with a count `Badge` and a composable `Table`. The URL encodes both SBOM IDs for bookmarkable, shareable comparisons.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar, diff sections, and empty/loading states
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping PatternFly ExpandableSection, Badge, and Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM Select dropdowns, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — add route for `/sbom/compare` pointing to `SbomComparePage`
- `src/App.tsx` — add lazy import for `SbomComparePage` if required by the router setup

## Implementation Notes
- Per CONVENTIONS.md §Component Library: use PatternFly 5 components for all UI elements. See `src/components/SeverityBadge.tsx` for an existing PF5 component example.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TSX component file scope.
- Per CONVENTIONS.md §Page Structure: create a directory under `src/pages/` with the main component, test file, and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.
- Per CONVENTIONS.md §Testing: write unit tests using Vitest + React Testing Library with MSW for API mocking.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's test file scope.
- **Figma design — header toolbar:**
  - Two PatternFly `Select` (single, typeahead) dropdowns for left and right SBOM selection, pre-populated from URL query params `left` and `right`. Fetch SBOM list via existing `useSboms` hook.
  - Primary `Button` labeled "Compare", disabled until both selectors have values. Triggers the comparison API call via `useSbomComparison` hook.
  - Secondary `Dropdown` labeled "Export" with items "Export JSON" and "Export CSV". Disabled until a comparison result is loaded. Export is non-MVP but the UI element is included per the Figma design.
- **Figma design — diff sections (PatternFly `ExpandableSection`):**
  - Added Packages: green `Badge`, columns: Package Name, Version, License, Advisories (count)
  - Removed Packages: red `Badge`, columns: Package Name, Version, License, Advisories (count)
  - Version Changes: blue `Badge`, columns: Package Name, Left Version, Right Version, Direction
  - New Vulnerabilities: red `Badge`, columns: Advisory ID, Severity (using `SeverityBadge`), Title, Affected Package. Rows with severity "Critical" have a highlighted background.
  - Resolved Vulnerabilities: green `Badge`, columns: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: yellow `Badge`, columns: Package Name, Left License, Right License
- Each diff section contains a PatternFly composable `Table` with sortable columns. Use virtualized lists for sections with >100 rows to prevent browser freezing (non-functional requirement).
- Sections with >0 items should be expanded by default; sections with 0 items should be collapsed.
- **Figma design — empty state:** PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Figma design — loading state:** PatternFly `Skeleton` placeholders in each diff section, toolbar disabled during API call.
- URL must encode both SBOM IDs as query parameters (`?left={id1}&right={id2}`) for shareability. Use React Router `useSearchParams` for reading/updating query params.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity display component, use in New/Resolved Vulnerabilities diff tables
- `src/components/EmptyStateCard.tsx` — existing empty state component, follow the pattern for the comparison empty state
- `src/components/FilterToolbar.tsx` — existing toolbar pattern, reference for toolbar layout structure
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list, use for populating the SBOM selector dropdowns
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — existing page component, follow the page directory structure and component organization pattern

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] SBOM selectors load the SBOM list via `useSboms` hook
- [ ] URL query params `left` and `right` pre-populate the selectors on page load
- [ ] Compare button triggers comparison API call via `useSbomComparison` hook
- [ ] All six diff sections render with correct data, count badges, and color coding per Figma
- [ ] Rows with critical severity in New Vulnerabilities section have highlighted background
- [ ] Empty state displays when no comparison has been performed (no query params)
- [ ] Loading skeleton displays during API call
- [ ] Export dropdown renders and is disabled until comparison is loaded
- [ ] Sections with >0 items expanded by default, 0-item sections collapsed
- [ ] URL updates with both SBOM IDs when Compare is clicked, enabling shareable URLs

## Test Requirements
- [ ] Test that comparison page renders empty state on initial load without query params
- [ ] Test that selecting two SBOMs and clicking Compare triggers the comparison API call
- [ ] Test that diff sections render correct data from a mock comparison response
- [ ] Test that critical vulnerabilities in New Vulnerabilities have highlighted rows
- [ ] Test URL query param pre-population loads selectors and triggers comparison

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types and React Query hook
