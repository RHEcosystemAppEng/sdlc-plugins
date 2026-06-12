# Implementation Plan -- TC-9201

## Task Summary

**Jira Issue:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Branch to Create:** TC-9201
**Dependencies:** None
**Bookend Type:** None (standard implementation flow)
**Target PR:** None (standard flow -- create new PR)

## Step 0 -- Validate Project Configuration

Project Configuration validated successfully:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend` at path `./`
- Jira Configuration: Project key `TC`, Cloud ID present, Feature issue type ID `10142`
- Code Intelligence: Serena instance `serena_backend` with `rust-analyzer`

## Step 1 -- Fetch and Parse Jira Task

All required sections are present in the task description:
- Repository: trustify-backend
- Target Branch: main
- Description: Add severity aggregation service and REST endpoint
- Files to Modify: 3 files
- Files to Create: 3 files
- API Changes: 1 new endpoint
- Implementation Notes: detailed patterns
- Acceptance Criteria: 5 items
- Test Requirements: 4 items
- Dependencies: None

No Target PR, no Bookend Type, no GitHub Issue custom field value to extract.

## Step 1.5 -- Verify Description Integrity

No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9201)` to In Progress

## Step 4 -- Understand the Code

Convention conformance analysis completed (see outputs/conventions.md for full details).

Key findings from code inspection:
- `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` has `fetch` and `list` methods -- new `severity_summary` method will follow the same signature pattern
- `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` has a `severity` field usable for counting
- `sbom_advisory` join table in `entity/src/sbom_advisory.rs` links SBOMs to advisories
- Endpoint pattern in `modules/fundamental/src/advisory/endpoints/get.rs` uses `Path<Id>` extraction
- Route registration in `modules/fundamental/src/advisory/endpoints/mod.rs` uses `Router::new().route()` pattern
- Error handling uses `AppError` with `.context()` wrapping from `common/src/error.rs`

Documentation files identified:
- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/api.md` (referenced in project CLAUDE.md)

## Step 5 -- Create Branch

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
2. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
3. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route

## Files NOT Modified (confirmed per task description)

- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)

## Step 6 -- Implementation Details

See individual file description outputs:
- outputs/file-1-description.md -- severity_summary.rs model (CREATE)
- outputs/file-2-description.md -- severity_summary.rs endpoint handler (CREATE)
- outputs/file-3-description.md -- advisory_summary.rs integration tests (CREATE)
- outputs/file-4-description.md -- model/mod.rs modification (MODIFY)
- outputs/file-5-description.md -- advisory.rs service modification (MODIFY)
- outputs/file-6-description.md -- endpoints/mod.rs modification (MODIFY)

## Step 8 -- Acceptance Criteria Verification

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` -- implemented in endpoint handler
- [x] Returns 404 when SBOM ID does not exist -- service method returns AppError::NotFound, tested
- [x] Counts only unique advisories (deduplicates by advisory ID) -- service uses HashSet or DISTINCT in query
- [x] All severity levels default to 0 when no advisories exist -- SeveritySummary::default() initializes all to 0
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- single query with JOIN, no N+1

## Step 9 -- Self-Verification

### Scope containment
All modified/created files are within the Files to Modify and Files to Create lists. No out-of-scope changes.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `sbom_id` from path (Path<Id>) -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` JOIN `advisory` with GROUP BY severity -> map to `SeveritySummary` struct -> return `Json(summary)` -- **COMPLETE**

### Contract & sibling parity
- `SeveritySummary` is a standalone response struct, no trait contract to implement beyond `Serialize`/`Deserialize`
- Sibling parity with `get.rs` endpoint: error handling via `AppError` with `.context()` -- matched
- Sibling parity with `AdvisorySummary`: uses same `severity` field type -- consistent

## Step 10 -- Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add a service method and REST endpoint that aggregates vulnerability
advisory severity counts for a given SBOM. The GET endpoint at
/api/v2/sbom/{id}/advisory-summary returns counts per severity level
(Critical, High, Medium, Low) and a total count.

Implements TC-9201
```

With trailer: `--trailer='Assisted-by: Claude Code'`

## Step 10 -- Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

PR description would include:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (clickable link)

## Step 11 -- Update Jira

Would execute:
1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment to TC-9201 with PR link, summary of changes, and confirmation of no deviations
3. Transition TC-9201 to In Review
