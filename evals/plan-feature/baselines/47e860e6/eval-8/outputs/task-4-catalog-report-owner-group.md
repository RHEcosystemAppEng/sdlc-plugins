# Task 4 — Show `ownerGroup` in the downloadable catalog report

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (omitted — TC-9007 has no fixVersions)
**Parent / Epic:** TC-9007: Owner group display (if Epic type available)

## Repository
catalog-service

## Target Branch
main

## Description
Include the `ownerGroup` of each Service Catalog record in the downloadable catalog report (TC-9007 MVP requirement: "... and downloadable report show `ownerGroup`"). `src/reports/catalog_export.py` reads records from the shared Service Catalog; it must emit `ownerGroup` (added in Task 1) for each record.

**Scope note (TC-9007 scope conflict):** this task makes the report display whatever `ownerGroup` the shared record holds. The Feature AC "regardless of how that record was populated" additionally depends on every population path writing/preserving `ownerGroup`; that dependency is UNRESOLVED in the TC-9007 impact map and is not satisfied by this task.

## Files to Modify
- `src/reports/catalog_export.py` — add an `ownerGroup` column/field to the exported report for each record
- `tests/reports/test_catalog_export.py` — add tests asserting `ownerGroup` is exported and legacy records render the documented sentinel

## Implementation Notes
- In `src/reports/catalog_export.py`, read `ownerGroup` from the catalog record via the existing store read helper in `src/catalog/store.py` and add it to the exported row/field set following the existing column-definition pattern in that module. Append the new column rather than reordering existing columns so downstream report consumers are not broken.
- For legacy records without `ownerGroup`, emit the sentinel's report representation (e.g., empty cell) consistently with how the module renders other missing values; keep null-handling semantically consistent with the summary API (Task 3).
- Do not change record selection, ordering, or stable IDs in the report.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits; footer `Implements <task-key>`; `--trailer="Assisted-by: Claude Code"`.
  - §3 PR rules: branch named after the task issue ID; `gh pr create --base main`; post PR link on the Jira task.
  - §5 Code change rules: only the files listed above (5.1); inspect before modifying (5.2); reuse the store read helper (5.4); parity with the summary API consumer on missing-value handling (5.8).

## Reuse Candidates
- `src/catalog/store.py` — record read helper and `ownerGroup` field (Task 1)
- `src/api/catalog_summary.py` — sibling consumer; align missing-value handling with Task 3

## Acceptance Criteria
- [ ] The downloadable report includes an `ownerGroup` column/field for each catalog record
- [ ] The exported `ownerGroup` value equals the value stored on the shared record
- [ ] Legacy records without `ownerGroup` export successfully with the documented missing-value representation
- [ ] Existing report columns, their order, record set, and stable IDs are unchanged

## Test Requirements
- [ ] `tests/reports/test_catalog_export.py`: seed a record with `ownerGroup` and assert the exported report contains it
- [ ] `tests/reports/test_catalog_export.py`: seed a legacy record without `ownerGroup` and assert export succeeds with the missing-value representation
- [ ] `tests/reports/test_catalog_export.py`: assert existing columns (and their order) and stable IDs are unchanged (regression)

## Verification Commands
- `pytest tests/reports/test_catalog_export.py` — all tests pass

## Documentation Updates
- Downloadable report documentation — add the `ownerGroup` column (handled in Task 5)

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to the shared Service Catalog record schema with preserve-on-update semantics
