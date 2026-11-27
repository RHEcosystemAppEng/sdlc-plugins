# Task 3 — Expose ownerGroup in the catalog summary API

**Summary:** TC-9007: Show ownerGroup in the catalog summary API
**Epic:** TC-9007: Owner group display
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**fixVersions:** omitted (Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
Include each record's `ownerGroup` in the catalog summary API response, so API consumers can see who owns each service.

Scope note: this task validates the summary API with records created by registration and directly through the catalog store. Showing `ownerGroup` for records produced by other population paths ("regardless of how that record was populated") is recorded as unresolved in the impact map. This task does not claim that criterion is satisfied.

## Files to Modify
- `src/api/catalog_summary.py`: add `ownerGroup` to each record in the summary response.
- `tests/api/test_catalog_summary.py`: add summary API tests for `ownerGroup`.

## API Changes
- Catalog summary API: MODIFY. Each record in the response gains an `ownerGroup` field (string, or `null` for records stored without one). The change is additive and no existing field changes.

## Implementation Notes
- Read `ownerGroup` from the shared record via the existing read helpers in `src/catalog/store.py`. Do not re-query persistence.
- Records stored before TC-9007 have no `ownerGroup`. Serialize them with an explicit `null`. Do not drop the key or fail the response, so a missing owner group is visible to consumers and never silently hidden.
- Keep the existing response fields, ordering and record IDs unchanged.
- Constraints (docs/constraints.md): §1.4 scoped changes; §2.1–2.3 commit rules; §3.1–3.3 PR rules with `--base main`; §5.1–5.4 listed files only, inspect first, follow existing serialization pattern in `src/api/catalog_summary.py`, no duplicated read logic.

## Reuse Candidates
- `src/catalog/store.py`: catalog record read helpers (extended in Task 1).
- `src/api/catalog_summary.py`: existing per-record serialization.

## Acceptance Criteria
- [ ] The summary API response includes `ownerGroup` for each record.
- [ ] A record created by registration with an `ownerGroup` shows that value in the summary API.
- [ ] A record stored without `ownerGroup` returns `ownerGroup: null`, and the response still succeeds.
- [ ] Existing response fields and record IDs are unchanged.

## Test Requirements
- [ ] `tests/api/test_catalog_summary.py`: create a record through the registration flow with `ownerGroup` and assert the summary API returns it.
- [ ] `tests/api/test_catalog_summary.py`: update a record through the store without `ownerGroup` and assert the summary still shows the preserved value.
- [ ] `tests/api/test_catalog_summary.py`: seed a record without `ownerGroup` and assert `ownerGroup` is `null` and the response succeeds.
- [ ] Existing summary API tests still pass.

## Verification Commands
- `pytest tests/api/test_catalog_summary.py`: all tests pass.

## Documentation Updates
- Summary API documentation: add the `ownerGroup` response field (covered by Task 5).

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
- Depends on: Task 2 — Collect ownerGroup during initial service registration (registration-sourced test fixtures)
