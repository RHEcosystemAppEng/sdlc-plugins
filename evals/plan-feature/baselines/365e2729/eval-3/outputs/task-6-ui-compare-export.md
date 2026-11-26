## Repository
trustify-ui

## Target Branch
main

## Description
Implement the "Export" dropdown on the SBOM comparison page (TC-9003, non-MVP requirement "Export diff as JSON or CSV" for compliance documentation). "Export JSON" downloads the loaded `SbomComparison` as a `.json` file; "Export CSV" downloads a flat CSV with one row per diff entry and a `category` column. Export is performed client-side from the already-loaded comparison data — no new backend endpoint is required.

## Files to Modify
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — enable the Export `Dropdown` once a comparison result is loaded and wire its items to the export functions
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — export tests

## Files to Create
- `src/utils/exportComparison.ts` — `toComparisonJson(comparison)`, `toComparisonCsv(comparison)`, `downloadFile(content, filename, mimeType)`
- `src/utils/exportComparison.test.ts` — unit tests for serialization and CSV escaping

## Implementation Notes
- **Figma:** "Export" is a secondary PF5 `Dropdown` in the header toolbar with two `DropdownItem`s: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded (and while loading).
- File name: `sbom-compare-${leftId}-${rightId}.json|csv`.
- CSV columns: `category,name,version,left_version,right_version,direction,license,left_license,right_license,advisory_id,severity,title,affected_package,advisory_count`; one row per entry across all six arrays with `category` ∈ `added_package|removed_package|version_change|new_vulnerability|resolved_vulnerability|license_change`. Escape quotes, commas and newlines per RFC 4180. Use raw API values (e.g., lowercase `critical`) in exports — exports are data, not display.
- `downloadFile` uses `Blob` + `URL.createObjectURL` + a temporary anchor, then `URL.revokeObjectURL`.
- Data scope: export is **aggregated** — combines all six per-section arrays from the single loaded `SbomComparison` (the only aggregated view on the page).
- Place helpers alongside existing utilities like `src/utils/formatDate.ts`.
- **Per CONVENTIONS.md §Naming:** utility file is camelCase (`exportComparison.ts`), consistent with `src/utils/severityUtils.ts`.
  Applies: task modifies src/utils/exportComparison.ts matching the convention's TypeScript utilities naming scope.
- **Per CONVENTIONS.md §Component library:** use PF5 `Dropdown`/`MenuToggle`/`DropdownItem` for the export control.
  Applies: task modifies src/pages/SbomComparePage/components/CompareToolbar.tsx matching the convention's React `.tsx` UI component scope.
- **Per CONVENTIONS.md §Testing:** Vitest unit tests for the utility, RTL for the dropdown interaction.
  Applies: task modifies src/utils/exportComparison.test.ts matching the convention's Vitest `.test.ts` scope.
- **Constraints (docs/constraints.md):** §2 commits (Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer); §3 PRs (`--base main`, PR link on Jira task); §5 code changes (scoped files, inspect first, no duplication); §1.4/1.5 implement-task scope rules.

## Reuse Candidates
- `src/hooks/useSbomComparison.ts` (Task 3) — source of the loaded comparison (from React Query cache; do not refetch for export)
- `src/utils/formatDate.ts` — utility module pattern to follow

## Acceptance Criteria
- [ ] Export dropdown is disabled with no comparison loaded and while loading; enabled once data is loaded
- [ ] "Export JSON" downloads a file whose parsed content equals the API response
- [ ] "Export CSV" downloads a CSV with the header row and one row per diff entry across all six categories
- [ ] CSV values containing commas, quotes or newlines are correctly escaped
- [ ] Export of an empty comparison produces a valid JSON object with six empty arrays / a CSV with only the header row

## Test Requirements
- [ ] Unit test: `toComparisonJson` round-trips the fixture
- [ ] Unit test: `toComparisonCsv` row count equals total entries; escaping of special characters
- [ ] RTL test: dropdown disabled before load, enabled after; clicking "Export CSV" calls `downloadFile` with the expected filename and MIME type `text/csv`

## Verification Commands
- `npx vitest run src/utils/exportComparison.test.ts` — utility tests pass

## Dependencies
- Depends on: Task 4 — Build SBOM comparison page at /sbom/compare
