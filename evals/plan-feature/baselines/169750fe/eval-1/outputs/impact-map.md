# Repository Impact Map — TC-9001

## Workflow Mode Decision

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified:
- No coordinated schema migrations — no new database tables required; uses existing advisory-SBOM relationship tables
- No breaking API changes — this is a new endpoint, not a modification to existing ones
- No cross-cutting refactors — changes are additive within the sbom module
- No tightly coupled components — single backend repository, no frontend dependency

All tasks target `main` directly.

---

## trustify-backend

### Changes

- Create `AdvisorySeveritySummary` response model struct with fields: `critical`, `high`, `medium`, `low`, `total`
- Add aggregation method to `SbomService` that queries `sbom_advisory` join table, joins with `advisory` entity to access severity, groups and counts by severity level, deduplicates by advisory ID
- Create `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in the sbom endpoints module with 5-minute cache TTL via tower-http caching middleware
- Update advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to invalidate cached advisory summaries when new advisories are linked to an SBOM
- Add integration tests in `tests/api/` covering: successful aggregation, 404 for nonexistent SBOM, cache behavior
- Add optional `?threshold=critical` query parameter to filter severity counts above a given threshold (Non-MVP)

---

## Inherited Field Propagation

| Field | Feature Value | Propagated to Tasks | Rationale |
|---|---|---|---|
| Priority | Major | Yes | Feature has priority set (not "Undefined") — inherited by all created tasks |
| fixVersions | RHTPA 1.5.0 | Yes | Feature has non-empty fixVersions; fixVersion scope defaults to "both" (no Jira Field Defaults configured) |

---

## Excluded Requirements

_None — all requirements (MVP and non-MVP) can be planned with the available repository and specification._

---

## Documentation Signals

- **Doc Impact Type**: Updates
- **Details**: Add endpoint to REST API reference — API consumers need to know the endpoint path, parameters, and response shape
- **Action**: Generate documentation task

---

## Testing Readiness

- **Template found**: `docs/testing-readiness.md`
- **Categories**: Smoke Tests, Performance Benchmarks
- **Action**: Generate 2 testing tasks, one per category

---

## Task Summary

| # | Task | Repository | Type |
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

### Task Creation Fields

All tasks will be created with:
```
additional_fields: {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
