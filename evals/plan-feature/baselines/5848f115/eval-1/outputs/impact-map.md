# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## trustify-backend

### changes:
- Add `AdvisorySeveritySummary` response model struct with fields: critical, high, medium, low, total
- Add severity aggregation query method to `SbomService` that counts unique advisories by severity using the `sbom_advisory` join table
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute `tower-http` cache
- Return 404 when SBOM ID does not exist (consistent with existing SBOM endpoints)
- Add cache invalidation call in advisory ingestion pipeline when new advisories are linked to an SBOM
- Add optional `?threshold=critical` query parameter to filter severity counts (non-MVP)
- Add integration tests for the advisory-summary endpoint covering all scenarios
- Update REST API reference documentation with the new endpoint

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
1. No coordinated schema migrations — the feature explicitly requires no new database tables; it uses existing `sbom_advisory` relationship tables
2. No breaking API changes — this is a new endpoint (`/advisory-summary`), not a modification to existing endpoints
3. No cross-cutting refactors — all changes add new code within the existing module structure
4. No tightly coupled feature components — this is a backend-only feature; the frontend is a separate consumer and is not part of this change set

Each task can be merged to `main` independently without leaving the codebase in a broken state.

## Excluded Requirements

None. All requirements (MVP and non-MVP) from the Feature description can be decomposed into actionable tasks using the trustify-backend repository.

## Jira Field Propagation

The following fields will be propagated from Feature TC-9001 to all created tasks:

| Field | Value | Propagation |
|---|---|---|
| `priority` | Major | Propagated — Feature has a non-"Undefined" priority |
| `fixVersions` | RHTPA 1.5.0 | Propagated — Feature has fixVersions set; no `fixVersion scope` configured in Jira Field Defaults (defaults to "both") |
| `labels` | ai-generated-jira | Set on all created issues (required by skill) |

### additional_fields for created issues

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
