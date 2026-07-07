# Repository Impact Map

## Feature: TC-9001 "Add advisory severity aggregation endpoint"

### Repository: trustify-backend

#### Changes

1. **New model: AdvisorySeveritySummary struct**
   - `modules/fundamental/src/advisory/model/` — new `AdvisorySeveritySummary` struct with fields: `critical`, `high`, `medium`, `low`, `total` (all integer counts)
   - References existing `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` which already has a `severity` field

2. **New service method: aggregate severity counts from sbom_advisory join**
   - `modules/fundamental/src/advisory/service/advisory.rs` — new method on `AdvisoryService` to query `sbom_advisory` join table, deduplicate by advisory ID, and aggregate severity counts
   - Leverages existing `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` for SBOM existence checks
   - Uses `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) and `entity/src/advisory.rs` (Advisory entity)

3. **New endpoint: GET /api/v2/sbom/{id}/advisory-summary**
   - `modules/fundamental/src/sbom/endpoints/mod.rs` — register new route under `/api/v2/sbom`
   - Returns `{ critical: N, high: N, medium: N, low: N, total: N }`
   - Returns 404 if SBOM ID does not exist
   - Uses `common/src/error.rs` `AppError` for error handling

4. **Caching: 5-minute cache with invalidation on advisory ingestion**
   - In-memory cache layer for advisory summary responses with 5-minute TTL
   - `modules/ingestor/src/graph/advisory/mod.rs` — hook into advisory ingestion to invalidate cached summaries when new advisories are linked to an SBOM

5. **Optional: threshold query parameter (non-MVP)**
   - `?threshold=critical` query param to filter the summary response to only count advisories at or above the specified severity level
   - Non-MVP scope — implemented after core endpoint is functional

6. **Tests: integration tests for the new endpoint**
   - `tests/api/sbom.rs` — integration tests covering the new endpoint (success, 404, deduplication, caching behavior)
   - Follows existing test patterns in `tests/api/advisory.rs`

#### Unchanged

- No new database tables required
- No changes to `common/src/model/paginated.rs` (endpoint returns a summary object, not paginated results)
- No changes to existing advisory or SBOM endpoints
