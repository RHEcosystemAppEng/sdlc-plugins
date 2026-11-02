## Repository
catalog-service

## Target Branch
main

## Description
Update both catalog consumer paths to include `ownerGroup` in their output. The summary API and downloadable report read Service Catalog records and must display `ownerGroup` for every record regardless of how that record was populated (registration, scheduled sync, fallback import, or on-demand refresh).

## Files to Modify
- `src/api/catalog_summary.py` — include `ownerGroup` field in summary API response
- `src/reports/catalog_export.py` — include `ownerGroup` field in downloadable report output
- `tests/api/test_catalog_summary.py` — add tests for `ownerGroup` display in summary API, exercising records from each writer
- `tests/reports/test_catalog_export.py` — add tests for `ownerGroup` display in export, exercising records from each writer

## Implementation Notes
- Follow the existing field-inclusion pattern in `src/api/catalog_summary.py` for adding new fields to the API response
- Follow the existing column/field pattern in `src/reports/catalog_export.py` for adding new fields to the report output
- Tests must validate that entries produced by every writer (registration, scheduled sync, fallback import, on-demand refresh) are visible to both consumers. Create test fixtures with records from each writer path and verify `ownerGroup` appears in both the summary API and the export.

## Acceptance Criteria
- [ ] Summary API response includes `ownerGroup` for every catalog record
- [ ] Downloadable report includes `ownerGroup` for every catalog record
- [ ] Records from all four writer paths (registration, scheduled sync, fallback import, on-demand refresh) display `ownerGroup` correctly through both consumers

## Test Requirements
- [ ] Test summary API includes `ownerGroup` for a record created via registration in `tests/api/test_catalog_summary.py`
- [ ] Test summary API includes `ownerGroup` for a record created via scheduled sync in `tests/api/test_catalog_summary.py`
- [ ] Test summary API includes `ownerGroup` for a record created via fallback import in `tests/api/test_catalog_summary.py`
- [ ] Test summary API includes `ownerGroup` for a record created via on-demand refresh in `tests/api/test_catalog_summary.py`
- [ ] Test export includes `ownerGroup` for a record created via registration in `tests/reports/test_catalog_export.py`
- [ ] Test export includes `ownerGroup` for a record created via scheduled sync in `tests/reports/test_catalog_export.py`
- [ ] Test export includes `ownerGroup` for a record created via fallback import in `tests/reports/test_catalog_export.py`
- [ ] Test export includes `ownerGroup` for a record created via on-demand refresh in `tests/reports/test_catalog_export.py`

## Dependencies
- Depends on: Task 1 — Add ownerGroup to catalog store
- Depends on: Task 2 — Update catalog writers
