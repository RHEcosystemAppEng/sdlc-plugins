# Task 5 — Frontend: comparison diff section components

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the six collapsible diff sections of the SBOM comparison view (TC-9003) from the Figma "Comparison View" design: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities and License Changes. Each section shows a title, a colored count badge and a sortable data table. Critical new vulnerabilities get visual emphasis (an MVP requirement), and tables with more than 100 rows are virtualized (NFR).

## Files to Create
- `src/pages/SbomComparePage/components/DiffSection.tsx`: generic PF5 `ExpandableSection` wrapper with title, colored count `Badge`, `Skeleton` loading state, and default-expanded when the count is greater than 0
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx`: table for Added and Removed Packages (Package Name, Version, License, Advisories)
- `src/pages/SbomComparePage/components/VersionChangeTable.tsx`: table for Version Changes (Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx`: table for New and Resolved Vulnerabilities (Advisory ID, Severity, Title, Affected / Previously Affected Package), with critical-row highlight
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx`: table for License Changes (Package Name, Left License, Right License)
- `src/pages/SbomComparePage/components/DiffSection.test.tsx`: unit tests for the section and table components

## Implementation Notes
- **Section order, columns and badge colors** (from Figma):
  1. Added Packages: Package Name, Version, License, Advisories (count). Badge color: **green**
  2. Removed Packages: same columns. Badge color: **red**
  3. Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade). Badge color: **blue**
  4. New Vulnerabilities: Advisory ID, Severity (`SeverityBadge`), Title, Affected Package. Badge color: **red**. Rows with severity Critical get a highlighted background.
  5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package. Badge color: **green**
  6. License Changes: Package Name, Left License, Right License. Badge color: **yellow**
- **Custom sub-component specifications:**
  - Count badge: the PF5 `Badge` has no color variants. Use PF5 `Label` (`color="green" | "red" | "blue" | "gold"`, compact, `isCompact`), or a `Badge` with a token override such as `--pf-v5-global--palette--green-500`. Yellow maps to the PF `gold` palette. The Figma gives no explicit hex tokens, so map each color to the nearest PF5 palette token.
  - Critical row highlight: apply a row-level background using the PF5 danger palette (e.g., `--pf-v5-global--palette--red-50`) to `Tr` when `severity` is critical. Keep the `SeverityBadge` in the cell.
- **Data component rendering scope:**
  - Each table inside its `ExpandableSection` is **per-context**. Render only the array for that category (e.g., the New Vulnerabilities table renders `comparison.new_vulnerabilities` only). Do not merge or `flatMap` categories into a combined list.
  - The Added and Removed sections share `PackageDiffTable` but receive `comparison.added_packages` and `comparison.removed_packages` respectively.
- **Display text vs API value mismatches:**
  - `severity`: the API returns lowercase (`"critical"`, `"high"`, ...), while the Figma shows "Critical" and so on. Pass the value through `SeverityBadge` and `src/utils/severityUtils.ts`, which already handle the mapping and ordering. Compare critical severity case-insensitively. **Frontend mapping needed** (handled by the existing utility).
  - `direction`: the API returns `"upgrade"` / `"downgrade"`, while the Figma column label is "Direction (upgrade/downgrade)". **Frontend mapping needed**: `{ upgrade: "Upgrade", downgrade: "Downgrade" }` (optionally with an arrow icon).
  - `advisory_count`: a numeric value rendered as is under the "Advisories" column. No mismatch.
  - Column headers are static UI labels, not API values. No mapping needed.
- **Virtualization:** when a section has more than 100 rows, render a virtualized table body. First check `package.json` for an existing virtualization dependency (e.g., `@patternfly/react-virtualized-extension` or `react-window`). If none exists, adding one is a new dependency and must be called out in the PR description. Keep 100 rows or fewer non-virtualized.
- **Sorting:** use PF5 composable `Table` sortable column headers (`Th sort={...}`). There is no pagination.
- **Loading:** `DiffSection` accepts `isLoading` and renders PF5 `Skeleton` rows instead of the table.
- Per CONVENTIONS.md §Page structure: page-specific components go in `src/pages/SbomComparePage/components/`. See `src/pages/SbomDetailPage/components/PackageTable.tsx` and `AdvisoryList.tsx`.
  Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's page component (`src/pages/<Page>/components/*.tsx`) scope.
- Per CONVENTIONS.md §Component library: use PF5 components only (`ExpandableSection`, `Badge`/`Label`, `Table`/`Thead`/`Tbody`/`Tr`/`Th`/`Td`, `Skeleton`).
  Applies: task creates `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` matching the convention's UI component (`.tsx`) scope.
- Per CONVENTIONS.md §Shared components: reuse `src/components/SeverityBadge.tsx` for severity cells, and do not create a new severity badge.
  Applies: task creates `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` matching the convention's component (`.tsx`) scope.
- Per CONVENTIONS.md §Naming: use PascalCase component file names (`DiffSection.tsx`, `PackageDiffTable.tsx`).
  Applies: task creates `src/pages/SbomComparePage/components/PackageDiffTable.tsx` matching the convention's component naming (`.tsx`) scope.
- Per CONVENTIONS.md §Testing: use Vitest and React Testing Library with fixtures from `tests/mocks/fixtures/sbom-comparison.json` (Task 4).
  Applies: task creates `src/pages/SbomComparePage/components/DiffSection.test.tsx` matching the convention's unit test (`.test.tsx`) scope.
- Constraints (docs/constraints.md): §1.4/§5.1 scope to the listed files; §5.2 inspect `PackageTable.tsx`, `SeverityBadge.tsx` and `severityUtils.ts` before writing; §5.4 reuse the existing severity utilities and table patterns; §5.11–5.13 add test doc comments and given-when-then comments; §2.1–2.3 commit format; §3.3 open the PR with `--base TC-9003`.

## Reuse Candidates
- `src/components/SeverityBadge.tsx::SeverityBadge`: severity indicator required by the Figma
- `src/utils/severityUtils.ts`: severity ordering (sorting by severity) and color mapping (critical detection)
- `src/pages/SbomDetailPage/components/PackageTable.tsx`: existing PF5 package table (column layout, sorting) to mirror for `PackageDiffTable`
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx`: existing advisory list rendering to mirror for `VulnerabilityDiffTable`
- `src/components/LoadingSpinner.tsx`: existing loading pattern (the Figma specifies `Skeleton` per section, so use it only as a reference)

## Acceptance Criteria
- [ ] Six sections render in the Figma order, each with a title, a count badge in the specified color, and the specified columns
- [ ] Sections with more than 0 items are expanded by default; empty sections are collapsed
- [ ] Each table renders only its own category's data (per-context)
- [ ] New Vulnerabilities rows with critical severity have a highlighted background, and severity cells use `SeverityBadge`
- [ ] Direction renders as "Upgrade" / "Downgrade"
- [ ] Columns are sortable
- [ ] Sections with more than 100 rows use a virtualized body and stay responsive (no browser freeze)
- [ ] `isLoading` renders `Skeleton` placeholders in each section

## Test Requirements
- [ ] Test: each section renders the correct count badge and row count from the fixture
- [ ] Test: a section with 0 items is collapsed by default, and a section with items is expanded
- [ ] Test: a critical new vulnerability row has the highlight class/style, and a high-severity row does not
- [ ] Test: with 150+ rows, only a subset of rows is in the DOM (virtualized)
- [ ] Test: `isLoading` renders skeletons and no table rows
- [ ] Test: sorting by Package Name reorders rows

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Frontend: comparison API types, client function, React Query hook and mocks
