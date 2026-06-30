# Implementation Plan -- TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Status**: To Do
**Target Branch**: main
**Branch Name**: TC-9201
**Repository**: trustify-backend
**Serena Instance**: serena_backend
**Linked Issues**: is incorporated by TC-9001
**Dependencies**: None
**Bookend Type**: None (standard implementation flow)
**Target PR**: None (standard flow -- create new branch and PR)

## Description Digest Verification

> No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

## Dependency Verification

Dependencies: None. No blocking prerequisites.

## Branch Strategy

```
git checkout main
git pull
git checkout -b TC-9201
```

## Files to Create

1. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
3. `tests/api/advisory_summary.rs` -- Integration tests for the new endpoint

## Files to Modify

1. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
3. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService

## Files NOT Modified

- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration, as stated in task)

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint returning `{ critical: N, high: N, medium: N, low: N, total: N }`

## Implementation Approach

### Step-by-step

1. **Create SeveritySummary model** (`model/severity_summary.rs`) -- define the response struct
2. **Register model module** (`model/mod.rs`) -- add `pub mod severity_summary;`
3. **Add service method** (`service/advisory.rs`) -- add `severity_summary` method to `AdvisoryService`
4. **Create endpoint handler** (`endpoints/severity_summary.rs`) -- implement GET handler
5. **Register route** (`endpoints/mod.rs`) -- add route for the new endpoint
6. **Write integration tests** (`tests/api/advisory_summary.rs`) -- cover all test requirements
7. **Run tests** -- `cargo test` to verify
8. **Verify acceptance criteria** -- check each criterion
9. **Self-verification** -- scope containment, sensitive pattern check, data-flow trace, duplication check, contract & sibling parity
10. **Commit and push** -- conventional commit with Jira ID

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` request
  -> Axum extracts `Path<Id>` (SBOM ID) -- INPUT
  -> Calls `AdvisoryService::severity_summary(sbom_id, tx)` -- PROCESSING
  -> Service queries `sbom_advisory` join table to find advisories linked to SBOM -- PROCESSING
  -> For each advisory, reads `severity` field from `AdvisorySummary` -- PROCESSING
  -> Deduplicates by advisory ID, counts per severity level -- PROCESSING
  -> Returns `SeveritySummary { critical, high, medium, low, total }` -- OUTPUT
  -> Axum serializes via `Json` extractor and returns HTTP 200 -- OUTPUT
  -> On SBOM not found: returns 404 via `AppError` -- ERROR PATH

All stages connected. Flow is COMPLETE.

## Documentation Impact

- `docs/api.md` -- should be updated to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, its parameters, and response shape

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService.severity_summary method, and integration tests.

Implements TC-9201
```

With trailer: `--trailer='Assisted-by: Claude Code'`

## PR Creation

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

PR description would include:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- Link to acceptance criteria

## Jira Updates

1. Set Git Pull Request custom field (`customfield_10875`) with ADF inlineCard containing PR URL
2. Add comment with PR link, summary of changes, and any deviations
3. Transition TC-9201 to In Review
