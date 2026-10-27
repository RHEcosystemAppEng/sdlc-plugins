## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search relevance, filter parameters, and performance characteristics. This task consolidates test coverage for all search improvements introduced in Tasks 1–3.

**Assumption (pending clarification):** Performance target is p95 < 500ms for search queries. This is used in test assertions but should be validated with stakeholders.

## Files to Modify
- `tests/api/search.rs` — add integration tests for full-text search, filters, relevance ordering, and performance

## Implementation Notes
- Follow the existing test patterns in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` — use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for response assertions.
- Tests hit a real PostgreSQL test database as per the project's integration testing convention.
- Test data setup should create SBOMs, advisories, and packages with known searchable content so that relevance ordering can be verified deterministically.
- Test filter combinations: single filter, multiple filters, no filters, invalid filters.
- Include a basic performance assertion to validate that full-text search queries respond within acceptable bounds under test data load.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint tests demonstrating the integration test pattern, test data setup, and assertion style
- `tests/api/advisory.rs` — existing advisory endpoint tests with similar patterns

## Acceptance Criteria
- [ ] Full-text search tests verify that results match query terms in title/name fields
- [ ] Full-text search tests verify that results match query terms in description fields
- [ ] Relevance ordering tests verify that exact title matches rank higher than description matches
- [ ] Filter tests verify entity_type, severity, and date range filtering
- [ ] Filter combination tests verify that multiple filters produce the intersection of results
- [ ] Backward compatibility test verifies that search without parameters still works
- [ ] Error handling test verifies invalid filter values return 400 status

## Test Requirements
- [ ] At least 8 integration test cases covering: basic search, relevance ordering, entity type filter, severity filter, date range filter, combined filters, empty query, invalid filter
- [ ] All tests use the real PostgreSQL test database (no mocks)
- [ ] Test data is deterministic — each test sets up its own data to avoid cross-test interference

## Dependencies
- Depends on: Task 3 — Add search filter parameters (requires all search changes to be in place)
