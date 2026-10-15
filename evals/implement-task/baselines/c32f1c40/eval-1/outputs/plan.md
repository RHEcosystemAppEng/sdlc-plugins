# Implementation Plan: TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns
severity counts (Critical, High, Medium, Low, total) for a given SBOM, enabling
dashboard widgets to render severity breakdowns without client-side counting.

## Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Files to Create

| # | File | Purpose |
|---|------|---------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct with severity count fields |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File | Change |
|---|------|--------|
| 4 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |
| 5 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 6 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route |

## Files Not Modified

- `server/src/main.rs` — no changes needed (routes auto-mount via module registration, as confirmed by task description)

## API Changes

- **NEW**: `GET /api/v2/sbom/{id}/advisory-summary`
  - Response: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
  - 404 when SBOM ID does not exist
  - Deduplicates by advisory ID
  - All severity levels default to 0

## Data-Flow Trace

1. **Input**: HTTP GET request with SBOM ID path parameter
2. **Extraction**: Axum `Path<Id>` extractor parses the SBOM ID
3. **Service call**: Handler calls `AdvisoryService::severity_summary(sbom_id, tx)`
4. **Query**: Service queries `sbom_advisory` join table to find advisories linked to the SBOM
5. **Aggregation**: Service loads `AdvisorySummary` records, deduplicates by advisory ID, counts by `severity` field
6. **Response construction**: Counts assembled into `SeveritySummary` struct
7. **Output**: Axum serializes `SeveritySummary` via `Json` and returns HTTP 200

All stages connected; no incomplete paths.

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Enables dashboard widgets to render severity breakdowns without
client-side counting.

Implements TC-9201
```

## Verification Steps

1. Run `cargo test -p trustify-fundamental` to verify module compiles and unit tests pass
2. Run integration tests in `tests/api/advisory_summary.rs`
3. Verify `cargo fmt --check` and `cargo clippy` pass
4. Confirm scope containment: only the 6 files listed above are modified/created
5. Verify acceptance criteria:
   - Endpoint returns correct JSON shape
   - 404 for missing SBOM
   - Deduplication by advisory ID
   - Zero defaults for missing severity levels
