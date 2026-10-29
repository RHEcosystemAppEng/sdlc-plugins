# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Bookend Type**: None
**Target PR**: None
**Dependencies**: None

## Workflow Steps Executed

### Step 0 -- Validate Project Configuration

Project Configuration validated in CLAUDE.md:
- Repository Registry: present, contains `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: present, contains Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present, with tool naming convention `mcp__<serena-instance>__<tool>`

### Step 0.5 -- JIRA Access Initialization

Would use MCP (`jira.get_issue("TC-9201")`) as primary access method. REST API fallback available if MCP fails.

### Step 1 -- Fetch and Parse Jira Task

Parsed structured description:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add severity aggregation service and REST endpoint for SBOM advisory severity counts
- **Files to Modify**: 4 files (advisory.rs service, endpoints/mod.rs, model/mod.rs, main.rs)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: GET /api/v2/sbom/{id}/advisory-summary (new)
- **Acceptance Criteria**: 5 items
- **Test Requirements**: 4 items
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None
- **GitHub Issue custom field**: customfield_10747 (would check for linked GitHub issue)
- **Git Pull Request custom field**: customfield_10875 (for PR link update in Step 11)

### Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments("TC-9201")` and search for comments starting with `[sdlc-workflow] Description digest:`. Would compute digest using `python3 scripts/sha256-digest.py` and compare format tags and hex digests. If no digest comment found, log warning and proceed (backward compatibility).

### Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

### Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue("TC-9201", assignee=<account-id>)` to assign
3. `jira.transition_issue("TC-9201")` to "In Progress"

### Step 4 -- Understand the Code

Would use Serena instance `serena_backend` (from Repository Registry) to inspect:
1. `mcp__serena_backend__get_symbols_overview` on files to modify
2. `mcp__serena_backend__find_symbol` on `AdvisoryService`, `AdvisorySummary`, existing endpoint handlers
3. `mcp__serena_backend__find_referencing_symbols` on any symbols being modified
4. `mcp__serena_backend__search_for_pattern` for `sbom_advisory` join table usage
5. Sibling analysis on 2-3 sibling files (see conventions.md)
6. Check for `CONVENTIONS.md` at repository root (present per repo structure)
7. Identify documentation files: `docs/api.md`, `docs/architecture.md`, `README.md`

### Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6 -- Implement Changes

See file-N-description.md files for detailed changes per file.

**Files to Modify:**
1. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
2. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
3. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
4. `server/src/main.rs` -- no changes needed (routes auto-mount)

**Files to Create:**
5. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
6. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
7. `tests/api/advisory_summary.rs` -- integration tests

### Step 7 -- Write Tests

Integration tests in `tests/api/advisory_summary.rs` covering all 4 test requirements:
1. Valid SBOM with known advisories returns correct severity counts
2. Non-existent SBOM ID returns 404
3. SBOM with no advisories returns all zeros
4. Duplicate advisory links are deduplicated in the count

All tests follow skill guidance: doc comments on every test function, given-when-then section comments for non-trivial tests, value-based assertions on response body fields.

### Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- satisfied by endpoint implementation
- [x] Returns 404 when SBOM ID does not exist -- satisfied by service method checking SBOM existence first
- [x] Counts only unique advisories (deduplicates by advisory ID) -- satisfied by using DISTINCT in query or HashSet deduplication
- [x] All severity levels default to 0 when no advisories exist at that level -- satisfied by SeveritySummary::default() initialization
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- satisfied by single SQL query with GROUP BY (no N+1)

### Step 9 -- Self-Verification

Would perform:
- **Scope containment**: `git diff --name-only` compared against Files to Modify and Files to Create
- **Untracked file check**: `git status --short` to verify no unexpected files
- **Dead parameter detection**: Scan modified functions for unused parameters
- **Sensitive-pattern check**: `git diff --cached | grep -iE '(password|API_KEY|SECRET_KEY|PRIVATE KEY|\.env)'`
- **Documentation currency**: Check if `docs/api.md` needs updating for new endpoint
- **CI checks from CONVENTIONS.md**: Run all verification commands extracted from CONVENTIONS.md
- **Module-level test requirement (Rust)**: `cargo test -p trustify-fundamental` (or equivalent crate name from `cargo metadata`)
- **Data-flow trace**: Input (HTTP GET with SBOM ID) -> Processing (service queries sbom_advisory join, groups by severity, deduplicates) -> Output (JSON response with counts). All stages connected.
- **Contract & sibling parity**: Verify handler follows same pattern as `get.rs`, service method follows `fetch`/`list` pattern, error handling uses `AppError` with `.context()`
- **Duplication check**: Search for existing severity counting logic in the codebase

### Step 10 -- Commit and Push

Would commit, push, and create PR.

### Step 11 -- Update Jira

Would update Jira custom field `customfield_10875` with PR URL, add comment with PR link and change summary, transition to "In Review".

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to an SBOM. Includes deduplication by advisory ID
and proper 404 handling for non-existent SBOMs.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

## PR Description

```
## Summary
- Add `SeveritySummary` response model with counts per severity level
- Add `severity_summary` service method to `AdvisoryService` that queries the `sbom_advisory` join table and aggregates by severity
- Add GET `/api/v2/sbom/{id}/advisory-summary` endpoint with proper error handling
- Add integration tests covering valid counts, 404, empty results, and deduplication

## Test plan
- [ ] Verify GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape
- [ ] Verify 404 response for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no advisories
- [ ] Verify deduplication of advisory links
- [ ] Run `cargo test -p <crate-name>` to confirm all tests pass

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```
