## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record schema in `src/catalog/store.py`. This field stores which group owns a given service. The field must be included in the record schema so that all writers and consumers can reference it. Update semantics must preserve the current `ownerGroup` value unless a new value is explicitly supplied, ensuring that partial updates from any writer do not erase the field.

This task covers only the schema definition and persistence layer. Population of the field during specific workflows and display of the field in consumers are handled by separate tasks.

## Files to Modify
- `src/catalog/store.py` -- add `ownerGroup` field to the catalog record schema; add update-preservation logic so partial updates do not overwrite existing values
- `tests/catalog/test_store.py` -- add tests for the new field and update-preservation semantics

## Implementation Notes
- Inspect the existing record schema in `src/catalog/store.py` to determine the field definition pattern (e.g., dataclass, TypedDict, Pydantic model) and follow the same pattern for `ownerGroup`.
- The `ownerGroup` field should be a string type. Determine nullability by inspecting how existing optional fields are handled in the schema.
- Implement update-preservation: when a record is updated, the `ownerGroup` value must be kept unless the caller supplies a new value. Look at how existing fields handle partial updates in the persistence helpers and follow the same pattern.
- Ensure existing tests continue to pass -- the new field must not break existing persistence behavior or stable IDs.

## Acceptance Criteria
- [ ] The catalog record schema in `src/catalog/store.py` includes an `ownerGroup` field
- [ ] Updating a record without supplying `ownerGroup` preserves the existing value
- [ ] Updating a record with a new `ownerGroup` value overwrites the previous value
- [ ] Existing catalog persistence behavior and stable IDs remain unchanged

## Test Requirements
- [ ] Test that a new catalog record can be created with an `ownerGroup` value
- [ ] Test that updating a record without supplying `ownerGroup` retains the original value
- [ ] Test that updating a record with a new `ownerGroup` value stores the new value
- [ ] Test that existing records without `ownerGroup` are handled gracefully (backward compatibility)

## Dependencies
- None
