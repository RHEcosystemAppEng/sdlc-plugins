# Task 5 — Add SBOM comparison page with header toolbar and diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly Select with typeahead), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results using PatternFly ExpandableSection components with data tables inside. The page supports URL-shareable comparisons via `left` and `right` query parameters, and handles empty state (no comparison yet) and loading state (skeleton placeholders).

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff section layout
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section wrapper (ExpandableSection + Badge + Table)
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — Table for added packages diff section
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — Table for removed packages diff section
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — Table for version changes diff section
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — Table for new vulnerabilities diff section with critical row highlighting
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — Table for resolved vulnerabilities diff section
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — Table for license changes diff section

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- Follow the existing page structure pattern: each page has its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory (see `src/pages/SbomDetailPage/`).
- Use PatternFly 5 components exclusively per project conventions:
  - `Select` (single, typeahead) for SBOM selectors — fetch SBOM list via existing `useSboms` hook (`src/hooks/useSboms.ts`)
  - `ExpandableSection` for each diff category — default expanded when item count > 0
  - `Badge` for count indicators — color varies by section: green (added, resolved), red (removed, new vulns), blue (version changes), yellow (license changes)
  - `Table` (composable) for data display — sortable columns, no pagination
  - `EmptyState` with `CodeBranchIcon` for initial state before comparison
  - `Skeleton` for loading placeholders
  - `Dropdown` for Export button (JSON/CSV options)
- URL-shareable comparison: read `left` and `right` from URL query params on mount using React Router `useSearchParams`. When both are present, auto-trigger the comparison. Update URL params when Compare is clicked.
- Use the `useSbomComparison` hook (Task 4) for data fetching.
- Reuse the existing `SeverityBadge` component (`src/components/SeverityBadge.tsx`) for severity display in vulnerability tables.
- For the NewVulnerabilitiesTable, rows with severity "Critical" should have a highlighted background — use PatternFly's `isHoverable` or custom CSS class for row highlighting.
- Disable the header toolbar during loading state to prevent concurrent requests.
- Export functionality is MVP=No per the feature requirements, but the Export dropdown should be rendered (disabled until comparison result loads). The actual export logic can be a follow-up task.
- For large diffs (>100 changed packages), use virtualized lists per the non-functional requirements. Consider `react-window` or PatternFly's built-in virtualization.

**Data component rendering scope:**
- All six diff tables inside their respective ExpandableSection containers render **per-section** data — each table displays only its own diff category, not aggregated data across categories.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing shared component for severity display in vulnerability tables
- `src/components/EmptyStateCard.tsx` — Existing empty state component (adapt or use as reference for the comparison empty state)
- `src/components/LoadingSpinner.tsx` — Existing loading indicator (consider using Skeleton instead per Figma)
- `src/components/FilterToolbar.tsx` — Existing toolbar pattern for reference on toolbar layout
- `src/hooks/useSboms.ts` — Existing hook for fetching SBOM list (used in SBOM selectors)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Existing package table component for column layout reference
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Existing advisory list component for vulnerability display reference

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Two SBOM selectors allow typeahead search and selection from the SBOM list
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API and renders diff sections
- [ ] Six diff sections render in order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes
- [ ] Each section shows a count badge with the correct color
- [ ] Sections with items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Existing `SeverityBadge` component is used for severity display
- [ ] URL query params `left` and `right` encode SBOM IDs for bookmarkable comparisons
- [ ] Loading URL with both query params auto-triggers the comparison
- [ ] Empty state shows when no comparison has been performed
- [ ] Skeleton placeholders show during API loading
- [ ] Export dropdown is rendered but may be disabled until export logic is implemented

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: Compare button is disabled until both SBOMs are selected
- [ ] Unit test: comparison results render correct number of items per diff section
- [ ] Unit test: Critical vulnerability rows have highlighted styling
- [ ] Unit test: URL query params are read on mount and trigger comparison
- [ ] Unit test: SeverityBadge is rendered for vulnerability severity values

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add frontend API types, client function, and React Query hook for SBOM comparison
