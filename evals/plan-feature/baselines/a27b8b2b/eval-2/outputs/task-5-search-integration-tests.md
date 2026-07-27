## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests covering the new search filtering, relevance scoring, and paginated response format. The existing tests in `tests/api/search.rs` must be extended to verify the new capabilities introduced by Tasks 1-4.

## Files to Modify
- `tests/api/search.rs` — add integration test cases for filtering by entity type, filtering by date range, relevance score ordering, paginated response format, combined filters, and error cases

## Implementation Notes
- Follow test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests use a real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Test the following scenarios:
  1. **Entity type filter**: search with `entity_type=sbom`, verify only SBOM results returned
  2. **Date range filter**: search with `date_from` and `date_to`, verify results within range
  3. **Combined filters**: search with entity_type AND date range simultaneously
  4. **Relevance ordering**: search with a known term, verify first result is the most relevant
  5. **Pagination**: verify `PaginatedResults` response shape with offset/limit
  6. **No filters**: verify backward compatibility — search without filters returns same results as before
  7. **Error cases**: invalid entity_type returns 400, invalid date format returns 400
- Ensure test data setup includes multiple entity types (sbom, advisory, package) with known values to enable deterministic assertions.
- All test functions should include doc comments explaining the scenario being tested.

## Reuse Candidates
- `tests/api/sbom.rs` — reference integration test patterns including test database setup and HTTP assertion style
- `tests/api/advisory.rs` — another reference for integration test structure
- `tests/api/search.rs` — existing search tests to extend (current test patterns and data setup)

## Acceptance Criteria
- [ ] Integration tests cover entity type filtering (sbom, advisory, package)
- [ ] Integration tests cover date range filtering (date_from, date_to, both)
- [ ] Integration tests cover relevance score ordering
- [ ] Integration tests cover paginated response format
- [ ] Integration tests cover combined filter scenarios
- [ ] Integration tests cover error cases (invalid filter values)
- [ ] All new tests pass against a PostgreSQL test database
- [ ] Existing search tests continue to pass (no regressions)

## Test Requirements
- [ ] At least one test per filter dimension (entity_type, date_from, date_to)
- [ ] At least one test verifying relevance ordering with known test data
- [ ] At least one test verifying PaginatedResults response shape (items array, total count)
- [ ] At least one negative test for invalid query parameters
- [ ] All tests include doc comments explaining the scenario

## Verification Commands
- `cargo test --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Add search result model types
- Depends on: Task 2 — Add filtering parameters to search endpoint
- Depends on: Task 3 — Add relevance scoring to search results
- Depends on: Task 4 — Add database index migration for search performance
