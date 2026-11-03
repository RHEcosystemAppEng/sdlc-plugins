# Task 3 — Show `ownerGroup` in the catalog summary API

**Labels**: ai-generated-jira
**Priority**: Major (inherited from TC-9007)
**Fix Versions**: (omitted — TC-9007 has no fixVersions)

## Repository
catalog-service

## Target Branch
main

## Description
Add `ownerGroup` from the shared Service Catalog record to the catalog summary API response. This covers the TC-9007 requirement "The catalog summary API … show[s] `ownerGroup`."

The API reads `ownerGroup` from the stored record, so it shows whatever value the record holds. Whether records populated by writers outside the approved onboarding scope have a value is an open question in the TC-9007 impact map.

## Files to Modify
- `src/api/catalog_summary.py` — add `ownerGroup` to each record entry in the summary response
- `tests/api/test_catalog_summary.py` — add tests asserting `ownerGroup` appears in the response

## API Changes
- Catalog summary API (served by `src/api/catalog_summary.py`) — MODIFY: each record entry in the response gains an additive `ownerGroup` field. Existing fields are unchanged.

## Implementation Notes
- `src/api/catalog_summary.py` reads catalog records for the summary API. Read `ownerGroup` from the record returned by the `src/catalog/store.py` helpers, and map it into the response the same way the existing fields are mapped.
- Records that predate the field and have no `ownerGroup` should produce `null` (or the API's existing convention for absent values). They must not cause an error.
- The change is additive. Do not rename or remove existing response fields.
- Constraints (docs/constraints.md):
  - §1.4/§1.5/§1.6: scoped changes, inspect before modifying, ask if this description is incomplete.
  - §2.1–2.3: Conventional Commits, Jira footer, Assisted-by trailer.
  - §3.1–3.3: branch named after the task key, PR link posted to Jira, `--base main`.
  - §5.1–5.8: only the listed files, trace the data flow from the stored record to the response, keep parity with how sibling fields are serialized.

## Reuse Candidates
- `src/catalog/store.py` — record read helpers (extended with `ownerGroup` in Task 1)
- `src/api/catalog_summary.py` — existing record-to-response field mapping

## Acceptance Criteria
- [ ] The summary API response includes `ownerGroup` for each record, taken from the stored Service Catalog record
- [ ] A record without a stored `ownerGroup` returns the absent-value representation without error
- [ ] Existing summary response fields are unchanged

## Test Requirements
- [ ] `tests/api/test_catalog_summary.py`: seed a catalog record with `ownerGroup` directly through the store and assert the summary response contains it
- [ ] `tests/api/test_catalog_summary.py`: seed a record without `ownerGroup` and assert the response succeeds with the absent-value representation
- [ ] Existing tests in `tests/api/test_catalog_summary.py` still pass

## Documentation Updates
- Summary API reference documentation (if present in the repository) — add the `ownerGroup` response field

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to the Service Catalog record schema and persistence helpers
