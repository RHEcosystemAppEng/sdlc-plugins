## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the search improvements introduced by TC-9002. This task covers test scenarios for the new filter parameters (entity type, severity, date range), relevance ordering, and search performance characteristics.

The existing test file `tests/api/search.rs` contains search endpoint integration tests. This task extends that file with new test functions covering the filter and relevance features added in Tasks 1-3.

## Files to Modify
- `tests/api/search.rs` — add integration test functions for filtered search, relevance ordering, filter combinations, error cases, and backward compatibility

## Implementation Notes
- Inspect the existing tests in `tests/api/search.rs` to understand the established test setup pattern (database fixtures, HTTP client construction, assertion style) before adding new tests.
- Per Key Conventions (Testing): integration tests hit a real PostgreSQL test database. Use the same test database setup and teardown pattern as existing tests in `tests/api/search.rs`.
  Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Testing): use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for asserting successful responses, and check for `StatusCode::BAD_REQUEST` on validation error tests.
  Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` file scope.
- Each test function must have a doc comment explaining what it verifies.
- Use given-when-then inline comments for non-trivial tests that have distinct setup, action, and assertion phases.
- Reference `tests/api/sbom.rs` and `tests/api/advisory.rs` for the established integration test patterns (fixture setup, HTTP client usage, response parsing).
- Test data fixtures should include: at least 2 SBOMs, 2 advisories (with different severities), and 2 packages with different creation dates to enable meaningful filter and ordering assertions.
- Consider whether parameterized tests are appropriate for filter combinations — check sibling test files for existing parameterized test patterns first.

## Reuse Candidates
- `tests/api/search.rs` — existing search integration tests; follow the established fixture setup and assertion patterns
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test database setup and HTTP client patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests; reference for test patterns involving severity values

## Acceptance Criteria
- [ ] Test for `entity_type=sbom` filter returns only SBOM results
- [ ] Test for `entity_type=advisory` filter returns only advisory results
- [ ] Test for `entity_type=package` filter returns only package results
- [ ] Test for `severity` filter returns only advisories with matching severity
- [ ] Test for `date_from`/`date_to` filter returns only results within the date range
- [ ] Test for combined filters (e.g., `entity_type=advisory&severity=high`) returns correct results
- [ ] Test for unfiltered search confirms backward compatibility (same behavior as before the feature)
- [ ] Test for invalid filter values confirms 400 Bad Request response
- [ ] Test for relevance ordering confirms that title matches rank higher than description matches
- [ ] All tests pass in CI against the PostgreSQL test database

## Test Requirements
- [ ] `test_search_filter_entity_type_sbom` — search with `entity_type=sbom` returns only SBOMs
- [ ] `test_search_filter_entity_type_advisory` — search with `entity_type=advisory` returns only advisories
- [ ] `test_search_filter_entity_type_package` — search with `entity_type=package` returns only packages
- [ ] `test_search_filter_severity` — search with `severity=critical` returns only critical advisories
- [ ] `test_search_filter_date_range` — search with date range returns only results within range
- [ ] `test_search_filter_combination` — search with multiple filters returns correctly narrowed results
- [ ] `test_search_no_filters_backward_compatible` — search without filters matches pre-feature behavior
- [ ] `test_search_invalid_entity_type` — invalid entity type returns 400 Bad Request
- [ ] `test_search_invalid_date_format` — invalid date format returns 400 Bad Request
- [ ] `test_search_relevance_ordering` — results are ordered by relevance (title match > description match)

## Verification Commands
- `cargo test --test search` — all search integration tests pass
- `cargo test --test search -- --nocapture` — run with output to verify test execution details

## Dependencies
- Depends on: Task 3 — Add filter parameters to the search API endpoint (tests exercise the filter functionality)
- Depends on: Task 2 — Optimize SearchService full-text search execution (tests verify relevance ordering)
- Depends on: Task 1 — Add search performance indexes via database migration (tests require indexes to be present)
