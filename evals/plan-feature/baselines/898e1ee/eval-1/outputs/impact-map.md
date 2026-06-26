# Repository Impact Map — TC-9001

## Feature

**TC-9001**: Add advisory severity aggregation endpoint

A new read-only REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts (critical, high, medium, low, total) for a given SBOM, eliminating client-side counting and reducing dashboard load time from ~2s to <200ms.

## Workflow Mode

**direct-to-main** — This is a new read-only endpoint with no atomicity constraints across repositories. All tasks target `main` directly.

## Repository: trustify-backend

### Files to Create

| File | Purpose | Task |
|---|---|---|
| `modules/fundamental/src/sbom/model/advisory_summary.rs` | `AdvisorySeveritySummary` response struct with fields: critical, high, medium, low, total | Task 1 |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | Axum handler for `GET /api/v2/sbom/{id}/advisory-summary` with optional `?threshold` query param | Task 3 |
| `tests/api/sbom_advisory_summary.rs` | Integration tests for the advisory summary endpoint | Task 5 |

### Files to Modify

| File | Change | Task |
|---|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod advisory_summary;` to expose the new model | Task 1 |
| `modules/fundamental/src/sbom/service/sbom.rs` | Add `get_advisory_severity_summary(&self, sbom_id, threshold)` method that queries `sbom_advisory` join table, joins to `advisory` entity, groups by severity, and returns `AdvisorySeveritySummary` | Task 2 |
| `modules/fundamental/src/sbom/service/mod.rs` | Re-export the summary method if needed by service module structure | Task 2 |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register the `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache layer | Task 3 |
| `server/src/main.rs` | No change needed — SBOM routes are already mounted; new route is registered within existing SBOM endpoint module | — |
| `modules/ingestor/src/graph/advisory/mod.rs` | After advisory-SBOM correlation, invalidate cached advisory summaries for affected SBOM IDs | Task 4 |
| `tests/api/sbom.rs` | Import shared test helpers if advisory summary tests reference SBOM test fixtures | Task 5 |

### Entity Layer (No Changes)

The feature uses existing entities without modification:
- `entity/src/sbom.rs` — SBOM entity (read existing records)
- `entity/src/advisory.rs` — Advisory entity (read severity field)
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table (query for aggregation)

### Dependency Graph

```
Task 1 (Model) ─── no dependencies
Task 2 (Service) ── depends on Task 1
Task 3 (Endpoint) ─ depends on Task 2
Task 4 (Cache) ──── depends on Task 3
Task 5 (Tests) ──── depends on Task 3
Task 6 (Threshold) ─ depends on Task 3
```

## Risk Assessment

- **Low risk**: Read-only endpoint, no schema changes, uses existing join table
- **Performance consideration**: Aggregation query on `sbom_advisory` joined with `advisory` must be indexed; existing FK indexes on `sbom_advisory` should suffice
- **Cache coherence**: Cache invalidation in the advisory ingestion path is the primary correctness concern; must ensure all ingestion code paths that link advisories to SBOMs trigger invalidation
