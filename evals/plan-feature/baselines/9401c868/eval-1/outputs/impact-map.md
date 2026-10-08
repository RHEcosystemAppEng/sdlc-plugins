# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Workflow Mode

**Mode:** direct-to-main

**Rationale:** No atomicity indicators are present. The feature is an additive, single-repository change that introduces a new endpoint without modifying existing API contracts, database schemas, or cross-cutting structures. Each task PR can be merged independently to `main` without leaving the codebase in a broken state:
- No coordinated schema migrations (no new database tables)
- No breaking API changes (new endpoint only, existing endpoints unaffected)
- No cross-cutting refactors (no renames or module reorganizations)
- No tightly coupled cross-repo components (single backend repository)

## Changes

trustify-backend:
  changes:
    - Add `AdvisorySeveritySummary` response model struct with severity count fields (critical, high, medium, low, total)
    - Add `advisory_severity_summary` service method on `SbomService` that aggregates advisory severity counts from the `sbom_advisory` join table with deduplication by advisory ID
    - Add support for optional severity threshold filtering in the service method
    - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with optional `?threshold` query parameter
    - Register the new route in the SBOM endpoints module with 5-minute cache TTL via tower-http caching middleware
    - Add cache invalidation in the advisory ingestion pipeline to invalidate advisory summary cache entries when new advisories are linked to SBOMs
    - Add integration tests for the advisory summary endpoint in `tests/api/advisory_summary.rs`
    - Update REST API reference documentation with the new endpoint path, parameters, response shape, and error codes

## Excluded Requirements

No requirements were excluded. All MVP and non-MVP requirements from TC-9001 are covered:
- MVP: Endpoint returning severity counts, 404 for missing SBOM, 5-minute caching
- Non-MVP: Optional `?threshold` query parameter for severity filtering

## Task Summary

| # | Task | Type | Dependencies |
|---|---|---|---|
| 1 | Add advisory severity summary model and service method | Implementation | None |
| 2 | Add advisory severity summary endpoint with caching and threshold filter | Implementation | Task 1 |
| 3 | Add cache invalidation for advisory summaries in the ingestor | Implementation | Task 2 |
| 4 | Update REST API reference documentation | Documentation | Tasks 1, 2, 3 |
| 5 | Smoke Tests | Testing | Tasks 1, 2, 3 |
| 6 | Performance Benchmarks | Testing | Tasks 1, 2, 3 |

## Inherited Field Values

The following field values are inherited from the parent Feature (TC-9001) and will be propagated to all created tasks:

- **Priority:** Major (propagated to all tasks)
- **Fix Versions:** RHTPA 1.5.0 (propagated to all tasks; fixVersion scope defaults to "both" since no Jira Field Defaults section is configured)

### additional_fields for task creation

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
