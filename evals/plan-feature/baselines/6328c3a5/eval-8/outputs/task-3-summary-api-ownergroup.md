## Repository
catalog-service

## Target Branch
main

## Description
Update the catalog summary API in `src/api/catalog_summary.py` to include the `ownerGroup` field when reading and returning Service Catalog records. After this change, API consumers will see `ownerGroup` in the summary response for any record that has the field populated.

Note: The summary API reads the shared Service Catalog. It will display `ownerGroup` for records that have the value set (currently only those created through the registration workflow). Records populated through excluded paths (scheduled synchronization, fallback import, on-demand refresh) will not have `ownerGroup` until those paths are brought into scope -- see the impact map for the unresolved scope conflict.

## Files to Modify
- `src/api/catalog_summary.py` -- include `ownerGroup` in the API response when reading catalog records
- `tests/api/test_catalog_summary.py` -- add tests verifying `ownerGroup` appears in the summary API response

## API Changes
- `GET /api/catalog/summary` (or equivalent endpoint) -- MODIFY: response includes `ownerGroup` field for each catalog record

## Implementation Notes
- Inspect `src/api/catalog_summary.py` to understand how catalog records are read from the store and serialized into the API response.
- Add `ownerGroup` to the response serialization. Follow the existing field inclusion pattern.
- Inspect existing tests in `tests/api/test_catalog_summary.py` to follow the established test patterns for API response assertions.

## Acceptance Criteria
- [ ] The summary API response includes `ownerGroup` for catalog records that have the field set
- [ ] The summary API response handles records without `ownerGroup` gracefully (e.g., returns null or omits the field)
- [ ] Existing summary API behavior for other fields remains unchanged

## Test Requirements
- [ ] Test that the summary API includes `ownerGroup` in the response for a record that has it set
- [ ] Test that the summary API handles a record without `ownerGroup` without error
- [ ] Test that existing summary API response fields are not affected

## Dependencies
- Depends on: Task 1 -- Add ownerGroup field to catalog record schema
