# Task 6 — Render the six collapsible diff sections with virtualization and critical highlighting

**Summary:** Add collapsible diff sections (packages, versions, vulnerabilities, licenses) with count badges, virtualized tables, and critical-vulnerability highlighting
**Epic:** TC-9003: SBOM comparison UI

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Render the comparison result as six collapsible sections in Figma order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. Each section has a title, a colored count badge, and a sortable table. Tables with more than 100 rows must be virtualized so large diffs do not freeze the browser (NFR). New vulnerabilities with severity Critical get a highlighted row background (MVP requirement: "Highlight packages with new critical vulnerabilities").

## Files to Modify
- `src/pages/SbomComparePage/SbomComparePage.tsx` — replace the result placeholder from Task 5 with the six `DiffSection` instances
- `src/utils/severityUtils.ts` — add a normalization helper only if no existing helper maps the lowercase API severity (`"critical"`) to the `SeverityBadge` level; otherwise reuse the existing one
- `package.json` — add a virtualization dependency only if none is already present (check for `@patternfly/react-virtualized-extension` or `react-window` first)

## Files to Create
- `src/pages/SbomComparePage/components/DiffSection.tsx` — generic `ExpandableSection` wrapper: title, colored count `Badge`, default-expanded when count > 0, renders its child table
- `src/pages/SbomComparePage/components/DiffTable.tsx` — generic composable PF `Table` with sortable columns. Switches to virtualized rendering above 100 rows. Accepts an optional `isRowHighlighted(row)` predicate
- `src/pages/SbomComparePage/components/diffSectionConfig.tsx` — column definitions, badge color, and title for each of the six sections
- `src/pages/SbomComparePage/components/DiffSection.test.tsx` — tests for sections, badges, expansion, sorting, virtualization, and highlight

## Implementation Notes
**Section specification (from Figma):**

| # | Section | Data array | Columns | Badge color |
|---|---|---|---|---|
| 1 | Added Packages | `added_packages` | Package Name, Version, License, Advisories (count) | green |
| 2 | Removed Packages | `removed_packages` | Package Name, Version, License, Advisories (count) | red |
| 3 | Version Changes | `version_changes` | Package Name, Left Version, Right Version, Direction | blue |
| 4 | New Vulnerabilities | `new_vulnerabilities` | Advisory ID, Severity (`SeverityBadge`), Title, Affected Package | red |
| 5 | Resolved Vulnerabilities | `resolved_vulnerabilities` | Advisory ID, Severity, Title, Previously Affected Package | green |
| 6 | License Changes | `license_changes` | Package Name, Left License, Right License | yellow |

**Data component rendering scope:**
- Each table sits inside its own `ExpandableSection`, so it is **per-context**: render only `comparison.<section_array>` for that section. For example, the New Vulnerabilities table renders only `comparison.new_vulnerabilities`. Do not merge the package arrays into one table, and do not `flatMap` vulnerabilities across sections.
- The count badge for each section is `comparison.<section_array>.length` for that section only.

**Custom sub-component specifications:**
- Count badge: PF5 `Badge` has no color variants. Render it as a compact PF `Label` (`isCompact`) with color green, red, blue, or yellow (PF5 Label colors `green` / `red` / `blue` / `gold`), or style `Badge` with PF tokens (`--pf-v5-global--success-color--100`, `--pf-v5-global--danger-color--100`, `--pf-v5-global--info-color--100`, `--pf-v5-global--warning-color--100`). Figma did not supply hex values, so map each color to the nearest PF token.
- Critical row highlight (New Vulnerabilities only): rows where the severity normalizes to Critical get a highlighted background, using the PF danger background token (e.g., `--pf-v5-global--palette--red-50`) plus the existing `SeverityBadge`. Figma did not supply hex values; map to the nearest danger token.

**Display text vs API value mismatches:**
- `severity` (New/Resolved Vulnerabilities): Figma and `SeverityBadge` use title case (Critical/High/Medium/Low), but the API returns lowercase (`"critical"`). **Frontend mapping needed**: `{ critical: "Critical", high: "High", medium: "Medium", low: "Low" }`. Check `src/utils/severityUtils.ts` for an existing ordering/color map that already handles this before adding one. Base the critical-row predicate on the normalized value.
- `direction` (Version Changes): Figma shows a "Direction (upgrade/downgrade)" column, and the API returns lowercase `"upgrade"` / `"downgrade"`. **Frontend mapping needed**: `{ upgrade: "Upgrade", downgrade: "Downgrade" }`. An arrow icon (PF `ArrowUpIcon` / `ArrowDownIcon`) is optional polish.
- Advisories (count): the API field is `advisory_count` (number). No mismatch; render as is.
- Section titles are static UI text, not API values, so no mapping is needed.

**Virtualization (NFR: no browser freeze for more than 100 changed packages):** when `rows.length > 100`, render the table body virtualized. Prefer `@patternfly/react-virtualized-extension` (PF-consistent) if it is already in `package.json`. Otherwise add a virtualization library, noting it in the PR description. At 100 rows or fewer, render the plain composable `Table`. Sorting must work in both modes; sort the data array before passing it to the virtualizer.

**Default expansion:** sections with more than 0 items start expanded. Empty sections start collapsed and show their `0` badge.

**Conventions:**
- Per CONVENTIONS.md §Page structure: put page-specific components in `src/pages/SbomComparePage/components/`, like `src/pages/SbomDetailPage/components/PackageTable.tsx`.
  Applies: task modifies `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's page `components/` subdirectory scope.
- Per CONVENTIONS.md §Component library: use PF5 `ExpandableSection`, `Badge`/`Label`, and composable `Table` (`Thead`/`Tbody`/`Tr`/`Th sort`/`Td`).
  Applies: task modifies `src/pages/SbomComparePage/components/DiffTable.tsx` matching the convention's `.tsx` UI component scope.
- Per CONVENTIONS.md §Shared components: reuse `src/components/SeverityBadge.tsx` for severity cells. Do not create a new severity component.
  Applies: task modifies `src/pages/SbomComparePage/components/diffSectionConfig.tsx` matching the convention's `.tsx` component scope.
- Per CONVENTIONS.md §Naming: PascalCase components (`DiffSection.tsx`, `DiffTable.tsx`); camelCase utilities (`severityUtils.ts`).
  Applies: task modifies `src/utils/severityUtils.ts` matching the convention's utility naming scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library using the `tests/mocks/fixtures/sbom-compare.json` fixture from Task 4.
  Applies: task modifies `src/pages/SbomComparePage/components/DiffSection.test.tsx` matching the convention's unit test (`*.test.tsx`) scope.

**Project constraints (docs/constraints.md):**
- §2: Conventional Commits, `Implements TC-XXXX` footer, `Assisted-by:` trailer.
- §3: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5: Change only the listed files; reuse `SeverityBadge`, `severityUtils`, and the `PackageTable` column patterns rather than duplicating them.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity badge required by Figma for the New Vulnerabilities column, and reusable for Resolved.
- `src/utils/severityUtils.ts` — severity ordering and color mapping. Reuse it to sort by severity and to normalize the lowercase API values.
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table (name/version/license columns). Reuse its column and cell rendering patterns for Added/Removed Packages.
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory row rendering (ID, title, severity) for the vulnerability sections.

## Acceptance Criteria
- [ ] Six `ExpandableSection`s render in Figma order with the specified titles
- [ ] Each section's count badge shows the length of that section's array in the specified color (green/red/blue/red/green/yellow)
- [ ] Sections with more than 0 items are expanded by default; empty sections are collapsed
- [ ] Each table shows exactly the Figma columns for its section and supports column sorting
- [ ] The New Vulnerabilities severity column uses `SeverityBadge` with title-case levels mapped from lowercase API values
- [ ] Rows in New Vulnerabilities with Critical severity have a highlighted background
- [ ] Version Changes shows "Upgrade" / "Downgrade" mapped from the API `direction`
- [ ] Tables with more than 100 rows render virtualized; the DOM row count stays well below the data row count
- [ ] Each section renders only its own array (per-context scope)

## Test Requirements
- [ ] Test: all six sections render in order with the correct counts from the fixture
- [ ] Test: an empty section is collapsed and an expanded section shows its rows
- [ ] Test: a Critical row in New Vulnerabilities has the highlight class/style and a High row does not
- [ ] Test: severity `"critical"` renders `SeverityBadge` as "Critical"; direction `"downgrade"` renders "Downgrade"
- [ ] Test: with more than 100 added packages, fewer than 100 rows exist in the DOM (virtualized)
- [ ] Test: clicking a sortable column header reorders rows

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/pages/SbomComparePage` — all tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, and empty/loading states
