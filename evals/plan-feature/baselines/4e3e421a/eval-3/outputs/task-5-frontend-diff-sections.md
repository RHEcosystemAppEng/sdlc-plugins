# Task 5 — Add comparison diff section components

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the six collapsible diff-section components for the SBOM comparison page (TC-9003), following the Figma design "SBOMCompare / Comparison View". Each section is a PatternFly `ExpandableSection` with a title, a colored count badge, and a sortable composable `Table`. Packages with new critical vulnerabilities get visual emphasis (an MVP requirement). Large lists use virtualization so the browser does not freeze (NFR: more than 100 rows).

## Files to Create
- `src/pages/SbomComparePage/components/DiffSection.tsx` — generic wrapper: `ExpandableSection` + title + colored count badge + `Skeleton` loading slot. Expanded by default when count > 0.
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — table for Added/Removed Packages (columns: Package Name, Version, License, Advisories)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — table for Version Changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — table for New/Resolved Vulnerabilities (columns: Advisory ID, Severity, Title, Affected / Previously Affected Package). Highlights critical rows when used for new vulnerabilities.
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — table for License Changes (columns: Package Name, Left License, Right License)
- `src/pages/SbomComparePage/components/DiffSections.test.tsx` — unit tests for the components above

## Implementation Notes
- **Section order, titles and badge colors (from Figma):**
  1. Added Packages — green
  2. Removed Packages — red
  3. Version Changes — blue
  4. New Vulnerabilities — red
  5. Resolved Vulnerabilities — green
  6. License Changes — yellow
- **Custom sub-component specifications:**
  - Count badge: PF5 `Badge` has no color variants. Use PF5 `Label` with `color="green" | "red" | "blue" | "gold"` (`isCompact`), or a `Badge` with a PF color-token class (`--pf-v5-global--palette--green-300`, etc.). Yellow maps to the PF `gold` palette. The badge shows the item count of its section.
  - Critical row highlight: rows in **New Vulnerabilities** with `severity === "critical"` get a highlighted background using the PF danger token (`--pf-v5-global--danger-color--100` at low opacity, or `--pf-v5-global--palette--red-50`). Map hex to the nearest token. Pair the background with the `SeverityBadge` so the emphasis is not conveyed by color alone.
- **Data component rendering scope:**
  - Each table is nested inside its own `ExpandableSection` → **per-context**: each section renders only its own array from `SbomComparison`. Added Packages renders `comparison.added_packages`, Removed renders `comparison.removed_packages`, and so on. Do not merge or `flatMap` categories into one list.
  - The count badge shows `array.length` for that section only.
- **Display text vs API value mismatches:**
  - `severity`: the API returns lowercase (`"critical"`, `"high"`, `"medium"`, `"low"`), while Figma and `SeverityBadge` show title case ("Critical", ...). **Frontend mapping needed.** Pass the value through the existing helpers in `src/utils/severityUtils.ts` / `SeverityBadge` (check whether `SeverityBadge` already normalizes case; if it does not, map `{ critical: "Critical", high: "High", medium: "Medium", low: "Low" }`). Do the critical-row check on the raw API value `"critical"`.
  - `direction`: the API returns `"upgrade"` / `"downgrade"`, and the Direction column shows "Upgrade" / "Downgrade". **Frontend mapping needed:** `{ upgrade: "Upgrade", downgrade: "Downgrade" }`. Optionally add an arrow-up/arrow-down icon.
  - `license` / `left_license` / `right_license` may be `null`. Display "—" (the API returns null and Figma shows no placeholder, so the UI must provide one).
  - Section titles and column headers are static UI text, so no mapping is needed.
- **Sorting**: use the PF5 composable `Table` (`Thead`/`Th sort={...}`) with local sort state, following `src/pages/SbomDetailPage/components/PackageTable.tsx`. Default sort for vulnerability tables is severity descending, using the ordering helper in `src/utils/severityUtils.ts`.
- **Virtualization (NFR)**:
  - No pagination, per Figma. When a section has more than 100 rows, render the body virtualized.
  - First check `package.json` for an existing virtualization dependency, such as `@patternfly/react-virtualized-extension` or `react-window`.
  - If none exists, adding `@patternfly/react-virtualized-extension` (PF-aligned) is the preferred choice. Flag the new dependency in the PR description for reviewer approval, and add `package.json` to the PR.
  - With 100 rows or fewer, render the plain table.
- **Loading state**: `DiffSection` accepts `isLoading` and renders a PF `Skeleton` in place of the table, matching Figma's loading state.
- Per CONVENTIONS.md §Page structure: page-specific components go in `src/pages/<Page>/components/`. Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's page-specific component scope. Example: `src/pages/SbomDetailPage/components/PackageTable.tsx`.
- Per CONVENTIONS.md §Component library: use PF5 equivalents for all UI (`ExpandableSection`, `Label`/`Badge`, `Table`, `Skeleton`). Applies: task creates `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` matching the convention's React UI component scope. Example: `src/pages/SbomDetailPage/components/AdvisoryList.tsx`.
- Per CONVENTIONS.md §Naming: components use PascalCase. Applies: task creates `src/pages/SbomComparePage/components/PackageDiffTable.tsx` matching the convention's component naming scope. Example: `src/components/SeverityBadge.tsx`.
- Per CONVENTIONS.md §Testing: use Vitest + React Testing Library. Applies: task creates `src/pages/SbomComparePage/components/DiffSections.test.tsx` matching the convention's unit test scope. Example: `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`.
- Constraints (docs/constraints.md):
  - §2: commit format, Jira footer, `Assisted-by` trailer
  - §3: `gh pr create --base TC-9003`, and post the PR link to Jira
  - §5: scoped changes, reuse `SeverityBadge`/`severityUtils` rather than reimplementing them

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — required by Figma for the Severity column
- `src/utils/severityUtils.ts` — severity ordering for the default sort, plus severity color mapping
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing PF5 composable package table (columns: name, version, license). Base `PackageDiffTable` on it.
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory rendering for an SBOM
- `src/components/LoadingSpinner.tsx` / PF `Skeleton` — loading indicators

## Acceptance Criteria
- [ ] Six sections render in Figma order with the correct titles, columns, and badge colors (green/red/blue/red/green/yellow)
- [ ] Each section renders only its own category data (per-context), and its badge count equals that category's length
- [ ] Sections with more than 0 items are expanded by default, and sections with 0 items are collapsed
- [ ] New Vulnerabilities rows with `severity: "critical"` have a highlighted background and show `SeverityBadge`
- [ ] Severity and direction API values display as title-case labels, and null licenses display as "—"
- [ ] Columns are sortable
- [ ] Sections with more than 100 rows render virtualized, and the UI stays responsive with 2000 rows
- [ ] Each section shows a `Skeleton` while `isLoading` is true

## Test Requirements
- [ ] Renders each section with the fixture data and asserts the titles, column headers, and badge counts
- [ ] Asserts critical rows in New Vulnerabilities carry the highlight class, and non-critical rows do not
- [ ] Asserts the severity and direction label mapping (e.g., `"upgrade"` renders as "Upgrade")
- [ ] Asserts an empty section is collapsed and a non-empty section is expanded
- [ ] Asserts that with more than 100 rows, only a windowed subset of rows is in the DOM
- [ ] Asserts `Skeleton` renders when `isLoading`

## Verification Commands
- `npx vitest run src/pages/SbomComparePage` — component tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison API client, types, and React Query hook
