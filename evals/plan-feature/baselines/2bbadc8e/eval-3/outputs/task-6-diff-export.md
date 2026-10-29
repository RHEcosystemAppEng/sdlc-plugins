## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add diff export functionality to the SBOM comparison page, enabling users to export the comparison result as JSON or CSV for compliance documentation. This is a non-MVP requirement. The export operates on the comparison data already loaded in the browser — no new backend endpoint is needed. The Export dropdown is enabled only after a comparison result is loaded.

## Files to Create
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` — Export dropdown component with JSON and CSV export options
- `src/utils/exportComparison.ts` — utility functions for serializing SbomComparison data to JSON and CSV formats

## Files to Modify
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — replace disabled Export dropdown placeholder with the functional ExportDropdown component

## Implementation Notes
**Figma design reference (from figma-context.md):**
- "Export" dropdown: PatternFly `Dropdown` (secondary button style) with two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded.

**Export formats:**
- **JSON export:** serialize the `SbomComparison` object as formatted JSON and trigger a browser download as `sbom-comparison-{leftId}-{rightId}.json`
- **CSV export:** flatten the comparison data into rows with columns: Category, Package Name, Version/Left Version/Right Version, License, Advisory ID, Severity, Direction. Trigger a browser download as `sbom-comparison-{leftId}-{rightId}.csv`

Use the browser `Blob` API and `URL.createObjectURL` for triggering downloads without a server round-trip.

Per CONVENTIONS.md: use PatternFly 5 `Dropdown` component; use camelCase for utility function names.
Applies: task creates `src/utils/exportComparison.ts` matching the convention's `.ts` utility file scope.

## Reuse Candidates
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — toolbar created in Task 5; modify to integrate the export dropdown
- `src/utils/formatDate.ts` — existing utility module; follow its pattern for the export utility module

## Acceptance Criteria
- [ ] Export dropdown renders in the comparison toolbar as a PatternFly `Dropdown`
- [ ] Export dropdown is disabled when no comparison result is loaded
- [ ] Export dropdown is enabled after a comparison result is displayed
- [ ] Clicking "Export JSON" triggers a browser download of the comparison as formatted JSON
- [ ] Clicking "Export CSV" triggers a browser download of the comparison as CSV with appropriate column headers
- [ ] Downloaded files are named `sbom-comparison-{leftId}-{rightId}.json` and `.csv` respectively

## Test Requirements
- [ ] Unit test: Export dropdown is disabled when no comparison data is available
- [ ] Unit test: Export dropdown is enabled when comparison data is present
- [ ] Unit test: JSON export produces valid JSON containing all six diff categories
- [ ] Unit test: CSV export produces valid CSV with headers and flattened rows
- [ ] Unit test: export utility functions handle empty comparison results (all categories empty)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Create SBOM comparison page with diff sections
