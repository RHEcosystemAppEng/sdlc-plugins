# Implementation Plan for TC-9201

## Task Summary
Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM.

## Repository
trustify-backend

## Target Branch
main

## Branch Name
TC-9201

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** — New response model struct `SeveritySummary`
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** — GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. **`tests/api/advisory_summary.rs`** — Integration tests for the new endpoint

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** — Add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Register the new route for the severity summary endpoint
3. **`modules/fundamental/src/advisory/model/mod.rs`** — Add `pub mod severity_summary;` to register the new model module

## Files NOT Modified
- `server/src/main.rs` — No changes needed (routes auto-mount via module registration, as confirmed by task description)

## Implementation Sequence

1. Create the `SeveritySummary` response model struct (file-1)
2. Register the model module in `model/mod.rs` (file-4)
3. Add the `severity_summary` service method to `AdvisoryService` (file-5)
4. Create the endpoint handler (file-2)
5. Register the route in `endpoints/mod.rs` (file-6)
6. Write integration tests (file-3)

## Cross-Section Reference Consistency

Verified that all entity-to-file-path references are consistent across the task description sections:
- `AdvisoryService` — consistently at `modules/fundamental/src/advisory/service/advisory.rs` in both Files to Modify and Implementation Notes
- `AdvisorySummary` — consistently at `modules/fundamental/src/advisory/model/summary.rs` in Implementation Notes
- Route registration — consistently at `modules/fundamental/src/advisory/endpoints/mod.rs`

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` request
  -> Extract `id` from path via `Path<Id>` extractor
  -> Call `AdvisoryService::severity_summary(sbom_id, tx)`
  -> Query `sbom_advisory` join table to find advisories linked to SBOM
  -> Join with advisory data to get severity levels from `AdvisorySummary.severity`
  -> Deduplicate by advisory ID
  -> Count per severity level (Critical, High, Medium, Low)
  -> Return `SeveritySummary { critical, high, medium, low, total }`
  -> Axum serializes via `Json` extractor
  -> **COMPLETE**

- Error path: SBOM ID not found
  -> Service method returns `AppError` with 404 status
  -> Axum converts to HTTP 404 response
  -> **COMPLETE**

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201
```

## PR Description

```
## Summary

- Add `SeveritySummary` response model with per-severity counts and total
- Add `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, deduplicates by advisory ID, and counts by severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint with 404 handling for missing SBOMs
- Add integration tests covering valid SBOM, non-existent SBOM, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```
