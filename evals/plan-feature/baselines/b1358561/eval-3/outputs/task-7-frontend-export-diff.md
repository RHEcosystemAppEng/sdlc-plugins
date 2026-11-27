# Task 7 — Export comparison as JSON or CSV (non-MVP)

**Summary:** TC-9003: Export SBOM comparison as JSON or CSV
**Issue type:** Task
**Parent (Epic):** Epic 3 — TC-9003: Comparison export
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
main

## Description
Implement the "Export" dropdown from the Figma header toolbar so compliance officers can save a
comparison for documentation (TC-9003 requirement "Export diff as JSON or CSV" — marked
**non-MVP** in the Feature; can be scheduled after the MVP tasks). Export is client-side from
the already-loaded `SbomComparison` — no backend change is required.

## Files to Modify
- `src/pages/sbom-compare-page/SbomComparePage.tsx` — add the Export `Dropdown` to the header toolbar

## Files to Create
- `src/pages/sbom-compare-page/components/ExportDropdown.tsx` — PatternFly `Dropdown` with items "Export JSON" and "Export CSV"
- `src/utils/exportComparison.ts` — `comparisonToJson(comparison)`, `comparisonToCsv(comparison)` and a `downloadFile(content, filename, mimeType)` helper
- `src/utils/exportComparison.test.ts` — unit tests for serialization

## Implementation Notes
- Figma: "Export" is a secondary `Dropdown` with two items, disabled until a comparison result is loaded (and while loading).
- JSON export: the `SbomComparison` object as returned by the API, pretty-printed, plus a header object `{ left: {id, name, version}, right: {id, name, version}, generated_at }` for compliance traceability.
- CSV export: a single flat CSV with a leading `category` column (`added_package`, `removed_package`, `version_change`, `new_vulnerability`, `resolved_vulnerability`, `license_change`) and the union of item columns; escape values per RFC 4180 (quotes, commas, newlines). This is an **aggregated** view across all six categories by design (export, not on-screen rendering).
- Filename: `sbom-compare-<leftName>-<leftVersion>-vs-<rightName>-<rightVersion>.(json|csv)`.
- Download via `Blob` + `URL.createObjectURL` + temporary anchor; revoke the object URL afterwards.
- Per CONVENTIONS.md §Naming: camelCase utilities (`exportComparison.ts`), PascalCase components (`ExportDropdown.tsx`).
  Applies: task creates `src/utils/exportComparison.ts` matching the convention's utility `.ts` naming scope.
- Per CONVENTIONS.md §Component library: use PF5 `Dropdown`, `DropdownItem`, `MenuToggle`.
  Applies: task creates `src/pages/sbom-compare-page/components/ExportDropdown.tsx` matching the convention's React `.tsx` component scope.
- Constraints (docs/constraints.md): §5.1 scope; §2.1–2.3 commit rules; §3.3 PR `--base main`.

## Reuse Candidates
- `src/utils/formatDate.ts` — `generated_at` timestamp formatting
- `src/api/models.ts::SbomComparison` — types from Task 3

## Acceptance Criteria
- [ ] The Export dropdown is disabled until a comparison has loaded
- [ ] "Export JSON" downloads a JSON file containing all six categories plus left/right SBOM identifiers
- [ ] "Export CSV" downloads a CSV with one row per diff item and a `category` column; values with commas/quotes/newlines are correctly escaped
- [ ] Exported content matches the comparison displayed on screen

## Test Requirements
- [ ] Unit test: `comparisonToJson` output round-trips to the input comparison
- [ ] Unit test: `comparisonToCsv` produces correct header and row counts per category and escapes special characters
- [ ] Component test: dropdown disabled with no data, enabled with data; selecting an item calls the download helper

## Dependencies
- Depends on: Task 5 — Render collapsible diff sections, count badges and critical highlighting
