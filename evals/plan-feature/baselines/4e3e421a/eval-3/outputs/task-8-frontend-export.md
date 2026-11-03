# Task 8 — Add JSON/CSV export to SBOM comparison page (non-MVP)

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the "Export" dropdown from the Figma header toolbar to the SBOM comparison page (TC-9003). It offers "Export JSON" and "Export CSV" so compliance officers can attach diff reports to release documentation. The feature marks this requirement **non-MVP**; it is planned because the Figma design specifies it fully and it needs no backend change. The export is generated client-side from the `SbomComparison` data the page has already loaded.

## Files to Modify
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — add the Export `Dropdown` with two items
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — tests for export enablement

## Files to Create
- `src/utils/exportComparison.ts` — `toComparisonJson(comparison, meta)` and `toComparisonCsv(comparison, meta)` plus a `downloadFile(content, filename, mime)` helper
- `src/utils/exportComparison.test.ts` — unit tests for serialization

## Implementation Notes
- Figma: the Export button is a secondary PF5 `Dropdown` with the items "Export JSON" and "Export CSV". It is **disabled until a comparison result is loaded**, and also while loading or in an error state.
- JSON export: the `SbomComparison` response plus a `meta` header `{ left: {id, name, version}, right: {id, name, version}, generated_at }`.
- CSV export:
  - Use a single file with columns `category,name,advisory_id,severity,left_value,right_value,license,advisory_count`.
  - Use one row per diff entry. `category` is one of `added_package | removed_package | version_change | new_vulnerability | resolved_vulnerability | license_change`.
  - Escape values per RFC 4180 (quote fields containing commas, quotes, or newlines).
- Use raw API values (e.g., `"critical"`, `"upgrade"`) in exported files, not display labels, so exports stay machine-readable.
- Filename: `sbom-compare-<leftName>-<rightName>.<json|csv>`, sanitized.
- Trigger the download with a `Blob` + object URL. Revoke the URL after the click.
- Put the helper in `src/utils/` with a camelCase file name, following `src/utils/formatDate.ts`.
- Per CONVENTIONS.md §Naming: utilities use camelCase file names. Applies: task creates `src/utils/exportComparison.ts` matching the convention's utility naming scope. Example: `src/utils/severityUtils.ts`.
- Per CONVENTIONS.md §Component library: use the PF5 `Dropdown`. Applies: task modifies `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's React UI component scope. Example: PF components used in `src/components/FilterToolbar.tsx`.
- Per CONVENTIONS.md §Testing: Vitest unit tests. Applies: task creates `src/utils/exportComparison.test.ts` matching the convention's unit test scope. Example: `src/pages/SbomListPage/SbomListPage.test.tsx`.
- Constraints (docs/constraints.md):
  - §2: commit format, Jira footer, `Assisted-by` trailer
  - §3: `gh pr create --base TC-9003`, and post the PR link to Jira
  - §5: scoped changes

## Reuse Candidates
- `src/utils/formatDate.ts` — for the `generated_at` timestamp formatting
- `src/api/models.ts::SbomComparison` (Task 4) — typed input for the serializers

## Acceptance Criteria
- [ ] The Export dropdown is disabled until a comparison has loaded successfully, and also while loading or on error
- [ ] "Export JSON" downloads a JSON file with all six categories and left/right metadata
- [ ] "Export CSV" downloads a CSV with one row per diff entry across all categories, escaped correctly
- [ ] Exported values use raw API values

## Test Requirements
- [ ] Unit test: the JSON serializer includes all categories and metadata
- [ ] Unit test: the CSV serializer emits the header plus one row per entry, and escapes commas and quotes
- [ ] Page test: Export is disabled before load and enabled after the comparison loads

## Verification Commands
- `npx vitest run src/utils/exportComparison.test.ts src/pages/SbomComparePage` — tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page at /sbom/compare
