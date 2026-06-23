# Implementation Plan: TC-9201 -- Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verified the project CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured with rust-analyzer

All required configuration is in place. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Fetch the task using `jira.get_issue("TC-9201")` and parse the structured description.

**Parsed fields:**

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
  - `tests/api/advisory_summary.rs` -- integration tests for the new endpoint
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- **Bookend Type:** not present (standard implementation flow)
- **Target PR:** not present (standard flow -- create new branch and PR)
- **Dependencies:** None

**GitHub Issue extraction:** Look up the GitHub Issue custom field (`customfield_10747`) from the fetched issue fields. If present, parse the GitHub issue URL for use in the PR description's `Closes` line. If absent, skip silently.

**Issue webUrl:** Capture from the API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

## Step 1.5 -- Verify Description Integrity

See `digest-match.md` for the full description of this step. Summary: the digest comment is found with marker `[sdlc-workflow] Description digest:`, the format tag is `sha256-md`, the comment was not edited (created == updated), and the computed digest matches the stored digest. Proceed silently with no user prompt.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification is needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve the current user's Jira account ID: `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect existing files using Serena (serena_backend)

**Files to Modify -- symbols overview:**

1. `modules/fundamental/src/advisory/service/advisory.rs`:
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__find_symbol("severity_summary", include_body=false)` to confirm the method does not already exist
   - `mcp__serena_backend__find_symbol("list", include_body=true)` to read the `list` method as a pattern for the new `severity_summary` method

2. `modules/fundamental/src/advisory/endpoints/mod.rs`:
   - `mcp__serena_backend__get_symbols_overview` to see how routes are registered
   - Identify the pattern for adding new routes (e.g., `Router::new().route(...)`)

3. `modules/fundamental/src/advisory/model/mod.rs`:
   - `mcp__serena_backend__get_symbols_overview` to see existing `pub mod` declarations

**Sibling files for convention analysis:**

4. `modules/fundamental/src/advisory/endpoints/get.rs`:
   - Read to understand the existing endpoint pattern (path params via `Path<Id>`, service call, JSON response)

5. `modules/fundamental/src/advisory/model/summary.rs`:
   - Read to understand the `AdvisorySummary` struct, particularly the `severity` field for counting

6. `modules/fundamental/src/sbom/endpoints/get.rs`:
   - Read as a second sibling endpoint for convention confirmation

**Related entity files:**

7. `entity/src/sbom_advisory.rs`:
   - Read to understand the SBOM-Advisory join table structure for querying advisories linked to an SBOM

**Error handling pattern:**

8. `common/src/error.rs`:
   - Read `AppError` enum to understand error wrapping with `.context()`

### 4.2 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract:
- CI check commands for Step 9
- Code generation commands
- Any naming or structural conventions

### 4.3 Convention conformance analysis

**Expected discovered conventions (from sibling analysis):**

- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`); the new method `severity_summary` follows this convention
- **Endpoint pattern:** Extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Route registration:** `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Response types:** Direct struct return with Axum `Json` extractor handling serialization
- **Model modules:** Each model is in its own file, registered via `pub mod` in `model/mod.rs`
- **Service method signature:** `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`

### 4.4 Test convention analysis

**Sibling test files to inspect:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

**Expected discovered test conventions:**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation:** Validate specific field values in the response body
- **Error cases:** Include 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Setup:** Tests hit a real PostgreSQL test database; use test fixtures for SBOMs and advisories

### 4.5 Documentation file identification

Identify documentation files that may need updating:
- `README.md` at repo root
- `docs/api.md` -- REST API reference (if it lists endpoints, the new endpoint should be added)
- `docs/architecture.md` -- system architecture overview (likely no change needed)

### 4.6 Backward compatibility check

Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers and confirm the new method addition will not break existing consumers (adding a method to a struct does not break callers in Rust).

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
#[derive(Debug, Clone, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with critical severity.
    pub critical: u64,
    /// Number of advisories with high severity.
    pub high: u64,
    /// Number of advisories with medium severity.
    pub medium: u64,
    /// Number of advisories with low severity.
    pub low: u64,
    /// Total number of unique advisories.
    pub total: u64,
}
```

Add `Default` derive or implement it to default all fields to 0.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module. Follow the existing pattern of `pub mod` declarations in this file.

### 6.3 Add `severity_summary` method to `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService` following the pattern of `fetch` and `list`:

- **Signature:** `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- **Logic:**
  1. Query the `sbom_advisory` join table to find all advisories linked to the given SBOM ID
  2. Join with the advisory table to get severity information
  3. Deduplicate by advisory ID (use `DISTINCT` or equivalent)
  4. Count advisories per severity level (Critical, High, Medium, Low)
  5. Return `SeveritySummary` with the counts and total
  6. If the SBOM does not exist, return a 404-equivalent error consistent with existing SBOM endpoints

Use `.context("Failed to aggregate advisory severity summary")` for error wrapping.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Error fetching severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Import the new module at the top of the file: `mod severity_summary;`

### 6.6 Documentation impact

Check `docs/api.md` for endpoint listings. If the file documents REST endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request parameters and response schema. Keep the update lightweight and scoped.

### 6.7 Code quality practices

Verify all new structs, public functions, and endpoints have documentation comments (Rust `///` convention). The examples above include doc comments on all public symbols.

## Step 7 -- Write Tests

### 7.1 Create `tests/api/advisory_summary.rs`

Write integration tests following the conventions discovered in sibling test files:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories of known severities
    // (set up test fixtures with specific severity distributions)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then the response is 200 with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical);
    assert_eq!(summary.high, expected_high);
    assert_eq!(summary.medium, expected_medium);
    assert_eq!(summary.low, expected_low);
    assert_eq!(summary.total, expected_total);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .send()
        .await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then each advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Assert total matches unique advisory count, not link count
    assert_eq!(summary.total, expected_unique_count);
}
```

### 7.2 Run tests

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. **GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape** -- verified by `test_advisory_summary_valid_sbom`
2. **Returns 404 for non-existent SBOM ID** -- verified by `test_advisory_summary_nonexistent_sbom`
3. **Counts only unique advisories** -- verified by `test_advisory_summary_deduplication`
4. **All severity levels default to 0** -- verified by `test_advisory_summary_no_advisories`
5. **Response time under 200ms for up to 500 advisories** -- verify by inspecting the query plan; the join query with aggregation should perform well with proper indexing on `sbom_advisory`

## Step 9 -- Self-Verification

### 9.1 Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- in scope
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in scope
- `modules/fundamental/src/advisory/model/mod.rs` -- in scope

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in scope
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in scope
- `tests/api/advisory_summary.rs` -- in scope

Note: `server/src/main.rs` is listed in Files to Modify with "no changes needed" -- confirm no modifications were made.

If `docs/api.md` was updated (documentation impact), flag it as out-of-scope and ask user approval since it is not listed in Files to Modify.

### 9.2 Untracked file check

Run `git status --short` and check for `??` entries in directories where implementation occurred. Flag any untracked files that are referenced by code for user review.

### 9.3 Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Confirm no secrets are staged.

### 9.4 Documentation currency

Check whether `docs/api.md` describes the endpoint list. If so and it was not already updated in Step 6, update it now with the new endpoint.

### 9.5 Documentation scope preservation

If documentation was modified, verify that replacement text still covers all use cases from the original text.

### 9.6 Cross-section reference consistency

Verify file paths are consistent across the task description sections:
- `AdvisoryService` is referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent.
- `SeveritySummary` is referenced in Files to Create (`advisory/model/severity_summary.rs`) and is distinct from `AdvisorySummary` in Implementation Notes (`advisory/model/summary.rs`) -- no conflict.

### 9.7 Duplication check

Search the repository for existing severity aggregation logic using Grep or `mcp__serena_backend__search_for_pattern`. Confirm no existing utility provides equivalent functionality.

### 9.8 CI checks from CONVENTIONS.md

If CI check commands were extracted in Step 4, run them all. Hard stop on any failure.

If no CONVENTIONS.md or CI section was found, run:

```bash
cargo build
cargo clippy -- -D warnings
cargo fmt --check
```

Fix any issues before proceeding.

### 9.9 Data-flow trace

Trace the data through the complete lifecycle:

- **Input:** HTTP GET request with SBOM ID path parameter
- **Processing:** Path param extraction -> AdvisoryService.severity_summary() -> query sbom_advisory join table -> aggregate by severity -> deduplicate by advisory ID
- **Output:** JSON response with SeveritySummary struct (critical, high, medium, low, total)

All stages are connected: request -> handler -> service -> database -> response. **COMPLETE**.

### 9.10 Contract and sibling parity

- **Contract verification:** `SeveritySummary` derives `Serialize` and `ToSchema` matching all response structs in the module. The handler returns `Result<Json<SeveritySummary>, AppError>` matching the contract for all endpoints.
- **Sibling parity:** Compare with `get.rs` endpoint -- error handling (`.context()`), response type (`Json`), path extraction (`Path<Id>`) all match.
- **Cross-module shared entity:** The `sbom_advisory` join table is read-only in this implementation (SELECT only), so no write-pattern anomalies apply.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes deduplication by advisory
ID and proper 404 handling for non-existent SBOMs.

Implements TC-9201"

git push -u origin TC-9201
```

Create PR with `--base main`:

```bash
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" \
  --body "## Summary

- Add SeveritySummary response model
- Add severity_summary method to AdvisoryService
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Add integration tests for the new endpoint

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

Closes <owner>/<repo>#<number>  (if GitHub issue was extracted)"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

   ```
   jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
   - No deviations from the plan
   - Comment ends with the skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition** TC-9201 to In Review:
   ```
   jira.transition_issue("TC-9201") -> In Review
   ```
