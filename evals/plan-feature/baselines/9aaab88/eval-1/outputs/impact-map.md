# Repository Impact Map: TC-9001 — Add Advisory Severity Aggregation Endpoint

## Workflow Mode Decision

**Mode: direct-to-main**

No atomicity indicators are present. The feature adds a new read-only aggregation endpoint with no schema migrations, no breaking API changes, and no cross-cutting refactors. Each task can be merged independently without leaving the system in an inconsistent state.

## Repository: trustify-backend

### Impact Areas

#### 1. New model: Advisory severity summary response struct

- **Files to Create**:
  - `modules/fundamental/src/sbom/model/advisory_summary.rs` — New struct `AdvisorySeveritySummary` with fields `critical`, `high`, `medium`, `low`, `total` to represent aggregated severity counts
  - Modify `modules/fundamental/src/sbom/model/mod.rs` — Register the new `advisory_summary` module

#### 2. New service method: Severity aggregation query

- **Files to Modify**:
  - `modules/fundamental/src/sbom/service/sbom.rs` — Add `get_advisory_summary(sbom_id)` method that queries `sbom_advisory` join table, joins with `advisory` entity to get severity, and aggregates counts with deduplication by advisory ID
  - `entity/src/advisory.rs` — Reference existing severity field on the Advisory entity
  - `entity/src/sbom_advisory.rs` — Reference existing SBOM-Advisory join table for the aggregation query

#### 3. New endpoint: `GET /api/v2/sbom/{id}/advisory-summary`

- **Files to Create**:
  - `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Handler function for the advisory summary endpoint with optional `?threshold` query param, 5-minute cache header, and 404 for missing SBOMs
- **Files to Modify**:
  - `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route

#### 4. Cache invalidation in advisory ingestion pipeline

- **Files to Modify**:
  - `modules/ingestor/src/graph/advisory/mod.rs` — After advisory ingestion correlates advisories with SBOMs, invalidate cached advisory summaries for affected SBOMs

#### 5. Integration tests

- **Files to Create**:
  - `tests/api/sbom_advisory_summary.rs` — Integration tests covering: successful aggregation, 404 for missing SBOM, deduplication, threshold filtering, cache headers
- **Files to Modify**:
  - `tests/Cargo.toml` — Ensure the new test file is included in the test suite if needed

### Dependency Order

```
Task 1 (model) → Task 2 (service) → Task 3 (endpoint) → Task 4 (cache invalidation)
                                                       → Task 5 (integration tests)
```

Tasks 4 and 5 can run in parallel after Task 3 is complete.
