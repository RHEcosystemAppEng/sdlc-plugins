# Task 6 — Add comprehensive integration tests for search improvements

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests covering the full search improvement feature: relevance ranking, filtering, pagination, and edge cases. While individual tasks include unit and targeted integration tests, this task adds end-to-end integration tests that exercise the complete search flow — from indexed data through query ranking, filtering, and paginated response — to ensure all components work together correctly.

## Files to Modify
- `tests/api/search.rs` — add new integration test functions covering relevance ranking, filtering, pagination, edge cases, and backward compatibility

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs` — use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern established in the codebase.
- Also reference patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test data setup and assertion conventions.
- Tests should run against a real PostgreSQL test database, consistent with the project's testing convention.
- Test data setup: create a mix of SBOMs, advisories (with varying severities), and packages with known names and descriptions so that relevance ranking can be deterministically verified.
- Key test scenarios to cover:
  1. **Relevance ranking**: insert items where a search term appears in the name of one item and only in the description of another — verify the name-match ranks higher.
  2. **Entity type filter**: search with `entity_type=advisory` — verify only advisories are returned.
  3. **Severity filter**: search with `entity_type=advisory&severity=critical` — verify only critical advisories appear.
  4. **Date range filter**: insert items with known creation dates — verify `created_after` and `created_before` narrow results correctly.
  5. **Combined filters**: apply entity type + severity + date range together — verify correct intersection.
  6. **Pagination**: verify `offset` and `limit` produce correct pages with accurate `total` count.
  7. **Empty results**: search for a nonexistent term — verify empty results array with 200 status (not 404).
  8. **Backward compatibility**: search without any new parameters — verify response structure and results match pre-improvement behavior.
  9. **Invalid input**: invalid date format, unknown entity type — verify 400 Bad Request responses.
- Error handling: ensure all error paths return appropriate HTTP status codes and error messages.

## Reuse Candidates
- `tests/api/search.rs` — existing search integration tests to extend (follow same setup/teardown patterns)
- `tests/api/sbom.rs` — SBOM endpoint test patterns for data setup and assertion style
- `tests/api/advisory.rs` — advisory endpoint test patterns, especially for severity-related assertions

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Relevance ranking test verifies name matches rank above description matches
- [ ] Filter tests verify each filter dimension independently and in combination
- [ ] Pagination tests verify correct page boundaries and total count
- [ ] Backward compatibility test confirms no regressions in existing search behavior
- [ ] Edge case tests (empty results, invalid input) return correct status codes

## Test Requirements
- [ ] At least 9 integration test functions covering the scenarios listed in Implementation Notes
- [ ] Each test function includes a doc comment explaining what scenario it tests
- [ ] Tests use deterministic test data so ranking and filtering results are predictable

## Verification Commands
- `cargo test -p tests -- search --test-threads=1` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration (indexes must exist)
- Depends on: Task 2 — Add search result model types with relevance scoring (response types must exist)
- Depends on: Task 3 — Implement weighted full-text search ranking (ranking logic must be implemented)
- Depends on: Task 4 — Add filter query parameters to the search endpoint (filters must be implemented)
- Depends on: Task 5 — Update search endpoint response to use PaginatedResults (pagination must be implemented)
