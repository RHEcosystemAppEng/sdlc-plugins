# Implementation Plan: TC-9201 -- Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- Present. Contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- Present. Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID: 10142.
3. **Code Intelligence** -- Present. Tool naming convention: `mcp__<serena-instance>__<tool>`. Configured instance: `serena_backend` with `rust-analyzer`.

All required sections are present. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt the user for REST API fallback, retry, or skip.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing patterns in `get.rs`, add method to AdvisoryService following `fetch`/`list` pattern, use `sbom_advisory` join table, use `AdvisorySummary.severity` field, register route in `endpoints/mod.rs`, use `AppError` with `.context()`, return struct directly with Axum `Json`.
- **Acceptance Criteria**: 5 items (correct response shape, 404 on missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 tests (correct counts, 404, empty SBOM, deduplication)
- **Target PR**: Not present (default flow)
- **Bookend Type**: Not present (default flow)
- **Dependencies**: None

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

### GitHub Issue Extraction

Look up `GitHub Issue custom field: customfield_10747` from Jira Configuration. Check the field value on the fetched issue. If present, extract the GitHub issue reference for use in the PR description. If empty, skip silently.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the full description of this step.

**Summary**: The digest comment is found with body `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890...`. The comment's `created` and `updated` timestamps are identical (not edited). The format tag is `sha256-md`. Computing the digest of the current description via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` produces the same format tag (`md`) and the same hex digest. **Result: MATCH.** Proceed silently.

## Step 2 -- Verify Dependencies

The task has no dependencies. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`.

## Step 4 -- Understand the Code

Use the `serena_backend` Serena instance (tools called as `mcp__serena_backend__<tool>`) to inspect the codebase.

### 4.1 Inspect Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see `AdvisoryService` structure, `fetch` and `list` methods.
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand the pattern (takes `&self, id: Id, tx: &Transactional<'_>`, returns `Result<T, AppError>`).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see existing route registration pattern (`Router::new().route(...)` calls).

3. **`modules/fundamental/src/advisory/model/mod.rs`**:
   - Read to see existing `pub mod` declarations (summary, details).

### 4.2 Inspect Reference Files

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** (reference pattern for endpoint):
   - `mcp__serena_backend__find_symbol` on the handler function to see `Path<Id>` extraction, service call, JSON response pattern.

2. **`modules/fundamental/src/advisory/model/summary.rs`** (reference for `AdvisorySummary` with `severity` field):
   - `mcp__serena_backend__get_symbols_overview` to see the `severity` field type and how it's defined.

3. **`entity/src/sbom_advisory.rs`** (join table):
   - `mcp__serena_backend__get_symbols_overview` to understand the join table entity structure.

4. **`common/src/error.rs`** (error handling pattern):
   - `mcp__serena_backend__get_symbols_overview` to confirm `AppError` enum and `.context()` wrapping pattern.

### 4.3 Check Backward Compatibility

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure adding a new method doesn't conflict.
- `mcp__serena_backend__find_referencing_symbols` on the `endpoints/mod.rs` route registration to understand how routes are mounted.

### 4.4 Convention Conformance Analysis

**Siblings for endpoints**: Inspect `endpoints/list.rs` and `endpoints/get.rs` in the advisory module.
**Siblings for models**: Inspect `model/summary.rs` and `model/details.rs`.
**Siblings for service methods**: Inspect `fetch` and `list` methods in `advisory.rs`.

Expected discovered conventions:
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`)
- **Endpoint pattern**: Extract path params via `Path<Id>`, call service, return `Json(result)`
- **Response types**: Structs derive `Serialize, Deserialize, Debug` and are returned directly
- **Route registration**: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`

### 4.5 Test Convention Analysis

**Sibling test files**: Inspect `tests/api/advisory.rs` and `tests/api/sbom.rs`.

Expected discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: Check response fields directly
- **Error cases**: Include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: Use test database with fixture data

### 4.6 Documentation File Identification

- `README.md` at repository root
- `docs/api.md` (API reference)
- `CONVENTIONS.md` at repository root -- read for CI check commands and code conventions

### 4.7 CONVENTIONS.md Lookup

Read `CONVENTIONS.md` at the repository root (path `./CONVENTIONS.md` from the Repository Registry). Extract:
- CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`)
- Code generation commands (if any)
- Naming rules, directory structure conventions

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated advisory severity counts for an SBOM.
///
/// Provides a breakdown of linked advisories by severity level,
/// enabling dashboard widgets to render severity distributions
/// without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
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

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` alongside existing module declarations.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Following the pattern of `fetch` and `list`:

```rust
/// Computes an aggregated severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories linked to the specified SBOM,
/// deduplicates by advisory ID, and counts occurrences per severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query advisories linked to the SBOM via the sbom_advisory join table
    // Deduplicate by advisory ID
    // Count by severity level using AdvisorySummary.severity field
    // Return SeveritySummary with counts and total
    // Return 404 (via AppError) if SBOM ID does not exist
}
```

Key implementation details:
- Use `sbom_advisory` entity to join SBOMs to advisories
- Use `AdvisorySummary.severity` field to categorize each advisory
- Deduplicate by advisory ID before counting (per acceptance criteria)
- Default all severity levels to 0 when no advisories exist at that level
- Wrap errors with `.context()` matching the pattern in `common/src/error.rs`
- First verify the SBOM exists; if not, return 404 consistent with existing SBOM endpoints

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns an aggregated count of advisory severities for the specified SBOM,
/// broken down by Critical, High, Medium, and Low levels.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Import the `severity_summary` module at the top of the file.

### 6.6 Documentation Impact

- No Documentation Updates section in the task
- Update `docs/api.md` if it exists, adding the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation
- Keep documentation updates lightweight -- only describe the new endpoint

### 6.7 Code Quality

Verify all new structs, types, and public functions have documentation comments (as shown above in the code snippets).

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests following the sibling test conventions.

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with linked advisories returns the correct
/// severity count breakdown.
#[tokio::test]
async fn test_advisory_summary_correct_counts() {
    // Given an SBOM with known advisories at various severity levels
    // (setup: seed test DB with SBOM + linked advisories)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").send().await;

    // Then the response status is 200 and counts match expected values
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical);
    assert_eq!(summary.high, expected_high);
    assert_eq!(summary.medium, expected_medium);
    assert_eq!(summary.low, expected_low);
    assert_eq!(summary.total, expected_total);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").send().await;

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts at zero.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").send().await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated in the count

```rust
/// Verifies that duplicate advisory-SBOM links do not inflate the severity
/// counts -- each advisory is counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").send().await;

    // Then counts reflect unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, expected_unique_count);
    // Verify individual severity counts match deduplicated values
}
```

Each test function includes a documentation comment explaining what it verifies. Non-trivial tests use given-when-then section comments.

Run tests:
```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by Test 1
2. Returns 404 when SBOM ID does not exist -- verified by Test 2
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by Test 4
4. All severity levels default to 0 when no advisories exist -- verified by Test 3
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by query design (single join query, no N+1)

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

Expected modified/created files:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (new -- in Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (new -- in Files to Create)
- `tests/api/advisory_summary.rs` (new -- in Files to Create)
- `modules/fundamental/src/advisory/service/advisory.rs` (modified -- in Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified -- in Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modified -- in Files to Modify)

If any out-of-scope files appear, list them and ask for user approval.

### Untracked File Check

Run `git status --short` to find untracked files (`??` entries). Filter by proximity to directories with modified files. Search for code references to any flagged untracked files. Ask user before staging.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to check for secrets. Flag any matches.

### Documentation Currency

If `docs/api.md` describes existing endpoints and the new endpoint was not already added in Step 6, update it now.

### Cross-Section Reference Consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` -- referenced in Files to Modify as `advisory/service/advisory.rs` and in Implementation Notes as the same path. Consistent.
- `SeveritySummary` -- referenced in Files to Create as `advisory/model/severity_summary.rs`. Consistent.
- Route registration -- referenced in Files to Modify as `advisory/endpoints/mod.rs` and in Implementation Notes as the same. Consistent.

### Duplication Check

Search for existing severity aggregation or summary functions in the repository. Verify no existing utility already provides this functionality.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4 (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`). Hard stop on any failure.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary`:
  - Input: HTTP request with SBOM ID path parameter -- handler extracts via `Path<Id>` -- COMPLETE
  - Processing: `AdvisoryService.severity_summary()` queries `sbom_advisory` join, deduplicates, counts by severity -- COMPLETE
  - Output: `SeveritySummary` struct serialized as JSON response -- COMPLETE
  - Full path: request -> endpoint handler -> service method -> database query -> response -- COMPLETE

### Contract & Sibling Parity

- `SeveritySummary` derives `Serialize, Deserialize` matching sibling model structs (summary.rs, details.rs)
- `get_severity_summary` handler follows the same `Result<Json<T>, AppError>` return type as `get.rs`
- `severity_summary` service method follows the same `&self, id, tx` signature pattern as `fetch` and `list`
- Error handling uses `.context()` wrapping consistent with all sibling handlers

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated advisory severity counts (critical, high, medium, low, total)
for a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"
```

Push and create PR targeting main:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

- Add `SeveritySummary` response struct with critical/high/medium/low/total counts
- Add `severity_summary` method to `AdvisoryService` using the `sbom_advisory` join table
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler
- Add integration tests covering correct counts, 404, empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test Plan

- [ ] Integration tests pass: correct severity counts for known advisories
- [ ] 404 returned for non-existent SBOM ID
- [ ] All-zero counts for SBOM with no advisories
- [ ] Duplicate advisory links deduplicated in counts
- [ ] CI checks pass (fmt, clippy, test)"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field**: Update `customfield_10875` on TC-9201 with the PR URL in ADF format (inlineCard).

2. **Add comment**: Post a comment to TC-9201 with:
   - PR link
   - Summary of changes: Added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
   - No deviations from the plan
   - Comment ends with the standard footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition**: Transition TC-9201 to "In Review" via `jira.transition_issue`.
