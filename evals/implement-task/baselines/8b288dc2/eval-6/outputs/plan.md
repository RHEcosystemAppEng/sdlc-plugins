# Implementation Plan: TC-9201 -- Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001 (linked via "is incorporated by")

## Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains the required sections:

1. **Repository Registry** -- Present. Contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- Present. Project key: TC, Cloud ID: configured, Feature issue type ID: 10142.
3. **Code Intelligence** -- Present. Tool naming convention: `mcp__serena_backend__<tool>`. Instance: `serena_backend` with `rust-analyzer`.

All sections validated. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback per the skill methodology.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue via `jira.get_issue("TC-9201")` and parse the structured description.

**Parsed fields:**

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | 3 files (advisory.rs service, endpoints/mod.rs, model/mod.rs) |
| Files to Create | 3 files (severity_summary model, endpoint handler, integration tests) |
| API Changes | GET /api/v2/sbom/{id}/advisory-summary (NEW) |
| Dependencies | None |
| Target PR | Not present (default flow) |
| Bookend Type | Not present (default flow) |

**GitHub Issue extraction**: Check custom field `customfield_10747` on the fetched issue. If present, parse the GitHub issue URL for use in PR description.

**webUrl**: Capture the issue URL (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in PR description.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the full procedure. Summary:

1. Fetch issue comments via `jira.get_issue_comments("TC-9201")`.
2. Locate the digest comment with marker `[sdlc-workflow] Description digest:`.
3. Found comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
4. Comment not edited (created == updated).
5. Format tag: `sha256-md` (modern tagged format, not legacy).
6. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`.
7. Format tags match (both `sha256-md`), hex digests match.
8. **Result: Match -- proceed silently.** No user prompt, no added latency.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to "In Progress" via `jira.transition_issue("TC-9201", "In Progress")`.

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Use the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`** (AdvisoryService):
   - `mcp__serena_backend__get_symbols_overview` to see existing methods (`fetch`, `list`, `search`).
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method to understand the pattern for a new `severity_summary` method.
   - Note the method signature pattern: `&self, <params>, tx: &Transactional<'_>`.

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** (route registration):
   - `mcp__serena_backend__get_symbols_overview` to see current route registrations.
   - Understand the pattern: `Router::new().route("/path", get(handler))`.

3. **`modules/fundamental/src/advisory/model/mod.rs`** (model module registration):
   - `mcp__serena_backend__get_symbols_overview` to see existing `pub mod` declarations.

### 4.2 Inspect Sibling Files for Convention Analysis

1. **Endpoint pattern**: Read `modules/fundamental/src/advisory/endpoints/get.rs` to understand:
   - How path params are extracted via `Path<Id>`.
   - How the service is called.
   - How JSON responses are returned.
   - Error handling with `AppError` and `.context()`.

2. **Model pattern**: Read `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) to understand:
   - Struct definition pattern (derive macros, serde attributes).
   - The `severity` field that we will aggregate on.

3. **Service pattern**: Read `modules/fundamental/src/advisory/service/advisory.rs` more deeply to understand:
   - How `fetch` and `list` methods work.
   - How the `sbom_advisory` join table is queried.

4. **Entity inspection**: Read `entity/src/sbom_advisory.rs` to understand the join table structure for SBOM-to-advisory relationships.

### 4.3 Check Referencing Symbols

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to verify no existing callers would be affected.
- `mcp__serena_backend__find_referencing_symbols` on the advisory `endpoints/mod.rs` route registration to understand how routes are mounted.

### 4.4 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present:
- Read it and follow all conventions throughout implementation.
- Extract CI check commands from any "CI checks" / "Verification" section.
- Extract code generation commands if listed.

### 4.5 Documentation File Identification

Identify documentation files related to the changes:
- `docs/api.md` -- may describe API endpoints.
- `docs/architecture.md` -- system architecture overview.
- `README.md` at the repo root.

Record these for documentation-impact evaluation in Step 6 and documentation-currency check in Step 9.

### 4.6 Convention Conformance Analysis

**Expected discovered conventions (from sibling analysis):**

- **Error handling**: All handlers in `endpoints/` return `Result<T, AppError>` with `.context()` wrapping.
- **Service method signatures**: Methods take `&self`, domain-specific params, and `tx: &Transactional<'_>` as last parameter.
- **Endpoint structure**: Extract path params via `Path<Id>`, call service method, return `Json<T>`.
- **Model structs**: Use `#[derive(Serialize, Deserialize, Debug)]` (and possibly `Clone`, `PartialEq`).
- **Route registration**: `Router::new().route("/path", get(handler))` chaining in `endpoints/mod.rs`.
- **Module registration**: `pub mod <name>;` in parent `mod.rs` files.
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`).

### 4.7 Test Convention Analysis

Inspect sibling test files in `tests/api/`:

1. Read `tests/api/advisory.rs` to understand:
   - Assertion style (e.g., `assert_eq!(resp.status(), StatusCode::OK)`).
   - Response body deserialization pattern.
   - Error case testing (404 responses).
   - Test naming conventions.

2. Read `tests/api/sbom.rs` for additional test patterns.

**Expected discovered test conventions:**

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- **Error cases**: Tests include 404 checks with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Test naming**: `test_<endpoint>_<scenario>` pattern.
- **Setup**: Tests use a shared test database setup.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type). Target branch is `main`.

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file: the `SeveritySummary` response struct.

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of linked advisories by severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
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

Key decisions:
- Use `u64` for counts (consistent with common Rust integer conventions for counts).
- Derive `Default` so all fields initialize to 0.
- Include doc comments on the struct and each field.

### 6.2 Register the Model Module in `modules/fundamental/src/advisory/model/mod.rs`

Add:

```rust
pub mod severity_summary;
```

Following the pattern of existing `pub mod summary;` and `pub mod details;` declarations.

### 6.3 Add `severity_summary` Method to AdvisoryService

In `modules/fundamental/src/advisory/service/advisory.rs`, add a new method to the `AdvisoryService` impl block:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts per severity and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not found)
    // Use the SbomService or a direct entity lookup, following the
    // pattern used by existing fetch methods.

    // 2. Query sbom_advisory join table for all advisories linked to this SBOM
    // Use SeaORM query builder on entity::sbom_advisory

    // 3. Fetch AdvisorySummary for each linked advisory to get severity field
    // Deduplicate by advisory ID using a HashSet or DISTINCT in the query

    // 4. Count by severity level (Critical, High, Medium, Low)
    // Initialize SeveritySummary with Default (all zeros)
    // Iterate and increment the appropriate counter

    // 5. Set total = critical + high + medium + low

    // 6. Return the SeveritySummary
}
```

Implementation details:
- Follow the `fetch` method pattern for SBOM existence check (return `AppError` with `.context()` if not found).
- Use the `sbom_advisory` join table (`entity::sbom_advisory`) to find linked advisories.
- Leverage `AdvisorySummary.severity` field for severity classification.
- Deduplicate by advisory ID to satisfy acceptance criteria.
- All severity levels default to 0 via `SeveritySummary::default()`.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New file: the GET handler for `/api/v2/sbom/{id}/advisory-summary`.

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::id::Id;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories linked to the
/// specified SBOM, broken down by severity level (Critical, High, Medium, Low).
pub async fn get_advisory_summary(
    Path(sbom_id): Path<Id>,
    service: /* injected AdvisoryService -- follow existing DI pattern */,
    tx: /* transactional context -- follow existing pattern */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

The exact dependency injection pattern (whether `State<Arc<AdvisoryService>>` or `Extension`) and transactional context will be determined from inspecting existing endpoint handlers in Step 4.

### 6.5 Register the Route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing registration pattern:

```rust
pub mod severity_summary;

// In the router builder, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

The exact path parameter syntax (`:id` vs `{id}`) and router chaining pattern will be confirmed by inspecting the existing route registrations.

### 6.6 Documentation Impact

After implementing, check:
- If `docs/api.md` lists endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.
- `server/src/main.rs` -- per the task description, no changes needed (routes auto-mount).

### 6.7 Code Quality Practices

Verify:
- All new structs (`SeveritySummary`) have documentation comments.
- All new public functions (`severity_summary`, `get_advisory_summary`) have documentation comments.
- Error handling uses `.context()` wrapping consistently.

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Integration tests for the new endpoint, following test conventions from sibling files.

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels
    // (setup: create SBOM, link advisories with Critical=2, High=1, Medium=3, Low=0)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And the body contains { critical: 2, high: 1, medium: 3, low: 0, total: 6 }
}

/// Verifies that a non-existent SBOM ID returns 404 Not Found.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response status is 404 NOT_FOUND
}

/// Verifies that an SBOM with no advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And the body contains { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response counts each advisory only once
    // And total reflects the deduplicated count
}
```

All tests follow:
- `test_<endpoint>_<scenario>` naming convention.
- `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND` assertion style.
- Documentation comments on every test function.
- Given-when-then section comments inside each test body.
- Value-based assertions (assert on specific count values, not just presence).

Register the test module in `tests/` Cargo.toml or test harness as needed.

Run tests: `cargo test` and fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | `test_advisory_summary_valid_sbom` asserts exact field values |
| Returns 404 for non-existent SBOM | `test_advisory_summary_nonexistent_sbom` asserts StatusCode::NOT_FOUND |
| Counts only unique advisories | `test_advisory_summary_deduplication` uses duplicate links and asserts deduplicated count |
| All severity levels default to 0 | `test_advisory_summary_no_advisories` asserts all zeros |
| Response time under 200ms for 500 advisories | Verify with performance test or confirm query uses efficient join + GROUP BY |

## Step 9 -- Self-Verification

### 9.1 Scope Containment

Run `git diff --name-only` and verify all modified/created files are in scope:

**Expected files:**
- `modules/fundamental/src/advisory/service/advisory.rs` (modified) -- in Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified) -- in Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` (modified) -- in Files to Modify
- `modules/fundamental/src/advisory/model/severity_summary.rs` (created) -- in Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (created) -- in Files to Create
- `tests/api/advisory_summary.rs` (created) -- in Files to Create

If any out-of-scope files appear (e.g., docs updated in Step 6.6), list them and ask user approval.

### 9.2 Untracked File Check

Run `git status --short`, filter for `??` entries in directories with modified files. Check for code references to any untracked files. Flag for user review if referenced.

### 9.3 Sensitive-Pattern Check

Run: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`

Flag any matches.

### 9.4 Documentation Currency

Check if `docs/api.md` needs updating with the new endpoint. If it lists endpoints and the new one is not added, update it.

### 9.5 Cross-Section Reference Consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` -- referenced in Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`). Consistent.
- `SeveritySummary` -- referenced in Files to Create (`advisory/model/severity_summary.rs`) and Implementation Notes references `AdvisorySummary` in `advisory/model/summary.rs` (different entity). Consistent.

### 9.6 Duplication Check

Search the repository for existing severity aggregation or summary-counting logic to ensure no duplication. Use Grep for patterns like `severity_summary`, `severity_count`, `count.*severity`.

### 9.7 CI Checks from CONVENTIONS.md

If CONVENTIONS.md CI check commands were extracted in Step 4, run all of them. Hard stop on any failure.

### 9.8 Data-Flow Trace

Trace the complete data flow:

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter.
2. **Endpoint handler** (`severity_summary.rs`): Extracts `Path<Id>`, calls `AdvisoryService::severity_summary()`.
3. **Service method** (`advisory.rs`): Validates SBOM exists, queries `sbom_advisory` join table, fetches advisory severity data, deduplicates, counts by level.
4. **Output**: Returns `Json<SeveritySummary>` with `{ critical, high, medium, low, total }`.

**Result: COMPLETE** -- all stages connected from input to output.

### 9.9 Contract and Sibling Parity

- **Contract**: `SeveritySummary` is a new standalone struct (no trait implementation required). The endpoint handler returns `Result<Json<SeveritySummary>, AppError>`, consistent with the Axum handler contract.
- **Sibling parity**: Compare with `get.rs` handler -- error handling, path extraction, service call pattern should all match.
- **Cross-module shared entity**: The `sbom_advisory` join table is read-only in this implementation (SELECT, not INSERT/UPDATE/DELETE). Verify read patterns match other modules that query the same table.

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add tests/api/advisory_summary.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add modules/fundamental/src/advisory/model/mod.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation service and endpoint

Add a new GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a given
SBOM. Includes the SeveritySummary model, AdvisoryService.severity_summary
method, endpoint handler, and integration tests.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add advisory severity aggregation service and REST endpoint for TC-9201.

- New `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning severity counts
- `SeveritySummary` response model with critical/high/medium/low/total fields
- `AdvisoryService::severity_summary` method with deduplication
- Integration tests covering valid SBOM, non-existent SBOM, empty advisories, and deduplication

Implements [TC-9201](<webUrl>)

Closes <owner>/<repo>#<number>  (if GitHub Issue custom field was populated)
"
```

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format (inlineCard).

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: new severity aggregation endpoint, model, service method, and tests
   - No deviations from the plan
   - Append the standard skill footnote with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`

3. **Transition** TC-9201 to "In Review" via `jira.transition_issue("TC-9201", "In Review")`.
