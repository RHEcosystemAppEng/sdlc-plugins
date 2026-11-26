# Task 6 — Render collapsible diff sections with tables, critical highlighting, and virtualization

**Summary:** Render the six SBOM diff sections with count badges, sortable tables, and critical-vulnerability highlighting
**Epic:** TC-9003: SBOM comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003; fixVersion scope = both)

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the body of the comparison page (TC-9003): six vertically stacked PatternFly `ExpandableSection`s — Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes — each with a title, a colored count badge, and a sortable data table. Rows in New Vulnerabilities with severity Critical are visually highlighted (MVP requirement "Highlight packages with new critical vulnerabilities"). Tables with more than 100 rows must be virtualized so large diffs do not freeze the browser (NFR).

## Files to Modify
- `src/pages/SbomComparePage/SbomComparePage.tsx` — replace the diff placeholder container from Task 5 with the six `DiffSection`s
- `src/utils/severityUtils.ts` — add (or reuse, if present) a normalizer from API severity strings (e.g., `"critical"`) to the `SeverityBadge` level, and severity-based default sort order
- `package.json` — add a virtualization dependency only if none is already present (check for `@patternfly/react-virtualized-extension` / `react-window` first)

## Files to Create
- `src/pages/SbomComparePage/components/DiffSection.tsx` — generic `ExpandableSection` + count `Badge`/`Label` + table wrapper, default-expanded when count > 0
- `src/pages/SbomComparePage/components/DiffTable.tsx` — composable PatternFly `Table` with sortable columns, switching to a virtualized body above 100 rows
- `src/pages/SbomComparePage/components/diffColumns.ts` — column definitions and label mappings for each of the six sections
- `src/pages/SbomComparePage/components/DiffSection.test.tsx` — section/table tests

## Implementation Notes
**Section specifications (from Figma, in this order):**

| # | Section | Data source | Columns | Badge color |
|---|---|---|---|---|
| 1 | Added Packages | `added_packages` | Package Name, Version, License, Advisories (count) | green |
| 2 | Removed Packages | `removed_packages` | Package Name, Version, License, Advisories (count) | red |
| 3 | Version Changes | `version_changes` | Package Name, Left Version, Right Version, Direction | blue |
| 4 | New Vulnerabilities | `new_vulnerabilities` | Advisory ID, Severity (`SeverityBadge`), Title, Affected Package | red |
| 5 | Resolved Vulnerabilities | `resolved_vulnerabilities` | Advisory ID, Severity, Title, Previously Affected Package | green |
| 6 | License Changes | `license_changes` | Package Name, Left License, Right License | yellow |

- `ExpandableSection` default expanded when the section has > 0 items, collapsed when 0.
- Tables: PatternFly composable `Table`, sortable columns, **no pagination**; virtualize when rows > 100.

**Data component rendering scope:**
- Each table inside its `ExpandableSection` → **per-context** — render only that section's array (e.g., Added Packages table renders `comparison.added_packages`, New Vulnerabilities renders `comparison.new_vulnerabilities`); do not merge or `flatMap` arrays across sections.
- Count badge in each section header → **per-context** — `comparison.<section_key>.length` for that section only.
- There is no aggregated/summary table in the design.

**Custom sub-component specifications:**
- Count badge: PatternFly `Badge` does not support semantic colors; use PatternFly `Label` (compact, `isCompact`) with `color="green" | "red" | "blue" | "gold"` or a `Badge` styled with PF tokens — green = `--pf-v5-global--success-color--100`, red = `--pf-v5-global--danger-color--100`, blue = `--pf-v5-global--info-color--100`, yellow = `--pf-v5-global--warning-color--100`. Figma supplies color names only (no hex/tokens); these are the nearest PF5 tokens — confirm with design if exact values differ.
- Critical row highlight (New Vulnerabilities): rows whose normalized severity is Critical get a highlighted background — use `--pf-v5-global--danger-color--100` at low emphasis (e.g., PF `Tr` with `isRowSelected`-style background or a class using `--pf-v5-global--palette--red-50`) plus the existing `SeverityBadge`; nearest-token mapping as Figma gives no hex value. Ensure the highlight is not color-only (the `SeverityBadge` text provides the non-color cue).
- Direction cell: PF `Label` with an arrow icon — upgrade = `ArrowUpIcon`, downgrade = `ArrowDownIcon` (no Figma icon specified; nearest PF icons).

**Display text vs API value mismatches:**
- Field `severity` in New/Resolved Vulnerabilities: Figma shows "Critical" (title case, via `SeverityBadge` levels Critical/High/Medium/Low) but the API returns lowercase `"critical"` — **frontend mapping needed**: `{ critical: "Critical", high: "High", medium: "Medium", low: "Low" }`; implement the normalizer in `src/utils/severityUtils.ts` (reuse existing ordering/color mapping there) and handle unknown values with a neutral fallback instead of dropping the row.
- Field `direction` in Version Changes: Figma column "Direction (upgrade/downgrade)", API returns `"upgrade"` / `"downgrade"` — **frontend mapping needed** (case transformation): `{ upgrade: "Upgrade", downgrade: "Downgrade" }`.
- Section titles ("Added Packages", "New Vulnerabilities", …) vs API keys (`added_packages`, `new_vulnerabilities`, …) — **frontend mapping needed**: `{ added_packages: "Added Packages", removed_packages: "Removed Packages", version_changes: "Version Changes", new_vulnerabilities: "New Vulnerabilities", resolved_vulnerabilities: "Resolved Vulnerabilities", license_changes: "License Changes" }` in `diffColumns.ts`.
- Column headers vs fields: "Advisories (count)" ↔ `advisory_count`, "Previously Affected Package" ↔ `previously_affected_package`, "Left/Right Version" ↔ `left_version`/`right_version`, "Left/Right License" ↔ `left_license`/`right_license` — static header labels, no value transformation.
- Package names, versions, licenses, advisory IDs and titles — **no mismatch** (displayed as returned).

**Sorting:** default sort for New Vulnerabilities by severity descending (Critical first) using the ordering in `src/utils/severityUtils.ts`; other tables default to Package Name / Advisory ID ascending.

**Virtualization:** check `package.json` for an existing virtualization library before adding one; prefer the PatternFly virtualized table extension for visual consistency. Only `DiffTable.tsx` should know about virtualization.

**Conventions:**
- Per CONVENTIONS.md §Component library: all UI uses PatternFly 5 equivalents (`ExpandableSection`, `Label`/`Badge`, composable `Table`). Applies: task modifies `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's UI component (`.tsx`) scope.
- Per CONVENTIONS.md §Page structure: page-specific components live in the page's `components/` subdirectory. Applies: task modifies `src/pages/SbomComparePage/components/DiffTable.tsx` matching the convention's `src/pages/<Page>/components/` scope. Example: `src/pages/SbomDetailPage/components/PackageTable.tsx`.
- Per CONVENTIONS.md §Naming: PascalCase components, camelCase utilities. Applies: task modifies `src/pages/SbomComparePage/components/diffColumns.ts` matching the convention's utility naming scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library. Applies: task modifies `src/pages/SbomComparePage/components/DiffSection.test.tsx` matching the convention's unit test scope.

**Project constraints (docs/constraints.md):**
- §2 Commit rules: Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5 Code change rules: scope to listed files; reuse `SeverityBadge`, `severityUtils`, `PackageTable` patterns; doc comments on every test; prefer parameterized tests (`it.each`) for the six sections if sibling tests use them (§5.9/§5.10).

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity badge required by Figma for the Severity column
- `src/utils/severityUtils.ts` — severity ordering and color mapping (sorting, critical detection)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table (columns, sorting) to mirror for package-based sections
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory rendering to mirror for vulnerability sections
- `src/components/EmptyStateCard.tsx` — for the empty body of an expanded zero-item section, if needed

## Acceptance Criteria
- [ ] Six `ExpandableSection`s render in Figma order with titles matching the mapping above
- [ ] Each section header shows a count badge with the specified color and the count of that section's array only
- [ ] Sections with > 0 items are expanded by default; sections with 0 items are collapsed
- [ ] Each table shows exactly the Figma columns for its section and supports column sorting
- [ ] Severity renders via `SeverityBadge` with the API → display mapping applied
- [ ] New Vulnerabilities rows with Critical severity have a highlighted background; non-critical rows do not
- [ ] Direction renders as "Upgrade"/"Downgrade"
- [ ] Tables with > 100 rows render virtualized (only visible rows in the DOM); no pagination controls appear
- [ ] Unknown severity values render with a neutral fallback rather than being dropped

## Test Requirements
- [ ] Test: with the fixture from Task 4, all six sections render with correct titles, counts, and badge colors
- [ ] Test: zero-item section is collapsed; non-empty section is expanded
- [ ] Test: Critical row in New Vulnerabilities has the highlight class/style; a High row does not
- [ ] Test: severity mapping (`"critical"` → "Critical") and direction mapping (`"upgrade"` → "Upgrade")
- [ ] Test: Added Packages table only contains `added_packages` rows (no rows from other sections)
- [ ] Test: with > 100 added packages, the number of rendered rows in the DOM is less than the total
- [ ] Test: clicking a sortable column header reorders rows

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/pages/SbomComparePage` — tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, empty and loading states
