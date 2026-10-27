# Plan Summary — TC-9001: Add advisory severity aggregation endpoint

## Tasks Created

| # | Summary | Repository | Type |
|---|---|---|---|
| 1 | Advisory severity summary model | trustify-backend | Implementation |
| 2 | Advisory summary service | trustify-backend | Implementation |
| 3 | Advisory summary endpoint | trustify-backend | Implementation |
| 4 | Cache invalidation | trustify-backend | Implementation |
| 5 | Integration tests | trustify-backend | Implementation |
| 6 | Threshold query param | trustify-backend | Implementation |
| 7 | Documentation | trustify-backend | Documentation |
| 8 | Smoke tests | trustify-backend | Testing |
| 9 | Performance benchmarks | trustify-backend | Testing |

## Repositories Affected

- **trustify-backend** — all 9 tasks target this repository

## Architecture Summary

The implementation adds a new advisory severity aggregation endpoint to the existing SBOM module following the established `model/ + service/ + endpoints/` pattern:

1. **Model layer**: New `AdvisorySeveritySummary` struct for the response
2. **Service layer**: Aggregation query in `SbomService` using the `sbom_advisory` join table and advisory severity data
3. **Endpoint layer**: New `GET /api/v2/sbom/{id}/advisory-summary` route with 5-minute cache TTL
4. **Ingestion integration**: Cache invalidation hook in the advisory ingestion pipeline
5. **Non-MVP extension**: Optional `?threshold` query parameter for severity filtering

## Inherited Field Propagation

### Priority
- **Feature priority**: Major
- **Propagated to tasks**: Yes — all 9 tasks inherit `priority: Major`
- **Rationale**: Feature has priority set (not "Undefined"), so it is inherited by all created tasks per plan-feature Step 6a

### Fix Versions
- **Feature fixVersions**: RHTPA 1.5.0
- **Propagated to tasks**: Yes — all 9 tasks inherit `fixVersions: ["RHTPA 1.5.0"]`
- **Rationale**: Feature has non-empty fixVersions array; `fixVersion scope` defaults to "both" (no `### Jira Field Defaults` section configured in CLAUDE.md), so fixVersions are propagated to tasks

### Task Creation Fields
All tasks created with:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Workflow Mode

**Mode**: `direct-to-main`

No atomicity indicators were identified — the feature is a new additive endpoint in a single repository with no breaking API changes, coordinated migrations, or cross-cutting refactors.
