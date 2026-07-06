## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the search query performance in the SearchService to reduce response latency for GET /api/v2/search. The feature description states that "search is slow" but provides no performance baseline or target SLA — this task addresses the performance concern by optimizing database queries, adding indexes for frequently searched columns, and configuring caching on the search endpoint.

**Assumption (pending clarification):** The primary performance bottleneck is at the database query level (full-text search queries, missing indexes, unoptimized joins). If profiling reveals the bottleneck is elsewhere (e.g., serialization, network), the optimization strategy may need to be revised. No specific latency target has been defined by stakeholders — this task improves performance structurally and measures the improvement, but cannot guarantee a specific SLA without a defined target.

## Files to Modify
- `modules/search/src/service/mod.rs` — Optimize full-text search queries: review and improve query construction, reduce unnecessary joins, leverage PostgreSQL full-text search functions (tsvector/tsquery) if not already used
- `modules/search/src/endpoints/mod.rs` — Add or tune tower-http caching middleware configuration for the search endpoint route builder to cache frequent search queries
- `migration/src/lib.rs` — Register the new search index migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Add database indexes on frequently searched columns (e.g., full-text search indexes on name/description fields across SBOM, advisory, and package entities) to improve query performance

## Implementation Notes
- Profile the existing search queries before optimizing to establish a baseline. Use `EXPLAIN ANALYZE` on the generated SQL to identify slow paths.
- Review `common/src/db/query.rs` for shared query builder patterns — ensure the search service uses the optimized query helpers for pagination and sorting rather than custom implementations.
- When adding database indexes, follow the SeaORM migration pattern established in `migration/src/m0001_initial/mod.rs`. Use `Index::create()` for new indexes.
- For caching, follow the existing tower-http caching middleware pattern used in other endpoint route builders. Set appropriate cache TTLs for search results (search results are relatively dynamic, so short TTLs are recommended).
- **Assumption (pending clarification):** The search scope includes all entity types (SBOMs, advisories, packages). If only a subset should be optimized, the index creation and query optimization can be scoped accordingly.

Per CONVENTIONS.md §Error handling: ensure all new or modified handler functions return `Result<T, AppError>` with `.context()` wrapping for meaningful error messages.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs` rather than implementing custom query logic.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.

Per CONVENTIONS.md §Caching: configure caching using tower-http caching middleware in the endpoint route builder.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` using a real PostgreSQL test database with the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for filtering, pagination, and sorting. Reuse for constructing optimized search queries instead of writing custom query logic.
- `common/src/db/limiter.rs::limiter` — Connection pool limiter. Review whether connection pool limits affect search performance under load.
- `migration/src/m0001_initial/mod.rs` — Established migration pattern for creating database indexes. Follow this pattern for the new search index migration.

## Acceptance Criteria
- [ ] Search queries execute with measurably lower latency than before optimization (document before/after EXPLAIN ANALYZE results)
- [ ] Database indexes are created for full-text search columns via a new migration
- [ ] Caching is configured on the search endpoint with appropriate TTL
- [ ] Existing GET /api/v2/search response shape and query parameters remain backward compatible (no breaking changes)
- [ ] All existing search integration tests continue to pass

## Test Requirements
- [ ] Integration test verifying GET /api/v2/search returns results within acceptable response time under normal data volume
- [ ] Integration test verifying the new migration applies cleanly and creates the expected indexes
- [ ] Integration test verifying cached search responses are returned for repeated identical queries
- [ ] Regression test verifying existing search functionality (basic full-text search) is not broken by optimizations

## Verification Commands
- `cargo test -p tests --test search` — verify all search integration tests pass
- `cargo run -p migration` — verify the new migration applies without errors
