# Task 4 — Add comprehensive search integration tests

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search relevance ranking, filter combinations, edge cases, and backward compatibility. These tests validate the end-to-end search experience across all three tasks (migration, service optimization, and filters) and ensure the "don't break existing functionality" non-functional requirement is met.

**Ambiguity note (assumption pending clarification):** The non-functional requirement "Don't break existing functionality" is vague. These tests assume backward compatibility means: (1) existing API request parameters continue to work, (2) response shape (`PaginatedResults<T>`) is unchanged, and (3) previously findable results remain findable. Stakeholders should confirm whether additional backward compatibility guarantees are expected.

## Files to Modify
- `tests/api/search.rs` — add new integration test functions for full-text search, relevance ranking, filters, edge cases, and backward compatibility

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs` and sibling files (`tests/api/sbom.rs`, `tests/api/advisory.rs`). Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the codebase.
- Tests should hit a real PostgreSQL test database per the project's testing convention.
- Test data setup: insert test records into sbom, advisory, and package tables with known searchable content to enable deterministic assertions on search results and ranking.
- Relevance ranking tests: insert documents with varying term frequency and verify that `ts_rank` ordering returns the most relevant documents first.
- Filter tests: verify each filter in isolation and in combination. Ensure filters compose correctly with AND logic.
- Edge case tests: empty query string, very long query string, special characters in query (e.g., SQL injection attempts), query with no matching results.
- Backward compatibility tests: verify that API calls without the new filter parameters return the same structure and contain the same results as before the changes.
- Per `docs/constraints.md` §5.11: add a doc comment to every test function created.
- Per `docs/constraints.md` §5.12: add given-when-then inline comments to non-trivial test functions.
- Per `docs/constraints.md` §5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., different filter combinations).
- Per `docs/constraints.md` §2 (Commit Rules): commit must reference TC-9002 in the footer.

### Convention applicability
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating test setup, HTTP request construction, and response assertion patterns
- `tests/api/advisory.rs` — existing advisory integration tests; reference for test data setup involving advisory entities with severity fields
- `tests/api/search.rs` — existing search tests to extend; understand current test coverage to avoid duplication
- `common/src/model/paginated.rs` — `PaginatedResults<T>` struct for deserializing and asserting on search response shape

## Acceptance Criteria
- [ ] At least one test verifies full-text search returns results matching the query term
- [ ] At least one test verifies results are ordered by relevance (ts_rank)
- [ ] At least one test per filter type (entity_type, severity, date_from, date_to) verifies correct filtering
- [ ] At least one test verifies combined filters work with AND logic
- [ ] At least one test verifies backward compatibility (no filters = same behavior as before)
- [ ] At least one test verifies edge cases (empty query, no results, invalid filter)
- [ ] All test functions have doc comments
- [ ] Non-trivial tests have given-when-then inline comments

## Test Requirements
- [ ] Integration test: full-text search for a known term returns the expected matching records
- [ ] Integration test: search results for a term appearing in multiple documents are ranked by relevance (most matches first)
- [ ] Integration test: `entity_type` filter returns only the specified entity type
- [ ] Integration test: `severity` filter returns only advisories with the specified severity
- [ ] Integration test: `date_from`/`date_to` filter returns only records within the range
- [ ] Integration test: combined `entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] Integration test: search with empty query string returns appropriate response (empty results or paginated all)
- [ ] Integration test: search with special characters does not cause errors (SQL injection safety)
- [ ] Integration test: calling search endpoint without any new parameters returns `PaginatedResults` with expected shape

## Verification Commands
- `cargo test --test search` — all search integration tests pass
- `cargo test --test search -- --nocapture` — run with output for debugging

## Dependencies
- Depends on: Task 3 — Add filter parameters to the search endpoint

[sdlc-workflow] Description digest: sha256-md:9e6140ae4f6e2f314f0ed968a047ef37b957dce15711b8d8731517afc5d06ef9
