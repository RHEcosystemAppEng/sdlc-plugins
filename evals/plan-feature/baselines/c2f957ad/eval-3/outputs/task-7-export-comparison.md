# Task 7 — Export comparison as JSON or CSV

**Summary:** Implement "Export JSON" / "Export CSV" for the SBOM comparison (non-MVP)
**Issue type:** Task | **Parent (Epic):** Epic C — TC-9003: Compliance export and documentation
**Labels:** ai-generated-jira | **Priority:** Critical | **Fix Versions:** RHTPA 1.5.0

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Enable the Export dropdown on the comparison page (rendered disabled in Task 5) so compliance officers can download the loaded diff as JSON or CSV for release documentation. Export is client-side from the already-loaded `SbomComparison` data — no new backend endpoint. This requirement is marked **non-MVP** in TC-9003; it can be deferred without blocking the MVP tasks.

## Files to Modify
- `src/pages/SbomComparePage/SbomComparePage.tsx` — wire the Export `Dropdown` items to the export utilities, enabled once a comparison is loaded

## Files to Create
- `src/utils/exportComparison.ts` — `toComparisonJson(comparison, meta)` and `toComparisonCsv(comparison, meta)` plus a `downloadFile(content, filename, mimeType)` helper
- `src/utils/exportComparison.test.ts` — unit tests for serialization

## Implementation Notes
- **Data source:** the `SbomComparison` object already returned by `useSbomComparison` (Task 4) for `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response fields `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes` (trustify-backend `modules/fundamental/src/sbom/model/comparison.rs`). Do not refetch. Verify the contract against the backend repo during implementation using the implement-task cross-repo API verification step.
- **JSON:** pretty-printed API payload wrapped with metadata `{ left: {id, name, version}, right: {id, name, version}, generated_at, comparison }`. Filename: `sbom-compare-<leftName>-vs-<rightName>.json`.
- **CSV:** a single flat file with columns `section,name,version,left_version,right_version,direction,license,left_license,right_license,advisory_id,severity,title,affected_package,advisory_count` — one row per diff item, `section` = the API array key. Escape per RFC 4180 (quote fields containing commas, quotes or newlines). Raw API values (e.g., `critical`, `upgrade`) are exported as-is for machine readability.
- Trigger download via `Blob` + `URL.createObjectURL` + temporary anchor; revoke the object URL afterwards.
- Format timestamps with `src/utils/formatDate.ts`.
- Per CONVENTIONS.md §Naming: utility file and functions in camelCase (`exportComparison.ts`, `toComparisonCsv`).
  Applies: task creates `src/utils/exportComparison.ts` matching the convention's TypeScript (`.ts`) naming scope.
- Per CONVENTIONS.md §Component library: keep the PF5 `Dropdown` with items "Export JSON" and "Export CSV" as specified in Figma.
  Applies: task modifies `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's React component (`.tsx`) scope.
- Per CONVENTIONS.md §Testing: Vitest unit tests for the utilities; RTL test for the dropdown wiring.
  Applies: task creates `src/utils/exportComparison.test.ts` matching the convention's Vitest test scope.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.3 `--base TC-9003`; §5.1–5.4 scope and reuse.

## Reuse Candidates
- `src/utils/formatDate.ts` — date formatting for export metadata/filename
- `src/hooks/useSbomComparison.ts` — source of the loaded diff (Task 4)
- `tests/mocks/fixtures/sbom-comparison.json` — fixture for export tests (Task 4)

## Acceptance Criteria
- [ ] Export dropdown is disabled until a comparison is loaded and enabled afterwards
- [ ] "Export JSON" downloads a JSON file containing both SBOM identifiers and all six diff arrays
- [ ] "Export CSV" downloads a CSV with one row per diff item and a `section` column, correctly escaped
- [ ] Export makes no additional network requests

## Test Requirements
- [ ] Unit: JSON output contains metadata and all six arrays from the fixture
- [ ] Unit: CSV output has the header row and the expected number of rows; values with commas/quotes are escaped
- [ ] Unit: empty comparison exports a header-only CSV and empty arrays in JSON
- [ ] RTL: dropdown disabled before load, enabled after; selecting an item calls the download helper

## Verification Commands
- `npx vitest run src/utils/exportComparison.test.ts` — tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Build SBOM comparison page at /sbom/compare
