## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI as specified in the Figma design. The page includes a header toolbar with two SBOM selectors, a Compare button, and an Export dropdown, followed by six vertically stacked collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). The page supports empty state (no comparison yet), loading state (API call in progress), and URL-shareable comparisons via query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown

## Implementation Notes
### Figma design specifications

**Header Toolbar (CompareToolbar.tsx):**
- Left SBOM selector: PatternFly `Select` (single, typeahead) showing SBOM name and version. Pre-populated from URL query param `left`. Fetches SBOM list via existing `useSboms` hook.
- Right SBOM selector: identical PatternFly `Select` dropdown for the second SBOM. Pre-populated from URL query param `right`.
- "Compare" button: PatternFly primary action `Button`, disabled until both selectors have values. Triggers the comparison API call.
- "Export" dropdown: PatternFly `Dropdown` with two items "Export JSON" and "Export CSV". Disabled until a comparison result is loaded.

**Diff Sections (DiffSection.tsx):**
Each section uses PatternFly `ExpandableSection` with a title, PatternFly `Badge` for count, and a composable `Table` inside. Sections default expanded when item count > 0.

1. **Added Packages** — Badge color: green. Table columns: Package Name, Version, License, Advisories (count).
2. **Removed Packages** — Badge color: red. Table columns: Package Name, Version, License, Advisories (count).
3. **Version Changes** — Badge color: blue. Table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
4. **New Vulnerabilities** — Badge color: red. Table columns: Advisory ID, Severity (using existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have a highlighted background.
5. **Resolved Vulnerabilities** — Badge color: green. Table columns: Advisory ID, Severity, Title, Previously Affected Package.
6. **License Changes** — Badge color: yellow. Table columns: Package Name, Left License, Right License.

**Empty State:**
When no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Use the existing `EmptyStateCard` component pattern from `src/components/EmptyStateCard.tsx`.

**Loading State:**
While the comparison API call is in progress, each diff section shows PatternFly `Skeleton` placeholders. The header toolbar is disabled during loading.

**Component mapping (Figma to PatternFly):**

| Figma Element | PatternFly Component |
|---|---|
| SBOM selector | `Select` (single, typeahead) |
| Diff section | `ExpandableSection` |
| Count badge | `Badge` |
| Data table | `Table` (composable, sortable columns) |
| Severity indicator | `SeverityBadge` (existing shared component) |
| Empty state | `EmptyState` |
| Export button | `Dropdown` |

### Technical implementation

- Per CONVENTIONS.md §Component Library: use PatternFly 5 components for all UI elements (Select, ExpandableSection, Badge, Table, EmptyState, Dropdown, Button, Skeleton).
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.
- Per CONVENTIONS.md §Page Structure: create the page directory at `src/pages/SbomComparePage/` with a main component, test file, and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` page scope.
- Use `useSearchParams()` from React Router to read/write `left` and `right` query parameters for URL-shareable comparisons.
- Use the `useSbomComparison` hook from Task 4 for data fetching.
- Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the SBOM selector dropdowns.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for vulnerability severity display.
- For large diffs (>100 changed items), use virtualized lists to prevent browser freezing (non-functional requirement).
- Export functionality (non-MVP): implement client-side JSON/CSV export from the loaded comparison data. JSON export serializes the `SbomComparisonResult`. CSV export flattens each diff section into rows.
- Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests with MSW for API mocking.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.test.tsx` test file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for rendering severity levels with color coding; reuse directly in the New Vulnerabilities and Resolved Vulnerabilities diff sections
- `src/components/EmptyStateCard.tsx` — existing empty state pattern; follow its structure for the comparison empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; consider for the loading state alongside PatternFly Skeleton
- `src/hooks/useSboms.ts` — existing hook for loading the SBOM list; reuse for populating the selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference its Table composition pattern for the diff section tables
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component; reference its advisory rendering pattern for vulnerability sections
- `src/utils/severityUtils.ts` — existing severity ordering and color mapping utilities

## Acceptance Criteria
- [ ] Comparison page renders with header toolbar containing two SBOM selectors, Compare button, and Export dropdown
- [ ] SBOM selectors are PatternFly Select (single, typeahead) populated from `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call via `useSbomComparison`
- [ ] Six diff sections render as PatternFly ExpandableSection with correct titles and count Badges
- [ ] Badge colors match Figma spec: green (Added, Resolved), red (Removed, New Vulns), blue (Version Changes), yellow (License Changes)
- [ ] Each diff section contains a sortable PatternFly Table with correct columns per section
- [ ] New Vulnerabilities rows with severity "Critical" have highlighted background
- [ ] SeverityBadge component is used for vulnerability severity display
- [ ] Empty state displays when no comparison is loaded (PatternFly EmptyState with CodeBranchIcon)
- [ ] Loading state shows Skeleton placeholders while API call is in progress
- [ ] URL query parameters `left` and `right` pre-populate selectors for shareable URLs
- [ ] Export dropdown offers JSON and CSV options (disabled until comparison loaded)
- [ ] Large diffs (>100 items) use virtualized lists

## Test Requirements
- [ ] Unit test: comparison page renders empty state when no query params present
- [ ] Unit test: comparison page renders loading state while API call is in progress
- [ ] Unit test: comparison page renders all six diff sections with correct data
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted background
- [ ] Unit test: URL query parameters pre-populate SBOM selectors
- [ ] Unit test: Export dropdown is disabled when no comparison result is loaded

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types and React Query hook
