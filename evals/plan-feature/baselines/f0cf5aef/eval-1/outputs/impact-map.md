# Repository Impact Map — TC-9001

## trustify-backend

changes:
  - Add `AdvisorySeveritySummary` response model struct with fields: critical, high, medium, low, total
  - Add severity aggregation service method to query the `sbom_advisory` join table, deduplicate by advisory ID, and group counts by severity level
  - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler returning the severity summary
  - Register the new endpoint route in the SBOM module's route configuration (`endpoints/mod.rs`)
  - Add 5-minute cache configuration for the advisory-summary endpoint using tower-http caching middleware
  - Add cache invalidation in the advisory ingestion pipeline to clear cached summaries when new advisories are linked to an SBOM
  - Add integration tests for the advisory-summary endpoint covering success, 404 (missing SBOM), deduplication, and empty advisory scenarios
  - Add optional `?threshold` query parameter to filter severity counts above a given level (non-MVP)

## Excluded requirements

None. All requirements (MVP and non-MVP) can be planned against the trustify-backend repository using existing database tables and infrastructure.

---

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **Coordinated schema migrations** — not present. The feature explicitly requires no new database tables; it uses existing `sbom_advisory` and `advisory` relationship tables.
2. **Breaking API changes** — not present. This adds a new endpoint (`/advisory-summary`) without modifying any existing endpoint contracts.
3. **Cross-cutting refactors** — not present. Changes are localized to the SBOM module and advisory ingestion pipeline.
4. **Tightly coupled feature components** — not present. This is a single-repository backend change with no frontend dependency for initial delivery.

All tasks target `main` as their branch.

---

## Epic Grouping (by-sub-feature)

Assuming a level-1 Epic type is available in the Jira project (to be confirmed via `get_project_issue_types`):

| Epic | Summary | Tasks |
|---|---|---|
| Epic 1 | TC-9001: Severity aggregation endpoint | Task 1, Task 2, Task 3 |
| Epic 2 | TC-9001: Threshold filtering | Task 5 |
| Epic 3 | TC-9001: Quality assurance and documentation | Task 4, Task 6, Task 7, Task 8 |

---

## Jira Field Inheritance

The following fields from the Feature issue will be propagated to all created Epics and Tasks via `additional_fields`:

- **Priority:** Major (inherited from TC-9001)
- **Fix Versions:** RHTPA 1.5.0 (inherited from TC-9001; no `fixVersion scope` setting found in Jira Configuration, defaulting to `"both"` — propagate to tasks)
- **Labels:** `["ai-generated-jira"]` (required on all AI-generated issues)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

---

## Documentation Signals

- **Doc impact type:** Updates
- **Details:** Add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint to the REST API reference. User purpose: API consumers need to know the endpoint path, parameters, and response shape.
- **Action:** Generate a documentation task (Task 6).

## Testing Readiness

A testing readiness template was found at `docs/testing-readiness.md` with two categories:
- Smoke Tests
- Performance Benchmarks

**Action:** Generate one testing task per category (Tasks 7, 8).
