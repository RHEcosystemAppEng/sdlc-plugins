## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search relevance ranking, filter combinations, performance characteristics, and backward compatibility. This task ensures the search improvements from Tasks 1-3 are thoroughly tested end-to-end.

**Ambiguity flag:** The feature's non-functional requirement "should be fast enough" lacks a quantifiable threshold. This task assumes (Assumption A1) that p95 search latency under 500ms for datasets up to 50k records is the target. The test will validate query execution time but the actual threshold must be confirmed with the product owner. The test uses a placeholder assertion that can be adjusted once a concrete SLA is defined.

## Files to Modify
- `tests/api/search.rs` — add integration tests for full-text search, filters, and performance

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`
- Use the established test database setup pattern (real PostgreSQL test database)
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests
- Test data setup: create test SBOMs, advisories, and packages with known searchable text to verify relevance ranking
- Performance test: measure query execution time for search operations and assert it falls within the assumed threshold (Assumption A1: p95 < 500ms). Include a comment noting the threshold is an assumption pending confirmation.
- Per docs/constraints.md §5.2: inspect existing test files before modifying to follow established patterns
- Per docs/constraints.md §5.11: add a doc comment to every test function

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test patterns, test database setup, and assertion style
- `tests/api/advisory.rs` — reference for advisory-specific test data setup
- `tests/api/search.rs` — existing search tests to extend (do not duplicate existing coverage)

## Acceptance Criteria
- [ ] Integration tests cover full-text search with relevance ranking verification
- [ ] Integration tests cover each filter type individually and in combination
- [ ] Integration tests verify backward compatibility (no filters = existing behavior)
- [ ] Integration tests verify error responses for invalid filter values
- [ ] A performance-oriented test validates search query execution time is within acceptable bounds
- [ ] All new test functions have doc comments

## Test Requirements
- [ ] Test: full-text search ranks name matches above description-only matches
- [ ] Test: entity_type filter returns only the specified entity type
- [ ] Test: severity filter returns only matching advisories
- [ ] Test: date range filter returns entities within the specified window
- [ ] Test: combined filters apply intersection semantics
- [ ] Test: empty search query returns results in default order
- [ ] Test: search performance stays within threshold for representative dataset

## Verification Commands
- `cargo test --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 3 — Add search filter parameters to search endpoint

---

[sdlc-workflow] Description digest: sha256-md:a137b83634ac4f052560b075cf287c3d9a88cbf58c2245074e58263b837f4bcc
