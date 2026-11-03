# Task 2 — Collect `ownerGroup` during service registration

**Labels**: ai-generated-jira
**Priority**: Major (inherited from TC-9007)
**Fix Versions**: (omitted — TC-9007 has no fixVersions)

## Repository
catalog-service

## Target Branch
main

## Description
Collect `ownerGroup` in the initial onboarding (registration) workflow and store it on the new Service Catalog record through the store helpers from Task 1. This covers the TC-9007 requirement "A registered service record includes its `ownerGroup` — collected during initial onboarding."

**Scope note:** This task covers the primary (onboarding) writer only. Other workflows that populate the shared catalog record are outside the stakeholder-approved scope. Their coverage is an open question in the TC-9007 impact map, so this task must not be treated as proof that every catalog record has an `ownerGroup`.

## Files to Modify
- `src/workflows/registration.py` — accept `ownerGroup` as registration input and pass it to the store create helper
- `tests/workflows/test_registration.py` — add registration tests for `ownerGroup`

## Implementation Notes
- `src/workflows/registration.py` adds a service to the catalog during initial registration. Add `ownerGroup` to the registration input alongside the existing fields and pass it to the `src/catalog/store.py` create helper extended in Task 1. Do not write the record directly.
- Registration is the point where the record is first created, so a newly registered record must not be left without an owner group. If `ownerGroup` is missing or empty, reject the registration with the workflow's existing validation-error pattern. Do not silently create a record without it.
- Keep the existing registration behavior unchanged, including how stable IDs are assigned.
- Constraints (docs/constraints.md):
  - §1.4/§1.5/§1.6: scoped changes, inspect before modifying, ask if this description is incomplete.
  - §2.1–2.3: Conventional Commits, Jira footer, Assisted-by trailer.
  - §3.1–3.3: branch named after the task key, PR link posted to Jira, `--base main`.
  - §5.1–5.8: only the listed files, reuse the store helpers, trace the data flow from registration input to the persisted record.

## Reuse Candidates
- `src/catalog/store.py` — create helper (extended with `ownerGroup` in Task 1)
- `src/workflows/registration.py` — existing input validation pattern for required registration fields

## Acceptance Criteria
- [ ] Registering a service with an `ownerGroup` creates a catalog record that contains that `ownerGroup`
- [ ] Registering a service without an `ownerGroup`, or with an empty one, is rejected using the existing validation pattern, and no record is created
- [ ] Existing registration behavior and stable ID assignment are unchanged

## Test Requirements
- [ ] `tests/workflows/test_registration.py`: register with `ownerGroup` and assert the stored record has the supplied value
- [ ] `tests/workflows/test_registration.py`: register without `ownerGroup` and assert a validation error and that no catalog record is created
- [ ] `tests/workflows/test_registration.py`: assert the registered record's ID matches the existing ID-assignment behavior
- [ ] Existing tests in `tests/workflows/test_registration.py` still pass

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to the Service Catalog record schema and persistence helpers
