# Task 3: Add entity-type filter to search API

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Add an entity-type filter parameter to the search endpoint so users can restrict search results to specific entity types (SBOM, advisory, package). The feature TC-9002 requires "add filters" but provides no specification of which filters. Entity-type filtering is the most fundamental filter for a cross-entity search service.

**Assumption**: The initial filter values will be `sbom`, `advisory`, and `package`, matching the three entity types in the data model (see `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`). The filter accepts a single value or comma-separated list for multi-select. This assumption is pending clarification from the product owner on the exact filter specification.

**Assumption**: When no entity-type filter is provided, all entity types are searched (backward-compatible default behavior).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add `entity_type` query parameter to the search endpoint
- `modules/search/src/service/mod.rs` — Extend SearchService to filter queries by entity type

## Implementation Notes
In the search endpoint (`modules/search/src/endpoints/mod.rs`):
- Add an optional `entity_type` query parameter accepting values: `sbom`, `advisory`, `package` (or comma-separated combination)
- Parse and validate the parameter, returning a 400 Bad Request via `AppError` for invalid entity types
- Pass the parsed entity types to the service layer

In the SearchService (`modules/search/src/service/mod.rs`):
- Accept an optional entity-type filter parameter
- When present, restrict the search query to only the specified entity tables
- When absent, search across all entity types (current behavior preserved)

Leverage the filtering utilities in `common/src/db/query.rs` to build the entity-type filter clause. Follow the existing pattern where list endpoints accept filter parameters via query strings.

Per CONVENTIONS.md §Module pattern: Maintain the model/ + service/ + endpoints/ structure. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's modules directory scope.

Per CONVENTIONS.md §Error handling: Return Result<T, AppError> with .context() wrapping for validation errors. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Endpoint registration: Register any new routes via endpoints/mod.rs. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's file path scope (endpoints/mod.rs).

Per CONVENTIONS.md §Query helpers: Use shared filtering utilities from common/src/db/query.rs for the entity-type filter. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's file path scope (common/src/db/query.rs).

## Reuse Candidates
- `common/src/db/query.rs::filtering helpers` — Reuse existing filter clause builders for the entity-type filter instead of writing custom WHERE clause logic
- `common/src/error.rs::AppError` — Use existing error enum for invalid filter value responses

## Acceptance Criteria
- [ ] Search endpoint accepts an optional `entity_type` query parameter
- [ ] Valid values are `sbom`, `advisory`, `package` (single or comma-separated)
- [ ] Invalid entity type values return 400 Bad Request with a descriptive error message
- [ ] When `entity_type` is omitted, all entity types are searched (backward compatible)
- [ ] When `entity_type=sbom`, only SBOM results are returned
- [ ] Filtering works in combination with the existing search query parameter

## Test Requirements
- [ ] Search with `entity_type=sbom` returns only SBOM results
- [ ] Search with `entity_type=advisory,package` returns advisory and package results but not SBOMs
- [ ] Search without `entity_type` returns all entity types
- [ ] Invalid `entity_type` value returns 400 status code
- [ ] Entity-type filter combined with a text query returns correctly filtered and matched results

## Verification Commands
- `cargo test -p modules-search` — search module compiles and tests pass
- `cargo test -p tests --test search` — integration tests pass

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional `entity_type` query parameter (values: `sbom`, `advisory`, `package`; comma-separated for multi-select)
