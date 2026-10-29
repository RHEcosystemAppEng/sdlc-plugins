## Repository
catalog-service

## Target Branch
main

## Description
Collect the `ownerGroup` value during the initial service registration workflow and persist it to the Service Catalog record. This is the primary writer path identified in TC-9007's scope. During onboarding, the registration flow must accept `ownerGroup` as an input and pass it through to the catalog record creation in `store.py`.

## Files to Modify
- `src/workflows/registration.py` — add `ownerGroup` parameter to the registration workflow and pass it to the catalog record creation call
- `tests/workflows/test_registration.py` — add tests for `ownerGroup` collection during registration

## Implementation Notes
- Inspect the existing registration flow in `src/workflows/registration.py` to understand how it creates catalog records via `store.py`.
- Add `ownerGroup` as a parameter to the registration entry point or data class that feeds into record creation.
- Pass `ownerGroup` through to the `store.py` record creation call so it is persisted in the catalog.
- Follow the existing parameter patterns in `registration.py` for how other fields are collected and forwarded.
- Note: this task covers only the registration path. Other population paths (scheduled sync, fallback import, on-demand refresh) are excluded from current scope per stakeholder instruction. See the impact map for the unresolved scope conflict.

## Acceptance Criteria
- [ ] The registration workflow in `src/workflows/registration.py` accepts an `ownerGroup` parameter
- [ ] A registered service record includes `ownerGroup` in the resulting catalog record
- [ ] The `ownerGroup` value is persisted correctly through the catalog store

## Test Requirements
- [ ] Test that registration with a valid `ownerGroup` creates a catalog record containing that `ownerGroup`
- [ ] Test that the `ownerGroup` value persisted during registration matches the input value
- [ ] Test registration behavior when `ownerGroup` is provided as an input parameter

## Dependencies
- Depends on: Task 1 — Add ownerGroup field to catalog record schema
