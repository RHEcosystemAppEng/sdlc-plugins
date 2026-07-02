## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI at `/sbom/compare` following the Figma design specifications. The page includes a header toolbar with SBOM selectors, a compare button, an export dropdown, and vertically stacked collapsible diff sections for each change category. The page reads left/right SBOM IDs from URL query params to support bookmarkable, shareable comparison URLs.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main page component: reads left/right query params, renders ComparisonToolbar and DiffSection components, handles empty/loading/error states
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests using React Testing Library and MSW mocks
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar with left/right SBOM Select dropdowns, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable expandable section component wrapping PatternFly ExpandableSection with title, count Badge, and child table
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — composable Table for added/removed packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangeTable.tsx` — composable Table for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — composable Table for new/resolved vulnerabilities (columns: Advisory ID, Severity via SeverityBadge, Title, Affected Package) with critical-severity row highlighting
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` — composable Table for license changes (columns: Package Name, Left License, Right License)

## Implementation Notes
**Figma: Header Toolbar** — Two PatternFly `Select` components (single-select, typeahead variant) for left and right SBOM selection. Each selector shows SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populate selections from URL query params `left` and `right`. Include a primary "Compare" `Button` disabled until both selectors have values. Include a secondary "Export" `Dropdown` with two items ("Export JSON", "Export CSV"), disabled until comparison data is loaded.

**Figma: Diff Sections** — Six PatternFly `ExpandableSection` components stacked vertically in this order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes. Each section title includes a PatternFly `Badge` showing the item count with section-specific colors: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes. Sections with count > 0 are default expanded; sections with count 0 are default collapsed.

**Figma: Data Tables** — Each section contains a PatternFly composable `Table` with sortable columns. Use virtualized rendering for sections with > 100 rows to prevent browser freezing (per non-functional requirements).

**Figma: New Vulnerabilities** — Rows where severity is "Critical" have a highlighted background (use PatternFly danger/warning row variant). The Severity column uses the existing `SeverityBadge` shared component from `src/components/SeverityBadge.tsx`.

**Figma: Empty State** — When no comparison has been performed (page loads without query params or before clicking Compare), render a PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body text "Choose an SBOM for each side and click Compare to see what changed."

**Figma: Loading State** — While the comparison API call is in progress, show PatternFly `Skeleton` placeholders inside each diff section. Disable the header toolbar during loading to prevent concurrent requests.

The SBOM selectors fetch the SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. The comparison data is fetched via the `useSbomComparison` hook (Task 4).

Per CONVENTIONS.md §Component library: use PatternFly 5 components for all UI elements (Select, ExpandableSection, Badge, Table, EmptyState, Skeleton, Button, Dropdown). Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. Applies: task creates `src/pages/SbomComparePage/` directory structure matching the convention's page directory scope.

Per CONVENTIONS.md §Naming: PascalCase for components. Applies: task creates `SbomComparePage.tsx`, `ComparisonToolbar.tsx`, `DiffSection.tsx`, and table components matching the convention's `.tsx` scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component for vulnerability table rows
- `src/components/EmptyStateCard.tsx` — empty state pattern reference for the no-comparison state
- `src/components/LoadingSpinner.tsx` — loading indicator pattern reference
- `src/components/FilterToolbar.tsx` — toolbar layout pattern reference for ComparisonToolbar
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list to populate selectors

## Acceptance Criteria
- [ ] Comparison page renders with header toolbar containing left/right SBOM selectors, Compare button, and Export dropdown
- [ ] SBOM selectors are typeahead-enabled and populate from the SBOM list API
- [ ] Compare button is disabled until both selectors have values
- [ ] Export dropdown is disabled until comparison data is loaded
- [ ] Page reads `left` and `right` URL query params and pre-populates selectors
- [ ] All six diff sections render as expandable sections with correct count badges and colors
- [ ] Sections with items > 0 are expanded by default; empty sections are collapsed
- [ ] Added Packages table shows Package Name, Version, License, Advisories columns
- [ ] Removed Packages table shows Package Name, Version, License, Advisories columns
- [ ] Version Changes table shows Package Name, Left Version, Right Version, Direction columns
- [ ] New Vulnerabilities table shows Advisory ID, Severity (SeverityBadge), Title, Affected Package columns
- [ ] Resolved Vulnerabilities table shows Advisory ID, Severity, Title, Previously Affected Package columns
- [ ] License Changes table shows Package Name, Left License, Right License columns
- [ ] Critical-severity vulnerability rows have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Skeleton loading state displays during API call
- [ ] Large diffs (>100 rows) use virtualized rendering without browser freezing

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders comparison results with correct section counts and badge colors
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: selectors pre-populate from URL query params
- [ ] Unit test: Export dropdown is disabled before comparison data loads

## Dependencies
- Depends on: Task 1 — Create feature branch (create-branch bookend)
- Depends on: Task 4 — Frontend comparison API layer (hook and types must be available)
