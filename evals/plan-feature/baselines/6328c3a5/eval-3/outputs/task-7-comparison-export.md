## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add export functionality to the SBOM comparison page, allowing users to download the comparison diff as JSON or CSV for compliance documentation. This is a non-MVP requirement supporting compliance officers who need to document changes between SBOM versions. The export dropdown is integrated into the comparison page header toolbar.

## Files to Create
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` — PatternFly Dropdown with "Export JSON" and "Export CSV" menu items
- `src/utils/exportComparison.ts` — Utility functions: `exportAsJson(data: SbomComparisonResult, filename: string)` and `exportAsCsv(data: SbomComparisonResult, filename: string)`

## Files to Modify
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Integrate ExportDropdown into the header toolbar, disabled until comparison result is loaded

## Implementation Notes
Per CONVENTIONS.md §Component Library: use PatternFly 5 `Dropdown` component for the export menu.
Applies: task creates `src/pages/SbomComparePage/components/ExportDropdown.tsx` matching the convention's `.tsx` component scope.

**Figma design:** The export dropdown is a secondary button in the header toolbar with two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded.

**Export implementation (client-side):**
- JSON export: serialize the `SbomComparisonResult` as formatted JSON and trigger browser download using `Blob` + `URL.createObjectURL` + anchor click
- CSV export: flatten each diff category into rows with a "Category" column (e.g., "Added Package", "Removed Package", "Version Change", "New Vulnerability", "Resolved Vulnerability", "License Change") and category-specific columns. Trigger download using same Blob approach.
- Filename format: `sbom-comparison-{leftId}-{rightId}.json` or `.csv`

**CSV column layout:**
```
Category, Package Name, Version/Left Version, Right Version, License/Left License, Right License, Advisory ID, Severity, Title, Direction
```
Each row populates only the columns relevant to its category; unused columns are empty.

## Reuse Candidates
- `src/utils/formatDate.ts` — existing utility; reference for utility file conventions (camelCase naming, pure functions)

## Acceptance Criteria
- [ ] Export dropdown appears in the comparison page header toolbar
- [ ] Export dropdown is disabled when no comparison result is loaded
- [ ] Export dropdown is enabled when comparison result is available
- [ ] "Export JSON" downloads a valid JSON file containing the full comparison result
- [ ] "Export CSV" downloads a valid CSV file with all diff categories flattened into rows
- [ ] Downloaded files have descriptive filenames including both SBOM IDs

## Test Requirements
- [ ] Unit test: ExportDropdown renders with two menu items
- [ ] Unit test: ExportDropdown is disabled when `data` prop is undefined
- [ ] Unit test: `exportAsJson` produces valid JSON matching the input data
- [ ] Unit test: `exportAsCsv` produces CSV with correct headers and row count matching all diff categories
- [ ] Unit test: `exportAsCsv` handles empty diff categories (zero rows for that category)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Create SBOM comparison page with diff sections (export integrates into the comparison page toolbar)
