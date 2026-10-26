# Implementation Plan for TC-9201

## Task Summary

**Jira Key:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Linked Issues:** is incorporated by TC-9001
**Dependencies:** None
**Bookend Type:** None
**Target PR:** None

## Step 0 -- Validate Project Configuration

CLAUDE.md contains all required sections:
- **Repository Registry**: trustify-backend entry with Serena Instance `serena_backend` and Path `./`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID 10142, Git Pull Request custom field customfield_10875, GitHub Issue custom field customfield_10747
- **Code Intelligence**: Tool naming convention `mcp__<serena-instance>__<tool>`, serena_backend configured for trustify-backend with rust-analyzer

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:
- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify:** 3 files (advisory service, endpoints mod, model mod)
- **Files to Create:** 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes:** GET /api/v2/sbom/{id}/advisory-summary (NEW)
- **Implementation Notes:** Follow existing endpoint/service patterns, use sbom_advisory join table, use AdvisorySummary.severity for counting
- **Acceptance Criteria:** 5 criteria
- **Test Requirements:** 4 test cases
- **webUrl:** https://redhat.atlassian.net/browse/TC-9201

**GitHub Issue custom field:** customfield_10747 -- would read from the Jira issue response. If populated, parse owner/repo#number for PR description Closes line.

## Step 1.5 -- Verify Description Integrity

Would fetch comments via `jira.get_issue_comments(TC-9201)` and search for the marker `[sdlc-workflow] Description digest:`. If found, would:
1. Check created vs updated timestamps for edit detection
2. Extract the tagged digest (e.g., `sha256-md:<hex>`)
3. Write the current description to `/tmp/desc-TC-9201.txt`
4. Run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
5. Compare format tags, then compare hex digests if tags match
6. Proceed on match; alert user on mismatch

If no digest comment found, log warning and proceed (backward compatibility).

## Step 2 -- Verify Dependencies

No dependencies listed. Skip.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9201)` to "In Progress"

## Step 4 -- Understand the Code

### Code Inspection Plan

Using Serena instance `serena_backend` (tool prefix: `mcp__serena_backend__`):

1. **get_symbols_overview** on files to modify:
   - `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService struct, existing methods (fetch, list, search), their signatures
   - `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration pattern

2. **find_symbol** with `include_body=true`:
   - `AdvisoryService::fetch` -- to understand method signature pattern (self, id, tx params)
   - `AdvisoryService::list` -- to understand list method pattern
   - Route registration in endpoints/mod.rs -- to see Router::new().route() pattern

3. **find_referencing_symbols** on:
   - `AdvisoryService` -- to check all callers and ensure new method won't break existing usage

4. **Sibling convention analysis** (see outputs/conventions.md):
   - Endpoints: read `endpoints/get.rs` and `endpoints/list.rs` for handler patterns
   - Models: read `model/summary.rs` and `model/details.rs` for struct patterns
   - Service: read `advisory.rs` for service method patterns
   - Tests: read `tests/api/advisory.rs` and `tests/api/sbom.rs` for test patterns

5. **search_for_pattern** for:
   - `sbom_advisory` entity usage -- how the join table is queried
   - `severity` field usage in AdvisorySummary -- how severity is represented
   - `AppError` usage -- error handling pattern
   - `Transactional` usage -- transaction parameter pattern

6. **CONVENTIONS.md lookup**: Check `./CONVENTIONS.md` at repo root using `mcp__serena_backend__list_dir` or Read. If present, read it for naming rules, directory structure, code patterns, test conventions, and CI check commands.

7. **Cargo metadata for crate resolution**: Run `cargo metadata --no-deps --format-version 1` from workspace root to resolve package names for modified files. This maps `modules/fundamental/` files to their crate name (likely `trustify-fundamental` or similar) for running `cargo test -p <crate-name>`.

### Documentation Files Identified

- `README.md` at repo root
- `CONVENTIONS.md` at repo root
- `docs/api.md` -- REST API reference (would need updating for new endpoint)
- `docs/architecture.md` -- system architecture overview

### Data-Flow Trace

Input: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID as path parameter
Processing:
  1. Axum extracts `Path<Id>` from URL
  2. Handler calls `AdvisoryService::severity_summary(sbom_id, tx)`
  3. Service queries `sbom_advisory` join table to find advisories linked to the SBOM
  4. Service loads AdvisorySummary for each advisory, extracts severity field
  5. Service deduplicates by advisory ID
  6. Service counts by severity level (Critical, High, Medium, Low), defaults to 0
  7. Service constructs SeveritySummary with counts and total
Output: JSON response `{ critical: N, high: N, medium: N, low: N, total: N }`

All stages are connected. The endpoint receives the request, delegates to the service, which queries the database and returns the aggregated result.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Files to Modify

### File 1: `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` to register the new model module.
See: outputs/file-1-description.md

### File 2: `modules/fundamental/src/advisory/service/advisory.rs`
Add `severity_summary` method to AdvisoryService.
See: outputs/file-2-description.md

### File 3: `modules/fundamental/src/advisory/endpoints/mod.rs`
Register the new `/api/v2/sbom/{id}/advisory-summary` route.
See: outputs/file-3-description.md

## Step 6 -- Files to Create

### File 4: `modules/fundamental/src/advisory/model/severity_summary.rs`
SeveritySummary response struct.
See: outputs/file-4-description.md

### File 5: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
GET handler for `/api/v2/sbom/{id}/advisory-summary`.
See: outputs/file-5-description.md

### File 6: `tests/api/advisory_summary.rs`
Integration tests for the new endpoint.
See: outputs/file-6-description.md

## Step 7 -- Tests

Four test cases as specified in Test Requirements:
1. Valid SBOM with known advisories returns correct severity counts
2. Non-existent SBOM ID returns 404
3. SBOM with no advisories returns all zeros
4. Duplicate advisory links are deduplicated in the count

See outputs/file-6-description.md for detailed test implementation.

## Step 8 -- Verify Acceptance Criteria

| Criterion | How Verified |
|---|---|
| GET endpoint returns `{ critical, high, medium, low, total }` | SeveritySummary struct fields match; handler returns Json(summary) |
| Returns 404 for non-existent SBOM | Service checks SBOM existence first, returns AppError::NotFound |
| Counts only unique advisories (deduplicates by advisory ID) | Service uses HashSet or .unique() on advisory IDs before counting |
| All severity levels default to 0 | SeveritySummary uses Default derive or explicit 0 initialization |
| Response time under 200ms for up to 500 advisories | Single SQL query with GROUP BY aggregation avoids N+1 |

## Step 9 -- Self-Verification Checks

### Scope containment
`git diff --name-only` would list exactly 6 files (3 modified, 3 created). All are within Files to Modify and Files to Create. No out-of-scope files.

### Untracked file check
New files (`severity_summary.rs` model, `severity_summary.rs` endpoint, `advisory_summary.rs` test) are all listed in Files to Create. Stage them after verifying they are referenced by modified files.

### Dead parameter detection
No parameters removed from existing functions. Not applicable.

### Sensitive-pattern check
`git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches for this change.

### Documentation currency
The new endpoint `/api/v2/sbom/{id}/advisory-summary` would need to be added to `docs/api.md` if it documents all REST endpoints. Since the task has no Documentation Updates section, would check `docs/api.md` and update if it lists endpoints.

### Duplication check
Search for existing severity aggregation logic -- grep for `severity_summary`, `SeveritySummary`, `severity.*count`, `advisory.*summary` in the repository. Ensure no existing utility provides this aggregation.

### Symbol deduplication
Before declaring `SeveritySummary` struct, search the package for existing definitions. Search for `SeveritySummary`, `severity_summary`, `AdvisorySeverity` to ensure no collision.

### Contract and sibling parity
- **Contract**: AdvisoryService methods follow `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>` pattern. New method conforms.
- **Sibling parity**: Compare `severity_summary` method structure with `fetch` and `list` methods for consistent error handling, logging, transaction usage.
- **Cross-module entity**: `sbom_advisory` join table is read-only for this use case. Check other modules that read from it for consistent query patterns.
- **Caller-site**: New endpoint follows same handler pattern as `get.rs` and `list.rs`.

### CI checks from CONVENTIONS.md
If CONVENTIONS.md contains CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo check`), run each one. Hard stop on any failure.

### Module-level test (Rust)
Run `cargo metadata --no-deps --format-version 1` to resolve the crate name for `modules/fundamental/`. The package name from Cargo.toml (likely `trustify-module-fundamental` or similar) is used:
```
cargo test -p <resolved-crate-name>
```
Hard stop on any test failure.

### Query-scope verification
The query targets advisories linked to a specific SBOM via `sbom_advisory` join table, filtered by `sbom_id`. This correctly scopes to the requested SBOM -- no broad query issue.

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
vulnerability advisory severity counts (critical, high, medium, low,
total) for a given SBOM. Includes SeveritySummary model, service
method, endpoint handler, and integration tests.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

### Fork detection

Run `git remote get-url upstream 2>/dev/null` to detect fork. Adjust PR creation command accordingly.

### Branch push and PR creation

```
git push -u origin TC-9201
```

If no fork detected:
```
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

- Add GET /api/v2/sbom/{id}/advisory-summary endpoint returning advisory severity counts per SBOM
- Implements SeveritySummary model, AdvisoryService::severity_summary method, and endpoint handler
- Includes integration tests for valid SBOM, non-existent SBOM (404), empty advisory list, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [ ] Verify GET /api/v2/sbom/{id}/advisory-summary returns correct counts for SBOM with known advisories
- [ ] Verify 404 response for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no advisories
- [ ] Verify deduplication of advisory links in severity count
- [ ] Verify response time acceptable for SBOM with many advisories
EOF
)"
```

If GitHub Issue custom field was populated, would append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (customfield_10875) with the PR URL using ADF inlineCard format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add Jira comment** with PR link, summary of changes, and any deviations. Comment ends with footnote from `comment-footnote.md` using ADF contentFormat, with skill name `implement-task` and version read from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.

3. **Transition** to In Review:
   ```
   jira.transition_issue(TC-9201) -> In Review
   ```
