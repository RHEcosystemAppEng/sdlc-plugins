## Repository
trustify-backend

## Target Branch
main

## Description
Extend the search integration tests to cover the new relevance scoring, filtering, and caching behavior introduced by Tasks 1-4. This ensures the "don't break existing functionality" NFR from TC-9002 is addressed and provides regression coverage for the enhanced search experience.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for relevance-ranked results, filter parameters (entity_type, severity, date range), filter combinations, backward compatibility (no filters = same behavior), and cache behavior

## Implementation Notes
Inspect the existing tests in `tests/api/search.rs` to understand the current test setup (database seeding, HTTP client configuration, assertion patterns). Follow the same patterns for new tests.

Per the repo conventions, integration tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern. New tests should:

1. Seed the test database with known SBOM, advisory, and package records that have distinct text content and severity levels
2. Execute search queries via the HTTP API and verify:
   - Results are ordered by relevance (a more specific match ranks higher)
   - Filter parameters narrow results correctly
   - Combined filters use AND semantics
   - Omitting filters returns all matching results (backward compatibility)
3. Verify error responses for invalid filter values

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Response types: verify that search responses deserialize correctly into `PaginatedResults<T>`. Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM endpoint test patterns, database seeding, and assertion style
- `tests/api/advisory.rs` — reference for advisory endpoint test patterns
- `common/src/model/paginated.rs::PaginatedResults<T>` — response type to deserialize and assert against in tests

## Acceptance Criteria
- [ ] Integration tests exist for relevance-ranked search results
- [ ] Integration tests exist for each filter parameter individually (entity_type, severity, created_after, created_before)
- [ ] Integration tests exist for combined filters
- [ ] A backward-compatibility test verifies that search with no filters works as before
- [ ] Tests follow the existing test patterns in `tests/api/`
- [ ] All new tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Test: search returns results ordered by relevance (exact match ranked above partial match)
- [ ] Test: `entity_type=sbom` filter returns only SBOM results
- [ ] Test: `entity_type=advisory` filter returns only advisory results
- [ ] Test: `severity=critical` filter returns only critical-severity advisories
- [ ] Test: `created_after` filter excludes older results
- [ ] Test: `created_before` filter excludes newer results
- [ ] Test: combined `entity_type` + `severity` filters return correct subset
- [ ] Test: no filter parameters returns all results (backward compatibility)
- [ ] Test: invalid filter value returns error status code

## Dependencies
- Depends on: Task 1 — Search indexes
- Depends on: Task 2 — Relevance scoring
- Depends on: Task 3 — Search filters
- Depends on: Task 4 — Search caching
