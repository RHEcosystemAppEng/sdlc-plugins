## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page component at `/sbom/compare` with the full UI as specified in the Figma design: header toolbar with SBOM selectors, Compare button, and Export dropdown; six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes); empty state and loading state handling. The page reads `left` and `right` SBOM IDs from URL query parameters to support shareable comparison URLs.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with a count `Badge` and a data `Table`
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar component with SBOM selectors, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- **Figma component mapping (PatternFly 5):**
  - SBOM selectors: PatternFly `Select` (single, typeahead) — fetches SBOM list using the existing `useSboms` hook. Pre-populate from URL query params `left` and `right`.
  - Compare button: PatternFly `Button` (primary variant) — disabled until both selectors have values. On click, updates URL query params and triggers comparison via `useSbomComparison` hook.
  - Export dropdown: PatternFly `Dropdown` (secondary variant) — two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded.
  - Diff sections: PatternFly `ExpandableSection` — default expanded for sections with >0 items. Each section title includes a PatternFly `Badge` with count.
  - Data tables inside sections: PatternFly `Table` (composable) — sortable columns. For >100 rows, use virtualized rendering to prevent browser freezing (per non-functional requirement).
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Loading state: PatternFly `Skeleton` placeholder in each diff section while API call is in progress. Header toolbar disabled during loading.
  - Severity indicators in New/Resolved Vulnerabilities sections: use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`.
  - Rows with Critical severity in the New Vulnerabilities section should have a highlighted/danger background.

- **Count badge colors by section:**
  - Added Packages: green
  - Removed Packages: red
  - Version Changes: blue
  - New Vulnerabilities: red
  - Resolved Vulnerabilities: green
  - License Changes: yellow

- **Table columns per section:**
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License

- **URL-shareable comparison:** The page reads `left` and `right` from `useSearchParams()`. When the user clicks Compare, update the URL params so the comparison is bookmarkable. On page load with both params present, auto-trigger comparison.

- **Export functionality (non-MVP):** Include the Export dropdown UI but the actual export implementation can be deferred — for now, the dropdown items can be disabled or trigger a TODO placeholder. The export feature is marked as non-MVP in the requirements.

- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TypeScript/React page scope.
- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's TypeScript/React component scope.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's TypeScript routing file scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; MSW for API mocking.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's TypeScript test file scope.

**Data component rendering scope:**
- All six diff section tables inside their respective `ExpandableSection` containers render **per-section** data — each table displays only the items for its diff category (e.g., the Added Packages table shows only `comparison.added_packages`, not all packages). Do not aggregate data across sections.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity level badges, used in New/Resolved Vulnerabilities table columns
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar patterns (though comparison page uses a custom toolbar)
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern (may need customization for the comparison-specific empty state)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (for general loading; diff sections use Skeleton)
- `src/hooks/useSboms.ts` — used by SBOM selectors to fetch the SBOM list for dropdown options
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page-level component structure with tabs/sections
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly Table usage with package data
- `src/utils/severityUtils.ts` — severity level ordering and color mapping, used for highlighting Critical vulnerabilities

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] SBOM selectors load the SBOM list and allow single selection with typeahead
- [ ] Compare button triggers API call and renders diff results in collapsible sections
- [ ] Each diff section shows a count badge with the correct color
- [ ] New Vulnerabilities section uses `SeverityBadge` and highlights Critical rows
- [ ] Empty state displays when no comparison has been performed (no query params)
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL query params `left` and `right` are updated on Compare and read on page load for shareable URLs
- [ ] Page handles large diffs (>100 changed packages) without browser freezing via virtualized lists

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders diff sections with correct data when comparison result is loaded
- [ ] Unit test: Compare button is disabled until both SBOM selectors have values
- [ ] Unit test: Critical severity rows in New Vulnerabilities section have highlighted background
- [ ] Unit test: diff sections with 0 items are collapsed by default, sections with >0 items are expanded
- [ ] Add mock comparison response fixture to `tests/mocks/fixtures/` for MSW handlers

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Frontend API layer (types, client, hook)

<!-- [sdlc-workflow] Description digest: sha256-md:cb04b5b1f0af2c4bb22318ea0063407487b1565349454a7e217dc06c9bc67ceb -->
