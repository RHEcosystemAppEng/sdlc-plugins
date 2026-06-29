# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns counts of vulnerability advisory severities (Critical, High, Medium, Low) for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Project Configuration Validation (Step 0)

The project CLAUDE.md contains:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142, custom fields configured
- Code Intelligence: Serena with rust-analyzer configured

All required sections are present.

## Parsed Task Fields (Step 1)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Linked Issues**: is incorporated by TC-9001
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None
- **GitHub Issue**: Not present in task

## Branch Strategy (Step 5)

Default flow (no Target PR, no Bookend Type):
```
git checkout main
git pull
git checkout -b TC-9201
```

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register the new route
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;` to register the new model module

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- `SeveritySummary` response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. **`tests/api/advisory_summary.rs`** -- integration tests for the new endpoint

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint returning `{ critical: N, high: N, medium: N, low: N, total: N }`

## Implementation Order

1. Create the `SeveritySummary` model struct (outputs/file-1-description.md)
2. Register the model module in `model/mod.rs` (outputs/file-2-description.md)
3. Add the `severity_summary` service method to `AdvisoryService` (outputs/file-3-description.md)
4. Create the endpoint handler (outputs/file-4-description.md)
5. Register the route in `endpoints/mod.rs` (outputs/file-5-description.md)
6. Write integration tests (outputs/file-6-description.md)

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` request received by Axum router
  -> Path parameter `{id}` extracted via `Path<Id>`
  -> `severity_summary` handler invoked
  -> Calls `AdvisoryService::severity_summary(sbom_id, tx)`
  -> Queries `sbom_advisory` join table for advisories linked to the given SBOM
  -> Loads `AdvisorySummary` for each advisory to access the `severity` field
  -> Deduplicates by advisory ID
  -> Counts by severity level (Critical, High, Medium, Low)
  -> Constructs `SeveritySummary` struct with counts and total
  -> Returns `Json(SeveritySummary)` response
  -> **COMPLETE**

## Cross-Section Reference Consistency

- Entity `AdvisoryService` -- referenced in:
  - Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`
  - Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs`
  - Consistent across sections.
- Entity `AdvisorySummary` -- referenced in:
  - Implementation Notes: `modules/fundamental/src/advisory/model/summary.rs`
  - Consistent (not a file to modify, only referenced for reading the `severity` field).
- Entity `sbom_advisory` join table -- referenced in:
  - Implementation Notes: `entity/src/sbom_advisory.rs`
  - Consistent (not a file to modify, only referenced for querying).

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201
```

The commit will include the `--trailer="Assisted-by: Claude Code"` flag.

## PR Details

- **Base branch**: main
- **Head branch**: TC-9201
- **Title**: feat(api): add advisory severity aggregation endpoint
- **Body**:

  Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

  ## Summary
  - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning severity counts per level
  - Add `SeveritySummary` response struct, `AdvisoryService::severity_summary` method, and endpoint handler
  - Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

## Jira Updates (Step 11)

1. Set custom field `customfield_10875` (Git Pull Request) to the PR URL in ADF format
2. Add comment with PR link, summary of changes, and no deviations from the plan
3. Transition TC-9201 to "In Review"
