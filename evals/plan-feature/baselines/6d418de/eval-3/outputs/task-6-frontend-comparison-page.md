# Task 6 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the main SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selectors, a Compare button, and an Export dropdown, plus six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). Each section uses a PatternFly `ExpandableSection` with a count `Badge` and a sortable data `Table`. The page supports URL-shareable comparisons via `left` and `right` query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections layout
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for comparison page
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors (PatternFly `Select` with typeahead), Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section wrapper using PatternFly `ExpandableSection` with count `Badge`
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — Table for added packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — Table for removed packages (same columns as added)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — Table for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — Table for new vulnerabilities (columns: Advisory ID, Severity, Title, Affected Package) with critical severity row highlighting
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — Table for resolved vulnerabilities (columns: Advisory ID, Severity, Title, Previously Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — Table for license changes (columns: Package Name, Left License, Right License)

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- **PatternFly components to use**: `Select` (single, typeahead) for SBOM selectors, `ExpandableSection` for diff sections, `Badge` for count badges, `Table` (composable) for data tables, `EmptyState` for initial state, `Skeleton` for loading state, `Dropdown` for Export button, `CodeBranchIcon` for empty state icon.
- **SBOM selectors**: use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the dropdown options. Display SBOM name and version (e.g., "my-product-sbom v2.3.1").
- **URL query params**: read `left` and `right` from URL search params using React Router's `useSearchParams`. Pre-populate selectors from URL params on page load. Update URL params when the user clicks Compare, enabling URL-shareable comparisons.
- **Compare button**: disabled until both selectors have values. On click, update URL search params and trigger the `useSbomComparison` hook.
- **Diff section behavior**: sections with >0 items default to expanded; sections with 0 items default to collapsed. Count badge colors: green for Added Packages, red for Removed Packages, blue for Version Changes, red for New Vulnerabilities, green for Resolved Vulnerabilities, yellow for License Changes.
- **Critical vulnerability highlighting**: rows in New Vulnerabilities where severity is "critical" should have a highlighted/warning background. Use PatternFly's `isRowSelected` or custom row styling.
- **Existing SeverityBadge component**: use `src/components/SeverityBadge.tsx` for severity display in vulnerability tables. Do not create a new severity component.
- **Large diff handling**: the NFR specifies virtualized lists for >100 changed packages. Use `react-window` or PatternFly's built-in virtualization for tables exceeding 100 rows.
- **Empty state**: when no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: while comparison API call is in progress, show `Skeleton` placeholders in each diff section and disable the header toolbar.
- **Export dropdown** (non-MVP): include the dropdown with "Export JSON" and "Export CSV" options. Disable until comparison result is loaded. For MVP, the export functionality can be implemented as a follow-up — wire up the dropdown UI but the actual export logic is optional.
- **Route placement**: add the `/sbom/compare` route in `src/routes.tsx` before `/sbom/:id` to prevent the route matcher from treating "compare" as an ID parameter.

**Data component rendering scope:**
- All six diff section tables render data from the single `SbomComparisonResult` response. Each table receives its specific array prop (e.g., `AddedPackagesTable` receives `data.added_packages`). No per-context filtering is needed — the data is already segmented by the backend.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity display in vulnerability tables
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar patterns (though the comparison toolbar is custom)
- `src/components/EmptyStateCard.tsx` — reference for empty state pattern (may need adaptation for the comparison-specific empty state)
- `src/components/LoadingSpinner.tsx` — reference for loading state patterns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly table patterns with sortable columns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for advisory data display patterns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability tables
- `src/hooks/useSboms.ts` — existing hook for populating SBOM selector dropdowns

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selectors populated from existing SBOM list
- [ ] Compare button triggers API call and renders diff sections
- [ ] URL encodes both SBOM IDs for shareability (bookmarkable URLs)
- [ ] Page loads comparison directly when `left` and `right` query params are present in URL
- [ ] Six collapsible diff sections render with correct data and count badges
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] Badge colors match Figma: green (added), red (removed), blue (version changes), red (new vulns), green (resolved vulns), yellow (license changes)
- [ ] Critical severity vulnerabilities have highlighted row background
- [ ] Empty state displays when no comparison is active
- [ ] Loading skeletons display during API call
- [ ] Existing `SeverityBadge` component is used for vulnerability severity display
- [ ] Export dropdown is present and disabled until comparison loads

## Test Requirements
- [ ] Unit test: renders empty state when no query params present
- [ ] Unit test: renders diff sections with correct data after comparison API returns
- [ ] Unit test: Compare button is disabled when fewer than two SBOMs are selected
- [ ] Unit test: URL params are updated on Compare click
- [ ] Unit test: pre-populates selectors from URL query params
- [ ] Unit test: critical severity rows receive highlighted styling
- [ ] Unit test: sections with zero items are collapsed by default

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add frontend API types, client function, and React Query hook for SBOM comparison
