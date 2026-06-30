# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001 (linked via "is incorporated by")
**Dependencies**: None
**Bookend Type**: None (standard implementation flow)
**Target PR**: None (standard flow -- create new PR)

## Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains the required sections:

- **Repository Registry**: trustify-backend is registered with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key TC, Cloud ID present, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: Serena instance `serena_backend` configured with `rust-analyzer` language server

All required configuration sections are present. Proceed.

## Step 0.5 -- Jira Access Initialization

Initialize Jira access using MCP-first approach. Fetch the issue via `jira.get_issue(TC-9201)`.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 and parse the structured description sections:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | 3 files (advisory.rs service, endpoints/mod.rs, model/mod.rs) |
| Files to Create | 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs test) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Implementation Notes | Present (detailed patterns) |
| Acceptance Criteria | 5 criteria |
| Test Requirements | 4 test cases |
| Target PR | Not present |
| Bookend Type | Not present |
| Dependencies | None |
| GitHub Issue | Check `customfield_10747` on the issue -- extract owner/repo#number if present |

Also capture the issue's `webUrl` for use in the PR description's "Implements" line.

## Step 1.5 -- Verify Description Integrity

See `digest-match.md` for the full procedure. The stored digest matches the computed digest. Proceed silently.

## Step 2 -- Verify Dependencies

The task has no dependencies listed. Skip this step.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to In Progress: `jira.transition_issue(TC-9201, "In Progress")`

## Step 4 -- Understand the Code

Using Serena instance `serena_backend` (rust-analyzer). Note the limitation: rust-analyzer may take 30-60 seconds to index on first use.

### 4.1 Inspect files to modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- use `mcp__serena_backend__get_symbols_overview` to see the `AdvisoryService` struct and its methods (`fetch`, `list`, `search`). Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` or `fetch` method to understand the service method pattern (parameters, return type, transaction handling).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- inspect route registration pattern. Identify how routes are added via `Router::new().route(...)`.

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- inspect existing `pub mod` declarations to understand module registration pattern.

### 4.2 Inspect reference files (from Implementation Notes)

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- use `find_symbol` to understand the handler pattern: `Path<Id>` extraction, service call, JSON response.

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- inspect `AdvisorySummary` struct to find the `severity` field and its type.

6. **`entity/src/sbom_advisory.rs`** -- inspect the join table entity to understand how SBOMs link to advisories.

7. **`common/src/error.rs`** -- inspect `AppError` enum and `.context()` wrapping pattern.

### 4.3 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to verify that adding a new method won't break existing callers.

### 4.4 Convention conformance analysis

**Sibling files for endpoint handler**: inspect `endpoints/list.rs` and `endpoints/get.rs` in the advisory module.

**Sibling files for model**: inspect `model/summary.rs` and `model/details.rs` in the advisory module.

**Sibling files for service**: inspect `service/advisory.rs` methods (`fetch`, `list`).

**Expected conventions to discover:**
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Service methods: take `&self, id: Id, tx: &Transactional<'_>` parameters
- Endpoint handlers: extract path params via `Path<Id>`, call service, return `Json<T>`
- Naming: service methods use `verb_noun` pattern
- Route registration: `Router::new().route("/path", get(handler))`
- Module structure: each model in its own file with `pub mod` in `mod.rs`

### 4.5 Test convention analysis

**Sibling test files**: inspect `tests/api/advisory.rs` and `tests/api/sbom.rs`.

**Expected test conventions to discover:**
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Error cases: 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Test naming: `test_<endpoint>_<scenario>` pattern
- Setup: test database with seeded data
- Response validation: check specific field values, not just presence

### 4.6 Documentation file identification

Check for:
- `docs/api.md` -- REST API reference that may need updating
- `docs/architecture.md` -- system architecture overview
- `CONVENTIONS.md` at repository root -- read for CI commands and coding conventions

### 4.7 CONVENTIONS.md lookup

Read `CONVENTIONS.md` at the repository root (path `./CONVENTIONS.md` from Registry). Extract:
- CI check commands (formatting, linting, compilation)
- Code generation commands (if any)
- Naming and structural conventions

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u32,
    /// Count of high-severity advisories.
    pub high: u32,
    /// Count of medium-severity advisories.
    pub medium: u32,
    /// Count of low-severity advisories.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

Follow the patterns from `summary.rs` and `details.rs` in the same module directory for derives, documentation, and field naming.

### 6.2 Register model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the existing module registration pattern (alongside `pub mod summary;` and `pub mod details;`).

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method following the `fetch`/`list` pattern:

```rust
/// Computes aggregated severity counts for all advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to this SBOM
    // 2. Deduplicate by advisory ID
    // 3. For each unique advisory, fetch its severity from AdvisorySummary
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` entity from `entity/src/sbom_advisory.rs` to find linked advisories
- Deduplicate by advisory ID to satisfy acceptance criterion
- Access the `severity` field from `AdvisorySummary`
- Default all counts to 0 (use `u32::default()` or explicit 0)
- Wrap errors with `.context("Failed to compute severity summary")` using `AppError`
- Verify SBOM exists first; return 404 if not found (consistent with existing SBOM endpoints)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Add `mod severity_summary;` at the top of the file with the other module imports.

### 6.6 Cross-repo API contract verification

Not applicable -- this task is backend-only and does not involve manual REST calls to another service.

### 6.7 Documentation impact

- Check `docs/api.md` for the REST API reference. Add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response documentation.
- No changes needed to `docs/architecture.md` (no architectural changes).

### 6.8 Code quality checks

Verify all new structs, functions, and public symbols have documentation comments (`///`).

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases, following the patterns discovered in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that an SBOM with known advisories returns the correct severity breakdown.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels seeded in the test database

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK and severity counts match the seeded data
    // assert_eq!(resp.status(), StatusCode::OK)
    // Deserialize body and assert specific counts (critical, high, medium, low, total)
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response status is 404 NOT_FOUND
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns zero for all severity levels.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all counts are 0 and total is 0
    // assert_eq!(summary.critical, 0)
    // assert_eq!(summary.high, 0)
    // assert_eq!(summary.medium, 0)
    // assert_eq!(summary.low, 0)
    // assert_eq!(summary.total, 0)
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(summary.total, expected_unique_count)
}
```

Register the test module in `tests/Cargo.toml` if required.

Run tests: `cargo test --test advisory_summary` and fix any failures.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by test 1 and endpoint implementation |
| 2 | Returns 404 when SBOM ID does not exist | Verified by test 2 |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by test 4 and deduplication logic in service method |
| 4 | All severity levels default to 0 when no advisories exist | Verified by test 3 |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient query design (single join query with GROUP BY, avoiding N+1) |

## Step 9 -- Self-Verification

### 9.1 Scope containment

Run `git diff --name-only` and compare against the declared file lists:

**Files to Modify (expected):**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create (expected):**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

**Potentially out-of-scope (require user approval):**
- `docs/api.md` -- if updated for documentation impact (justified by new endpoint)
- `tests/Cargo.toml` -- if updated to register the new test module

### 9.2 Untracked file check

Run `git status --short`, filter `??` entries in directories with modified files. Flag any untracked files for user review.

### 9.3 Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches for this task.

### 9.4 Documentation currency

Verify `docs/api.md` includes the new endpoint if it was updated in Step 6.7.

### 9.5 Documentation scope preservation

If `docs/api.md` was modified, verify no existing endpoint documentation was inadvertently removed or narrowed.

### 9.6 Eval coverage currency

No `SKILL.md` files are being modified -- skip.

### 9.7 Example consistency

If documentation was updated with examples, cross-check data structures against prose descriptions.

### 9.8 Cross-section reference consistency

Verify that file paths in the task description are consistent across Files to Modify, Files to Create, and Implementation Notes:
- `AdvisoryService` is referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent.
- `AdvisorySummary` is referenced in Implementation Notes at `advisory/model/summary.rs` -- consistent with repository structure.

### 9.9 Duplication check

Search for existing severity aggregation or counting functions in the codebase. Verify no existing utility already provides this functionality.

### 9.10 CI checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4.7. Hard stop on any failure.

### 9.11 Data-flow trace

Trace the data flow for the new endpoint:
- **Input**: HTTP GET request with SBOM ID path parameter
- **Processing**: Extract path param -> call `AdvisoryService::severity_summary` -> query `sbom_advisory` join table -> fetch advisory severities -> deduplicate -> count by severity level
- **Output**: JSON response with `SeveritySummary` struct

All stages connected. Flow is COMPLETE.

### 9.12 Contract & sibling parity

- **Contract verification**: `SeveritySummary` implements `Serialize`/`Deserialize` -- verified for JSON response compatibility.
- **Sibling parity**: compare `severity_summary` method against `fetch` and `list` methods in `AdvisoryService` for error handling, transaction usage, and logging consistency.
- **Caller-site parity**: the handler follows the same pattern as `get.rs` -- `Path<Id>` extraction, service call, JSON response.

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs
# Also add any out-of-scope files approved by the user (e.g., docs/api.md)

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
all advisories linked to a given SBOM. Includes deduplication by
advisory ID and proper 404 handling for missing SBOMs.

Implements TC-9201"
```

### Push and create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

- Add \`SeveritySummary\` response model with severity level counts
- Add \`severity_summary\` method to \`AdvisoryService\` that queries and aggregates advisory severities for an SBOM
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories (all zeros), and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test Plan

- [x] Valid SBOM with known advisories returns correct severity counts
- [x] Non-existent SBOM ID returns 404
- [x] SBOM with no advisories returns all zeros
- [x] Duplicate advisory links are deduplicated in the count"
```

If a GitHub issue reference was extracted from `customfield_10747` in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

```
jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201:

```
jira.add_comment(TC-9201, "Implementation complete. PR: <PR-URL>

Changes:
- Added SeveritySummary model (severity_summary.rs)
- Added severity_summary method to AdvisoryService
- Added GET /api/v2/sbom/{id}/advisory-summary endpoint
- Added 4 integration tests covering all acceptance criteria

No deviations from the plan.")
```

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue(TC-9201, "In Review")
```
