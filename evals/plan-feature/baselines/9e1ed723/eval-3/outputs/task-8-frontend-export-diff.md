# Task 8 — Export comparison result as JSON or CSV

**Summary:** Add Export dropdown to download the SBOM diff as JSON or CSV
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
Add the "Export" dropdown from the Figma header toolbar so compliance officers can download the comparison as JSON or CSV (TC-9003 requirement "Export diff as JSON or CSV", marked **non-MVP**). Export is computed client-side from the already-loaded `SbomComparison` — no new backend endpoint is required. Because this requirement is non-MVP, this task can be deprioritized or moved out of the feature branch without affecting MVP delivery; it is planned because the design and data contract fully specify it.

## Files to Modify
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — add the Export `Dropdown` (secondary) with items "Export JSON" and "Export CSV"

## Files to Create
- `src/utils/exportComparison.ts` — pure functions `comparisonToJson(comparison)` and `comparisonToCsv(comparison)`, plus a `downloadFile(content, filename, mimeType)` helper
- `src/utils/exportComparison.test.ts` — unit tests for serialization

## Implementation Notes
- Figma: Export is a PatternFly `Dropdown` (secondary toggle) with two items, **disabled until a comparison result is loaded** (and while loading/error).
- JSON export: the `SbomComparison` object as returned by `GET /api/v2/sbom/compare` (pretty-printed), wrapped with `{ left, right, generated_at, comparison }` metadata so the file is self-describing for compliance records.
- CSV export: single file with a `section` column plus a union of columns (`section,name,version,left_version,right_version,direction,license,left_license,right_license,advisory_count,advisory_id,severity,title,affected_package`). Escape values per RFC 4180 (quote fields containing commas, quotes, or newlines; double embedded quotes). Use the section display labels from `src/pages/SbomComparePage/components/diffColumns.ts` (Task 6) for the `section` column.
- Filename: `sbom-compare-<left>-vs-<right>.<json|csv>`.
- Implement download with `Blob` + `URL.createObjectURL` and revoke the URL afterwards.
- Fail-closed: the Export dropdown must not be enabled (and must not produce an empty file) when the comparison is in an error state — gate on `data !== undefined && !isError` in `CompareToolbar.tsx`.
- Format dates with `src/utils/formatDate.ts` for `generated_at`.

**Conventions:**
- Per CONVENTIONS.md §Component library: Export uses the PatternFly 5 `Dropdown`. Applies: task modifies `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's UI component (`.tsx`) scope.
- Per CONVENTIONS.md §Naming: camelCase for utilities. Applies: task modifies `src/utils/exportComparison.ts` matching the convention's utility naming scope. Example: `src/utils/formatDate.ts`, `src/utils/severityUtils.ts`.
- Per CONVENTIONS.md §Testing: Vitest for unit tests. Applies: task modifies `src/utils/exportComparison.test.ts` matching the convention's unit test scope.

**Project constraints (docs/constraints.md):**
- §2 Commit rules: Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5 Code change rules: scope to listed files; reuse `formatDate` and the section label mapping; doc comments on every test.

## Reuse Candidates
- `src/utils/formatDate.ts` — date formatting for export metadata
- `src/pages/SbomComparePage/components/diffColumns.ts` (Task 6) — section display labels and column definitions
- `src/hooks/useSbomComparison.ts` (Task 4) — source of the loaded comparison data

## Acceptance Criteria
- [ ] Export dropdown with "Export JSON" and "Export CSV" appears in the header toolbar
- [ ] Export is disabled before a comparison is loaded, while loading, and on error
- [ ] "Export JSON" downloads a file containing the full comparison plus `left`, `right`, and `generated_at`
- [ ] "Export CSV" downloads a valid RFC 4180 CSV with one row per diff entry and a `section` column
- [ ] Filenames follow `sbom-compare-<left>-vs-<right>.<ext>`

## Test Requirements
- [ ] Unit test: `comparisonToJson` round-trips the fixture comparison
- [ ] Unit test: `comparisonToCsv` produces the header row and one row per entry across all six sections
- [ ] Unit test: CSV escaping for values with commas, quotes, and newlines
- [ ] Component test: Export disabled with no data and on error; enabled after data loads

## Verification Commands
- `npx vitest run src/utils/exportComparison.test.ts` — tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, empty and loading states
- Depends on: Task 6 — Render collapsible diff sections with tables, critical highlighting, and virtualization
