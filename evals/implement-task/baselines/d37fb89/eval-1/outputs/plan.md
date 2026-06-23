# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Status**: To Do
**Labels**: ai-generated-jira
**Parent Feature**: TC-9001 (is incorporated by)
**Dependencies**: None

## Step 1.5 -- Description Digest

WARNING: No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 2 -- Dependencies

No dependencies declared. Proceeding.

## Step 5 -- Branch Creation

```
git checkout main
git pull
git checkout -b TC-9201
```

Target Branch for PR base: `main`

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register the new route for the severity summary endpoint
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;` to register the new model module

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- `SeveritySummary` response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. **`tests/api/advisory_summary.rs`** -- integration tests for the new endpoint

## No Changes Needed

- **`server/src/main.rs`** -- routes auto-mount via module registration; no changes required

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint returning `{ critical: N, high: N, medium: N, low: N, total: N }`

## Implementation Approach

### Phase 1: Model (file-1)
Create the `SeveritySummary` response struct following the existing model pattern from sibling files like `summary.rs` and `details.rs`.

### Phase 2: Service (file-2)
Add the `severity_summary` method to `AdvisoryService` following the pattern of existing `fetch` and `list` methods. The method queries the `sbom_advisory` join table, resolves advisory severity from `AdvisorySummary`, deduplicates by advisory ID, and counts by severity level.

### Phase 3: Model Registration (file-3)
Register the new model module in `modules/fundamental/src/advisory/model/mod.rs`.

### Phase 4: Endpoint Handler (file-4)
Create the endpoint handler following the pattern in `advisory/endpoints/get.rs`.

### Phase 5: Route Registration (file-5)
Register the new route in `modules/fundamental/src/advisory/endpoints/mod.rs`.

### Phase 6: Tests (file-6)
Create integration tests following the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

## Acceptance Criteria Verification Plan

- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by successful endpoint response with correct fields
- [ ] Returns 404 when SBOM ID does not exist -- verified by test and consistent with existing SBOM endpoint behavior
- [ ] Counts only unique advisories (deduplicates by advisory ID) -- verified by deduplication logic in service and test with duplicate advisory links
- [ ] All severity levels default to 0 when no advisories exist -- verified by test with empty advisory set
- [ ] Response time under 200ms for SBOMs with up to 500 advisories -- verified by efficient query using join table and single-pass counting

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `id` from path (Path<Id>) -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table for advisories linked to SBOM -> resolve each advisory's severity from `AdvisorySummary` -> deduplicate by advisory ID -> count per severity level -> construct `SeveritySummary` -> return `Json<SeveritySummary>` -- **COMPLETE**

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService::severity_summary method, and integration tests.

Implements TC-9201
```

Commit command:
```
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService::severity_summary method, and integration tests.

Implements TC-9201"
```

## PR Creation

```
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

The PR description will include:
- Summary of changes
- Link to Jira issue: `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- Acceptance criteria checklist
