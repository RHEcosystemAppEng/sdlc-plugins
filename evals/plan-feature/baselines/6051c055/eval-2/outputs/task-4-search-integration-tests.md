## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality introduced by the preceding tasks (full-text search indexes, relevance ranking, and filters). While each prior task includes basic test requirements, this task creates a dedicated, thorough test suite covering edge cases, error conditions, and cross-feature interactions that span all search improvements.

Per the repo's CONVENTIONS.md, integration tests live in `tests/api/` and run against a real PostgreSQL database. This task follows that established pattern.

## Files to Modify
- `tests/api/search.rs` — Add new test cases covering edge cases, error conditions, cross-feature interactions, and performance characteristics of the improved search

## Files to Create
None.

## Implementation Notes
- Per the repo's CONVENTIONS.md, integration tests are placed in `tests/api/` and use a real PostgreSQL instance. All new tests must follow the existing test setup/teardown patterns found in `tests/api/search.rs`.
- Per the repo's CONVENTIONS.md, error handling uses `Result<T, AppError>` with `.context()`. Tests should verify that error responses use the `AppError` format with appropriate HTTP status codes.
- Tests should use the existing test database setup infrastructure (likely a shared test fixture or per-test database).
- Each test should be independent and not rely on ordering or shared state from other tests.
- ASSUMPTION (pending clarification): The test database setup pattern (fixture creation, seed data insertion) follows whatever pattern is already established in `tests/api/search.rs`. New tests should reuse the same helpers.
- Test categories to cover:
  - **Empty results:** search with no matches returns empty array, not an error
  - **Special characters:** search queries with SQL-special characters (`'`, `"`, `;`, `--`) are handled safely (no SQL injection)
  - **Unicode:** search queries with Unicode characters return correct results
  - **Pagination interaction:** filters and relevance ranking work correctly with pagination parameters
  - **Filter edge cases:** date_from equals date_to, severity with mixed case, unknown type value
  - **Relevance edge cases:** query matches multiple fields in the same document, very long queries

## Acceptance Criteria
- [ ] All new integration tests pass against a real PostgreSQL database
- [ ] Edge cases for empty results, special characters, and Unicode are covered
- [ ] Cross-feature interactions (filters + relevance ranking + pagination) are tested
- [ ] Error conditions (invalid parameters, malformed queries) are tested
- [ ] No existing tests are broken by the new test additions
- [ ] Tests are independent and do not rely on execution order

## Test Requirements
- [ ] Test: empty search query returns all results (or a defined default behavior)
- [ ] Test: search with no matching results returns 200 with empty results array
- [ ] Test: search query with SQL-special characters does not cause errors or injection
- [ ] Test: search query with Unicode characters returns correct matches
- [ ] Test: combining filters with relevance sorting returns correctly filtered and ordered results
- [ ] Test: pagination (offset/limit) works correctly with filters applied
- [ ] Test: invalid `date_from` > `date_to` returns 400 error
- [ ] Test: unknown `type` filter value returns 400 or empty results (per chosen behavior)
