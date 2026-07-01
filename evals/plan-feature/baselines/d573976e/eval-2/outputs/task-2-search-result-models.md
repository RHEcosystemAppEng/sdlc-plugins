# Task 2 — Add search result model types with relevance scoring

## Repository
trustify-backend

## Target Branch
main

## Description
Create dedicated model types for search results that include relevance scores and entity type discrimination. Currently, the search module (`modules/search/`) lacks a `model/` directory, unlike other domain modules (sbom, advisory, package) which all follow the `model/ + service/ + endpoints/` pattern. Adding search-specific result types enables the endpoint to return ranked, typed results that consumers can differentiate by entity kind.

## Files to Create
- `modules/search/src/model/mod.rs` — module registration for search models
- `modules/search/src/model/summary.rs` — `SearchResultSummary` struct containing: entity type discriminator (enum: Sbom, Advisory, Package), entity ID, display title, snippet/excerpt, relevance score (f64), and entity-specific metadata (severity for advisories, license for packages)

## Files to Modify
- `modules/search/src/lib.rs` — add `pub mod model;` declaration
- `modules/search/src/service/mod.rs` — update `SearchService` return types to use the new `SearchResultSummary` instead of raw entity types

## Implementation Notes
- Follow the model pattern from `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) for struct layout, derive macros, and serialization.
- The `SearchResultSummary` should implement `Serialize` and `Deserialize` (serde) for JSON API responses.
- Use a Rust enum for the entity type discriminator with serde tag for JSON discrimination:
  ```rust
  #[serde(tag = "type")]
  pub enum SearchEntityType { Sbom, Advisory, Package }
  ```
- The relevance score field should carry the `ts_rank` value from PostgreSQL full-text search (to be wired up in Task 3).
- The `SearchService` changes should maintain backward compatibility — the new types wrap the existing data, they don't replace the underlying queries yet.
- Follow error handling pattern: all methods return `Result<T, AppError>` with `.context()` wrapping.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — struct layout pattern with serde derives
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes severity field, demonstrates entity-specific metadata pattern
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes license field, another metadata pattern
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper that search results will be wrapped in

## Acceptance Criteria
- [ ] `SearchResultSummary` struct exists with entity type, ID, title, snippet, relevance score, and metadata fields
- [ ] Entity type discriminator enum correctly serializes to JSON with type tagging
- [ ] `SearchService` return type updated to use `SearchResultSummary`
- [ ] Module follows the existing `model/ + service/ + endpoints/` directory convention

## Test Requirements
- [ ] Unit test verifying `SearchResultSummary` serialization/deserialization roundtrip
- [ ] Unit test verifying entity type discriminator produces correct JSON tags

## Dependencies
- None (can proceed in parallel with Task 1, though both are needed before Task 3)
