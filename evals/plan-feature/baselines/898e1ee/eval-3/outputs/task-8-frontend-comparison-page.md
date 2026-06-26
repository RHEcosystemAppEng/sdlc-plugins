## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI at `/sbom/compare` based on the Figma design. The page features a header toolbar with two SBOM selectors, a Compare button, and an Export dropdown, followed by vertically stacked collapsible diff sections for each category of change. The page reads SBOM IDs from URL query parameters to support URL-shareable comparisons.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count `Badge` and data `Table`
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — SBOM selector component wrapping PatternFly `Select` (single, typeahead) populated via `useSboms` hook
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` — Export dropdown component using PatternFly `Dropdown` with JSON and CSV export options

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `SbomComparePage`
- `src/App.tsx` — Add lazy import for `SbomComparePage` if routes use lazy loading

## Implementation Notes
Build the UI according to the Figma design specifications from `figma-context.md`.

**Header Toolbar** (per Figma "Header Toolbar" section):
- Two PatternFly `Select` components (single, typeahead variant) for left and right SBOM selection. Each selector fetches the SBOM list via the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display format: "SBOM name vVersion" (e.g., "my-product-sbom v2.3.1"). Pre-populate from URL query params `left` and `right`.
- A primary PatternFly `Button` labeled "Compare", disabled until both selectors have values. On click, update URL query params and trigger the comparison via `useSbomComparison` hook.
- A secondary PatternFly `Dropdown` labeled "Export" with items "Export JSON" and "Export CSV". Disabled until comparison data is loaded.

**Diff Sections** (per Figma "Diff Sections" section):
Use the `DiffSection` component for each category. Each section uses a PatternFly `ExpandableSection` with a title, a count `Badge` (color per Figma spec), and a PatternFly composable `Table` inside. Sections default to expanded when they have >0 items. Section order:
1. **Added Packages** — green `Badge`, columns: Package Name, Version, License, Advisories (count)
2. **Removed Packages** — red `Badge`, columns: Package Name, Version, License, Advisories (count)
3. **Version Changes** — blue `Badge`, columns: Package Name, Left Version, Right Version, Direction
4. **New Vulnerabilities** — red `Badge`, columns: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" get a highlighted background row style.
5. **Resolved Vulnerabilities** — green `Badge`, columns: Advisory ID, Severity, Title, Previously Affected Package
6. **License Changes** — yellow `Badge`, columns: Package Name, Left License, Right License

**Empty State** (per Figma "Empty State" section):
When no comparison has been performed (no query params), render a PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Loading State** (per Figma "Loading State" section):
While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.

**URL Sharing**:
Use React Router's `useSearchParams` to read and update `left` and `right` query params. When the page loads with both params, auto-trigger the comparison.

For large diffs (>100 changed packages in a section), use virtualized lists to prevent browser freezing per the non-functional requirements.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity indicator for vulnerability rows (per Figma component mapping)
- `src/components/EmptyStateCard.tsx` — pattern for empty state (adapt to use `CodeBranchIcon`)
- `src/components/LoadingSpinner.tsx` — loading indicator pattern
- `src/components/FilterToolbar.tsx` — pattern for toolbar layout with PatternFly
- `src/hooks/useSboms.ts` — fetch SBOM list for selectors
- `src/hooks/useSbomComparison.ts` — comparison data hook (from Task 7)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — pattern for PatternFly composable table with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — pattern for rendering advisory data in a table

## Acceptance Criteria
- [ ] Page renders at `/sbom/compare` route
- [ ] Two SBOM selectors populate from the SBOM list API
- [ ] Compare button triggers comparison API call and updates URL query params
- [ ] All six diff sections render with correct columns, count badges, and badge colors per Figma spec
- [ ] Empty state displays when no comparison is active (per Figma empty state spec)
- [ ] Loading state shows Skeleton placeholders during API call (per Figma loading state spec)
- [ ] URL with `left` and `right` query params auto-triggers comparison on page load
- [ ] Critical severity rows in New Vulnerabilities section have highlighted background
- [ ] Export dropdown is present with JSON and CSV options (functional export is non-MVP; dropdown presence is required)
- [ ] `SeverityBadge` component is used for severity display in vulnerability sections

## Test Requirements
- [ ] Unit test: empty state renders when no SBOM IDs are in URL
- [ ] Unit test: selectors populate with SBOM list data
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: diff sections render with correct data after comparison
- [ ] Unit test: critical severity rows have highlighted styling

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run SbomComparePage` — component tests pass
- `npm run build` — production build succeeds

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 7 — Frontend comparison hook

[sdlc-workflow] Description digest: sha256-md:0b4aeaeffd2565b90d8fadfe6d573059f5f01380454e844983486404f365fb99
