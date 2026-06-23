## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search relevance ranking, entity type filtering, backward compatibility of the existing API contract, and edge cases. These tests validate the changes from Tasks 1-3 and establish a regression safety net for future search improvements.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for relevance-ranked search, entity type filtering, edge cases, and backward compatibility

## Implementation Notes
- Follow the existing test patterns in `tests/api/search.rs` — tests should hit a real PostgreSQL test database per project convention.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests (see `tests/api/sbom.rs` and `tests/api/advisory.rs` for reference patterns).
- Test scenarios should:
  1. Seed test data with known entities (SBOMs, advisories, packages) with distinctive names/descriptions
  2. Execute search queries and validate result ordering, filtering, and pagination
  3. Validate backward compatibility: existing search queries without new parameters should continue working
- Edge cases to test:
  - Empty search query
  - Search query with no matches
  - Search with all filters applied
  - Search with pagination across filtered results

Per CONVENTIONS.md §Testing: integration tests in tests/api/ hit a real PostgreSQL test database.
Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Example integration test patterns for API endpoints. Follow the same test setup, assertion, and teardown patterns.
- `tests/api/advisory.rs` — Additional integration test reference showing how to test list/filter endpoints.

## Acceptance Criteria
- [ ] Integration tests cover relevance-ranked search (results ordered by ts_rank)
- [ ] Integration tests cover entity type filtering (single type, multiple types, no filter)
- [ ] Integration tests cover invalid filter values (400 Bad Request)
- [ ] Integration tests cover edge cases (empty query, no results, pagination with filters)
- [ ] Integration tests verify backward compatibility (existing queries without new params work)
- [ ] All tests pass against the test PostgreSQL database

## Test Requirements
- [ ] Test: search for a term matching multiple entities returns results ordered by relevance
- [ ] Test: search with `type=sbom` filter returns only SBOM results
- [ ] Test: search with `type=advisory,package` filter returns advisory and package results
- [ ] Test: search without type parameter returns all entity types
- [ ] Test: search with `type=invalid` returns 400 status
- [ ] Test: empty search query returns appropriate response
- [ ] Test: search for non-existent term returns empty result set with 200 status
- [ ] Test: pagination parameters work correctly with filtered and ranked results

## Verification Commands
- `cargo test --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 3 — Add search filter support (entity type filter)

[sdlc-workflow] Description digest: sha256-md:1a0179d021efbf0abf76ac70f9ea2594f6e1f57f308f1212382eac5b488de29d
