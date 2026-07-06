# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns
counts of vulnerability advisories per severity level (Critical, High, Medium, Low)
for a given SBOM, plus a total count.

**Repository:** trustify-backend
**Target Branch:** main
**API:** `GET /api/v2/sbom/{id}/advisory-summary` (NEW)

## Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Files to Create

| # | File | Purpose |
|---|------|---------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File | Change |
|---|------|--------|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new route |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |

## No Changes Needed

- `server/src/main.rs` -- routes auto-mount via module registration, no changes needed.

## Data-Flow Trace

```
GET /api/v2/sbom/{id}/advisory-summary
  -> severity_summary handler (extract Path<Id>)
    -> AdvisoryService::severity_summary(sbom_id, tx)
      -> query sbom_advisory join table for matching SBOM
      -> join advisory table to get severity field
      -> deduplicate by advisory ID
      -> count by severity level
      -> return SeveritySummary { critical, high, medium, low, total }
    -> return Json(summary)
```

All stages connected: input (HTTP request) -> processing (service query + aggregation) -> output (JSON response). **COMPLETE**.

## Cross-Section Reference Consistency

- Entity `AdvisoryService` -- Files to Modify and Implementation Notes both reference `modules/fundamental/src/advisory/service/advisory.rs`. Consistent.
- Entity `AdvisorySummary` -- Implementation Notes reference `modules/fundamental/src/advisory/model/summary.rs` for the `severity` field. Consistent (this is a read reference, not a modification target).
- Entity route registration -- Files to Modify and Implementation Notes both reference `modules/fundamental/src/advisory/endpoints/mod.rs`. Consistent.

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns counts of
vulnerability advisories per severity level (critical, high, medium,
low) and a total count for a given SBOM. Includes the SeveritySummary
model, AdvisoryService::severity_summary method, endpoint handler,
and integration tests.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

## PR Description

```
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns advisory severity counts (critical, high, medium, low, total) for a given SBOM
- Add `SeveritySummary` response model, `AdvisoryService::severity_summary` service method, and endpoint handler following existing module patterns
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```

## Acceptance Criteria Verification

| Criterion | How Verified |
|-----------|-------------|
| Returns `{ critical, high, medium, low, total }` | Response struct has all five fields; handler returns `Json(summary)` |
| Returns 404 for non-existent SBOM | Service checks SBOM existence first; returns `AppError` with 404 |
| Deduplicates by advisory ID | Query uses `DISTINCT` on advisory ID or equivalent SeaORM grouping |
| Defaults to 0 for missing severity levels | `SeveritySummary::default()` initializes all counts to 0 |
| Response time under 200ms for 500 advisories | Single query with GROUP BY, no N+1; verified by integration test timing |
