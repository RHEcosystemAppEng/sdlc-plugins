## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search ranking, filter combinations, and edge cases. These tests validate the changes introduced by Tasks 1–3 and establish a regression baseline for future search improvements.

## Files to Modify
- `tests/api/search.rs` — add integration tests for full-text search relevance ranking, filter parameters, and combined filter+search scenarios

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status validation.
- Test data setup should create entities with known searchable text values to validate ranking order deterministically.
- For filter tests, create entities spanning multiple types and severities to verify filter isolation.
- For relevance tests, create entities where one is a strong match (name contains search term) and another is a weak match (description references the term) to verify ranking order.
- Per docs/constraints.md §5 (Code Change Rules): keep test changes scoped to the search test module.

## Acceptance Criteria
- [ ] All new integration tests pass against a real PostgreSQL database
- [ ] Relevance ranking tests verify that exact name matches rank above description-only matches
- [ ] Filter tests verify each filter parameter in isolation and in combination
- [ ] Edge case tests cover empty queries, special characters in search terms, and no-result scenarios
- [ ] Existing search tests continue to pass (regression check)

## Test Requirements
- [ ] Relevance ranking: search for a term that appears in one entity's name and another's description; verify the name-match entity ranks first
- [ ] Type filter: create SBOMs and advisories, filter by `type=sbom`, verify only SBOMs returned
- [ ] Severity filter: create advisories with different severities, filter by `severity=critical`, verify only critical advisories returned
- [ ] Date range filter: create entities with different ingestion dates, filter by date range, verify only entities within range returned
- [ ] Combined filters: apply type + search term, verify both constraints are enforced
- [ ] Empty query with filters: verify filters work without a search term
- [ ] Special characters: search for terms with quotes, ampersands, and SQL-sensitive characters without errors
- [ ] No results: search for a nonexistent term, verify empty result set with 200 status

## Dependencies
- Depends on: Task 2 — Improve search relevance scoring
- Depends on: Task 3 — Add search filter parameters
