# Task 8 — Add Export JSON / CSV dropdown to comparison view (non-MVP)

**Summary:** Add Export dropdown (JSON, CSV) to the SBOM comparison toolbar
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
Let compliance users export the loaded comparison as a JSON or CSV file for documentation. TC-9003 lists this requirement as **non-MVP**. It is planned as a separate, independently mergeable task because the Figma design already specifies the control. The work is entirely client-side: the export serializes the `SbomComparison` already loaded by `useSbomComparison`, so no backend change is needed. This task can be deprioritized or moved out of the feature branch without affecting the MVP tasks.

## Files to Modify
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — add the "Export" PF5 `Dropdown` with the items "Export JSON" and "Export CSV"
- `src/pages/SbomComparePage/SbomComparePage.tsx` — pass the loaded comparison and the selected SBOM names to the toolbar

## Files to Create
- `src/utils/exportComparison.ts` — `toComparisonJson(comparison, meta)`, `toComparisonCsv(comparison, meta)`, and `downloadFile(content, filename, mimeType)`
- `src/utils/exportComparison.test.ts` — unit tests for serialization

## Implementation Notes
- **Figma (Header Toolbar).** The "Export" control is a secondary dropdown with two items, "Export JSON" and "Export CSV". It is disabled until a comparison result has loaded, and also disabled while loading or on error.
- **JSON export.** Pretty-print the `SbomComparison` object, wrapped as `{ left: {id, name, version}, right: {id, name, version}, generated_at, diff: <SbomComparison> }`. Filename: `sbom-compare-<leftName>-vs-<rightName>.json`.
- **CSV export.**
  - Produce a single CSV with a leading `category` column (`added_package`, `removed_package`, `version_change`, `new_vulnerability`, `resolved_vulnerability`, `license_change`).
  - Use a superset of columns: `name, version, left_version, right_version, direction, license, left_license, right_license, advisory_id, severity, title, affected_package, advisory_count`. Leave inapplicable columns empty.
  - Escape values per RFC 4180 (quote fields containing commas, quotes, or newlines).
  - Prefix values beginning with `=`, `+`, `-`, or `@` with `'` to prevent CSV formula injection.
- **Download.** Use `Blob` + `URL.createObjectURL` + a temporary anchor, and call `URL.revokeObjectURL` afterwards. Do not use `window.location`.
- **Utility placement.** Check `src/utils/` first. Only `formatDate.ts` and `severityUtils.ts` exist, so there is no existing CSV helper to reuse. Use `formatDate.ts` for the `generated_at` timestamp format.
- Per CONVENTIONS.md §Naming: camelCase for utilities (`exportComparison.ts`).
  Applies: task creates `src/utils/exportComparison.ts` matching the convention's utility naming scope.
- Per CONVENTIONS.md §Component library: use the PF5 `Dropdown` / `DropdownItem` / `MenuToggle` for the Export control.
  Applies: task modifies `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's `.tsx` UI component scope.
- Per CONVENTIONS.md §Testing: Vitest unit tests for the utility.
  Applies: task creates `src/utils/exportComparison.test.ts` matching the convention's unit-test scope.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits format, a `Implements TC-<task-key>` footer, and an `Assisted-by:` trailer.
  - §3 PR rules: use `--base TC-9003` and post the PR link on the Jira task.
  - §5 Code change rules: stay within the listed files; inspect before modifying.
  - §1.4/§1.5: no unrelated refactoring.

## Reuse Candidates
- `src/utils/formatDate.ts` — existing date formatting; reuse it for the export timestamp and filename
- `src/hooks/useSbomComparison.ts` — added in Task 4; the export reads its cached data and makes no second request
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — added in Task 5; extend it in place

## Acceptance Criteria
- [ ] The Export dropdown is disabled until a comparison result has loaded, and while loading or on error
- [ ] "Export JSON" downloads a `.json` file containing the left and right SBOM metadata and the full diff
- [ ] "Export CSV" downloads a `.csv` file with one row per diff entry and a `category` column
- [ ] CSV values containing commas, quotes, or newlines are escaped correctly; values starting with `=`, `+`, `-`, or `@` are neutralized
- [ ] Export makes no additional network request

## Test Requirements
- [ ] Unit test: `toComparisonJson` output parses back to an object that deep-equals the input diff
- [ ] Unit test: `toComparisonCsv` emits a header row plus one row per entry across all six categories, with the correct `category` values
- [ ] Unit test: escaping of commas, quotes, and newlines, and formula-injection prefixing
- [ ] Component test: the Export dropdown is disabled before results load and enabled after

## Verification Commands
- `npx vitest run src/utils/exportComparison.test.ts src/pages/SbomComparePage` — all tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add /sbom/compare page with SBOM selectors, Compare button, URL-shareable state, empty and loading states
