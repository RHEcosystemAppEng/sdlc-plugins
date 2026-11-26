# Task 3 — Show ownerGroup in the catalog summary API

**Summary:** TC-9007: Include `ownerGroup` in the catalog summary API response
**Issue type:** Task | **Parent Epic:** TC-9007: Owner group display and documentation
**Labels:** ai-generated-jira | **Priority:** Major | **Fix Versions:** (none — Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
The catalog summary API reads Service Catalog records. It must include each record's `ownerGroup` in its response so API consumers can see who owns each service.

Scope note: the API displays whatever `ownerGroup` is stored on the shared record. In this feature's scope, only registration (Task 2) is guaranteed to write one. AC2 ("display regardless of how that record was populated") stays unresolved for records written by scheduled sync, fallback import, or on-demand refresh until the stakeholder decides on scope (see the TC-9007 impact map).

## Files to Modify
- `src/api/catalog_summary.py` — add `ownerGroup` to each record in the summary response
- `tests/api/test_catalog_summary.py` — add tests asserting `ownerGroup` appears in the response

## API Changes
- Catalog summary endpoint (served by `src/api/catalog_summary.py`) — MODIFY: each record in the response gains an `ownerGroup` field (string, or `null` when the stored record has none). The change is additive, and existing fields are unchanged.

## Implementation Notes
- Read `ownerGroup` from the record object returned by the existing store read helpers in `src/catalog/store.py`. Do not add a separate query.
- Serialize a record with no stored `ownerGroup` (for example, a legacy record) as `null`. Do not error, and do not substitute a fabricated default. A fabricated value would hide the population gap in the unresolved paths.
- Keep the existing response shape and field order. Add the new key next to the other record attributes.
- Constraints (docs/constraints.md): §2 Conventional Commits with the Jira footer and `Assisted-by:` trailer; §3 task-ID branch, `--base main`, PR link posted to Jira; §5 stay within the listed files, reuse store read helpers, add doc and given-when-then comments to tests.

## Reuse Candidates
- `src/catalog/store.py` — existing record read helpers (now carrying `ownerGroup`, from Task 1)
- `tests/api/test_catalog_summary.py` — existing summary API fixtures and response assertions

## Acceptance Criteria
- [ ] The summary API response includes `ownerGroup` for each record with the stored value
- [ ] A record with no stored `ownerGroup` is returned with `ownerGroup: null`, without error
- [ ] All existing response fields and record IDs are unchanged

## Test Requirements
- [ ] `tests/api/test_catalog_summary.py`: seed a record with `ownerGroup` and assert the response contains the matching value
- [ ] `tests/api/test_catalog_summary.py`: seed a record without `ownerGroup` and assert the response returns `null` and status 200
- [ ] `tests/api/test_catalog_summary.py`: assert existing fields and IDs are unchanged in the response

## Verification Commands
- `pytest tests/api/test_catalog_summary.py` — all tests pass

## Documentation Updates
- API documentation for the catalog summary endpoint — add the `ownerGroup` response field (handled in Task 5)

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
