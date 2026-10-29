# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct for severity count response
    - Add advisory_summary aggregation method to SbomService using sbom_advisory join table
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and optional threshold filter
    - Add cache invalidation in advisory ingestion pipeline when new advisories are linked to an SBOM
    - Add integration tests for the new endpoint in tests/api/
    - Update REST API reference documentation for the new endpoint
```

## Excluded Requirements

None — all MVP and non-MVP requirements from the Feature description are plannable within the trustify-backend repository.

Note: "Customer Information/Supportability" items (Grafana dashboard, p95 alerting) are operational considerations, not code changes in this repository. They are covered by the Performance Benchmarks testing task which validates the p95 < 200ms requirement.

## Workflow Mode Decision

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **Coordinated schema migrations** — No. The feature uses existing advisory-SBOM relationship tables; no new database tables or migrations are required.
2. **Breaking API changes** — No. The feature adds a new endpoint; no existing endpoints are modified.
3. **Cross-cutting refactors** — No. Changes are additive (new model, new service method, new endpoint, ingestion hook).
4. **Tightly coupled feature components** — No. All changes are within a single backend repository. Each task's PR can be merged independently without breaking main.

All tasks use Target Branch: `main`.

## Task Creation — additional_fields

The following fields are propagated from the parent Feature (TC-9001) to every created task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **Priority**: "Major" — inherited from Feature TC-9001 (not "Undefined", so propagated)
- **fixVersions**: ["RHTPA 1.5.0"] — inherited from Feature TC-9001 (non-empty array, and `fixVersion scope` is "both" per Jira Field Defaults in CLAUDE.md, so propagated to tasks)
- **Labels**: ["ai-generated-jira"] — always included per plan-feature rules

## Task Summary

| # | Task | Type | Dependencies |
|---|---|---|---|
| 1 | Add advisory severity summary model and service method | Implementation | None |
| 2 | Add advisory-summary REST endpoint with caching | Implementation | Task 1 |
| 3 | Add cache invalidation for advisory severity summaries | Implementation | Task 1 |
| 4 | Update REST API documentation for advisory-summary endpoint | Documentation | Tasks 1, 2, 3 |
| 5 | Smoke Tests — advisory severity aggregation | Testing | Tasks 1, 2, 3 |
| 6 | Performance Benchmarks — advisory severity aggregation | Testing | Tasks 1, 2, 3 |
