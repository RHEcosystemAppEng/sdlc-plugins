## Repository
catalog-service

## Target Branch
main

## Description
Update the registration workflow in `src/workflows/registration.py` to collect and persist the `ownerGroup` value when a service is initially registered. The registration flow is the primary onboarding path and should pass `ownerGroup` through to the catalog store.

## Files to Modify
- `src/workflows/registration.py` — accept `ownerGroup` parameter and pass it to the catalog store during record creation
- `tests/workflows/test_registration.py` — add tests verifying `ownerGroup` is captured during registration

## Implementation Notes
- Review the existing registration workflow in `src/workflows/registration.py` to understand how it calls into `src/catalog/store.py` for record creation.
- Ensure the `ownerGroup` value is passed through to the store's create method added in Task 1.
- The registration path is the only writer path in scope per stakeholder instruction.

## Acceptance Criteria
- [ ] Registration workflow accepts an `ownerGroup` parameter
- [ ] The supplied `ownerGroup` is persisted on the created catalog record
- [ ] Registration without `ownerGroup` still succeeds (backward compatibility)

## Test Requirements
- [ ] Test that registering a service with `ownerGroup` persists the value on the catalog record
- [ ] Test that registering a service without `ownerGroup` does not break (backward compatibility)

## Dependencies
- Depends on: Task 1 — Add ownerGroup to catalog store
