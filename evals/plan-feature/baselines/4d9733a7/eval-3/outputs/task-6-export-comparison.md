## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add export functionality to the SBOM comparison page. Users can export the comparison results as JSON or CSV format for compliance documentation. The Figma design shows an "Export" dropdown (PatternFly Dropdown) with two options: "Export JSON" and "Export CSV". The export button is disabled until a comparison result is loaded.

## Files to Create
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` -- Export dropdown component with JSON and CSV export options
- `src/utils/comparisonExport.ts` -- Utility functions to convert SbomComparisonResult to JSON string and CSV string for download

## Files to Modify
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- Add ExportDropdown to the header toolbar, pass comparison data

## Implementation Notes
- Use PatternFly `Dropdown` component for the export menu with two items: "Export JSON" and "Export CSV".
- The dropdown should be disabled when no comparison result is loaded (no data to export).
- **JSON export**: serialize the SbomComparisonResult as formatted JSON and trigger a browser download with filename `sbom-comparison-{leftId}-{rightId}.json`.
- **CSV export**: flatten the comparison result into CSV rows with a category column, then trigger download with filename `sbom-comparison-{leftId}-{rightId}.csv`. Use a structure like: `category,name,version,left_value,right_value,details`.
- Use the browser `Blob` API and `URL.createObjectURL()` for file downloads -- no backend endpoint needed.
- Per CONVENTIONS.md: use camelCase for utility function names (e.g., `exportAsJson`, `exportAsCsv`).
  Applies: task creates `src/utils/comparisonExport.ts` matching the convention's TypeScript utility scope.
- Per CONVENTIONS.md: use PascalCase for the component name (ExportDropdown).
  Applies: task creates `src/pages/SbomComparePage/components/ExportDropdown.tsx` matching the convention's TypeScript component scope.

## Reuse Candidates
- `src/utils/formatDate.ts` -- existing utility module; follow the same export pattern and naming conventions
- `src/utils/severityUtils.ts` -- existing utility module; reference for utility function structure

## Acceptance Criteria
- [ ] Export dropdown appears in the comparison page header toolbar next to the Compare button
- [ ] Export dropdown is disabled when no comparison result is loaded
- [ ] "Export JSON" triggers a browser download of the comparison result as formatted JSON
- [ ] "Export CSV" triggers a browser download of the comparison result as CSV with all diff categories
- [ ] Downloaded files use the naming convention sbom-comparison-{leftId}-{rightId}.{ext}

## Test Requirements
- [ ] Unit test: ExportDropdown renders disabled state when no data is provided
- [ ] Unit test: ExportDropdown renders enabled state when comparison data is provided
- [ ] Unit test: exportAsJson produces valid JSON matching the comparison result structure
- [ ] Unit test: exportAsCsv produces valid CSV with correct headers and rows for each diff category

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
