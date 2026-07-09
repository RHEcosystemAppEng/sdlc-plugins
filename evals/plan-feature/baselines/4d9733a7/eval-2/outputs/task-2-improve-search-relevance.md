## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based result ranking for the search endpoint using PostgreSQL's ts_rank scoring. Currently, search results are returned without meaningful ordering by match quality (TC-9002). This task adds relevance scoring to the SearchService so that results are sorted by how well they match the search query, with the most relevant results appearing first.

**Ambiguity note:** No definition of "relevant" is provided in the feature description. The assumption (pending clarification) is that relevance means text match quality as computed by PostgreSQL's ts_rank function. No external search engine or machine learning ranking is required. The team should clarify if additional ranking signals (e.g., recency, popularity, entity type weighting) are desired.

## Files to Modify
- `modules/search/src/service/mod.rs` — add ts_rank scoring to search queries and sort results by relevance score
- `modules/search/src/endpoints/mod.rs` — expose optional `sort_by=relevance` query parameter on the search endpoint

## API Changes
- `GET /api/v2/search` — MODIFY: add optional `sort_by` query parameter accepting `relevance` (default when a search query is provided) or `name`/`date` for explicit ordering. Response items include a new optional `relevance_score` field (float, 0.0-1.0) when sorted by relevance.

## Implementation Notes
- Use `ts_rank(tsvector_column, to_tsquery('english', query))` to compute relevance scores. This depends on the tsvector infrastructure from Task 1.
- Add `relevance_score` as an optional field in search result items. This field is present only when the search is sorted by relevance (i.e., when a text query is provided).
- The `sort_by` query parameter should default to `relevance` when a search query string is provided, and to `name` when no query string is provided (browse mode).
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` from the service method and wrap database errors with `.context("Failed to compute search relevance ranking")`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's handler/service file scope.
- Per CONVENTIONS.md §Response types: the search endpoint already returns `PaginatedResults<T>` from `common/src/model/paginated.rs`. Ensure the response wrapper is preserved; add the `relevance_score` field to the item type, not the wrapper.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Module pattern: maintain the existing model/ + service/ + endpoints/ structure. If a new model type is needed for scored results, place it in the search module's model directory.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Endpoint registration: if adding a new route variant, register it in `modules/search/src/endpoints/mod.rs` following the existing route registration pattern.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Caching: review and update cache configuration in the search endpoint route builder if relevance scoring changes caching semantics (cache keys may need to include the sort parameter).
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint route builder scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` — existing paginated response wrapper; extend the item type to include relevance_score rather than creating a new response type
- `common/src/db/query.rs` — shared query builder helpers for sorting; check for existing sort parameter handling before adding new sort logic

## Acceptance Criteria
- [ ] Search results are sorted by relevance score (ts_rank) when a text query is provided
- [ ] An optional `sort_by` query parameter is available on the search endpoint
- [ ] Response items include `relevance_score` field when sorted by relevance
- [ ] Backward compatibility is maintained — existing API consumers that do not pass `sort_by` get relevance-sorted results by default (matching the improved behavior expectation)

## Test Requirements
- [ ] Integration test verifying results are ordered by relevance score for a known dataset
- [ ] Integration test verifying `sort_by=relevance` returns scored results
- [ ] Integration test verifying `sort_by=name` returns alphabetically sorted results without relevance scores
- [ ] Integration test verifying backward compatibility — requests without `sort_by` return relevance-sorted results when a query is provided

## Verification Commands
- `cargo test -p search` — verify search module tests pass
- `cargo test --test search` — verify search integration tests pass

## Dependencies
- Depends on: Task 1 — Optimize search performance (requires tsvector infrastructure for ts_rank scoring)
