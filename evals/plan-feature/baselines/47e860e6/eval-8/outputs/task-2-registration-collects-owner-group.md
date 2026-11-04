# Task 2 — Collect `ownerGroup` during initial service registration

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (omitted — TC-9007 has no fixVersions)
**Parent / Epic:** TC-9007: Owner group capture (if Epic type available)

## Repository
catalog-service

## Target Branch
main

## Description
Extend the initial onboarding (registration) workflow so that a newly registered service record includes its `ownerGroup` (TC-9007 MVP requirement: "A registered service record includes its `ownerGroup` — collected during initial onboarding"). The registration workflow in `src/workflows/registration.py` is the primary writer that first adds a service to the shared Service Catalog; it must accept `ownerGroup` as part of the registration input and persist it via the store helpers extended in Task 1.

**Scope note (TC-9007 scope conflict):** this task covers only the registration writer. It satisfies the "after creation" half of the Feature AC for records created through registration. Records created or updated by other population paths are out of this plan's scope and remain UNRESOLVED in the TC-9007 impact map.

## Files to Modify
- `src/workflows/registration.py` — accept `ownerGroup` in the registration input, validate it, and pass it to the catalog store when creating the record
- `tests/workflows/test_registration.py` — add tests for registration with `ownerGroup`, validation of missing/invalid values, and unchanged stable IDs

## Implementation Notes
- In `src/workflows/registration.py`, add `ownerGroup` to the registration input handled by the existing registration entry point and forward it to the catalog record creation call in `src/catalog/store.py` (field added in Task 1). Reuse the store's create helper — do not write the record directly.
- Since the Feature AC requires every record to have an `ownerGroup` after creation, registration must reject (with the workflow's existing validation-error pattern) a registration request that omits `ownerGroup` or supplies an empty value, rather than persisting a record without it.
- Do not alter how registration derives the stable record ID or any other existing field.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits; footer `Implements <task-key>`; `--trailer="Assisted-by: Claude Code"`.
  - §3 PR rules: branch named after the task issue ID; `gh pr create --base main`; post PR link on the Jira task.
  - §5 Code change rules: only the files listed above (5.1); inspect before modifying (5.2); follow the existing validation pattern in `src/workflows/registration.py` (5.3); trace `ownerGroup` from registration input → store → persisted record (5.6).
  - §1.4/1.5: keep changes scoped; inspect code before modifying.

## Reuse Candidates
- `src/catalog/store.py` — record creation helper and `ownerGroup` schema field from Task 1
- `src/workflows/registration.py` — existing input validation and error-reporting pattern; reuse for `ownerGroup` validation
- `tests/workflows/test_registration.py` — existing registration fixtures; extend rather than duplicate

## Acceptance Criteria
- [ ] Registering a service with an `ownerGroup` creates a catalog record whose `ownerGroup` equals the supplied value
- [ ] Registering a service without an `ownerGroup` (or with an empty value) is rejected using the existing registration validation-error behavior and no record is persisted
- [ ] Registration still assigns the same stable ID and existing fields as before this change

## Test Requirements
- [ ] `tests/workflows/test_registration.py`: register a service with `ownerGroup` and assert the persisted catalog record contains it
- [ ] `tests/workflows/test_registration.py`: register a service without `ownerGroup` and assert a validation error and no persisted record
- [ ] `tests/workflows/test_registration.py`: register a service with an empty `ownerGroup` and assert a validation error
- [ ] `tests/workflows/test_registration.py`: assert the stable ID and existing fields of a registered record are unchanged compared with pre-change behavior

## Verification Commands
- `pytest tests/workflows/test_registration.py` — all tests pass

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to the shared Service Catalog record schema with preserve-on-update semantics
