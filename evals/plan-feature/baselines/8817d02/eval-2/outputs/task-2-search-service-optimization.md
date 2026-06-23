# Task 2 — Optimize SearchService with full-text search and relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL full-text search (tsvector/tsquery) with `ts_rank` for relevance-based result ordering. This replaces any existing naive text matching (LIKE/ILIKE) with proper full-text search that leverages the GIN indexes created in Task 1. Results are returned ordered by relevance score.

**Ambiguity note (assumption pending clarification):** The feature description says "Results should be more relevant" without defining relevance criteria or ranking weights. We assume `ts_rank` with default weights is sufficient as a starting point. If stakeholders require field-specific weighting (e.g., title matches ranked higher than description matches), the weights in the `setweight()` calls within the migration triggers (Task 1) and the `ts_rank` call here should be adjusted accordingly.

**Ambiguity note (assumption pending clarification):** The feature says search is "currently too slow" without baseline metrics. We assume the primary performance bottleneck is the lack of full-text indexes, and that switching from LIKE/ILIKE to tsvector/tsquery with GIN indexes will provide sufficient improvement. A measurable performance target (e.g., p95 latency < 200ms) should be defined by stakeholders.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace text matching logic with tsquery-based search using `ts_rank` for ordering
- `modules/search/src/lib.rs` — update any re-exports if the service interface changes

## Implementation Notes
- In `modules/search/src/service/mod.rs`, locate the existing `SearchService` and its full-text search method. Replace LIKE/ILIKE queries with `to_tsquery('english', ...)` matched against the `search_vector` column using the `@@` operator.
- Add `ts_rank(search_vector, query)` as an ORDER BY clause to sort results by relevance.
- Use `plainto_tsquery` for simple user input or `websearch_to_tsquery` if the PostgreSQL version supports it, to handle multi-word queries gracefully.
- Preserve the existing `PaginatedResults<T>` response wrapper from `common/src/model/paginated.rs` — the response shape must not change (backward compatibility per ambiguity 5 in the impact map).
- Use the shared query builder helpers in `common/src/db/query.rs` for pagination and sorting integration.
- All handlers must continue to return `Result<T, AppError>` using the error handling pattern from `common/src/error.rs`.
- Per `docs/constraints.md` §5.4: do not duplicate existing functionality — reuse `common/src/db/query.rs` helpers for pagination/sorting.
- Per `docs/constraints.md` §5.1: changes must be scoped to the files listed above.
- Per `docs/constraints.md` §2 (Commit Rules): commit must reference TC-9002 in the footer.

### Convention applicability
- Per CONVENTIONS.md §Module pattern: follow `model/ + service/ + endpoints/` structure.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module service scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for integrating relevance-ranked results with existing pagination
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; must be used for search results
- `common/src/error.rs` — `AppError` enum for error handling; follow existing `.context()` wrapping pattern
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` demonstrates the existing service pattern including search; use as reference for service method signatures

## Acceptance Criteria
- [ ] `SearchService` uses `tsvector`/`tsquery` for full-text search instead of LIKE/ILIKE
- [ ] Search results are ordered by `ts_rank` relevance score (most relevant first)
- [ ] Multi-word queries are handled correctly (e.g., "security vulnerability" matches documents containing both words)
- [ ] The search endpoint continues to return `PaginatedResults<T>` with the same response shape (backward compatible)
- [ ] Empty search queries return a sensible default (e.g., empty results or all results paginated)
- [ ] Search across SBOMs, Advisories, and Packages works correctly

## Test Requirements
- [ ] Integration test: search with a single keyword returns results containing that keyword
- [ ] Integration test: search with multiple keywords returns results ranked by relevance (documents containing all keywords ranked higher)
- [ ] Integration test: search returns results across entity types (SBOMs, Advisories, Packages)
- [ ] Integration test: search with no matching results returns empty `PaginatedResults`
- [ ] Integration test: verify backward compatibility — existing search API calls with the same parameters return results in the expected shape

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — integration tests in `tests/api/search.rs` pass

## Dependencies
- Depends on: Task 1 — Add full-text search database migration

[sdlc-workflow] Description digest: sha256-md:84efee3f4940b70919269547496b9599219e4d86438fcc785574c584e975d8fa
