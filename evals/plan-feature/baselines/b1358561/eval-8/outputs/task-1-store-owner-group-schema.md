# Task 1 — Add ownerGroup to the shared Service Catalog record schema

**Summary:** TC-9007: Add ownerGroup to Service Catalog record schema and persistence helpers
**Epic:** TC-9007: Owner group onboarding
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**fixVersions:** omitted (Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so each service record can carry the group that owns it. Every writer and reader of the catalog depends on this schema and its persistence helpers, so this task sets the contract the rest of TC-9007 relies on. Update semantics must keep the current `ownerGroup` when an update omits it and replace it when an update supplies a new value. Stable record IDs and existing population behavior must not change.

Scope note: this task covers the shared store only. The impact map records which record writers are validated against this contract and which are unresolved. This task does not claim the Feature-level "every record after creation or update" criterion is met for every writer.

## Files to Modify
- `src/catalog/store.py`: add `ownerGroup` to the catalog record schema. Persist it on create, and on update keep the stored value when the field is omitted.
- `tests/catalog/test_store.py`: add persistence tests for `ownerGroup`.

## Implementation Notes
- Extend the existing record schema and persistence helpers in `src/catalog/store.py` instead of adding a parallel structure. All writers already go through these helpers, so the preservation rule belongs here, in the shared update helper, not in individual callers.
- Treat "omitted" (key absent or `None`) as "keep the existing value". Treat an explicit non-empty value as a replacement. Document this rule in the helper's docstring so later callers follow it.
- Records stored before this change have no `ownerGroup`. Reads must handle that deterministically, for example by returning `None`, and must not raise. Do not backfill or rewrite existing records in this task, because the Feature requires existing population behavior to stay unchanged.
- Do not change how record IDs are generated or matched. Updates must still resolve to the same record ID.
- Constraints (docs/constraints.md): §1.4 keep changes scoped to this task; §2.1–2.3 commits use Conventional Commits, reference TC-9007's task key in the footer and include an `Assisted-by:` trailer; §3.1–3.3 branch named after the task key, `gh pr create --base main`, PR link posted to Jira; §5.1–5.4 modify only the listed files, inspect before changing, follow existing store patterns and do not duplicate helper logic.

## Reuse Candidates
- `src/catalog/store.py`: the existing record schema and persistence/update helpers. Extend them, do not wrap or reimplement them.
- `tests/catalog/test_store.py`: existing persistence test fixtures and patterns for create/update round-trips.

## Acceptance Criteria
- [ ] The catalog record schema includes an `ownerGroup` field.
- [ ] Creating a record with an `ownerGroup` value persists and returns that value.
- [ ] Updating a record without supplying `ownerGroup` keeps the previously stored value.
- [ ] Updating a record with a new `ownerGroup` value replaces the stored value.
- [ ] Record IDs stay stable across create and update. An update that sets or omits `ownerGroup` does not change the record's ID.
- [ ] Records stored without `ownerGroup` (pre-existing data) can still be read without error.

## Test Requirements
- [ ] `tests/catalog/test_store.py`: create a record with `ownerGroup` and assert it round-trips.
- [ ] `tests/catalog/test_store.py`: update a record while omitting `ownerGroup` and assert the existing value is kept.
- [ ] `tests/catalog/test_store.py`: update a record with a new `ownerGroup` and assert it replaces the old value.
- [ ] `tests/catalog/test_store.py`: assert the record ID is unchanged after each update scenario.
- [ ] `tests/catalog/test_store.py`: read a record persisted without `ownerGroup` and assert no error and a deterministic empty value.
- [ ] Existing tests in `tests/catalog/test_store.py` still pass unchanged.

## Verification Commands
- `pytest tests/catalog/test_store.py`: all tests pass.

## Dependencies
- None.
