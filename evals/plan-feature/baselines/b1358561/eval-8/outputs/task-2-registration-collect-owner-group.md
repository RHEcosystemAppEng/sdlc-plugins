# Task 2 — Collect ownerGroup during initial service registration

**Summary:** TC-9007: Collect and persist ownerGroup in the registration workflow
**Epic:** TC-9007: Owner group onboarding
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**fixVersions:** omitted (Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
Collect `ownerGroup` in the onboarding (initial registration) flow, so a newly registered service record carries its owner group from the moment it is created. This covers the Feature requirement "A registered service record includes its `ownerGroup`".

Scope note: this task covers the registration writer only. Registration alone does not satisfy the Feature criterion "Every Service Catalog record has an `ownerGroup` value after creation or update" for records populated by other paths. That criterion is recorded as unresolved in the impact map until the stakeholder scope conflict is resolved.

## Files to Modify
- `src/workflows/registration.py`: accept `ownerGroup` as registration input and pass it to the catalog store when the record is created.
- `tests/workflows/test_registration.py`: add registration tests for `ownerGroup`.

## Implementation Notes
- Pass `ownerGroup` through the existing catalog create helper in `src/catalog/store.py` (extended in Task 1). Do not write to persistence directly from the workflow.
- The Feature says `ownerGroup` is collected during onboarding. Validate the input the same way registration already validates its other required fields, and reject registration with a clear validation error when `ownerGroup` is missing or empty. Registration must not create a record without an owner group.
- Do not change how the registration workflow assigns record IDs or its other existing behavior.
- Constraints (docs/constraints.md): §1.4 scoped changes; §2.1–2.3 commit format, Jira footer and `Assisted-by:` trailer; §3.1–3.3 branch/PR rules with `--base main`; §5.1–5.4 listed files only, inspect first, follow existing workflow patterns, reuse store helpers.

## Reuse Candidates
- `src/catalog/store.py`: catalog create helper with `ownerGroup` support (from Task 1).
- `src/workflows/registration.py`: existing input validation pattern for required registration fields.
- `tests/workflows/test_registration.py`: existing registration fixtures.

## Acceptance Criteria
- [ ] Registering a service with an `ownerGroup` persists a catalog record that has that `ownerGroup`.
- [ ] Registering a service without an `ownerGroup`, or with an empty value, fails with a validation error and creates no record.
- [ ] The registered record's ID and other fields are produced exactly as before this change.

## Test Requirements
- [ ] `tests/workflows/test_registration.py`: register with `ownerGroup` and assert the stored catalog record contains the supplied value.
- [ ] `tests/workflows/test_registration.py`: register without `ownerGroup` and assert a validation error and that no record was created.
- [ ] `tests/workflows/test_registration.py`: assert the record ID and other existing fields are unchanged compared with current behavior.
- [ ] Existing registration tests still pass.

## Verification Commands
- `pytest tests/workflows/test_registration.py`: all tests pass.

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
