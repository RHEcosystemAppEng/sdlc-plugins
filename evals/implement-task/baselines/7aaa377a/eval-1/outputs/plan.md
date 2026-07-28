# Implementation Plan for TC-9201

## Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM. This enables dashboard widgets to render severity breakdowns without client-side counting.

## Task Metadata

- **Jira Issue**: TC-9201
- **Repository**: trustify-backend
- **Target Branch**: main
- **Branch Name**: TC-9201
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None

## Cross-Section Reference Consistency

- Entity `AdvisoryService` — referenced in both "Files to Modify" (`modules/fundamental/src/advisory/service/advisory.rs`) and "Implementation Notes" (`modules/fundamental/src/advisory/service/advisory.rs`) -- consistent
- Entity `AdvisorySummary` — referenced in "Implementation Notes" (`modules/fundamental/src/advisory/model/summary.rs`) -- consistent with repository structure
- Entity route registration — referenced in "Files to Modify" (`modules/fundamental/src/advisory/endpoints/mod.rs`) and "Implementation Notes" (same path) -- consistent

## Files to Modify

### 1. `modules/fundamental/src/advisory/model/mod.rs`
- **Change**: Add `pub mod severity_summary;` line to register the new model submodule
- **Details**: See `outputs/file-1-description.md`

### 2. `modules/fundamental/src/advisory/service/advisory.rs`
- **Change**: Add `severity_summary` method to `AdvisoryService`
- **Details**: See `outputs/file-2-description.md`

### 3. `modules/fundamental/src/advisory/endpoints/mod.rs`
- **Change**: Register the new `/api/v2/sbom/{id}/advisory-summary` route and import the handler module
- **Details**: See `outputs/file-3-description.md`

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`
- **Change**: New file defining the `SeveritySummary` response struct
- **Details**: See `outputs/file-4-description.md`

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- **Change**: New file with the GET handler for `/api/v2/sbom/{id}/advisory-summary`
- **Details**: See `outputs/file-5-description.md`

### 6. `tests/api/advisory_summary.rs`
- **Change**: New file with integration tests for the advisory summary endpoint
- **Details**: See `outputs/file-6-description.md`

## Files Not Modified

- `server/src/main.rs` — No changes needed; routes auto-mount via module registration

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `Path<Id>` -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> join with `advisory` table to get `AdvisorySummary.severity` -> deduplicate by advisory ID -> count by severity level -> construct `SeveritySummary` response -> return `Json(summary)` -- **COMPLETE**

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint
  - Returns: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
  - 404 when SBOM ID does not exist
  - Deduplicates advisories by advisory ID
  - All severity levels default to 0

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService::severity_summary method,
route registration, and integration tests.

Implements TC-9201
```

## PR Description

```
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning advisory severity counts per SBOM
- Add `SeveritySummary` response model with critical, high, medium, low, and total fields
- Add `severity_summary` method to `AdvisoryService` using `sbom_advisory` join table with deduplication
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```
