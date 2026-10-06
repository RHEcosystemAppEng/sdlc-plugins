# Task 5 — Add integration tests for search improvements

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests covering the new search capabilities introduced by TC-9002: filtering, relevance ranking, and performance improvements. The existing test file `tests/api/search.rs` contains basic search tests, but does not cover the new filter parameters, relevance ordering, or the interaction between filters and ranking. This task adds tests to validate all new search behaviors and ensure backward compatibility with existing behavior.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for search filtering (entity_type, date range, severity), relevance ranking (sort parameter), combined filter+ranking scenarios, and backward compatibility (no-filter queries return same results as before)

## Implementation Notes
- Follow the existing test pattern in `tests/api/search.rs`: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status checks
- Each test should set up its own test data (SBOMs, advisories, packages with known attributes) to make assertions predictable
- Test the interaction between filters and ranking (e.g., filtering by entity_type=advisory and sorting by relevance)
- Include negative tests: invalid filter values should return 400, empty result sets should return 200 with empty items array
- Test edge cases: date range with no results, severity filter on non-advisory entity types, empty search query with filters
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/search.rs` — Existing search integration tests; follow the same setup/teardown pattern and assertion style
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test data setup patterns (creating SBOMs in the test database)
- `tests/api/advisory.rs` — Advisory endpoint integration tests; reference for creating advisories with specific severity values in test data

## Acceptance Criteria
- [ ] Integration tests exist for entity_type filter (sbom, advisory, package)
- [ ] Integration tests exist for date range filters (created_after, created_before)
- [ ] Integration tests exist for severity filter on advisory results
- [ ] Integration tests exist for combined filters (e.g., entity_type + severity)
- [ ] Integration tests exist for relevance ranking (sort=relevance vs sort=date)
- [ ] Integration tests exist for backward compatibility (no-filter queries)
- [ ] Integration tests exist for error cases (invalid filter values return 400)
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test: GET /api/v2/search?q=test&entity_type=sbom returns only SBOM results
- [ ] Test: GET /api/v2/search?q=test&entity_type=advisory returns only advisory results
- [ ] Test: GET /api/v2/search?q=test&entity_type=package returns only package results
- [ ] Test: GET /api/v2/search?q=test&created_after=<timestamp> returns only recent results
- [ ] Test: GET /api/v2/search?q=test&severity=critical returns only critical advisories
- [ ] Test: GET /api/v2/search?q=test&entity_type=advisory&severity=high returns filtered results
- [ ] Test: GET /api/v2/search?q=specific_term&sort=relevance returns most relevant result first
- [ ] Test: GET /api/v2/search?q=test&sort=date returns results in chronological order
- [ ] Test: GET /api/v2/search?q=test returns same results as before (no regression)
- [ ] Test: GET /api/v2/search?q=test&entity_type=invalid returns 400 Bad Request

## Verification Commands
- `cargo test --test search` — All search integration tests pass
- `cargo test --test search -- --nocapture` — Run with output to verify test coverage

## Dependencies
- Depends on: Task 1 — Add database indexes for search-relevant columns
- Depends on: Task 2 — Optimize SearchService query execution
- Depends on: Task 3 — Add filter parameters to search endpoint
- Depends on: Task 4 — Implement search result relevance ranking
