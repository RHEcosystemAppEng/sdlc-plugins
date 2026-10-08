# Task 2: Add relevance ranking to search results

## Repository
trustify-backend

## Target Branch
main

## Description
Add relevance-based ranking to the SearchService so that search results are ordered by match quality rather than an arbitrary or insertion-time ordering. The feature requirement states "results should be more relevant" (TC-9002) but does not define what "relevant" means.

**Assumption pending clarification:** "Relevant" is interpreted as ordering results by text match quality using PostgreSQL full-text search ranking functions (e.g., `ts_rank` or `ts_rank_cd`). This ranks results by how well they match the search query terms. No field weighting preferences have been specified -- the default PostgreSQL ranking normalization will be used. If the product owner has specific ranking requirements (e.g., title matches weighted higher than description matches, recency boost), those should be communicated before implementation.

**Assumption pending clarification:** The ranking applies uniformly across all entity types returned by the search endpoint (SBOMs, advisories, packages). No entity-type-specific ranking rules have been defined.

## Files to Modify
- `modules/search/src/service/mod.rs` -- add relevance scoring logic to the SearchService query, using PostgreSQL ts_rank or equivalent to compute a relevance score per result, and order results by score descending
- `modules/search/src/endpoints/mod.rs` -- expose the relevance score in the search response (optional field) and ensure the endpoint propagates the ranking order from the service layer
- `tests/api/search.rs` -- add integration tests verifying that results are returned in relevance-ranked order

## Implementation Notes
- Per CONVENTIONS.md [Error handling]: all modified handlers and service methods must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` handler file scope.
- Per CONVENTIONS.md [Response types]: the search endpoint returns `PaginatedResults<T>` from `common/src/model/paginated.rs`. Ensure the relevance-ranked results are wrapped in this type.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md [Testing]: integration tests must hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` assertions.
  Applies: task modifies `tests/api/search.rs` matching the convention's `tests/api/` test file scope.
- Use PostgreSQL `ts_rank(tsvector, tsquery)` to compute relevance scores. This requires the full-text search indexes from Task 1 to be present for optimal performance, but works functionally without them.
- Add an `ORDER BY rank DESC` clause to the search query.
- Consider adding an optional `score` field to the search result response so consumers can display relevance indicators.
- Reference `modules/fundamental/src/sbom/service/sbom.rs` for the established service method pattern (fetch, list operations with query building).

## Reuse Candidates
- `common/src/db/query.rs` -- existing query builder helpers that may support sort/order customization
- `common/src/model/paginated.rs::PaginatedResults` -- response wrapper that the search endpoint must continue to use
- `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService as a reference implementation for service method patterns

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (best match first)
- [ ] A search for a specific term returns the most closely matching entity as the first result
- [ ] The search endpoint response maintains backward compatibility (PaginatedResults format)
- [ ] All existing search integration tests continue to pass
- [ ] New integration tests verify relevance ordering

## Test Requirements
- [ ] Integration test: insert entities with varying degrees of text match to a search term, verify the most relevant entity appears first in results
- [ ] Integration test: search with an exact title match returns that entity as the top result
- [ ] Integration test: verify pagination still works correctly with relevance-ordered results
- [ ] Integration test: verify existing search test cases still pass (regression)

## Verification Commands
- `cargo test --test search` -- run search integration tests, expect all tests to pass
- `cargo build` -- verify the project compiles without errors

## Dependencies
- Depends on: Task 1 -- Optimize search query performance with full-text indexes (full-text indexes improve ranking function performance, though ranking works without them)
