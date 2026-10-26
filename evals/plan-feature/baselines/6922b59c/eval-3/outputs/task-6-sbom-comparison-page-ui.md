## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI with a header toolbar for SBOM selection and vertically stacked collapsible diff sections. The page displays the structured diff result from the comparison API using PatternFly components. This is the primary user-facing UI for the SBOM comparison feature.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — SBOM selector dropdown component wrapping PatternFly Select with typeahead

## Implementation Notes
- **Figma design reference:** The comparison view uses a full-page layout with a header toolbar and vertically stacked collapsible diff sections. All UI components map to PatternFly 5 equivalents.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page component scope. See `src/pages/SbomDetailPage/` for the established pattern.
- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TypeScript component scope. See `src/pages/SbomListPage/SbomListPage.tsx` for the established pattern.
- Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests and MSW for API mocking. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's test file scope. See `src/pages/SbomListPage/SbomListPage.test.tsx` for the established pattern.
- **Header toolbar components (per Figma):**
  - Left/Right SBOM selectors: PatternFly `Select` (single, typeahead) — pre-populated from URL query params `left` and `right`. Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to fetch the SBOM list for dropdown options.
  - "Compare" button: PatternFly primary `Button`, disabled until both selectors have values. Triggers `useSbomComparison` hook.
  - "Export" dropdown: PatternFly `Dropdown` with "Export JSON" and "Export CSV" items, disabled until comparison data is loaded (implementation deferred to Task 8).
- **Diff sections (per Figma, in order):**
  1. Added Packages — Badge color green, Table columns: Package Name, Version, License, Advisories (count)
  2. Removed Packages — Badge color red, Table columns: Package Name, Version, License, Advisories (count)
  3. Version Changes — Badge color blue, Table columns: Package Name, Left Version, Right Version, Direction
  4. New Vulnerabilities — Badge color red, Table columns: Advisory ID, Severity (use `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have highlighted background.
  5. Resolved Vulnerabilities — Badge color green, Table columns: Advisory ID, Severity, Title, Previously Affected Package
  6. License Changes — Badge color yellow, Table columns: Package Name, Left License, Right License
- **Each diff section** should be a `DiffSection` component using PatternFly `ExpandableSection` with `isExpanded` defaulting to `true` when the section has >0 items. Include a PatternFly `Badge` showing the item count.
- **Data tables** inside each section: use PatternFly composable `Table` with sortable columns. For sections with >100 rows, implement virtualized rendering per non-functional requirement (use `react-window` or PatternFly's built-in virtualization).
- **Empty state (per Figma):** When no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state:** While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area and disable the header toolbar.
- **URL-shareable comparison:** Read `left` and `right` from URL query params on page load. When the user clicks "Compare", update the URL query params so the comparison is bookmarkable. Use React Router's `useSearchParams` hook.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for vulnerability severity display in the New Vulnerabilities and Resolved Vulnerabilities sections.
- Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` as reference for the empty state pattern, adapting it for the comparison-specific content.
- Use the existing `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` as reference for loading indicator patterns.

## Reuse Candidates
- `src/components/SeverityBadge.tsx::SeverityBadge` — reuse for vulnerability severity display in diff sections
- `src/components/EmptyStateCard.tsx::EmptyStateCard` — reference for empty state pattern
- `src/components/LoadingSpinner.tsx::LoadingSpinner` — reference for loading state pattern
- `src/hooks/useSboms.ts::useSboms` — reuse for SBOM list data in the selector dropdowns
- `src/hooks/useSbomComparison.ts::useSbomComparison` — use for comparison data fetching (created in Task 5)
- `src/pages/SbomDetailPage/components/PackageTable.tsx::PackageTable` — reference for PatternFly Table component usage pattern with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx::AdvisoryList` — reference for advisory display pattern

## Acceptance Criteria
- [ ] Comparison page renders with header toolbar containing two SBOM selectors, Compare button, and Export dropdown
- [ ] SBOM selectors are PatternFly Select (single, typeahead) populated from the SBOM list API
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and renders diff sections
- [ ] All six diff sections render as PatternFly ExpandableSection with correct count Badges and color coding
- [ ] Diff section tables display correct columns per the Figma design
- [ ] New Vulnerabilities rows with severity "Critical" have highlighted background
- [ ] Severity values use the existing SeverityBadge component
- [ ] Empty state is shown when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL query params (`left`, `right`) are read on page load and updated on Compare click
- [ ] Page is URL-shareable: navigating to `/sbom/compare?left={id1}&right={id2}` auto-triggers comparison
- [ ] Large diffs (>100 rows in a section) use virtualized rendering

## Test Requirements
- [ ] Unit test: renders empty state when no query params are present
- [ ] Unit test: renders loading state when comparison is in progress
- [ ] Unit test: renders all six diff sections with correct data from mock comparison response
- [ ] Unit test: Compare button is disabled when only one selector has a value
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: URL params are updated when Compare is clicked

## Verification Commands
- `npx tsc --noEmit` — TypeScript compiles without errors
- `npx vitest run src/pages/SbomComparePage` — page tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison API client and React Query hook
