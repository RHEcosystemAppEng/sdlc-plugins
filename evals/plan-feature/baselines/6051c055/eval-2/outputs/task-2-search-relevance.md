## Repository
trustify-backend

## Target Branch
main

## Description
Implement weighted relevance ranking for search results using PostgreSQL's `ts_rank` function. Currently, search results are likely returned in insertion order or arbitrary database order. This task adds explicit relevance scoring so that results matching the query more closely appear first, improving the user's search experience.

ASSUMPTION (pending clarification): The "results should be more relevant" requirement provides no relevance criteria, no field-weight preferences, and no acceptance test for relevance quality. This task implements `ts_rank` with reasonable default weights (title > description > other fields) as a starting point. The weights and ranking strategy should be validated with the Product Owner after deployment.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add `ts_rank` scoring to search queries, order results by relevance score descending, and expose the score in the service response type
- `modules/search/src/endpoints/mod.rs` — Include relevance score in the search API response and add optional `sort` query parameter to allow sorting by relevance (default) or date
- `common/src/db/query.rs` — Add helper function to append `ts_rank` computation and `ORDER BY` clause to search queries

## Files to Create
None.

## Implementation Notes
- Per the repo's CONVENTIONS.md, the project uses the module pattern: model/ + service/ + endpoints/. The ranking logic belongs in the service layer, with the endpoint layer only responsible for serialization and parameter extraction.
- Per the repo's CONVENTIONS.md, error handling uses `Result<T, AppError>` with `.context()`. Any new error paths (e.g., invalid sort parameter) must follow this pattern.
- Per the repo's CONVENTIONS.md, the framework is Axum for HTTP. New query parameters should be extracted using Axum's `Query` extractor with a dedicated params struct.
- The `ts_rank` function signature is: `ts_rank(tsvector, tsquery, normalization)`. Use normalization flag `32` (rank / (rank + 1)) to keep scores between 0 and 1.
- ASSUMPTION (pending clarification): Default field weights will use PostgreSQL's weight categories: A (1.0) for title/name fields, B (0.4) for description fields, C (0.2) for metadata, D (0.1) for other content. These are the standard `ts_rank` defaults and should be tuned based on user feedback.
- ASSUMPTION (pending clarification): The search response model may need a new `score` or `relevance` field. This depends on whether the existing response type is a generic struct or a per-entity type.
- This task depends on task-1 (search indexes) being completed first, as `ts_rank` requires `tsvector` columns to exist.

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (highest first) by default
- [ ] The relevance score is computed using `ts_rank` with weighted fields
- [ ] The search API response includes a `relevance_score` field for each result
- [ ] An optional `sort` query parameter allows switching between `relevance` (default) and `date` ordering
- [ ] Results with exact matches in title/name fields rank higher than partial matches in description fields

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: verify that a search for a term appearing in a title ranks that result above one where the term only appears in the description
- [ ] Integration test: verify that the `sort=date` parameter overrides relevance ordering
- [ ] Integration test: verify that `relevance_score` is present and is a number between 0 and 1 in the API response
