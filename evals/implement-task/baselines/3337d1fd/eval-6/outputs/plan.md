# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains:

1. **Repository Registry** -- present, with `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured with `rust-analyzer`

All sections are complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all Jira operations. Fall back to REST API (`scripts/jira-client.py`) if MCP fails, after prompting the user.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue:

```
jira.get_issue("TC-9201")
```

Parsed structured description:

| Section | Value |
|---|---|
| **Repository** | trustify-backend |
| **Target Branch** | main |
| **Description** | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| **Files to Modify** | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| **Files to Create** | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| **API Changes** | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| **Bookend Type** | Not present (standard implementation task) |
| **Target PR** | Not present (new PR flow) |
| **Dependencies** | None |
| **Linked Issues** | is incorporated by TC-9001 |

Capture `webUrl` for the Jira issue (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

### GitHub Issue extraction

Look up `customfield_10747` from the issue fields. If a URL is present, parse `owner/repo#number` for use in the PR description's `Closes` line. If empty, skip.

## Step 1.5 -- Verify Description Integrity

(See outputs/digest-match.md for full details.)

Result: **Digest match.** The description is unmodified since plan-feature created it. Proceed silently.

## Step 2 -- Verify Dependencies

The task lists `Dependencies: None`. No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign the task: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- `get_symbols_overview` to see AdvisoryService's existing methods (`fetch`, `list`, `search`). Use `find_symbol` with `include_body=true` on `fetch` and `list` methods to understand the pattern (parameter types, return types, transaction handling).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- `get_symbols_overview` to see how existing routes are registered. Inspect the `Router::new().route(...)` pattern.

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- `get_symbols_overview` to see existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`).

### 4.2 Inspect reference patterns

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- `find_symbol` to understand the existing GET handler pattern: `Path<Id>` extraction, service call, JSON response return.

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- `find_symbol` on `AdvisorySummary` to see the `severity` field type and structure.

6. **`entity/src/sbom_advisory.rs`** -- `get_symbols_overview` to understand the join table structure for linking SBOMs to advisories.

7. **`common/src/error.rs`** -- `find_symbol` on `AppError` to understand the error handling pattern and `.context()` wrapping.

### 4.3 Check backward compatibility

8. Use `find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure the new `severity_summary` method does not conflict.

### 4.4 Convention conformance analysis (sibling inspection)

Inspect sibling files for patterns:

- **Endpoint siblings**: `endpoints/get.rs` and `endpoints/list.rs` in the advisory module -- examine handler signatures, error handling, response types
- **Model siblings**: `model/summary.rs` and `model/details.rs` -- examine struct definitions, derive macros, serde attributes
- **Service siblings**: `service/advisory.rs` methods -- examine method signatures, transaction usage, return types

Expected discovered conventions:
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Service methods:** Take `&self, id: Id, tx: &Transactional<'_>` parameters
- **Naming:** Service methods use `verb_noun` pattern (e.g., `fetch`, `list`)
- **Route registration:** `Router::new().route("/path", get(handler))` pattern
- **Response:** Structs derive `Serialize, Deserialize, Debug` and are returned directly via Axum's `Json`

### 4.5 Test convention analysis

Inspect sibling test files:

- **`tests/api/advisory.rs`** -- examine assertion patterns, status code checks, response body validation
- **`tests/api/sbom.rs`** -- examine test setup, fixture creation, 404 handling

Expected discovered test conventions:
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases:** Tests include 404 with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Setup:** Tests use a real PostgreSQL test database with fixture data

### 4.6 Documentation file identification

- Check for `CONVENTIONS.md` at repository root -- if present, read for CI check commands and code generation commands
- Check for `docs/api.md` for API documentation that may need updating
- Check `README.md` for any endpoint listings

### 4.7 CONVENTIONS.md lookup

Look for `CONVENTIONS.md` at `./CONVENTIONS.md` in the repository root. If present:
- Read and follow all conventions throughout implementation
- Extract CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`)
- Extract code generation commands if any

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
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of linked advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u32,
    /// Number of high-severity advisories.
    pub high: u32,
    /// Number of medium-severity advisories.
    pub medium: u32,
    /// Number of low-severity advisories.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

Follow the same derive macros and doc comment style observed in sibling model files (`summary.rs`, `details.rs`).

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module registration:

```rust
pub mod severity_summary;
```

Place it alongside existing `pub mod summary;` and `pub mod details;` declarations.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Add a method following the `fetch`/`list` pattern:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Counts unique advisories by severity level (critical, high, medium, low)
/// using the `sbom_advisory` join table. Deduplicates by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to sbom_id
    // 2. Deduplicate by advisory ID
    // 3. For each unique advisory, look up its AdvisorySummary.severity field
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Compute total as sum of all levels
    // 6. Return SeveritySummary struct with all counts (defaulting to 0)
}
```

Error handling: use `.context("Failed to compute severity summary for SBOM")` wrapping, matching the pattern in `common/src/error.rs`. Return 404 via `AppError` when the SBOM ID does not exist, consistent with existing SBOM endpoints.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories at each severity
/// level (critical, high, medium, low) and a total count for the given SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Error fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Match the exact parameter extraction and error handling patterns observed in sibling endpoint handlers.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing pattern:

```rust
use severity_summary::get_severity_summary;

// In the router setup:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### 6.6 No changes to `server/src/main.rs`

Per the task description, routes auto-mount via module registration. No modification needed.

### 6.7 Documentation impact

- Check if `docs/api.md` lists endpoints -- if so, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response format
- Keep documentation updates lightweight and scoped

### 6.8 Code quality verification

Verify all new structs and public functions have documentation comments (already included above). Verify naming matches conventions discovered in Step 4.

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Following the assertion patterns and naming conventions discovered in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test database fixtures with specific advisory-SBOM links)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, <expected_critical>);
    assert_eq!(summary.high, <expected_high>);
    assert_eq!(summary.medium, <expected_medium>);
    assert_eq!(summary.low, <expected_low>);
    assert_eq!(summary.total, <expected_total>);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

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
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Assert that the total reflects unique advisories, not duplicate links
    assert_eq!(summary.total, <expected_unique_count>);
}
```

Run tests:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification Method |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by `test_advisory_summary_valid_sbom` -- response shape and field values checked |
| Returns 404 when SBOM ID does not exist | Verified by `test_advisory_summary_not_found` -- status code 404 assertion |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_advisory_summary_deduplication` -- duplicate links produce single count |
| All severity levels default to 0 when no advisories exist | Verified by `test_advisory_summary_empty` -- all fields assert 0 |
| Response time under 200ms for SBOMs with up to 500 advisories | Verify via database query plan (EXPLAIN ANALYZE) or by adding a timing assertion in a load-style test if feasible |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

If any out-of-scope files appear (e.g., `docs/api.md` from documentation updates), list them and ask for user approval.

### Untracked file check

Run `git status --short` to identify `??` entries. Filter by proximity to implementation directories. Search for code references to any untracked files before staging.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation currency

Verify `docs/api.md` (if it exists) reflects the new endpoint. Update if needed.

### Cross-section reference consistency

Verify that file paths referenced in Files to Modify, Files to Create, and Implementation Notes are consistent:

- `AdvisoryService` -- referenced in both Files to Modify (`service/advisory.rs`) and Implementation Notes (`service/advisory.rs`) -- consistent
- Route registration -- referenced in both Files to Modify (`endpoints/mod.rs`) and Implementation Notes (`endpoints/mod.rs`) -- consistent
- `AdvisorySummary` struct -- referenced in Implementation Notes (`model/summary.rs`) -- consistent with model directory

### Duplication check

Search for existing severity aggregation or counting logic in the repository:

```
search_for_pattern("severity.*count|count.*severity|severity_summary")
```

If overlapping logic exists, refactor to reuse it.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract SBOM ID from path (input) -> call `AdvisoryService.severity_summary()` (processing) -> query `sbom_advisory` join table, aggregate by severity, deduplicate (processing) -> return `SeveritySummary` JSON (output) -- **COMPLETE**

### Contract and sibling parity

- `SeveritySummary` -- standalone struct, no trait contract to verify
- Sibling parity with `get.rs` and `list.rs` endpoint handlers -- error handling, response type, parameter extraction patterns should match
- Sibling parity with `fetch` and `list` service methods -- transaction handling, error context wrapping should match

### CI checks from CONVENTIONS.md

If CI commands were extracted, run them all:

```bash
cargo fmt --check
cargo clippy -- -D warnings
cargo test
```

Hard stop on any non-zero exit code.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Add any documentation files if modified and approved

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity summary endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
proper 404 handling for missing SBOMs.

Implements TC-9201"
```

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If upstream exists, use fork-aware PR creation.

### Push and create PR

```bash
git push -u origin TC-9201
```

Create the PR targeting `main`:

```bash
gh pr create --base main \
  --title "feat(api): add advisory severity summary endpoint" \
  --body "## Summary

Add a new REST endpoint \`GET /api/v2/sbom/{id}/advisory-summary\` that returns
aggregated advisory severity counts for a given SBOM, enabling dashboard widgets
to render severity breakdowns without client-side counting.

### Changes
- New \`SeveritySummary\` response struct in \`advisory/model/severity_summary.rs\`
- New \`severity_summary\` method on \`AdvisoryService\`
- New GET handler in \`advisory/endpoints/severity_summary.rs\`
- Route registered in \`advisory/endpoints/mod.rs\`
- Integration tests covering valid SBOM, 404, empty results, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

Closes <owner>/<repo>#<number> (if GitHub Issue was extracted)"
```

## Step 11 -- Update Jira

### Update Git Pull Request custom field

Using the configured field `customfield_10875`:

```
jira.update_issue("TC-9201", fields={
  "customfield_10875": {
    "type": "doc",
    "version": 1,
    "content": [{
      "type": "paragraph",
      "content": [{
        "type": "inlineCard",
        "attrs": {"url": "<PR-URL>"}
      }]
    }]
  }
})
```

### Add implementation comment

Post a Jira comment summarizing the implementation:

- PR link
- Summary: Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint with `SeveritySummary` response model, `AdvisoryService.severity_summary()` method, and integration tests
- No deviations from plan
- Include the skill footer (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

### Transition to In Review

```
jira.transition_issue("TC-9201") -> In Review
```
