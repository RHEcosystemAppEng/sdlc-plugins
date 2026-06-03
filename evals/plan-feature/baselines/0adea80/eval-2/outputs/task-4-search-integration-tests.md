# Task 4 — Add comprehensive search integration tests

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality introduced
by TC-9002. This task covers end-to-end testing of full-text search with relevance
ranking, filter parameters, pagination interaction, and backward compatibility. While
Tasks 2 and 3 each include test requirements for their specific changes, this task
provides broader cross-cutting integration coverage that exercises the complete search
pipeline from HTTP request through to database query and response.

## Files to Modify
- `tests/api/search.rs` — add integration tests for full-text search relevance ranking, filter parameters, combined filter+search queries, pagination with filters, and backward compatibility

## Implementation Notes
- Inspect the existing tests in `tests/api/search.rs` to understand the test setup pattern, database seeding approach, and assertion style before adding new tests.
- Follow the existing integration test pattern: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
- Test setup should seed the database with:
  - Multiple SBOMs with varying names and descriptions (for relevance ranking tests)
  - Advisories with different severity levels (for severity filter tests)
  - Packages with different licenses (for license filter tests)
- Test categories to cover:
  1. **Relevance ranking**: verify that exact title matches rank higher than partial/description matches
  2. **Filter correctness**: verify each filter individually (entity_type, severity, license)
  3. **Filter combinations**: verify AND-combination of multiple filters
  4. **Pagination with filters**: verify offset/limit work correctly when filters reduce the result set
  5. **Backward compatibility**: verify that requests without any new parameters return the same results as before
  6. **Edge cases**: empty search string, no results, special characters in search query
- Also inspect `tests/api/sbom.rs` and `tests/api/advisory.rs` for patterns on seeding test data and making API requests in the test harness.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits, reference TC-9002, and include the Assisted-by trailer.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing test code before modifying; prefer parameterized tests when multiple cases exercise the same behavior with different inputs (per §5.9); add doc comments to every test function (per §5.11).

## Reuse Candidates
- `tests/api/search.rs` — existing search endpoint integration tests; follow the same setup/assertion patterns
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test data seeding patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests; reference for test data seeding and assertion patterns

## Acceptance Criteria
- [ ] Integration tests cover full-text search relevance ranking
- [ ] Integration tests cover each filter parameter individually
- [ ] Integration tests cover combined filter and search queries
- [ ] Integration tests cover pagination with filters (total count, offset, limit)
- [ ] Integration tests verify backward compatibility with existing API contract
- [ ] Integration tests cover edge cases (empty query, no results, special characters)
- [ ] All new test functions have doc comments
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] All new tests pass: `cargo test --test search`
- [ ] Existing tests continue to pass (no regressions): `cargo test`
- [ ] Tests are structured with clear given-when-then phases for non-trivial test functions

## Verification Commands
- `cargo test --test search` — all search integration tests pass
- `cargo test` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add filter query parameters to the search endpoint
