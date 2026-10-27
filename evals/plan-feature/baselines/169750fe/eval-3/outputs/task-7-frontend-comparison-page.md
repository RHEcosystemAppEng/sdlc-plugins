## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` based on the Figma design mockups. The page features a header toolbar with two SBOM selector dropdowns, a Compare button, and collapsible diff sections showing added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The URL is shareable via query parameters encoding both SBOM IDs.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — component tests
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section with count badge and data table

## Files to Modify
- `src/routes.tsx` — add route for `/sbom/compare` with lazy-loaded SbomComparePage

## Implementation Notes
Build the page from the Figma design context. The layout is a full-page view with a header toolbar and vertically stacked collapsible diff sections.

**PatternFly component mapping (from Figma):**
- SBOM selectors: PatternFly `Select` (single, typeahead) — pre-populated from URL query params `left` and `right`. Use existing `useSboms` hook to fetch SBOM list.
- Diff sections: PatternFly `ExpandableSection` — default expanded for sections with >0 items. Six sections in order: Added Packages (green badge), Removed Packages (red badge), Version Changes (blue badge), New Vulnerabilities (red badge), Resolved Vulnerabilities (green badge), License Changes (yellow badge).
- Count badges: PatternFly `Badge` with color varying by section.
- Data tables: PatternFly `Table` (composable) with sortable columns. Use virtualized rendering for >100 rows (non-functional requirement).
- Severity indicator: reuse existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`.
- Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- Loading state: PatternFly `Skeleton` placeholders in each diff section while API call is in progress.
- Export button: PatternFly `Dropdown` with "Export JSON" and "Export CSV" items — disabled until comparison result is loaded. (Export is non-MVP; wire the dropdown UI but leave the handler as a placeholder.)

**New Vulnerabilities section:** rows with severity "Critical" have a highlighted background (per Figma design).

**URL sharing:** Read `left` and `right` from URL query params on mount. Update URL query params when comparison is triggered. This makes the comparison URL shareable.

Follow the existing page structure pattern: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory.

Per CONVENTIONS.md §Component Library: all UI components use PatternFly 5 equivalents.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TypeScript React component scope.

Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.

Per CONVENTIONS.md §Naming: PascalCase for components, camelCase for hooks and utilities.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's naming scope.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's TypeScript route file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component for vulnerability severity display
- `src/components/EmptyStateCard.tsx` — existing empty state component (adapt for comparison-specific empty state)
- `src/components/FilterToolbar.tsx` — existing filter toolbar pattern for toolbar layout reference
- `src/components/LoadingSpinner.tsx` — existing loading indicator (use alongside Skeleton placeholders)
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list (for selector dropdowns)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component for column pattern reference

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two PatternFly Select dropdowns load SBOM list from `useSboms` hook
- [ ] Compare button triggers comparison API call via `useSbomComparison` hook
- [ ] Six diff sections render as PatternFly ExpandableSection with correct count badges and colors
- [ ] Data tables within sections display correct columns per Figma specification
- [ ] Critical vulnerabilities have highlighted row background
- [ ] Empty state renders when no comparison has been performed
- [ ] Loading skeleton renders during API call
- [ ] URL query parameters (`left`, `right`) enable shareable comparison URLs
- [ ] Route is registered in `src/routes.tsx` with lazy loading

## Test Requirements
- [ ] Component test: renders empty state when no comparison is loaded
- [ ] Component test: renders diff sections with correct data after comparison
- [ ] Component test: Compare button is disabled until both selectors have values
- [ ] Component test: URL query parameters pre-populate SBOM selectors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Frontend API types and client
