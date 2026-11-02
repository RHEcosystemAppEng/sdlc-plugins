# Repository Impact Map — TC-9001

## Workflow Mode

**Selected mode:** `direct-to-main`
**Rationale:** No atomicity indicators identified. Each task can be merged independently without leaving main in a broken state. The model and service can exist before the endpoint is registered, and cache invalidation is additive.

## trustify-backend

### Changes

- Add `AdvisorySeveritySummary` response model struct with fields: `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- Add `advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table, joins to the `advisory` table, deduplicates by advisory ID, and groups counts by severity
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls `SbomService::advisory_summary` and returns the summary model
- Register the new endpoint route in the SBOM `endpoints/mod.rs` with 5-minute `tower-http` cache configuration
- Add cache invalidation hook in the advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to invalidate cached summaries when new advisories are linked to an SBOM
- Support optional `?threshold=critical` query parameter on the advisory-summary endpoint to filter counts above a severity level
- Add integration tests for the new endpoint covering: successful aggregation, 404 for missing SBOM, deduplication of advisories, cache behavior, and threshold filtering
- Update REST API reference documentation to include the new endpoint

## Inherited Field Propagation

- **Priority:** `Major` (ID: 10002) — inherited from TC-9001, propagated to all created tasks via `additional_fields.priority`
- **fixVersions:** `RHTPA 1.5.0` (ID: 62648) — inherited from TC-9001, propagated to all created tasks via `additional_fields.fixVersions`. fixVersion scope is `both` (default), so task-level propagation applies.

## Task Creation Log

| Task | Summary | Repository | Epic | Priority | fixVersions | Labels |
|------|---------|------------|------|----------|-------------|--------|
| 1 | Advisory severity summary model | trustify-backend | — | Major | RHTPA 1.5.0 | ai-generated-jira |
| 2 | Advisory summary aggregation service | trustify-backend | — | Major | RHTPA 1.5.0 | ai-generated-jira |
| 3 | Advisory summary endpoint with caching | trustify-backend | — | Major | RHTPA 1.5.0 | ai-generated-jira |
| 4 | Cache invalidation on advisory ingestion | trustify-backend | — | Major | RHTPA 1.5.0 | ai-generated-jira |
| 5 | Threshold query parameter filter | trustify-backend | — | Major | RHTPA 1.5.0 | ai-generated-jira |
| 6 | Integration tests for advisory summary | trustify-backend | — | Major | RHTPA 1.5.0 | ai-generated-jira |
| 7 | Documentation — REST API reference | trustify-backend | — | Major | RHTPA 1.5.0 | ai-generated-jira |
| 8 | Smoke Tests | trustify-backend | — | Major | RHTPA 1.5.0 | ai-generated-jira |
| 9 | Performance Benchmarks | trustify-backend | — | Major | RHTPA 1.5.0 | ai-generated-jira |
