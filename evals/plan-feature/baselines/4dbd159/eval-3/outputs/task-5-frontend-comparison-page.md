# Task 5 — Add SBOM comparison page with diff sections and route

## Repository
trustify-ui

## Target Branch
main

## Description
Add the SBOM comparison page at `/sbom/compare` with a header toolbar containing two SBOM selectors, a Compare button, and an Export dropdown, followed by six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). The page reads `left` and `right` query parameters from the URL for shareable comparisons. The UI follows the Figma design specification and uses PatternFly components throughout.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare`
- `tests/mocks/fixtures/sboms.json` — Add mock comparison response data (or create a separate `comparison.json` fixture)

## Implementation Notes
- **Figma design mapping to PatternFly components:**
  - SBOM selectors: PatternFly `Select` (single, typeahead) — fetch SBOM list via existing `useSboms` hook
  - Diff sections: PatternFly `ExpandableSection` — default expanded for sections with >0 items
  - Count badges: PatternFly `Badge` — colors: green (added/resolved), red (removed/new vulns), blue (version changes), yellow (license changes)
  - Data tables: PatternFly `Table` (composable) — sortable columns
  - Severity indicator: existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Export button: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV"
  - Loading state: PatternFly `Skeleton` in each diff section while API call is in progress

- **URL-shareable comparison:** Use React Router `useSearchParams` to read `left` and `right` query parameters. Pre-populate the selectors from URL params. Update URL params when the user clicks Compare, using `setSearchParams` for history push.

- **Diff section configuration:** Define each section's config (title, badge color, table columns, data key) in an array to avoid duplicating the ExpandableSection+Table pattern six times. The `DiffSection` component should accept these props generically.

- **Diff section details per Figma:**
  1. Added Packages — green badge — columns: Package Name, Version, License, Advisories (count)
  2. Removed Packages — red badge — columns: Package Name, Version, License, Advisories (count)
  3. Version Changes — blue badge — columns: Package Name, Left Version, Right Version, Direction
  4. New Vulnerabilities — red badge — columns: Advisory ID, Severity (SeverityBadge), Title, Affected Package — rows with "Critical" severity get highlighted background
  5. Resolved Vulnerabilities — green badge — columns: Advisory ID, Severity, Title, Previously Affected Package
  6. License Changes — yellow badge — columns: Package Name, Left License, Right License

- **Virtualized lists:** For diff sections with >100 rows, use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization if available.

- **Export functionality (non-MVP):** The Export dropdown can be implemented as disabled/placeholder in this task. The actual export logic is a non-MVP requirement that can be addressed later.

- **Critical vulnerability highlighting:** In the New Vulnerabilities section, rows where `severity === "critical"` should have a highlighted/warning background. Use PatternFly table row variant or custom CSS class.

- Follow the existing page structure pattern: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory per `src/pages/SbomDetailPage/`.

- Use React Router v6 lazy-loaded routes per the convention in `src/routes.tsx`.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Reuse directly for severity display in vulnerability sections
- `src/components/EmptyStateCard.tsx` — Reference for empty state pattern (though this page uses a custom empty state)
- `src/components/LoadingSpinner.tsx` — Reference for loading state pattern
- `src/hooks/useSboms.ts` — Reuse for populating the SBOM selector dropdowns
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — Follow page structure pattern (directory layout, component organization)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Reference for PatternFly Table usage with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Reference for advisory list rendering pattern
- `src/utils/severityUtils.ts` — Reuse severity ordering and color mapping for critical vulnerability highlighting

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and loads the comparison page
- [ ] Header toolbar displays two SBOM selector dropdowns, a Compare button (disabled until both selected), and an Export dropdown
- [ ] SBOM selectors are populated from the existing SBOM list API
- [ ] Clicking Compare calls the comparison API and renders six diff sections
- [ ] Each diff section uses a collapsible PatternFly ExpandableSection with the correct count badge color
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] Data tables in each section display the correct columns per Figma design
- [ ] New Vulnerabilities section uses `SeverityBadge` and highlights Critical rows
- [ ] Empty state is shown when no comparison has been performed (no URL params)
- [ ] Skeleton loading state is shown during API call
- [ ] URL query parameters `left` and `right` are read on page load and updated on Compare
- [ ] URL is shareable — opening a URL with `left` and `right` params triggers the comparison automatically

## Test Requirements
- [ ] Unit test: page renders empty state when no SBOM IDs are provided
- [ ] Unit test: page renders comparison results when API returns data (using MSW mock)
- [ ] Unit test: each diff section renders correct number of rows from mock data
- [ ] Unit test: Compare button is disabled when fewer than two SBOMs are selected
- [ ] Unit test: Critical vulnerability rows have highlighted styling
- [ ] Unit test: URL search params are updated when Compare is clicked

## Dependencies
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
