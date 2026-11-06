# Task 4 — Show ownerGroup in the downloadable catalog report

**Summary:** TC-9007: Include `ownerGroup` in the downloadable catalog report
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Epic group (by-sub-feature, pending approval):** TC-9007: Owner group display

## Repository
catalog-service

## Target Branch
main

## Description
Add `ownerGroup` to the downloadable catalog report (TC-9007 MVP requirement: "The ... downloadable report show[s] `ownerGroup`"). The value is read from the shared Service Catalog record.

Note: the Feature criterion "display `ownerGroup` for a record regardless of how that record was populated" is **unresolved** in the TC-9007 impact map — this task renders whatever value the shared record holds, but does not guarantee records populated by scheduled sync, fallback import, or on-demand refresh carry a value (those paths are out of scope pending stakeholder clarification).

## Files to Modify
- `src/reports/catalog_export.py` — add an `ownerGroup` column/field to the exported report
- `tests/reports/test_catalog_export.py` — add tests asserting `ownerGroup` appears in the report

## Implementation Notes
- `src/reports/catalog_export.py` already reads catalog records from `src/catalog/store.py`; add `ownerGroup` to the existing per-record output rather than performing a separate lookup.
- Append the new column so existing column order is preserved for downstream consumers of the report.
- Records without `ownerGroup` must export an empty cell/value rather than raising.
- Keep field naming and empty-value handling consistent with the summary API change in Task 3.
- Follow the existing test structure in `tests/reports/test_catalog_export.py`.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits, `Implements TC-<task-key>` footer, `Assisted-by:` trailer.
  - §3 PR rules: branch named after the task issue ID; `gh pr create --base main`; post PR link to the Jira task.
  - §5 Code change rules: limit changes to Files to Modify; inspect before modifying; reuse existing export logic (§5.4); parity with the summary API consumer (§5.8).
  - §1 Skill scope rules applicable to implement-task.

## Reuse Candidates
- `src/catalog/store.py` — shared record read helpers that now return `ownerGroup`
- `src/api/catalog_summary.py` — sibling consumer; align `ownerGroup` naming and empty-value handling (Task 3)

## Acceptance Criteria
- [ ] The downloadable report includes `ownerGroup` for each record that has one
- [ ] A record without `ownerGroup` exports an empty value and no error
- [ ] Existing report columns and their order are unchanged

## Test Requirements
- [ ] `tests/reports/test_catalog_export.py`: a record created with `ownerGroup` shows that value in the report
- [ ] `tests/reports/test_catalog_export.py`: a record without `ownerGroup` exports an empty value without error
- [ ] `tests/reports/test_catalog_export.py`: existing columns are present in their original order

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
