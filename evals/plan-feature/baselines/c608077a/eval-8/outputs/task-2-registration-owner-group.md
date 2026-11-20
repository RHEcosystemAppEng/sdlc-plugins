# Task 2 — Collect ownerGroup during initial service registration

**Epic:** TC-9007: Owner group capture
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)

## Repository
catalog-service

## Target Branch
main

## Description
Collect `ownerGroup` in the initial registration (onboarding) workflow and persist it on the new Service Catalog record through the shared store helpers from Task 1 (TC-9007, Requirement 1).

Scope note: this covers the primary onboarding writer only. The other writers of the same shared record (scheduled sync, fallback import, on-demand refresh) are excluded by stakeholder instruction and are recorded as unresolved in the TC-9007 impact map. Records created or updated through those paths are not guaranteed an `ownerGroup` by this task.

## Files to Modify
- `src/workflows/registration.py` — accept `ownerGroup` as registration input, validate it, and pass it to the store create helper
- `tests/workflows/test_registration.py` — add registration tests for `ownerGroup`

## Implementation Notes
- Pass `ownerGroup` through the existing create/persist helper in `src/catalog/store.py` (extended in Task 1). Do not write to persistence directly from `registration.py`.
- Registration is the onboarding point where the Feature says the value is "collected", so registration must require a non-empty `ownerGroup`. Reject a missing or blank value with the workflow's existing validation-error pattern instead of silently creating a record without an owner. This avoids a registration that succeeds while leaving the field empty.
- Do not change how registration assigns record IDs.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules (scope changes to listed files, reuse store helpers, trace onboarding input → store → persisted record).

## Reuse Candidates
- `src/catalog/store.py` — record create helper (extended with `ownerGroup` in Task 1)
- `src/workflows/registration.py` — existing input validation and error-reporting pattern for required registration fields
- `tests/workflows/test_registration.py` — existing registration fixtures

## Acceptance Criteria
- [ ] Registering a service with an `ownerGroup` creates a catalog record whose stored `ownerGroup` equals the supplied value
- [ ] Registering a service without an `ownerGroup`, or with a blank one, fails with a validation error and creates no record
- [ ] Registration still assigns record IDs exactly as before

## Test Requirements
- [ ] `tests/workflows/test_registration.py`: successful registration persists `ownerGroup` (assert through the store read helper)
- [ ] `tests/workflows/test_registration.py`: missing `ownerGroup` is rejected and no record is written
- [ ] `tests/workflows/test_registration.py`: blank `ownerGroup` is rejected and no record is written
- [ ] `tests/workflows/test_registration.py`: the registered record's ID matches existing ID generation behavior
- [ ] Existing tests in `tests/workflows/test_registration.py` pass. Update their fixtures to supply `ownerGroup` where registration now requires it.

## Verification Commands
- `pytest tests/workflows/test_registration.py` — all tests pass

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
