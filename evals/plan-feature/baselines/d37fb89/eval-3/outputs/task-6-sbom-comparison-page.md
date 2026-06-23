## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page at `/sbom/compare` with the header toolbar (SBOM selectors, Compare button, Export dropdown) and vertically stacked collapsible diff sections. The page reads `left` and `right` query parameters from the URL for shareable comparisons, and uses the `useSbomComparison` hook to fetch diff data from the backend.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- Main comparison page component with header toolbar and diff sections layout
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` -- Header toolbar with left/right SBOM `Select` dropdowns, primary "Compare" button, and secondary "Export" `Dropdown`
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- Reusable collapsible diff section using PatternFly `ExpandableSection` with count `Badge` and composable `Table`

## Files to Modify
- `src/routes.tsx` -- Add route for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- **Figma reference**: The comparison view uses a full-page layout with a header toolbar and vertically stacked collapsible diff sections (see figma-context.md).
- **ComparisonToolbar**: Use PatternFly `Select` (single, typeahead) for both SBOM selectors. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populate from URL query params `left` and `right`. The "Compare" button is a PatternFly primary `Button`, disabled until both selectors have values. The "Export" button is a PatternFly `Dropdown` with items "Export JSON" and "Export CSV", disabled until comparison data is loaded.
- **DiffSection**: Each section is a PatternFly `ExpandableSection` with a title and count `Badge`. Badge colors: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes. Sections with >0 items default to expanded. Each section contains a PatternFly composable `Table` with sortable columns. For >100 rows, use virtualized rendering to prevent browser freezing per the non-functional requirements.
- **Diff section order and columns** (per Figma):
  1. Added Packages: Package Name, Version, License, Advisories (count)
  2. Removed Packages: Package Name, Version, License, Advisories (count)
  3. Version Changes: Package Name, Left Version, Right Version, Direction
  4. New Vulnerabilities: Advisory ID, Severity (using `SeverityBadge`), Title, Affected Package -- rows with "Critical" severity have highlighted background
  5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  6. License Changes: Package Name, Left License, Right License
- **Empty state**: When no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.
- **URL-shareable**: Update URL query parameters `left` and `right` when the user clicks Compare, using React Router's `useSearchParams`. On page load, read params and auto-trigger comparison if both are present.
- **Route registration**: Add the `/sbom/compare` route in `src/routes.tsx` using lazy loading per existing patterns. Register it before `/sbom/:id` to avoid path conflicts.

## Reuse Candidates
- `src/hooks/useSboms.ts` -- Existing hook to fetch SBOM list for the selector dropdowns
- `src/components/SeverityBadge.tsx` -- Existing shared component for severity display in the New Vulnerabilities section
- `src/components/EmptyStateCard.tsx` -- Existing empty state component; adapt for comparison empty state
- `src/components/LoadingSpinner.tsx` -- Existing loading indicator; use alongside Skeleton placeholders
- `src/components/FilterToolbar.tsx` -- PatternFly toolbar pattern reference

## Acceptance Criteria
- [ ] Page renders at `/sbom/compare` with header toolbar and empty state when no params provided
- [ ] SBOM selectors populate with SBOM list from existing endpoint
- [ ] Clicking "Compare" triggers API call and renders diff sections with correct data
- [ ] URL updates with `left` and `right` query parameters when comparison is triggered
- [ ] Opening a URL with `left` and `right` params auto-loads the comparison
- [ ] Diff sections use correct column layouts and badge colors per Figma spec
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Sections with >0 items default to expanded; sections with 0 items default to collapsed
- [ ] Loading state shows Skeleton placeholders and disables toolbar
- [ ] Empty state shows CodeBranchIcon with correct title and body text

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- API types and client function for SBOM comparison

[sdlc-workflow] Description digest: sha256-md:3f2bf825508e2a37932a7f7b7ff3068bebb6c6cb4f23eef3d582db48ec220bc6
