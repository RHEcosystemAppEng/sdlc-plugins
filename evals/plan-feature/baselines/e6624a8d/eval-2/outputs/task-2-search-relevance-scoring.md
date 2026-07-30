## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance scoring and ranking for search results in the SearchService. Currently, search results are returned without meaningful ordering by relevance. This task adds a scoring mechanism so that results matching the query more closely are ranked higher in the response.

**Assumption pending clarification:** No relevance criteria have been defined by the feature owner. This task assumes implementing PostgreSQL full-text search ranking (e.g., `ts_rank` or equivalent SeaORM constructs) as a baseline relevance mechanism. The specific ranking weights and factors (text match quality, recency, entity type boosting) should be validated with stakeholders.

**Assumption pending clarification:** It is unclear whether relevance scoring should apply uniformly across all entity types (SBOMs, advisories, packages) or use entity-specific ranking factors. This task assumes uniform scoring as a starting point.

## Files to Modify
- `modules/search/src/service/mod.rs` — add relevance scoring logic to search query and result ordering
- `modules/search/src/endpoints/mod.rs` — expose relevance score in search response (if applicable) and ensure results are ordered by score
- `tests/api/search.rs` — add integration tests verifying result ordering by relevance

## API Changes
- `GET /api/v2/search` — MODIFY: results are now ordered by relevance score (descending) by default; response may include an optional `score` field per result

## Implementation Notes
- Inspect the current `SearchService` in `modules/search/src/service/mod.rs` to understand the existing full-text search query structure. Identify where to inject ranking/scoring logic.
- SeaORM supports raw SQL expressions — use this to leverage PostgreSQL's `ts_rank()` or `ts_rank_cd()` functions for full-text search ranking if the search uses `tsvector`/`tsquery`.
- Ensure the relevance-ordered results still work with the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` — pagination must be applied after sorting by relevance.
- Review the existing entity models (`entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`) to understand which text fields are searchable and should contribute to relevance scoring.
- The search endpoint in `modules/search/src/endpoints/mod.rs` should default to relevance ordering but may accept an optional `sort` parameter to allow overriding with other orderings.

Per CONVENTIONS.md (Key Conventions) - Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust handler file scope.

Per CONVENTIONS.md (Key Conventions) - Module pattern: each domain module follows `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module structure scope.

Per CONVENTIONS.md (Key Conventions) - Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint response scope.

Per CONVENTIONS.md (Key Conventions) - Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` — existing paginated response wrapper that must be preserved when adding relevance-based ordering
- `common/src/db/query.rs::sorting helpers` — existing sorting infrastructure that may support adding a relevance-score sort key

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (most relevant first) by default
- [ ] Relevance scoring produces meaningfully different scores for different query-result match quality
- [ ] Existing search behavior is preserved for empty or wildcard queries
- [ ] Pagination continues to work correctly with relevance-ordered results
- [ ] Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping

## Test Requirements
- [ ] Integration test verifying that a specific search term returns its exact match ranked higher than partial matches
- [ ] Integration test verifying that relevance ordering does not break pagination (page 2 results differ from page 1)
- [ ] Integration test verifying that existing search queries still return expected results (regression)
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` — run search integration tests, expected: all pass
- `cargo build` — verify compilation, expected: success with no errors

## Dependencies
- None
