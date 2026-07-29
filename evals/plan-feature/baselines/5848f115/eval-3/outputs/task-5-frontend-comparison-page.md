## Repository
trustify-ui

## Target Branch
main

## Description
Build the SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with SBOM selectors, a Compare button, and an Export dropdown (disabled placeholder for non-MVP), plus six collapsible diff sections rendered from the comparison API response. The page supports URL-shareable comparisons via query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable expandable diff section component with count badge and data table

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)

## Implementation Notes
- Follow the existing page structure pattern: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory (see `src/pages/SbomDetailPage/` for reference).
- Use PatternFly 5 components exclusively per project convention:
  - `Select` (single, typeahead) for SBOM selectors — fetch SBOM list via existing `useSboms` hook
  - `ExpandableSection` for each diff section — default expanded for sections with >0 items
  - `Badge` for count badges — color per section: green (Added, Resolved), red (Removed, New Vulns), blue (Version Changes), yellow (License Changes)
  - `Table` (composable) for data tables within each section — sortable columns
  - `EmptyState` with `CodeBranchIcon` for the initial empty state before comparison
  - `Dropdown` for Export button — items "Export JSON" and "Export CSV", disabled until comparison is loaded (placeholder for non-MVP)
  - `Skeleton` for loading state in each diff section
- **URL-shareable comparisons**: read `left` and `right` query params from the URL on page load. If both are present, pre-populate the selectors and trigger the comparison automatically. When the user clicks Compare, update the URL query params using React Router's `useSearchParams` so the URL is always shareable.
- **Diff section ordering** (per Figma): Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
- **Table columns per section** (per Figma):
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction
  - New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- **Critical vulnerability highlighting**: Rows in the New Vulnerabilities section with severity "Critical" must have a highlighted background (use PatternFly danger variant or a custom `--pf-v5-global--danger-color--100` background).
- **Virtualized lists**: For sections with >100 items, implement virtualized rendering to prevent browser freezing (per NFR). Consider using `react-window` or PatternFly's built-in virtualization.
- **Loading state**: While the comparison API call is in progress, show Skeleton placeholders in each diff section and disable the header toolbar.
- **Existing shared component**: Use `SeverityBadge` from `src/components/SeverityBadge.tsx` for severity display in vulnerability sections.
- **Route registration**: Add the route in `src/routes.tsx` using lazy loading per the existing pattern. Place the `/sbom/compare` route BEFORE any `/sbom/:id` route to avoid path conflicts.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — demonstrates the page structure with tabs and sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — demonstrates the PatternFly Table pattern for package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — demonstrates advisory list rendering
- `src/components/SeverityBadge.tsx` — existing shared component for severity display (reuse directly)
- `src/components/EmptyStateCard.tsx` — existing empty state component (may serve as reference for the comparison empty state)
- `src/components/FilterToolbar.tsx` — reusable filter toolbar pattern with PatternFly
- `src/components/LoadingSpinner.tsx` — existing loading indicator
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list (used in selectors)
- `src/utils/severityUtils.ts` — severity level ordering and color mapping utilities

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Both SBOM selectors load the SBOM list via useSboms hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API and renders diff sections
- [ ] Each diff section shows as an ExpandableSection with correct count badge color
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Empty state shows when no comparison has been performed (CodeBranchIcon, "Select two SBOMs to compare")
- [ ] Loading state shows Skeleton placeholders and disables toolbar during API call
- [ ] URL query params (left, right) are updated on Compare and read on page load for shareability
- [ ] Export dropdown is present but disabled (non-MVP placeholder)
- [ ] Page handles large diffs (>100 items per section) without browser freezing

## Test Requirements
- [ ] Unit test: renders empty state when no comparison is loaded
- [ ] Unit test: renders comparison results with all six diff sections
- [ ] Unit test: Compare button disabled when selectors are empty
- [ ] Unit test: Critical severity rows have highlighted styling
- [ ] Unit test: URL query params pre-populate selectors and trigger comparison
- [ ] Unit test: loading state shows Skeleton placeholders
- [ ] E2E test: full comparison workflow — select two SBOMs, click Compare, verify diff sections render

## Verification Commands
- `npm run build` — TypeScript compiles without errors
- `npm run test` — all unit tests pass
- `npx playwright test sbom-compare` — E2E tests pass

## Dependencies
- Depends on: Task 4 — Frontend API and hooks (useSbomComparison hook must exist)
