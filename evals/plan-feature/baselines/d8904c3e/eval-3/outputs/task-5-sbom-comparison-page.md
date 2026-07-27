## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page UI at `/sbom/compare` with a header toolbar for SBOM selection and vertically stacked collapsible diff sections. The page renders the comparison result from the useSbomComparison hook (Task 4) in six categorized sections: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. Each section uses PatternFly ExpandableSection with a count Badge and a sortable Table inside. The page handles empty state (no comparison performed), loading state (Skeleton placeholders), and large diffs (virtualized lists for >100 items).

**Figma design reference:** The comparison view uses a full-page layout per the Figma SBOMCompare mockup (mock123, page "Comparison View"). The header toolbar contains two PatternFly `Select` (single, typeahead) dropdowns for SBOM selection pre-populated from URL query params, a primary `Button` ("Compare") disabled until both selectors have values, and a secondary `Dropdown` ("Export") with JSON/CSV options (disabled in initial implementation -- non-MVP). Each diff section is a PatternFly `ExpandableSection` default-expanded when item count > 0, containing a composable `Table` with sortable columns. Count badges use PatternFly `Badge` with color coding: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes. Empty state uses PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body text as specified. Loading state shows `Skeleton` placeholders in each section with the toolbar disabled.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main comparison page component orchestrating toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- component tests using MSW mocks
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` -- header toolbar with SBOM Select dropdowns, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section with ExpandableSection, Badge count, and Table

## Implementation Notes
Per CONVENTIONS.md page structure: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory for page-specific components. See `src/pages/SbomDetailPage/` for the established pattern.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` page component scope.

Per CONVENTIONS.md PatternFly 5: all UI components use PF5 equivalents. Import from `@patternfly/react-core` and `@patternfly/react-table`.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md testing: use Vitest + React Testing Library for unit tests and MSW for API mocking. See `src/pages/SbomListPage/SbomListPage.test.tsx` for the established test pattern.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.tsx` test file scope.

**Component architecture:**
- `SbomComparePage` manages URL query params (`left`, `right`) using React Router's `useSearchParams`, calls `useSbomComparison(leftId, rightId)`, and renders `ComparisonToolbar` + six `DiffSection` instances
- `ComparisonToolbar` renders two PatternFly `Select` (typeahead, single-select) dropdowns populated via the existing `useSboms` hook, a "Compare" `Button` (primary, disabled until both selected), and an "Export" `Dropdown` (disabled -- non-MVP placeholder)
- `DiffSection` accepts generic props: `title`, `count`, `badgeColor`, `columns`, `rows`, `isLoading`. Renders `ExpandableSection` (default expanded when count > 0), `Badge` with count and color, and composable `Table` with sortable columns

**Table column definitions per section:**
- Added Packages: Package Name, Version, License, Advisories (count)
- Removed Packages: Package Name, Version, License, Advisories (count)
- Version Changes: Package Name, Left Version, Right Version, Direction
- New Vulnerabilities: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package
- Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
- License Changes: Package Name, Left License, Right License

**Critical vulnerability highlighting:**
- In the New Vulnerabilities section, rows where `severity === "critical"` receive a highlighted row background. Use PatternFly's `isHoverable` row prop or a custom CSS class for visual emphasis.

**Large diff handling:**
- When a section has >100 rows, use virtualized rendering (e.g., `react-window` or PatternFly's built-in virtualization) to prevent browser freezing per the non-functional requirement.

**Display text vs API value considerations:**
- The `severity` field returns lowercase strings from the API ("critical", "high", etc.). The existing `SeverityBadge` component handles the display transformation -- no additional mapping needed.
- The `direction` field returns "upgrade" or "downgrade" from the API. Display as-is with title case ("Upgrade", "Downgrade") using a simple capitalize transform.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- existing shared component for rendering severity indicators in the New/Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` -- existing empty state component pattern (may need adaptation for comparison-specific content)
- `src/components/LoadingSpinner.tsx` -- existing loading indicator (Skeleton may be more appropriate per Figma, but reference this for pattern)
- `src/components/FilterToolbar.tsx` -- reference for PatternFly toolbar layout patterns
- `src/hooks/useSboms.ts` -- existing hook to populate the SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- reference for PatternFly Table usage with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` -- reference for advisory display patterns

## Acceptance Criteria
- [ ] SbomComparePage renders with header toolbar and six collapsible diff sections
- [ ] SBOM selector dropdowns are populated from the existing SBOM list endpoint
- [ ] Compare button triggers API call and renders diff results in the appropriate sections
- [ ] Each section shows a colored count Badge matching the Figma specification
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with critical severity have highlighted backgrounds
- [ ] Empty state renders when no comparison has been performed (no query params)
- [ ] Loading state shows Skeleton placeholders while the comparison API call is in progress
- [ ] URL query params (left, right) pre-populate the selectors on page load
- [ ] Export dropdown is rendered but disabled with non-MVP indicator

## Test Requirements
- [ ] Component test: renders empty state when no SBOM IDs are provided
- [ ] Component test: renders loading skeletons while comparison is in progress
- [ ] Component test: renders all six diff sections with correct data from mock response
- [ ] Component test: sections with zero items are collapsed by default
- [ ] Component test: critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] Component test: SBOM selectors are populated from mock SBOM list data
- [ ] Component test: Compare button is disabled until both selectors have values

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 4 -- Add SBOM comparison API layer (provides useSbomComparison hook and TypeScript types)
