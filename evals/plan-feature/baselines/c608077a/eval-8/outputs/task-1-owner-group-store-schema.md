# Task 1 — Add ownerGroup to the shared Service Catalog record schema

**Epic:** TC-9007: Owner group capture
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so each service can show who owns it (TC-9007). This is the foundation for the onboarding and display tasks. The persistence helpers must keep the stored `ownerGroup` when an update does not supply a new value, and must not change record IDs.

Scope note: this task changes the shared store only. Whether the scheduled-sync, fallback-import, and on-demand-refresh writers set or keep `ownerGroup` is **outside this task's scope** (stakeholder instruction) and is tracked as an unresolved scope conflict in the TC-9007 impact map. This task does not by itself satisfy the Feature criterion "every record has an ownerGroup after creation or update".

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the catalog record schema; make create/update persistence helpers accept it; on update, keep the existing value when no new value is supplied
- `tests/catalog/test_store.py` — add persistence tests for the new field and its update semantics

## Implementation Notes
- Extend the existing record schema in `src/catalog/store.py` rather than adding a parallel model. All writers and readers share this schema.
- Treat `ownerGroup` as optional on read: records written before this change, or by writers not updated in this feature, have no value. Readers must get an explicit empty/`None` value, not an exception.
- Update semantics: in the store's update/upsert helper, merge the incoming payload over the stored record so an absent `ownerGroup` key (or `None`, if that is the existing convention for "not supplied") keeps the stored value. Only an explicitly supplied non-empty value replaces it.
- Do not change how record IDs are generated or matched. The existing key/ID logic in `store.py` must stay unchanged (Feature AC3).
- Constraints (docs/constraints.md): §2 commit rules (Conventional Commits, Jira ID footer `Implements <task-key>`, `Assisted-by:` trailer); §3 PR rules (`gh pr create --base main`, post PR link on the Jira task); §5 code change rules (scope changes to listed files, inspect before modifying, reuse existing helpers, trace the data flow end to end).

## Reuse Candidates
- `src/catalog/store.py` — existing record schema and create/update persistence helpers. Extend these rather than writing new persistence code.
- `tests/catalog/test_store.py` — existing persistence test fixtures and patterns for creating and updating records

## Acceptance Criteria
- [ ] The catalog record schema in `src/catalog/store.py` includes an `ownerGroup` field
- [ ] Creating a record with `ownerGroup` persists and returns the value
- [ ] Updating a record without supplying `ownerGroup` keeps the previously stored value
- [ ] Updating a record with a new `ownerGroup` replaces the stored value
- [ ] Reading a record that has no stored `ownerGroup` returns an explicit empty/`None` value without error
- [ ] Record IDs and existing persistence behavior for other fields are unchanged

## Test Requirements
- [ ] `tests/catalog/test_store.py`: create a record with `ownerGroup` and assert it round-trips
- [ ] `tests/catalog/test_store.py`: update a record without `ownerGroup` and assert the original value is kept
- [ ] `tests/catalog/test_store.py`: update a record with a new `ownerGroup` and assert it is replaced
- [ ] `tests/catalog/test_store.py`: load a legacy record with no `ownerGroup` and assert an explicit empty value with no exception
- [ ] `tests/catalog/test_store.py`: assert the record ID is identical before and after an update (stable ID regression)
- [ ] Existing tests in `tests/catalog/test_store.py` pass unchanged

## Verification Commands
- `pytest tests/catalog/test_store.py` — all tests pass

## Dependencies
- None
