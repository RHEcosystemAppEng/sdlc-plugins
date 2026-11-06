# Task 2 — Collect ownerGroup during service registration

**Summary:** TC-9007: Collect `ownerGroup` during initial service registration
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Epic group (by-sub-feature, pending approval):** TC-9007: Owner group onboarding

## Repository
catalog-service

## Target Branch
main

## Description
Extend the initial registration (onboarding) workflow so that a newly registered service record includes its `ownerGroup` (TC-9007 MVP requirement: "A registered service record includes its `ownerGroup` — collected during initial onboarding"). Registration must persist the value through the shared catalog helpers added/extended in Task 1, leaving existing registration behavior and stable IDs unchanged.

## Files to Modify
- `src/workflows/registration.py` — accept `ownerGroup` as part of registration input and pass it to the shared catalog persistence helper when the record is created
- `tests/workflows/test_registration.py` — add registration tests for `ownerGroup`

## Implementation Notes
- `src/workflows/registration.py` already adds a service to the catalog during initial registration; thread the `ownerGroup` value through the existing call into `src/catalog/store.py` rather than writing the record directly.
- Decide validation per the acceptance criterion that every record has an `ownerGroup` after creation: registration should reject (or require) a missing/empty `ownerGroup` instead of silently creating a record without one.
- Do not alter how the registration workflow assigns record IDs.
- Follow the existing test structure in `tests/workflows/test_registration.py`.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits, `Implements TC-<task-key>` footer, `Assisted-by:` trailer.
  - §3 PR rules: branch named after the task issue ID; `gh pr create --base main`; post PR link to the Jira task.
  - §5 Code change rules: limit changes to Files to Modify; inspect before modifying; reuse the shared store helpers (§5.4); trace input → persistence → output (§5.6).
  - §1 Skill scope rules applicable to implement-task.

## Reuse Candidates
- `src/catalog/store.py` — shared create helper (extended in Task 1) that persists `ownerGroup`; registration must use it rather than duplicate persistence logic

## Acceptance Criteria
- [ ] Registering a service with an `ownerGroup` creates a catalog record containing that `ownerGroup`
- [ ] Registration without a valid `ownerGroup` is rejected with a clear error rather than creating a record with no owner group
- [ ] Existing registration behavior (other fields, stable IDs) is unchanged

## Test Requirements
- [ ] `tests/workflows/test_registration.py`: register a service with `ownerGroup` and assert the stored catalog record contains it
- [ ] `tests/workflows/test_registration.py`: register a service without `ownerGroup` and assert the registration is rejected and no record is created
- [ ] `tests/workflows/test_registration.py`: assert the registered record's ID and other fields match pre-change behavior

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
