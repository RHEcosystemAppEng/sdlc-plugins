# Task 5: Add SbomComparePage with header toolbar and diff sections

**Summary**: Add SbomComparePage with comparison UI from Figma design

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the main SBOM comparison page component following the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly Select with typeahead), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. Each section uses a PatternFly ExpandableSection with a count Badge and a data Table. The page supports URL-shareable comparisons via query parameters and handles empty, loading, and error states.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component (ExpandableSection + Badge + Table)
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — Table for added packages (Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — Table for removed packages (Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — Table for version changes (Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — Table for new vulnerabilities (Advisory ID, Severity, Title, Affected Package) with critical row highlighting
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — Table for resolved vulnerabilities (Advisory ID, Severity, Title, Previously Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — Table for license changes (Name, Left License, Right License)

## Implementation Notes
- **PatternFly component mapping** (from Figma design):
  - SBOM selectors: PatternFly `Select` (single, typeahead variant). Use the existing `useSboms` hook to populate the dropdown options with SBOM name and version (e.g., "my-product-sbom v2.3.1").
  - Diff sections: PatternFly `ExpandableSection`. Default expanded for sections with >0 items, collapsed for sections with 0 items.
  - Count badges: PatternFly `Badge`. Colors by section: green (Added Packages, Resolved Vulnerabilities), red (Removed Packages, New Vulnerabilities), blue (Version Changes), yellow (License Changes).
  - Data tables: PatternFly `Table` (composable variant) with sortable columns. For sections with >100 rows, implement virtualized rendering to prevent browser freezing (use `react-window` or PatternFly's virtualized table pattern).
  - Severity indicators: use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`.
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Loading state: PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading.
  - Export dropdown: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. Export is a client-side download from the already-fetched comparison response (non-MVP but included in the UI per Figma design).
- **URL-shareable comparison**: read `left` and `right` query parameters from the URL on page load using React Router's `useSearchParams`. When the Compare button is clicked, update the URL query parameters so the comparison is bookmarkable. Pre-populate the selectors from URL params if present.
- **Critical vulnerability highlighting**: in the New Vulnerabilities table, rows where `severity` is "critical" should have a highlighted background (use PatternFly's `--pf-v5-global--danger-color--100` or a warning row variant).
- Use the `useSbomComparison` hook from Task 4 for data fetching. The hook is triggered when the Compare button is clicked (or when both URL params are present on load).
- Follow the existing page structure pattern: each page has its own directory under `src/pages/` with a main component and a `components/` subdirectory for page-specific components. Reference `src/pages/SbomDetailPage/` for the pattern.
- Use the existing `EmptyStateCard` from `src/components/EmptyStateCard.tsx` as reference for empty state patterns, but implement the Figma-specific empty state with `CodeBranchIcon`.
- Use the existing `LoadingSpinner` from `src/components/LoadingSpinner.tsx` as reference for loading patterns.

**Backend API contracts:**
- `GET /api/v2/sbom` — existing endpoint, returns SBOM list for selectors. Used via the existing `useSboms` hook.
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — new endpoint, returns `SbomComparisonResult` with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`. (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/hooks/useSboms.ts` — existing hook for SBOM list, used to populate the SBOM selector dropdowns
- `src/components/SeverityBadge.tsx` — existing severity badge component, used in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — existing empty state component, reference for empty state pattern
- `src/components/LoadingSpinner.tsx` — existing loading indicator, reference for loading state pattern
- `src/components/FilterToolbar.tsx` — reusable filter toolbar with PatternFly, reference for toolbar layout patterns
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — existing detail page with tabs, reference for page structure and PatternFly layout
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component, reference for table column definitions and rendering patterns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping, use for sorting vulnerability tables by severity

## Acceptance Criteria
- [ ] SbomComparePage renders with header toolbar containing two SBOM selector dropdowns, a Compare button, and an Export dropdown
- [ ] SBOM selectors are populated with SBOM names and versions from the existing `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API and renders six diff sections with correct data
- [ ] Each diff section uses a PatternFly ExpandableSection with the correct count Badge and color
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] New Vulnerabilities rows with severity "Critical" have a highlighted background
- [ ] Empty state is shown when no comparison has been performed (no URL params)
- [ ] Loading state shows Skeleton placeholders while the API call is in progress
- [ ] URL query parameters (`left` and `right`) are updated when Compare is clicked, making the comparison URL-shareable
- [ ] Page loads with pre-populated selectors and auto-triggers comparison when both URL params are present
- [ ] Large diffs (>100 changed packages) render without browser freezing via virtualized lists
- [ ] Export dropdown is present and disabled until comparison data is loaded

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no query params are present
- [ ] Unit test: SbomComparePage renders comparison results after Compare button click (mock API via MSW)
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Critical vulnerability rows have highlighted styling
- [ ] Unit test: Each diff section shows correct count badge with appropriate color
- [ ] Unit test: Diff sections with 0 items are collapsed by default
- [ ] Unit test: URL search params are updated when Compare is clicked

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison API types and React Query hook
