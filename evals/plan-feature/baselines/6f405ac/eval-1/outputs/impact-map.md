# Impact Map: TC-9001 — Add Advisory Severity Aggregation Endpoint

## Repository: trustify-backend

### New Files

| File | Purpose |
|---|---|
| `modules/fundamental/src/sbom/model/advisory_summary.rs` | `AdvisorySeveritySummary` response struct with fields: critical, high, medium, low, total |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | Handler for `GET /api/v2/sbom/{id}/advisory-summary` with optional `?threshold` query param and 5-minute cache |
| `tests/api/sbom_advisory_summary.rs` | Integration tests for the advisory-summary endpoint (happy path, 404, threshold filter, caching) |

### Modified Files

| File | Change |
|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod advisory_summary;` to expose the new model |
| `modules/fundamental/src/sbom/service/sbom.rs` | Add `advisory_severity_summary` method that queries `sbom_advisory` join table, groups by severity, deduplicates by advisory ID, returns `AdvisorySeveritySummary` |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register the `GET /api/v2/sbom/{id}/advisory-summary` route |
| `modules/ingestor/src/graph/advisory/mod.rs` | Add cache invalidation call after advisory-SBOM correlation so cached summaries are refreshed when new advisories are linked |
| `modules/ingestor/Cargo.toml` | Add dependency on caching infrastructure if not already present for invalidation support |

### Unchanged Files (referenced for patterns only)

| File | Reason Referenced |
|---|---|
| `common/src/error.rs` | `AppError` enum — all handlers return `Result<T, AppError>` |
| `common/src/model/paginated.rs` | `PaginatedResults<T>` — pattern reference (not used directly since this is an aggregation, not a list) |
| `common/src/db/query.rs` | Query builder helpers — referenced for filtering pattern with threshold param |
| `entity/src/sbom_advisory.rs` | SBOM-Advisory join entity — used in the aggregation query |
| `entity/src/advisory.rs` | Advisory entity — severity field used for grouping |
| `modules/fundamental/src/sbom/endpoints/get.rs` | Existing SBOM endpoint — pattern reference for handler structure and 404 handling |
| `modules/fundamental/src/advisory/model/summary.rs` | `AdvisorySummary` — severity field reference |
| `server/src/main.rs` | Route mounting — no change needed since SBOM module's `endpoints/mod.rs` handles sub-route registration |
| `tests/api/sbom.rs` | Existing SBOM integration tests — pattern reference for test structure |
