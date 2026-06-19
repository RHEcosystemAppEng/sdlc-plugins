# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Branch Operations

1. Check out target branch and create task branch:
   ```
   git checkout main
   git pull
   git checkout -b TC-9201
   ```

## Description Digest Verification (Step 1.5)

> WARNING: No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

## Dependencies

No dependencies. Proceeding.

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new severity summary route
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` to register the new model module

## Files to Create

4. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- `SeveritySummary` response struct
5. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`
6. **`tests/api/advisory_summary.rs`** -- Integration tests for the new endpoint

## No Changes Needed

- `server/src/main.rs` -- Routes auto-mount via module registration (confirmed by conventions)

## Cross-Section Reference Consistency

- Entity `AdvisoryService`: Files to Modify lists `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes also references `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- Entity `AdvisorySummary` (existing): Implementation Notes references `modules/fundamental/src/advisory/model/summary.rs` for the `severity` field -- CONSISTENT (this is the existing struct, not the new one)
- Entity `SeveritySummary` (new): Files to Create lists `modules/fundamental/src/advisory/model/severity_summary.rs` -- no cross-reference conflicts
- Entity `sbom_advisory` join table: Implementation Notes references `entity/src/sbom_advisory.rs` -- CONSISTENT with repo structure
- Entity `AppError`: Implementation Notes references `common/src/error.rs` -- CONSISTENT with repo structure

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary`:
  - Input: HTTP request with SBOM ID path parameter -> `Path<Id>` extraction in handler
  - Processing: Handler calls `AdvisoryService::severity_summary(sbom_id, tx)` -> service queries `sbom_advisory` join table -> joins with advisory table to get severity -> aggregates counts by severity level -> deduplicates by advisory ID
  - Output: Returns `Json<SeveritySummary>` with `{ critical, high, medium, low, total }` -> serialized as JSON response
  - **STATUS: COMPLETE** -- all stages connected

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService::severity_summary method, and integration tests.

Implements TC-9201
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Creation

```
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

PR description body would include:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- Link to acceptance criteria

## Jira Updates (Step 11)

1. Set Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment to TC-9201 with PR link and summary of changes
3. Transition TC-9201 to "In Review"
