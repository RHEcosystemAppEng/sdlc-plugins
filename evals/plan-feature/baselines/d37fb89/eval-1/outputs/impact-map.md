# Repository Impact Map

**Feature**: TC-9001 — Add advisory severity aggregation endpoint

## Repositories Affected

### trustify-backend

**Role**: Primary backend service — all changes are within this repository.

**Changes needed**:

1. **New response model** — `AdvisorySeveritySummary` struct in the SBOM model layer to represent the `{ critical, high, medium, low, total }` response shape.
2. **New service method** — `SbomService::advisory_severity_summary()` that queries the `sbom_advisory` join table, joins to the advisory entity for severity, deduplicates by advisory ID, and aggregates counts by severity level.
3. **New endpoint** — `GET /api/v2/sbom/{id}/advisory-summary` handler with optional `?threshold` query parameter, registered in the SBOM endpoint module.
4. **Caching** — 5-minute cache layer on the new endpoint using `tower-http` caching middleware, consistent with existing caching patterns.
5. **Cache invalidation** — Advisory ingestion pipeline updated to invalidate cached severity summaries when new advisories are linked to an SBOM.
6. **Integration tests** — Tests covering the happy path, 404 for missing SBOM, severity counting correctness, deduplication, threshold filtering, and cache behavior.

**Key entity/module touchpoints**:
- `entity/src/sbom_advisory.rs` — existing join table used for aggregation queries
- `entity/src/advisory.rs` — severity field used for grouping
- `modules/fundamental/src/sbom/` — model, service, endpoints additions
- `modules/ingestor/src/graph/advisory/mod.rs` — cache invalidation hook
- `tests/api/` — new integration test file

## Workflow Mode Decision

**Mode**: direct-to-main

**Rationale**: This feature is confined to a single repository (trustify-backend). All tasks target the same codebase and can be merged independently in sequence. There is no cross-repository coordination required. The changes are additive (new endpoint, new model, new service method) with minimal risk of destabilizing existing functionality. Each task produces a self-contained, reviewable PR that can land on `main` without requiring a feature branch to coordinate multi-repo merges. The atomicity indicators (single repo, additive changes, no breaking API modifications) all favor direct-to-main workflow.
