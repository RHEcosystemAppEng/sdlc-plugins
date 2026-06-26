# Implementation Plan for TC-9201

## Task Summary

**Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch to create**: TC-9201
**Linked Issues**: is incorporated by TC-9001

## Step 0 -- Validate Project Configuration

Project Configuration validated in CLAUDE.md:
- Repository Registry: present (trustify-backend, serena_backend, path `./`)
- Jira Configuration: present (Project key TC, Cloud ID, Feature issue type ID)
- Code Intelligence: present (serena_backend with rust-analyzer)

All required sections present. Proceeding.

## Step 1 -- Parse Task Description

Parsed sections:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes**: Follow existing endpoint/service patterns, use sbom_advisory join table, count by severity level
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 handling, deduplication, defaults to zero, performance)
- **Test Requirements**: 4 tests (valid counts, 404, empty SBOM, deduplication)
- **Dependencies**: None
- **Bookend Type**: not present (standard flow)
- **Target PR**: not present (standard flow)

## Step 1.5 -- Description Digest Verification

No digest comment provided. Warning:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

Proceeding normally (backward compatibility).

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue("TC-9201", assignee=<account-id>)` to assign the task
3. `jira.transition_issue("TC-9201")` to In Progress

## Step 4 -- Understand the Code

### Files to inspect before implementation

Using Serena instance `serena_backend` (from Repository Registry):

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Read existing `AdvisoryService` to understand `fetch` and `list` method signatures, understand `&self` and `Transactional` patterns, and identify how queries are built using SeaORM.
   - Tool: `mcp__serena_backend__get_symbols_overview` then `mcp__serena_backend__find_symbol` for `fetch` and `list` methods with `include_body=true`

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Read route registration pattern to understand how routes are composed.
   - Tool: `mcp__serena_backend__get_symbols_overview`

3. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Read the existing GET handler as the template for the new endpoint (Path extraction, service call, JSON response).
   - Tool: `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read to understand module registration pattern for adding `pub mod severity_summary;`.
   - Tool: `mcp__serena_backend__read_file` or Read tool

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- Read `AdvisorySummary` struct to understand the `severity` field that will be used for counting.
   - Tool: `mcp__serena_backend__find_symbol` for `AdvisorySummary` with `include_body=true`

6. **`entity/src/sbom_advisory.rs`** -- Read the join table entity to understand how to query SBOM-Advisory relationships.
   - Tool: `mcp__serena_backend__get_symbols_overview`

7. **`common/src/error.rs`** -- Read `AppError` enum to understand error handling pattern.
   - Tool: `mcp__serena_backend__find_symbol` for `AppError`

### Sibling analysis (convention conformance)

**Production code siblings:**
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler for list pattern
- `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling endpoint handler for get pattern
- `modules/fundamental/src/advisory/model/details.rs` -- sibling model struct
- `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module sibling for SBOM-scoped endpoint pattern
- `modules/fundamental/src/sbom/service/sbom.rs` -- cross-module sibling for service method patterns

**Test file siblings:**
- `tests/api/advisory.rs` -- sibling test file for advisory endpoint tests
- `tests/api/sbom.rs` -- sibling test file for SBOM endpoint tests

### CONVENTIONS.md lookup

Would read `./CONVENTIONS.md` at repository root using `mcp__serena_backend__read_file` or Read tool. Extract CI check commands and code generation commands for Step 9.

### Documentation files identified

- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating with new endpoint)
- `CONVENTIONS.md` at repository root

### Cross-section reference consistency check

Verified that all file paths for each entity are consistent across Files to Modify, Files to Create, and Implementation Notes:
- `AdvisoryService` -- referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent
- `SeveritySummary` -- referenced in Files to Create (`advisory/model/severity_summary.rs`) -- no cross-section conflict
- Route registration -- referenced in both Files to Modify (`advisory/endpoints/mod.rs`) and Implementation Notes (`advisory/endpoints/mod.rs`) -- consistent

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route for the severity summary endpoint
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` to register the new model module

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- `SeveritySummary` response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. **`tests/api/advisory_summary.rs`** -- Integration tests for the new endpoint

## Step 6-7 -- Implementation and Tests

See individual file descriptions in `file-1-description.md` through `file-6-description.md` for detailed changes.

## Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- satisfied by the SeveritySummary struct and endpoint handler
- [x] Returns 404 when SBOM ID does not exist -- satisfied by checking SBOM existence before querying advisories, returning AppError with 404
- [x] Counts only unique advisories (deduplicates by advisory ID) -- satisfied by collecting advisory IDs into a HashSet or using DISTINCT in the query
- [x] All severity levels default to 0 when no advisories exist -- satisfied by SeveritySummary::default() initializing all counts to 0
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- satisfied by a single database query with JOIN, no N+1 pattern

## Step 9 -- Self-Verification

### Scope containment
Would run `git diff --name-only` and verify all changed files are within:
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

### Untracked file check
Would run `git status --short` and check for `??` entries in directories where implementation occurred.

### Sensitive-pattern check
Would run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` and verify no matches.

### Documentation currency
Would check `docs/api.md` to determine if it needs updating with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (Id) -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query sbom_advisory join table -> count by severity level -> return SeveritySummary as JSON -- **COMPLETE**

### Contract & sibling parity
- SeveritySummary implements Serialize (for Axum Json response) -- consistent with sibling model structs
- Endpoint handler follows same pattern as `get.rs`: Path extraction, service call, Result<Json<T>, AppError> -- consistent
- Service method follows same pattern as `fetch`/`list`: takes `&self, id, tx` -- consistent
- Error handling uses `.context()` wrapping -- consistent with all siblings

### Duplication check
Would search for existing severity aggregation logic to confirm no duplication. The `severity` field exists on `AdvisorySummary` (used for per-advisory severity), but no aggregation/counting service exists yet.

### CI checks
Would run CI check commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`, `cargo build`).

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
all advisories linked to a given SBOM. Includes deduplication by
advisory ID and proper 404 handling for non-existent SBOMs.

Implements TC-9201
```

With flag: `--trailer='Assisted-by: Claude Code'`

### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

PR description would include:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (clickable link using webUrl from Jira API response)
- Link to GitHub issue if configured in Jira custom field

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment to TC-9201 with PR link, summary of changes, and skill footer
3. Transition TC-9201 to In Review
