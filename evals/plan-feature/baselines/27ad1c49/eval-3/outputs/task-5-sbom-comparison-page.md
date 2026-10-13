## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page at `/sbom/compare` with a header toolbar containing SBOM selectors, a Compare button, and an Export dropdown, followed by vertically stacked collapsible diff sections for each change category. The page reads left/right SBOM IDs from URL query parameters to support shareable comparison URLs.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and six collapsible diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly ExpandableSection with count Badge and composable Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with left/right SBOM Select dropdowns, Compare button, and Export Dropdown

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to lazy-loaded SbomComparePage

## Implementation Notes
**Figma Design Context** (SBOMCompare / Comparison View):

Header Toolbar:
- Left and right SBOM selectors use PatternFly `Select` (single, typeahead variant) pre-populated from URL query params `left` and `right`. Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate selector options with SBOM name and version (e.g., "my-product-sbom v2.3.1").
- "Compare" button is a PatternFly primary `Button`, disabled until both selectors have values. On click, triggers the comparison via the `useSbomComparison` hook from `src/hooks/useSbomComparison.ts` and updates URL query parameters.
- "Export" uses PatternFly `Dropdown` (secondary variant) with two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded.

Diff Sections (each uses PatternFly `ExpandableSection` with `Badge` count and composable `Table`):
1. **Added Packages** — green `Badge`. Columns: Package Name, Version, License, Advisories (count).
2. **Removed Packages** — red `Badge`. Columns: Package Name, Version, License, Advisories (count).
3. **Version Changes** — blue `Badge`. Columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
4. **New Vulnerabilities** — red `Badge`. Columns: Advisory ID, Severity (render with existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" receive a highlighted background row style.
5. **Resolved Vulnerabilities** — green `Badge`. Columns: Advisory ID, Severity, Title, Previously Affected Package.
6. **License Changes** — yellow `Badge`. Columns: Package Name, Left License, Right License.

Each section defaults to expanded when its item count is greater than 0, collapsed when empty.

Empty State (no comparison performed yet): PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Reuse the pattern from `src/components/EmptyStateCard.tsx`.

Loading State: PatternFly `Skeleton` placeholders within each diff section area. Header toolbar controls disabled during loading.

For sections with more than 100 items, use virtualized list rendering to prevent browser freezing per non-functional requirements.

URL shareability: encode both SBOM IDs as query parameters (`left`, `right`). On page load, if both params are present, auto-trigger the comparison.

Follow page structure convention: page directory under `src/pages/` with main component file and `components/` subdirectory for page-specific components. Route in `src/routes.tsx` uses lazy-loaded import following existing route patterns.

## Reuse Candidates
- `src/hooks/useSboms.ts` — SBOM list for populating selector dropdown options
- `src/hooks/useSbomComparison.ts` — comparison data fetching hook (created in Task 4)
- `src/components/SeverityBadge.tsx` — severity display in New/Resolved Vulnerabilities table rows
- `src/components/EmptyStateCard.tsx` — empty state pattern reference
- `src/components/LoadingSpinner.tsx` — loading state fallback
- `src/utils/severityUtils.ts` — severity ordering and color mapping for vulnerability row highlighting

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Left and right SBOM selectors load options from the SBOM list endpoint via useSboms
- [ ] Compare button triggers comparison API call when both SBOMs are selected
- [ ] All six diff sections render with correct column definitions and colored count badges
- [ ] Rows with critical-severity new vulnerabilities are visually highlighted
- [ ] Empty state shown when page loads without query parameters or selections
- [ ] Loading skeleton placeholders shown while comparison API call is in progress
- [ ] URL query parameters encode both SBOM IDs so the comparison is shareable/bookmarkable
- [ ] Export dropdown offers JSON and CSV options (disabled until comparison loaded)

## Test Requirements
- [ ] Unit test: page renders empty state when no SBOMs are selected
- [ ] Unit test: page renders all six diff sections with mock comparison data
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: critical-severity vulnerability rows receive highlighted styling
