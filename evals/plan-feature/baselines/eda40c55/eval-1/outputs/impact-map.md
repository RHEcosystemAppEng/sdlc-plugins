# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Workflow Mode

**Mode:** direct-to-main

**Rationale:** No atomicity indicators were identified. All tasks can be merged to main independently without leaving the codebase in a broken state:
- Task 1 (model + service) adds new code with no consumers until Task 2 is merged — unused code does not break main.
- Task 2 (endpoint) adds a new route — existing endpoints are unaffected.
- Task 3 (cache invalidation) modifies the ingestion pipeline to invalidate a cache that may or may not exist yet — a no-op if the cache entry is absent.
- Task 4 (integration tests) adds new test files — no impact on production code.
- No coordinated schema migrations, no breaking API changes, no cross-cutting refactors, no tightly coupled cross-repo components.

## Impact Map

```
trustify-backend:
  changes:
    - Add SeveritySummary model struct in modules/fundamental/src/sbom/model/ with fields: critical, high, medium, low, total
    - Add get_advisory_summary service method to SbomService in modules/fundamental/src/sbom/service/sbom.rs that aggregates severity counts from sbom_advisory + advisory entities, deduplicating by advisory ID
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler in modules/fundamental/src/sbom/endpoints/ with 5-minute tower-http cache and optional ?threshold query parameter
    - Register the new advisory-summary route in modules/fundamental/src/sbom/endpoints/mod.rs
    - Add cache invalidation in modules/ingestor/src/graph/advisory/mod.rs to clear advisory-summary cache entries when new advisories are linked to SBOMs
    - Add integration tests in tests/api/advisory_summary.rs covering happy path, 404, threshold filter, deduplication, and cache invalidation
    - Update REST API reference documentation with the new endpoint path, parameters, response shape, and caching behavior
```

## Field Inheritance

- **Priority:** Major (inherited from TC-9001, propagated to all created tasks via `additional_fields`)
- **Fix Versions:** RHTPA 1.5.0 (inherited from TC-9001, propagated to all created tasks via `additional_fields`; fixVersion scope defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md)

## Task Summary

| # | Task | Type | Dependencies |
|---|---|---|---|
| 1 | Add advisory severity summary model and service method | Implementation | None |
| 2 | Add advisory-summary endpoint with caching | Implementation | Task 1 |
| 3 | Add cache invalidation for advisory ingestion | Implementation | Task 2 |
| 4 | Add integration tests for advisory-summary endpoint | Implementation | Tasks 1, 2, 3 |
| 5 | Documentation: Update REST API reference | Documentation | Tasks 1, 2, 3, 4 |
| 6 | Smoke Tests | Testing | Tasks 1, 2, 3, 4 |
| 7 | Performance Benchmarks | Testing | Tasks 1, 2, 3, 4 |

## DAG

```
Task 1 (model + service)
  └─> Task 2 (endpoint + caching)
        └─> Task 3 (cache invalidation)
              └─> Task 4 (integration tests)
                    ├─> Task 5 (documentation)
                    ├─> Task 6 (smoke tests)
                    └─> Task 7 (performance benchmarks)
```

All dependencies flow forward — no circular dependencies.

## CONVENTIONS.md

CONVENTIONS.md was found in the trustify-backend repository root. Conventions were applied to implementation tasks where file-type applicability matched:
- §Module Pattern — applied to Task 1 (creates .rs model file in module directory)
- §Error Handling — applied to Tasks 1, 2, 3 (all modify/create .rs handler/service files)
- §Query Helpers — applied to Task 1 (modifies service file that performs queries)
- §Endpoint Registration — applied to Task 2 (modifies endpoints/mod.rs)
- §Caching — applied to Task 2 (creates endpoint with cache configuration)
- §Testing — applied to Task 4 (creates integration test .rs file)

## Excluded Requirements

None. All requirements from TC-9001 (both MVP and non-MVP) have been decomposed into tasks:
- MVP: advisory-summary endpoint, 404 handling, 5-minute cache — Tasks 1, 2, 3
- Non-MVP: optional ?threshold query parameter — included in Tasks 1 and 2

## additional_fields for Task Creation

Each task would be created with the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
