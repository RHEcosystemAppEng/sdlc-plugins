# Task 4 — Include ownerGroup in the downloadable catalog report

**Summary:** TC-9007: Show ownerGroup in the downloadable catalog report
**Epic:** TC-9007: Owner group display
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**fixVersions:** omitted (Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` column/field to the downloadable catalog report, so report users can see who owns each service.

Scope note: this task validates the report with records created by registration and directly through the catalog store. Showing `ownerGroup` for records produced by other population paths is recorded as unresolved in the impact map. This task does not claim that criterion is satisfied.

## Files to Modify
- `src/reports/catalog_export.py`: add `ownerGroup` to each exported record.
- `tests/reports/test_catalog_export.py`: add export tests for `ownerGroup`.

## Implementation Notes
- Read `ownerGroup` via the existing catalog read helpers in `src/catalog/store.py`.
- Add the field next to the existing record fields, following the export's current column/field ordering conventions. Append it so existing consumers of the report layout are not broken.
- Records without `ownerGroup` must export an explicit empty value. They must not be skipped and the export must not fail.
- Keep record IDs and existing columns unchanged.
- Constraints (docs/constraints.md): §1.4 scoped changes; §2.1–2.3 commit rules; §3.1–3.3 PR rules with `--base main`; §5.1–5.4 listed files only, inspect first, follow the existing export pattern, no duplicated read logic.

## Reuse Candidates
- `src/catalog/store.py`: catalog record read helpers (extended in Task 1).
- `src/reports/catalog_export.py`: existing per-record export formatting.

## Acceptance Criteria
- [ ] The downloadable report includes `ownerGroup` for each record.
- [ ] A record created by registration with an `ownerGroup` shows that value in the report.
- [ ] A record stored without `ownerGroup` is still exported, with an empty `ownerGroup` value.
- [ ] Existing columns/fields and record IDs in the report are unchanged.

## Test Requirements
- [ ] `tests/reports/test_catalog_export.py`: create a record through the registration flow with `ownerGroup` and assert the report contains it.
- [ ] `tests/reports/test_catalog_export.py`: update a record through the store without `ownerGroup` and assert the report shows the preserved value.
- [ ] `tests/reports/test_catalog_export.py`: seed a record without `ownerGroup` and assert it is exported with an empty value.
- [ ] Existing export tests still pass.

## Verification Commands
- `pytest tests/reports/test_catalog_export.py`: all tests pass.

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
- Depends on: Task 2 — Collect ownerGroup during initial service registration (registration-sourced test fixtures)
