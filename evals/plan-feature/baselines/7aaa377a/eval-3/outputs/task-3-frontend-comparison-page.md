# Task 3 — Build SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
main

## Description
Create the SBOM comparison page at `/sbom/compare` that displays a structured diff between two SBOMs. The page includes a header toolbar with SBOM selectors and a Compare button, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), an empty state for initial page load, and loading skeletons during API calls. The page supports URL-shareable comparisons via `left` and `right` query parameters.

This is the primary UI for the SBOM comparison feature (TC-9003), built from the Figma design mockups.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to the new SbomComparePage component (lazy-loaded)

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component using PatternFly ExpandableSection with count Badge
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — table for added packages (name, version, license, advisory count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — table for removed packages (name, version, license, advisory count)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — table for version changes (name, left version, right version, direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — table for new vulnerabilities with SeverityBadge and critical row highlighting
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — table for resolved vulnerabilities with SeverityBadge
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — table for license changes (name, left license, right license)
- `tests/mocks/handlers.ts` — add MSW handler for `GET /api/v2/sbom/compare` (modify existing file)
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response data

## Implementation Notes
- **SBOM selectors:** use PatternFly `Select` component (single, typeahead variant) for both left and right SBOM selectors. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in each option (e.g., "my-product-sbom v2.3.1"). Pre-populate selections from URL query params `left` and `right`.
- **Compare button:** PatternFly primary Button, disabled until both selectors have values. On click, update URL query params and trigger the `useSbomComparison` hook from Task 2.
- **Export dropdown:** PatternFly `Dropdown` (secondary variant) with two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded. Export implementation is handled in Task 5.
- **Diff sections:** each section is a PatternFly `ExpandableSection` with a title, PatternFly `Badge` showing the count of items, and a data table inside. Sections default to expanded when they have >0 items. Section order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
- **Count badge colors:** Added Packages = green, Removed Packages = red, Version Changes = blue, New Vulnerabilities = red, Resolved Vulnerabilities = green, License Changes = yellow. Use PatternFly Badge variant or custom CSS to apply colors.
- **New Vulnerabilities critical highlighting:** rows with severity "Critical" should have a highlighted background (use PatternFly table row variant or custom CSS class).
- **Severity display:** use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` in the New Vulnerabilities and Resolved Vulnerabilities tables.
- **Empty state:** when no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon` (from PatternFly icons), title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Follow the pattern in `src/components/EmptyStateCard.tsx`.
- **Loading state:** while the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading.
- **URL-shareable:** the page reads `left` and `right` query parameters on load and pre-populates the selectors. When a comparison is triggered, update the URL query params so the comparison can be bookmarked and shared.
- **Virtualized lists:** for sections with >100 items, use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's virtualized table variant.
- **Routing:** add the route as a lazy-loaded component in `src/routes.tsx` following the existing pattern (React Router v6 lazy loading).
- Use PatternFly `Table` (composable variant) with sortable columns for all data tables, following the pattern in `src/pages/SbomDetailPage/components/PackageTable.tsx`.

## Reuse Candidates
- `src/hooks/useSboms.ts` — existing hook for fetching the SBOM list; use to populate both SBOM selector dropdowns
- `src/components/SeverityBadge.tsx` — existing shared component for displaying severity levels (Critical/High/Medium/Low); use in vulnerability tables
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern; follow for the comparison page empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; use for loading states
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reuse or follow its column structure pattern for Added/Removed package tables
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component; follow its pattern for vulnerability display
- `src/utils/severityUtils.ts` — existing severity level ordering and color mapping utilities; use for sorting vulnerabilities by severity

## Acceptance Criteria
- [ ] `/sbom/compare` route exists and renders the SbomComparePage
- [ ] Header toolbar displays two SBOM selector dropdowns populated with available SBOMs
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and displays results
- [ ] Six collapsible diff sections display with correct titles, count badges, and data tables
- [ ] Count badges use correct colors: green (added/resolved), red (removed/new vulns), blue (version changes), yellow (license changes)
- [ ] Diff sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities table rows with severity "Critical" have highlighted background
- [ ] SeverityBadge component is used for severity display in vulnerability tables
- [ ] Empty state displays when no comparison query params are present
- [ ] Loading skeletons display during API call
- [ ] URL query params `left` and `right` are read on page load and pre-populate selectors
- [ ] URL is updated when a comparison is triggered, making the comparison URL-shareable
- [ ] Tables support sortable columns

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no query params are provided
- [ ] Unit test: SbomComparePage pre-populates selectors from URL query params
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: comparison results render correctly with all six diff sections
- [ ] Unit test: diff sections show correct count in Badge components
- [ ] Unit test: New Vulnerabilities table highlights Critical severity rows
- [ ] Unit test: loading state shows Skeleton components during API call
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add mock comparison fixture data in `tests/mocks/fixtures/sbom-comparison.json`

## Dependencies
- Depends on: Task 2 — Add comparison API types, client function, and React Query hook
