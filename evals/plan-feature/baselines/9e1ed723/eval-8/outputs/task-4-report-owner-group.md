# Task 4 — Include ownerGroup in the downloadable catalog report

**Summary:** TC-9007: Add ownerGroup to the downloadable catalog report
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (none; the Feature has no fixVersions)
**Epic group (by-sub-feature, pending approval):** Owner group display

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` column/field to the downloadable catalog report, read from the shared Service Catalog record. This covers the report part of the Feature requirement "The catalog summary API and downloadable report show `ownerGroup`".

Scope note: as with the summary API, records written by catalog paths outside the approved onboarding-and-display scope may not have `ownerGroup` populated. That gap is unresolved in the TC-9007 impact map.

## Files to Modify
- `src/reports/catalog_export.py` — emit `ownerGroup` for each catalog record in the report

## Implementation Notes
- `src/reports/catalog_export.py` reads catalog records for the downloadable report. Read `ownerGroup` from the shared record in `src/catalog/store.py`.
- Add the column/field without reordering or renaming existing report columns, so existing report consumers keep working.
- For records with no stored `ownerGroup`, emit an empty value consistently (match the null handling chosen for the summary API in Task 3).
- Constraints (docs/constraints.md): §2 commit rules; §3 PR to `main` with `--base main`; §5.1 file scope; §5.4 reuse store accessors; §5.8 keep parity with the summary API output in Task 3.

## Reuse Candidates
- `src/catalog/store.py` — shared record schema/accessors with `ownerGroup` (from Task 1)
- `src/api/catalog_summary.py` — sibling consumer reading the same field (Task 3). Keep the field name and missing-value handling consistent.

## Acceptance Criteria
- [ ] The downloadable report includes an `ownerGroup` value for each catalog record that has one stored
- [ ] Records without a stored `ownerGroup` produce an empty `ownerGroup` value and report generation does not fail
- [ ] Existing report columns and record identifiers are unchanged

## Test Requirements
- [ ] `tests/reports/test_catalog_export.py`: a record with `ownerGroup` is exported with that value
- [ ] `tests/reports/test_catalog_export.py`: a legacy record without `ownerGroup` exports an empty value without error
- [ ] `tests/reports/test_catalog_export.py`: regression check that existing columns and record IDs are unchanged

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
