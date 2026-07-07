# Repository Impact Map

## Feature: TC-9002 "Improve search experience"

### Repository: trustify-backend

#### Changes Required

| Area | Files | Change Summary |
|------|-------|----------------|
| Search indexing | `modules/search/src/service/mod.rs` | Add full-text search index creation/migration support; configure `tsvector` columns and GIN indexes for improved query performance |
| Search relevance | `modules/search/src/service/mod.rs` | Implement weighted `ts_rank` scoring to order results by relevance using field-specific weights |
| Query helpers | `common/src/db/query.rs` | Extend query builder with full-text search operators (`@@`, `to_tsquery`), filter composition, and ranking helpers |
| Search endpoint | `modules/search/src/endpoints/mod.rs` | Add query parameters for filters (type, date range, severity) and expose relevance score in response |
| Search tests | `tests/api/search.rs` | Add integration tests covering full-text search, filter combinations, ranking order, and edge cases |
| Database migration | `migration/src/` (new migration file) | SeaORM migration adding GIN indexes and `tsvector` columns to searchable tables |

#### Excluded Requirements

The following items from the feature description are **excluded** from this plan due to insufficient specification. Each requires Product Owner clarification before work can proceed.

1. **"Search should be faster" -- no latency targets defined.**
   The feature requests improved speed but provides no baseline measurements, target latency (e.g., p95 < 200ms), or dataset size expectations. Without measurable targets, there is no way to validate whether the improvement is sufficient. This plan assumes that adding PostgreSQL full-text search indexes (GIN) will improve performance, but cannot guarantee specific latency outcomes.

2. **"Results should be more relevant" -- no relevance criteria defined.**
   The feature requests "more relevant" results but does not define what relevance means in this context: no ranking algorithm preference, no field-weight priorities (e.g., title vs. description), no user feedback mechanism, and no acceptance test for relevance quality. This plan assumes a `ts_rank`-based approach with equal field weights as a reasonable default, but the ranking strategy requires Product Owner validation.

3. **"Add filters" -- no filter types specified.**
   The feature requests filters but does not enumerate which fields should be filterable. This plan assumes three commonly useful filters (type, date range, severity) based on the expected data model, but the actual filter set should be confirmed with stakeholders.

4. **"Better UI" -- no frontend repository or design mockups available.**
   The feature mentions UI improvements, but `trustify-backend` is a backend-only repository. No frontend repository is referenced in the project configuration, no Figma mockups are linked, and no design specifications exist. UI work is entirely excluded from this plan. A separate feature or task in the appropriate frontend repository would be needed.

#### Assumptions

- **ASSUMPTION (pending clarification):** Full-text search will use PostgreSQL `tsvector`/`tsquery` with GIN indexes, as this is the standard approach for the existing PostgreSQL-backed stack.
- **ASSUMPTION (pending clarification):** Filter parameters will be: `type` (string enum), `date_from`/`date_to` (ISO 8601 timestamps), and `severity` (string enum). The actual filterable fields should be confirmed against the data model and product requirements.
- **ASSUMPTION (pending clarification):** Relevance ranking will use `ts_rank` with default weights (D=0.1, C=0.2, B=0.4, A=1.0). Weights should be tuned based on user feedback after initial deployment.
- **ASSUMPTION (pending clarification):** The search endpoint (`GET /api/v2/search`) will be extended in-place rather than creating a new versioned endpoint.
