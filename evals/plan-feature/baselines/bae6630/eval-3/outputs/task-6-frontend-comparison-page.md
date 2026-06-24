# Task 6 — Frontend SBOM comparison page with Figma-based UI

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the main SBOM comparison page component following the Figma design specifications. The page includes a header toolbar with SBOM selectors and action buttons, and a vertically stacked set of collapsible diff sections displaying comparison results. The page reads `left` and `right` query parameters from the URL for shareable comparison links.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component. Reads `left` and `right` from URL search params using React Router `useSearchParams`. Renders the `CompareToolbar` and six `DiffSection` components for each diff category. Shows PatternFly `EmptyState` with `CodeBranchIcon` when no comparison is loaded. Shows PatternFly `Skeleton` placeholders during loading.
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page using React Testing Library and MSW mocks.
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar component with: two PatternFly `Select` (single, typeahead) dropdowns for SBOM selection populated via the existing `useSboms` hook from `src/hooks/useSboms.ts`; a primary "Compare" button disabled until both selectors have values; a secondary PatternFly `Dropdown` "Export" button with "Export JSON" and "Export CSV" items, disabled until comparison data is loaded. When "Compare" is clicked, updates URL search params with selected SBOM IDs.
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component using PatternFly `ExpandableSection`. Props: `title` (string), `count` (number), `badgeColor` (green/red/blue/yellow), `children` (table content). Default expanded when count > 0. Renders a PatternFly `Badge` with the count next to the title.
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data for testing.

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns the mock fixture data from `tests/mocks/fixtures/sbom-comparison.json`

## Implementation Notes
- **Figma: Header Toolbar** — Use PatternFly `Select` component with `variant="typeahead"` for SBOM selectors. Each selector displays SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populate selections from URL query params `left` and `right`. The "Compare" button uses PatternFly `Button` with `variant="primary"`, disabled until both selectors have values. The "Export" button uses PatternFly `Dropdown` with `variant="secondary"` containing two `DropdownItem` entries for JSON and CSV export.
- **Figma: Diff Sections** — Render six `DiffSection` components in order: Added Packages (green badge), Removed Packages (red badge), Version Changes (blue badge), New Vulnerabilities (red badge), Resolved Vulnerabilities (green badge), License Changes (yellow badge). Each section uses PatternFly `ExpandableSection` with a `Badge` count in the title.
- **Figma: Data Tables** — Each diff section contains a PatternFly composable `Table` with sortable columns. Added/Removed Packages tables have columns: Package Name, Version, License, Advisories (count). Version Changes table: Package Name, Left Version, Right Version, Direction. New Vulnerabilities table: Advisory ID, Severity (using existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" get a highlighted background. Resolved Vulnerabilities table: Advisory ID, Severity, Title, Previously Affected Package. License Changes table: Package Name, Left License, Right License.
- **Figma: Empty State** — When no comparison is loaded (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Figma: Loading State** — During API call, show PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading.
- For large diffs (>100 rows), implement virtualized table rendering to prevent browser freezing per the non-functional requirements.
- Use the `useSbomComparison` hook from `src/hooks/useSbomComparison.ts` for data fetching.
- Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the SBOM selector dropdowns.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display in vulnerability tables.
- Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` as reference for the empty state pattern.

## Acceptance Criteria
- [ ] Comparison page renders header toolbar with two SBOM selectors, Compare button, and Export dropdown
- [ ] SBOM selectors are PatternFly `Select` with typeahead, populated from `useSboms` hook
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] Export dropdown is disabled until comparison results are loaded
- [ ] Six diff sections render as PatternFly `ExpandableSection` with correct badge colors
- [ ] Each section contains a PatternFly composable `Table` with correct columns per category
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] `SeverityBadge` component is used for severity display in vulnerability tables
- [ ] Empty state shows PatternFly `EmptyState` with `CodeBranchIcon` when no comparison is loaded
- [ ] Loading state shows `Skeleton` placeholders and disables toolbar
- [ ] URL search params `left` and `right` pre-populate SBOM selectors for shareable links
- [ ] Diff sections default expanded when they contain items (count > 0)

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders comparison results when data is loaded
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: all six diff sections render with correct titles and badges
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted styling
- [ ] Unit test: SBOM selectors pre-populate from URL query params

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 5 — Frontend React Query hook for SBOM comparison

## Digest
[sdlc-workflow] Description digest: sha256-md:d98d1eee3661eed0de565c7ee04106807eb22afc555bb48a09aa577e21f30a24
