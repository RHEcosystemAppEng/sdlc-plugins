# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Workflow Mode

**Mode**: `direct-to-main`

**Rationale**: No atomicity indicators are present. Each task produces a self-contained change that does not break `main` when merged independently:
- The model and service layer (Task 1) can land without the endpoint — unused code is harmless.
- The endpoint (Task 2) depends on Task 1 but both can merge sequentially without a feature branch.
- Cache invalidation (Task 3) extends existing ingestion logic and is safe to merge independently.
- Integration tests (Task 4) exercise the endpoint and can merge after the endpoint lands.
- No coordinated schema migrations, no breaking API changes, no cross-cutting refactors, no tightly coupled frontend/backend components.

## Inherited Field Values

The following field values are inherited from the parent Feature issue TC-9001 and propagated to all created tasks:

- **Priority**: Major (inherited from Feature; not "Undefined", so it is propagated)
- **fixVersions**: RHTPA 1.5.0 (inherited from Feature; `fixVersion scope` defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md, so fixVersions are propagated to tasks)

## Impact Map

trustify-backend:
  changes:
    - Create AdvisorySeveritySummary response model struct with fields: critical, high, medium, low, total
    - Add advisory_summary() aggregation method to SbomService that queries sbom_advisory join table, groups by severity, and deduplicates by advisory ID
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler with 5-minute cache via tower-http middleware
    - Register the advisory-summary route in the sbom endpoints module and mount in server
    - Support optional ?threshold query parameter for severity filtering
    - Add cache invalidation in the advisory ingestion pipeline to clear cached advisory-summary entries when new advisories are linked to an SBOM
    - Add integration tests covering: valid SBOM response, 404 for missing SBOM, threshold filtering, advisory deduplication, cache behavior
    - Update REST API reference documentation to include the new endpoint

## Excluded Requirements

None. All requirements (MVP and non-MVP) from the Feature description can be decomposed into actionable tasks within the trustify-backend repository.

## Task Summary

| Task | Summary | Type | Dependencies |
|---|---|---|---|
| 1 | Create AdvisorySeveritySummary model and aggregation service | Implementation | None |
| 2 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | Implementation | Task 1 |
| 3 | Add cache invalidation on advisory ingestion | Implementation | Task 2 |
| 4 | Add integration tests for advisory-summary endpoint | Implementation | Task 2 |
| 5 | Update REST API reference documentation | Documentation | Tasks 1-4 |
| 6 | Smoke Tests | Testing | Tasks 1-4 |
| 7 | Performance Benchmarks | Testing | Tasks 1-4 |
