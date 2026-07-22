# Implementation Plan: TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM. This enables dashboard widgets to render severity breakdowns without client-side counting.

## Target Branch

main

## New Endpoint

`GET /api/v2/sbom/{id}/advisory-summary` -- returns `{ critical: N, high: N, medium: N, low: N, total: N }`

## Files to Modify

### 1. `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` to register the new model module alongside existing `pub mod summary;` and `pub mod details;`.

### 2. `modules/fundamental/src/advisory/service/advisory.rs`
Add a `severity_summary` method to `AdvisoryService` that:
- Takes `&self, sbom_id: Id, tx: &Transactional<'_>` (matching existing `fetch`/`list` signature pattern)
- Queries the `sbom_advisory` join table to find all advisories linked to the given SBOM
- Deduplicates by advisory ID
- Reads the `severity` field from each `AdvisorySummary`
- Counts occurrences per severity level (Critical, High, Medium, Low)
- Returns a `SeveritySummary` struct with the counts and total
- Returns 404 (via `AppError`) if the SBOM does not exist

### 3. `modules/fundamental/src/advisory/endpoints/mod.rs`
Register the new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))` following the existing `Router::new().route(...)` pattern.

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`
New model file defining the `SeveritySummary` response struct with fields: `critical: u32`, `high: u32`, `medium: u32`, `low: u32`, `total: u32`. Derives `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default`. Includes a doc comment explaining the struct's purpose.

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
New endpoint handler file containing:
- `get_severity_summary` async handler function
- Extracts path params via `Path<Id>` (matching pattern from `get.rs`)
- Calls `AdvisoryService::severity_summary()`
- Returns `Json<SeveritySummary>` on success or `AppError` on failure
- Error handling uses `.context()` wrapping

### 6. `tests/api/advisory_summary.rs`
Integration test file with four test functions:
- `test_advisory_summary_valid_sbom` -- verifies correct severity counts for a known SBOM
- `test_advisory_summary_not_found` -- verifies 404 for non-existent SBOM ID
- `test_advisory_summary_no_advisories` -- verifies all-zero response for SBOM with no advisories
- `test_advisory_summary_deduplication` -- verifies duplicate advisory links are deduplicated

## Files NOT Modified

- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration, as stated in the task description)

## Cross-Section Reference Consistency

- Entity `AdvisoryService` -- Files to Modify references `service/advisory.rs`, Implementation Notes also references `service/advisory.rs` -- consistent.
- Entity `sbom_advisory` join table -- Implementation Notes references `entity/src/sbom_advisory.rs` -- consistent with entity directory structure.
- Entity `AdvisorySummary.severity` -- Implementation Notes references `model/summary.rs` -- consistent with model directory.

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `id` from path -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> load `AdvisorySummary` records -> count by severity -> return `Json<SeveritySummary>` -- COMPLETE

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService method, endpoint handler,
and integration tests.

Implements TC-9201
```

(Committed with `--trailer="Assisted-by: Claude Code"`)

## PR Description

```
## Summary
- Add `SeveritySummary` response struct for advisory severity counts
- Add `severity_summary` method to `AdvisoryService` that aggregates advisory severities per SBOM
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning critical/high/medium/low/total counts
- Add integration tests covering valid SBOM, 404, empty advisories, and deduplication scenarios

## Jira
Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```
