## Repository
catalog-service

## Target Branch
main

## Description
Display the `ownerGroup` field in the catalog summary API and the downloadable report. Both are consumers of the shared Service Catalog record. The summary API (`catalog_summary.py`) and the export report (`catalog_export.py`) must read and present the `ownerGroup` field from catalog records.

Note: the acceptance criterion states that `ownerGroup` should be displayed "regardless of how that record was populated." This task implements the display side, which will show `ownerGroup` for any record that has the field set. However, per the unresolved scope conflict in the impact map, only the registration path (Task 2) currently sets `ownerGroup` — records from other population paths may display `None`/`null` until those paths are updated.

## Files to Modify
- `src/api/catalog_summary.py` — include `ownerGroup` in the summary API response
- `src/reports/catalog_export.py` — include `ownerGroup` in the downloadable report output
- `tests/api/test_catalog_summary.py` — add tests for `ownerGroup` display in summary API
- `tests/reports/test_catalog_export.py` — add tests for `ownerGroup` display in the report

## API Changes
- `GET /api/catalog/summary` (or equivalent summary endpoint) — MODIFY: response includes `ownerGroup` field for each service record

## Implementation Notes
- Inspect `src/api/catalog_summary.py` to see how catalog records are read and serialized for the API response. Add `ownerGroup` to the response shape following the existing field pattern.
- Inspect `src/reports/catalog_export.py` to see how catalog records are formatted for the downloadable report. Add `ownerGroup` as a column or field in the report output, following the existing field pattern.
- Both files are readers of the shared catalog record — they should access `ownerGroup` via the same record interface used for other fields.
- Handle the case where `ownerGroup` is `None`/`null` gracefully in both the API response and the report (e.g., display as empty or "N/A").

## Acceptance Criteria
- [ ] The summary API response includes `ownerGroup` for each catalog record
- [ ] The downloadable report includes `ownerGroup` for each catalog record
- [ ] Records with `ownerGroup` set display the correct value in both the API and the report
- [ ] Records without `ownerGroup` (value is `None`/`null`) are handled gracefully in both outputs

## Test Requirements
- [ ] Test that the summary API response includes `ownerGroup` for a record that has it set
- [ ] Test that the summary API response handles a record with `ownerGroup` as `None`/`null`
- [ ] Test that the downloadable report includes `ownerGroup` for a record that has it set
- [ ] Test that the downloadable report handles a record with `ownerGroup` as `None`/`null`

## Dependencies
- Depends on: Task 1 — Add ownerGroup field to catalog record schema
