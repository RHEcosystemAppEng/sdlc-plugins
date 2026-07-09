# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.

## Repository and Branch

- **Repository:** trustify-backend (Serena instance: `serena_backend`)
- **Target Branch:** main
- **Task Branch:** TC-9201

## Dependencies

None -- no prerequisite tasks to verify.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed directly.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve the current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<accountId>)`.
3. Transition TC-9201 to In Progress via `jira.transition_issue`.

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Use `mcp__serena_backend__get_symbols_overview` on:

- `modules/fundamental/src/advisory/service/advisory.rs` -- understand the `AdvisoryService` struct, its existing methods (`fetch`, `list`, `search`), and the method signature pattern (parameters like `&self`, ID types, `Transactional` usage).
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand the route registration pattern (`Router::new().route(...)` calls, how handlers are wired).
- `modules/fundamental/src/advisory/model/mod.rs` -- see existing `pub mod` declarations to understand module registration.

### 4.2 Inspect Sibling Files for Convention Analysis

Use `mcp__serena_backend__get_symbols_overview` on sibling files to discover conventions:

- `modules/fundamental/src/advisory/endpoints/get.rs` -- understand the handler pattern (Path extractor, service call, JSON response).
- `modules/fundamental/src/advisory/endpoints/list.rs` -- see how list endpoints differ from single-resource endpoints.
- `modules/fundamental/src/advisory/model/summary.rs` -- understand the `AdvisorySummary` struct structure including its `severity` field.
- `modules/fundamental/src/advisory/model/details.rs` -- see the model struct pattern (derive macros, serde attributes, field types).
- `modules/fundamental/src/sbom/endpoints/get.rs` -- compare SBOM endpoint patterns with advisory endpoints.

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:

- `AdvisoryService::fetch` and `AdvisoryService::list` -- read the full method bodies to understand the service method pattern.
- `AdvisorySummary` struct -- read the struct definition to understand the `severity` field type.

Use `mcp__serena_backend__search_for_pattern` to locate:

- `sbom_advisory` entity usage across the codebase -- understand the join table pattern for linking SBOMs to advisories.
- `AppError` usage in endpoint handlers -- understand error handling and `.context()` wrapping.

### 4.3 Check Backward Compatibility

Use `mcp__serena_backend__find_referencing_symbols` on:

- `AdvisoryService` -- ensure adding a new method does not conflict with existing consumers.
- The advisory endpoints `mod.rs` router -- understand how routes are composed.

### 4.4 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract CI check commands for use in Step 9.

### 4.5 Documentation File Identification

Check for:
- `README.md` at the repository root.
- `docs/api.md` or `docs/architecture.md` as referenced in the project CLAUDE.md.
- Any OpenAPI spec files if present.

### 4.6 Test Convention Analysis

Inspect sibling test files:
- `tests/api/advisory.rs` -- understand existing advisory endpoint test patterns (assertions, status code checks, setup, naming).
- `tests/api/sbom.rs` -- see SBOM endpoint test patterns for cross-reference.
- `tests/api/search.rs` -- compare test patterns across different modules.

Record assertion style, response validation, error case coverage, test naming, and any parameterized test usage.

### Expected Discovered Conventions

**Production code conventions (from sibling analysis):**
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` for wrapping
- **Service methods:** Follow `verb_noun` pattern, take `&self`, an ID parameter, and `tx: &Transactional<'_>`
- **Route registration:** `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`
- **Response types:** Structs derive `Serialize` and are returned directly via Axum's `Json` extractor
- **Model modules:** Each model is a separate file, registered via `pub mod` in the parent `mod.rs`
- **Path extraction:** Handlers use `Path<Id>` extractor from Axum

**Test conventions (from sibling analysis):**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases:** 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Setup:** Tests use a real PostgreSQL test database with fixture data

## Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
use serde::Serialize;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Provides a breakdown of advisory counts by severity level (critical, high,
/// medium, low) along with the total count, enabling dashboard widgets to render
/// severity distributions without client-side counting.
#[derive(Debug, Default, Serialize)]
pub struct SeveritySummary {
    /// Number of advisories with critical severity.
    pub critical: u64,
    /// Number of advisories with high severity.
    pub high: u64,
    /// Number of advisories with medium severity.
    pub medium: u64,
    /// Number of advisories with low severity.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

Key decisions:
- Derive `Default` so all fields initialize to 0 (satisfies acceptance criterion: all severity levels default to 0).
- Use `u64` for counts to match Rust conventions for non-negative integers.
- Derive `Serialize` for Axum `Json` response serialization.
- Add doc comments on the struct and every field.

### 6.2 Register the Model Module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` alongside the existing `pub mod summary;` and `pub mod details;` declarations.

### 6.3 Add `severity_summary` Method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method following the pattern of `fetch` and `list`:

```rust
/// Computes an aggregated severity summary for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts each severity level. Returns a `SeveritySummary`
/// with counts for critical, high, medium, low, and total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Given: the SBOM ID to query
    // When: fetching all linked advisories via the join table
    let advisories = /* query sbom_advisory join table for sbom_id,
                        join to advisory table to get AdvisorySummary data,
                        deduplicate by advisory ID */;

    // Then: count severities and build the summary
    let mut summary = SeveritySummary::default();
    for advisory in &advisories {
        match advisory.severity.as_deref() {
            Some("critical") => summary.critical += 1,
            Some("high") => summary.high += 1,
            Some("medium") => summary.medium += 1,
            Some("low") => summary.low += 1,
            _ => {} // Unknown or missing severity -- counted in total but not in a bucket
        }
    }
    summary.total = advisories.len() as u64;

    Ok(summary)
}
```

Key decisions:
- Deduplicate by advisory ID before counting (acceptance criterion: counts only unique advisories).
- Use the `sbom_advisory` join table as specified in Implementation Notes.
- Match severity strings case-insensitively if the actual data format requires it (verify during Step 4 by inspecting the `severity` field on `AdvisorySummary`).
- Return `AppError` with `.context()` wrapping, matching the existing error handling convention.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns an aggregated severity summary of all vulnerability advisories
/// linked to the specified SBOM, with counts per severity level and a total.
pub async fn get_severity_summary(
    Path(sbom_id): Path<Id>,
    service: /* extracted via Axum state */,
    tx: /* transactional context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

Key decisions:
- Follow the exact handler signature pattern from `get.rs` (Path extractor, service from state, transactional context).
- Use `.context()` for error wrapping matching the project convention.
- Return 404 when the SBOM ID does not exist -- this will be handled by the service layer's existing SBOM lookup logic (verify during Step 4 that the service pattern returns a not-found error for missing entities).

### 6.5 Register the Route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route to the existing router registration:

```rust
pub mod severity_summary;

// In the router function, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follow the existing pattern of how other routes are registered in this file.

### 6.6 Documentation Impact

- Check if `docs/api.md` exists and documents REST endpoints. If so, add an entry for `GET /api/v2/sbom/{id}/advisory-summary` with the response shape.
- No changes to `server/src/main.rs` needed (routes auto-mount via module registration as noted in the task).

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts
/// for each level and the total matches the number of unique advisories.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test fixtures: create SBOM, create advisories with known severities,
    //  link them via sbom_advisory join table)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then it returns 200 with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical_count);
    assert_eq!(summary.high, expected_high_count);
    assert_eq!(summary.medium, expected_medium_count);
    assert_eq!(summary.low, expected_low_count);
    assert_eq!(summary.total, expected_total_count);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 status, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").await;

    // Then it returns 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts at zero and total at zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    // (create SBOM but do not link any advisories)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links (the same advisory linked to the same
/// SBOM multiple times) are deduplicated, producing correct unique counts.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links
    // (create SBOM, create one advisory, link it multiple times via sbom_advisory)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then duplicates are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, 1); // Not the number of duplicate links
    // Assert the single advisory's severity is counted exactly once
}
```

Key decisions:
- Each test function has a `///` doc comment explaining what it verifies.
- Tests use given-when-then section comments for clarity.
- Assertions are value-based (checking specific counts), not just length-based.
- Test naming follows `test_<endpoint>_<scenario>` pattern from sibling tests.
- Tests hit a real PostgreSQL test database following the project's integration test pattern.

Register the test module in `tests/api/` if a `mod.rs` or `main.rs` test harness exists.

Run tests:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by `test_advisory_summary_valid_sbom` -- asserts response shape and values |
| Returns 404 when SBOM ID does not exist | Verified by `test_advisory_summary_nonexistent_sbom` |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_advisory_summary_deduplication` |
| All severity levels default to 0 when no advisories exist | Verified by `test_advisory_summary_no_advisories` |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by ensuring the query uses the `sbom_advisory` join table efficiently with deduplication at the database level rather than in application code; performance testing against a dataset with 500 advisories during integration tests |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files are within the task scope:

**Files to Modify (expected):**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create (expected):**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Flag any out-of-scope files for user approval.

### Untracked File Check

Run `git status --short` to identify untracked files (`??` prefix). Filter by directories containing modified files and search for code references to any proximity-matched untracked files.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to verify no secrets are staged.

### Documentation Currency

Check whether `docs/api.md` needs an entry for the new endpoint. If it documents existing endpoints and this new endpoint is not yet listed, add it.

### Duplication Check

Search for existing severity counting or advisory aggregation logic in the repository using `mcp__serena_backend__search_for_pattern` or Grep to ensure the new `severity_summary` method does not duplicate existing functionality.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `sbom_id` from path -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> join to advisory table for severity data -> deduplicate by advisory ID -> count by severity level -> return `SeveritySummary` as JSON -- **COMPLETE**

### Contract and Sibling Parity

- `SeveritySummary` is a standalone response struct (no trait/interface contract to implement).
- Sibling parity with `get.rs` handler: Path extraction, service call, `.context()` error wrapping, `Json` return -- all present.

### CI Checks

Run any CI check commands extracted from `CONVENTIONS.md` (if found). If none, run `cargo build` and `cargo clippy` to verify no warnings were introduced.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
proper 404 handling for missing SBOMs.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint \`GET /api/v2/sbom/{id}/advisory-summary\` that aggregates
vulnerability advisory severity counts for a given SBOM, returning counts per severity
level (Critical, High, Medium, Low) and a total.

- New \`SeveritySummary\` response model
- New \`severity_summary\` method on \`AdvisoryService\`
- New endpoint handler with 404 handling for missing SBOMs
- Deduplication of advisories by ID
- Integration tests covering valid SBOM, missing SBOM, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test Plan

- [x] Valid SBOM returns correct severity counts
- [x] Non-existent SBOM returns 404
- [x] SBOM with no advisories returns all zeros
- [x] Duplicate advisory links are deduplicated
"
```

## Step 11 -- Update Jira

1. Update the Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL in ADF format (inline card).

2. Add a comment to TC-9201 summarizing:
   - PR link
   - Summary of changes: added `SeveritySummary` model, `severity_summary` service method, `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler, and integration tests
   - No deviations from the plan

3. Transition TC-9201 to In Review.
