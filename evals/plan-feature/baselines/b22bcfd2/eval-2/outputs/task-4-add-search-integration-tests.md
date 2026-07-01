## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the new search functionality: full-text search performance, relevance scoring, and filter parameters. These tests validate that the ambiguous requirements have been correctly interpreted and implemented per the documented assumptions. Tests serve as executable documentation of the assumed acceptance criteria until stakeholder clarification is received.

## Files to Modify
- `tests/api/search.rs` — Add integration tests covering full-text search with GIN index, relevance scoring with ts_rank ordering, filter parameter handling (entity_type, date range, severity), filter combinations, backward compatibility of the existing search API, and edge cases (empty results, invalid filters)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for response status assertions, consistent with existing tests.
- Test data setup should create a mix of SBOMs, advisories, and packages with varying text content, dates, and severity levels to exercise all filter combinations.
- Test relevance scoring by searching for a term that appears with different frequencies across entities and verifying the order matches ts_rank expectations.
- Include a backward compatibility test that calls `GET /api/v2/search` with only the existing query parameter (no new filter params) and verifies the response matches the `PaginatedResults<T>` format.
- Per CONVENTIONS.md: integration tests use a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration test patterns for test setup and assertion style
- `tests/api/advisory.rs` — Existing advisory integration test patterns
- `common/src/model/paginated.rs::PaginatedResults` — Response type to assert against in test assertions

## Acceptance Criteria
- [ ] All new integration tests pass against a PostgreSQL test database
- [ ] Tests cover: full-text search, relevance ordering, each filter type individually, filter combinations, backward compatibility, and error cases
- [ ] Test failures would catch regressions in search performance, relevance ordering, or filter behavior
- [ ] **Assumption pending clarification**: test performance thresholds (e.g., 500ms query time) are based on assumed targets and may need adjustment

## Test Requirements
- [ ] Full-text search returns results matching the query term
- [ ] Relevance scoring test: search for a term, verify results are ordered by descending relevance score
- [ ] Entity type filter test: `entity_type=sbom` returns only SBOMs
- [ ] Date range filter test: `created_after` and `created_before` correctly bound results
- [ ] Severity filter test: `severity=critical` returns only critical advisories
- [ ] Combined filter test: multiple filters applied simultaneously
- [ ] Backward compatibility test: existing API call without new params returns valid results
- [ ] Error handling test: invalid entity_type value returns 400

## Dependencies
- Depends on: Task 2 — Implement search result relevance scoring
- Depends on: Task 3 — Add search filter parameters

## Additional Fields
- priority: Normal
- fixVersions: RHTPA 1.6.0

## Description Digest
[sdlc-workflow] Description digest: sha256-md:<computed-at-creation-time>
(Actual digest computed by re-fetching description from Jira API and running `scripts/sha256-digest.py`)
