# Implementation Plan: TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Bookend Type**: (none -- standard flow)
**Target PR**: (none -- standard flow)
**Dependencies**: None

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains:
- Repository Registry: trustify-backend with Serena instance `serena_backend` at path `./`
- Jira Configuration: Project key TC, Cloud ID present, Feature issue type ID 10142, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- Code Intelligence: Serena MCP servers configured, tool naming convention documented, `serena_backend` instance with rust-analyzer

Configuration valid. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description sections:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**: 3 files (advisory service, endpoints/mod.rs, model/mod.rs)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Present with patterns and code references
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 test cases
- **Target PR**: Not present
- **Bookend Type**: Not present
- **Dependencies**: None

**GitHub Issue extraction**: Would read `customfield_10747` from the fetched issue fields. If populated, parse the GitHub issue URL and store `owner/repo#number` for PR description.

All required sections present. No gaps. Proceeding.

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9201)` and search for comments starting with `[sdlc-workflow] Description digest:`. If found, would:
1. Check comment `created` vs `updated` timestamps for edit detection
2. Extract the tagged digest value (e.g., `sha256-md:<hex>`)
3. Write the current description to `/tmp/desc-TC-9201.txt`
4. Compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
5. Compare format tags, then compare hex digests if tags match
6. On match: proceed silently. On mismatch: alert user and stop.

If no digest comment found: log warning and proceed normally.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user via `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition: `jira.transition_issue(TC-9201) -> In Progress`

## Step 4 -- Understand the Code

### CONVENTIONS.md Lookup

Would read `./CONVENTIONS.md` at the repository root (path from Repository Registry). Extract any CI check commands and code generation commands for use in Step 9.

### Code Inspection (via Serena instance `serena_backend`)

**Files to inspect before modifying:**

1. `modules/fundamental/src/advisory/service/advisory.rs`
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its methods (fetch, list, search)
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand the pattern for querying and returning results
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method to see pagination/filtering pattern

2. `modules/fundamental/src/advisory/endpoints/mod.rs`
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern
   - Identify how routes are composed with `Router::new().route()`

3. `modules/fundamental/src/advisory/model/mod.rs`
   - `mcp__serena_backend__get_symbols_overview` to see existing module declarations

4. `modules/fundamental/src/advisory/endpoints/get.rs` (sibling -- pattern reference)
   - `mcp__serena_backend__get_symbols_overview` to see handler function signature
   - `mcp__serena_backend__find_symbol` on the handler to see Path extraction, service call, JSON return

5. `modules/fundamental/src/advisory/model/summary.rs` (sibling -- pattern reference)
   - `mcp__serena_backend__get_symbols_overview` to see AdvisorySummary struct fields (especially the `severity` field)

6. `entity/src/sbom_advisory.rs` (join table)
   - `mcp__serena_backend__get_symbols_overview` to understand the SBOM-Advisory relationship columns

7. `common/src/error.rs` (error handling pattern)
   - `mcp__serena_backend__find_symbol` on `AppError` to understand error variants and `.context()` usage

### Sibling Analysis for Conventions

Inspected siblings (details in outputs/conventions.md):
- Advisory endpoints: `get.rs`, `list.rs`
- Advisory models: `summary.rs`, `details.rs`
- Advisory service: `advisory.rs` (existing methods)
- SBOM endpoints: `get.rs`, `list.rs` (cross-module sibling)
- Test files: `tests/api/advisory.rs`, `tests/api/sbom.rs`

### Documentation Files Identified

- `docs/api.md` -- REST API reference (may need updating with new endpoint)
- `docs/architecture.md` -- System architecture overview
- `README.md` -- Repository readme

## Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new severity_summary route
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` declaration

### Files to Create

4. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
5. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for the endpoint
6. **`tests/api/advisory_summary.rs`** -- Integration tests

Detailed changes for each file are in `outputs/file-1-description.md` through `outputs/file-6-description.md`.

## Step 7 -- Write Tests

Tests are described in `outputs/file-6-description.md`. Four test cases covering:
1. Valid SBOM with known advisories returns correct severity counts
2. Non-existent SBOM ID returns 404
3. SBOM with no advisories returns all zeros
4. Duplicate advisory links are deduplicated in count

Would run `cargo test` to verify all tests pass.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Handler returns `Json<SeveritySummary>` with all fields |
| 2 | Returns 404 when SBOM ID does not exist | Service returns `AppError` with NOT_FOUND when SBOM lookup fails |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Query uses `DISTINCT` on advisory ID before grouping by severity |
| 4 | All severity levels default to 0 when no advisories exist | SeveritySummary fields initialized to 0 via `Default` trait |
| 5 | Response time under 200ms for 500 advisories | Single SQL query with JOIN and GROUP BY; no N+1 queries |

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and compare against Files to Modify and Files to Create. All 6 files are in scope.

### Untracked file check
Run `git status --short` and check for `??` entries in directories containing modified files. Flag any referenced untracked files.

### Dead parameter detection
No parameters are being removed from existing functions. The `severity_summary` method adds new parameters only.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency
The new endpoint `GET /api/v2/sbom/{id}/advisory-summary` is a public API addition. Would check `docs/api.md` and update it with the new endpoint documentation if it describes existing endpoints.

### Data-flow trace
`GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (Id) -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` JOIN `advisory` with GROUP BY severity -> map to `SeveritySummary` struct -> return `Json<SeveritySummary>` -- **COMPLETE**

### Contract & sibling parity
- SeveritySummary implements `Serialize` (required for JSON response) -- verified
- Handler follows same pattern as `get.rs`: Path extraction, service call, error wrapping, JSON return -- parity maintained
- Service method follows same pattern as `fetch`/`list`: accepts `&self, id, tx` -- parity maintained

### CI checks from CONVENTIONS.md
Would run all CI check commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`).

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary response model,
AdvisoryService::severity_summary method, and integration tests.

Implements TC-9201
```

### Commit command

```bash
git add modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary response model,
AdvisoryService::severity_summary method, and integration tests.

Implements TC-9201"
```

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If no upstream remote, use standard flow. If upstream exists, parse owner/repo from both remotes.

### Push and PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint returning severity counts per advisory level
- Add \`SeveritySummary\` response model and \`AdvisoryService::severity_summary\` service method
- Add integration tests for the new endpoint

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

If a GitHub issue reference was extracted from `customfield_10747`, would append `Closes owner/repo#number` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes made
   - Footnote with plugin version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`

3. **Transition**: `jira.transition_issue(TC-9201) -> In Review`
