## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page at `/sbom/compare` following the Figma design. The page features a header toolbar with two SBOM selectors (PatternFly Select with typeahead), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page supports URL-shareable comparisons via `left` and `right` query parameters. This is the main UI deliverable for the SBOM comparison view feature.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section component wrapping PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/SbomSelector.tsx` -- SBOM selector dropdown component using PatternFly Select with typeahead, backed by useSboms hook
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` -- header toolbar component containing both selectors, Compare button, and Export dropdown
- `tests/mocks/fixtures/sbom-comparison.json` -- mock comparison API response data for tests

## Files to Modify
- `src/routes.tsx` -- add route definition for `/sbom/compare` pointing to lazy-loaded SbomComparePage
- `tests/mocks/handlers.ts` -- add MSW handler for GET /api/v2/sbom/compare

## Implementation Notes

Per CONVENTIONS.md §Page Structure: create a directory under `src/pages/` with main component, test file, and `components/` subdirectory for page-specific components. See `src/pages/SbomDetailPage/` for the established page directory structure.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.

Per CONVENTIONS.md §Component Library: use PatternFly 5 components throughout. See `src/pages/SbomListPage/SbomListPage.tsx` for PatternFly component usage patterns.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. See `src/routes.tsx` for the existing route definition pattern.
Applies: task modifies `src/routes.tsx` matching the convention's routing file scope.

Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests and MSW for API mocking. See `src/pages/SbomListPage/SbomListPage.test.tsx` for the established test setup pattern.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.test.tsx` test file scope.

**Figma component mapping:**

| Figma Element | PatternFly Component | Notes |
|---|---|---|
| SBOM selector | `Select` (single, typeahead) | Fetches SBOM list via existing `useSboms` hook |
| Diff section | `ExpandableSection` | Default expanded for sections with >0 items |
| Count badge | `Badge` | Color: green (added/resolved), red (removed/new vuln), blue (version changes), yellow (license) |
| Data table | `Table` (composable) | Sortable columns, virtualized for >100 rows |
| Severity indicator | `SeverityBadge` | Existing shared component in `src/components/` |
| Empty state | `EmptyState` with `CodeBranchIcon` | "Select two SBOMs to compare" |
| Export button | `Dropdown` | Two items: JSON, CSV. Disabled until comparison loaded. Non-MVP functionality. |

**Diff section details:**

1. **Added Packages** (green badge): columns -- Package Name, Version, License, Advisories (count)
2. **Removed Packages** (red badge): columns -- Package Name, Version, License, Advisories (count)
3. **Version Changes** (blue badge): columns -- Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
4. **New Vulnerabilities** (red badge): columns -- Advisory ID, Severity (SeverityBadge), Title, Affected Package. Rows with severity "Critical" have highlighted background.
5. **Resolved Vulnerabilities** (green badge): columns -- Advisory ID, Severity, Title, Previously Affected Package
6. **License Changes** (yellow badge): columns -- Package Name, Left License, Right License

**URL-shareable comparison:** Read `left` and `right` from URL query parameters using React Router's `useSearchParams`. Pre-populate the SBOM selectors from these values. When the user clicks Compare, update the URL query parameters so the comparison is bookmarkable.

**Empty state:** When no query parameters are present and no comparison has been performed, show a PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Loading state:** While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading.

**Virtualized lists (NFR):** For diff sections with >100 rows, use virtualized rendering (e.g., react-window or PatternFly's built-in virtualization) to prevent browser freezing with large diffs.

**Export functionality (non-MVP):** Include the Export dropdown button in the header toolbar UI per the Figma design. The dropdown shows "Export JSON" and "Export CSV" options and is disabled until comparison data is loaded. The actual export implementation (generating and downloading files) is non-MVP scope -- implement placeholder click handlers that can be completed in a follow-up task.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- existing shared component for severity level badges; use in New Vulnerabilities and Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` -- existing empty state component; use as reference for the comparison empty state (may need customization for CodeBranchIcon)
- `src/components/LoadingSpinner.tsx` -- existing loading indicator; reference for loading state patterns
- `src/hooks/useSboms.ts` -- existing React Query hook for SBOM list; use in SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- existing package table component; reference for table column definition and PatternFly Table usage
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` -- existing advisory list component; reference for advisory data display patterns
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping; use for critical vulnerability highlighting

## Acceptance Criteria
- [ ] Comparison page renders at /sbom/compare route
- [ ] SBOM selectors load SBOM list and allow single selection with typeahead
- [ ] Compare button is disabled until both selectors have values
- [ ] Compare button triggers API call and renders diff sections
- [ ] All six diff sections render with correct columns and count badges
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerability rows with "Critical" severity have highlighted background
- [ ] URL query parameters (left, right) are read on page load and updated on compare
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders while API call is in progress
- [ ] Export dropdown is present in toolbar (non-MVP: actual export can use placeholder handlers)
- [ ] Page handles large diffs (>100 items per section) without browser freezing

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: SBOM selectors populate from useSboms hook data
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: comparison data renders correctly in all six diff sections
- [ ] Unit test: critical vulnerabilities have highlighted row styling
- [ ] Unit test: empty diff sections are collapsed by default
- [ ] Unit test: URL query params are used to pre-populate selectors
- [ ] Unit test: loading state shows Skeleton placeholders
- [ ] MSW mock handler returns comparison fixture data for test assertions

## Verification Commands
- `npm test -- --run SbomComparePage` -- run comparison page unit tests
- `npm run dev` then navigate to `/sbom/compare` -- verify page renders correctly in browser

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 4 -- Add comparison API types, client function, and React Query hook
