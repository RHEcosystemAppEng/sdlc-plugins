## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` to use PostgreSQL full-text search with `ts_rank` scoring so that search results are ordered by relevance instead of being returned in an unranked order. This addresses the requirement that "results should be more relevant."

**Assumption pending clarification:** The feature description states users complain about "irrelevant results" but provides no definition of relevance, no ranking criteria, and no example queries with expected results. This task assumes relevance means ordering results by PostgreSQL `ts_rank` text match quality score. If stakeholders have specific ranking requirements (e.g., boost recently ingested SBOMs, weight advisory severity), those need to be specified before this approach can be validated.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` to use `to_tsquery` and `ts_rank` for full-text search queries and relevance-based ordering
- `modules/search/src/endpoints/mod.rs` — update the search endpoint handler to pass the search query to the refactored service and expose relevance score in results if applicable

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` provides full-text search across entities. Refactor it to:
  1. Convert user search terms to a `tsquery` using `plainto_tsquery('english', ...)` for natural language queries
  2. Match against the `tsvector` columns added by Task 1's migration
  3. Order results by `ts_rank(tsvector_column, tsquery)` descending
- The search endpoint in `modules/search/src/endpoints/mod.rs` currently registers `GET /api/v2/search`. Update the handler to use the refactored service method.
- Leverage the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` for response formatting.
- Follow the error handling pattern: `Result<T, AppError>` with `.context()` wrapping, as used throughout `modules/fundamental/src/sbom/service/sbom.rs` and other service modules.
- Per docs/constraints.md §5 (Code Change Rules): keep changes scoped to the search module; do not modify other domain modules.

## Acceptance Criteria
- [ ] Search queries return results ordered by relevance score (best match first)
- [ ] Search results using `ts_rank` scoring are demonstrably better-ordered than the previous unranked results for multi-word queries
- [ ] Empty search queries return results in a deterministic order (e.g., by creation date)
- [ ] Existing search API contract (request/response shape) is preserved — no breaking changes
- [ ] **Assumption pending clarification:** No specific relevance benchmarks exist; acceptance is subjective until stakeholders define expected query-result pairs

## Test Requirements
- [ ] Test that a search for a specific term returns the most relevant entity first (e.g., searching "openssl" returns an SBOM named "openssl" before one that merely references it)
- [ ] Test that multi-word search queries rank exact matches above partial matches
- [ ] Test that empty or whitespace-only search terms do not cause errors
- [ ] Test that pagination still works correctly with relevance-ordered results

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (requires `tsvector` columns and GIN indexes to exist)
