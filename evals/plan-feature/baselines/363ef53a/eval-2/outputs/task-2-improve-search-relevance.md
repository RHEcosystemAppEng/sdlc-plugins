## Repository
trustify-backend

## Target Branch
main

## Description
Improve search result relevance by adding a ranking and scoring mechanism to the SearchService. Currently, search results are returned without relevance ordering, causing users to see irrelevant results. This task introduces a search result model with a relevance score and implements ranking logic using PostgreSQL full-text search capabilities (ts_rank or similar).

**Assumption (pending clarification):** The feature description does not define what "relevant" means or what ranking criteria to use. This task assumes relevance is determined by text match quality using PostgreSQL's built-in full-text search ranking (ts_rank). The product owner should clarify whether additional relevance signals are needed (e.g., recency, popularity, user-specific weighting).

**Assumption (pending clarification):** The feature description does not specify whether relevance scoring should be exposed in the API response or used only for internal ordering. This task assumes the score should be included in the response so that consumers can display or further filter by relevance. If the score should be hidden, the API Changes section should be adjusted.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Add relevance scoring and ranking logic to search queries using PostgreSQL full-text search functions
- `modules/search/src/endpoints/mod.rs` -- Update the search endpoint response to include the relevance score and order results by rank
- `modules/search/src/lib.rs` -- Register the new model module

## Files to Create
- `modules/search/src/model/mod.rs` -- Module registration for search result models
- `modules/search/src/model/summary.rs` -- SearchResultSummary struct with entity reference, match context, and relevance score field

## API Changes
- `GET /api/v2/search` -- MODIFY: response items now include a `score` field (f64) representing relevance rank; results are ordered by score descending by default

## Implementation Notes
- Follow the model pattern from `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) for structuring the SearchResultSummary type. Include fields for entity type, entity ID, matched text excerpt, and relevance score.
- Follow the module structure pattern: the search module currently has `service/` and `endpoints/` but no `model/` directory. Add `model/mod.rs` and `model/summary.rs` following the same structure as `modules/fundamental/src/sbom/model/`.
- Use PostgreSQL `ts_vector` and `ts_rank` functions via SeaORM raw queries or expressions for computing relevance scores. Reference the existing full-text search implementation in `modules/search/src/service/mod.rs` to understand the current query structure before modifying it.
- Per CONVENTIONS.md §Module pattern: follow the established model/ + service/ + endpoints/ structure for the search module. See `modules/fundamental/src/sbom/` for a complete reference. Applies: task creates `modules/search/src/model/mod.rs` matching the convention's module structure scope.
- Per CONVENTIONS.md §Error handling: wrap all new database operations and ranking computations with `.context()` for descriptive error messages. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Response types: wrap ranked search results in `PaginatedResults<SearchResultSummary>` from `common/src/model/paginated.rs`. See `modules/fundamental/src/sbom/endpoints/list.rs` for the established pattern. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint list scope.
- Per CONVENTIONS.md §Endpoint registration: register any new routes in `modules/search/src/endpoints/mod.rs`. See `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration pattern. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Query helpers: use shared pagination and sorting from `common/src/db/query.rs` to integrate relevance-based sorting with existing pagination support. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's query builder scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- Existing summary model struct showing the established pattern for response types with derived fields
- `common/src/model/paginated.rs::PaginatedResults` -- Wrapper for paginated responses; use with SearchResultSummary for the ranked results response
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- Service pattern with list and search capabilities that can inform the ranking query structure
- `common/src/db/query.rs` -- Shared query builder helpers for pagination and sorting integration

## Acceptance Criteria
- [ ] SearchResultSummary model is created with entity reference, matched text, and relevance score fields
- [ ] Search results are ranked by relevance score in descending order
- [ ] GET /api/v2/search response includes the score field for each result
- [ ] Results with higher text match quality appear before less relevant results
- [ ] Existing search functionality is not broken (backward-compatible response shape with added field)

## Test Requirements
- [ ] Integration test: search for a specific term returns the most relevant entity first (highest score)
- [ ] Integration test: search results include a numeric score field in the response body
- [ ] Integration test: search results are ordered by score descending
- [ ] Integration test: search with no matches returns an empty paginated result
- [ ] Integration test: verify backward compatibility -- existing search response fields remain present

## Verification Commands
- `cargo test -p tests --test search` -- verify all search integration tests pass
- `cargo build -p search` -- verify search module compiles with new model types

## Dependencies
- Depends on: Task 1 -- Optimize search query performance (indexes should be in place before adding ranking)
