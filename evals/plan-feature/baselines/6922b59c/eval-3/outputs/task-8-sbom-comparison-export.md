## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the export functionality on the SBOM comparison page. Users can export the comparison result as JSON or CSV for compliance documentation. This is a non-MVP requirement that supports compliance officers who need to attach structured diff reports to release documentation.

## Files to Modify
- `src/pages/SbomComparePage/SbomComparePage.tsx` — wire up the Export dropdown with handler functions for JSON and CSV export

## Files to Create
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` — export dropdown component with JSON and CSV options
- `src/utils/exportComparison.ts` — utility functions for converting SbomComparisonResult to JSON download and CSV download

## Implementation Notes
- **Figma design reference:** The Export dropdown is a PatternFly `Dropdown` button positioned in the header toolbar next to the Compare button. It contains two items: "Export JSON" and "Export CSV". The dropdown is disabled until a comparison result is loaded.
- Per CONVENTIONS.md §Naming: use camelCase for utilities. Applies: task creates `src/utils/exportComparison.ts` matching the convention's utility file scope. See `src/utils/formatDate.ts` for the established pattern.
- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents. Applies: task creates `src/pages/SbomComparePage/components/ExportDropdown.tsx` matching the convention's TypeScript component scope.
- **JSON export:** Serialize the `SbomComparisonResult` data as a formatted JSON file and trigger a browser download using `URL.createObjectURL` and a temporary anchor element.
- **CSV export:** Flatten the comparison result into a single CSV with columns: Category, Package Name, Version/Left Version/Right Version, License, Advisory Info. Each row is prefixed with its diff category (Added, Removed, Version Change, New Vulnerability, Resolved Vulnerability, License Change).
- Follow the existing utility pattern in `src/utils/formatDate.ts` and `src/utils/severityUtils.ts` for the export utility module — export pure functions that transform data.
- The PatternFly `Dropdown` component should use `onSelect` to dispatch the appropriate export function.
- File naming convention for downloads: `sbom-comparison-{leftId}-vs-{rightId}.{json|csv}`.

## Reuse Candidates
- `src/utils/formatDate.ts` — reference for utility function pattern
- `src/utils/severityUtils.ts` — reference for utility function pattern
- `src/pages/SbomComparePage/SbomComparePage.tsx` — the page being modified; the Export dropdown placeholder should already exist from Task 6

## Acceptance Criteria
- [ ] Export dropdown renders in the comparison page header toolbar
- [ ] Export dropdown is disabled when no comparison result is loaded
- [ ] Clicking "Export JSON" triggers a JSON file download of the comparison result
- [ ] Clicking "Export CSV" triggers a CSV file download with all diff categories
- [ ] Downloaded JSON file contains the full SbomComparisonResult data
- [ ] Downloaded CSV file has correct headers and data for all diff categories
- [ ] File names follow the convention `sbom-comparison-{leftId}-vs-{rightId}.{json|csv}`

## Test Requirements
- [ ] Unit test for `exportComparison.ts`: JSON export produces valid JSON matching the input data
- [ ] Unit test for `exportComparison.ts`: CSV export produces correct headers and row data for each diff category
- [ ] Unit test: Export dropdown is disabled when comparison data is not loaded
- [ ] Unit test: Export dropdown is enabled when comparison data is loaded

## Verification Commands
- `npx tsc --noEmit` — TypeScript compiles without errors
- `npx vitest run src/utils/exportComparison` — export utility tests pass
- `npx vitest run src/pages/SbomComparePage` — page tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Build SBOM comparison page UI
