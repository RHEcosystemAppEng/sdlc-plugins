# Task 4 — Show `ownerGroup` in the downloadable catalog report

**Labels**: ai-generated-jira
**Priority**: Major (inherited from TC-9007)
**Fix Versions**: (omitted — TC-9007 has no fixVersions)

## Repository
catalog-service

## Target Branch
main

## Description
Add `ownerGroup` from the shared Service Catalog record to the downloadable catalog report. This covers the TC-9007 requirement "The … downloadable report show[s] `ownerGroup`."

The report reads `ownerGroup` from the stored record. Whether records populated by writers outside the approved onboarding scope have a value is an open question in the TC-9007 impact map.

## Files to Modify
- `src/reports/catalog_export.py` — add an `ownerGroup` column/field to the exported report
- `tests/reports/test_catalog_export.py` — add tests asserting the `ownerGroup` column/field and its values

## Implementation Notes
- `src/reports/catalog_export.py` reads catalog records for the downloadable report. Add `ownerGroup` using the same column/field definition pattern as the existing record fields, and read the value from the `src/catalog/store.py` record.
- Records without a stored `ownerGroup` should produce an empty cell/value, not an error.
- Add the new column without reordering or renaming existing columns, so existing consumers of the report are not broken.
- Constraints (docs/constraints.md):
  - §1.4/§1.5/§1.6: scoped changes, inspect before modifying, ask if this description is incomplete.
  - §2.1–2.3: Conventional Commits, Jira footer, Assisted-by trailer.
  - §3.1–3.3: branch named after the task key, PR link posted to Jira, `--base main`.
  - §5.1–5.8: only the listed files, trace the data flow from the stored record to the report output, keep parity with sibling columns.

## Reuse Candidates
- `src/catalog/store.py` — record read helpers (extended with `ownerGroup` in Task 1)
- `src/reports/catalog_export.py` — existing column/field definitions for record attributes

## Acceptance Criteria
- [ ] The downloadable report includes an `ownerGroup` column/field populated from the stored Service Catalog record
- [ ] A record without a stored `ownerGroup` exports with an empty value and no error
- [ ] Existing report columns keep their names and order

## Test Requirements
- [ ] `tests/reports/test_catalog_export.py`: seed a record with `ownerGroup` directly through the store and assert the export contains the column and value
- [ ] `tests/reports/test_catalog_export.py`: seed a record without `ownerGroup` and assert the export succeeds with an empty value
- [ ] `tests/reports/test_catalog_export.py`: assert existing columns are unchanged
- [ ] Existing tests in `tests/reports/test_catalog_export.py` still pass

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to the Service Catalog record schema and persistence helpers
