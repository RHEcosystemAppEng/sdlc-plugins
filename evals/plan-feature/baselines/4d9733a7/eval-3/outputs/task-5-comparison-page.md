## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly Select with typeahead), a Compare button, and vertically stacked collapsible diff sections showing the comparison results. The page supports URL-shareable comparisons via `left` and `right` query parameters. Packages with new critical vulnerabilities are visually highlighted.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- Reusable collapsible diff section component using PatternFly ExpandableSection with count Badge
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` -- Header toolbar with SBOM selectors and Compare button
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` -- Table component for added/removed packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangeTable.tsx` -- Table component for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` -- Table component for new/resolved vulnerabilities (columns: Advisory ID, Severity, Title, Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` -- Table component for license changes (columns: Package Name, Left License, Right License)

## Files to Modify
- `src/routes.tsx` -- Add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)

## Implementation Notes
- **PatternFly component mapping** (from Figma design context):
  - SBOM selectors: PatternFly `Select` (single, typeahead) -- fetch SBOM list using existing `useSboms` hook
  - Diff sections: PatternFly `ExpandableSection` -- default expanded for sections with >0 items
  - Count badges: PatternFly `Badge` -- green for Added/Resolved, red for Removed/New Vulnerabilities, blue for Version Changes, yellow for License Changes
  - Data tables: PatternFly `Table` (composable) -- sortable columns, no pagination (virtualized for >100 rows)
  - Severity indicator: existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon` -- "Select two SBOMs to compare"
  - Loading state: PatternFly `Skeleton` placeholder in each diff section while API call is in progress
- **URL query parameter support**: read `left` and `right` from URL search params on page load to pre-populate selectors. Update URL when selectors change or Compare is clicked, so the comparison URL is shareable/bookmarkable.
- **Critical vulnerability highlighting**: in the New Vulnerabilities table, rows with severity "Critical" should have a highlighted background (use PatternFly danger/warning row variant).
- **Virtualized lists**: for sections with >100 changed items, use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization support.
- **Section ordering** (from Figma): Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
- Follow the page directory structure pattern from existing pages (e.g., `src/pages/SbomDetailPage/`). Each page gets its own directory with a main component and a `components/` subdirectory.
- Per CONVENTIONS.md: use PascalCase for all component file names and component names, camelCase for hooks and utility variables.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TypeScript component scope.
- Per CONVENTIONS.md: all UI components must use PatternFly 5 equivalents.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's React component scope.
- Per CONVENTIONS.md: use React Router v6 for routing with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's route definition scope.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` -- existing SBOM detail page; follow the same page structure with tabs/sections pattern
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- existing package table component; reuse or reference for table column definitions
- `src/components/SeverityBadge.tsx` -- existing shared component for severity display; use directly in vulnerability tables
- `src/components/EmptyStateCard.tsx` -- existing empty state component; reference for empty state pattern (may need custom empty state for comparison)
- `src/components/FilterToolbar.tsx` -- existing filter toolbar; reference for toolbar layout pattern
- `src/components/LoadingSpinner.tsx` -- existing loading indicator; use for initial page load state
- `src/hooks/useSboms.ts` -- existing hook for SBOM list; use to populate SBOM selectors

## Acceptance Criteria
- [ ] Comparison page renders at /sbom/compare route
- [ ] Two SBOM selectors with typeahead allow selecting SBOMs from the full list
- [ ] Compare button triggers the comparison API call and is disabled until both selectors have values
- [ ] All six diff sections render as collapsible sections with correct count badges and color coding
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] New Vulnerabilities table rows with Critical severity have highlighted background
- [ ] URL query parameters `left` and `right` pre-populate selectors on page load
- [ ] Clicking Compare updates the URL with the selected SBOM IDs for shareability
- [ ] Empty state shows "Select two SBOMs to compare" when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders while comparison API call is in progress

## Test Requirements
- [ ] Component test: page renders empty state when no query params are present
- [ ] Component test: selectors populate with SBOM list from useSboms hook
- [ ] Component test: Compare button is disabled when only one SBOM is selected
- [ ] Component test: comparison results render all six diff sections with correct data
- [ ] Component test: Critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] Component test: URL parameters are read on mount and pre-populate selectors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 4 -- Add SBOM comparison API types and data-fetching hook
