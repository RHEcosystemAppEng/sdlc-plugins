# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified. All changes are within a single repository (trustify-backend). Each task adds new code (model, service method, endpoint, tests) that can be merged independently without leaving `main` in a broken state. There are no coordinated schema migrations, no breaking API changes between tasks, no cross-cutting refactors, and no tightly coupled cross-repo components.

## Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct with severity count fields (critical, high, medium, low, total)
    - Add advisory severity aggregation query method to SbomService that counts unique advisories by severity from the sbom_advisory join table
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute tower-http cache and optional ?threshold query parameter
    - Add cache invalidation in the advisory ingestion pipeline (modules/ingestor/src/graph/advisory/mod.rs) to invalidate advisory-summary cache when new advisories are linked to an SBOM
    - Add integration tests in tests/api/advisory_summary.rs covering severity counting, deduplication, 404 handling, and threshold filtering
    - Update REST API documentation with the new advisory-summary endpoint specification
```

## Inherited Field Values

- **Priority:** Major (inherited from feature TC-9001; propagated to all created tasks)
- **fixVersions:** RHTPA 1.5.0 (inherited from feature TC-9001; propagated to all created tasks — no `fixVersion scope` restriction in Jira Field Defaults, defaulting to "both")

## additional_fields for Task Creation

All tasks are created with the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Task Summary

| # | Task | Repository | Dependencies |
|---|---|---|---|
| 1 | Add advisory severity summary response model | trustify-backend | None |
| 2 | Add advisory severity aggregation service method | trustify-backend | Task 1 |
| 3 | Add advisory-summary REST endpoint with caching | trustify-backend | Task 2 |
| 4 | Add cache invalidation for advisory ingestion | trustify-backend | Task 3 |
| 5 | Add integration tests for advisory-summary endpoint | trustify-backend | Task 3 |
| 6 | Update REST API documentation for advisory-summary endpoint | trustify-backend | Tasks 1-5 |
| 7 | Smoke Tests — advisory severity aggregation | trustify-backend | Tasks 1-5 |
| 8 | Performance Benchmarks — advisory severity aggregation | trustify-backend | Tasks 1-5 |

## Excluded Requirements

No requirements were excluded. All MVP and non-MVP requirements from the feature description are covered by the tasks above:
- MVP: severity count endpoint, 404 handling, 5-minute caching
- Non-MVP: threshold query parameter (included in Task 3)
