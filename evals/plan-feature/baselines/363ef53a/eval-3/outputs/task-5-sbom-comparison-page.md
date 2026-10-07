## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page at `/sbom/compare` with a header toolbar (dual SBOM selectors, Compare button, Export dropdown) and vertically stacked collapsible diff sections for each change category. The page reads `left` and `right` query parameters from the URL to support shareable comparison links. When no comparison has been performed, an empty state prompts the user to select two SBOMs. Large diffs (>100 changed packages) use virtualized lists to prevent browser freezing.

This task also includes the export functionality: an Export dropdown with "Export JSON" and "Export CSV" options that serialize the fetched comparison result for download.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Component tests
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section with count badge and data table

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage`

## Implementation Notes
Follow the existing page structure pattern: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.

Per the repo's page structure convention: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TypeScript component file scope.

Per the repo's component library convention: all UI components use PatternFly 5 equivalents.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TypeScript/TSX component file scope.

Per the repo's routing convention: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's TypeScript route file scope.

Per the repo's testing convention: Vitest + React Testing Library for unit tests; MSW for API mocking.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's TypeScript test file scope.

**Figma design implementation — Header Toolbar:**
- Left SBOM selector: PatternFly `Select` (single, typeahead) fetching SBOM list via existing `useSboms` hook. Pre-populated from URL query param `left`.
- Right SBOM selector: identical `Select` dropdown. Pre-populated from URL query param `right`.
- "Compare" button: PatternFly primary `Button`, disabled until both selectors have values. Triggers the comparison API call via `useSbomComparison` hook.
- "Export" dropdown: PatternFly `Dropdown` with two items ("Export JSON", "Export CSV"). Disabled until comparison result is loaded.

**Figma design implementation — Diff Sections:**
Each section is a PatternFly `ExpandableSection` with a title, PatternFly `Badge` (count), and a PatternFly composable `Table` inside. Sections are default expanded when item count > 0.

| Section | Badge Color | Table Columns |
|---|---|---|
| Added Packages | green | Package Name, Version, License, Advisories (count) |
| Removed Packages | red | Package Name, Version, License, Advisories (count) |
| Version Changes | blue | Package Name, Left Version, Right Version, Direction |
| New Vulnerabilities | red | Advisory ID, Severity (SeverityBadge), Title, Affected Package |
| Resolved Vulnerabilities | green | Advisory ID, Severity, Title, Previously Affected Package |
| License Changes | yellow | Package Name, Left License, Right License |

- Rows in "New Vulnerabilities" with severity "Critical" must have a highlighted background (use PatternFly table row variant or custom CSS).
- The `SeverityBadge` shared component (in `src/components/SeverityBadge.tsx`) is used for the severity column.

**Figma design implementation — Empty State:**
PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Figma design implementation — Loading State:**
PatternFly `Skeleton` placeholders in each diff section while the comparison API call is in progress. Header toolbar is disabled during loading.

**URL-shareable comparison:**
Read `left` and `right` from URL search params (`useSearchParams`). When the user clicks Compare, update the URL params so the comparison is bookmarkable. When both params are present on page load, auto-trigger the comparison.

**Virtualized lists:**
For diff sections with >100 items, use a virtualized list (e.g., `react-window` or PatternFly's virtualized table) to prevent browser freezing per non-functional requirements.

**Export implementation:**
- Export JSON: `JSON.stringify(comparisonResult, null, 2)` → download as `.json` file
- Export CSV: convert each diff category to CSV rows → download as `.csv` file
- Use `Blob` + `URL.createObjectURL` for client-side download

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity display in the New Vulnerabilities section
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern (adapt for comparison-specific content)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (though Skeleton placeholders are preferred per Figma)
- `src/components/FilterToolbar.tsx` — existing PatternFly toolbar pattern for reference on toolbar layout
- `src/hooks/useSboms.ts` — existing hook for SBOM list used by the SBOM selectors
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — existing page with tabs pattern for reference on page layout
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability highlighting

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selectors fetch and display SBOM list from `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API and renders diff sections
- [ ] All six diff sections render with correct columns, count badges, and badge colors
- [ ] Critical vulnerabilities in "New Vulnerabilities" section have highlighted background
- [ ] Empty state renders when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL query params `left` and `right` are updated when comparison is triggered
- [ ] Page auto-compares when both URL params are present on load (shareable URL)
- [ ] Export JSON downloads the comparison result as a JSON file
- [ ] Export CSV downloads the comparison result as a CSV file
- [ ] Export dropdown is disabled until comparison result is loaded
- [ ] Large diffs (>100 items per section) use virtualized lists

## Test Requirements
- [ ] Component test: renders empty state when no comparison params are set
- [ ] Component test: renders loading state while comparison API is in progress
- [ ] Component test: renders all six diff sections with correct data after successful API response
- [ ] Component test: Compare button is disabled when selectors are empty
- [ ] Component test: Compare button is enabled when both selectors have values
- [ ] Component test: critical vulnerability rows have highlighted styling
- [ ] Component test: URL params are updated after clicking Compare
- [ ] Component test: export buttons are disabled before comparison, enabled after

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types, client function, and hook
