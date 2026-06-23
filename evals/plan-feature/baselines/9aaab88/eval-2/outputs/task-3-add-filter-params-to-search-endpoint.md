## Repository
trustify-backend

## Target Branch
main

## Description
Extend the search API endpoint to accept filter query parameters so users can narrow search results by entity type, date range, and severity. The current GET /api/v2/search endpoint in `modules/search/src/endpoints/mod.rs` does not support filtering. This task adds optional query parameters that map to the SearchFilter model.

**Assumption pending clarification**: The filter parameters are added as optional query parameters to the existing GET /api/v2/search endpoint rather than creating a new endpoint, since the feature description says "add filters" without specifying the API design.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- Add SearchFilterQuery extractor struct with optional query parameters (entity_type, date_from, date_to, severity); parse parameters into SearchFilter and pass to SearchService; return results as PaginatedResults<SearchResultItem>

## API Changes
- `GET /api/v2/search` -- MODIFY: add optional query parameters `entity_type` (string enum: sbom|advisory|package), `date_from` (ISO 8601), `date_to` (ISO 8601), `severity` (string enum matching advisory severity levels). All parameters are optional for backward compatibility.

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` (GET /api/v2/sbom) for handling query parameters with Axum extractors. The existing route registration pattern in `modules/search/src/endpoints/mod.rs` should be extended, not replaced.

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Use the `Query<T>` Axum extractor for parsing filter parameters. Deserialize into a SearchFilterQuery struct, convert to SearchFilter, and pass to SearchService.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- example of list endpoint with query parameters and PaginatedResults response
- `common/src/model/paginated.rs::PaginatedResults<T>` -- standard paginated response wrapper
- `common/src/error.rs::AppError` -- error type with IntoResponse implementation

## Dependencies
- Depends on: Task 2 -- Add full-text search ranking to search service (requires updated SearchService with filter support)

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional query parameters: entity_type, date_from, date_to, severity
- [ ] Omitting all filter parameters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Response uses PaginatedResults<SearchResultItem> format
- [ ] Results include relevance_score from the search service
- [ ] **Assumption pending clarification**: Filter parameter names and types match stakeholder API design expectations

## Test Requirements
- [ ] Integration test that GET /api/v2/search without filters returns 200 with paginated results
- [ ] Integration test that GET /api/v2/search?entity_type=sbom returns only SBOM results
- [ ] Integration test that GET /api/v2/search with date_from and date_to filters returns date-scoped results
- [ ] Integration test that GET /api/v2/search with invalid entity_type returns 400

[sdlc-workflow] Description digest: sha256-md:a33e1160ac3230a1dd95d6b064b486a4cf4829b4bc4ae6e3c7fe2417a53940f1
