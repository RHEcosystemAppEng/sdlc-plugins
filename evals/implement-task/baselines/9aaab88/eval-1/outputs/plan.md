# Implementation Plan for TC-9201

## Task Summary

**Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Status**: To Do
**Parent**: TC-9001
**Repository**: trustify-backend
**Target Branch**: main
**Bookend Type**: None
**Target PR**: None

## Step 0 - Project Configuration Validation

PASSED. All required sections present in CLAUDE.md:
- Repository Registry with `trustify-backend` mapped to `serena_backend`
- Jira Configuration with Project key TC, Cloud ID, Feature issue type ID
- Code Intelligence with tool naming convention and serena_backend instance

## Step 1 - Task Parsing

### Parsed Sections
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity summary model, severity summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes**: Present with detailed patterns
- **Acceptance Criteria**: 5 items
- **Test Requirements**: 4 test cases
- **Dependencies**: None
- **GitHub Issue custom field**: customfield_10747 (would check for value)
- **webUrl**: Would capture from Jira API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`)

### Validation
All required sections are present. No missing information. Proceed.

## Step 1.5 - Description Integrity Verification

Would fetch comments via `jira.get_issue_comments(TC-9201)` and search for `[sdlc-workflow] Description digest:` marker. Compare stored digest with computed digest using `scripts/sha256-digest.py`. Since this is an eval, we note this step would be performed.

## Step 2 - Dependency Verification

Dependencies: None. Proceed.

## Step 3 - Transition to In Progress

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9201)` to "In Progress"

## Step 4 - Understand the Code

### Serena Instance
Using `serena_backend` (from Repository Registry). Tools called as `mcp__serena_backend__<tool>`.

### Files to Inspect

**Files to Modify:**
1. `modules/fundamental/src/advisory/service/advisory.rs` - Would use `mcp__serena_backend__get_symbols_overview` to see existing `AdvisoryService` methods (`fetch`, `list`, `search`), then `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method to understand the query pattern and return type.
2. `modules/fundamental/src/advisory/endpoints/mod.rs` - Would inspect route registration patterns using `get_symbols_overview`.
3. `modules/fundamental/src/advisory/model/mod.rs` - Would inspect to see existing `pub mod` declarations.

**Sibling Files for Convention Analysis:**
1. `modules/fundamental/src/advisory/endpoints/get.rs` - Primary sibling for the new endpoint handler. Would inspect via `get_symbols_overview` to understand: path param extraction pattern, service call pattern, response wrapping.
2. `modules/fundamental/src/advisory/endpoints/list.rs` - Secondary sibling for endpoint patterns.
3. `modules/fundamental/src/advisory/model/summary.rs` - Sibling for the new model struct. Would inspect `AdvisorySummary` to understand: field types, derive macros, the `severity` field structure.
4. `modules/fundamental/src/advisory/model/details.rs` - Secondary sibling for model patterns.
5. `modules/fundamental/src/sbom/endpoints/get.rs` - Cross-module sibling for SBOM-scoped endpoint patterns (since the new endpoint is under `/api/v2/sbom/{id}/...`).

**Entity Files:**
1. `entity/src/sbom_advisory.rs` - Would inspect the join table structure to understand how to query advisories linked to an SBOM.
2. `entity/src/advisory.rs` - Would inspect the advisory entity for available fields.

**Backward Compatibility Check:**
- Would use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to see all callers and ensure the new `severity_summary` method doesn't conflict.

**Documentation Files Identified:**
- `README.md` (repository root)
- `docs/api.md` (API reference)
- `docs/architecture.md` (system architecture)
- `CONVENTIONS.md` (repository root - conventions)

### Cross-Section Reference Consistency

Checking entity-to-file-path consistency across task description sections:

- **AdvisoryService** - Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs` / Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- **SeveritySummary** - Files to Create: `modules/fundamental/src/advisory/model/severity_summary.rs` -- only referenced in one section, consistent
- **Endpoint handler** - Files to Create: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` / Implementation Notes reference pattern from `modules/fundamental/src/advisory/endpoints/get.rs` -- CONSISTENT (different files, one is sibling reference)
- **Route registration** - Files to Modify: `modules/fundamental/src/advisory/endpoints/mod.rs` / Implementation Notes: `modules/fundamental/src/advisory/endpoints/mod.rs` -- CONSISTENT
- **Model module** - Files to Modify: `modules/fundamental/src/advisory/model/mod.rs` -- CONSISTENT
- **AdvisorySummary** - Implementation Notes: `modules/fundamental/src/advisory/model/summary.rs` -- CONSISTENT with repo structure

Result: All cross-section references are consistent.

## Step 5 - Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 - Implement Changes

### Files to Create (3 files)

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** - New SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** - GET handler for the new endpoint
3. **`tests/api/advisory_summary.rs`** - Integration tests (implemented in Step 7)

### Files to Modify (3 files)

4. **`modules/fundamental/src/advisory/service/advisory.rs`** - Add `severity_summary` method
5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** - Register the new route
6. **`modules/fundamental/src/advisory/model/mod.rs`** - Register the new model module

### Detailed changes per file: see `outputs/file-N-description.md`

## Step 7 - Write Tests

See `outputs/file-3-description.md` for test implementation details.

Would run: `cargo test` to verify all tests pass.

## Step 8 - Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by endpoint implementation returning `SeveritySummary` struct with all fields, and by `test_advisory_summary_valid_sbom` |
| 2 | Returns 404 when SBOM ID does not exist | Verified by checking SBOM existence before querying advisories, returning `AppError::NotFound`, and by `test_advisory_summary_nonexistent_sbom` |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by using `HashSet` or `.distinct()` in the query to deduplicate by advisory ID, and by `test_advisory_summary_deduplication` |
| 4 | All severity levels default to 0 when no advisories exist | Verified by initializing all counts to 0 in `SeveritySummary::default()`, and by `test_advisory_summary_no_advisories` |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by using a single aggregation query rather than N+1 fetches; would confirm with load testing |

## Step 9 - Self-Verification

### Scope Containment
Expected modified/created files:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)
- `tests/api/advisory_summary.rs` (CREATE)
- `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)
- `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

All within scope of Files to Modify and Files to Create. No out-of-scope changes.

### Untracked File Check
New files (`severity_summary.rs`, `advisory_summary.rs`) would appear as untracked. All are listed in Files to Create -- would stage for commit.

### Sensitive Pattern Check
Would run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation Currency
- The new `GET /api/v2/sbom/{id}/advisory-summary` endpoint should be documented in `docs/api.md` if it lists API endpoints. Would check and update if needed.
- No changes to configuration or setup steps.

### Data-Flow Trace
- `GET /api/v2/sbom/{id}/advisory-summary` request -> Axum path extraction (`Path<Id>`) -> `severity_summary` endpoint handler -> `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> count by severity from `AdvisorySummary.severity` field -> build `SeveritySummary` response -> return `Json(summary)` -- **COMPLETE**

### Contract & Sibling Parity
- `SeveritySummary` struct: standalone response type, no trait implementation required
- Sibling parity with `get.rs` endpoint: path extraction pattern, service call pattern, error handling pattern -- all would match
- Sibling parity with `AdvisorySummary` model: derive macros, field documentation -- all would match

### Duplication Check
- Would search for existing severity aggregation logic in the codebase. No known duplicates based on repo structure analysis.

### CI Checks
- Would read `CONVENTIONS.md` and run any CI check commands found. Fall back to `cargo build && cargo clippy && cargo test` if no specific CI section.

## Step 10 - Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService::severity_summary method, and integration tests.

Implements TC-9201
```

### Branch and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

PR description would include:
- Summary of changes
- `Implements [TC-9201](<webUrl>)` with clickable link
- `Closes <owner>/<repo>#<number>` if GitHub Issue custom field has a value

## Step 11 - Update Jira

1. Update `customfield_10875` (Git Pull Request) with PR URL in ADF format
2. Add comment with PR link, summary of changes, and any deviations
3. Transition TC-9201 to "In Review"
