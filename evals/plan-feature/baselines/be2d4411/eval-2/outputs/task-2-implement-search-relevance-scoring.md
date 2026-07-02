## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the `SearchService` with PostgreSQL full-text search capabilities and relevance
scoring using `tsvector`/`tsquery` and `ts_rank`. This replaces the presumed simple
LIKE/ILIKE pattern matching with ranked search results, so that results are ordered by
relevance to the user's query. Search results will include a relevance score and be
sorted by score descending by default.

**Ambiguity note:** The feature description does not define what "more relevant" means —
no ranking algorithm preference, no examples of irrelevant results, no expected result
ordering test cases. This task assumes PostgreSQL full-text search with `ts_rank` scoring
is the appropriate approach. This assumption is pending stakeholder clarification.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` to use `tsvector`/`tsquery` for full-text search with `ts_rank` scoring instead of simple pattern matching
- `modules/search/src/endpoints/mod.rs` — update the `GET /api/v2/search` endpoint to accept a `q` query parameter and return results sorted by relevance score
- `tests/api/search.rs` — add integration tests for relevance-scored search results

## Files to Create
- `modules/search/src/model/mod.rs` — define `SearchResult` struct wrapping entity summaries with a `score: f32` relevance field, and `SearchQuery` struct for parsed search parameters

## API Changes
- `GET /api/v2/search` — MODIFY: add `q` query parameter for the search term; response now includes `score` field in each result item and results are sorted by score descending by default

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` provides the full-text search implementation. Refactor it to:
  1. Build a `tsquery` from the user's search term using `plainto_tsquery('english', &query)`
  2. Match against `tsvector` columns indexed in Task 1
  3. Rank results using `ts_rank(tsvector_column, tsquery)` and order by rank descending
- The new `SearchResult` model should wrap the existing entity summary types (`SbomSummary` from `modules/fundamental/src/sbom/model/summary.rs`, `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs`, `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`) with a `score` field.
- Use the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` for the response — the new `SearchResult` type replaces the generic `T` parameter.
- Follow the endpoint registration pattern: update route configuration in `modules/search/src/endpoints/mod.rs` to extract the `q` query parameter.
- Use the shared query builder helpers from `common/src/db/query.rs` for pagination and sorting integration.
- All endpoint handlers must return `Result<T, AppError>` using `.context()` error wrapping from `common/src/error.rs`.
- Follow the module pattern: model/ + service/ + endpoints/ as established in `modules/fundamental/src/sbom/`.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for integrating relevance-based sort with existing pagination
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; reuse as the outer response type for search results
- `common/src/error.rs` — `AppError` enum with `IntoResponse` implementation; reuse for error handling
- `modules/fundamental/src/sbom/model/summary.rs` — `SbomSummary` struct; reference for entity summary type that SearchResult wraps
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct; reference for entity summary type
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` implementation; reference for service pattern (fetch, list methods)

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=<term>` returns results ranked by relevance score (highest first)
- [ ] Each search result item includes a `score` field indicating its relevance to the query
- [ ] Full-text search matches across SBOM names, advisory titles/descriptions, and package names
- [ ] Empty or missing `q` parameter returns all results (backward compatible with existing callers)
- [ ] Response structure uses `PaginatedResults<SearchResult>` maintaining backward compatibility with pagination parameters

## Test Requirements
- [ ] Integration test: search for a known term returns matching results with non-zero scores
- [ ] Integration test: results are ordered by score descending (most relevant first)
- [ ] Integration test: search for a term present in multiple entity types returns results from all matching entities
- [ ] Integration test: empty query returns results (backward compatibility)
- [ ] Integration test: search for a non-existent term returns empty results with 200 status

## Verification Commands
- `cargo test -p search` — search module compiles and unit tests pass
- `cargo test -p tests --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add database migration for search performance indexes

## additional_fields
- priority: Normal
- fixVersions: RHTPA 1.6.0
- labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:1fd3b4a1d501b3683e21cd2f1f097715b88435a8744086a6771528204b20f3cc
