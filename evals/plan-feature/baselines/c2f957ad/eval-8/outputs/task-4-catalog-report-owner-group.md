# Task 4 — Show ownerGroup in the downloadable catalog report

**Summary:** TC-9007: Add an `ownerGroup` column to the downloadable catalog report
**Issue type:** Task | **Parent Epic:** TC-9007: Owner group display and documentation
**Labels:** ai-generated-jira | **Priority:** Major | **Fix Versions:** (none — Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
The downloadable catalog report reads Service Catalog records. It must include each record's `ownerGroup` so report users can see who owns each service.

Scope note: the report displays whatever `ownerGroup` is stored on the shared record. AC2 ("regardless of how that record was populated") stays unresolved for records written by scheduled sync, fallback import, or on-demand refresh until the stakeholder decides on scope (see the TC-9007 impact map).

## Files to Modify
- `src/reports/catalog_export.py` — add an `ownerGroup` column/field to the exported report
- `tests/reports/test_catalog_export.py` — add tests asserting `ownerGroup` appears in the export

## Implementation Notes
- Read `ownerGroup` from the records returned by the existing store read helpers in `src/catalog/store.py`, the same source the report already uses for its other columns.
- Add the column to the report's existing header/field definition and to row generation. Write an empty cell for records with no stored `ownerGroup`. Do not fabricate a placeholder value.
- Keep the existing columns and their order. Append `ownerGroup` so consumers that parse by position are not broken.
- Constraints (docs/constraints.md): §2 Conventional Commits with the Jira footer and `Assisted-by:` trailer; §3 task-ID branch, `--base main`, PR link posted to Jira; §5 stay within the listed files, reuse store read helpers, add doc and given-when-then comments to tests.

## Reuse Candidates
- `src/catalog/store.py` — existing record read helpers (now carrying `ownerGroup`, from Task 1)
- `tests/reports/test_catalog_export.py` — existing export fixtures and output assertions
- `src/api/catalog_summary.py` — Task 3 applies the same rule for records with no `ownerGroup`; keep the two consistent

## Acceptance Criteria
- [ ] The downloadable report includes an `ownerGroup` column with the stored value for each record
- [ ] A record with no stored `ownerGroup` produces an empty cell, without error
- [ ] Existing columns, their order, and record IDs are unchanged

## Test Requirements
- [ ] `tests/reports/test_catalog_export.py`: export a record with `ownerGroup` and assert the column header and value appear
- [ ] `tests/reports/test_catalog_export.py`: export a record without `ownerGroup` and assert an empty cell, no error
- [ ] `tests/reports/test_catalog_export.py`: assert existing columns, their order, and IDs are unchanged

## Verification Commands
- `pytest tests/reports/test_catalog_export.py` — all tests pass

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
