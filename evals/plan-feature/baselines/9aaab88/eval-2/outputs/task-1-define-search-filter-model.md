## Repository
trustify-backend

## Target Branch
main

## Description
Define the model types for search filters and improved search results. The current search module (`modules/search/`) lacks structured filter types. This task creates the model layer that will be used by the search service and endpoints to support filtering by entity type, date range, and severity.

**Assumption pending clarification**: The specific filter fields (entity type, date range, severity) are assumed based on the existing entity model since the feature description only says "some kind of filtering capability" without specifying which fields.

## Files to Create
- `modules/search/src/model/mod.rs` -- Define SearchFilter struct with optional fields for entity_type, date_from, date_to, and severity; define SearchResultItem struct with relevance score field

## Files to Modify
- `modules/search/src/lib.rs` -- Add `pub mod model;` to expose the new model module

## Implementation Notes
Follow the existing module pattern used in `modules/fundamental/src/sbom/model/mod.rs` and `modules/fundamental/src/advisory/model/summary.rs` for struct definitions with serde derives.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure for the search module.
Applies: task creates `modules/search/src/model/mod.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Response types: use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the search result wrapper.
Applies: task creates `modules/search/src/model/mod.rs` matching the convention's `.rs` file scope.

Reuse the severity field pattern from `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary includes a severity field). Reuse the paginated response pattern from `common/src/model/paginated.rs` (PaginatedResults<T>).

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` -- wraps paginated list responses; search results should use this same wrapper
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains severity field pattern to reuse for severity filter enum values

## Acceptance Criteria
- [ ] SearchFilter struct defined with optional fields: entity_type (enum), date_from (DateTime), date_to (DateTime), severity (enum)
- [ ] SearchResultItem struct defined with fields for entity reference and relevance_score (f64)
- [ ] Model module is publicly exported from `modules/search/src/lib.rs`
- [ ] All structs derive Serialize, Deserialize, and Debug
- [ ] **Assumption pending clarification**: Filter fields match stakeholder requirements (entity_type, date_range, severity are assumed)

## Test Requirements
- [ ] Unit test that SearchFilter serializes/deserializes correctly with all fields populated
- [ ] Unit test that SearchFilter serializes/deserializes correctly with all optional fields as None
- [ ] Unit test that SearchResultItem includes relevance_score in serialized output

[sdlc-workflow] Description digest: sha256-md:3b3ceceb47a34470d700f4f86186dbec82690744383fd7987cc987f6367debef
