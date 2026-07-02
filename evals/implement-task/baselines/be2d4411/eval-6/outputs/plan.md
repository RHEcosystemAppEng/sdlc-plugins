# Implementation Plan for TC-9201

**Task:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains:
- **Repository Registry**: Present -- trustify-backend mapped to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Present -- Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
- **Code Intelligence**: Present -- serena_backend configured with rust-analyzer

All required sections are present. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description.

**Parsed sections:**
- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed (auto-mount)
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- returns `{ critical, high, medium, low, total }`
- **Acceptance Criteria:** 5 criteria (correct response shape, 404 handling, deduplication, zero defaults, performance)
- **Test Requirements:** 4 tests (valid SBOM, non-existent SBOM, empty advisories, deduplication)
- **Dependencies:** None
- **Bookend Type:** Not present (standard implementation flow)
- **Target PR:** Not present (new PR flow)

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

Check GitHub Issue custom field (`customfield_10747`): if populated, extract `owner/repo#number` for the PR Closes line.

## Step 1.5 -- Verify Description Integrity

Fetch comments via `jira.get_issue_comments("TC-9201")`. Locate the comment whose body starts with the marker string `[sdlc-workflow] Description digest:`.

One digest comment found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

- Comment `created` and `updated` timestamps are identical -- not edited.
- Stored tag: `sha256-md`, computed tag: `sha256-md` -- tags match.
- Hex digests match -- description unmodified since planning.

Proceed silently with no user prompt.

## Step 2 -- Verify Dependencies

The task states "Depends on: None". No dependency checks required. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`.
2. Assign TC-9201 to current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to In Progress: `jira.transition_issue("TC-9201") -> In Progress`.

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol`:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- inspect `AdvisoryService` struct and its existing methods (`fetch`, `list`, `search`). Understand method signatures: `&self, id: Id, tx: &Transactional<'_>` pattern. Understand return types (`Result<T, AppError>`).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- inspect route registration pattern. Understand how `Router::new().route("/path", get(handler))` is structured. See how existing handlers (`list`, `get`) are imported and mounted.

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- inspect existing module declarations (`pub mod summary;`, `pub mod details;`).

### 4.2 Inspect Reference Files

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- understand the existing endpoint pattern: `Path<Id>` extraction, service call, JSON response.
2. **`modules/fundamental/src/advisory/model/summary.rs`** -- understand `AdvisorySummary` struct, especially the `severity` field used for counting.
3. **`entity/src/sbom_advisory.rs`** -- understand the SBOM-Advisory join table structure for linking advisories to SBOMs.
4. **`common/src/error.rs`** -- understand `AppError` enum and `.context()` wrapping pattern.
5. **`modules/fundamental/src/sbom/endpoints/get.rs`** -- reference for `Path<Id>` usage in SBOM context and 404 handling.

### 4.3 Convention Conformance Analysis

Examine sibling files for established patterns:

- **`modules/fundamental/src/advisory/endpoints/list.rs`** and **`get.rs`** -- endpoint handlers
- **`modules/fundamental/src/advisory/model/summary.rs`** and **`details.rs`** -- model structs
- **`modules/fundamental/src/sbom/service/sbom.rs`** -- service method patterns

**Discovered conventions (from sibling analysis):**
- **Error handling:** All handlers use `Result<T, AppError>` with `.context()` wrapping
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern:** Extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Model structs:** Use `#[derive(Serialize, Deserialize, Debug)]` with serde
- **Module structure:** Each domain follows `model/ + service/ + endpoints/` layout
- **Route registration:** `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`

### 4.4 Test Convention Analysis

Examine sibling test files:

- **`tests/api/advisory.rs`** -- advisory endpoint integration tests
- **`tests/api/sbom.rs`** -- SBOM endpoint integration tests

**Discovered test conventions (from sibling test analysis):**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases:** 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Test structure:** Tests hit a real PostgreSQL test database
- **Setup:** Test fixtures created via service methods or direct DB insertion

### 4.5 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract CI check commands and code generation commands.

### 4.6 Documentation File Identification

Identify documentation files that may need updating:
- `docs/api.md` -- REST API reference (may need new endpoint documented)
- `README.md` -- repository overview

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
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Contains counts per severity level (Critical, High, Medium, Low) and a total,
/// enabling dashboard widgets to render severity breakdowns without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
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

### 6.2 Register the Model Module

In `modules/fundamental/src/advisory/model/mod.rs`, add:

```rust
pub mod severity_summary;
```

alongside existing `pub mod summary;` and `pub mod details;`.

### 6.3 Add `severity_summary` Method to `AdvisoryService`

In `modules/fundamental/src/advisory/service/advisory.rs`, add a new method following the existing `fetch`/`list` pattern:

```rust
/// Computes a severity summary for all advisories linked to a given SBOM.
///
/// Returns counts of unique advisories per severity level (Critical, High, Medium, Low)
/// and a total count. Advisories are deduplicated by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Join with advisory table to get severity field
    // 4. Deduplicate by advisory ID
    // 5. Count by severity level
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `entity::sbom_advisory` join table to find advisories linked to the SBOM
- Join with advisory entity to access severity information
- Use `AdvisorySummary.severity` field for severity level classification
- Deduplicate by advisory ID using `DISTINCT` or equivalent
- Return `AppError` with `.context()` wrapping for errors
- Return 404 (via AppError) when the SBOM ID does not exist

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts per severity level for all advisories
/// linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: AdvisoryService,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the Route

In `modules/fundamental/src/advisory/endpoints/mod.rs`, add the new route:

```rust
mod severity_summary;

// In the Router setup, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follow the existing pattern for how routes are registered in this file.

### 6.6 Code Quality Verification

- All new structs (`SeveritySummary`) have documentation comments
- All new public functions (`severity_summary`, `get_severity_summary`) have documentation comments
- Error handling follows `.context()` wrapping pattern
- No unrelated changes

### 6.7 Documentation Impact

- Check `docs/api.md` -- if it documents REST endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response format.
- No changes to `server/src/main.rs` needed (routes auto-mount via module registration as stated in the task).

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests:

### Test 1: Valid SBOM with Known Advisories

```rust
/// Verifies that the advisory summary endpoint returns correct severity counts
/// for an SBOM with known advisory links.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories of known severities (e.g., 2 critical, 1 high, 0 medium, 1 low)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK and the body contains correct counts
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, 2);
    // assert_eq!(body.high, 1);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 1);
    // assert_eq!(body.total, 4);
}
```

### Test 2: Non-Existent SBOM ID Returns 404

```rust
/// Verifies that requesting a severity summary for a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response status is 404 NOT FOUND
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with No Advisories Returns All Zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no advisory links

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are 0 and total is 0
    // assert_eq!(body.critical, 0);
    // assert_eq!(body.high, 0);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate Advisory Links Are Deduplicated

```rust
/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, 1); // not 2
}
```

Run tests to verify: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Test 1 validates response fields |
| Returns 404 for non-existent SBOM | Test 2 validates 404 behavior |
| Counts only unique advisories | Test 4 validates deduplication |
| All severity levels default to 0 | Test 3 validates zero defaults via `#[derive(Default)]` |
| Response time under 200ms for 500 advisories | Service uses single query with joins and group-by; no N+1 |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files are in scope:
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in Files to Create
- `modules/fundamental/src/advisory/model/mod.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in Files to Create
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in Files to Modify
- `tests/api/advisory_summary.rs` -- in Files to Create

Flag any out-of-scope files for user approval.

### Untracked File Check

Run `git status --short`, filter untracked files by proximity to modified directories, search for code references. Flag any referenced untracked files for user confirmation.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation Currency

If `docs/api.md` describes existing endpoints and was not updated in Step 6, update it now with the new endpoint.

### Documentation Scope Preservation

Verify any modified documentation still covers all original use cases.

### Cross-Section Reference Consistency

Verify file paths are consistent across Files to Modify, Files to Create, and Implementation Notes sections. No conflicts detected in the task description.

### Duplication Check

Search for existing severity counting or aggregation functions. Grep for `severity_summary`, `severity_count`, `aggregate_severity` patterns. If found, refactor to reuse.

### CI Checks from CONVENTIONS.md

Run any CI check commands extracted from CONVENTIONS.md. If none found, run `cargo build` and `cargo clippy` as standard checks. Fix any failures.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary`:
  - Input: HTTP request with SBOM ID path parameter
  - Processing: `get_severity_summary` handler extracts ID, calls `AdvisoryService::severity_summary`, which queries DB
  - Output: JSON response with `SeveritySummary` struct
  - **COMPLETE** -- all stages connected

### Contract & Sibling Parity

- `SeveritySummary` struct: standalone response type, no trait contract to implement
- Sibling parity with `get.rs` handler: error handling (`.context()` wrapping), path extraction (`Path<Id>`), service call pattern -- all consistent
- Sibling parity with `fetch`/`list` service methods: method signature pattern, `Transactional` usage -- all consistent

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary response model,
AdvisoryService.severity_summary method, and integration tests.

Implements TC-9201"

git push -u origin TC-9201
```

Create PR targeting main:

```bash
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts
for a given SBOM, enabling dashboard severity breakdown widgets.

- Add `SeveritySummary` response model with critical/high/medium/low/total counts
- Add `AdvisoryService::severity_summary` method with deduplication
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- Add integration tests for valid SBOM, 404, empty, and deduplication cases

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add implementation comment** to TC-9201 with:
   - PR link
   - Summary: Added severity aggregation endpoint with SeveritySummary model, service method, route registration, and integration tests
   - No deviations from the plan
   - Include skill footnote with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue("TC-9201") -> In Review
```
