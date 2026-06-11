# Implementation Plan: TC-9201

## Task Summary

**Jira Issue:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Target Branch:** main
**Feature Branch Name:** TC-9201
**Parent Feature:** TC-9001 (is incorporated by)
**Status:** To Do
**Repository:** trustify-backend

## Step 1.5 — Description Digest Check

No description digest comment was found on the issue. Proceeding with a warning:

> "No description digest found — skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 2 — Dependency Verification

No dependencies listed. Proceeding.

## Step 3 — Jira Transitions

- Retrieve current user's Jira account ID via `jira.user_info()`
- Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
- Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 5 — Branch Creation

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch is named after the Jira issue ID (`TC-9201`) per workflow conventions.

## Files to Create

| # | File Path | Purpose |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | SeveritySummary response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for /api/v2/sbom/{id}/advisory-summary |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File Path | Change Description |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to AdvisoryService |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new route for the severity summary endpoint |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |

## No Changes Needed

- `server/src/main.rs` — routes auto-mount via module registration; no changes needed as confirmed by the task description.

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` — **NEW** endpoint
- Returns: `{ critical: N, high: N, medium: N, low: N, total: N }`
- Returns 404 when SBOM ID does not exist
- Counts only unique advisories (deduplicated by advisory ID)
- All severity levels default to 0

## Implementation Approach

### Convention Conformance

All implementations will follow the conventions discovered from sibling analysis (see `outputs/conventions.md`):
- Handlers return `Result<T, AppError>` with `.context()` wrapping
- Path parameters extracted via Axum `Path<Id>`
- Service methods take `(&self, sbom_id: Id, tx: &Transactional<'_>)`
- Model structs derive `Serialize, Deserialize, Debug, Clone`
- Route registration via `.route()` chaining in `endpoints/mod.rs`
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern with real PostgreSQL

### Data Flow Trace

```
GET /api/v2/sbom/{id}/advisory-summary
  -> severity_summary handler (endpoints/severity_summary.rs)
    -> extracts Path<Id> for sbom_id
    -> calls AdvisoryService::severity_summary(sbom_id, tx)
      -> queries sbom_advisory join table for advisories linked to SBOM
      -> loads AdvisorySummary records to access severity field
      -> deduplicates by advisory ID
      -> counts per severity level (Critical, High, Medium, Low)
    -> returns Json<SeveritySummary> with counts + total
```

All stages connected: input (path param) -> processing (service query + aggregation) -> output (JSON response). **COMPLETE**.

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService::severity_summary method,
and integration tests.

Implements TC-9201
```

With trailer: `--trailer='Assisted-by: Claude Code'`

Full commit command:
```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      tests/api/advisory_summary.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService::severity_summary method,
and integration tests.

Implements TC-9201"
```

## Step 10 — Push and PR

```bash
git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary
- Add SeveritySummary response model with critical, high, medium, low, and total count fields
- Add AdvisoryService::severity_summary method that queries sbom_advisory join table and aggregates by severity level
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler
- Register the new route in advisory endpoints module
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

## Jira
Implements [TC-9201](https://<jira-host>/browse/TC-9201)"
```

## Step 11 — Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL in ADF format
2. Add comment to TC-9201 with PR link and summary of changes
3. Transition TC-9201 to "In Review"
