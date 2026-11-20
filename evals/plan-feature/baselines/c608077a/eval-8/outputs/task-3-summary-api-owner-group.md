# Task 3 — Show ownerGroup in the catalog summary API

**Epic:** TC-9007: Owner group display
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)

## Repository
catalog-service

## Target Branch
main

## Description
Add `ownerGroup` to each record returned by the catalog summary API, read from the shared Service Catalog record (TC-9007, Requirement 2).

Scope note: this task makes the consumer display whatever `ownerGroup` the shared record holds. It does not make sure that records populated by scheduled sync, fallback import, or on-demand refresh hold a value. Those writers are excluded by stakeholder instruction and are tracked as unresolved in the TC-9007 impact map. So Feature AC2 ("regardless of how that record was populated") is **not** satisfied by this task alone.

## Files to Modify
- `src/api/catalog_summary.py` — include `ownerGroup` in the per-record summary payload
- `tests/api/test_catalog_summary.py` — add tests for `ownerGroup` in the response

## API Changes
- Catalog summary API endpoint (served by `src/api/catalog_summary.py`) — MODIFY: each record in the response gains an `ownerGroup` field (string, or `null` when the stored record has no value). The change is additive and existing fields are unchanged.

## Implementation Notes
- Read `ownerGroup` from the record object returned by the existing read helpers in `src/catalog/store.py`. Do not query persistence separately.
- Records with no stored value (legacy records, or records from writers outside this scope) must serialize `ownerGroup` as `null` explicitly. Do not drop the key and do not raise, so API consumers can tell "unset" apart from "field not supported".
- Keep the existing response shape and ordering. Only add the field.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules.

## Reuse Candidates
- `src/catalog/store.py` — record read helpers and schema (Task 1)
- `src/api/catalog_summary.py` — existing per-record serialization. Extend it in place.

## Acceptance Criteria
- [ ] Summary API responses include `ownerGroup` for every record
- [ ] A record with a stored `ownerGroup` returns that value
- [ ] A record without a stored `ownerGroup` returns `ownerGroup: null` and the request succeeds
- [ ] All existing summary fields and record IDs are unchanged

## Test Requirements
- [ ] `tests/api/test_catalog_summary.py`: a record created with `ownerGroup` appears in the summary with the correct value
- [ ] `tests/api/test_catalog_summary.py`: a record stored without `ownerGroup` appears with `ownerGroup: null` and no error
- [ ] `tests/api/test_catalog_summary.py`: existing response fields and IDs are unchanged (regression)

## Verification Commands
- `pytest tests/api/test_catalog_summary.py` — all tests pass

## Documentation Updates
- API reference for the catalog summary endpoint (if present in the repository) — document the new `ownerGroup` response field and its `null` semantics

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
