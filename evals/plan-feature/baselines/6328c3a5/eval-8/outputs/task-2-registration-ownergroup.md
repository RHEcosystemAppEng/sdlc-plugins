## Repository
catalog-service

## Target Branch
main

## Description
Update the registration workflow in `src/workflows/registration.py` to collect and persist the `ownerGroup` field when a service is added to the catalog during initial onboarding. This is the primary population path identified by the stakeholder. After this change, every service record created through the registration workflow will include its `ownerGroup`.

Note: This task covers only the registration workflow. Other population paths (scheduled synchronization, fallback import, on-demand refresh) are excluded from scope per stakeholder instruction. Records populated through those paths will not have `ownerGroup` set -- see the impact map for the unresolved scope conflict.

## Files to Modify
- `src/workflows/registration.py` -- accept `ownerGroup` as a parameter during registration and pass it to the catalog store when creating the record
- `tests/workflows/test_registration.py` -- add tests verifying `ownerGroup` is collected and persisted during registration

## Implementation Notes
- Inspect `src/workflows/registration.py` to understand the current registration flow -- how it receives input, validates it, and calls `src/catalog/store.py` to create a record.
- Add `ownerGroup` as a required parameter to the registration entry point. Follow the existing parameter pattern (function arguments, request object, etc.).
- Pass `ownerGroup` through to the catalog store's record creation method.
- Inspect existing tests in `tests/workflows/test_registration.py` to follow the established test patterns (fixtures, mocking, assertion style).

## Acceptance Criteria
- [ ] The registration workflow accepts an `ownerGroup` value as input
- [ ] A service record created through registration includes the supplied `ownerGroup`
- [ ] Registration fails or rejects the request if `ownerGroup` is not provided (if the field is required)

## Test Requirements
- [ ] Test that a service registered with `ownerGroup` has the value stored in the catalog record
- [ ] Test that the registration workflow passes `ownerGroup` to the catalog store
- [ ] Test the behavior when `ownerGroup` is missing from registration input (error handling or default behavior, depending on field requirements)

## Dependencies
- Depends on: Task 1 -- Add ownerGroup field to catalog record schema
