## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the Export dropdown to the SBOM comparison page, allowing users to export the comparison diff as JSON or CSV for compliance documentation. This is a non-MVP enhancement referenced in the feature requirements.

## Files to Modify
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Add Export dropdown to the header toolbar

## Files to Create
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` — Export dropdown component with JSON and CSV export options

## Implementation Notes
- **Export dropdown** (from Figma): PatternFly `Dropdown` as a secondary button with two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded.
- **JSON export**: Serialize the `SbomComparisonResult` to a formatted JSON file and trigger a browser download.
- **CSV export**: Flatten the comparison result into CSV rows (one section per block, with a section header row) and trigger a browser download. Include columns appropriate to each diff category.
- **File naming**: Use a descriptive filename pattern like `sbom-comparison-{leftId}-{rightId}.json` or `.csv`.
- **Download mechanism**: Use `URL.createObjectURL()` with a `Blob` to trigger the download without a server round-trip.
- Follow PatternFly `Dropdown` usage patterns consistent with the existing codebase.

## Reuse Candidates
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Parent component where the export dropdown is integrated (from Task 5)

## Acceptance Criteria
- [ ] Export dropdown appears in the header toolbar next to the Compare button
- [ ] Dropdown is disabled when no comparison result is loaded
- [ ] "Export JSON" downloads a properly formatted JSON file
- [ ] "Export CSV" downloads a properly formatted CSV file with all diff categories
- [ ] File names include both SBOM IDs for identification

## Test Requirements
- [ ] Unit test: Export dropdown is disabled when no comparison data exists
- [ ] Unit test: Export dropdown is enabled when comparison data is loaded
- [ ] Unit test: JSON export produces valid JSON matching the comparison result
- [ ] Unit test: CSV export produces valid CSV with expected columns

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Frontend comparison page UI
