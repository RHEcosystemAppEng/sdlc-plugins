# Implementation Plan: TC-9201 — Add advisory severity aggregation service and endpoint

## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.

## Branch

- Branch name: `TC-9201`
- Base branch: `main`

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** — `SeveritySummary` response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** — GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. **`tests/api/advisory_summary.rs`** — integration tests for the new endpoint

## Files to Modify

4. **`modules/fundamental/src/advisory/service/advisory.rs`** — add `severity_summary` method to `AdvisoryService`
5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — register the new route
6. **`modules/fundamental/src/advisory/model/mod.rs`** — add `pub mod severity_summary;` to register the new model module

## No Changes Needed

- `server/src/main.rs` — routes auto-mount via module registration (confirmed by task description)

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Includes SeveritySummary model, AdvisoryService.severity_summary
method, and integration tests.

Implements TC-9201
```

The commit would include `--trailer="Assisted-by: Claude Code"`.

## Data-flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` request received
  -> Axum extracts `Path<Id>` from URL -> calls `AdvisoryService::severity_summary(sbom_id, tx)`
  -> service queries `sbom_advisory` join table for advisories linked to the SBOM
  -> for each advisory, reads the `severity` field from `AdvisorySummary`
  -> deduplicates by advisory ID
  -> counts by severity level (Critical, High, Medium, Low)
  -> returns `SeveritySummary { critical, high, medium, low, total }` as JSON response
  -> **COMPLETE**

## Cross-section Reference Consistency

- Entity `AdvisoryService` — Files to Modify lists `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes also references `modules/fundamental/src/advisory/service/advisory.rs` — **consistent**
- Entity `SeveritySummary` — Files to Create lists `modules/fundamental/src/advisory/model/severity_summary.rs`, not referenced elsewhere with a different path — **consistent**
- Entity route registration — Files to Modify lists `modules/fundamental/src/advisory/endpoints/mod.rs`, Implementation Notes also references `modules/fundamental/src/advisory/endpoints/mod.rs` — **consistent**

## Acceptance Criteria Verification Plan

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` — verified by response struct shape and integration test
2. Returns 404 when SBOM ID does not exist — verified by service method checking SBOM existence first and returning AppError
3. Counts only unique advisories (deduplicates by advisory ID) — verified by using `HashSet` or `DISTINCT` in query
4. All severity levels default to 0 when no advisories exist at that level — verified by `SeveritySummary::default()` initialization
5. Response time under 200ms for SBOMs with up to 500 advisories — verified by efficient SQL query with join and GROUP BY
