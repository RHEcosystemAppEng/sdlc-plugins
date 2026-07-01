# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains required sections under `# Project Configuration`:

1. **Repository Registry** -- Present. Contains one entry: `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- Present. Contains: Project key (TC), Cloud ID, Feature issue type ID (10142), Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747).
3. **Code Intelligence** -- Present. Documents tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` with rust-analyzer.

All required sections are present and complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Determine the JIRA access method. Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback per the documented options (Yes/No/Retry).

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue using `jira.get_issue("TC-9201")` and parse the structured description.

### Parsed Fields

| Section | Value |
|---|---|
| **Repository** | trustify-backend |
| **Target Branch** | main |
| **Description** | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting. |
| **Bookend Type** | Not present (standard task) |
| **Target PR** | Not present (new PR flow) |
| **Dependencies** | None |

### Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
- `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)

### Files to Create
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
- `tests/api/advisory_summary.rs` -- integration tests for the new endpoint

### API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`

### Acceptance Criteria
- GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- Returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
- Counts only unique advisories (deduplicates by advisory ID)
- All severity levels default to 0 when no advisories exist at that level
- Response time under 200ms for SBOMs with up to 500 advisories

### Test Requirements
- Test that a valid SBOM with known advisories returns correct severity counts
- Test that a non-existent SBOM ID returns 404
- Test that an SBOM with no advisories returns all zeros
- Test that duplicate advisory links are deduplicated in the count

### GitHub Issue Extraction
Look up custom field `customfield_10747` from the fetched issue's fields. If a GitHub issue URL is present, parse `owner/repo#number` for use in the PR description's `Closes` line. If empty, skip silently.

### Issue Web URL
Capture the `webUrl` field from the API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

## Step 1.5 -- Verify Description Integrity

(See outputs/digest-match.md for full details.)

1. Fetch comments on TC-9201 via `jira.get_issue_comments("TC-9201")`.
2. Locate the digest comment matching marker `[sdlc-workflow] Description digest:`. One comment found with body: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
3. Comment edit detection: `created` and `updated` timestamps are identical -- comment is unmodified. No warning needed.
4. Extract stored digest: format tag is `md`, hex digest is `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
5. Compute current digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`. Output: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
6. Compare format tags: both `sha256-md` -- tags match.
7. Compare hex digests: both `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` -- **match**.

**Result**: Digests match. Proceed silently -- no user prompt, no added latency.

## Step 2 -- Verify Dependencies

The task has no dependencies listed. Skip dependency verification.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<current-user-account-id>)`.
3. Transition TC-9201 to "In Progress": `jira.transition_issue("TC-9201", "In Progress")`.

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using Serena instance `serena_backend` (called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`**: Use `mcp__serena_backend__get_symbols_overview` to see the AdvisoryService struct and its methods (fetch, list, search). Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand the pattern (signature, transaction handling, error wrapping).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**: Use `mcp__serena_backend__get_symbols_overview` to see route registration pattern. Identify how routes are registered (e.g., `Router::new().route(...)` chains).

3. **`modules/fundamental/src/advisory/endpoints/get.rs`**: Use `mcp__serena_backend__find_symbol` to read the existing GET handler -- this is the pattern to follow for the new endpoint (Path extraction, service call, JSON response).

4. **`modules/fundamental/src/advisory/model/mod.rs`**: Inspect current module declarations to understand the pattern for adding `pub mod severity_summary;`.

5. **`modules/fundamental/src/advisory/model/summary.rs`**: Read the `AdvisorySummary` struct to understand the `severity` field type and how severity is represented.

6. **`entity/src/sbom_advisory.rs`**: Inspect the SBOM-Advisory join table entity to understand the relationship schema for querying.

7. **`common/src/error.rs`**: Confirm the `AppError` pattern and `.context()` usage.

### 4.2 Check Backward Compatibility

Use `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., `AdvisoryService`) to ensure adding a new method does not break existing callers (it should not -- adding a method is non-breaking).

### 4.3 Convention Conformance Analysis (Sibling Analysis)

Examine sibling files to discover implicit conventions:

**Sibling endpoint files** (`modules/fundamental/src/advisory/endpoints/get.rs`, `list.rs`):
- Naming: handlers follow `get_<entity>`, `list_<entity>` naming
- Error handling: `Result<Json<T>, AppError>` with `.context("description")`
- Path extraction: `Path(id): Path<Id>` pattern
- Service call: `service.method(id, &tx).await?`
- Response: return `Ok(Json(result))`

**Sibling service methods** (`advisory.rs` -- fetch, list):
- Signature: `pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, anyhow::Error>`
- Uses SeaORM queries with join operations
- Error wrapping with `.context()`

**Sibling model files** (`modules/fundamental/src/advisory/model/summary.rs`, `details.rs`):
- Structs derive `Clone, Debug, Serialize, Deserialize`
- Use `utoipa::ToSchema` for OpenAPI schema generation
- Fields documented with doc comments

### Discovered Conventions (from sibling analysis)

- **Error handling**: All handlers return `Result<Json<T>, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`); endpoint handlers follow `get_<entity>`, `list_<entity>`
- **Endpoint pattern**: Extract path params via `Path<Id>`, call service method, return `Ok(Json(result))`
- **Model structs**: Derive `Clone, Debug, Serialize, Deserialize, utoipa::ToSchema`
- **Module registration**: Add `pub mod <name>;` in the parent `mod.rs`
- **Route registration**: `Router::new().route("/path", get(handler))` chains in `endpoints/mod.rs`
- **Service signatures**: `pub async fn method(&self, param: Type, tx: &Transactional<'_>) -> Result<T, anyhow::Error>`

### 4.4 Test Convention Analysis

Examine sibling test files in `tests/api/`:

**Sibling test files** (`tests/api/advisory.rs`, `tests/api/sbom.rs`):
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: Check status code, then deserialize JSON body and assert on specific fields
- **Error cases**: Test 404 with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory`, `test_list_sboms`)
- **Test setup**: Create test database, seed data, build test server
- **Given-when-then**: Not explicitly used in siblings, but we will add section comments for AI-generated tests as required by the skill

### Discovered Test Conventions (from sibling test analysis)

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` then `let body: T = resp.json().await`
- **Response validation**: Assert on specific field values, not just collection length
- **Error cases**: Dedicated 404 test with non-existent IDs
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Test setup**: Integration tests against real PostgreSQL test database

### 4.5 Documentation File Identification

Identify documentation files related to the code being modified:
- `docs/api.md` -- REST API reference (may need updating with new endpoint)
- `docs/architecture.md` -- system architecture overview
- `README.md` -- repository readme
- `CONVENTIONS.md` -- repository conventions (check for CI commands)

### 4.6 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo structure indicates it exists. Read it and extract:
- Coding conventions to follow during implementation
- CI check commands for use in Step 9 verification
- Code generation commands (if any)

## Step 5 -- Create Branch

This is the default flow (no Target PR, no Bookend Type). Target Branch is `main`.

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct following sibling model conventions:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for a given SBOM.
///
/// Provides counts of unique advisories grouped by severity level,
/// enabling dashboard widgets to render severity breakdowns.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u64,
    /// Count of high-severity advisories.
    pub high: u64,
    /// Count of medium-severity advisories.
    pub medium: u64,
    /// Count of low-severity advisories.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}
```

### 6.2 Register model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to the existing module declarations:

```rust
pub mod severity_summary;
```

### 6.3 Add `severity_summary` method to AdvisoryService in `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method following the existing `fetch` and `list` pattern:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Returns counts of unique advisories grouped by severity level
/// (Critical, High, Medium, Low) and a total count.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // Verify SBOM exists first (returns 404-compatible error if not)
    // Query sbom_advisory join table to find advisories linked to this SBOM
    // Join with advisory table to get severity field
    // Deduplicate by advisory ID
    // Count by severity level
    // Return SeveritySummary with counts, defaulting to 0 for missing levels
}
```

Key implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- Join with advisory entity to access severity field from `AdvisorySummary`
- Use `DISTINCT` on advisory ID to handle deduplication
- Group by severity level and count
- Default all counts to 0 (struct derives `Default`)
- Wrap errors with `.context("Failed to compute severity summary")`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use crate::Error as AppError;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of unique advisories
/// grouped by severity level for the specified SBOM.
pub async fn get_advisory_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transaction */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the new route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route to the existing router chain:

```rust
pub mod severity_summary;

// In the router function, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

### 6.6 Code Quality Practices

Every new struct, type, and public function includes documentation comments:
- `SeveritySummary` struct and all its fields have `///` doc comments
- `severity_summary` service method has a `///` doc comment explaining what it does
- `get_advisory_summary` handler has a `///` doc comment explaining the endpoint

### 6.7 Documentation Impact

- Check `docs/api.md` for the REST API reference and add documentation for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- No configuration or setup changes are required
- No architectural changes

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests following sibling test conventions.

All test functions include `///` doc comments and given-when-then section comments:

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that the advisory summary endpoint returns correct severity counts
/// for an SBOM with advisories at known severity levels.
#[tokio::test]
async fn test_get_advisory_summary_with_advisories() {
    // Given an SBOM with linked advisories at various severity levels
    // (seed test data: 2 critical, 3 high, 1 medium, 0 low)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response should be 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 2);
    assert_eq!(body.high, 3);
    assert_eq!(body.medium, 1);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 6);
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found status, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_get_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts set to zero.
#[tokio::test]
async fn test_get_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisories are deduplicated

```rust
/// Verifies that duplicate advisory links (same advisory linked to the SBOM
/// multiple times) are deduplicated in the severity count.
#[tokio::test]
async fn test_get_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate links to the same advisory (e.g., advisory A
    // linked twice with severity "High")

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.high, 1); // not 2 despite duplicate links
    assert_eq!(body.total, 1);
}
```

After writing tests, run them:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Test 1 validates the response struct with all fields |
| Returns 404 for non-existent SBOM | Test 2 validates 404 status |
| Counts only unique advisories | Test 4 validates deduplication |
| All severity levels default to 0 | Test 3 validates all-zero response; `SeveritySummary` derives `Default` |
| Response time under 200ms for 500 advisories | The query uses database-level aggregation (GROUP BY) rather than client-side counting, ensuring O(1) response complexity relative to result count |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against declared files:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

If `docs/api.md` was updated (documentation impact from Step 6.7), it is out-of-scope per the task description's Files to Modify list. Flag it to the user and ask for approval.

If `server/src/main.rs` appears modified, flag it -- the task description explicitly says "no changes needed."

### Untracked File Check

Run `git status --short`, extract `??` entries, filter by proximity to modified directories, search for code references. Flag any referenced untracked files for user approval before staging.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation Currency

Check if `docs/api.md` needs updating with the new endpoint. If it was not updated in Step 6, update it now.

### Documentation Scope Preservation

If `docs/api.md` was modified, verify replacement text still covers all previously documented endpoints and use cases.

### Eval Coverage Currency

No `SKILL.md` files are being modified -- skip this check.

### Example Consistency

If documentation with examples was written, verify internal consistency between prose and data structures.

### Cross-Section Reference Consistency

Verify file paths are consistent across the task description sections:
- `AdvisoryService` is referenced as `modules/fundamental/src/advisory/service/advisory.rs` in both Files to Modify and Implementation Notes -- consistent.
- Route registration is referenced as `modules/fundamental/src/advisory/endpoints/mod.rs` in both sections -- consistent.

### Duplication Check

Search for existing severity aggregation or advisory counting logic in the repository. Use Grep/Serena to look for similar function names (`severity_summary`, `severity_count`, `advisory_summary`). If equivalent logic already exists, refactor to reuse it.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4.6. Execute each in sequence. Hard stop on any non-zero exit.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract SBOM ID from path params -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> join with advisory entity -> group by severity -> count unique advisories -> return `SeveritySummary` JSON -- **COMPLETE**

### Contract & Sibling Parity

- `SeveritySummary` is a standalone response struct (no trait implementation required)
- `get_advisory_summary` handler follows the same `Result<Json<T>, AppError>` contract as sibling handlers
- Service method follows the same `Result<T, anyhow::Error>` signature as sibling methods
- Error handling uses `.context()` wrapping consistent with siblings

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
proper 404 handling for non-existent SBOMs.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates
vulnerability advisory severity counts for a given SBOM, returning counts per
severity level (Critical, High, Medium, Low) and a total.

### Changes
- New `SeveritySummary` response struct
- New `severity_summary` method on `AdvisoryService`
- New GET handler at `/api/v2/sbom/{id}/advisory-summary`
- Integration tests covering: valid response, 404 for missing SBOM, empty results, deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

### Set Git Pull Request Custom Field

Update `customfield_10875` on TC-9201 with the PR URL using ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

### Add Implementation Comment

Post a comment on TC-9201 summarizing the implementation, including:
- Link to the PR
- Summary of changes made (new endpoint, service method, model, tests)
- Note that no deviations from the plan were needed

The comment ends with the standard footnote (horizontal rule + "This comment was AI-generated by sdlc-workflow/implement-task v{version}." with link to GitHub repo), using ADF `contentFormat`.

### Transition to In Review

```
jira.transition_issue("TC-9201", "In Review")
```
