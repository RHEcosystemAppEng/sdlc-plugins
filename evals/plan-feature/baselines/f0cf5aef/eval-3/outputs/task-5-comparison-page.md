## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page component per the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown, plus six vertically stacked collapsible diff sections. Each diff section displays a data table with category-specific columns. The page supports URL-shareable comparisons via `left` and `right` query parameters, and handles empty state (no comparison performed) and loading state (API call in progress).

## Files to Create
- `src/pages/SbomComparisonPage/SbomComparisonPage.tsx` — main comparison page component with header toolbar, SBOM selectors, Compare button, and diff section rendering
- `src/pages/SbomComparisonPage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count badge and data table
- `src/pages/SbomComparisonPage/components/ComparisonToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown

## Implementation Notes
Per the frontend page structure convention: each page gets its own directory under `src/pages/` with a main component and optional `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparisonPage/SbomComparisonPage.tsx` matching the convention's page directory scope.

Per the frontend component library convention: all UI components use PatternFly 5 equivalents.
Applies: task creates `src/pages/SbomComparisonPage/SbomComparisonPage.tsx` matching the convention's TypeScript component scope.

**Component mapping (from Figma):**

| Figma Element | PatternFly Component | Notes |
|---|---|---|
| SBOM selector | `Select` (single, typeahead) | Fetches SBOM list via existing `useSboms` hook |
| Diff section | `ExpandableSection` | Default expanded for sections with >0 items |
| Count badge | `Badge` | Green for added/resolved, red for removed/new vulns, blue for version changes, yellow for license changes |
| Data table | `Table` (composable) | Sortable columns, no pagination |
| Severity indicator | `SeverityBadge` | Existing shared component in `src/components/` |
| Empty state | `EmptyState` with `CodeBranchIcon` | "Select two SBOMs to compare" |
| Loading state | `Skeleton` | PatternFly Skeleton placeholder per diff section |
| Export button | `Dropdown` | Two items: "Export JSON", "Export CSV". Disabled until comparison loaded. Non-MVP — render shell but disable functionality. |

**Header Toolbar behavior:**
- Left SBOM selector pre-populated from URL query param `left`
- Right SBOM selector pre-populated from URL query param `right`
- Compare button disabled until both selectors have values
- Compare button triggers the comparison API call (via `useSbomComparison` hook)
- On Compare click, update URL query params for shareability
- Toolbar disabled during loading state

**Diff sections** (in order):
1. Added Packages — columns: Package Name, Version, License, Advisories (count). Badge: green.
2. Removed Packages — columns: Package Name, Version, License, Advisories (count). Badge: red.
3. Version Changes — columns: Package Name, Left Version, Right Version, Direction. Badge: blue.
4. New Vulnerabilities — columns: Advisory ID, Severity (SeverityBadge), Title, Affected Package. Badge: red. Rows with severity "Critical" have highlighted background.
5. Resolved Vulnerabilities — columns: Advisory ID, Severity, Title, Previously Affected Package. Badge: green.
6. License Changes — columns: Package Name, Left License, Right License. Badge: yellow.

**Virtualized lists:** For >100 changed packages, use virtualized rendering to prevent browser freezing (per NFR). Consider `react-window` or PatternFly's built-in virtualization.

**Empty state:** When no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**URL-shareable comparison:** Use React Router's `useSearchParams` to read/write `left` and `right` query params. When both params are present on page load, auto-trigger the comparison.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity level display in New/Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` — existing empty state placeholder (evaluate if the comparison empty state can reuse this)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (may use alongside Skeleton)
- `src/hooks/useSboms.ts` — existing hook to fetch SBOM list for the selector dropdowns
- `src/hooks/useSbomComparison.ts` — the hook created in Task 4 for comparison data fetching
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for consistent severity display

## Acceptance Criteria
- [ ] Comparison page renders header toolbar with two SBOM selector dropdowns
- [ ] SBOM selectors fetch and display available SBOMs via `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and displays results
- [ ] Six diff sections render with correct column structures per Figma
- [ ] Each diff section uses `ExpandableSection` with count badge in the correct color
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders in each diff section
- [ ] URL query params `left` and `right` are updated on Compare click
- [ ] Page auto-triggers comparison when both URL params are present on load
- [ ] Export dropdown renders but is disabled (non-MVP)
- [ ] Virtualized rendering activates for diff sections with >100 rows

## Test Requirements
- [ ] Component test: renders empty state when no comparison is active
- [ ] Component test: renders loading skeletons when comparison is in progress
- [ ] Component test: renders all six diff sections with correct data
- [ ] Component test: Compare button is disabled when only one selector has a value
- [ ] Component test: Critical severity rows in New Vulnerabilities have highlighted styling
- [ ] Component test: sections with 0 items are collapsed by default

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison API types, client function, and React Query hook
