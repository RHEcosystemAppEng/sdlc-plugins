## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based search ranking in the SearchService by integrating PostgreSQL `ts_rank` scoring with the tsvector columns added in Task 1. Search results will be ordered by relevance score by default, replacing the current unranked or insertion-order result listing. Update entity definitions to include the tsvector field mapping so SeaORM can interact with the new columns.

This addresses the "Results should be more relevant" requirement from TC-9002.

**Assumption pending clarification:** Relevance ranking should use PostgreSQL `ts_rank` with default weights. Text match quality is the primary ranking signal. No additional signals (recency, popularity, user context) are required for MVP.

## Files to Modify
- `modules/search/src/service/mod.rs` — Implement `ts_rank`-based scoring in SearchService query; convert search terms to `tsquery`; order results by rank score descending
- `entity/src/sbom.rs` — Add `search_vector` tsvector field mapping to the SBOM SeaORM entity
- `entity/src/advisory.rs` — Add `search_vector` tsvector field mapping to the Advisory SeaORM entity
- `entity/src/package.rs` — Add `search_vector` tsvector field mapping to the Package SeaORM entity
- `tests/api/search.rs` — Add integration tests verifying relevance-ordered results

## API Changes
- `GET /api/v2/search` — MODIFY: Results are now ordered by relevance score (ts_rank) by default when a search query is provided. Response shape unchanged.

## Implementation Notes
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service .rs file scope.
- Per CONVENTIONS.md §Testing: use integration tests hitting a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's test .rs file scope.
- Convert user search input to a `tsquery` using `plainto_tsquery()` or `websearch_to_tsquery()` for natural language queries
- Use `ts_rank(search_vector, query)` to compute a relevance score for each matching row
- Order results by `ts_rank` descending when a search query is present; fall back to default ordering when no query is provided
- Use the weighted tsvector columns from Task 1 so that matches in title/name fields rank higher than matches in description fields
- Ensure the `search_vector` field is excluded from API response serialization (it is an internal implementation detail, not a user-facing field)
- Maintain backward compatibility: existing search behavior without a query term should remain unchanged

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; extend with relevance sorting support
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used for search result responses
- `common/src/error.rs` — `AppError` enum for error handling in service methods
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` as a reference implementation showing the service query pattern with SeaORM

## Acceptance Criteria
- [ ] Search results are ordered by relevance score when a query term is provided
- [ ] Matches in title/name fields rank higher than matches in description fields
- [ ] Search without a query term returns results in the existing default order
- [ ] Entity definitions include the search_vector field mapping (not serialized in API responses)
- [ ] Integration tests verify relevance ordering for known test data

## Test Requirements
- [ ] Insert test entities with known text content; verify that a search for a term present in a title ranks that result above one where the term appears only in the description
- [ ] Verify that search results include a relevance score or are demonstrably ordered by relevance
- [ ] Verify that searching with an empty/missing query returns results in the previous default order (backward compatibility)
- [ ] Verify that the search_vector field is not exposed in the API response body

## Verification Commands
- `cargo test -p search` — search module unit tests pass
- `cargo test --test search` — search integration tests pass (tests/api/search.rs)

## Dependencies
- Depends on: Task 1 — Add database indexes and tsvector support for search performance
