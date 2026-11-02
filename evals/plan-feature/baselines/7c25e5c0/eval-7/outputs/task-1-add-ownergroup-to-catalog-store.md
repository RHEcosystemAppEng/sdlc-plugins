## Repository
catalog-service

## Target Branch
main

## Description
Add the `ownerGroup` field to the shared Service Catalog record schema and persistence helpers in `src/catalog/store.py`. This is the foundation for all subsequent writer and consumer changes. The field must be stored as a string, with persistence helpers updated to read and write `ownerGroup` while preserving existing catalog population behavior and stable IDs.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` field to catalog record schema and update persistence helpers to read/write the new field
- `tests/catalog/test_store.py` — add tests for `ownerGroup` persistence, omitted-update preservation, explicit replacement, and unchanged stable IDs

## Implementation Notes
- Follow the existing field pattern in `src/catalog/store.py` for adding a new field to the record schema
- The `ownerGroup` field should default to `None` for backward compatibility with existing records
- Persistence helpers must support three operations:
  1. **Set**: persist a supplied `ownerGroup` value on new records
  2. **Preserve**: when an update omits `ownerGroup`, keep the current value unchanged
  3. **Replace**: when an update supplies a new `ownerGroup`, overwrite the existing value
- Stable IDs must remain unchanged — adding `ownerGroup` must not alter ID generation logic

## Acceptance Criteria
- [ ] `src/catalog/store.py` record schema includes an `ownerGroup` field (string, nullable)
- [ ] Persistence helpers correctly store `ownerGroup` when provided
- [ ] Persistence helpers preserve existing `ownerGroup` when update omits the field
- [ ] Persistence helpers replace `ownerGroup` when update supplies a new value
- [ ] Existing catalog record IDs remain stable after the schema change
- [ ] Existing population behavior (records without `ownerGroup`) is not broken

## Test Requirements
- [ ] Test that a new record with `ownerGroup` persists the value correctly in `tests/catalog/test_store.py`
- [ ] Test that updating a record without supplying `ownerGroup` preserves the existing value in `tests/catalog/test_store.py`
- [ ] Test that updating a record with a new `ownerGroup` replaces the existing value in `tests/catalog/test_store.py`
- [ ] Test that stable IDs remain unchanged after adding `ownerGroup` in `tests/catalog/test_store.py`

## Dependencies
- None (first task)
