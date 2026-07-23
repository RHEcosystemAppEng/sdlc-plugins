## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI based on the Figma design. The page features a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page supports URL-shareable comparisons via query parameters and handles empty state and loading state per the Figma specification.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main comparison page component orchestrating toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` -- header toolbar with left/right SBOM Select dropdowns (PatternFly Select, single, typeahead), Compare button (primary, disabled until both selectors have values), and Export dropdown (secondary, disabled until comparison loaded)
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section component wrapping PatternFly ExpandableSection with title, count Badge (color-coded), and data Table inside

## Implementation Notes
- **PatternFly 5 components to use:**
  - `Select` (single, typeahead) for SBOM selectors -- fetches SBOM list via existing `useSboms` hook
  - `ExpandableSection` for diff sections -- default expanded when item count > 0
  - `Badge` for count badges -- colors: green (Added Packages, Resolved Vulnerabilities), red (Removed Packages, New Vulnerabilities), blue (Version Changes), yellow (License Changes)
  - `Table` (composable) for data tables inside diff sections -- sortable columns, no pagination
  - `EmptyState` with `CodeBranchIcon` for initial empty state -- title: "Select two SBOMs to compare", body: "Choose an SBOM for each side and click Compare to see what changed."
  - `Dropdown` for Export button with items "Export JSON" and "Export CSV"
  - `Skeleton` for loading state placeholders per section

- **URL-shareable comparisons:** read `left` and `right` query parameters from the URL on page load to pre-populate the SBOM selectors. When the user clicks Compare, update the URL query parameters so the comparison is bookmarkable. Use React Router's `useSearchParams` hook.

- **Diff section table columns per Figma design:**
  1. Added Packages: Package Name, Version, License, Advisories (count)
  2. Removed Packages: Package Name, Version, License, Advisories (count)
  3. Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  4. New Vulnerabilities: Advisory ID, Severity (using `SeverityBadge`), Title, Affected Package
  5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  6. License Changes: Package Name, Left License, Right License

- **Critical vulnerability highlighting:** Rows in the New Vulnerabilities section where severity is "Critical" must have a highlighted background (e.g., PatternFly danger variant or custom CSS class).

- **Virtualized lists:** For diff sections with >100 items, use a virtualization library (e.g., react-window or react-virtualized) to prevent browser freezing per the non-functional requirements.

- **Loading state:** While the comparison API call is in progress, show PatternFly Skeleton placeholders in each diff section area. Disable the header toolbar (selectors and Compare button) during loading.

- **Export dropdown:** Render the Export dropdown in the toolbar but mark it as disabled until a comparison result is loaded. Export logic itself is non-MVP and will be implemented in a follow-up task.

- Follow existing page structure from `src/pages/SbomDetailPage/SbomDetailPage.tsx` for component organization with a `components/` subdirectory.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- existing severity badge component; use for vulnerability severity display in New Vulnerabilities and Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` -- existing empty state component; reference for empty state pattern (may need customization for CodeBranchIcon)
- `src/components/LoadingSpinner.tsx` -- existing loading indicator; consider for loading states
- `src/hooks/useSboms.ts` -- existing hook for fetching SBOM list; use to populate selector dropdowns
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` -- existing detail page; follow its component structure and PatternFly usage patterns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- existing package table component; reference for Table component usage pattern
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping utilities

## Acceptance Criteria
- [ ] Comparison page renders with header toolbar containing two SBOM selectors, Compare button, and Export dropdown
- [ ] SBOM selectors are populated from the SBOM list via useSboms hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API and renders six diff sections
- [ ] Each diff section is collapsible (ExpandableSection) with color-coded count Badge
- [ ] Diff sections are expanded by default when they contain items
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Empty state displays when no comparison has been performed (CodeBranchIcon, descriptive text)
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL query parameters (left, right) are read on page load and updated on Compare
- [ ] Export dropdown is rendered but disabled (non-MVP placeholder)
- [ ] Virtualized lists are used for diff sections exceeding 100 items

## Test Requirements
- [ ] Unit test: page renders empty state when no query parameters are present
- [ ] Unit test: page pre-populates selectors from URL query parameters
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button triggers API call and renders diff sections
- [ ] Unit test: diff sections display correct data from comparison response
- [ ] Unit test: New Vulnerabilities rows with Critical severity are visually highlighted
- [ ] Unit test: loading state shows Skeleton placeholders

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 4 -- Frontend: Add comparison API types, client function, and React Query hook
