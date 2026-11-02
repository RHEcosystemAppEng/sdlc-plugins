## Repository
catalog-service

## Target Branch
main

## Description
Update the two catalog consumers — the summary API (`src/api/catalog_summary.py`) and the downloadable report (`src/reports/catalog_export.py`) — to include the `ownerGroup` field in their output. Both consumers read shared Service Catalog records and should display the field for records from any population path, though the in-scope testing covers records created via registration only.

**Note:** This task validates display for records created via registration. Records from excluded population paths (scheduled sync, fallback import, on-demand refresh) are out of scope per stakeholder instruction and may not have `ownerGroup` set — see the unresolved scope conflict in the impact map.

## Files to Modify
- `src/api/catalog_summary.py` — include `ownerGroup` in the summary API response
- `src/reports/catalog_export.py` — include `ownerGroup` in the downloadable report output
- `tests/api/test_catalog_summary.py` — add tests verifying `ownerGroup` appears in the summary API response
- `tests/reports/test_catalog_export.py` — add tests verifying `ownerGroup` appears in the report output

## Implementation Notes
- Review `src/api/catalog_summary.py` to identify how catalog records are serialized for the API response and add `ownerGroup` to the output shape.
- Review `src/reports/catalog_export.py` to identify how catalog records are formatted for the downloadable report and add `ownerGroup` to the export format.
- Tests should create records via registration (the in-scope writer) and verify display through both consumers.

## Acceptance Criteria
- [ ] Summary API response includes `ownerGroup` for catalog records
- [ ] Downloadable report includes `ownerGroup` for catalog records
- [ ] Both consumers display `ownerGroup` for records created via registration

## Test Requirements
- [ ] Test that the summary API response includes `ownerGroup` for a record created via registration
- [ ] Test that the downloadable report includes `ownerGroup` for a record created via registration
- [ ] Test that both consumers handle records without `ownerGroup` gracefully (backward compatibility for pre-existing records)

## Dependencies
- Depends on: Task 1 — Add ownerGroup to catalog store
- Depends on: Task 2 — Capture ownerGroup in registration
