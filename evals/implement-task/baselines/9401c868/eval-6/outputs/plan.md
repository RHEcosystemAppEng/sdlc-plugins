# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

- **Jira Key**: TC-9201
- **Summary**: Add advisory severity aggregation service and endpoint
- **Repository**: trustify-backend
- **Target Branch**: main
- **Parent Feature**: TC-9001 (is incorporated by)
- **Dependencies**: None
- **Bookend Type**: None (standard implementation task)
- **Target PR**: None (new branch and PR flow)

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID `10142`
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` (rust-analyzer)

All sections are valid. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all Jira operations. If MCP fails, fall back to REST API via `scripts/jira-client.py` after user confirmation.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description.

### Parsed Sections

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed (auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`, use `sbom_advisory` join table, count by severity from `AdvisorySummary.severity` field, return `Result<T, AppError>` with `.context()`, use Axum `Json` extractor
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 test cases
- **Target PR**: not present
- **Bookend Type**: not present
- **GitHub Issue custom field**: `customfield_10747` -- check issue fields for value; if present, extract and store reference for PR description
- **Issue webUrl**: captured for use in PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`)

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for detailed walkthrough. Summary:

1. Fetch comments on TC-9201
2. Locate the digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890...`
3. Comment `created` equals `updated` -- no edit warning
4. Extract format tag `sha256-md` and hex digest
5. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
6. Format tags match (`sha256-md` == `sha256-md`)
7. Hex digests match
8. **Proceed silently** -- no user prompt needed

## Step 2 -- Verify Dependencies

The task lists `Dependencies: None`. No prerequisite verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID: `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition TC-9201 to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify using Serena (`serena_backend`)

1. **Get symbols overview** of files to modify:
   - `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` -- understand AdvisoryService struct, existing methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/mod.rs")` -- understand route registration pattern
   - `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")` -- understand module declarations

2. **Read specific symbols** with `include_body=true`:
   - `mcp__serena_backend__find_symbol("AdvisoryService")` -- full struct definition
   - `mcp__serena_backend__find_symbol("fetch")` in `advisory.rs` -- understand method signature pattern (params: `&self, id: Id, tx: &Transactional<'_>`)
   - `mcp__serena_backend__find_symbol("list")` in `advisory.rs` -- understand return type pattern

3. **Check referencing symbols** for backward compatibility:
   - `mcp__serena_backend__find_referencing_symbols("AdvisoryService")` -- identify all callers

4. **Search for patterns**:
   - `mcp__serena_backend__search_for_pattern("sbom_advisory")` in `entity/src/sbom_advisory.rs` -- understand the join table structure
   - `mcp__serena_backend__search_for_pattern("severity")` in `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary.severity field type

### 4.2 Inspect sibling files for convention conformance

**Production code siblings:**
- `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/get.rs")` -- endpoint handler pattern
- `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/list.rs")` -- list handler pattern
- `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/details.rs")` -- model struct pattern

**Test siblings:**
- `mcp__serena_backend__get_symbols_overview("tests/api/advisory.rs")` -- test patterns, assertions, setup

### 4.3 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read it and extract:
- CI check commands (formatting, linting, compilation)
- Code generation commands
- Naming and structure conventions

### 4.4 Documentation file identification

Look for documentation files related to modified code:
- `README.md` at repository root
- `docs/api.md` -- REST API reference
- `docs/architecture.md` -- architecture overview

Record these for documentation-impact evaluation in Step 6 and currency check in Step 9.

### 4.5 Convention conformance analysis output

Expected discovered conventions (based on repository structure):

- **Error handling**: handlers use `Result<T, AppError>` with `.context()` wrapping
- **Naming**: snake_case for functions and variables, PascalCase for types/structs
- **Endpoint registration**: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Service method signature**: `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- **Model pattern**: derive `Serialize, Deserialize`, separate file per model type
- **Test assertions**: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Module registration**: `pub mod <name>;` in parent `mod.rs`

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
/// Aggregates the number of unique advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
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

Follows the sibling model pattern (`summary.rs`, `details.rs`) with derives and documentation.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module declaration:

```rust
pub mod severity_summary;
```

Place it alphabetically among existing module declarations, following the established pattern.

### 6.3 Add `severity_summary` method to `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService` following the existing `fetch`/`list` pattern:

```rust
/// Computes an aggregated severity summary for all advisories linked to the given SBOM.
///
/// Joins through the `sbom_advisory` table, deduplicates by advisory ID,
/// and counts advisories at each severity level (Critical, High, Medium, Low).
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to this SBOM
    // 2. Join with advisory table to get severity field
    // 3. Deduplicate by advisory ID (HashSet or DISTINCT in query)
    // 4. Count by severity level
    // 5. Return SeveritySummary with counts and total
    // If SBOM ID does not exist, return 404 AppError consistent with existing endpoints
}
```

Key implementation details:
- Use `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) to join SBOM to advisories
- Leverage `AdvisorySummary.severity` field for severity classification
- Deduplicate by advisory ID (use `DISTINCT` in SQL query or `HashSet` in Rust)
- Default all severity counts to 0 when no advisories exist
- Return `AppError` with `.context()` for error wrapping
- Return 404 when SBOM ID does not exist (verify SBOM existence first)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns an aggregated severity summary of all advisories linked to the
/// specified SBOM, with counts per severity level and a total.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transactional context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Defensive property access: guard against null/absent severity values from the advisory data using `.unwrap_or_default()` or similar Rust idiom.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route in the existing router:

```rust
mod severity_summary;

// In the route registration block:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 `server/src/main.rs`

No changes needed -- routes auto-mount via module registration as noted in the task description.

### 6.7 Documentation impact

- No **Documentation Updates** section in the task description.
- Check `docs/api.md` -- if it lists REST endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation.
- Keep updates lightweight and scoped to the new endpoint only.

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Write integration tests matching the sibling test patterns in `tests/api/advisory.rs`:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (setup: create test SBOM, link advisories with Critical=2, High=1, Medium=3, Low=0)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response should contain correct counts
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, 2)
    // assert_eq!(body.high, 1)
    // assert_eq!(body.medium, 3)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 6)
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response should be 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all counts should be zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory ID linked twice)

    // When requesting the advisory summary

    // Then the duplicate should be counted only once
    // assert_eq!(body.total, expected_unique_count)
    // Verify specific severity counts reflect deduplicated values
}
```

Test conventions applied:
- Value-based assertions (assert on actual severity counts, not just collection length)
- Documentation comment on every test function
- Given-when-then section comments for each non-trivial test
- `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests

### Run tests

```bash
cargo test -p trustify-fundamental
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Verified by `test_severity_summary_with_known_advisories` -- asserts all fields present with correct values |
| 2 | Returns 404 for non-existent SBOM ID | Verified by `test_severity_summary_not_found` |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_severity_summary_deduplication` |
| 4 | All severity levels default to 0 when no advisories exist | Verified by `test_severity_summary_empty` |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient SQL query design (DISTINCT + GROUP BY at the database level avoids loading all advisory objects into memory) |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- in scope
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in scope
- `modules/fundamental/src/advisory/model/mod.rs` -- in scope

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in scope
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in scope
- `tests/api/advisory_summary.rs` -- in scope

If any out-of-scope files appear, list them and ask user for approval.

Note: `server/src/main.rs` is listed in Files to Modify as "no changes needed" -- confirm it is not in the diff.

### Untracked file check

Run `git status --short`, filter for `??` entries in directories with modified files. Flag any referenced untracked files for user approval.

### Dead parameter detection

Scan modified functions for parameters no longer referenced after changes. Since we are adding new methods (not removing code from existing ones), this is unlikely to flag anything, but verify.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Confirm no secrets are staged.

### Documentation currency

Check if `docs/api.md` describes the advisory endpoints. If it does, ensure the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint is documented (done in Step 6.7).

### Documentation scope preservation

Not applicable -- no documentation sections are being replaced.

### Duplication check

Search for existing severity aggregation logic:
- Grep for `severity_summary`, `severity_count`, `SeveritySummary` in the codebase
- Verify no existing utility performs the same aggregation
- If found, refactor to reuse

### Symbol deduplication

Before declaring `SeveritySummary`, search for existing definitions:
- Grep for `SeveritySummary`, `severity_summary`, `SeverityCount` across the codebase
- If found, import and reuse rather than declaring a new type

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` (if found):
- Formatting: `cargo fmt --check`
- Linting: `cargo clippy`
- Compilation: `cargo check`
- Hard stop on any non-zero exit

### Module-level test requirement (Rust)

Run `cargo metadata --no-deps --format-version 1` to resolve package names for modified files. Run tests for each affected crate:

```bash
cargo test -p <crate-name-for-fundamental>
```

Hard stop on test failure.

### Data-flow trace

Trace the new feature's data lifecycle:

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter
2. **Processing**: Axum extracts path param -> handler calls `AdvisoryService.severity_summary()` -> service queries `sbom_advisory` join table -> joins with advisory table -> deduplicates by advisory ID -> counts by severity level -> builds `SeveritySummary` struct
3. **Output**: Axum serializes `SeveritySummary` to JSON -> HTTP 200 response with `{ critical, high, medium, low, total }`

All stages are connected. The flow is complete.

### Query-scope verification

The service method queries advisories linked to a specific SBOM ID (filtered by `sbom_id` parameter). This is correctly scoped -- no broad/unfiltered query.

### Contract & sibling parity

| Check | Result |
|-------|--------|
| **Contract** | `severity_summary` method follows `AdvisoryService` method signature pattern (`&self, id: Id, tx: &Transactional<'_>`) and returns `Result<T, AppError>` |
| **Sibling parity** | Handler follows `get.rs` pattern: Path extraction, service call, Json response, `.context()` error wrapping |
| **Cross-module entity** | Uses `sbom_advisory` join table read-only (no writes) -- no transaction/locking concerns |
| **Caller-site** | Endpoint handler follows the same invocation pattern as existing `get` and `list` handlers |

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Stage any documentation updates if applicable

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated advisory severity counts (critical, high, medium, low, total)
for a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"
```

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

- If upstream exists: parse `<upstream-owner/repo>` and `<fork-owner>` from remote URLs
- If not: use default `gh pr create` behavior

### Push and create PR

```bash
git push -u origin TC-9201
```

Create PR with `--base main`:

```bash
gh pr create --base main \
  --title "feat(advisory): add severity aggregation endpoint" \
  --body "## Summary

- Add GET /api/v2/sbom/{id}/advisory-summary endpoint returning aggregated advisory severity counts per SBOM
- Add SeveritySummary response model, AdvisoryService.severity_summary() method, and endpoint handler
- Add integration tests covering correct counts, 404, empty SBOM, and deduplication

Implements [TC-9201](<webUrl>)

## Test Plan

- [x] Test valid SBOM with known advisories returns correct severity counts
- [x] Test non-existent SBOM ID returns 404
- [x] Test SBOM with no advisories returns all zeros
- [x] Test duplicate advisory links are deduplicated"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

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

2. **Add comment** to TC-9201:

```
jira.add_comment("TC-9201", "Implementation complete for TC-9201.

**Changes:**
- Created `SeveritySummary` response model in `modules/fundamental/src/advisory/model/severity_summary.rs`
- Added `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`
- Created GET handler in `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- Registered route in `modules/fundamental/src/advisory/endpoints/mod.rs`
- Added integration tests in `tests/api/advisory_summary.rs`

**PR:** <PR-URL>

No deviations from the plan.

[footnote per shared/comment-footnote.md]")
```

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue("TC-9201") -> In Review
```
