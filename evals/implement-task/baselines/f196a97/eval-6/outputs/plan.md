# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001 (linked via "is incorporated by")

## Description Integrity

The description digest check passed (Step 1.5): format tags match (`sha256-md`), hex digests match. Proceeding silently with implementation.

## Parsed Task Structure

### Repository
trustify-backend

### Target Branch
main

### Description
Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.

### Files to Modify
1. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
3. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module

### Files to Create
1. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
3. `tests/api/advisory_summary.rs` -- integration tests for the new endpoint

### API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`

### Dependencies
None -- no prerequisite tasks to verify.

### Bookend Type
Not present -- standard implementation flow.

### Target PR
Not present -- create a new branch and PR.

### GitHub Issue
Check `customfield_10747` on the fetched issue. If present, extract the GitHub issue URL and parse `owner/repo#number` for use in the PR description's `Closes` line.

---

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed immediately.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve the current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`.
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`.

## Step 4 -- Understand the Code

### 4.1 CONVENTIONS.md Lookup

Look up the Repository Registry in CLAUDE.md: trustify-backend is at `./` with Serena instance `serena_backend`. Check for `CONVENTIONS.md` at the repository root using `mcp__serena_backend__list_dir` or Read. If present, read it and extract:
- Code conventions (naming, structure, patterns)
- CI check commands (for Step 9)
- Code generation commands (for Step 9)

### 4.2 Inspect Files to Modify

Use Serena to examine the existing codebase:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** (AdvisoryService):
   - `mcp__serena_backend__get_symbols_overview` to see the service structure
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` and `list` methods to understand the pattern for service methods (parameter types, return types, transaction handling)
   - Identify how `Transactional` is used, how errors are wrapped with `.context()`

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** (route registration):
   - `mcp__serena_backend__get_symbols_overview` to see existing route registrations
   - Understand the `Router::new().route()` pattern and how handlers are mounted

3. **`modules/fundamental/src/advisory/model/mod.rs`** (model module registration):
   - Read to see how existing model sub-modules are declared (`pub mod summary;`, `pub mod details;`)

4. **`modules/fundamental/src/advisory/model/summary.rs`** (AdvisorySummary):
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` with `include_body=true` to understand the `severity` field type and derive macros used

5. **`entity/src/sbom_advisory.rs`** (join table):
   - `mcp__serena_backend__get_symbols_overview` to understand the SBOM-Advisory relationship and how to query it

6. **`common/src/error.rs`** (error handling):
   - `mcp__serena_backend__find_symbol` on `AppError` to understand error variants and the `.context()` pattern

### 4.3 Inspect Sibling Files for Patterns

Examine sibling endpoint files to discover conventions:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- the primary reference for endpoint handler pattern (Path extraction, service call, JSON response)
2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- list handler for comparison
3. **`modules/fundamental/src/sbom/endpoints/get.rs`** -- cross-module sibling to confirm pattern consistency

Expected conventions to discover:
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Path extraction**: `Path<Id>` extractor from Axum
- **Response**: return struct directly (Axum `Json` handles serialization)
- **Service access**: service injected via Axum state/extension
- **Naming**: service methods follow `verb_noun` pattern

### 4.4 Test Convention Analysis

Examine sibling test files:

1. **`tests/api/advisory.rs`** -- advisory endpoint tests
2. **`tests/api/sbom.rs`** -- SBOM endpoint tests
3. **`tests/api/search.rs`** -- search endpoint tests

Expected test conventions to discover:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Error cases**: 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>`
- **Setup**: test database initialization patterns, fixture creation
- **Parameterized tests**: check for `#[rstest]` / `#[case]` usage in siblings

### 4.5 Documentation File Identification

Identify documentation files for documentation impact evaluation:
- `README.md` at repository root
- `docs/api.md` -- REST API reference (likely needs updating for new endpoint)
- `docs/architecture.md` -- system architecture overview

### 4.6 Backward Compatibility Check

Use `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` -- to confirm no callers will be affected by adding a new method
- Route registration in `endpoints/mod.rs` -- to confirm adding a new route won't conflict

---

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

---

## Step 6 -- Implement Changes

### 6.1 Create SeveritySummary Response Struct

**File**: `modules/fundamental/src/advisory/model/severity_summary.rs` (NEW)

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Summary of advisory severity counts for a given SBOM.
///
/// Provides counts per severity level (Critical, High, Medium, Low) and a total,
/// enabling dashboard widgets to render severity breakdowns without client-side counting.
#[derive(Clone, Debug, Default, Serialize, ToSchema)]
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

Follow the derive macro pattern from sibling structs (`AdvisorySummary`, `SbomSummary`) -- use `Serialize`, `ToSchema`, and any other derives they use. Apply `Default` so all counts initialize to 0.

### 6.2 Register Model Module

**File**: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

Add `pub mod severity_summary;` following the pattern of existing module declarations (`pub mod summary;`, `pub mod details;`).

### 6.3 Add `severity_summary` Method to AdvisoryService

**File**: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

Add a new method following the pattern of `fetch` and `list`:

```rust
/// Computes the severity summary for all advisories linked to a given SBOM.
///
/// Returns counts per severity level (Critical, High, Medium, Low) and a total.
/// Advisories are deduplicated by advisory ID before counting.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table to find advisories linked to this SBOM
    // 2. Join with advisory table to get severity fields
    // 3. Deduplicate by advisory ID
    // 4. Count by severity level
    // 5. Return SeveritySummary with counts and total
}
```

Implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- Join with advisory data to access the `severity` field from `AdvisorySummary`
- Use `HashSet` or `DISTINCT` to deduplicate by advisory ID
- Count each severity level, default to 0 for missing levels
- Wrap errors with `.context("Failed to compute severity summary")` matching the error pattern in `common/src/error.rs`
- Verify the SBOM exists first -- if not, return a 404-equivalent error consistent with existing SBOM endpoints

### 6.4 Create Endpoint Handler

**File**: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (NEW)

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

/// GET handler for /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts per level (Critical, High, Medium, Low)
/// and a total for all advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* extracted from Axum state, following sibling pattern */,
    tx: /* transaction extraction, following sibling pattern */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the exact pattern from `modules/fundamental/src/advisory/endpoints/get.rs`:
- Path parameter extraction via `Path<Id>`
- Service access via Axum state/extension (match how siblings access it)
- Transaction handling (match the `Transactional` pattern)
- Return `Json<SeveritySummary>` directly

### 6.5 Register Route

**File**: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

Add the new route registration following the existing `Router::new().route()` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Import the new handler module and register it alongside existing routes.

### 6.6 Documentation Impact

Check if `docs/api.md` lists existing endpoints. If so, add the new endpoint:
- `GET /api/v2/sbom/{id}/advisory-summary` -- returns severity summary with `{ critical, high, medium, low, total }`

This is a new public API endpoint, so API documentation must be updated.

---

## Step 7 -- Write Tests

**File**: `tests/api/advisory_summary.rs` (NEW)

Follow test conventions discovered from `tests/api/advisory.rs` and `tests/api/sbom.rs`.

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisory links returns the correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels
    // (set up test DB with SBOM, link advisories of various severities)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, expected_critical);
    // assert_eq!(body.high, expected_high);
    // assert_eq!(body.medium, expected_medium);
    // assert_eq!(body.low, expected_low);
    // assert_eq!(body.total, expected_total);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent_id}/advisory-summary

    // Then the response is 404 Not Found
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, 0);
    // assert_eq!(body.high, 0);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated in the count

```rust
/// Verifies that duplicate advisory links for the same SBOM are deduplicated in severity counts.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the count reflects unique advisories only (no double-counting)
    // assert_eq!(body.total, expected_unique_count);
}
```

Run tests:
```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

---

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification Method |
|---|-----------|-------------------|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Test 1 validates response shape and correct counts |
| 2 | Returns 404 when SBOM ID does not exist | Test 2 validates 404 response |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Test 4 validates deduplication |
| 4 | All severity levels default to 0 when no advisories exist | Test 3 validates zero defaults |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by query design (single aggregation query vs N+1); can be further validated with a performance test if needed |

---

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against expected files:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Any file outside this list requires user approval before committing.

### Untracked File Check

Run `git status --short`, extract `??` entries, filter by proximity to implementation directories, and check for code references. Flag any referenced untracked files for user review.

### Sensitive-Pattern Check

Run:
```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

If any matches, flag and do not proceed.

### Documentation Currency

If `docs/api.md` describes existing endpoints and was not already updated in Step 6, update it now with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

### Duplication Check

Search for existing severity aggregation or counting logic in the codebase to ensure the new code does not duplicate existing utilities.

### CI Checks

Run any CI check commands extracted from `CONVENTIONS.md` in Step 4. If none found, run `cargo build` and `cargo clippy` as standard Rust checks.

### Data-Flow Trace

Trace the data flow for the new endpoint:
- **Input**: HTTP GET request with SBOM ID path parameter
- **Processing**: AdvisoryService.severity_summary() queries sbom_advisory join table, deduplicates, counts by severity level
- **Output**: JSON response with SeveritySummary struct

All stages connected: request -> path extraction -> service method -> DB query -> aggregation -> JSON response. **COMPLETE**.

### Contract & Sibling Parity

- SeveritySummary implements `Serialize` and `ToSchema` consistent with sibling model structs
- Endpoint handler follows same `Result<Json<T>, AppError>` pattern as siblings
- Error handling uses `.context()` wrapping consistent with all other handlers
- Route registration follows same `Router::new().route()` pattern

### Cross-Section Reference Consistency

Verify that file paths referenced in Files to Modify, Files to Create, and Implementation Notes are consistent:
- `AdvisoryService` -- referenced in both Files to Modify and Implementation Notes at `modules/fundamental/src/advisory/service/advisory.rs` -- consistent
- `endpoints/mod.rs` -- referenced consistently at `modules/fundamental/src/advisory/endpoints/mod.rs`
- `model/mod.rs` -- referenced consistently at `modules/fundamental/src/advisory/model/mod.rs`

---

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary() method,
endpoint handler, and integration tests.

Implements TC-9201"

git push -u origin TC-9201
```

Create PR:
```bash
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates vulnerability advisory severity counts for a given SBOM. Returns counts per severity level (Critical, High, Medium, Low) and a total.

### Changes
- **SeveritySummary model** -- new response struct with severity count fields
- **AdvisoryService.severity_summary()** -- service method that queries the sbom_advisory join table, deduplicates by advisory ID, and counts by severity level
- **GET handler** -- new endpoint following existing handler patterns
- **Route registration** -- wired into advisory endpoints module
- **Integration tests** -- 4 test cases covering correct counts, 404, zero defaults, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

---

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format (inlineCard).

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint with SeveritySummary model, service method, route registration, and 4 integration tests
   - No deviations from the plan

3. **Transition** TC-9201 to "In Review".
