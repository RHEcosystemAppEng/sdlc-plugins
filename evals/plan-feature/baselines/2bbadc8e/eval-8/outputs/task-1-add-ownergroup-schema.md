## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record schema. This is the foundational change for TC-9007: all downstream tasks (registration collection, API display, report display) depend on this field existing in the catalog record. The field must support update-preserving semantics — when a record is updated, the current `ownerGroup` value is retained unless a new value is explicitly supplied.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` field to the catalog record schema and update persistence helpers to handle the new field with update-preserving semantics
- `tests/catalog/test_store.py` — add tests for the new field

## Implementation Notes
- Add `ownerGroup` as a string field to the catalog record schema/model in `src/catalog/store.py`.
- Implement update-preserving semantics: when updating a record, if `ownerGroup` is not supplied in the update payload, retain the existing value. If supplied, overwrite with the new value.
- Ensure that existing catalog population behavior and stable IDs remain unchanged — the new field must not affect record identity or existing persistence logic.
- Follow the existing field patterns in `store.py` for naming, type annotations, and default values.
- Existing records that lack `ownerGroup` should be handled gracefully (e.g., default to `None`/`null`).

## Acceptance Criteria
- [ ] The catalog record schema in `src/catalog/store.py` includes an `ownerGroup` field
- [ ] A new record can be created with an `ownerGroup` value
- [ ] A new record can be created without an `ownerGroup` value (field defaults to `None`/`null`)
- [ ] Updating a record without supplying `ownerGroup` preserves the existing value
- [ ] Updating a record with a new `ownerGroup` value overwrites the existing value
- [ ] Existing catalog records without `ownerGroup` are handled gracefully (no errors)
- [ ] Stable IDs and existing catalog population behavior remain unchanged

## Test Requirements
- [ ] Test that a catalog record can be created with `ownerGroup` set
- [ ] Test that a catalog record can be created without `ownerGroup` (defaults to `None`/`null`)
- [ ] Test that updating a record without `ownerGroup` in the payload preserves the existing `ownerGroup`
- [ ] Test that updating a record with a new `ownerGroup` replaces the old value
- [ ] Test that existing records without `ownerGroup` do not cause errors when accessed

## Dependencies
- None (this is the foundational task)
