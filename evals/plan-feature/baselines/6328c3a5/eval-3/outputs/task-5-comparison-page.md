## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page at `/sbom/compare` with a header toolbar containing two SBOM selectors and a Compare button, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), an empty state for initial page load, and skeleton loading states. The page reads `left` and `right` query parameters from the URL for shareable comparisons. This is the primary UI deliverable of the SBOM comparison feature.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component with count badge and data table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors and Compare button

## Files to Modify
- `src/routes.tsx` — Add `/sbom/compare` route pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.

Per CONVENTIONS.md §Component Library: all UI components must use PatternFly 5 equivalents.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests and MSW for API mocking.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's test file scope.

**Figma design specifications (from figma-context.md):**

**Header toolbar:**
- Left SBOM selector: PatternFly `Select` (single, typeahead) showing SBOM name and version. Pre-populated from URL query param `left`. Fetches SBOM list via existing `useSboms` hook.
- Right SBOM selector: identical `Select` for second SBOM. Pre-populated from URL query param `right`.
- "Compare" button: PatternFly primary button, disabled until both selectors have values. Triggers navigation to update URL params and fires comparison API call.

**Diff sections** (PatternFly `ExpandableSection` with `Badge` count and composable `Table`):
1. **Added Packages** — columns: Package Name, Version, License, Advisories (count). Badge color: green.
2. **Removed Packages** — columns: Package Name, Version, License, Advisories (count). Badge color: red.
3. **Version Changes** — columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade). Badge color: blue.
4. **New Vulnerabilities** — columns: Advisory ID, Severity (use existing `SeverityBadge`), Title, Affected Package. Badge color: red. Rows with severity "Critical" must have highlighted background.
5. **Resolved Vulnerabilities** — columns: Advisory ID, Severity, Title, Previously Affected Package. Badge color: green.
6. **License Changes** — columns: Package Name, Left License, Right License. Badge color: yellow.

Default behavior: sections with >0 items are expanded; sections with 0 items are collapsed.

**Empty state** (PatternFly `EmptyState`):
- Icon: `CodeBranchIcon` (PatternFly)
- Title: "Select two SBOMs to compare"
- Body: "Choose an SBOM for each side and click Compare to see what changed."

**Loading state:** PatternFly `Skeleton` placeholders in each diff section while API call is in progress. Header toolbar disabled during loading.

**Critical vulnerability highlighting:** Rows in the "New Vulnerabilities" section where severity is "Critical" must have a highlighted/warning background color.

**URL sharing:** Use React Router `useSearchParams` to read `left` and `right` query parameters. When both params are present on page load, auto-trigger the comparison. When the user clicks Compare, update the URL params for bookmarkability.

**Virtualized lists:** For diff sections with >100 rows, implement virtualized rendering to prevent browser freezing (non-functional requirement). Consider `react-window` or PatternFly's built-in virtualization.

**PatternFly component mapping:**
| UI Element | PatternFly Component |
|---|---|
| SBOM selector | `Select` (single, typeahead) |
| Diff section | `ExpandableSection` |
| Count badge | `Badge` |
| Data table | `Table` (composable) |
| Severity indicator | `SeverityBadge` (existing shared component) |
| Empty state | `EmptyState` |
| Loading skeleton | `Skeleton` |

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity level badge component; use directly in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — existing empty state placeholder; evaluate whether it can be reused or if a custom EmptyState is needed for the comparison page
- `src/components/LoadingSpinner.tsx` — existing loading indicator; may be used alongside Skeleton placeholders
- `src/hooks/useSboms.ts` — existing React Query hook for SBOM list; use to populate the SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference for table column patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component; reference for advisory display patterns

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] SBOM selectors load and display SBOM list from existing `useSboms` hook
- [ ] Compare button is disabled until both SBOM selectors have values
- [ ] Clicking Compare triggers API call and displays diff results in six sections
- [ ] Each diff section shows correct count in badge with appropriate color (green/red/blue/yellow)
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Severity badges display correctly using existing `SeverityBadge` component
- [ ] Empty state displays with correct icon, title, and body text when no comparison is loaded
- [ ] Skeleton loading state shows while comparison API call is in progress
- [ ] URL query params `left` and `right` are read on page load to pre-populate selectors
- [ ] URL is updated when Compare is clicked, enabling shareable/bookmarkable comparisons
- [ ] Tables have sortable columns

## Test Requirements
- [ ] Unit test: renders empty state when no SBOM IDs are in URL params
- [ ] Unit test: renders comparison results with all six diff sections
- [ ] Unit test: sections with 0 items are collapsed, sections with >0 items are expanded
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button is enabled when both SBOMs are selected
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted styling
- [ ] Unit test: loading skeleton renders while comparison is being fetched
- [ ] Unit test: SBOM selectors pre-populate from URL query params

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API client, types, and React Query hook
