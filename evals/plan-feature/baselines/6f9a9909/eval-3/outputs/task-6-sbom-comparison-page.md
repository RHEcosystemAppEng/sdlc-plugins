## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page at `/sbom/compare` with a header toolbar for SBOM selection and vertically stacked collapsible diff sections. The page reads `left` and `right` SBOM IDs from URL query parameters to support URL-shareable comparisons. This is the primary user-facing component for the comparison feature.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to `SbomComparePage`

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping ExpandableSection and Table
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — table component for added/removed packages and version changes
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — table component for new/resolved vulnerabilities
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` — table component for license changes

## Implementation Notes
**Figma design reference (from SBOMCompare mock123, page: Comparison View):**

**Header Toolbar (CompareToolbar.tsx):**
- Left SBOM selector: PatternFly `Select` (single, typeahead) showing SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populate from URL query param `left`. Fetch SBOM list via existing `useSboms` hook.
- Right SBOM selector: identical PatternFly `Select` (single, typeahead) for second SBOM. Pre-populate from URL query param `right`.
- "Compare" button: PatternFly primary `Button`, disabled until both selectors have values. Triggers the diff API call via `useSbomComparison` hook.
- "Export" dropdown: PatternFly `Dropdown` (secondary) with options "Export JSON" and "Export CSV". Disabled until comparison result is loaded. For MVP, render as disabled with tooltip "Coming soon" (export is non-MVP).

**Diff Sections (DiffSection.tsx wrapping each category):**
Each section uses PatternFly `ExpandableSection` with a title, PatternFly `Badge` count, and a composable `Table` inside. Default expanded for sections with >0 items. Sections appear in this order:

1. **Added Packages** — PatternFly `Badge` in green. Table columns: Package Name, Version, License, Advisories (count).
2. **Removed Packages** — PatternFly `Badge` in red. Table columns: Package Name, Version, License, Advisories (count).
3. **Version Changes** — PatternFly `Badge` in blue. Table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
4. **New Vulnerabilities** — PatternFly `Badge` in red. Table columns: Advisory ID, Severity (using existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have a highlighted background (use PatternFly `TableComposable` row variant `warning` or custom CSS).
5. **Resolved Vulnerabilities** — PatternFly `Badge` in green. Table columns: Advisory ID, Severity, Title, Previously Affected Package.
6. **License Changes** — PatternFly `Badge` in yellow. Table columns: Package Name, Left License, Right License.

**Empty State:**
When no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Loading State:**
While the comparison API call is in progress, each diff section shows a PatternFly `Skeleton` placeholder. The header toolbar is disabled during loading.

**Virtualization:**
For large diffs (>100 changed packages), use virtualized lists to prevent browser freezing per the non-functional requirements.

**URL shareability:**
The page reads `left` and `right` from URL query parameters on mount. When the user clicks "Compare", update the URL query params using React Router's `useSearchParams` so the comparison is bookmarkable and shareable.

Per CONVENTIONS.md (Key Conventions) -- Component library: PatternFly 5 -- all UI components use PF5 equivalents.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component file scope.

Per CONVENTIONS.md (Key Conventions) -- Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` page directory scope.

Per CONVENTIONS.md (Key Conventions) -- Naming: PascalCase for components.
Applies: task creates `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's `.tsx` component naming scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component; reuse in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — existing empty state component; reference for empty state pattern (may use directly or adapt)
- `src/components/LoadingSpinner.tsx` — existing loading indicator; reference for loading state pattern
- `src/hooks/useSboms.ts` — existing SBOM list hook; use to populate the SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference for table column patterns and package data rendering
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component; reference for advisory data rendering

## Acceptance Criteria
- [ ] `SbomComparePage` renders at `/sbom/compare` route
- [ ] Two PatternFly `Select` (typeahead) dropdowns for left and right SBOM selection
- [ ] "Compare" button disabled until both SBOMs selected; triggers comparison API call
- [ ] Six collapsible diff sections rendered using PatternFly `ExpandableSection` with `Badge` counts
- [ ] Added Packages section displays package name, version, license, advisory count with green badge
- [ ] Removed Packages section displays package name, version, license, advisory count with red badge
- [ ] Version Changes section displays package name, left/right versions, direction with blue badge
- [ ] New Vulnerabilities section uses `SeverityBadge` component; rows with Critical severity have highlighted background
- [ ] Resolved Vulnerabilities section displays advisory details with green badge
- [ ] License Changes section displays package name with left/right licenses and yellow badge
- [ ] Empty state shown with `CodeBranchIcon` when no comparison performed
- [ ] Loading state shows PatternFly `Skeleton` placeholders during API call
- [ ] URL query params `left` and `right` pre-populate selectors on page load
- [ ] Clicking "Compare" updates URL query params for shareability
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed

## Test Requirements
- [ ] Unit test: page renders empty state when no query params present
- [ ] Unit test: selectors pre-populate from URL query params
- [ ] Unit test: "Compare" button is disabled when selectors are empty
- [ ] Unit test: diff sections render with correct data from mock comparison result
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted styling
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Add MSW mock handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add mock comparison fixture data in `tests/mocks/fixtures/`

## Verification Commands
- `npx tsc --noEmit` — no TypeScript compilation errors
- `npx vitest run --reporter=verbose -- SbomComparePage` — page unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add comparison API types, client function, and React Query hook
