# Repository Impact Map

**Feature:** TC-9001 — Add advisory severity aggregation endpoint

## trustify-backend

changes:
  - Add `AdvisorySeveritySummary` response model struct in `modules/fundamental/src/sbom/model/`
  - Add severity aggregation service method in `modules/fundamental/src/sbom/service/sbom.rs` that queries `sbom_advisory` joined with `advisory`, groups by severity, deduplicates by advisory ID, and returns counts
  - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in `modules/fundamental/src/sbom/endpoints/` with 404 handling for non-existent SBOMs
  - Register the advisory-summary route in `modules/fundamental/src/sbom/endpoints/mod.rs`
  - Add 5-minute response cache using tower-http caching middleware on the endpoint route builder
  - Add cache invalidation in advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to invalidate cached advisory summaries when new advisories are linked to an SBOM
  - Add optional `?threshold=critical` query parameter to filter severity counts above a given severity level (non-MVP)
  - Add integration tests in `tests/api/` for the advisory-summary endpoint covering basic aggregation, 404, deduplication, caching, and threshold filtering

## Excluded requirements

None. All requirements from the feature description can be planned with the available repository structure.

---

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
1. No coordinated schema migrations — the feature uses existing tables (`sbom_advisory`, `advisory`) with no new migrations.
2. No breaking API changes — this is a new endpoint addition, not a modification of existing API contracts.
3. No cross-cutting refactors — changes are confined to the sbom module, ingestor module, and test directory within a single repository.
4. No tightly coupled cross-repo components — all changes are within `trustify-backend`.

All tasks can be merged to `main` independently without leaving the codebase in a broken state.

---

## Field Inheritance

The following fields are inherited from the parent Feature (TC-9001) and will be propagated to all created tasks:

| Field | Feature Value | Propagation |
|---|---|---|
| **priority** | Major | Propagated to all tasks — Feature priority is set and is not "Undefined" |
| **fixVersions** | RHTPA 1.5.0 | Propagated to all tasks — Feature has fixVersions set, and no `fixVersion scope` setting exists in Jira Configuration (defaults to "both") |

### additional_fields for created issues

Every created task will include:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
