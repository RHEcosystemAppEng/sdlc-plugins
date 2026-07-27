## Repository
trustify-backend

## Target Branch
main

## Description
Create model types for search results following the established model/service/endpoints module pattern used by the sbom, advisory, and package modules. Currently the search module (`modules/search/`) lacks a `model/` directory with structured result types. This task adds a `SearchResultSummary` struct so search results have a consistent type that supports relevance scoring (Task 3) and filtering (Task 2).

## Files to Create
- `modules/search/src/model/mod.rs` — module declaration and re-exports for search model types
- `modules/search/src/model/summary.rs` — `SearchResultSummary` struct with fields for entity type, entity ID, title/name, snippet, and relevance_score

## Files to Modify
- `modules/search/src/lib.rs` — add `pub mod model;` declaration
- `modules/search/src/service/mod.rs` — update SearchService return types to use `SearchResultSummary` instead of raw query results
- `modules/search/src/endpoints/mod.rs` — update GET /api/v2/search handler to return `PaginatedResults<SearchResultSummary>`
- `modules/search/Cargo.toml` — add any necessary dependencies for model serialization

## API Changes
- `GET /api/v2/search` — MODIFY: response body changes from unstructured results to `PaginatedResults<SearchResultSummary>` with fields: `entity_type`, `entity_id`, `title`, `snippet`, `relevance_score`

## Implementation Notes
- Follow the model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary). Each has a struct with derive macros for Serialize, Deserialize, and any ORM traits needed.
- Use `PaginatedResults<SearchResultSummary>` from `common/src/model/paginated.rs` as the response wrapper, matching the pattern used by all list endpoints.
- All handlers must return `Result<T, AppError>` per the error handling convention, with `.context()` wrapping for error propagation (see `common/src/error.rs`).
- Include a `relevance_score: f32` field in `SearchResultSummary` to support relevance ranking in Task 3. Default to 0.0 until scoring is implemented.
- Include an `entity_type: String` field to distinguish between sbom, advisory, and package results, supporting the filtering in Task 2.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper; use directly for the search endpoint response type
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference implementation for the summary struct pattern (derive macros, field types, serialization)
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — another reference implementation showing how severity and other domain fields are included
- `common/src/error.rs::AppError` — error type for handler return signatures

## Acceptance Criteria
- [ ] `modules/search/src/model/mod.rs` and `modules/search/src/model/summary.rs` exist with a `SearchResultSummary` struct
- [ ] `SearchResultSummary` includes fields: entity_type, entity_id, title, snippet, relevance_score
- [ ] GET /api/v2/search returns `PaginatedResults<SearchResultSummary>`
- [ ] The search endpoint compiles and returns results in the new format
- [ ] Existing search functionality is not broken (backward compatibility for callers that consume the response body)

## Test Requirements
- [ ] Verify GET /api/v2/search returns a response matching the `PaginatedResults<SearchResultSummary>` schema
- [ ] Verify `SearchResultSummary` fields are populated correctly for each entity type (sbom, advisory, package)
- [ ] Verify the endpoint returns `StatusCode::OK` with valid search terms
- [ ] Verify the endpoint returns an empty `PaginatedResults` (not an error) for search terms with no matches

## Verification Commands
- `cargo build -p search` — compiles without errors
- `cargo test -p search` — existing tests pass

## Dependencies
- None (this is the foundational task)
