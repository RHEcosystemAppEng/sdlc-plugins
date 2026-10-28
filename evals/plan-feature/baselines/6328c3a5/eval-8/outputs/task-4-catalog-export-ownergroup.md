## Repository
catalog-service

## Target Branch
main

## Description
Update the downloadable catalog report in `src/reports/catalog_export.py` to include the `ownerGroup` field when generating the export. After this change, the report will show `ownerGroup` for any Service Catalog record that has the field populated.

Note: The report reads the shared Service Catalog. It will display `ownerGroup` for records that have the value set (currently only those created through the registration workflow). Records populated through excluded paths (scheduled synchronization, fallback import, on-demand refresh) will not have `ownerGroup` until those paths are brought into scope -- see the impact map for the unresolved scope conflict.

## Files to Modify
- `src/reports/catalog_export.py` -- include `ownerGroup` in the report output when reading catalog records
- `tests/reports/test_catalog_export.py` -- add tests verifying `ownerGroup` appears in the exported report

## Implementation Notes
- Inspect `src/reports/catalog_export.py` to understand the report generation format (CSV, JSON, PDF, etc.) and how catalog record fields are included.
- Add `ownerGroup` as a column or field in the report output. Follow the existing field inclusion pattern.
- Inspect existing tests in `tests/reports/test_catalog_export.py` to follow the established test patterns for report content assertions.

## Acceptance Criteria
- [ ] The downloadable report includes `ownerGroup` for catalog records that have the field set
- [ ] The report handles records without `ownerGroup` gracefully (e.g., shows empty cell or omits the field)
- [ ] Existing report content and format for other fields remain unchanged

## Test Requirements
- [ ] Test that the exported report includes `ownerGroup` for a record that has it set
- [ ] Test that the report handles a record without `ownerGroup` without error
- [ ] Test that existing report fields and format are not affected

## Dependencies
- Depends on: Task 1 -- Add ownerGroup field to catalog record schema
