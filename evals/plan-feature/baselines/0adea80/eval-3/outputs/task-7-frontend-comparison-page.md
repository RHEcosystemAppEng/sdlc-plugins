# Task 7 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` per the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page supports URL-shareable comparisons via `left` and `right` query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and diff section rendering
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component using PatternFly `ExpandableSection` with count `Badge` and data `Table`
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — Table for added packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — Table for removed packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — Table for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — Table for new vulnerabilities (columns: Advisory ID, Severity via SeverityBadge, Title, Affected Package); rows with Critical severity get highlighted background
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — Table for resolved vulnerabilities (columns: Advisory ID, Severity, Title, Previously Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — Table for license changes (columns: Package Name, Left License, Right License)

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)
- `src/App.tsx` — Verify router setup includes the new route (likely no change needed if routes.tsx is auto-consumed)

## Implementation Notes
- **PatternFly components**: Use `Select` (single, typeahead) for SBOM selectors, `ExpandableSection` for diff sections, `Badge` for count badges, `Table` (composable) for data tables, `EmptyState` with `CodeBranchIcon` for the initial empty state, `Skeleton` for loading states, `Dropdown` for the Export button.
- **SBOM selectors**: Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the selector dropdowns. Display SBOM name and version (e.g., "my-product-sbom v2.3.1").
- **URL-shareable state**: Read `left` and `right` from URL search params on mount. When the user clicks Compare, update the URL search params using React Router's `useSearchParams`. Pre-populate selectors from URL params.
- **Diff section ordering**: Added Packages (green badge), Removed Packages (red badge), Version Changes (blue badge), New Vulnerabilities (red badge), Resolved Vulnerabilities (green badge), License Changes (yellow badge).
- **Section expand behavior**: Sections with >0 items default to expanded; sections with 0 items default to collapsed.
- **Critical vulnerability highlighting**: In `NewVulnerabilitiesTable`, rows where severity is "critical" should have a highlighted/warning background row style.
- **Virtualized lists**: For sections with >100 rows, implement virtualized rendering to prevent browser freezing. Consider using `react-window` or PatternFly's built-in table virtualization.
- **Loading state**: While comparison API call is in progress, show `Skeleton` placeholders in each diff section area and disable the header toolbar controls.
- **Empty state**: When no comparison has been performed (no query params, page first load), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Export dropdown**: Secondary button with "Export JSON" and "Export CSV" options. Disabled until comparison result is loaded. Export functionality is non-MVP but include the disabled dropdown UI.
- Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` for vulnerability severity display.
- Follow the existing page structure pattern in `src/pages/SbomListPage/SbomListPage.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.tsx` for component organization.
- Follow React Router v6 lazy-loading pattern in `src/routes.tsx` matching existing route definitions.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing shared component for severity level display; use in vulnerability tables
- `src/components/EmptyStateCard.tsx` — Existing empty state component; reference pattern for the comparison empty state
- `src/components/LoadingSpinner.tsx` — Existing loading indicator; may be used alongside Skeleton placeholders
- `src/components/FilterToolbar.tsx` — Existing filter toolbar pattern; reference for toolbar layout
- `src/hooks/useSboms.ts` — Existing hook for fetching SBOM list; use for selector dropdowns
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing page pattern with table and filters
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — Existing detail page with tabs; reference for page structure
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Existing package table component; reference for table column patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Existing advisory list component; reference for advisory display pattern
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping; use for critical vulnerability highlighting

## Acceptance Criteria
- [ ] Page renders at `/sbom/compare` with SBOM selectors and Compare button
- [ ] Both SBOM selectors are populated from the SBOM list API
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API and renders six diff sections
- [ ] URL is updated with `left` and `right` query params when Compare is clicked
- [ ] Page loads comparison directly when URL contains `left` and `right` params (URL-shareable)
- [ ] Each diff section shows correct count badge with appropriate color
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] Critical vulnerabilities are visually highlighted in the New Vulnerabilities section
- [ ] Empty state is shown when no comparison has been performed
- [ ] Loading skeletons are shown while the comparison API call is in progress
- [ ] Export dropdown is present but disabled when no comparison is loaded

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: selectors populate with SBOM list data
- [ ] Unit test: Compare button enables when both selectors have values
- [ ] Unit test: clicking Compare triggers API call and renders diff sections
- [ ] Unit test: URL params pre-populate selectors and trigger comparison on mount
- [ ] Unit test: critical vulnerability rows are highlighted
- [ ] Unit test: sections with zero items are collapsed by default

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add frontend API types, client function, and React Query hook for SBOM comparison
