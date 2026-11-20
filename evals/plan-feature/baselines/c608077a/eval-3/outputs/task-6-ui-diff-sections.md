# Task 6 — Build diff section components with virtualization and critical highlighting

**Summary:** Add six collapsible diff sections (tables, count badges, critical-vulnerability highlight, virtualized rows)
**Epic:** TC-9003: Comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Render the comparison result as six vertically stacked, collapsible diff sections, in the order shown in the Figma "Comparison View":

1. Added Packages
2. Removed Packages
3. Version Changes
4. New Vulnerabilities
5. Resolved Vulnerabilities
6. License Changes

Each section shows a title, a colored count badge, and a sortable table. New vulnerabilities with "Critical" severity are visually highlighted (an MVP requirement in TC-9003). Tables with more than 100 rows are virtualized so large diffs do not freeze the browser (an NFR). The sections are rendered by `SbomComparePage` (Task 5) once data has loaded.

## Files to Modify
- `src/pages/SbomComparePage/SbomComparePage.tsx` — replace the results-area placeholder with the six `DiffSection`s, wired to `useSbomComparison` data
- `src/utils/severityUtils.ts` — add (or reuse, if one exists) a normalizer from API severity strings (`"critical"`) to the `SeverityBadge` level (`Critical`)
- `package.json` — add a row-virtualization dependency (see Implementation Notes) if none is already present

## Files to Create
- `src/pages/SbomComparePage/components/DiffSection.tsx` — generic `ExpandableSection` wrapper: title, colored count `Badge`, default-expanded when count > 0, and children
- `src/pages/SbomComparePage/components/DiffTable.tsx` — generic composable PF5 `Table` with sortable columns and virtualization above 100 rows
- `src/pages/SbomComparePage/components/diffSectionConfig.ts` — the six section definitions: title, badge color, column definitions, and the response key each section reads
- `src/pages/SbomComparePage/components/DiffSection.test.tsx` — unit tests for sections and tables

## Implementation Notes
- **Section and column definitions (figma-context.md, "Diff Sections").**

  | Section | Response key | Columns | Badge color |
  |---|---|---|---|
  | Added Packages | `added_packages` | Package Name (`name`), Version (`version`), License (`license`), Advisories (`advisory_count`) | green |
  | Removed Packages | `removed_packages` | Package Name, Version, License, Advisories (count) | red |
  | Version Changes | `version_changes` | Package Name (`name`), Left Version (`left_version`), Right Version (`right_version`), Direction (`direction`) | blue |
  | New Vulnerabilities | `new_vulnerabilities` | Advisory ID (`advisory_id`), Severity (`severity`, rendered with `SeverityBadge`), Title (`title`), Affected Package (`affected_package`) | red |
  | Resolved Vulnerabilities | `resolved_vulnerabilities` | Advisory ID, Severity (`SeverityBadge`), Title, Previously Affected Package (`previously_affected_package`) | green |
  | License Changes | `license_changes` | Package Name (`name`), Left License (`left_license`), Right License (`right_license`) | yellow |

- **Data component rendering scope.**
  - Each `DiffTable` sits inside its own `ExpandableSection` frame, so it is **per-context**. Each section's table renders only `comparison[section.responseKey]`, for example `comparison.new_vulnerabilities` in the "New Vulnerabilities" section.
  - Do not merge, `flatMap`, or concatenate arrays across sections.
  - Each count badge shows `comparison[section.responseKey].length` for that section only, not a total.
- **Custom sub-component specifications.**
  - Count badge: PF5 `Badge` has no color variants. Use PF5 `Label` (compact, `isCompact`) with the PF color prop, or a `Badge` styled with PF tokens. Colors: green = `--pf-v5-global--success-color--100`, red = `--pf-v5-global--danger-color--100`, blue = `--pf-v5-global--info-color--100`, yellow = `--pf-v5-global--warning-color--100`. The Figma frame gives color names only, not hex values; map each name to the nearest PF token. Text is the item count, rendered in the label's default bold small font.
  - Critical row highlight (New Vulnerabilities): when the normalized severity is `Critical`, give the row a danger-tinted background (`--pf-v5-global--palette--red-50`, or the nearest PF token) and add an accessible indicator (e.g., `aria-label="critical"` on the row or a visually hidden "Critical" text). Color must not be the only signal.
  - The direction cell (Version Changes) shows "Upgrade" with `ArrowUpIcon` or "Downgrade" with `ArrowDownIcon` from `@patternfly/react-icons`.
- **Display text vs API value mismatches.**
  - Field `severity` in the New and Resolved Vulnerabilities tables: Figma shows "Critical", but the API returns lowercase (`"critical"`, `"high"`, `"medium"`, `"low"`), the same representation as `AdvisorySummary.severity`. **Frontend mapping needed** to the `SeverityBadge` levels: `{ critical: "Critical", high: "High", medium: "Medium", low: "Low" }`. Reuse an existing mapping in `src/utils/severityUtils.ts` if one exists; otherwise add it there, not inline. Unknown values fall back to rendering the raw string.
  - Field `direction` in Version Changes: Figma shows "upgrade/downgrade" as the Direction column, and the API returns `"upgrade"` / `"downgrade"`. **Frontend mapping needed** (case transformation): `{ upgrade: "Upgrade", downgrade: "Downgrade" }`.
  - Field `license`, `left_license`, `right_license`: the API may return `null` for an unknown license. Render "—" (em dash) or "Unknown" instead of an empty cell.
  - Section titles and column headers are static UI chrome, not API values, so no mapping is needed.
- **Default expansion.** A section is expanded when it has more than 0 items and collapsed when it has 0. Collapsed sections still show the title and a "0" badge.
- **Sorting.** All columns are sortable client-side, using PF5 composable `Table` `sort` props on `Th`. For the vulnerability tables, sort the Severity column by severity rank using the ordering in `src/utils/severityUtils.ts`, not alphabetically.
- **Virtualization (NFR: >100 changed packages).**
  - The project has no virtualization library in its listed dependencies.
  - Add `@patternfly/react-virtualized-extension` (preferred, because it is consistent with PF5) or `@tanstack/react-virtual`, and apply it inside `DiffTable` only when `rows.length > 100`.
  - Keep the composable table header and sticky header behaviour.
  - Per the Figma component mapping, the tables have no pagination.
- Per CONVENTIONS.md §Shared components: reuse `src/components/SeverityBadge.tsx` for severity cells rather than building a new badge. Keep `DiffSection` and `DiffTable` page-specific under `src/pages/SbomComparePage/components/` unless another page needs them. See `src/pages/SbomDetailPage/components/AdvisoryList.tsx`, which already renders `SeverityBadge` in a list.
  Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's `.tsx` component scope.
- Per CONVENTIONS.md §Component library: use PF5 `ExpandableSection`, composable `Table`/`Thead`/`Tbody`/`Tr`/`Th`/`Td`, `Label`/`Badge`, and `Skeleton`.
  Applies: task creates `src/pages/SbomComparePage/components/DiffTable.tsx` matching the convention's `.tsx` UI component scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library, using the MSW fixture `tests/mocks/fixtures/sbom-compare.json` (from Task 4).
  Applies: task creates `src/pages/SbomComparePage/components/DiffSection.test.tsx` matching the convention's unit-test scope.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits format, a `Implements TC-<task-key>` footer, and an `Assisted-by:` trailer.
  - §3 PR rules: use `--base TC-9003` and post the PR link on the Jira task.
  - §5 Code change rules: stay within the listed files; inspect before modifying; no duplicate severity logic (§5.4).
  - §1.4/§1.5: no unrelated refactoring.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing Critical/High/Medium/Low badge; required by the Figma design for the Severity columns
- `src/utils/severityUtils.ts` — existing severity ordering and color mapping; reuse it for sort order, the critical check, and the label mapping
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table (name, version, license columns); follow its composable-table and column patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory rendering with severity; follow its row layout

## Acceptance Criteria
- [ ] Six sections render in this order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes
- [ ] Each section shows a count badge equal to the length of its own response array, colored green, red, blue, red, green, and yellow respectively
- [ ] Each section's table shows exactly the Figma columns listed above, filled only from that section's response key
- [ ] Sections with more than 0 items are expanded by default; empty sections are collapsed
- [ ] Severity cells render `SeverityBadge` with the correct level for lowercase API values
- [ ] Rows in New Vulnerabilities with critical severity have a highlighted background and an accessible non-color indicator
- [ ] The Direction column shows "Upgrade" or "Downgrade" with an icon
- [ ] Null licenses render as a placeholder, not as empty cells
- [ ] Tables with more than 100 rows are virtualized (only visible rows are in the DOM); tables with 100 rows or fewer render normally
- [ ] Columns are sortable; severity sorts by rank

## Test Requirements
- [ ] Test: with the fixture, each section's title and badge count match its array length
- [ ] Test: the New Vulnerabilities row with `severity: "critical"` has the highlight class or attribute; a `"high"` row does not
- [ ] Test: severity `"medium"` renders `SeverityBadge` labelled "Medium"
- [ ] Test: an empty section (e.g., `license_changes: []`) is collapsed and shows a "0" badge
- [ ] Test: a 500-row `added_packages` input renders far fewer than 500 `<tr>` elements (virtualized); a 50-row input renders all 50
- [ ] Test: clicking the Severity header sorts Critical before High before Medium before Low
- [ ] Test: a section table never shows rows from another section (e.g., an `advisory_id` never appears in Added Packages)

## Verification Commands
- `npx vitest run src/pages/SbomComparePage` — all tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SbomComparison types, fetchSbomComparison() and useSbomComparison hook with MSW mocks
- Depends on: Task 5 — Add /sbom/compare page with SBOM selectors, Compare button, URL-shareable state, empty and loading states
