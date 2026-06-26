# Task 4: Add integration tests for search improvements

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests covering the search performance, relevance ranking, and filtering improvements introduced in Tasks 1-3. The TC-9002 feature description requires "don't break existing functionality" as a non-functional requirement.

**Ambiguity noted:** "Don't break existing functionality" does not specify a regression test baseline or which behaviors are critical. Assumption pending clarification: all existing tests in `tests/api/search.rs` constitute the regression baseline, and new tests must cover all added functionality (ranking, filters, edge cases).

## Files to Modify
- `tests/api/search.rs` -- Add new integration test functions covering relevance ranking, filter parameters, combined search+filter queries, edge cases, and error cases. Follow the existing test pattern using `assert_eq!(resp.status(), StatusCode::OK)` for success cases.

## Implementation Notes
Follow the existing integration test patterns in `tests/api/search.rs` and the other test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`). Tests hit a real PostgreSQL test database, so:

1. Set up test data with known properties (e.g., advisories with different severities, SBOMs with different creation dates, entities with search terms in titles vs. descriptions).
2. Execute search requests via the HTTP API.
3. Assert on response status, result ordering, filter correctness, and relevance scores.

Test categories to cover:
- **Relevance ranking:** Insert entities where a search term appears in the title of one and the description of another. Verify the title match ranks higher.
- **Entity type filter:** Search with `entity_type=advisory` and verify no SBOMs or packages in results.
- **Severity filter:** Search with `severity=critical` and verify only critical advisories returned.
- **Date range filter:** Search with `created_after` and verify only recent results returned.
- **Combined filters:** Search with query + entity_type + severity and verify intersection.
- **Error cases:** Invalid entity_type value returns 400. Severity filter with entity_type=sbom returns 400. Invalid date format returns 400. created_after > created_before returns 400.
- **Backward compatibility:** Existing search queries without filters return results in the new ranked order (not a breaking change, but a behavior change to verify).

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- Existing SBOM integration tests. Follow the same test setup and assertion patterns.
- `tests/api/advisory.rs` -- Existing advisory integration tests. Follow the same data setup patterns for advisories with known severity values.

## Acceptance Criteria
- [ ] All existing search tests continue to pass unchanged
- [ ] New tests cover relevance ranking (title vs. description match ordering)
- [ ] New tests cover each filter parameter individually
- [ ] New tests cover combined filter scenarios
- [ ] New tests cover error cases (invalid filters, invalid dates)
- [ ] Test data setup is self-contained (each test creates its own test data)
- [ ] All new tests pass in CI against a PostgreSQL test database

## Test Requirements
- [ ] Test: search term in title ranks higher than same term in description only
- [ ] Test: entity_type filter restricts result types correctly
- [ ] Test: severity filter returns only matching advisories
- [ ] Test: date range filter returns only results within range
- [ ] Test: combined query + filters return correct intersection
- [ ] Test: invalid entity_type returns 400
- [ ] Test: severity filter with non-advisory entity_type returns 400
- [ ] Test: malformed date parameter returns 400
- [ ] Test: created_after > created_before returns 400
- [ ] Test: empty query with filters returns filtered results

## Dependencies
- Depends on: Task 2 -- Implement search relevance ranking (tests validate ranking behavior)
- Depends on: Task 3 -- Add search filter query parameters (tests validate filter behavior)

[sdlc-workflow] Description digest: sha256-md:699dc5bdecaf57ef07a25bf6a09ecc57cbc0c4b93134837cffa1a05ecb067bc8
