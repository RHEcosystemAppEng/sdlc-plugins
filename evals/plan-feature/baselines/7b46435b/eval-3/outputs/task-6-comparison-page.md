## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the main SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly Select, single, typeahead), a Compare button, and an Export dropdown (initially disabled, wired up in Task 8). Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page supports empty state (no comparison yet), loading state (skeleton placeholders), and URL-shareable comparisons via query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- Main comparison page component
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` -- Header toolbar with SBOM selectors and action buttons
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- Reusable collapsible diff section component with count badge and data table

## Files to Modify
- `src/routes.tsx` -- Add route for `/sbom/compare` with lazy-loaded SbomComparePage

## Implementation Notes
- Follow the page structure pattern from `src/pages/SbomDetailPage/` -- main page component with `components/` subdirectory for page-specific components.
- **Header Toolbar (CompareToolbar):**
  - Two PatternFly `Select` components (single, typeahead) for SBOM selection, using the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the dropdown items.
  - Pre-populate selectors from URL query params `left` and `right` using React Router's `useSearchParams`.
  - "Compare" button (PatternFly `Button`, primary variant) -- disabled until both selectors have values. On click, update URL params and trigger comparison via `useSbomComparison` hook.
  - "Export" dropdown -- render as a disabled PatternFly `Dropdown` with "Export JSON" and "Export CSV" items. Functional wiring deferred to Task 8.
- **Diff Sections (DiffSection):**
  - Each section is a PatternFly `ExpandableSection` with title, count `Badge`, and data `Table` (composable variant).
  - Section order and badge colors: Added Packages (green), Removed Packages (red), Version Changes (blue), New Vulnerabilities (red), Resolved Vulnerabilities (green), License Changes (yellow).
  - Sections with >0 items are expanded by default; sections with 0 items are collapsed.
  - **New Vulnerabilities section:** rows with severity "Critical" must have a highlighted/danger background row styling.
  - Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display in vulnerability sections.
  - For large diffs (>100 rows), implement virtualized rendering using `react-window` or PatternFly's built-in virtualization to prevent browser freezing per the non-functional requirement.
- **Table columns per section:**
  - Added/Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- **Empty State:** When no comparison has been performed (page load without query params or with incomplete params), show PatternFly `EmptyState` with `CodeBranchIcon` (PatternFly icon fallback), title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Use the same pattern as `src/components/EmptyStateCard.tsx`.
- **Loading State:** While comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the toolbar controls during loading.
- **URL-shareable comparison:** The URL encodes both SBOM IDs as query params (`?left={id1}&right={id2}`). When both params are present on page load, auto-trigger the comparison. This enables bookmarking and sharing.
- Add lazy-loaded route in `src/routes.tsx` using React Router v6 following the pattern of existing routes (e.g., SbomDetailPage).
- Per CONVENTIONS.md (Key Conventions) -- Component library: all UI components use PatternFly 5 equivalents. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's component scope.
- Per CONVENTIONS.md (Key Conventions) -- Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory. Applies: task creates `src/pages/SbomComparePage/` directory matching the convention's page structure scope.
- Per CONVENTIONS.md (Key Conventions) -- Naming: PascalCase for components, kebab-case for directories. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's naming scope.
- Per docs/constraints.md SS2: commit must reference TC-9003 in footer.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- existing severity badge component for vulnerability display in New/Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` -- existing empty state component pattern to follow
- `src/hooks/useSboms.ts` -- existing hook for populating SBOM selectors dropdown
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping for consistent severity display
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` -- page structure and component organization pattern reference

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] SBOM selectors load available SBOMs from the API and support typeahead filtering
- [ ] Compare button triggers comparison API call and renders results in diff sections
- [ ] All six diff sections render with correct data and table columns
- [ ] Count badges show correct counts with appropriate colors per section (green, red, blue, yellow)
- [ ] Sections with >0 items are expanded by default; 0-item sections are collapsed
- [ ] Critical vulnerabilities in "New Vulnerabilities" section have highlighted/danger background
- [ ] Empty state renders with CodeBranchIcon when no comparison has been performed
- [ ] Loading state shows skeleton placeholders during API call with toolbar disabled
- [ ] URL query params `left` and `right` encode both SBOM IDs for bookmarking/sharing
- [ ] Navigating to URL with pre-set `left` and `right` params auto-triggers comparison
- [ ] Large diffs (>100 rows) use virtualized rendering without browser freezing

## Test Requirements
- [ ] Component renders empty state when no query params are present
- [ ] Component renders comparison results with all six diff sections populated
- [ ] Count badges display correct counts with correct colors
- [ ] Critical vulnerability rows have highlighted/danger styling
- [ ] SBOM selectors populate from API data
- [ ] URL parameters are updated when Compare is clicked
- [ ] Component handles API error state gracefully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Add SBOM comparison API types and React Query hook
