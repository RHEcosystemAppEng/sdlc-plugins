## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record schema in `src/catalog/store.py`. The field stores the team or group that owns the service. Persistence helpers must support three operations: setting `ownerGroup` on initial creation, preserving the existing value when an update omits the field, and replacing the value when a new one is explicitly supplied. Stable record IDs must remain unchanged.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` field to the catalog record schema; update persistence helpers for set, preserve-on-omit, and explicit-replace semantics
- `tests/catalog/test_store.py` — add tests for `ownerGroup` persistence behavior

## Implementation Notes
- Review the existing record schema in `src/catalog/store.py` to identify the field definition pattern and add `ownerGroup` consistently.
- The preserve-on-omit behavior means that when an update payload does not include `ownerGroup`, the existing value must be retained — not set to `None` or overwritten with a default.
- Stable IDs: ensure that adding `ownerGroup` does not alter how record IDs are generated or compared.

## Acceptance Criteria
- [ ] `ownerGroup` field is present on the catalog record schema
- [ ] Creating a record with `ownerGroup` persists the value
- [ ] Updating a record without supplying `ownerGroup` preserves the existing value
- [ ] Updating a record with an explicit new `ownerGroup` replaces the existing value
- [ ] Stable record IDs remain unchanged after adding the field

## Test Requirements
- [ ] Test that `ownerGroup` is persisted when set during record creation
- [ ] Test that `ownerGroup` is preserved when an update omits the field
- [ ] Test that `ownerGroup` is replaced when an update supplies a new value
- [ ] Test that record IDs are stable and unaffected by the new field

## Dependencies
- None (first task)
