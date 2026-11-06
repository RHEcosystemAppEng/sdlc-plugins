# Task 1 — Add ownerGroup to the shared Service Catalog record schema

**Summary:** TC-9007: Add `ownerGroup` to Service Catalog record schema and persistence helpers
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Epic group (by-sub-feature, pending approval):** TC-9007: Owner group onboarding

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so every service record can carry the group that owns it (TC-9007). The persistence helpers must preserve the existing `ownerGroup` when a record is updated without a new value, and overwrite it only when a new value is supplied. Stable record IDs and existing population behavior must remain unchanged.

This task is limited to the shared schema and persistence layer. Note: per the TC-9007 impact map, whether the scheduled sync, fallback import, and on-demand refresh writers route through these helpers is an **unresolved scope question** and is not covered by this task.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the catalog record schema; update create/update persistence helpers so updates preserve the current `ownerGroup` unless a new value is supplied
- `tests/catalog/test_store.py` — add persistence tests for `ownerGroup`

## Implementation Notes
- `src/catalog/store.py` is the single shared schema and persistence module for Service Catalog records; extend the existing record definition and helpers rather than introducing a parallel record type.
- Update semantics: when an update payload omits `ownerGroup` (or supplies `None`), keep the stored value; when a non-empty value is supplied, replace it. Implement this merge in the existing update helper so any caller that uses the helper inherits the behavior.
- Do not change how record IDs are generated or assigned — stable IDs must be identical before and after this change.
- Records persisted before this change will have no `ownerGroup`; reads must tolerate an absent value (return `None`/empty) rather than raising, so consumers in Tasks 3 and 4 can render safely.
- Follow the existing test structure in `tests/catalog/test_store.py`.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits, `Implements TC-<task-key>` footer, `Assisted-by:` trailer.
  - §3 PR rules: branch named after the task issue ID; `gh pr create --base main`; post PR link to the Jira task.
  - §5 Code change rules: limit changes to Files to Modify; inspect code before modifying; reuse existing helpers (§5.4); trace the data flow end-to-end (§5.6).
  - §1 Skill scope rules applicable to implement-task.

## Reuse Candidates
- `src/catalog/store.py` — existing record schema and persistence helpers; extend in place for the new field and preserve-on-update merge

## Acceptance Criteria
- [ ] The Service Catalog record schema includes an `ownerGroup` field
- [ ] Creating a record with an `ownerGroup` persists the value
- [ ] Updating a record without supplying `ownerGroup` preserves the current value
- [ ] Updating a record with a new `ownerGroup` replaces the stored value
- [ ] Stable record IDs are unchanged by create and update operations
- [ ] Reading a legacy record without `ownerGroup` does not error

## Test Requirements
- [ ] `tests/catalog/test_store.py`: create a record with `ownerGroup` and assert it is persisted and read back
- [ ] `tests/catalog/test_store.py`: update a record without `ownerGroup` and assert the previous value is preserved
- [ ] `tests/catalog/test_store.py`: update a record with a new `ownerGroup` and assert it is replaced
- [ ] `tests/catalog/test_store.py`: assert the record ID is identical before and after update (stable IDs unchanged)
- [ ] `tests/catalog/test_store.py`: read a record stored without `ownerGroup` and assert no error and an empty value

## Dependencies
- None
