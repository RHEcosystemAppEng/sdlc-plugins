## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the client-side export functionality for SBOM comparison results. The Export dropdown in the comparison page toolbar allows users to download the comparison diff as JSON or CSV for compliance documentation. This is a non-MVP feature that supports compliance workflows requiring documented change records between SBOM releases.

## Files to Create
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` -- Export dropdown component with JSON and CSV download options
- `src/utils/exportComparison.ts` -- Utility functions to convert comparison data to JSON string and CSV format, and trigger browser download

## Files to Modify
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` -- Replace disabled Export dropdown stub with functional ExportDropdown component

## Implementation Notes
- Use PatternFly `Dropdown` component for the Export button with two items: "Export JSON" and "Export CSV".
- Dropdown should be disabled until comparison results are loaded (check for non-null comparison data).
- **JSON export:** serialize the `SbomComparisonResult` directly using `JSON.stringify(data, null, 2)` with indentation, trigger browser download with `application/json` MIME type.
- **CSV export:** flatten the comparison result into a CSV format with a category column. Example structure:
  ```csv
  Category,Package Name,Version,License,Advisory Count,Left Version,Right Version,Direction,Advisory ID,Severity,Title
  Added Package,pkg-name,1.0.0,MIT,0,,,,,,
  Removed Package,old-pkg,2.0.0,Apache-2.0,1,,,,,,
  Version Change,shared-pkg,,,,,1.0.0,2.0.0,upgrade,,,
  New Vulnerability,,,,,,,,CVE-2024-001,critical,Buffer overflow
  ```
- Use `Blob` and `URL.createObjectURL` for client-side download (no server round-trip needed). Revoke the object URL after download.
- File names should include both SBOM identifiers: `sbom-comparison-{left-id}-vs-{right-id}.json` and `.csv`.
- Per CONVENTIONS.md (Key Conventions) -- Naming: camelCase for utilities. Applies: task creates `src/utils/exportComparison.ts` matching the convention's naming scope.
- Per docs/constraints.md SS2: commit must reference TC-9003 in footer.

## Reuse Candidates
- `src/utils/formatDate.ts` -- utility function pattern reference for new utility file structure

## Acceptance Criteria
- [ ] Export dropdown renders in the comparison toolbar with "Export JSON" and "Export CSV" items
- [ ] Dropdown is disabled when no comparison results are loaded
- [ ] "Export JSON" triggers download of a valid JSON file containing the full comparison result
- [ ] "Export CSV" triggers download of a correctly formatted CSV file with all diff categories
- [ ] Downloaded files have descriptive names including both SBOM identifiers
- [ ] JSON export contains the full comparison result with proper 2-space indented formatting
- [ ] CSV export contains all six diff categories in a flat, readable format

## Test Requirements
- [ ] Test JSON export produces valid JSON matching the comparison result structure
- [ ] Test CSV export produces correctly formatted CSV with all six categories
- [ ] Test export dropdown is disabled without comparison data
- [ ] Test file download is triggered with correct MIME type and filename

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 6 -- Implement SBOM comparison page with diff sections
