# Implementation Plan: TC-9201 -- Add advisory severity aggregation service and endpoint

## Task Summary

Add a `GET /api/v2/sbom/{id}/advisory-summary` endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns `{ critical, high, medium, low, total }` counts, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Project Configuration Validation (Step 0)

Verified the following sections exist in CLAUDE.md under `# Project Configuration`:
- Repository Registry: contains `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID present
- Code Intelligence: Serena instance `serena_backend` configured with `rust-analyzer`

## Task Parsing (Step 1)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: none (standard implementation task)
- **Target PR**: none (new PR flow)
- **Dependencies**: none
- **GitHub Issue custom field**: customfield_10747 (would check for linked GitHub issue)
- **Jira web URL**: would be captured from API response for PR description link

## Files to Create

| # | File | Purpose |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct with Serialize/Deserialize/ToSchema |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File | Change |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |
| 5 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 6 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new route and declare the severity_summary endpoint module |

## Files NOT Modified

- `server/src/main.rs` -- no changes needed; routes auto-mount via module registration in each module's `endpoints/mod.rs`.

## Implementation Order

1. Create the `SeveritySummary` response model (file 1) -- the data type must exist before the service or handler can reference it
2. Register the model module in `mod.rs` (file 4) -- makes the struct importable
3. Add the `severity_summary` service method (file 5) -- business logic that the handler delegates to
4. Create the endpoint handler (file 2) -- HTTP layer that calls the service
5. Register the route in endpoints `mod.rs` (file 6) -- wires the handler into the router
6. Add integration tests (file 3) -- validates the full stack end-to-end

## Data-Flow Trace (Step 9)

```
GET /api/v2/sbom/{id}/advisory-summary
  -> Path<Id> extraction (Axum)
  -> severity_summary handler (endpoints/severity_summary.rs)
  -> AdvisoryService::severity_summary (service/advisory.rs)
  -> sbom entity lookup (verify SBOM exists, 404 if not)
  -> sbom_advisory join table query (find linked advisories)
  -> HashSet deduplication (unique advisory IDs)
  -> advisory entity fetch (get severity fields)
  -> SeveritySummary aggregation (count per severity level)
  -> Json<SeveritySummary> response
```

**Status**: COMPLETE -- all stages connected from HTTP input through processing to JSON response.

## Cross-Section Reference Consistency

Verified that all file paths referenced across the task description sections are consistent:
- `AdvisoryService` is referenced in both Files to Modify (`service/advisory.rs`) and Implementation Notes (`service/advisory.rs`) -- consistent.
- `AdvisorySummary` is referenced in Implementation Notes as being in `model/summary.rs` -- this is a read-only reference (used for its `severity` field), not a file being modified. No conflict.
- `sbom_advisory` join table is referenced in Implementation Notes as `entity/src/sbom_advisory.rs` -- consistent with the repo structure.

## Acceptance Criteria Verification Plan

- [ ] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by `test_severity_summary_with_advisories`
- [ ] Returns 404 when SBOM ID does not exist -- verified by `test_severity_summary_sbom_not_found`
- [ ] Counts only unique advisories (deduplicates by advisory ID) -- verified by `test_severity_summary_deduplicates_advisories`
- [ ] All severity levels default to 0 when no advisories exist -- verified by `test_severity_summary_no_advisories`
- [ ] Response time under 200ms for SBOMs with up to 500 advisories -- addressed by query design (single join query + in-memory aggregation)

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Uses sbom_advisory join table with HashSet
deduplication and case-insensitive severity matching.

Includes SeveritySummary model, AdvisoryService method, endpoint
handler with utoipa OpenAPI annotations, and integration tests
covering correct counts, 404, zero counts, and deduplication.

Implements TC-9201
```

## PR Description

```
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning aggregated severity counts
- Enables dashboard widgets to render severity breakdowns without client-side counting
- Deduplicates advisories by ID and defaults all counts to 0

## Test plan

- [ ] `test_severity_summary_with_advisories` -- verifies correct severity counts for known data
- [ ] `test_severity_summary_sbom_not_found` -- verifies 404 for non-existent SBOM
- [ ] `test_severity_summary_no_advisories` -- verifies all-zero response for empty SBOM
- [ ] `test_severity_summary_deduplicates_advisories` -- verifies duplicate join entries produce single count

Implements [TC-9201](<jira-web-url>)
```
