## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page and its components following the Figma design specifications. The page includes a header toolbar with SBOM selectors and a Compare button, vertically stacked collapsible diff sections with data tables, empty state, and loading state. This is the primary UI for the SBOM comparison feature.

## Files to Modify
- `src/routes.tsx` — add `/sbom/compare` route pointing to the new `SbomComparePage` component

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with two PatternFly `Select` dropdowns (SBOM selectors), a primary "Compare" button, and an "Export" `Dropdown` with JSON/CSV options
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section using PatternFly `ExpandableSection` with count `Badge` and composable `Table`
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response data for tests

## Implementation Notes
**Figma Design Reference**: The comparison view is a full-page layout per the Figma design context (SBOMCompare mock123).

**Header Toolbar (`CompareToolbar.tsx`)**:
- Left and right SBOM selectors use PatternFly `Select` (single, typeahead variant). Pre-populate from URL query params `left` and `right`. Fetch SBOM list via existing `useSboms` hook from `src/hooks/useSboms.ts`.
- "Compare" button is a PatternFly primary button, disabled until both selectors have values.
- "Export" uses PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded.

**Diff Sections (`DiffSection.tsx`)**:
- Each section uses PatternFly `ExpandableSection` with a title and count `Badge`. Badge colors: green (added/resolved), red (removed/new vulnerabilities), blue (version changes), yellow (license changes).
- Default expanded for sections with >0 items.
- Each section contains a PatternFly composable `Table` with sortable columns. For >100 rows, use virtualized rendering to prevent browser freezing (per NFR).
- The "New Vulnerabilities" section uses the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the Severity column. Rows with severity "Critical" get a highlighted background.

**Empty State**: When no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` as a reference pattern.

**Loading State**: While comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Header toolbar disabled during loading.

**URL Shareability**: Both SBOM IDs are encoded in the URL as query params (`/sbom/compare?left={id1}&right={id2}`). Use React Router `useSearchParams` for reading/updating.

Six diff sections appear in order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.

Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` page file scope.

Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents.
Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's `.tsx` component file scope.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` route file scope.

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; MSW for API mocking.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.tsx` test file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — reuse for severity display in New/Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` — pattern reference for empty state implementation
- `src/components/LoadingSpinner.tsx` — pattern reference for loading states
- `src/components/FilterToolbar.tsx` — pattern reference for toolbar layout with PatternFly
- `src/hooks/useSboms.ts` — reuse for fetching SBOM list for selector dropdowns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability rows

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] SBOM selectors load SBOM list and allow typeahead selection
- [ ] "Compare" button triggers API call and renders diff sections
- [ ] All six diff sections display correct data with proper table columns per Figma spec
- [ ] Count badges show correct counts with specified colors (green/red/blue/yellow)
- [ ] Empty state shows when no comparison is loaded (no query params)
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL is shareable — navigating to `/sbom/compare?left=1&right=2` loads comparison directly
- [ ] Critical severity rows in New Vulnerabilities section have highlighted background
- [ ] Large diffs (>100 rows) use virtualized rendering without browser freezing

## Test Requirements
- [ ] Unit test: renders empty state when no SBOM IDs are provided
- [ ] Unit test: renders comparison results with all six diff sections after API response
- [ ] Unit test: "Compare" button is disabled until both selectors have values
- [ ] Unit test: count badges show correct counts for each section
- [ ] Unit test: critical severity rows have highlighted styling in New Vulnerabilities section
- [ ] Unit test: SBOM selectors pre-populate from URL query params

## Verification Commands
- `npx vitest run --reporter=verbose -- SbomComparePage` — page tests pass
- `npx tsc --noEmit` — TypeScript compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 4 — Frontend API types and hook

sha256-md:659f90381c01f70449e91c4d5879db2b1e291cc84f2048d5ac5259900cf973a4
