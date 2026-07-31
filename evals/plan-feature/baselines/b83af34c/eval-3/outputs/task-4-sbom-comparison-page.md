## Repository
trustify-ui

## Target Branch
main

## Description
Build the SBOM comparison page and its components for feature TC-9003 (SBOM comparison view), following the Figma design specifications in figma-context.md. The page includes a header toolbar with SBOM selectors and Compare/Export buttons, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty state, and loading state. Register the `/sbom/compare` route and add a "Compare" navigation link on the SBOM list page.

**Priority**: Critical (inherited from TC-9003)
**Fix Version**: RHTPA 1.5.0 (inherited from TC-9003)

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar (PatternFly `Select` dropdowns for SBOM selection, primary "Compare" button, secondary "Export" `Dropdown`), diff section rendering, empty state (PatternFly `EmptyState` with `CodeBranchIcon`), and loading state (PatternFly `Skeleton`)
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable diff section component using PatternFly `ExpandableSection` with title, count `Badge` (color-coded: green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes), and a composable PatternFly `Table` with sortable columns
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page and diff section components

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to the lazy-loaded `SbomComparePage` component
- `src/pages/SbomListPage/SbomListPage.tsx` — add a "Compare SBOMs" toolbar button that navigates to `/sbom/compare`

## Implementation Notes
**Figma design reference (figma-context.md):**

The comparison page follows the Figma design specification with these PatternFly component mappings:

**Header Toolbar:**
- Two PatternFly `Select` components (single, typeahead variant) for left and right SBOM selection. Pre-populate from URL query params `left` and `right`. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display format: SBOM name + version (e.g., "my-product-sbom v2.3.1").
- Primary action PatternFly `Button` labeled "Compare", disabled until both selectors have values. On click, updates URL query params and triggers the `useSbomComparison` hook from Task 3.
- Secondary PatternFly `Dropdown` labeled "Export" with items "Export JSON" and "Export CSV". Disabled until comparison data is loaded.

**Diff Sections (6 total, in order per Figma):**
1. Added Packages — PatternFly `ExpandableSection`, green `Badge`, `Table` columns: Package Name, Version, License, Advisories (count)
2. Removed Packages — red `Badge`, same column structure
3. Version Changes — blue `Badge`, `Table` columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
4. New Vulnerabilities — red `Badge`, `Table` columns: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have highlighted background.
5. Resolved Vulnerabilities — green `Badge`, `Table` columns: Advisory ID, Severity, Title, Previously Affected Package
6. License Changes — yellow `Badge`, `Table` columns: Package Name, Left License, Right License

Each section defaults to expanded when its item count > 0 and collapsed when empty.

**Empty State** (no comparison performed): PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Loading State**: PatternFly `Skeleton` placeholders in each diff section while the API call is in progress. Header toolbar disabled during loading.

**Virtualization**: For diff sections with > 100 items, use virtualized rendering to prevent browser freezing (per non-functional requirements).

**URL-shareable comparison**: Encode both SBOM IDs in URL query parameters (`?left={id1}&right={id2}`). On page load, read query params and auto-trigger comparison if both are present.

**Route registration**: Add the route in `src/routes.tsx` following the existing pattern (e.g., `SbomListPage`, `SbomDetailPage`) with lazy-loaded component import.

**List page integration**: Add a PatternFly `Button` (variant="link") in the `SbomListPage` toolbar area that navigates to `/sbom/compare` using React Router's `useNavigate`.

Per CONVENTIONS.md §Framework: use React 18 and TypeScript for all components. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Component library: use PatternFly 5 components (`Select`, `ExpandableSection`, `Badge`, `Table`, `EmptyState`, `Skeleton`, `Dropdown`, `Button`) for all UI elements per the Figma-to-PatternFly mapping. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §State management: use the `useSbomComparison` React Query hook (from Task 3) for server state; no Redux. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Routing: register the `/sbom/compare` route in `src/routes.tsx` with lazy-loaded page component following React Router v6 patterns. Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Page structure: create the `SbomComparePage` directory under `src/pages/` with main component, test file, and `components/` subdirectory for page-specific components (DiffSection). Applies: task creates files in `src/pages/SbomComparePage/` matching the convention's `src/pages/` directory scope.

Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests; use MSW for API mocking in tests. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Naming: use PascalCase for components (`SbomComparePage`, `DiffSection`), camelCase for hooks and utilities. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Mutation pattern: the comparison page is read-only; if any user action requires state changes (e.g., export), use React Query mutation with `onSuccess` and `queryClient.invalidateQueries()`; never use `window.location.reload()`. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component; reuse in the New Vulnerabilities and Resolved Vulnerabilities diff sections
- `src/components/EmptyStateCard.tsx` — existing empty state component; evaluate for reuse or follow its pattern for the comparison empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; reuse or complement with PatternFly Skeleton per Figma spec
- `src/components/FilterToolbar.tsx` — existing filter toolbar; evaluate for reuse in the header toolbar area
- `src/hooks/useSboms.ts` — existing hook for SBOM list; reuse to populate the SBOM selector dropdowns
- `src/utils/severityUtils.ts` — existing severity utilities; reuse for severity ordering and color mapping in vulnerability diff sections

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections per Figma design
- [ ] Left and right SBOM selectors are PatternFly `Select` (typeahead) components populated via `useSboms` hook
- [ ] "Compare" button triggers the comparison API call and renders diff results in six collapsible `ExpandableSection` components
- [ ] Each diff section has a color-coded count `Badge` (green, red, blue, yellow per Figma spec)
- [ ] New Vulnerabilities section uses `SeverityBadge` component and highlights Critical rows
- [ ] Empty state displays PatternFly `EmptyState` with "Select two SBOMs to compare" when no comparison is active
- [ ] Loading state shows PatternFly `Skeleton` placeholders during API call
- [ ] URL query params (`left`, `right`) encode the selected SBOM IDs for bookmarking and sharing
- [ ] Page auto-triggers comparison on load when both URL params are present
- [ ] Route is registered in `src/routes.tsx` with lazy-loaded component
- [ ] "Compare SBOMs" button is present on the SBOM list page and navigates to `/sbom/compare`
- [ ] Diff sections with > 100 items use virtualized rendering

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no SBOM IDs are selected
- [ ] Unit test: SbomComparePage renders loading skeleton when comparison is in progress
- [ ] Unit test: SbomComparePage renders all six diff sections with correct data when comparison result is returned
- [ ] Unit test: DiffSection component renders ExpandableSection with correct title, badge count, and table
- [ ] Unit test: DiffSection is expanded by default when item count > 0 and collapsed when empty
- [ ] Unit test: New Vulnerabilities section highlights Critical severity rows
- [ ] Unit test: SBOM selectors populate options from useSboms hook
- [ ] Unit test: Compare button is disabled when either selector is empty

## Dependencies
- Depends on: Task 3 — SBOM comparison API types, client function, and React Query hook
