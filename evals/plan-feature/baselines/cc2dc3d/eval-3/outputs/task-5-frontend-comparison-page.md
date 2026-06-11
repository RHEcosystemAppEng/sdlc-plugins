## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page at `/sbom/compare` with the full UI as specified in the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown, followed by six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). Each section uses PatternFly `ExpandableSection` with a count `Badge` and a sortable `Table`. The page supports URL-shareable comparisons via `left` and `right` query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping ExpandableSection + Badge + Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection for SBOMs and a "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- **Page structure:** Follow the existing page pattern — each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory (see `src/pages/SbomDetailPage/` for the established pattern).
- **PatternFly components from Figma design:**
  - SBOM selectors: PatternFly `Select` (single, typeahead variant) — fetches SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`
  - Diff sections: PatternFly `ExpandableSection` — default expanded for sections with >0 items
  - Count badges: PatternFly `Badge` — green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes
  - Data tables: PatternFly `Table` (composable) — sortable columns, no pagination; implement virtualized rendering for >100 rows per the non-functional requirement
  - Severity indicators: Reuse existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Export button: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV"
  - Loading state: PatternFly `Skeleton` placeholders in each diff section while API call is in progress; toolbar disabled during loading
- **URL-shareable comparison:** Read `left` and `right` query parameters from the URL using React Router `useSearchParams`. When both are present on page load, auto-populate the selectors and trigger the comparison. When the user clicks Compare, update the URL query parameters using `setSearchParams`.
- **New Vulnerabilities section:** Rows with severity "Critical" must have a highlighted background row style.
- **Table columns per section (from Figma):**
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- **Export functionality:** Export is non-MVP but included in the UI. Implement JSON export by serializing the comparison result. CSV export can format each section as a CSV block. Disable the Export dropdown until a comparison result is loaded.
- **SbomListPage integration:** Add a checkbox column to the existing SBOM table and a toolbar action button "Compare selected" that is enabled when exactly two SBOMs are checked. On click, navigate to `/sbom/compare?left={id1}&right={id2}`.
- **Routing:** Add the route in `src/routes.tsx` following the existing lazy-loading pattern (see how `SbomDetailPage` and `SbomListPage` are registered).

**Data component rendering scope:**
- All six diff section tables render data from the single comparison API response — each table displays its corresponding array from `SbomComparisonResult` (e.g., the Added Packages table renders `result.added_packages`). This is a flat rendering scope, not per-context.

**Reuse Candidates:**
- `src/components/SeverityBadge.tsx` — reuse for severity display in New/Resolved Vulnerabilities tables
- `src/components/FilterToolbar.tsx` — consider for future filtering within diff sections
- `src/components/EmptyStateCard.tsx` — reuse or follow the pattern for the empty state when no comparison is loaded
- `src/components/LoadingSpinner.tsx` — reuse for loading states
- `src/hooks/useSboms.ts` — reuse for populating SBOM selector dropdowns
- `src/utils/severityUtils.ts` — reuse for severity level ordering and color mapping in vulnerability tables

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with two SBOM selector dropdowns and a Compare button
- [ ] Clicking Compare with both selectors populated calls the comparison API and renders six diff sections
- [ ] Each diff section is a collapsible ExpandableSection with a count Badge and a sortable Table
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Badge colors match the Figma spec: green (Added, Resolved), red (Removed, New Vulns), blue (Version Changes), yellow (License Changes)
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] URL query parameters (`left`, `right`) are updated when Compare is clicked, enabling URL sharing
- [ ] Page loads with pre-populated selectors and auto-triggered comparison when URL has both query params
- [ ] Empty state is shown when no comparison has been performed
- [ ] Loading skeletons are displayed while the API call is in progress
- [ ] Export dropdown is present with JSON and CSV options, disabled until comparison is loaded
- [ ] SbomListPage has checkbox selection and a "Compare selected" button that navigates to the comparison page
- [ ] Large diffs (>100 changed packages per section) render without browser freezing (virtualized lists)

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no query params are present
- [ ] Unit test: SbomComparePage renders diff sections after comparison API returns data
- [ ] Unit test: each diff section displays correct columns and data
- [ ] Unit test: Critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] Unit test: Compare button is disabled until both selectors have values
- [ ] Unit test: URL query params are updated when Compare is clicked
- [ ] Unit test: SbomListPage Compare button is enabled only when exactly two SBOMs are selected
- [ ] Use MSW handlers in `tests/mocks/handlers.ts` to mock the comparison endpoint
- [ ] Add mock comparison data fixture to `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
