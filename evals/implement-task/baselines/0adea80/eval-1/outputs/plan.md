# Implementation Plan: TC-9201 — Add advisory severity aggregation service and endpoint

## Summary

Add a `GET /api/v2/sbom/{id}/advisory-summary` endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns `{ critical, high, medium, low, total }` counts, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Files to Create

| # | File | Purpose |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct with Serialize/Deserialize |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File | Change |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |
| 5 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 6 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new route for the severity summary handler |

## Files NOT Modified

- `server/src/main.rs` — no changes needed; routes auto-mount via module registration in each module's `endpoints/mod.rs`.

## Implementation Order

1. Create the `SeveritySummary` response model (file 1)
2. Register the model module (file 4)
3. Add the `severity_summary` service method (file 5)
4. Create the endpoint handler (file 2)
5. Register the route (file 6)
6. Add integration tests (file 3)

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories (TC-9201)

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, endpoint handler, and integration tests.
```
