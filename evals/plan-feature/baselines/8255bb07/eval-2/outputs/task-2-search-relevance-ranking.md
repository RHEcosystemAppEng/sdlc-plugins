# Task 2 — Implement relevance-based search result ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based ranking for search results so that results matching more query terms or matching them more precisely are ranked higher. Currently, the `SearchService` returns results without meaningful ordering, leading to user complaints about irrelevant results appearing first.

This task adds PostgreSQL `ts_rank()` scoring to the search query and exposes an optional `sort` parameter on the search endpoint to allow sorting by relevance (default) or other criteria.

**Assumption:** "Results should be more relevant" is interpreted as ranking results by PostgreSQL full-text search scoring (`ts_rank`), with results matching more query terms scoring higher. No specific relevance algorithm or ranking criteria were provided in the feature description (see TC-9002 ambiguity #2).

## Files to Modify
- `modules/search/src/service/mod.rs` — Add `ts_rank()` scoring to the search query and order results by relevance score descending
- `modules/search/src/endpoints/mod.rs` — Add optional `sort` query parameter (values: `relevance`, `name`, `date`) with `relevance` as the default when a search query is present
- `tests/api/search.rs` — Add integration tests verifying result ordering by relevance score

## Implementation Notes
- Use PostgreSQL `ts_rank(to_tsvector(text), to_tsquery(query))` to compute a relevance score for each matched row. The `ts_rank` function returns a float that can be used in `ORDER BY` clauses.
- The relevance score should be computed within the SQL query, not in application code, to allow the database to optimize the sort.
- Add a `sort` query parameter to the `GET /api/v2/search` endpoint. Valid values: `relevance` (default when `q` is present), `name`, `date`. This parameter is optional and additive — the existing endpoint contract is preserved.
- The search endpoint in `modules/search/src/endpoints/mod.rs` registers the route for `GET /api/v2/search`. Follow the existing pattern for adding query parameters.
- Per CONVENTIONS.md §Error Handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. The new sort parameter parsing must follow this pattern.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Query Helpers: use the shared sorting helpers from `common/src/db/query.rs` for the sort parameter implementation rather than implementing custom sorting logic.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Response Types: search results returned via the endpoint must continue using `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/search.rs` using the established test database pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test file scope.
- Relevant constraints from `docs/constraints.md`: commit messages must follow Conventional Commits (§2.2), every commit must reference TC-9002 in the footer (§2.1), and changes must be scoped to the files listed above (§5.1).

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers including sorting utilities. The sort parameter should delegate to these existing helpers for non-relevance sort orders (name, date).
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper that must be preserved for the search endpoint's return type. Relevance ranking changes the ordering within the paginated results, not the response shape.
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Example of a service implementing search with query parameters. Follow the same pattern for integrating relevance scoring.

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (most relevant first) when a query term is provided
- [ ] An optional `sort` query parameter is available on `GET /api/v2/search` with values `relevance`, `name`, `date`
- [ ] Default sort order is `relevance` when a search query is present
- [ ] Existing search endpoint contract is preserved (the `sort` parameter is optional; omitting it produces the same response shape)
- [ ] All existing integration tests continue to pass

## Test Requirements
- [ ] Integration test: verify that search results are returned in relevance-ranked order (a result matching the full query term ranks above a partial match)
- [ ] Integration test: verify `GET /api/v2/search?q=<term>&sort=relevance` returns results ordered by relevance
- [ ] Integration test: verify `GET /api/v2/search?q=<term>&sort=name` returns results ordered alphabetically
- [ ] Integration test: verify `GET /api/v2/search?q=<term>` with no sort parameter defaults to relevance ordering
- [ ] Integration test: verify invalid sort values return a 400 error with a descriptive message

## Verification Commands
- `cargo test -p search` — verify search module compiles with the ranking logic
- `cargo test --test search` — run search integration tests against the test database

## Dependencies
- Depends on: Task 1 — Add database indexes and optimize search query performance (relevance ranking benefits from the full-text search indexes created in Task 1, though it can function without them at reduced performance)
