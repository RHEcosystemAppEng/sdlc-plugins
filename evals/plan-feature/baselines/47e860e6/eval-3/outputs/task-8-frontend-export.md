# Task 8 — Frontend: export comparison as JSON / CSV (non-MVP)

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the "Export" dropdown on the SBOM comparison page (TC-9003) so compliance users can download the loaded diff as JSON or CSV. The Feature marks this requirement as **non-MVP**, but the Figma design specifies it, so it can be planned. The export is built client-side from the already-loaded `SbomComparison` and needs no backend change. It can be deprioritized or deferred without affecting the MVP tasks.

## Files to Modify
- `src/pages/SbomComparePage/components/CompareToolbar.tsx`: wire the "Export JSON" and "Export CSV" dropdown items to the export utility, enabled only when a comparison result is loaded

## Files to Create
- `src/utils/exportComparison.ts`: `toComparisonJson(comparison)`, `toComparisonCsv(comparison)` and `downloadFile(content, filename, mimeType)` helpers
- `src/utils/exportComparison.test.ts`: unit tests for serialization

## Implementation Notes
- JSON: `JSON.stringify(comparison, null, 2)`, which matches the API shape exactly.
- CSV: a single flat file with a `category` column (`added_package`, `removed_package`, `version_change`, `new_vulnerability`, `resolved_vulnerability`, `license_change`) plus the union of columns (`name`, `version`, `left_version`, `right_version`, `direction`, `license`, `left_license`, `right_license`, `advisory_count`, `advisory_id`, `severity`, `title`, `affected_package`). Escape fields per RFC 4180: quote values containing commas, quotes or newlines, and double any embedded quotes.
- Filename: `sbom-compare-<left>-vs-<right>.(json|csv)`.
- Download via `Blob` and `URL.createObjectURL` with a temporary anchor, then revoke the URL.
- Per CONVENTIONS.md §Naming: use a camelCase utility file and functions (`exportComparison.ts`), following `src/utils/formatDate.ts`.
  Applies: task creates `src/utils/exportComparison.ts` matching the convention's utilities (`src/utils/*.ts`) naming scope.
- Per CONVENTIONS.md §Component library: the Export control is a PF5 `Dropdown` with two `DropdownItem`s.
  Applies: task modifies `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's UI component (`.tsx`) scope.
- Per CONVENTIONS.md §Testing: Vitest unit tests for the utility.
  Applies: task creates `src/utils/exportComparison.test.ts` matching the convention's Vitest unit test scope.
- Constraints (docs/constraints.md): §1.4/§5.1 scope to the listed files; §5.2 inspect `CompareToolbar.tsx` (from Task 6) before changing; §2.1–2.3 commit format; §3.3 open the PR with `--base TC-9003`.

## Reuse Candidates
- `src/utils/formatDate.ts`: utility module pattern
- `tests/mocks/fixtures/sbom-comparison.json` (Task 4): fixture input for the serialization tests

## Acceptance Criteria
- [ ] The Export dropdown is disabled until a comparison is loaded
- [ ] "Export JSON" downloads a file whose content equals the loaded `SbomComparison` JSON
- [ ] "Export CSV" downloads a CSV with one row per diff entry and a `category` column covering all six categories
- [ ] CSV values containing commas, quotes or newlines are correctly escaped

## Test Requirements
- [ ] Unit test: `toComparisonJson` round-trips the fixture
- [ ] Unit test: `toComparisonCsv` produces a header plus the expected row count across all categories
- [ ] Unit test: a license value containing a comma and a quote is escaped per RFC 4180
- [ ] Component test: Export items are disabled before load and trigger a download after load

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Frontend: SBOM comparison page and /sbom/compare route
