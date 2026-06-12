# Task 4 — Expand search integration tests for filtering, ranking, and performance

## Repository
trustify-backend

## Target Branch
main

## Description
Expand the search integration test suite in `tests/api/search.rs` to provide comprehensive coverage for the new filtering, relevance ranking, and performance improvements introduced by Tasks 1-3. While each prior task includes test requirements for its specific scope, this task consolidates end-to-end and cross-cutting test scenarios that verify the combined behavior of all search improvements.

## Files to Modify
- `tests/api/search.rs` — Add integration tests covering combined filter + ranking scenarios, edge cases, backward compatibility, and performance characteristics

## Implementation Notes
- Follow the existing test patterns in `tests/api/search.rs` — use the `assert_eq!(resp.status(), StatusCode::OK)` pattern documented in the repository conventions.
- Tests hit a real PostgreSQL test database (per repository conventions). Set up test data that includes multiple SBOMs, advisories, and packages with varying dates, severities, and text content to exercise filtering and ranking thoroughly.
- Test scenarios to cover:
  - **Combined filters + ranking:** Apply entity_type filter with a search query and verify results are both filtered and relevance-ranked
  - **Empty result sets:** Apply filters that match no entities and verify empty `PaginatedResults` response
  - **Pagination with filters:** Verify that pagination works correctly when filters reduce the total result count
  - **Date boundary conditions:** Test date_from and date_to with exact boundary dates to verify inclusive/exclusive behavior
  - **Severity filter with no advisory results:** Apply severity filter when no advisories match — verify clean empty response
  - **Backward compatibility:** Verify that existing search queries (no filters, no sort parameter) return results consistent with pre-feature behavior
- Reference `PaginatedResults<T>` from `common/src/model/paginated.rs` for response shape assertions.
- Per docs/constraints.md Section 2 (Commit Rules): use Conventional Commits format and reference TC-9002 in the commit footer.
- Per docs/constraints.md Section 5 (Code Change Rules): inspect existing code before modifying, follow patterns found in the codebase.

## Reuse Candidates
- `tests/api/search.rs` — existing search test patterns and test database setup; extend rather than rewrite
- `tests/api/sbom.rs` — example of SBOM endpoint integration tests; reference for test data setup patterns
- `tests/api/advisory.rs` — example of advisory endpoint integration tests; reference for advisory-specific test data

## Acceptance Criteria
- [ ] Integration tests cover combined filter + relevance ranking scenarios
- [ ] Integration tests cover pagination with active filters
- [ ] Integration tests cover edge cases (empty results, boundary dates, invalid combinations)
- [ ] Integration tests verify backward compatibility of the search endpoint
- [ ] All tests pass against the test database

## Test Requirements
- [ ] At least 5 new integration test functions covering the cross-cutting scenarios described above
- [ ] Tests use representative test data with enough variety to exercise filtering and ranking meaningfully
- [ ] Each test function has a doc comment explaining what scenario it covers

## Verification Commands
- `cargo test -p tests --test search` — all search tests pass
- `cargo test -p tests` — full integration test suite passes (no regressions)

## Dependencies
- Depends on: Task 1 — Add full-text search indexes for searchable entities
- Depends on: Task 2 — Implement relevance ranking for search results
- Depends on: Task 3 — Add filter parameters to the search endpoint
