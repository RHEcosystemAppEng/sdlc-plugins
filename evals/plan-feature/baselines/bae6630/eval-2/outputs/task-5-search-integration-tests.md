## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering query optimization, relevance ranking, and filtering. These tests validate the combined behavior of Tasks 1-4 and ensure backward compatibility with existing search behavior.

## Files to Modify
- `tests/api/search.rs` — Add new integration test cases for full-text search, relevance ranking, and filter combinations. Follow the existing test pattern in this file, which uses `assert_eq!(resp.status(), StatusCode::OK)` and hits a real PostgreSQL test database.

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` — these tests hit a real PostgreSQL test database
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern per project testing conventions
- Test data setup: insert SBOMs, advisories, and packages with known names, descriptions, and severities so that assertions can verify ordering and filtering deterministically
- **Test scenarios to cover:**
  1. Full-text search returns results matching the query term
  2. Relevance ordering: entity with term in name ranks above entity with term only in description
  3. Filter by entity_type returns only matching entity types
  4. Filter by severity returns only advisories with matching severity
  5. Filter by date range returns only entities within the range
  6. Combined filters (entity_type + severity) return correct intersection
  7. Empty search query with filters returns filtered results in default sort order
  8. Search with no matching results returns empty `PaginatedResults` (status 200, empty items)
  9. Invalid filter values return 400 status
  10. Backward compatibility: existing search behavior (no filters, no ranking) still works
- **Assumption (pending clarification):** Since the feature provides no performance targets (Ambiguity 1), these tests validate functional correctness only, not latency. Performance benchmarks would require agreed-upon targets.

## Acceptance Criteria
- [ ] At least 8 new integration test cases added to `tests/api/search.rs`
- [ ] Tests cover full-text search, relevance ranking, filtering, and backward compatibility
- [ ] All new tests pass against a PostgreSQL test database
- [ ] All pre-existing tests continue to pass (no regressions)
- [ ] Test names follow existing naming conventions in the test file

## Test Requirements
- [ ] Full-text search test: verify results contain expected entities for a given query
- [ ] Relevance ranking test: verify ordering of results by match quality
- [ ] Entity type filter test: verify only specified entity types are returned
- [ ] Severity filter test: verify advisory severity filtering
- [ ] Date range filter test: verify temporal filtering
- [ ] Combined filter test: verify AND-combination of multiple filters
- [ ] Empty result test: verify correct response format when no results match
- [ ] Invalid filter test: verify 400 response for bad filter values
- [ ] Backward compatibility test: verify existing query patterns still work

## Dependencies
- Depends on: Task 3 — Search relevance ranking (ranking must be implemented to test ordering)
- Depends on: Task 4 — Add search filters (filters must be implemented to test filtering)

## Digest
[sdlc-workflow] Description digest: sha256-md:532ce6944a3ba2891cbc9dc54ea50f256788f89692c97c1d529dfa280a45f4a7
