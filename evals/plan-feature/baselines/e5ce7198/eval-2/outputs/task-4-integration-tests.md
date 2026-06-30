# Task 4: Add Integration Tests for Search Improvements

**Parent Feature**: TC-9002 — Improve search experience

## Repository
trustify-backend

## Target Branch
main

## Description
Write comprehensive integration tests for the improved search functionality, covering full-text search queries, relevance ranking, filter combinations, edge cases, and performance characteristics. These tests validate that the search improvements from Tasks 1-3 work correctly end-to-end against a real PostgreSQL test database.

## Files to Modify
- `tests/api/search.rs` — Extend existing search integration tests with new test cases covering full-text search, relevance ranking, filters, and edge cases

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` which hit a real PostgreSQL test database
- Use the established assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status code checks
- Test data setup: insert SBOMs, advisories, and packages with known content to validate search behavior deterministically
- For relevance tests: insert documents with varying relevance to a search term and verify ordering
- For filter tests: insert documents spanning multiple entity types, severities, and date ranges, then verify filter combinations
- For performance tests: use a reasonable dataset size and assert query completes within an acceptable time window (e.g., under 500ms)

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/search.rs` matching the convention's `tests/api/` scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration test patterns for test setup and assertions
- `tests/api/advisory.rs` — Existing advisory integration test patterns for reference

## Acceptance Criteria
- [ ] All new integration tests pass against a PostgreSQL test database
- [ ] Tests cover full-text search query functionality (term matching, phrase matching)
- [ ] Tests cover relevance ranking (results ordered by ts_rank score)
- [ ] Tests cover all filter parameters individually and in combination
- [ ] Tests cover edge cases (empty query, special characters, very long queries)
- [ ] Tests cover backward compatibility (existing search behavior is not broken)

## Test Requirements
- [ ] Test: full-text search for exact term returns matching documents
- [ ] Test: full-text search for partial term (stemming) returns relevant documents
- [ ] Test: search results are ordered by relevance (title match ranks above description match)
- [ ] Test: entity_type filter returns only the specified entity type
- [ ] Test: severity filter returns only advisories with matching severity
- [ ] Test: date_from and date_to filters restrict results to the specified date range
- [ ] Test: license filter returns only packages with matching license
- [ ] Test: combining multiple filters narrows results correctly (AND logic)
- [ ] Test: empty query string returns 400 Bad Request or empty result
- [ ] Test: special characters in search query do not cause server errors
- [ ] Test: search with no filters returns results from all entity types
- [ ] Test: pagination works correctly with filtered and ranked results

## Dependencies
- Depends on: Task 3 — Add Search Filter Parameters to Search Endpoint (all search features must be implemented)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}]}

[sdlc-workflow] Description digest: sha256-md:46df2c16039fd6f850dc94815437827954a3d3a2c0f4d565be5b704ac4069da8
