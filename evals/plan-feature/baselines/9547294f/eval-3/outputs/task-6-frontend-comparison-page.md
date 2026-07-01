# Task 6 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the main SBOM comparison page at `/sbom/compare` with a header toolbar (SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections based on the Figma design. This is the primary user-facing component for the SBOM comparison feature, allowing users to visually compare two SBOM versions side-by-side.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component using PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM Select dropdowns, Compare button, and Export Dropdown

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to lazy-loaded SbomComparePage
- `src/App.tsx` — Add route entry for the comparison page (if routes are registered here in addition to routes.tsx)

## Implementation Notes

### Figma design mapping

The page layout follows the Figma design context. Key PatternFly component mappings:

| Figma Element | PatternFly Component | Implementation Notes |
|---|---|---|
| SBOM selector | `Select` (single, typeahead) | Fetches SBOM list via existing `useSboms` hook. Pre-populate from URL query params `left` and `right`. |
| Compare button | `Button` (primary) | Disabled until both selectors have values. Triggers the comparison API call. |
| Export dropdown | `Dropdown` | Two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded. |
| Diff section | `ExpandableSection` | Default expanded for sections with >0 items. Title includes section name and count Badge. |
| Count badge | `Badge` | Color varies: green for Added/Resolved, red for Removed/New Vulnerabilities, blue for Version Changes, yellow for License Changes. |
| Data table | `Table` (composable) | Sortable columns. Use virtualized rendering for >100 rows (react-window or PatternFly virtual scroll). |
| Severity indicator | `SeverityBadge` | Reuse existing `src/components/SeverityBadge.tsx` component. |
| Empty state | `EmptyState` | Show when no comparison has been performed (no query params). Use `CodeBranchIcon`. Title: "Select two SBOMs to compare". |
| Loading state | `Skeleton` | PatternFly Skeleton in each diff section while API call is in progress. Header toolbar disabled during loading. |

### Diff section table columns (from Figma)

1. **Added Packages**: Package Name, Version, License, Advisories (count) — green badge
2. **Removed Packages**: Package Name, Version, License, Advisories (count) — red badge
3. **Version Changes**: Package Name, Left Version, Right Version, Direction (upgrade/downgrade) — blue badge
4. **New Vulnerabilities**: Advisory ID, Severity (SeverityBadge), Title, Affected Package — red badge. Rows with severity "Critical" have highlighted background.
5. **Resolved Vulnerabilities**: Advisory ID, Severity, Title, Previously Affected Package — green badge
6. **License Changes**: Package Name, Left License, Right License — yellow badge

### URL-shareable comparison

The comparison must be URL-shareable. Use React Router's `useSearchParams` to read and write `left` and `right` query parameters. When both params are present on page load, auto-trigger the comparison.

### Performance

Use virtualized lists (e.g., react-window) for diff sections with >100 items to prevent browser freezing per the NFR. The DiffSection component should detect row count and conditionally apply virtualization.

### Data component rendering scope

- All six diff section tables render **per-comparison** data — each table displays only the diff results from the current comparison, not aggregated data from multiple comparisons.

### Backend API contracts

- `GET /api/v2/sbom/compare?left={id}&right={id}` — response shape: `SbomComparisonResult` (see Task 5 for TypeScript interfaces, see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- `GET /api/v2/sbom` — existing endpoint for SBOM list in selectors (use existing `useSboms` hook)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

### Reuse candidates

- `src/components/SeverityBadge.tsx` — existing shared component for severity level display in New/Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — existing empty state component (adapt for comparison-specific empty state)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (may use alongside Skeleton)
- `src/components/FilterToolbar.tsx` — existing toolbar pattern for reference on toolbar layout
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list for the selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table for reference on table structure and column definitions
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list for reference on advisory display patterns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping utilities

Per CONVENTIONS.md: all UI components use PatternFly 5 equivalents; each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TypeScript page component scope.

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] SBOM selectors load the SBOM list and support typeahead search
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] Clicking Compare triggers the API call and renders six diff sections
- [ ] Each diff section uses PatternFly ExpandableSection with correct count Badge color
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders while API call is in progress
- [ ] URL query params `left` and `right` are updated when a comparison is triggered
- [ ] Page load with both query params auto-triggers the comparison
- [ ] Export dropdown is disabled until comparison result is loaded
- [ ] Virtualized rendering is used for diff sections with >100 rows

## Test Requirements
- [ ] Unit test: empty state renders when no comparison is active
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: diff sections render with correct data from mocked API response
- [ ] Unit test: New Vulnerabilities rows with Critical severity have highlighted styling
- [ ] Unit test: sections with zero items are collapsed by default

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add API types and client function for SBOM comparison

---
Priority: Critical
Fix Versions: RHTPA 1.5.0
Labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:f8c2e6d0a5b1794c3f9a0d6e8b2c4f7a1d5e9b3f6c8a0d2e4b7f9a1c3d5e8b0a
