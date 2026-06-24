# Repository Impact Map — TC-9001: Add Advisory Severity Aggregation Endpoint

## Repository: trustify-backend

### Summary

Add a new `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated severity counts (critical, high, medium, low, total) for advisories linked to a given SBOM. Includes 5-minute response caching, optional `?threshold` query parameter for severity filtering, cache invalidation on advisory ingestion, and integration tests.

### Concrete Changes

#### 1. New model: Advisory severity summary response struct
- **Create** `modules/fundamental/src/sbom/model/advisory_summary.rs` — Define `AdvisorySeveritySummary` struct with fields `critical`, `high`, `medium`, `low`, `total` (all `u64`), deriving `Serialize`, `Deserialize`, `ToSchema` (for OpenAPI). Also define `SeverityThreshold` enum for the optional query parameter.

#### 2. Register model module
- **Modify** `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export the new types.

#### 3. New service method: severity aggregation query
- **Modify** `modules/fundamental/src/sbom/service/sbom.rs` — Add `advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`. This method queries the `sbom_advisory` join table joined with `advisory` to count advisories grouped by severity, deduplicating by advisory ID.

#### 4. New endpoint handler: advisory-summary
- **Create** `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Implement the `GET /api/v2/sbom/{id}/advisory-summary` Axum handler. Accept path parameter `id` and optional query parameter `threshold`. Return `Json<AdvisorySeveritySummary>`. Return 404 if SBOM not found. Apply 5-minute cache header via `tower-http` cache-control.

#### 5. Register the new route
- **Modify** `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod advisory_summary;` and register the new route in the router (`.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))`).

#### 6. Cache invalidation on advisory ingestion
- **Modify** `modules/ingestor/src/graph/advisory/mod.rs` — After advisory-SBOM correlation completes, invalidate the cached advisory summary for the affected SBOM ID(s). Use the existing cache infrastructure's invalidation mechanism.

#### 7. Integration tests
- **Create** `tests/api/sbom_advisory_summary.rs` — Integration tests covering: valid SBOM returns correct counts, non-existent SBOM returns 404, threshold filtering returns only counts at or above the specified severity, deduplication of advisories by ID.
- **Modify** `tests/Cargo.toml` — Ensure the new test file is included in the test build (if necessary, though Rust auto-discovers test files).
