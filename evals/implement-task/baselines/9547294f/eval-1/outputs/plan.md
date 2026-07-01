# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Status**: To Do
**Parent Feature**: TC-9001

## Step 0 -- Validate Project Configuration

Project Configuration verified in CLAUDE.md:
- Repository Registry: present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`
- Jira Configuration: present, includes Project key (`TC`), Cloud ID, Feature issue type ID (`10142`), Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
- Code Intelligence: present, tool naming convention documented, `serena_backend` instance configured with `rust-analyzer`

All required sections are present. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

### Parsed Sections

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
  - `tests/api/advisory_summary.rs` -- integration tests for the new endpoint
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`, add method to AdvisoryService following `fetch`/`list` pattern, use `sbom_advisory` join table, use `AdvisorySummary.severity` field, register route in `endpoints/mod.rs`, return `AppError` with `.context()`, return struct directly via Axum `Json`
- **Acceptance Criteria**: 5 criteria (see task description)
- **Test Requirements**: 4 test cases (see task description)
- **Target PR**: none
- **Bookend Type**: none
- **Dependencies**: none

### Target Branch

`main` -- standard direct-to-main workflow.

### GitHub Issue

Would check `customfield_10747` on the fetched Jira issue. If present, extract the GitHub issue URL and parse owner/repo/number for use in the PR description.

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9201)`, search for digest comment starting with `[sdlc-workflow] Description digest:`, and if found, compute SHA-256 digest of the description and compare. If no digest comment is found, log warning and proceed.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code

### Code Inspection Plan

Use Serena instance `serena_backend` (from Repository Registry) to inspect:

1. **`modules/fundamental/src/advisory/service/advisory.rs`**: Use `mcp__serena_backend__get_symbols_overview` to see AdvisoryService methods (`fetch`, `list`, `search`). Then `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` to understand the method signature pattern and how it uses `Transactional`.

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**: Use `mcp__serena_backend__get_symbols_overview` to see route registration pattern. Inspect how existing routes are mounted.

3. **`modules/fundamental/src/advisory/endpoints/get.rs`**: Use `mcp__serena_backend__find_symbol` to read the GET handler -- understand path param extraction via `Path<Id>`, service call pattern, JSON return.

4. **`modules/fundamental/src/advisory/model/mod.rs`**: Check current module registrations.

5. **`modules/fundamental/src/advisory/model/summary.rs`**: Use `mcp__serena_backend__find_symbol` on `AdvisorySummary` to see the `severity` field type.

6. **`entity/src/sbom_advisory.rs`**: Inspect the join table entity to understand columns and relationships.

7. **`common/src/error.rs`**: Inspect `AppError` to understand error handling pattern.

8. **`common/src/model/paginated.rs`**: Inspect `PaginatedResults<T>` for reference (this endpoint does not paginate, but good to understand the pattern).

### Sibling Analysis (Convention Conformance)

**Sibling endpoint files**: `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`
**Sibling model files**: `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs`
**Sibling service files**: `modules/fundamental/src/advisory/service/advisory.rs` (the same file being modified)
**Sibling module patterns**: `modules/fundamental/src/sbom/` (parallel domain module)

### Test Convention Analysis

**Sibling test files**: `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`
Inspect these to understand assertion patterns, test naming, setup/teardown, and error case coverage.

### CONVENTIONS.md Lookup

The repository structure indicates a `CONVENTIONS.md` at the root. Would read it to extract:
- CI check commands (for Step 9)
- Code generation commands
- Any project-specific naming or structural rules

### Documentation Files Identified

- `README.md` at repository root
- `docs/architecture.md` -- system architecture overview
- `docs/api.md` -- REST API reference (likely needs updating with new endpoint)

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

Standard flow: no Target PR, no Bookend Type.

## Step 6 -- Implement Changes

### Files to Modify

1. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;`
2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method
3. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register new route

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler
3. **`tests/api/advisory_summary.rs`** -- integration tests

See `file-1-description.md` through `file-6-description.md` for detailed changes per file.

## Step 7 -- Write Tests

Integration tests in `tests/api/advisory_summary.rs` covering all 4 test requirements:
1. Valid SBOM with known advisories returns correct severity counts
2. Non-existent SBOM ID returns 404
3. SBOM with no advisories returns all zeros
4. Duplicate advisory links are deduplicated in the count

See `file-6-description.md` for detailed test implementations.

## Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- satisfied by the SeveritySummary struct and handler implementation
- [x] Returns 404 when SBOM ID does not exist -- satisfied by checking SBOM existence before querying advisories, returning AppError::NotFound
- [x] Counts only unique advisories (deduplicates by advisory ID) -- satisfied by using DISTINCT in the query or collecting into a HashSet by advisory ID
- [x] All severity levels default to 0 when no advisories exist at that level -- satisfied by initializing all counts to 0 in SeveritySummary::default()
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- satisfied by performing aggregation in a single SQL query rather than loading all advisories into memory

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all changed files are within the Files to Modify and Files to Create lists. Expected files:
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)

If `docs/api.md` is updated (documentation impact), flag as out-of-scope and request user approval.

### Untracked file check
Run `git status --short` and check for `??` entries in directories where implementation work occurred.

### Sensitive-pattern check
Run grep on staged diff for passwords, API keys, secrets, private keys, .env references.

### Documentation currency
Check if `docs/api.md` needs updating with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from CONVENTIONS.md.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> aggregate by severity -> return `SeveritySummary` as JSON -- **COMPLETE**

### Contract & sibling parity
- `severity_summary` handler follows the same `Result<T, AppError>` pattern as `get.rs` and `list.rs`
- Error handling uses `.context()` wrapping matching sibling handlers
- Response serialization uses Axum `Json` extractor like siblings

### Duplication check
Search for existing severity aggregation logic in the codebase to avoid duplicating functionality.

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service
method, handler, and integration tests.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

### PR Creation

```
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR description would include:
- Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
- Summary of changes
- Closes reference if GitHub issue exists on the Jira task

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format
2. Add comment to TC-9201 with PR link and summary of changes (with plugin version footer)
3. Transition TC-9201 to "In Review"
