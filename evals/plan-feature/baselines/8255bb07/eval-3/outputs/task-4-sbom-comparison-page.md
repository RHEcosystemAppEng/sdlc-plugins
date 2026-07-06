## Repository
trustify-ui

## Target Branch
main

## Description
Build the SBOM comparison page at `/sbom/compare` following the Figma design specifications. The page includes a header toolbar with two SBOM selectors and a Compare button, six collapsible diff sections with data tables, empty and loading states, and an export dropdown for JSON/CSV output. Packages with new critical vulnerabilities are visually highlighted with an emphasized background.

**Figma design context (from figma-context.md):**

The comparison view is a full-page layout with:

**Header Toolbar:**
- Left and Right SBOM selectors: PatternFly `Select` (single, typeahead) pre-populated from URL query params `left` and `right`. Fetches SBOM list via existing `useSboms` hook.
- "Compare" button: PatternFly primary button, disabled until both selectors have values. Triggers the diff API call.
- "Export" dropdown: PatternFly `Dropdown` with "Export JSON" and "Export CSV" options. Disabled until a comparison result is loaded.

**Diff Sections (each is a PatternFly `ExpandableSection` with a `Badge` count):**
1. Added Packages (green badge) — columns: Package Name, Version, License, Advisories (count)
2. Removed Packages (red badge) — columns: Package Name, Version, License, Advisories (count)
3. Version Changes (blue badge) — columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
4. New Vulnerabilities (red badge) — columns: Advisory ID, Severity (using existing `SeverityBadge` component), Title, Affected Package. Rows with severity "Critical" have a highlighted background.
5. Resolved Vulnerabilities (green badge) — columns: Advisory ID, Severity, Title, Previously Affected Package
6. License Changes (yellow badge) — columns: Package Name, Left License, Right License

**Empty State:** PatternFly `EmptyState` with `CodeBranchIcon` fallback icon, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Loading State:** PatternFly `Skeleton` placeholders in each diff section. Header toolbar is disabled during loading.

**Virtualization:** Use virtualized lists for tables with >100 rows to prevent browser freezing.

**PatternFly component mapping:** Select (single, typeahead), ExpandableSection, Badge, Table (composable, sortable), SeverityBadge (existing shared component), EmptyState, Dropdown, Skeleton.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component orchestrating the header toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Page component tests covering rendering states and user interactions
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with SBOM Select dropdowns, Compare button, and Export Dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly ExpandableSection with Badge count and a data table
- `src/pages/SbomComparePage/components/VulnerabilityTable.tsx` — Vulnerability-specific table with SeverityBadge column rendering and critical row highlighting

## Implementation Notes
- Follow the page structure pattern in `src/pages/SbomDetailPage/`: main page component file with a `components/` subdirectory for page-specific sub-components.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the vulnerability severity column in the New Vulnerabilities and Resolved Vulnerabilities sections. Do not create a duplicate severity display.
- Use the existing `EmptyStateCard` from `src/components/EmptyStateCard.tsx` as a reference for the pre-comparison empty state. Adapt it to use `CodeBranchIcon` and the specific title/body text from the Figma spec.
- Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the SBOM selector dropdowns with the list of available SBOMs.
- Use the `useSbomComparison` hook from Task 3 (`src/hooks/useSbomComparison.ts`) for comparison data fetching.
- Use PatternFly 5 components throughout: `Select` (single, typeahead variant) for SBOM selectors, `ExpandableSection` for collapsible diff sections, `Badge` for count indicators, `Table` (composable) for data tables with sortable columns, `Dropdown` for export menu, `Skeleton` for loading placeholders.
- Badge colors per section: green (`isRead` variant or custom) for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- Sections with >0 items should default to expanded (`isExpanded={true}`); sections with 0 items default to collapsed.
- For critical vulnerability highlighting: conditionally apply a CSS class or inline style to table rows where `severity === "critical"` to render a highlighted background using PatternFly's danger color token (e.g., `--pf-v5-global--danger-color--100`).
- Implement virtualized rendering for tables with >100 rows to meet the non-functional requirement. Use `react-window` or PatternFly's built-in virtualization support.
- Export JSON: serialize the `SbomComparisonResult` object to a formatted JSON string and trigger a browser file download (create a Blob, generate an object URL, click a hidden anchor).
- Export CSV: transform each diff category's data to CSV rows with headers and trigger a browser file download. Generate a combined CSV with a "Section" column or separate files per section.
- Use `src/utils/severityUtils.ts` for consistent severity ordering and color mapping in the vulnerability tables.
- Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` page file scope.
- Per CONVENTIONS.md §Component Library: all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.tsx` test file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component for rendering severity levels in vulnerability tables
- `src/components/EmptyStateCard.tsx` — existing empty state component; reference for PatternFly EmptyState usage
- `src/components/LoadingSpinner.tsx` — existing loading indicator; reference for loading state patterns
- `src/hooks/useSboms.ts` — existing hook to fetch the SBOM list for populating selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference for PatternFly Table column definitions and rendering
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component; reference for advisory/vulnerability data display
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for consistent vulnerability display across the app

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] SBOM selectors load the SBOM list via useSboms and allow typeahead selection
- [ ] Compare button is disabled until both SBOM selectors have values
- [ ] Compare button triggers the comparison API call via useSbomComparison and renders results in diff sections
- [ ] All six diff sections render with correct column definitions, count badges, and table data
- [ ] Sections with items default to expanded; empty sections default to collapsed
- [ ] Critical vulnerability rows in the New Vulnerabilities section are visually highlighted
- [ ] Empty state displays with CodeBranchIcon and correct text when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during the API call with toolbar disabled
- [ ] Export JSON downloads the comparison result as a .json file
- [ ] Export CSV downloads the comparison data as a .csv file
- [ ] Export dropdown is disabled until a comparison result is loaded
- [ ] Tables with >100 rows use virtualized rendering without browser freezing

## Test Requirements
- [ ] Unit test: page renders empty state when no SBOM IDs are present in URL or selectors
- [ ] Unit test: SBOM selectors are populated from useSboms hook data
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: page renders all six diff sections with correct data after a successful comparison
- [ ] Unit test: critical vulnerability rows have highlighted styling applied
- [ ] Unit test: ExpandableSection defaults to expanded for sections with items, collapsed for empty sections
- [ ] Unit test: export buttons are disabled before comparison result is loaded
- [ ] Unit test: DiffSection component renders with the correct badge count and table columns

## Verification Commands
- `npx tsc --noEmit` — no TypeScript compilation errors
- `npx vitest run src/pages/SbomComparePage` — all comparison page tests pass

## Dependencies
- Depends on: Task 3 — Add SBOM comparison API types, client function, and React Query hook
