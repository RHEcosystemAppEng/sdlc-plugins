# Task 2 — Refactor SearchService to use full-text search with relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL
native full-text search (`tsvector`/`tsquery`) with `ts_rank` relevance scoring instead
of the current `LIKE`/`ILIKE` pattern matching approach. This directly addresses two
requirements from TC-9002: "Search should be faster" (GIN-indexed tsvector lookups are
orders of magnitude faster than LIKE scans) and "Results should be more relevant"
(ts_rank scores results by term frequency and proximity).

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor the SearchService to build tsquery from user input, query against tsvector columns using `@@` operator, and sort results by `ts_rank` score
- `modules/search/src/lib.rs` — update module exports if the refactored service introduces new public types or re-exports

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Refactor the query logic to:
  1. Parse user search input into a `tsquery` using `plainto_tsquery()` or `websearch_to_tsquery()` for natural language input handling
  2. Match against the `search_vector` tsvector columns added in Task 1 using the `@@` operator
  3. Order results by `ts_rank(search_vector, query)` descending for relevance-based ranking
  4. Fall back gracefully if a search term produces no tsquery matches (e.g., return empty results rather than erroring)
- Use the shared query builder helpers in `common/src/db/query.rs` for pagination and sorting integration. The existing `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` should continue to be used for response formatting.
- Error handling must follow the existing `Result<T, AppError>` pattern with `.context()` wrapping, as established in `common/src/error.rs`.
- Ensure backward compatibility: if no search query is provided, the endpoint should return all results (paginated) as it does today. The `ts_rank` ordering only applies when a search term is present.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9002, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md §5.2 (Code Change Rules): inspect the existing SearchService code before modifying — do not guess its structure or query patterns.

## Reuse Candidates
- `modules/search/src/service/mod.rs` — current SearchService implementation to understand the existing query structure and entity search pattern
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting that the refactored search queries should integrate with
- `common/src/model/paginated.rs` — PaginatedResults<T> response wrapper used by all list endpoints
- `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService showing the established service pattern for querying entities with SeaORM
- `common/src/error.rs` — AppError enum for the error handling pattern used throughout the codebase

## Acceptance Criteria
- [ ] SearchService uses `tsquery`/`tsvector` matching with the `@@` operator instead of `LIKE`/`ILIKE`
- [ ] Search results are ranked by `ts_rank` relevance score in descending order
- [ ] Empty or no search query returns all results (paginated) without error
- [ ] Results are returned in the existing `PaginatedResults<T>` format (backward compatible)
- [ ] Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping

## Test Requirements
- [ ] Full-text search returns relevant results for known test data
- [ ] Results are ordered by relevance (higher-ranked results appear first)
- [ ] Empty search query returns paginated results without error
- [ ] Malformed search input is handled gracefully (no 500 errors)
- [ ] Search across multiple entity types (sbom, advisory, package) returns results from all matching entities

## Verification Commands
- `cargo test -p search` — search module unit tests pass
- `cargo clippy -p search -- -D warnings` — no clippy warnings in the search module

## Dependencies
- Depends on: Task 1 — Add full-text search database migration (tsvector columns and GIN indexes must exist)
