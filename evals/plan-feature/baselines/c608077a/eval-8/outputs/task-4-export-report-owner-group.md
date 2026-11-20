# Task 4 — Include ownerGroup in the downloadable catalog report

**Epic:** TC-9007: Owner group display
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` column/field to the downloadable catalog report, read from the shared Service Catalog record (TC-9007, Requirement 2).

Scope note: the report will show whatever `ownerGroup` the shared record holds. Records populated by scheduled sync, fallback import, or on-demand refresh are not guaranteed a value, because those writers are excluded by stakeholder instruction and recorded as unresolved in the TC-9007 impact map. Feature AC2 is therefore not fully satisfied by this task alone.

## Files to Modify
- `src/reports/catalog_export.py` — add `ownerGroup` to the exported record columns
- `tests/reports/test_catalog_export.py` — add tests for the new column

## Implementation Notes
- Read `ownerGroup` from records returned by the existing read helpers in `src/catalog/store.py`.
- Add the column at the end of the existing column order so downstream consumers that rely on column position keep working.
- Records with no stored value export an empty cell/value. Do not skip the record or fail the export.
- Keep the field naming consistent with the summary API (Task 3): `ownerGroup`.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules.

## Reuse Candidates
- `src/catalog/store.py` — record read helpers (Task 1)
- `src/reports/catalog_export.py` — existing column/field definition and row serialization. Extend them in place.

## Acceptance Criteria
- [ ] The downloadable report includes an `ownerGroup` column/field
- [ ] Records with a stored `ownerGroup` export that value
- [ ] Records without a stored `ownerGroup` export an empty value and the export completes
- [ ] Existing columns, their order, and record IDs are unchanged

## Test Requirements
- [ ] `tests/reports/test_catalog_export.py`: exported report contains the `ownerGroup` header and correct per-record values
- [ ] `tests/reports/test_catalog_export.py`: a record without `ownerGroup` exports an empty value without failing the export
- [ ] `tests/reports/test_catalog_export.py`: existing columns and their order are unchanged (regression)

## Verification Commands
- `pytest tests/reports/test_catalog_export.py` — all tests pass

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
