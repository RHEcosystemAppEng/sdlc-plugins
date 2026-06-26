# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

---

## Step 0 - Validate Project Configuration

The project CLAUDE.md contains all required sections:
1. **Repository Registry** - present with trustify-backend entry (Serena instance: serena_backend, path: ./)
2. **Jira Configuration** - present with Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** - present with serena_backend instance and rust-analyzer

Configuration is valid. Proceed.

## Step 1 - Fetch and Parse Jira Task

Parsed sections from TC-9201:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, returning counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` - add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` - register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` - add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` - no changes needed (routes auto-mount via module registration)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` - SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` - GET handler
  - `tests/api/advisory_summary.rs` - integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` - NEW endpoint
- **Acceptance Criteria**: 5 items (correct response shape, 404 for missing SBOM, deduplication, default zeros, performance)
- **Test Requirements**: 4 test cases
- **Dependencies**: None
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **GitHub Issue custom field**: customfield_10747 - would check the issue's fields for a GitHub issue URL

Captured `webUrl` for the Jira issue (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

## Step 1.5 - Verify Description Integrity

See `digest-match.md` for full details. Summary: The digest comment was found, timestamps show no editing, format tags match (both `sha256-md`), and hex digests match. Proceeding silently with no user prompt.

## Step 2 - Verify Dependencies

The task lists "Depends on: None". No dependency verification needed. Proceed.

## Step 3 - Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to the current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 - Understand the Code

### 4.1 Code inspection using Serena (serena_backend)

**Files to Modify - overview:**

1. `modules/fundamental/src/advisory/service/advisory.rs`:
   - Use `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its methods (fetch, list, search)
   - Use `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` or `list` methods to understand the service pattern (parameters: `&self, id, tx: &Transactional<'_>`)
   - Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers

2. `modules/fundamental/src/advisory/endpoints/mod.rs`:
   - Use `mcp__serena_backend__get_symbols_overview` to see route registration pattern
   - Understand how routes are registered using `Router::new().route("/path", get(handler))`

3. `modules/fundamental/src/advisory/model/mod.rs`:
   - Use `mcp__serena_backend__get_symbols_overview` to see existing module declarations

**Reference files for patterns:**

4. `modules/fundamental/src/advisory/endpoints/get.rs`:
   - Use `mcp__serena_backend__find_symbol` with `include_body=true` to read the GET handler pattern (Path<Id> extraction, service call, JSON return)

5. `modules/fundamental/src/advisory/model/summary.rs`:
   - Use `mcp__serena_backend__find_symbol` on `AdvisorySummary` to understand the `severity` field for counting

6. `entity/src/sbom_advisory.rs`:
   - Use `mcp__serena_backend__get_symbols_overview` to understand the SBOM-Advisory join table structure

7. `common/src/error.rs`:
   - Use `mcp__serena_backend__find_symbol` on `AppError` to understand error handling pattern with `.context()` wrapping

### 4.2 Convention conformance analysis

**Sibling files to inspect:**

- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` - endpoint siblings
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` - model siblings
- `modules/fundamental/src/sbom/service/sbom.rs` - service sibling from another module

**Expected discovered conventions:**

- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern**: Extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Response types**: Structs derive `Serialize, Deserialize` and use `utoipa::ToSchema`
- **Module registration**: Each model sub-module is registered in `model/mod.rs` with `pub mod <name>;`
- **Route registration**: Routes added in `endpoints/mod.rs` using `Router::new().route()`

### 4.3 Test convention analysis

**Sibling test files to inspect:**

- `tests/api/advisory.rs` - advisory endpoint tests
- `tests/api/sbom.rs` - SBOM endpoint tests

**Expected discovered test conventions:**

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: Validate response structure fields and specific values
- **Error cases**: Include 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: Tests use real PostgreSQL test database with fixture data

### 4.4 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract:
- CI check commands for Step 9
- Code generation commands
- Any additional naming or structural conventions

### 4.5 Documentation file identification

Identify documentation files related to the changes:
- `README.md` at repository root
- `docs/api.md` (API reference, if it exists) - may need updating for the new endpoint
- `docs/architecture.md` - system architecture overview

## Step 5 - Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 - Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u64,
    /// Number of high-severity advisories.
    pub high: u64,
    /// Number of medium-severity advisories.
    pub medium: u64,
    /// Number of low-severity advisories.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

Following conventions from sibling model files (`summary.rs`, `details.rs`): derive macros, doc comments, `utoipa::ToSchema` for OpenAPI.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module registration:

```rust
pub mod severity_summary;
```

### 6.3 Add `severity_summary` method to `modules/fundamental/src/advisory/service/advisory.rs`

Following the pattern of existing `fetch` and `list` methods:

```rust
/// Computes aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Deduplicate by advisory ID
    // For each unique advisory, fetch its AdvisorySummary and read the severity field
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find linked advisories
- Use `AdvisorySummary.severity` field to classify each advisory
- Deduplicate by advisory ID before counting (acceptance criterion)
- Default all counts to 0 when no advisories exist at a level (acceptance criterion)
- Return 404 via `AppError` when SBOM ID does not exist (acceptance criterion)
- Wrap errors with `.context()` following existing error handling patterns

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Following the pattern from `get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// GET handler for `/api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated severity counts for all advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following existing route registration patterns:

```rust
mod severity_summary;

// In the router builder:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation impact

- No Documentation Updates section in the task
- Check `docs/api.md` (if it exists) for API reference documentation - add the new endpoint
- `server/src/main.rs` requires no changes (routes auto-mount via module registration)

### 6.7 Code quality practices

- All new structs (`SeveritySummary`) have documentation comments
- All new public functions (`severity_summary`, `get_severity_summary`) have documentation comments
- Doc comments explain purpose, parameters, and behavior

## Step 7 - Write Tests

### Create `tests/api/advisory_summary.rs`

Following test conventions discovered in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

```rust
/// Verifies that the advisory summary endpoint returns correct severity counts
/// for an SBOM with known advisories.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test fixtures in PostgreSQL test database)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response should contain correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // Deserialize body and assert specific severity counts
    // Verify total equals sum of individual counts
}

/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 status code.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary

    // Then a 404 should be returned
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no linked advisories returns all severity
/// counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all counts should be zero
    // assert_eq!(summary.critical, 0)
    // assert_eq!(summary.high, 0)
    // assert_eq!(summary.medium, 0)
    // assert_eq!(summary.low, 0)
    // assert_eq!(summary.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated when computing
/// severity counts for an SBOM.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links in the sbom_advisory table

    // When requesting the advisory summary

    // Then each advisory should be counted only once
    // Assert that the total matches the number of unique advisories, not the
    // number of join table rows
}
```

All tests follow discovered conventions:
- `assert_eq!(resp.status(), StatusCode::...)` assertion pattern
- `test_<endpoint>_<scenario>` naming
- Doc comments on every test function
- Given-when-then section comments for non-trivial tests
- Value-based assertions (specific counts), not just length checks

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 - Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by `test_advisory_summary_valid_sbom` - response shape matches |
| Returns 404 when SBOM ID does not exist | Verified by `test_advisory_summary_nonexistent_sbom` |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_advisory_summary_deduplicates` |
| All severity levels default to 0 when no advisories exist | Verified by `test_advisory_summary_no_advisories` |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient query design using join table; would need load testing for full confirmation |

## Step 9 - Self-Verification

### Scope containment

Run `git diff --name-only` and verify all modified/created files are in scope:

**Expected files:**
- `modules/fundamental/src/advisory/service/advisory.rs` - in Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` - in Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` - in Files to Modify
- `modules/fundamental/src/advisory/model/severity_summary.rs` - in Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` - in Files to Create
- `tests/api/advisory_summary.rs` - in Files to Create

Any out-of-scope files would be flagged for user approval.

### Untracked file check

Run `git status --short`, filter `??` entries by proximity to modified directories, and search for code references to any untracked files.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to scan for secrets.

### Documentation currency

Check if `docs/api.md` needs updating for the new endpoint. If it describes existing endpoints and the new one is not yet documented, add it.

### Cross-section reference consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` - referenced in Files to Modify (`service/advisory.rs`) and Implementation Notes (`service/advisory.rs`) - consistent
- `SeveritySummary` - referenced in Files to Create (`model/severity_summary.rs`) and described in Implementation Notes - consistent
- Route registration - referenced in Files to Modify (`endpoints/mod.rs`) and Implementation Notes - consistent

### Duplication check

Search for existing severity aggregation or summary computation logic in the repository to avoid duplication. Use Grep/Serena to look for patterns like `severity_summary`, `severity_count`, or similar aggregation functions.

### CI checks from CONVENTIONS.md

Run any CI check commands extracted from CONVENTIONS.md. If none were found, run `cargo build` and `cargo clippy` as standard Rust checks.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract SBOM ID from path (input) -> call `AdvisoryService::severity_summary` (processing) -> query sbom_advisory join table -> count by severity -> return `Json<SeveritySummary>` (output) - **COMPLETE**

### Contract & sibling parity

- `SeveritySummary` derives `Serialize, Deserialize, ToSchema` matching sibling model structs
- `get_severity_summary` handler follows `Result<Json<T>, AppError>` contract matching sibling endpoints
- `severity_summary` service method follows `(&self, id, tx) -> Result<T, AppError>` pattern matching siblings
- Error handling uses `.context()` wrapping consistent with `common/src/error.rs` pattern

## Step 10 - Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes deduplication by advisory
ID and proper 404 handling for missing SBOMs.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM, enabling dashboard widgets to render severity
breakdowns without client-side counting.

### Changes
- Added \`SeveritySummary\` response struct in advisory model
- Added \`severity_summary\` method to \`AdvisoryService\`
- Added GET handler at \`/api/v2/sbom/{id}/advisory-summary\`
- Registered new route in advisory endpoints
- Added integration tests for all acceptance criteria

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If a GitHub issue reference was found in customfield_10747, append a `Closes <owner>/<repo>#<number>` line to the PR body.

## Step 11 - Update Jira

1. **Update Git Pull Request custom field** (customfield_10875) with the PR URL in ADF format:

```
jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added advisory severity aggregation endpoint with SeveritySummary model, AdvisoryService method, GET handler, and integration tests
   - No deviations from the plan

   Comment includes the skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`).

3. **Transition** TC-9201 to "In Review":

```
jira.transition_issue(TC-9201) -> In Review
```
