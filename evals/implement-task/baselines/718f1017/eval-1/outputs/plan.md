# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns
severity counts (Critical, High, Medium, Low, total) for a given SBOM's linked
advisories.

## Target Repository

trustify-backend (Serena instance: serena_backend, Path: ./)

## Target Branch

main

## Branch Name

TC-9201

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - Add a `severity_summary` method to `AdvisoryService`
   - Method signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
   - Queries `sbom_advisory` join table, joins with advisory to get severity, groups and counts by severity level, deduplicates by advisory ID

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - Add `pub mod severity_summary;` to register the new endpoint module
   - Add route registration: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))`

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - Add `pub mod severity_summary;` to register the new model module

4. **`server/src/main.rs`**
   - No changes needed (routes auto-mount via module registration, as stated in task description)

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`**
   - Define `SeveritySummary` response struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
   - Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`, `Eq`, `Default`
   - Add `utoipa::ToSchema` derive for OpenAPI spec generation
   - Add doc comment explaining the struct's purpose

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`**
   - Define `get_severity_summary` handler function
   - Extract path params via `Path<Id>` (following pattern from `get.rs`)
   - Call `AdvisoryService::severity_summary` with the SBOM ID
   - Return `Json<SeveritySummary>` on success, `AppError` with `.context()` wrapping on failure
   - Return 404 when SBOM ID does not exist

3. **`tests/api/advisory_summary.rs`**
   - Integration test: valid SBOM with known advisories returns correct severity counts
   - Integration test: non-existent SBOM ID returns 404
   - Integration test: SBOM with no advisories returns all zeros
   - Integration test: duplicate advisory links are deduplicated in counts

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given SBOM.
Includes SeveritySummary model, AdvisoryService method, and integration tests.

Implements TC-9201
```

The commit will include `--trailer="Assisted-by: Claude Code"`.

## PR Details

- **Base branch**: main
- **Head branch**: TC-9201
- **Title**: feat(advisory): add severity aggregation endpoint for SBOM advisories
- **Body**: Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Jira Updates

1. Transition TC-9201 to In Progress at start
2. Assign to current user
3. After PR creation: set `customfield_10875` (Git Pull Request) to PR URL in ADF format
4. Add comment with PR link and summary of changes
5. Transition TC-9201 to In Review
