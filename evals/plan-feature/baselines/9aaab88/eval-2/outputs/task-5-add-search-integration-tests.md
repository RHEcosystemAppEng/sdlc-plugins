## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality including filter parameters, relevance ranking, and caching behavior. The existing `tests/api/search.rs` contains search endpoint tests that must be extended to cover the new filter and ranking features.

**Assumption pending clarification**: The feature description says "don't break existing functionality" but does not specify a regression test baseline. This task extends the existing test file to cover new functionality while preserving existing test cases as regression tests.

## Files to Modify
- `tests/api/search.rs` -- Add integration tests for: filter query parameters (entity_type, date_from, date_to, severity), relevance ranking order, backward compatibility with no filters, error handling for invalid filter values, cache header presence

## Implementation Notes
Follow the existing test patterns in `tests/api/search.rs` and the other integration test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`). Tests use a real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` file scope.

Reference `tests/api/sbom.rs` for the test setup pattern (creating test data, making HTTP requests, asserting responses). Each test should set up search-relevant test data (SBOMs, advisories, packages) before exercising the search endpoint.

## Reuse Candidates
- `tests/api/sbom.rs` -- integration test patterns for endpoint testing with test data setup
- `tests/api/advisory.rs` -- integration test patterns, especially for severity-related test data

## Dependencies
- Depends on: Task 3 -- Add filter parameters to search endpoint (tests require the filter endpoint to be implemented)

## Acceptance Criteria
- [ ] Tests cover all filter parameter combinations (entity_type, date_from, date_to, severity)
- [ ] Tests verify relevance ranking order (more relevant results first)
- [ ] Tests verify backward compatibility (no filters returns all results)
- [ ] Tests verify error handling for invalid filter values (400 responses)
- [ ] Tests verify cache-control headers are present in responses
- [ ] All existing search tests continue to pass (regression)
- [ ] **Assumption pending clarification**: Test data setup covers representative scenarios (exact test data depends on the entity types and filter values finalized in earlier tasks)

## Test Requirements
- [ ] Integration test: GET /api/v2/search returns 200 with default pagination
- [ ] Integration test: GET /api/v2/search?entity_type=sbom filters to SBOMs only
- [ ] Integration test: GET /api/v2/search?entity_type=advisory filters to advisories only
- [ ] Integration test: GET /api/v2/search?severity=critical filters by severity
- [ ] Integration test: GET /api/v2/search?date_from=...&date_to=... filters by date range
- [ ] Integration test: GET /api/v2/search?entity_type=invalid returns 400
- [ ] Integration test: search results are ordered by relevance_score descending
- [ ] Integration test: response includes Cache-Control header

[sdlc-workflow] Description digest: sha256-md:9c7a793c90afb96e63cbbe802b2d91cc69e7029e5ab6bf7e4ea0d1005dbdcea6
