# Implementation Plan: TC-9201 -- Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

The project CLAUDE.md (`claude-md-mock.md`) contains all required sections:
1. **Repository Registry** -- present, lists `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID, custom fields
3. **Code Intelligence** -- present with tool naming convention `mcp__serena_backend__<tool>` and rust-analyzer

Configuration is valid. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed from `task-standard.md`:

- **Key**: TC-9201
- **Summary**: Add advisory severity aggregation service and endpoint
- **Repository**: trustify-backend
- **Target Branch**: `main`
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing patterns in `get.rs`, `advisory.rs` service, use `sbom_advisory` join table, use `AdvisorySummary.severity` field, return `AppError` with `.context()`.
- **Acceptance Criteria**: 5 items (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 test cases
- **Dependencies**: None
- **Bookend Type**: Not present (standard flow)
- **Target PR**: Not present (standard flow)
- **GitHub Issue**: Not extracted (no custom field value in mock)

## Step 1.5 -- Verify Description Integrity

Would fetch comments on TC-9201 via `jira.get_issue_comments("TC-9201")` and search for digest comments starting with `[sdlc-workflow] Description digest:`.

**Since this is an eval (no Jira access):** No description digest comment found. Logging warning and proceeding normally:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

This is the backward-compatible behavior: when no digest exists, we do not block execution.

## Step 2 -- Verify Dependencies

The task lists `Dependencies: None`. No dependency verification needed.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` -- get current user account ID
2. `jira.edit_issue("TC-9201", assignee=<account-id>)` -- assign task
3. `jira.transition_issue("TC-9201")` -> In Progress

## Step 4 -- Understand the Code

### Serena-based analysis plan

Using `mcp__serena_backend__<tool>` for code intelligence:

1. **get_symbols_overview** on files to modify:
   - `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` struct and existing methods (`fetch`, `list`, `search`)
   - `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration pattern

2. **find_symbol** with `include_body=true`:
   - `AdvisoryService::fetch` -- understand method signature and error handling pattern
   - `AdvisoryService::list` -- understand query pattern with transactional parameter
   - `AdvisorySummary` struct in `model/summary.rs` -- understand the `severity` field type

3. **find_referencing_symbols** on:
   - `AdvisoryService` -- identify all callers to ensure new method follows compatible patterns

4. **Sibling analysis** (convention conformance):
   - `get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` -- sibling endpoint
   - `get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- closest sibling
   - `get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` -- list endpoint pattern

5. **Test sibling analysis**:
   - `get_symbols_overview` on `tests/api/advisory.rs` -- existing advisory tests
   - `get_symbols_overview` on `tests/api/sbom.rs` -- SBOM test patterns

6. **Entity inspection**:
   - `search_for_pattern` for `sbom_advisory` in `entity/src/sbom_advisory.rs` -- understand join table structure

7. **CONVENTIONS.md lookup**:
   - Read `./CONVENTIONS.md` at repository root (noted in repo structure)
   - Extract CI check commands if present

8. **Documentation file identification**:
   - `docs/api.md` -- API reference documentation, may need updating with new endpoint
   - `README.md` -- project readme, unlikely to need changes for a single endpoint

### Cross-section reference consistency check

Verified file paths across task sections:
- `AdvisoryService` -- referenced in both "Files to Modify" (`service/advisory.rs`) and "Implementation Notes" (`service/advisory.rs`) -- **CONSISTENT**
- `AdvisorySummary` -- referenced in "Implementation Notes" (`model/summary.rs`) -- read-only reference, not in Files to Modify -- **CONSISTENT** (used for reading the severity field, not modified)
- Route registration -- both "Files to Modify" and "Implementation Notes" reference `endpoints/mod.rs` -- **CONSISTENT**

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

Target Branch is `main`. Standard flow (no Target PR, no Bookend Type).

## Step 6 -- Implement Changes

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- New file: SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- New file: GET handler

### Files to Modify

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add module registration
4. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method
5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register new route

### Files NOT Modified

- **`server/src/main.rs`** -- No changes needed (routes auto-mount via module registration, as stated in task)

### Test Files to Create

6. **`tests/api/advisory_summary.rs`** -- Integration tests

## Step 7 -- Write Tests

See `outputs/file-6-description.md` for detailed test implementation.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Implemented in endpoint handler; struct has `critical`, `high`, `medium`, `low`, `total` fields |
| Returns 404 when SBOM ID does not exist | Handler checks SBOM existence first, returns `AppError` 404 |
| Counts only unique advisories | Service method deduplicates by advisory ID using `HashSet` or `DISTINCT` in query |
| All severity levels default to 0 | Struct uses `Default` derive or explicit zero initialization |
| Response time under 200ms for 500 advisories | Single SQL query with COUNT + GROUP BY, no N+1 pattern |

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` would show exactly the 5 files modified/created plus 1 test file
- All files match Files to Modify and Files to Create sections

### Sensitive-pattern check
- No passwords, API keys, secrets, or .env files in changes

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `sbom_id` from path -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> join with `advisory` table -> group by severity -> count per group -> build `SeveritySummary` struct -> return `Json(summary)` -- **COMPLETE**

### Duplication check
- No existing severity aggregation logic found in the codebase
- Reuses existing `AdvisoryService` struct rather than creating a new service

### Contract & sibling parity
- `SeveritySummary` is a standalone struct (no trait implementation needed)
- Sibling parity with `get.rs` endpoint: same error handling pattern, same `Path<Id>` extraction, same `Result<T, AppError>` return type

### Documentation currency
- `docs/api.md` should be updated with the new endpoint documentation

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary response
model, AdvisoryService.severity_summary() method, and integration tests.

Implements TC-9201
```

With trailer: `--trailer='Assisted-by: Claude Code'`

### Branch and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

The PR description would include:
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (clickable link)
- Summary of changes
- Test coverage details

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment to TC-9201 with PR link, summary of changes, and confirmation of no deviations
3. Transition TC-9201 to **In Review**

## Summary of All Files

| # | File | Action | Description File |
|---|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | Create | `outputs/file-1-description.md` |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | Create | `outputs/file-2-description.md` |
| 3 | `modules/fundamental/src/advisory/model/mod.rs` | Modify | `outputs/file-3-description.md` |
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Modify | `outputs/file-4-description.md` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Modify | `outputs/file-5-description.md` |
| 6 | `tests/api/advisory_summary.rs` | Create | `outputs/file-6-description.md` |
