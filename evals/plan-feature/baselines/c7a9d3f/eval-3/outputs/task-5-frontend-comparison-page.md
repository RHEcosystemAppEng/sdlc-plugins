## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page UI at `/sbom/compare` with header toolbar (SBOM selectors, Compare button) and collapsible diff sections. The page reads left/right SBOM IDs from URL query parameters, allows users to select SBOMs via typeahead dropdowns, and displays the structured diff in expandable sections with data tables. This implements the Figma design from figma-context.md.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable expandable diff section component with count badge and data table
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — SBOM typeahead select dropdown component

## Files to Modify
- `src/routes.tsx` — Add `/sbom/compare` route pointing to `SbomComparePage`
- `src/App.tsx` — Add lazy import for `SbomComparePage` if routes use lazy loading

## Implementation Notes
- **Page structure** (from Figma): Full-page layout with a header toolbar and vertically stacked collapsible diff sections.
- **Header toolbar**:
  - Two PatternFly `Select` components (single, typeahead) for left and right SBOM selection. Pre-populate from URL query params `left` and `right`. Fetch SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`.
  - "Compare" button (PatternFly primary Button): disabled until both selectors have values. On click, update URL query params and trigger the comparison API call via `useSbomComparison` hook (from Task 4).
  - Disable toolbar during loading state.
- **Diff sections** (six sections in order):
  1. **Added Packages** — green `Badge` count, table columns: Package Name, Version, License, Advisories (count)
  2. **Removed Packages** — red `Badge` count, table columns: Package Name, Version, License, Advisories (count)
  3. **Version Changes** — blue `Badge` count, table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  4. **New Vulnerabilities** — red `Badge` count, table columns: Advisory ID, Severity (using existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have a highlighted background.
  5. **Resolved Vulnerabilities** — green `Badge` count, table columns: Advisory ID, Severity, Title, Previously Affected Package
  6. **License Changes** — yellow `Badge` count, table columns: Package Name, Left License, Right License
- **DiffSection component**: Wraps PatternFly `ExpandableSection` with a title, `Badge` count (color prop), and a PatternFly composable `Table` inside. Default expanded for sections with >0 items. Sortable columns. Use virtualized list rendering for >100 rows per non-functional requirements.
- **SbomSelector component**: Wraps PatternFly `Select` (single, typeahead). Fetches SBOM list via `useSboms` hook. Displays SBOM name and version (e.g., "my-product-sbom v2.3.1").
- **Empty state**: When no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Follow the pattern in `src/components/EmptyStateCard.tsx`.
- **Loading state**: While comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section.
- **URL-shareable comparison**: URL encodes both SBOM IDs as query params (`?left={id1}&right={id2}`). Use React Router's `useSearchParams` for reading/writing URL params.
- **Routing**: Add the route to `src/routes.tsx` following the existing pattern (lazy-loaded page components via React Router v6).

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing shared component for severity level display in New/Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` — Existing empty state pattern to follow for the comparison empty state
- `src/components/FilterToolbar.tsx` — Reference for PatternFly toolbar patterns
- `src/components/LoadingSpinner.tsx` — Existing loading indicator (though this page uses Skeleton instead)
- `src/hooks/useSboms.ts` — Existing hook to fetch SBOM list for the selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Existing package table component pattern to reference for DiffSection tables
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Existing advisory list component pattern to reference for vulnerability sections
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping for critical vulnerability highlighting

## Acceptance Criteria
- [ ] Page renders at `/sbom/compare` route
- [ ] SBOM selectors load and display SBOM list with name and version
- [ ] URL query params `left` and `right` pre-populate the selectors
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] All six diff sections render with correct data and column layouts
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] Count badges show correct colors per section (green, red, blue, yellow)
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Existing `SeverityBadge` component is used for severity display
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading skeleton displays while comparison API is in progress
- [ ] URL is shareable — opening a URL with left/right params loads the comparison directly
- [ ] Large diffs (>100 changed packages) use virtualized list rendering

## Test Requirements
- [ ] Unit test: renders empty state when no query params are present
- [ ] Unit test: renders comparison results with all six diff sections
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: critical severity rows have highlighted styling
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Add MSW mock handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add comparison fixture data in `tests/mocks/fixtures/` (e.g., `comparison.json`)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Frontend API layer and hook
