# Task 5 — Update search integration tests for ranking, filtering, and caching

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the existing search integration tests in `tests/api/search.rs` to comprehensively cover the new ranked search, filtering, and caching capabilities introduced in Tasks 1-4. The existing test file covers basic search endpoint behavior; this task adds tests for relevance ranking, filter combinations, edge cases, and performance characteristics.

This is the final task in the search improvement feature and ensures that all new behavior is covered by integration tests running against a real PostgreSQL test database, following the project's established testing conventions.

## Files to Modify
- `tests/api/search.rs` — Add integration tests covering:
  - Ranked search results (results ordered by relevance score)
  - Entity type filtering
  - Severity filtering for advisories
  - Date range filtering
  - Combined filter scenarios
  - Edge cases (empty queries, malformed queries, invalid filters)
  - Cache header presence

## Implementation Notes
- Follow the existing test pattern in `tests/api/search.rs`: integration tests hit a real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Reference sibling test files for patterns:
  - `tests/api/sbom.rs` — SBOM endpoint integration tests showing test data setup and assertion patterns
  - `tests/api/advisory.rs` — Advisory endpoint tests showing how to create test advisories with severity fields (needed for severity filter tests)
- Test data setup: create a representative set of SBOMs, advisories, and packages with known searchable content and varying severity levels and dates, so tests can assert specific expected results
- For ranking tests: create entities with different levels of matching text and verify that the entity with the strongest match has the highest score
- For filter tests: create a diverse dataset and verify that applying each filter correctly reduces the result set
- For date range tests: create entities with known timestamps and verify boundary conditions (inclusive/exclusive)
- Per docs/constraints.md section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., testing each entity_type filter value)
- Per docs/constraints.md section 5.11: add a doc comment to every test function
- Per docs/constraints.md section 5.12: add given-when-then inline comments to non-trivial test functions

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests; extend rather than replace to preserve existing coverage
- `tests/api/sbom.rs` — Test data setup patterns and assertion style for SBOM entities
- `tests/api/advisory.rs` — Test data setup patterns for advisory entities with severity fields

## Acceptance Criteria
- [ ] Integration tests cover ranked search result ordering
- [ ] Integration tests cover each filter type individually (entity_type, severity, date_from, date_to)
- [ ] Integration tests cover combined filter scenarios
- [ ] Integration tests cover error cases (invalid filters, malformed queries)
- [ ] Integration tests verify cache header presence on search responses
- [ ] All tests follow the existing pattern (real PostgreSQL, status code assertions)
- [ ] All tests pass consistently

## Test Requirements
- [ ] Test ranked search: search returns results ordered by descending relevance score
- [ ] Test entity_type filter: entity_type=sbom returns only SBOMs
- [ ] Test entity_type filter: entity_type=advisory returns only advisories
- [ ] Test entity_type filter: entity_type=package returns only packages
- [ ] Test severity filter: severity=critical returns only critical advisories
- [ ] Test date range filter: date_from and date_to correctly bound results
- [ ] Test combined filters: entity_type=advisory&severity=high returns only high-severity advisories
- [ ] Test invalid entity_type returns 400 Bad Request
- [ ] Test date_from > date_to returns 400 Bad Request
- [ ] Test empty query returns appropriate response
- [ ] Test Cache-Control header is present on successful search responses

## Verification Commands
- `cargo test -p tests -- search` — all search integration tests pass
- `cargo test -p tests -- search --nocapture` — view test output for debugging

## Dependencies
- Depends on: Task 4 — Add caching to the search endpoint
