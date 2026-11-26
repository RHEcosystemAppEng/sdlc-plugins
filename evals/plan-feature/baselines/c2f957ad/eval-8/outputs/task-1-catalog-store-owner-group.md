# Task 1 — Add ownerGroup to the shared Service Catalog record schema

**Summary:** TC-9007: Add `ownerGroup` field and preserve-on-update semantics to Service Catalog store
**Issue type:** Task | **Parent Epic:** TC-9007: Owner group data model and onboarding
**Labels:** ai-generated-jira | **Priority:** Major | **Fix Versions:** (none — Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so callers can record and read which group owns a service. The persistence helpers must keep the stored owner group when a record is updated unless the caller supplies a new non-empty value. Record ID generation and existing persistence behavior must not change.

This is the shared-store foundation for TC-9007. In this feature's scope only the registration writer (Task 2) and the summary/report readers (Tasks 3, 4) consume it. The field is added as **optional** at the store level on purpose: scheduled sync, fallback import, and on-demand refresh also write catalog records, and they are out of scope for this feature (see the impact map's unresolved scope conflict). Making the field required would break those writers and violate "existing catalog population behavior remains unchanged."

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the catalog record schema; update the create/update persistence helpers so a missing or empty `ownerGroup` on update keeps the stored value
- `tests/catalog/test_store.py` — add tests for the new field, preserve-on-update, and stable IDs

## Implementation Notes
- Extend the existing record schema in `src/catalog/store.py` instead of adding a parallel structure. Serialization/deserialization of stored records must round-trip `ownerGroup`, and records persisted before this change (with no `ownerGroup`) must still load, with `ownerGroup` defaulting to `None`.
- Update semantics: inside the existing update/upsert helper, merge `ownerGroup` like this: if the incoming value is `None`/missing (or an empty string), keep the stored value; otherwise replace it. Do not change any other field's merge behavior.
- Do not touch ID derivation. Whatever function computes or assigns the record ID today must be left as is.
- Do not modify `src/workflows/scheduled_sync.py`, `src/workflows/fallback_import.py`, or `src/api/on_demand_refresh.py` — out of scope pending stakeholder clarification.
- Constraints (docs/constraints.md): §2 commits must use Conventional Commits, reference the Jira task in the footer, and carry an `Assisted-by:` trailer; §3 branch is named after the task ID, `gh pr create --base main`, and the PR link is posted to Jira; §5 keep changes to the files listed above, inspect before modifying, reuse existing store helpers, add doc comments and given-when-then comments to non-trivial tests.

## Reuse Candidates
- `src/catalog/store.py` — existing record schema and create/update persistence helpers; extend these rather than writing new persistence code
- `tests/catalog/test_store.py` — existing persistence test fixtures/patterns for creating and updating records

## Acceptance Criteria
- [ ] The Service Catalog record schema includes an `ownerGroup` field, and it round-trips through persistence
- [ ] Creating a record with `ownerGroup` stores that value
- [ ] Updating a record without `ownerGroup` (missing or empty) keeps the previously stored `ownerGroup`
- [ ] Updating a record with a new non-empty `ownerGroup` replaces the stored value
- [ ] Records stored before this change (no `ownerGroup`) still load without error
- [ ] Record IDs are identical before and after this change for the same input
- [ ] Existing store tests pass unchanged

## Test Requirements
- [ ] `tests/catalog/test_store.py`: create a record with `ownerGroup` and assert it is persisted and read back
- [ ] `tests/catalog/test_store.py`: update the record without `ownerGroup` and assert the original value is preserved
- [ ] `tests/catalog/test_store.py`: update with an empty string `ownerGroup` and assert the original value is preserved
- [ ] `tests/catalog/test_store.py`: update with a new `ownerGroup` and assert it is replaced
- [ ] `tests/catalog/test_store.py`: load a legacy record with no `ownerGroup` and assert it loads with `ownerGroup` unset
- [ ] `tests/catalog/test_store.py`: assert the record ID is unchanged across create and update (stable IDs)

## Verification Commands
- `pytest tests/catalog/test_store.py` — all tests pass

## Dependencies
- None
