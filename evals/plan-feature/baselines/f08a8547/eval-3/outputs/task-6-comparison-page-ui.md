## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with SBOM selectors and Compare/Export buttons, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), an empty state for initial page load, and loading skeletons during API calls. Each diff section uses PatternFly ExpandableSection with a data table inside. The page reads SBOM IDs from URL query parameters for shareable comparisons.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component (ExpandableSection + Badge + Table)
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM Select dropdowns, Compare button, and Export dropdown

## Implementation Notes
- **Figma design reference**: the comparison view uses a full-page layout with vertically stacked collapsible sections. Each section is a PatternFly `ExpandableSection` with a count `Badge` and composable `Table`.
- **PatternFly component mapping** (from Figma):
  - SBOM selectors: `Select` (single, typeahead) — fetches SBOM list via existing `useSboms` hook
  - Diff sections: `ExpandableSection` — default expanded for sections with >0 items
  - Count badges: `Badge` — green for Added/Resolved, red for Removed/New Vulnerabilities, blue for Version Changes, yellow for License Changes
  - Data tables: `Table` (composable) — sortable columns, virtualized for >100 rows
  - Severity indicator: existing `SeverityBadge` shared component from `src/components/SeverityBadge.tsx`
  - Empty state: `EmptyState` with `CodeBranchIcon` — title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Loading state: `Skeleton` placeholders in each diff section
  - Export button: `Dropdown` with two items "Export JSON" and "Export CSV"
- **Diff section table columns**:
  1. Added Packages: Package Name, Version, License, Advisories (count)
  2. Removed Packages: Package Name, Version, License, Advisories (count)
  3. Version Changes: Package Name, Left Version, Right Version, Direction
  4. New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package — rows with severity "Critical" get highlighted background
  5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  6. License Changes: Package Name, Left License, Right License
- **URL-shareable comparison**: read `left` and `right` from URL search params (`useSearchParams`). When both are present, auto-trigger the comparison on page load. Update URL when user clicks Compare.
- **Virtualized lists**: for diff sections with >100 items, use virtualized rendering to prevent browser freezing (non-functional requirement). Consider `react-window` or PatternFly's built-in virtualization.
- **Export functionality** (non-MVP but included per Figma): the Export dropdown generates JSON or CSV from the in-memory comparison result. No additional API call needed.
- DiffSection component should be generic and reusable across all six section types. It accepts: title, count, badge color, columns configuration, and row data.
- Per CONVENTIONS.md: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.
- Per CONVENTIONS.md: all UI components use PatternFly 5 equivalents. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md: use PascalCase for component names. Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's naming scope.

**Data component rendering scope:**
- All six diff section tables are top-level page components (not nested inside wizard steps or tabs), so they render the full comparison result — no per-context filtering is needed.

**Relevant constraints from docs/constraints.md:**
- Commit rules (section 2): every commit must reference TC-9003, follow Conventional Commits, include AI attribution trailer
- PR rules (section 3): branch named after Jira issue ID, PR link posted to Jira task
- Code change rules (section 5): changes scoped to listed files, inspect code before modifying, follow referenced patterns, no duplication

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity level display, used in New Vulnerabilities and Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` — existing empty state component, reference for empty state pattern (though comparison page uses PatternFly EmptyState directly per Figma)
- `src/components/LoadingSpinner.tsx` — existing loading indicator, may be used alongside Skeleton placeholders
- `src/components/FilterToolbar.tsx` — existing reusable toolbar, reference for toolbar layout patterns
- `src/hooks/useSboms.ts` — existing hook to fetch SBOM list for the selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component, reference for table structure and column patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component, reference for advisory display patterns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping utility

## Acceptance Criteria
- [ ] SbomComparePage renders at /sbom/compare
- [ ] Header toolbar contains two SBOM Select dropdowns (typeahead, single-select) populated from useSboms hook
- [ ] Compare button is disabled until both SBOM selectors have values
- [ ] Compare button triggers comparison API call via useSbomComparison hook
- [ ] Export dropdown shows "Export JSON" and "Export CSV" options, disabled until comparison result loads
- [ ] Six diff sections render as ExpandableSection components in correct order
- [ ] Each section shows count Badge with correct color (green/red/blue/yellow per Figma spec)
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Added Packages table shows: Package Name, Version, License, Advisories columns
- [ ] Removed Packages table shows: Package Name, Version, License, Advisories columns
- [ ] Version Changes table shows: Package Name, Left Version, Right Version, Direction columns
- [ ] New Vulnerabilities table shows: Advisory ID, Severity (SeverityBadge), Title, Affected Package columns
- [ ] Rows with "Critical" severity in New Vulnerabilities have highlighted background
- [ ] Resolved Vulnerabilities table shows: Advisory ID, Severity, Title, Previously Affected Package columns
- [ ] License Changes table shows: Package Name, Left License, Right License columns
- [ ] Empty state displays when no comparison has been performed (CodeBranchIcon, "Select two SBOMs to compare")
- [ ] Loading state shows Skeleton placeholders while comparison API call is in progress
- [ ] URL query params `left` and `right` are read on page load for shareable comparisons
- [ ] URL is updated with selected SBOM IDs when Compare is clicked

## Test Requirements
- [ ] Unit test: renders empty state when no SBOM IDs are selected
- [ ] Unit test: renders SBOM selectors populated with data from useSboms
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button is enabled when both SBOMs are selected
- [ ] Unit test: renders loading skeletons while comparison is loading
- [ ] Unit test: renders all six diff sections with correct titles and data
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Unit test: sections with >0 items are expanded by default
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted style
- [ ] Unit test: Export dropdown items trigger JSON/CSV download
- [ ] Unit test: reads left and right from URL search params and auto-triggers comparison

## Dependencies
- Depends on: Task 4 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 5 — Add SBOM comparison API types, client function, and React Query hook
