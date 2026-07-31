# Impact Map: TC-9001 — Add advisory severity aggregation endpoint

## Feature Summary

Add a new REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates vulnerability advisory severity counts for a given SBOM, returning deduplicated counts by severity level (Critical, High, Medium, Low) with a total. Includes 5-minute caching and cache invalidation on advisory ingestion.

## Workflow Mode

**direct-to-main** — Single new endpoint with no atomicity constraints requiring a feature branch.

## Inherited Fields

- **Priority**: Major (propagated from TC-9001 to all tasks)
- **Fix Versions**: RHTPA 1.5.0 (propagated from TC-9001 to all tasks)

## Repository: trustify-backend

### Changes Required

1. **New model struct for advisory severity summary response**
   - Create `modules/fundamental/src/sbom/model/advisory_summary.rs` with `AdvisorySeveritySummary` struct containing fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
   - Register the new module in `modules/fundamental/src/sbom/model/mod.rs`

2. **Service method for advisory severity aggregation query**
   - Add `get_advisory_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`
   - Query `sbom_advisory` join table joined with `advisory` entity, group by severity, deduplicate by advisory ID using `SELECT DISTINCT` or equivalent SeaORM construct
   - Return 404 via `AppError` if the SBOM ID does not exist (check SBOM existence first)

3. **New endpoint handler with caching**
   - Create `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` with handler for `GET /api/v2/sbom/{id}/advisory-summary`
   - Support optional `?threshold=critical|high|medium|low` query parameter to filter counts at or above a severity level
   - Register route in `modules/fundamental/src/sbom/endpoints/mod.rs` under the existing SBOM router
   - Apply `tower-http` cache-control middleware with 5-minute TTL

4. **Cache invalidation on advisory ingestion**
   - Modify `modules/ingestor/src/graph/advisory/mod.rs` to invalidate cached advisory summary entries when new advisories are linked to SBOMs during ingestion

5. **Integration tests**
   - Create `tests/api/sbom_advisory_summary.rs` with tests covering: successful aggregation, 404 for nonexistent SBOM, deduplication of advisories, threshold query parameter filtering, cache behavior

6. **Documentation updates** (doc task)
   - Add the new endpoint to REST API reference documentation

7. **Smoke Tests** (testing task)
   - Cross-cutting smoke test validation per testing readiness template

8. **Performance Benchmarks** (testing task)
   - Cross-cutting performance benchmark validation per testing readiness template

## Task Creation Log

| Task | Summary | Repository | Priority | Fix Versions | Parent |
|------|---------|------------|----------|--------------|--------|
| Task 1 | Create advisory severity summary model | trustify-backend | Major | RHTPA 1.5.0 | TC-9001 |
| Task 2 | Implement advisory severity aggregation service method | trustify-backend | Major | RHTPA 1.5.0 | TC-9001 |
| Task 3 | Add advisory-summary endpoint with caching | trustify-backend | Major | RHTPA 1.5.0 | TC-9001 |
| Task 4 | Add cache invalidation for advisory summary on ingestion | trustify-backend | Major | RHTPA 1.5.0 | TC-9001 |
| Task 5 | Add integration tests for advisory-summary endpoint | trustify-backend | Major | RHTPA 1.5.0 | TC-9001 |
| Task 6 | Update REST API reference documentation for advisory-summary endpoint | trustify-backend | Major | RHTPA 1.5.0 | TC-9001 |
| Task 7 | Smoke Tests — advisory severity aggregation endpoint | trustify-backend | Major | RHTPA 1.5.0 | TC-9001 |
| Task 8 | Performance Benchmarks — advisory severity aggregation endpoint | trustify-backend | Major | RHTPA 1.5.0 | TC-9001 |

## Dependency Graph

```
Task 1 (model)
  └── Task 2 (service) depends on Task 1
       └── Task 3 (endpoint) depends on Task 2
            ├── Task 4 (cache invalidation) depends on Task 3
            ├── Task 5 (integration tests) depends on Task 3
            └── Task 6 (documentation) depends on Task 3
Task 7 (Smoke Tests) depends on Tasks 1, 2, 3, 4, 5
Task 8 (Performance Benchmarks) depends on Tasks 1, 2, 3, 4, 5
```
