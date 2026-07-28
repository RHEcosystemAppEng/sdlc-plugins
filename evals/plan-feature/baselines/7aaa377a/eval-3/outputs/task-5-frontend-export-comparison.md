# Task 5 — Add export functionality for comparison results

## Repository
trustify-ui

## Target Branch
main

## Description
Add export functionality to the SBOM comparison page, enabling users to download the comparison results as JSON or CSV files. This supports the compliance documentation workflow (UC-2 from TC-9003) where compliance officers need exportable diff reports. This is a non-MVP enhancement.

## Files to Modify
- `src/pages/SbomComparePage/SbomComparePage.tsx` — wire up the Export dropdown's menu items to trigger JSON and CSV download functions

## Files to Create
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` — PatternFly Dropdown component with "Export JSON" and "Export CSV" menu items, disabled until comparison data is loaded
- `src/utils/exportComparison.ts` — utility functions `exportAsJson(data: SbomComparisonResult)` and `exportAsCsv(data: SbomComparisonResult)` that generate downloadable files

## Implementation Notes
- The Export dropdown in the header toolbar is already scaffolded as a PatternFly `Dropdown` in Task 3 (secondary variant, disabled until comparison result is loaded). This task implements the actual export logic behind the dropdown items.
- **JSON export:** serialize the `SbomComparisonResult` object to formatted JSON, create a Blob, and trigger a browser download with filename `sbom-comparison-{leftId}-{rightId}.json`.
- **CSV export:** flatten the comparison result into CSV rows. Use one CSV section per diff category with a header row per section. Create a Blob and trigger a browser download with filename `sbom-comparison-{leftId}-{rightId}.csv`.
- Use the standard browser download pattern: `URL.createObjectURL(blob)` with a temporary `<a>` element, or the `file-saver` library if already in the project's dependencies.
- The Dropdown should use PatternFly's `Dropdown` component with `DropdownItem` children, following the existing Dropdown patterns in the codebase.

## Reuse Candidates
- `src/pages/SbomComparePage/SbomComparePage.tsx` — the comparison page where the Export dropdown is rendered; check Task 3's scaffolded Dropdown placeholder
- `src/api/models.ts::SbomComparisonResult` — TypeScript interface for the comparison data to be exported

## Acceptance Criteria
- [ ] Export dropdown renders with "Export JSON" and "Export CSV" options
- [ ] Export dropdown is disabled when no comparison result is loaded
- [ ] "Export JSON" downloads a correctly formatted JSON file containing the full comparison result
- [ ] "Export CSV" downloads a CSV file with all diff categories as sections
- [ ] Downloaded files have descriptive filenames including both SBOM IDs
- [ ] Export works for large comparison results (>100 items per category)

## Test Requirements
- [ ] Unit test: ExportDropdown renders with two menu items
- [ ] Unit test: ExportDropdown is disabled when comparison data is null/undefined
- [ ] Unit test: `exportAsJson` produces valid JSON matching the comparison result structure
- [ ] Unit test: `exportAsCsv` produces valid CSV with headers and rows for each diff category
- [ ] Unit test: clicking "Export JSON" triggers a file download

## Dependencies
- Depends on: Task 3 — Build SBOM comparison page with diff sections (export dropdown is integrated into the comparison page)
