# Task 3 — Display ownerGroup in the catalog summary API and downloadable report

**Summary:** TC-9007: Show ownerGroup in catalog summary API and report export
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Epic group (by-sub-feature):** Owner group display

## Repository
catalog-service

## Target Branch
main

## Description
Expose `ownerGroup` from the shared Service Catalog record in both consumers: the catalog summary API and the downloadable catalog report. Both consumers read the stored record, so they display whatever `ownerGroup` the record holds.

Scope note: the Feature criterion says consumers display `ownerGroup` "regardless of how that record was populated". End-to-end verification for records written by paths other than registration is unresolved pending scope clarification (see the impact map). This task does not claim that criterion is satisfied.

## Files to Modify
- `src/api/catalog_summary.py` — include `ownerGroup` in the summary response for each record
- `src/reports/catalog_export.py` — add an `ownerGroup` column or field to the downloadable report
- `tests/api/test_catalog_summary.py` — summary API tests for `ownerGroup`
- `tests/reports/test_catalog_export.py` — export tests for `ownerGroup`

## API Changes
- Catalog summary API — MODIFY: each record in the response gains an additive `ownerGroup` field (nullable for legacy records)

## Implementation Notes
- Both consumers read records through `src/catalog/store.py`. Read `ownerGroup` from the record schema extended in Task 1 instead of computing or defaulting it in each consumer.
- Handle legacy records that have no `ownerGroup` the same way in both consumers (for example, `null` in the API and an empty cell in the report). Do not let a missing value raise an error.
- Follow the existing field serialization in `src/api/catalog_summary.py` and the column/field ordering pattern in `src/reports/catalog_export.py`. Add the new field next to the existing record fields.
- The change is additive. Do not rename or remove existing response fields or report columns.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules (change only the listed files; keep the two consumers consistent in how they handle the field).

## Reuse Candidates
- `src/catalog/store.py` — record schema with `ownerGroup` (from Task 1); both consumers read through it
- `src/api/catalog_summary.py` / `src/reports/catalog_export.py` — existing record-to-output field mapping

## Acceptance Criteria
- [ ] The summary API response includes `ownerGroup` for each catalog record that has one
- [ ] The downloadable report includes `ownerGroup` for each catalog record that has one
- [ ] Records without `ownerGroup` (legacy) are rendered without errors in both consumers, with consistent empty-value handling
- [ ] Existing summary API fields and report columns are unchanged

## Test Requirements
- [ ] `tests/api/test_catalog_summary.py`: seed a record through the store with `ownerGroup` and assert the summary response contains it
- [ ] `tests/api/test_catalog_summary.py`: seed a legacy record without `ownerGroup` and assert the response is valid and returns the documented empty value
- [ ] `tests/api/test_catalog_summary.py`: seed a record created through registration (Task 2) and assert its `ownerGroup` is shown
- [ ] `tests/reports/test_catalog_export.py`: export a record with `ownerGroup` and assert the report contains the value
- [ ] `tests/reports/test_catalog_export.py`: export a legacy record without `ownerGroup` and assert the export succeeds with the empty value
- [ ] `tests/reports/test_catalog_export.py`: export a record created through registration (Task 2) and assert its `ownerGroup` appears

## Documentation Updates
- Summary API documentation — add `ownerGroup` to the record response fields (if API docs exist in the repository)

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema and persistence
- Depends on: Task 2 — Collect and persist ownerGroup during initial registration (for the registration-sourced test cases)
