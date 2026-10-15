## Repository
trustify-ui

## Target Branch
main

## Description
Add the SBOM comparison page component at `/sbom/compare` implementing the Figma design. The page includes a header toolbar with two PatternFly `Select` dropdowns for SBOM selection, a "Compare" button, and an "Export" dropdown. Below the toolbar, six collapsible diff sections display the comparison results using PatternFly `ExpandableSection` components with data tables inside. The page supports URL-shareable comparisons via `left` and `right` query parameters, and handles empty state and loading state per the Figma specification.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count `Badge` and data `Table`
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM `Select` dropdowns, Compare button, and Export `Dropdown`

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to lazy-loaded `SbomComparePage`

## Implementation Notes
- **Figma design reference — Header Toolbar:**
  - Left SBOM selector: PatternFly `Select` (single, typeahead) showing SBOM name and version. Pre-populated from URL query param `left`. Fetches SBOM list via existing `useSboms` hook.
  - Right SBOM selector: identical `Select` dropdown for the second SBOM. Pre-populated from URL query param `right`.
  - "Compare" button: PatternFly primary action button, disabled until both selectors have values. Triggers the comparison API call via `useSbomCompare` hook.
  - "Export" dropdown: PatternFly `Dropdown` with two items — "Export JSON" and "Export CSV". Disabled until a comparison result is loaded. Export is a client-side operation: serialize the `SbomComparisonResult` data as JSON or CSV and trigger browser download.

- **Figma design reference — Diff Sections (in order):**
  1. **Added Packages** — PatternFly `ExpandableSection`. Table columns: Package Name, Version, License, Advisories (count). Count `Badge` color: green.
  2. **Removed Packages** — Table columns: Package Name, Version, License, Advisories (count). Count `Badge` color: red.
  3. **Version Changes** — Table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade). Count `Badge` color: blue.
  4. **New Vulnerabilities** — Table columns: Advisory ID, Severity (using `SeverityBadge` component), Title, Affected Package. Count `Badge` color: red. Rows with severity "Critical" have a highlighted background.
  5. **Resolved Vulnerabilities** — Table columns: Advisory ID, Severity, Title, Previously Affected Package. Count `Badge` color: green.
  6. **License Changes** — Table columns: Package Name, Left License, Right License. Count `Badge` color: yellow.

- **Figma design reference — Empty State:**
  PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

- **Figma design reference — Loading State:**
  PatternFly `Skeleton` placeholders in each diff section. Header toolbar disabled during loading.

- **Figma component mapping:**
  | Figma Element | PatternFly Component |
  |---|---|
  | SBOM selector | `Select` (single, typeahead) |
  | Diff section | `ExpandableSection` |
  | Count badge | `Badge` |
  | Data table | `Table` (composable) |
  | Severity indicator | `SeverityBadge` (existing) |
  | Empty state | `EmptyState` |
  | Export button | `Dropdown` |
  | Loading skeleton | `Skeleton` |

- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components. See `src/pages/SbomDetailPage/` for the pattern.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` page file scope.
- Per CONVENTIONS.md §Component library: all UI components must use PatternFly 5 equivalents.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. See `src/routes.tsx` for the existing lazy-loading pattern.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` file scope.
- Per CONVENTIONS.md §Naming: PascalCase for components (SbomComparePage, DiffSection, CompareToolbar).
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` file scope.
- URL-shareable comparison: read `left` and `right` from URL search params using `useSearchParams()`. When both are present, auto-trigger comparison on page load. When the user clicks Compare, update the URL search params so the comparison is bookmarkable.
- NFR: For diffs with >100 changed packages, use virtualized lists (e.g., `react-window` or PatternFly's built-in virtualization) to prevent browser freezing.
- Sections with >0 items should be expanded by default; sections with 0 items should be collapsed.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing severity badge component; use in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — Existing empty state component; adapt or use as reference for the comparison empty state
- `src/components/LoadingSpinner.tsx` — Loading indicator; use alongside Skeleton for loading state
- `src/hooks/useSboms.ts` — Existing hook to fetch SBOM list for the Select dropdowns
- `src/hooks/useSbomCompare.ts` — Comparison hook created in Task 3
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping for vulnerability tables
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Existing package table component; reference for table column patterns

## Acceptance Criteria
- [ ] `SbomComparePage` renders at `/sbom/compare` with the header toolbar and diff sections per Figma design
- [ ] SBOM selectors load the SBOM list via `useSboms` and allow typeahead search
- [ ] Compare button is disabled until both SBOM selectors have values
- [ ] Clicking Compare triggers the comparison API call and displays results in diff sections
- [ ] Each diff section uses PatternFly `ExpandableSection` with a count `Badge` in the appropriate color
- [ ] New Vulnerabilities table uses `SeverityBadge` component and highlights Critical rows
- [ ] Empty state displays PatternFly `EmptyState` with `CodeBranchIcon` when no comparison is active
- [ ] Loading state shows `Skeleton` placeholders and disables the toolbar
- [ ] URL query params `left` and `right` are read on page load and updated on Compare, enabling URL sharing
- [ ] Export dropdown offers JSON and CSV options, downloads the comparison data client-side
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Large diffs (>100 items) use virtualized lists

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no comparison is active
- [ ] Unit test: SbomComparePage renders diff sections when comparison data is available
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: URL params are read and pre-populate the SBOM selectors
- [ ] Unit test: Critical vulnerability rows have highlighted background
- [ ] Unit test: Export dropdown triggers JSON/CSV download

## Dependencies
- Depends on: Task 3 — Add SBOM comparison API types, client function, and hook
