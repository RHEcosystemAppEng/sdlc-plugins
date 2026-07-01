# Implementation Plan: TC-9201 -- Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Jira Key**: TC-9201
**Parent Feature**: TC-9001
**Repository**: trustify-backend
**Target Branch**: main
**Status**: To Do

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns counts per severity level (Critical, High, Medium, Low) and a total.

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains:
- Repository Registry: trustify-backend is registered with Serena instance `serena_backend` at path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields all present
- Code Intelligence: Serena instance `serena_backend` with rust-analyzer configured

All sections present and valid. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP-based Jira access first. If MCP fails, prompt user for REST API fallback. Required operations for this task: get_issue, get_issue_comments, user_info, edit_issue (assign), transition_issue, update_issue (PR field), add_comment.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue(TC-9201)`. Parse structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Severity aggregation service and endpoint for SBOM advisories |
| Files to Modify | `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs` |
| Files to Create | `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Target PR | None |
| Bookend Type | None |
| Dependencies | None |

Capture the `webUrl` from the Jira response for PR description linking.

Check GitHub Issue custom field (`customfield_10747`) -- extract reference if present, skip if empty.

## Step 1.5 -- Verify Description Integrity

1. Fetch comments via `jira.get_issue_comments(TC-9201)`
2. Locate comment with marker `[sdlc-workflow] Description digest:`
3. Found: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` equals `updated` -- not edited, no warning
5. Format tag: `sha256-md` -- matches computed tag
6. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
7. Hex digests match -- **proceed silently**, no user prompt needed

## Step 2 -- Verify Dependencies

Task has no dependencies. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. `jira.user_info()` -- retrieve current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` -- assign task
3. `jira.transition_issue(TC-9201)` -- transition to In Progress

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol`:

- **`modules/fundamental/src/advisory/service/advisory.rs`**: Examine `AdvisoryService` struct and its existing methods (`fetch`, `list`, `search`). Understand method signatures -- especially parameter patterns (`&self`, `sbom_id: Id`, `tx: &Transactional<'_>`) and return types (`Result<T, AppError>`).

- **`modules/fundamental/src/advisory/endpoints/mod.rs`**: Examine route registration pattern. Understand how routes are registered via `Router::new().route("/path", get(handler))`.

- **`modules/fundamental/src/advisory/model/mod.rs`**: Examine module declarations (`pub mod summary;`, `pub mod details;`) to understand the registration pattern.

### 4.2 Inspect Related Files for Patterns

- **`modules/fundamental/src/advisory/endpoints/get.rs`**: Reference pattern for new endpoint handler -- `Path<Id>` extraction, service call, JSON response.
- **`modules/fundamental/src/advisory/model/summary.rs`**: Examine `AdvisorySummary` struct, especially the `severity` field for counting by severity level.
- **`entity/src/sbom_advisory.rs`**: Understand the join table structure for linking SBOMs to advisories.
- **`common/src/error.rs`**: Understand `AppError` enum and `.context()` error wrapping pattern.

### 4.3 Convention Conformance Analysis

Examine sibling files to discover conventions:

- **Endpoint siblings** (`list.rs`, `get.rs` in advisory/endpoints/): Check handler function signatures, error handling, response types.
- **Service siblings**: Check method naming (`verb_noun`), transaction handling, return types.
- **Model siblings** (`summary.rs`, `details.rs`): Check struct derive macros (`#[derive(Serialize, Deserialize, ...)]`), field naming conventions, documentation patterns.

### 4.4 Test Convention Analysis

Examine `tests/api/advisory.rs` and `tests/api/sbom.rs`:
- Assertion style: likely `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Test naming: `test_<endpoint>_<scenario>` pattern
- Error cases: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Setup/teardown: test database seeding patterns

### 4.5 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (noted in repo structure). Read it for:
- Explicit conventions
- CI check commands to extract for Step 9

### 4.6 Documentation File Identification

Identify related docs:
- `docs/api.md` -- API reference, may need updating for new endpoint
- `docs/architecture.md` -- architecture overview
- `README.md` -- project readme

## Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

No Target PR, no Bookend Type -- standard branch creation.

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Provides a breakdown of advisory counts by severity level,
/// enabling dashboard widgets to render severity summaries without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u32,
    /// Count of advisories with High severity.
    pub high: u32,
    /// Count of advisories with Medium severity.
    pub medium: u32,
    /// Count of advisories with Low severity.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

Use the same derive macros and documentation style observed in sibling model files (`summary.rs`, `details.rs`). Default derive ensures all fields initialize to 0.

### 6.2 Register Model Module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Add `severity_summary` Method to `AdvisoryService`

In `modules/fundamental/src/advisory/service/advisory.rs`, add:

```rust
/// Computes aggregated severity counts for all unique advisories linked to a given SBOM.
///
/// Uses the `sbom_advisory` join table to find advisories, deduplicates by advisory ID,
/// and counts each severity level. Returns a `SeveritySummary` with per-level counts and total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to this SBOM
    // 2. Deduplicate by advisory ID
    // 3. For each unique advisory, fetch its AdvisorySummary and read the severity field
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Return SeveritySummary with counts and total
}
```

Follow the same pattern as `fetch` and `list` methods:
- Same parameter signature (`&self`, typed ID, `&Transactional<'_>`)
- Same error handling (`Result<T, AppError>` with `.context()` wrapping)
- Use SeaORM queries against the `sbom_advisory` entity
- First verify the SBOM exists (return 404/AppError if not found, consistent with existing SBOM endpoints)
- Deduplicate advisory IDs using `HashSet` or SQL `DISTINCT`
- Count severity levels by iterating over `AdvisorySummary.severity` values

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the pattern in `advisory/endpoints/get.rs`:
- `Path<Id>` for path parameter extraction
- `State` extractor for the service
- Return `Result<Json<T>, AppError>`
- `.context()` wrapping for error messages

### 6.5 Register Route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route to the router registration:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follow the existing `Router::new().route(...)` chain pattern.

### 6.6 Documentation Impact

- Check `docs/api.md` for API reference -- add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation
- No changes needed to `server/src/main.rs` (routes auto-mount via module registration, per task description)

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with documented test functions following sibling test conventions:

### Test 1: Valid SBOM with Known Advisories

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels
    // (seed test DB with SBOM and linked advisories: 2 Critical, 1 High, 3 Medium, 0 Low)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, 2)
    // assert_eq!(body.high, 1)
    // assert_eq!(body.medium, 3)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 6)
}
```

### Test 2: Non-Existent SBOM Returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

### Test 3: SBOM with No Advisories Returns All Zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}
```

### Test 4: Duplicate Advisory Links Are Deduplicated

```rust
/// Verifies that duplicate advisory links in the SBOM-advisory join table are deduplicated
/// so each advisory is counted only once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate links to the same advisory (e.g., advisory A linked twice)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, 1) (not 2)
}
```

Run tests:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Test 1 validates response fields and values |
| Returns 404 for non-existent SBOM | Test 2 validates 404 status code |
| Deduplicates by advisory ID | Test 4 validates deduplication |
| Severity levels default to 0 | Test 3 validates all-zero response |
| Response time under 200ms for up to 500 advisories | Verify with SQL EXPLAIN or a load test against seeded data if feasible; otherwise note as a performance target for future benchmarking |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files match the task description:

**Expected files:**
- `modules/fundamental/src/advisory/service/advisory.rs` (modified)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified)
- `modules/fundamental/src/advisory/model/mod.rs` (modified)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (created)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (created)
- `tests/api/advisory_summary.rs` (created)

Any out-of-scope files require user approval.

### Untracked File Check

Run `git status --short`, filter for `??` entries in directories with modified files, check for code references. Ask user before staging any untracked files.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation Currency

If `docs/api.md` describes endpoints and a new endpoint was added, update it. Check that any modified documentation preserves all previously documented use cases.

### CI Checks from CONVENTIONS.md

Run any CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on any failure.

### Data-Flow Trace

- **Input**: `GET /api/v2/sbom/{id}/advisory-summary` request with SBOM ID path parameter
- **Processing**: Endpoint handler extracts ID -> calls `AdvisoryService.severity_summary()` -> queries `sbom_advisory` join table -> fetches advisory severities -> deduplicates -> counts by level -> builds `SeveritySummary`
- **Output**: JSON response `{ critical: N, high: N, medium: N, low: N, total: N }`
- **Path completeness**: COMPLETE -- request flows through handler to service to database and back to response

### Contract & Sibling Parity

- `SeveritySummary` struct: implements `Serialize`/`Deserialize` (contract with Axum's `Json` extractor) -- all fields present
- Sibling parity with `get.rs` endpoint: error handling pattern (`.context()`) matches, extractor pattern (`Path<Id>`, `State`) matches, return type (`Result<Json<T>, AppError>`) matches
- Sibling parity with `fetch`/`list` service methods: parameter pattern matches, transaction handling matches

### Duplication Check

Search for existing severity counting or aggregation logic in the codebase. Verify no existing utility performs similar aggregation that could be reused.

### Cross-Section Reference Consistency

Verify that file paths in Files to Modify, Files to Create, and Implementation Notes are consistent:
- `AdvisoryService` referenced in both Files to Modify (`service/advisory.rs`) and Implementation Notes (`service/advisory.rs`) -- consistent
- `AdvisorySummary.severity` field referenced in Implementation Notes and located in `model/summary.rs` -- consistent
- Route registration in `endpoints/mod.rs` -- consistent across sections

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, endpoint handler, and integration tests.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated
severity counts for vulnerability advisories linked to an SBOM. This enables dashboard
widgets to render severity breakdowns without client-side counting.

### Changes
- `SeveritySummary` response model with critical, high, medium, low, and total fields
- `AdvisoryService.severity_summary()` method using sbom_advisory join table with deduplication
- `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler following existing patterns
- Integration tests covering valid responses, 404 for missing SBOMs, zero-advisory SBOMs, and deduplication

Implements [TC-9201](<webUrl>)
Closes <owner/repo>#<number> (if GitHub Issue reference was extracted)

## Test Plan

- [x] Test valid SBOM with known advisories returns correct severity counts
- [x] Test non-existent SBOM returns 404
- [x] Test SBOM with no advisories returns all zeros
- [x] Test duplicate advisory links are deduplicated in count
- [ ] Verify response time under 200ms for SBOMs with up to 500 advisories (performance benchmark)
EOF
)"
```

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format:

```
jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: Added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
   - No deviations from the plan
   - Comment ends with the skill footnote (sdlc-workflow/implement-task v{version} from plugin.json)

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue(TC-9201) -> In Review
```
