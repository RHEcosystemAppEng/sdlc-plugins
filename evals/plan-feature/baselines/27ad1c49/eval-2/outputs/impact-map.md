# Impact Map: TC-9002 — Improve search experience

## Ambiguities

The following ambiguities were identified in the feature description and must be clarified with the product owner before finalizing implementation:

1. **No performance baseline or target for "faster" search.** The requirement states "Search should be faster" and "Currently too slow," but provides no current response-time measurements, no target latency (e.g., p95 < 200ms), and no benchmark methodology. Without quantitative targets, there is no way to verify the requirement is met.

2. **No definition of "relevant" results.** The requirement states "Results should be more relevant" and "Users complain about irrelevant results," but provides no ranking criteria, no examples of irrelevant results, no weighting rules for different entity types, and no specification of what fields should influence relevance scoring.

3. **No specification for "Add filters."** The requirement says "Some kind of filtering capability" but does not specify which fields should be filterable (e.g., entity type, severity, date range, license), what filter operators to support (equality, range, contains), whether filters should be combinable (AND/OR), or what the API contract should look like (query parameters, request body).

4. **Non-functional requirements lack quantitative thresholds.** "Should be fast enough" has no measurable definition. "Don't break existing functionality" does not specify backward-compatibility constraints, API versioning strategy, or acceptable behavioral changes in existing endpoints.

## Repositories Impacted

### trustify-backend

| Area | Files | Change Type | Rationale |
|---|---|---|---|
| Database migration | `migration/src/` (new migration module) | Create | Add full-text search indexes on searchable columns to improve query performance |
| Search service | `modules/search/src/service/mod.rs` | Modify | Implement relevance scoring logic and integrate with database indexes |
| Search endpoint | `modules/search/src/endpoints/mod.rs` | Modify | Add filter query parameters and relevance-sorted response |
| Query helpers | `common/src/db/query.rs` | Modify | Add filter builder helpers for search filter parameters |
| Search caching | `modules/search/src/endpoints/mod.rs` | Modify | Add tower-http caching middleware to search routes |
| Integration tests | `tests/api/search.rs` | Modify | Update tests for new filter parameters, relevance ordering, and caching headers |

## Excluded Requirements

### Better UI (Non-MVP)
The "Better UI" requirement (marked non-MVP) is excluded from this plan. It cannot be planned without:
- Design mockups or wireframes specifying the desired visual changes
- A frontend repository — trustify-backend is a Rust backend service with no frontend code

This requirement should be addressed in a separate feature once design specifications are available and a frontend repository is in scope.

## Inherited Field Values

The following field values are inherited from feature TC-9002 and will be propagated to all child tasks:

| Field | Value | Propagation |
|---|---|---|
| Priority | Normal | All tasks inherit Priority: Normal |
| Fix Versions | RHTPA 1.6.0 | All tasks inherit Fix Versions: RHTPA 1.6.0 |
