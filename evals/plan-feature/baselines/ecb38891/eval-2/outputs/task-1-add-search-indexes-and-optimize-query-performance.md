## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes optimized for full-text search and optimize the SearchService query execution to improve search response times. Users have reported that search is slow (TC-9002). This task addresses the performance aspect by ensuring proper GIN indexes exist on searchable text columns and that the SearchService query path is optimized to use these indexes efficiently.

**Note:** The feature does not specify quantitative performance targets. This task implements standard PostgreSQL full-text search optimizations (GIN indexing, query plan optimization). Performance benchmarks should be established with the product owner for future validation.

## Files to Modify
- `modules/search/src/service/mod.rs` — Optimize SearchService query construction to use indexed full-text search (tsvector/tsquery) instead of LIKE/ILIKE patterns if present; ensure queries use parameterized tsquery for GIN index utilization
- `modules/search/src/endpoints/mod.rs` — Add cache-control headers for search results using tower-http caching middleware configuration
- `tests/api/search.rs` — Add integration tests for search performance characteristics (index-backed queries return results, large result sets are paginated)

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — SeaORM migration adding GIN indexes on full-text searchable columns across SBOM, advisory, and package entities

## Implementation Notes
- Per CONVENTIONS.md (Key Conventions) - Module pattern: follow the existing `model/ + service/ + endpoints/` structure in the search module. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module structure scope.
- Per CONVENTIONS.md (Key Conventions) - Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping on database operations. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust error handling scope.
- Per CONVENTIONS.md (Key Conventions) - Response types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint response scope.
- Per CONVENTIONS.md (Key Conventions) - Caching: use `tower-http` caching middleware for search endpoint route builders. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's caching scope.
- Per CONVENTIONS.md (Key Conventions) - Testing: integration tests go in `tests/api/` and hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.
- Use PostgreSQL GIN indexes on `tsvector` columns for full-text search. The migration should create tsvector columns (or use `to_tsvector()` in the query) and add GIN indexes.
- Examine the existing query patterns in `common/src/db/query.rs` for pagination and sorting — ensure the search query integrates with these helpers rather than implementing custom pagination.
- See `modules/fundamental/src/sbom/endpoints/list.rs` for an example of a list endpoint that uses `PaginatedResults<T>` with the shared query helpers.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — shared filtering, pagination, and sorting utilities that the search query should integrate with rather than implementing custom logic
- `common/src/model/paginated.rs::PaginatedResults<T>` — standard paginated response wrapper already used by all list endpoints
- `common/src/db/limiter.rs::connection pool limiter` — connection pool management that search queries should respect for resource control
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation of a list endpoint using PaginatedResults with query helpers

## Acceptance Criteria
- [ ] GIN indexes are created on full-text searchable columns for SBOM, advisory, and package entities via a new SeaORM migration
- [ ] SearchService queries use `tsvector`/`tsquery` with GIN index utilization (no sequential scans on text columns for search queries)
- [ ] Search endpoint returns `PaginatedResults<T>` using the shared paginated response wrapper
- [ ] Cache-control headers are configured on the search endpoint using tower-http caching middleware
- [ ] Existing search functionality is not broken (all existing tests continue to pass)

## Test Requirements
- [ ] Integration test: verify search queries return results when matching documents exist in the database
- [ ] Integration test: verify search queries return empty results (not errors) when no documents match
- [ ] Integration test: verify paginated search results include correct `total` count and respect `limit`/`offset` parameters
- [ ] Integration test: verify the migration applies cleanly and indexes are created (migration up/down)

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass
- `cargo test -p migration` — migration tests pass

## Dependencies
- None (this is the first task — no prior dependencies)
