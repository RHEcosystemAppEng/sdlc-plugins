# Task 2 — Collect ownerGroup during initial service registration

**Summary:** TC-9007: Collect and persist `ownerGroup` in the onboarding registration workflow
**Issue type:** Task | **Parent Epic:** TC-9007: Owner group data model and onboarding
**Labels:** ai-generated-jira | **Priority:** Major | **Fix Versions:** (none — Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
The onboarding registration workflow must accept an `ownerGroup` when a service is first registered and store it on the new Service Catalog record through the shared store helpers from Task 1. This covers the Feature requirement "A registered service record includes its `ownerGroup`" for records created through onboarding.

Scope note: this task covers the registration writer only. Scheduled sync, fallback import, and on-demand refresh also write catalog records, but they are excluded by stakeholder instruction and listed as an unresolved scope conflict in the TC-9007 impact map. Completing this task does **not** satisfy AC1 ("every record has an `ownerGroup` after creation or update") for records written by those paths.

## Files to Modify
- `src/workflows/registration.py` — accept `ownerGroup` as a registration input and pass it to the catalog store when the record is created
- `tests/workflows/test_registration.py` — add registration tests for `ownerGroup`

## Implementation Notes
- Thread `ownerGroup` through the existing registration entry point in `src/workflows/registration.py` and into the existing store create call. Do not write to storage directly; use the `src/catalog/store.py` helpers extended in Task 1.
- Onboarding is where the value is first collected, so registration must reject a missing or empty `ownerGroup` with the workflow's existing validation-error mechanism. It must not create a record with no owner group. The check belongs at the start of the registration function, before the store call.
- Do not change how registration derives the record ID or any other registration behavior.
- Constraints (docs/constraints.md): §2 Conventional Commits with the Jira footer and `Assisted-by:` trailer; §3 task-ID branch, `--base main`, PR link posted to Jira; §5 stay within the listed files, reuse store helpers, add doc and given-when-then comments to tests.

## Reuse Candidates
- `src/catalog/store.py` — create helper with `ownerGroup` support (from Task 1)
- `tests/workflows/test_registration.py` — existing registration fixtures and assertions; extend these

## Acceptance Criteria
- [ ] Registering a service with an `ownerGroup` creates a catalog record that stores that `ownerGroup`
- [ ] Registration with a missing or empty `ownerGroup` fails with a validation error, and no catalog record is created
- [ ] Record IDs assigned by registration are unchanged for the same input
- [ ] Existing registration tests pass

## Test Requirements
- [ ] `tests/workflows/test_registration.py`: register a service with `ownerGroup` and assert the stored record contains it
- [ ] `tests/workflows/test_registration.py`: register without `ownerGroup` (and with an empty string) and assert a validation error is raised and no record is persisted
- [ ] `tests/workflows/test_registration.py`: assert the registered record's ID matches the pre-change ID for the same input

## Verification Commands
- `pytest tests/workflows/test_registration.py` — all tests pass

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
