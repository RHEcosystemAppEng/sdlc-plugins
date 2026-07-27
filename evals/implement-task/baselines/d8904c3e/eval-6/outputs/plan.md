# Implementation Plan -- TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

- **Jira Issue:** TC-9201
- **Parent Feature:** TC-9001
- **Repository:** trustify-backend
- **Target Branch:** main
- **Bookend Type:** None (standard implementation task)
- **Target PR:** None (new branch and PR)
- **Dependencies:** None

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured with rust-analyzer

All sections verified. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all Jira operations. If MCP fails, prompt user for REST API fallback using `scripts/jira-client.py`.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue:

```
jira.get_issue("TC-9201")
```

### Parsed sections

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns counts per severity level (Critical, High, Medium, Low) plus a total.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes:** Follow existing endpoint/service patterns, use `sbom_advisory` join table, return `AppError` with `.context()` wrapping
- **Acceptance Criteria:** 5 criteria (correct response shape, 404 handling, deduplication, zero defaults, performance)
- **Test Requirements:** 4 test cases
- **Bookend Type:** None
- **Target PR:** None
- **Dependencies:** None

### GitHub Issue extraction

Look up `GitHub Issue custom field: customfield_10747` from CLAUDE.md. Read the field value from the fetched issue. If present, parse `owner/repo#number` for use in PR description. If empty, skip.

### Issue webUrl

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for the PR description.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the detailed handling.

Summary: One digest comment found with marker `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890...`. Comment timestamps are identical (not edited). Format tags both `sha256-md` (match). Hex digests match. Proceed silently.

## Step 2 -- Verify Dependencies

Task description states "Dependencies: None". No dependency checks needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID:
   ```
   jira.user_info()
   ```
2. Assign the task:
   ```
   jira.edit_issue("TC-9201", assignee=<current-user-account-id>)
   ```
3. Transition to In Progress:
   ```
   jira.transition_issue("TC-9201") -> In Progress
   ```

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify using Serena

Tools are called as `mcp__serena_backend__<tool>`.

**Files to Modify:**

1. `modules/fundamental/src/advisory/service/advisory.rs`
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct, `fetch`, `list`, `search` methods
   - `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` to understand the method signature pattern: `&self, id: Id, tx: &Transactional<'_>` and return type `Result<T, AppError>`
   - `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` to see query pattern

2. `modules/fundamental/src/advisory/endpoints/mod.rs`
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern
   - Look for `Router::new().route(...)` pattern

3. `modules/fundamental/src/advisory/model/mod.rs`
   - `mcp__serena_backend__get_symbols_overview` to see existing module declarations (`pub mod summary; pub mod details;`)

### 4.2 Inspect reference files

1. `modules/fundamental/src/advisory/endpoints/get.rs`
   - `mcp__serena_backend__find_symbol` with `include_body=true` to see endpoint handler pattern: `Path<Id>` extraction, service call, JSON response

2. `modules/fundamental/src/advisory/model/summary.rs`
   - `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to see the `severity` field type and structure

3. `entity/src/sbom_advisory.rs`
   - `mcp__serena_backend__get_symbols_overview` to understand the join table entity structure

4. `common/src/error.rs`
   - `mcp__serena_backend__find_symbol("AppError", include_body=true)` to see error enum and `IntoResponse` implementation

### 4.3 Backward compatibility check

- `mcp__serena_backend__find_referencing_symbols("AdvisoryService")` to identify all callers and confirm the new method will not conflict

### 4.4 Convention conformance analysis

**Sibling files to analyze:**

- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- endpoint handler patterns
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- model struct patterns
- `modules/fundamental/src/sbom/service/sbom.rs` -- service method patterns for comparison

**Expected discovered conventions:**

- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern:** Extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Model pattern:** Structs derive `Serialize, Deserialize, Clone, Debug` and use `#[serde(rename_all = "camelCase")]`
- **Route registration:** `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Response types:** Single-entity endpoints return the struct directly via `Json<T>`, list endpoints use `PaginatedResults<T>`

### 4.5 Test convention analysis

**Sibling test files to analyze:**

- `tests/api/advisory.rs` -- advisory endpoint tests
- `tests/api/sbom.rs` -- SBOM endpoint tests

**Expected discovered test conventions:**

- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation:** Check status code, then deserialize JSON body, then assert on field values
- **Error cases:** Test 404 with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Setup:** Tests use a real PostgreSQL test database with fixture data

### 4.6 Documentation file identification

- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating with new endpoint)
- `CONVENTIONS.md` at repository root -- check for CI commands and code conventions

### 4.7 CONVENTIONS.md lookup

Read `CONVENTIONS.md` at the repository root. Extract:
- Any CI check commands (formatting, linting, compilation checks)
- Any code generation commands (OpenAPI spec generation if applicable)

Record verification commands for use in Step 9.

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file -- SeveritySummary response struct:

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for a given SBOM.
///
/// Aggregates the number of unique advisories at each severity level
/// linked to a specific SBOM, enabling dashboard severity breakdowns.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
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

Derive `Default` to ensure all fields start at 0.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module declaration:

```rust
pub mod severity_summary;
```

alongside existing `pub mod summary;` and `pub mod details;`.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService`, following the existing `fetch`/`list` pattern:

```rust
/// Retrieves a severity summary for all advisories linked to the given SBOM.
///
/// Counts unique advisories at each severity level (Critical, High, Medium, Low)
/// by querying the `sbom_advisory` join table and aggregating by severity.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, fetch its AdvisorySummary to get severity
    // 5. Count by severity level and build SeveritySummary
}
```

Key implementation details:
- First verify the SBOM exists by attempting to fetch it; return `AppError` with 404 context if not found
- Use the `sbom_advisory` entity to join SBOMs to advisories
- Deduplicate by advisory ID using a HashSet or DISTINCT query
- Read the `severity` field from `AdvisorySummary` for each advisory
- Map severity strings to the corresponding counter in `SeveritySummary`
- Use `.context("Failed to fetch severity summary")` for error wrapping

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler following the pattern in `get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

/// GET handler for `/api/v2/sbom/{id}/advisory-summary`.
///
/// Returns a severity count summary for all advisories linked to the given SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* injected Transactional */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route in the existing router:

```rust
mod severity_summary;

// In the router builder, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follow the exact pattern used for existing route registrations in this file.

### 6.6 Documentation impact

Check `docs/api.md` for API documentation. If it documents existing endpoints, add an entry for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with:
- Endpoint path and method
- Path parameters (`id` -- SBOM ID)
- Response schema (critical, high, medium, low, total)
- Example response

### 6.7 Code quality verification

Verify that all new symbols (SeveritySummary struct, severity_summary method, get_severity_summary handler) have documentation comments. Verify serde attributes and derives match sibling conventions.

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Follow the test conventions discovered in Step 4 (assertion style, naming, database setup).

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels
    // (set up test database with SBOM, linked advisories via sbom_advisory)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response has status 200 and correct severity counts
    // assert_eq!(resp.status(), StatusCode::OK);
    // Deserialize body as SeveritySummary
    // assert_eq!(summary.critical, expected_critical_count);
    // assert_eq!(summary.high, expected_high_count);
    // etc.
    // assert_eq!(summary.total, expected_total);
}

/// Verifies that a non-existent SBOM ID returns a 404 response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response has status 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all severity counts are 0 and total is 0
    // assert_eq!(summary.critical, 0);
    // assert_eq!(summary.high, 0);
    // assert_eq!(summary.medium, 0);
    // assert_eq!(summary.low, 0);
    // assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links in sbom_advisory

    // When requesting the advisory summary

    // Then each advisory is counted only once
    // (total should equal count of unique advisory IDs, not total link rows)
}
```

All test functions have doc comments explaining what they verify, and non-trivial tests use given-when-then section comments.

### Run tests

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Verified via `test_advisory_summary_valid_sbom` -- response contains critical, high, medium, low, total fields |
| Returns 404 for non-existent SBOM | Verified via `test_advisory_summary_nonexistent_sbom` |
| Counts only unique advisories | Verified via `test_advisory_summary_deduplicates` |
| All severity levels default to 0 | Verified via `test_advisory_summary_no_advisories` |
| Response time under 200ms for 500 advisories | Verify via performance test or query plan analysis; the query uses indexed joins on sbom_advisory |

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

**Potentially out-of-scope:** `docs/api.md` if updated for documentation impact. Flag to user if modified.

`server/src/main.rs` is listed in Files to Modify as "no changes needed" -- verify it was not modified.

### Untracked file check

Run `git status --short`, filter for `??` entries in directories where implementation work occurred. Check for references in staged code (e.g., `include_str!` patterns). Flag any referenced untracked files for user approval.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation currency

If `docs/api.md` describes existing endpoints and the new endpoint was not already documented in Step 6, update it now.

### Cross-section reference consistency

Verify file paths are consistent across Files to Modify, Files to Create, and Implementation Notes:

- `AdvisoryService` -- referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent
- `AdvisorySummary` -- referenced in Implementation Notes (`advisory/model/summary.rs`) -- this is an existing file being read, not modified -- consistent
- `SeveritySummary` -- referenced in Files to Create (`advisory/model/severity_summary.rs`) -- consistent

### Duplication check

Search for existing severity aggregation or counting logic:
- `mcp__serena_backend__search_for_pattern("severity_summary")` or `mcp__serena_backend__search_for_pattern("severity.*count")`
- Verify no existing utility performs this aggregation

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md in Step 4. Fix any failures. Hard stop on any non-zero exit.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> fetch advisory severities -> aggregate counts -> return `Json<SeveritySummary>` -- **COMPLETE**

### Contract and sibling parity

- `SeveritySummary` derives `Serialize, Deserialize` matching sibling model structs
- `get_severity_summary` handler follows the same `Path<Id>` + service call + Json return pattern as `get.rs`
- `severity_summary` service method follows the same `&self, id, tx` signature pattern as `fetch` and `list`
- Error handling uses `AppError` with `.context()` matching all sibling handlers

## Step 10 -- Commit and Push

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If upstream exists, use fork-aware PR creation.

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add tests/api/advisory_summary.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add modules/fundamental/src/advisory/model/mod.rs
# Add docs/api.md if modified

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary method,
endpoint handler, and integration tests.

Implements TC-9201"
```

### Push and create PR

```bash
git push -u origin TC-9201
```

Create PR with `--base main`:

```bash
gh pr create --base main \
  --title "feat(api): add advisory severity aggregation endpoint" \
  --body "## Summary

- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint returning severity counts per level
- Add \`SeveritySummary\` response model with critical, high, medium, low, and total fields
- Add \`AdvisoryService::severity_summary\` method with deduplication by advisory ID
- Add integration tests for valid SBOM, non-existent SBOM, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

### Set Git Pull Request custom field

Look up `Git Pull Request custom field: customfield_10875` from CLAUDE.md. Update with ADF:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

### Add comment

Post a comment to TC-9201 with:
- PR link
- Summary of changes: added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
- No deviations from the plan

Comment ends with the standard footnote (horizontal rule + "This comment was AI-generated by sdlc-workflow/implement-task v0.13.7.").

### Transition to In Review

```
jira.transition_issue("TC-9201") -> In Review
```
