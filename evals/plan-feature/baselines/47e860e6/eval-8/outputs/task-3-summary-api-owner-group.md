# Task 3 — Show `ownerGroup` in the catalog summary API

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (omitted — TC-9007 has no fixVersions)
**Parent / Epic:** TC-9007: Owner group display (if Epic type available)

## Repository
catalog-service

## Target Branch
main

## Description
Expose the `ownerGroup` of each Service Catalog record in the catalog summary API (TC-9007 MVP requirement: "The catalog summary API ... show[s] `ownerGroup`"). `src/api/catalog_summary.py` reads records from the shared Service Catalog; it must include the `ownerGroup` field (added in Task 1) in each summary entry.

**Scope note (TC-9007 scope conflict):** this task makes the summary API display whatever `ownerGroup` the shared record holds. The Feature AC "display `ownerGroup` for a record regardless of how that record was populated" additionally depends on every population path writing/preserving `ownerGroup`; that dependency is UNRESOLVED in the TC-9007 impact map and is not satisfied by this task.

## Files to Modify
- `src/api/catalog_summary.py` — include `ownerGroup` in each summary record in the API response
- `tests/api/test_catalog_summary.py` — add tests asserting `ownerGroup` appears in the response and that records lacking it render the documented sentinel

## API Changes
- Catalog summary API response — MODIFY: each summary record gains an additive `ownerGroup` field (string; `null` for legacy records persisted before TC-9007). No existing fields are removed or renamed.

## Implementation Notes
- In `src/api/catalog_summary.py`, read `ownerGroup` from the catalog record returned by the existing store read helper in `src/catalog/store.py` and add it to the per-record serialization alongside existing summary fields. Follow the existing field-mapping pattern in that module.
- For legacy records without `ownerGroup`, emit the sentinel defined in Task 1 (e.g., `null`) — do not fabricate a value and do not fail the request.
- The change is additive; keep existing response fields, ordering, and stable IDs unchanged so current API consumers are unaffected.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits; footer `Implements <task-key>`; `--trailer="Assisted-by: Claude Code"`.
  - §3 PR rules: branch named after the task issue ID; `gh pr create --base main`; post PR link on the Jira task.
  - §5 Code change rules: only the files listed above (5.1); inspect before modifying (5.2); reuse the store read helper (5.4); compare parity with the report consumer in Task 4 for null handling (5.8).

## Reuse Candidates
- `src/catalog/store.py` — record read helper and `ownerGroup` field (Task 1)
- `src/reports/catalog_export.py` — sibling consumer of the same record; keep `ownerGroup` null-handling consistent with Task 4

## Acceptance Criteria
- [ ] The summary API response includes `ownerGroup` for each catalog record
- [ ] The `ownerGroup` value in the response equals the value stored on the shared record
- [ ] Legacy records without `ownerGroup` are returned with the documented sentinel and the request succeeds
- [ ] Existing summary fields and stable IDs in the response are unchanged

## Test Requirements
- [ ] `tests/api/test_catalog_summary.py`: seed a catalog record with `ownerGroup` and assert the summary response contains it
- [ ] `tests/api/test_catalog_summary.py`: seed a legacy record without `ownerGroup` and assert the response contains the sentinel and returns success
- [ ] `tests/api/test_catalog_summary.py`: assert existing response fields and stable IDs are unchanged (regression)

## Verification Commands
- `pytest tests/api/test_catalog_summary.py` — all tests pass

## Documentation Updates
- Catalog summary API reference — add the `ownerGroup` response field (handled in Task 5)

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to the shared Service Catalog record schema with preserve-on-update semantics
