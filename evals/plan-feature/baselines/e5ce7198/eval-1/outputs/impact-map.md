# Impact Map: TC-9001 — Add advisory severity aggregation endpoint

## Feature Summary

Add a new REST API endpoint (`GET /api/v2/sbom/{id}/advisory-summary`) that aggregates vulnerability advisory severity counts for a given SBOM, returning critical/high/medium/low/total counts in a single call. Includes 5-minute caching with invalidation on advisory ingestion, and an optional `?threshold` query parameter for severity filtering.

## Repositories Affected

### trustify-backend

**Changes:**

- **New model struct** — `AdvisorySeveritySummary` response struct in `modules/fundamental/src/sbom/model/` to represent aggregated severity counts
- **New service method** — `get_advisory_summary` on `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` to query and aggregate advisory severities from the `sbom_advisory` join table
- **New endpoint** — `GET /api/v2/sbom/{id}/advisory-summary` handler in `modules/fundamental/src/sbom/endpoints/` with route registration in `endpoints/mod.rs`
- **Cache configuration** — 5-minute cache via `tower-http` caching middleware on the new endpoint route
- **Cache invalidation** — Modify advisory ingestion in `modules/ingestor/src/graph/advisory/mod.rs` to invalidate cached summaries when new advisories are linked to an SBOM
- **Integration tests** — New test file `tests/api/sbom_advisory_summary.rs` covering the endpoint, caching, error cases, and threshold filtering

## Workflow Mode

**Direct-to-main** — This feature affects a single repository (trustify-backend) with no cross-repo dependencies or atomicity constraints. All tasks target the `main` branch directly. There is no need for a feature branch or bookend tasks since changes can be merged incrementally without coordination across repositories.
