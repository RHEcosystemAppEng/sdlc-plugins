# Implementation Plan: TC-9201

## Task Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.

## Repository

trustify-backend

## Target Branch

main

## Branch Name

TC-9201

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** — Add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Register the new `severity_summary` route
3. **`modules/fundamental/src/advisory/model/mod.rs`** — Add `pub mod severity_summary;` to register the new model module

## Files to Create

4. **`modules/fundamental/src/advisory/model/severity_summary.rs`** — `SeveritySummary` response struct
5. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** — GET handler for `/api/v2/sbom/{id}/advisory-summary`
6. **`tests/api/advisory_summary.rs`** — Integration tests for the new endpoint

## Files NOT Modified

- `server/src/main.rs` — No changes needed (routes auto-mount via module registration)

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` (input: HTTP request with SBOM ID path param)
  -> `severity_summary` handler extracts `Path<Id>` (parsing)
  -> calls `AdvisoryService::severity_summary(sbom_id, tx)` (processing)
  -> service queries `sbom_advisory` join table to find advisories linked to the SBOM (data access)
  -> service maps each advisory's severity field and counts by level, deduplicating by advisory ID (transformation)
  -> service returns `SeveritySummary { critical, high, medium, low, total }` (output)
  -> handler wraps in `Json` and returns HTTP 200 (response)
  -> on missing SBOM: returns `AppError` with 404 status (error path)
  - **Status: COMPLETE** - all stages connected

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201
```

The commit would include the `--trailer="Assisted-by: Claude Code"` flag.

## PR Description

```
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning severity counts (critical, high, medium, low, total) for advisories linked to an SBOM
- Implement `SeveritySummary` model, `AdvisoryService::severity_summary` method, and endpoint handler following existing module patterns
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisory set, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```

## Cross-Section Reference Consistency

- Entity `AdvisoryService` — Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- Entity `AdvisorySummary` (existing, severity field source) — Implementation Notes: `modules/fundamental/src/advisory/model/summary.rs` -- CONSISTENT (read-only reference, not a file to modify)
- Entity `sbom_advisory` join table — Implementation Notes: `entity/src/sbom_advisory.rs` -- CONSISTENT (read-only reference for queries)
- Entity `AppError` — Implementation Notes: `common/src/error.rs` -- CONSISTENT (read-only reference for error pattern)

## Scope Verification Notes

All files in the implementation are within the scope defined by Files to Modify and Files to Create. No out-of-scope changes are needed. The `server/src/main.rs` is explicitly listed as "no changes needed" since routes auto-mount via module registration.
