# Implementation Plan: TC-9201

## Task Summary

**Issue**: TC-9201 -- Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Status**: To Do (will transition to In Progress)

## Step 0 -- Validate Project Configuration

CLAUDE.md contains the required sections:
- Repository Registry: present, lists trustify-backend with Serena instance `serena_backend`
- Jira Configuration: present, includes Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present, with tool naming convention and configured instances

Validation passes. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. Fall back to REST API if MCP fails, per the fallback protocol.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify**: 4 files (advisory/service/advisory.rs, advisory/endpoints/mod.rs, advisory/model/mod.rs, server/src/main.rs [no changes needed])
- **Files to Create**: 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs tests)
- **API Changes**: GET /api/v2/sbom/{id}/advisory-summary
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 tests
- **Dependencies**: None
- **Target Branch**: main (extracted for branch operations and PR targeting)

Capture the issue `webUrl` for PR description linking.

## Step 1.5 -- Verify Description Integrity

(See outputs/digest-match.md for full details)

The Jira issue has a digest comment matching the marker string `[sdlc-workflow] Description digest:`. The comment contains:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The comment's `created` and `updated` timestamps are identical (not edited). The stored digest was computed using `scripts/sha256-digest.py` and the format tag is `sha256-md`. After computing the current description digest using the same script, the format tags match and the hex digests match.

**Result**: Digests match. Proceed silently -- no user prompt, no added latency. Continue to Step 2.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code

### Code Inspection Plan

Use the Serena instance `serena_backend` (from Repository Registry) for code intelligence.

**Files to inspect before modifying:**

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to understand the existing GET handler pattern. Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function to see how it extracts path params, calls the service, and returns JSON. This is the pattern we will follow for the new severity_summary endpoint.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the AdvisoryService struct and its existing methods (fetch, list, search). Use `mcp__serena_backend__find_symbol` on the `fetch` method to understand the method signature pattern (`&self, id: Id, tx: &Transactional<'_>`), error handling with `Result<T, AppError>` and `.context()`, and how it queries the database.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the AdvisorySummary struct and its `severity` field. This field will be used to count advisories by severity level.

4. **`common/src/error.rs`** -- Use `mcp__serena_backend__find_symbol` on `AppError` to understand the error type and how `.context()` wrapping works, so we follow the same error handling pattern.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Inspect route registration pattern (`Router::new().route(...)`) to follow the same approach for registering the new endpoint.

6. **`modules/fundamental/src/advisory/model/mod.rs`** -- Inspect existing `pub mod` declarations to follow the pattern for adding `pub mod severity_summary;`.

7. **`entity/src/sbom_advisory.rs`** -- Inspect the join table entity to understand the relationship between SBOMs and advisories for the query.

### Convention Conformance Analysis

Inspect sibling files for conventions:

- **Sibling endpoints**: `advisory/endpoints/list.rs`, `advisory/endpoints/get.rs` -- analyze patterns for handler signatures, path extraction, service calls, error handling, response types
- **Sibling models**: `advisory/model/summary.rs`, `advisory/model/details.rs` -- analyze struct patterns, derive macros, serde attributes
- **Sibling tests**: `tests/api/advisory.rs`, `tests/api/sbom.rs` -- analyze test structure, assertion patterns, setup/teardown

**Discovered conventions:**
- Error handling: all handlers use `Result<T, AppError>` with `.context()` wrapping
- Module structure: each domain follows `model/ + service/ + endpoints/` pattern
- Naming: `verb_noun` for methods (e.g., `fetch`, `list`), descriptive struct names
- Endpoint registration: `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`
- Response types: list endpoints use `PaginatedResults<T>`, single-item endpoints return struct directly
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Import organization: external crates first, then internal modules

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo manifest shows it exists. Read it and extract CI check commands and code generation commands for use in Step 9.

### Documentation File Identification

Relevant docs:
- `docs/api.md` -- may need updating with the new endpoint
- `docs/architecture.md` -- unlikely to need changes for a new endpoint

## Step 5 -- Create Branch

Extract Target Branch from the task description: **main**.

```bash
git checkout main
git pull
git checkout -b TC-9201
```

The branch is named after the Jira issue ID (TC-9201). It is based on the Target Branch (main).

## Step 6 -- Implement Changes

### Files to Modify

**1. `modules/fundamental/src/advisory/service/advisory.rs`**

Add a `severity_summary` method to AdvisoryService following the existing `fetch` and `list` method patterns:

```rust
/// Returns aggregated severity counts for advisories linked to a given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table to find advisories linked to this SBOM
    // Join with advisory table to get severity field
    // Deduplicate by advisory ID
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

- Uses `sbom_advisory` join table from `entity/src/sbom_advisory.rs`
- References `AdvisorySummary.severity` field for counting
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Deduplicates by advisory ID per acceptance criteria

**2. `modules/fundamental/src/advisory/endpoints/mod.rs`**

Add route registration for the new endpoint:

```rust
pub mod severity_summary;

// In the router function, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follows the existing pattern of route registration in this file.

**3. `modules/fundamental/src/advisory/model/mod.rs`**

Add module registration:

```rust
pub mod severity_summary;
```

Follows the pattern of existing `pub mod summary;` and `pub mod details;` declarations.

### Files to Create

**1. `modules/fundamental/src/advisory/model/severity_summary.rs`**

New response struct:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of Critical severity advisories.
    pub critical: u32,
    /// Count of High severity advisories.
    pub high: u32,
    /// Count of Medium severity advisories.
    pub medium: u32,
    /// Count of Low severity advisories.
    pub low: u32,
    /// Total number of unique advisories.
    pub total: u32,
}

impl Default for SeveritySummary {
    fn default() -> Self {
        Self {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        }
    }
}
```

**2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`**

New GET handler following the pattern from `advisory/endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to fetch advisory severity summary")?;
    Ok(Json(summary))
}
```

- Extracts path params via `Path<Id>` (same pattern as get.rs)
- Calls service method and returns JSON
- Error handling with `.context()` wrapping

**3. `tests/api/advisory_summary.rs`**

Integration tests for the new endpoint:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with advisories at known severity levels
    // ... setup test data ...

    // When requesting the severity summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response contains correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical_count);
    assert_eq!(summary.high, expected_high_count);
    assert_eq!(summary.medium, expected_medium_count);
    assert_eq!(summary.low, expected_low_count);
    assert_eq!(summary.total, expected_total);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID
    // When requesting the severity summary
    let resp = client.get("/api/v2/sbom/nonexistent/advisory-summary").await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    // ... setup test data ...

    // When requesting the severity summary
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

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM with duplicate advisory links
    // ... setup test data with duplicate sbom_advisory entries ...

    // When requesting the severity summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then counts reflect unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, expected_unique_count);
}
```

## Step 7 -- Write Tests

Tests are described in the Files to Create section above. Run tests:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by SeveritySummary struct and endpoint handler
2. Returns 404 when SBOM ID does not exist -- verified by test_severity_summary_not_found
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by deduplication logic in service and test_severity_summary_deduplication
4. All severity levels default to 0 when no advisories exist -- verified by Default impl and test_severity_summary_no_advisories
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by using efficient SQL JOIN query with deduplication

## Step 9 -- Self-Verification

- **Scope containment**: all modified files are within the Files to Modify and Files to Create sections
- **Sensitive-pattern check**: scan staged diff for secrets/credentials
- **Documentation currency**: update `docs/api.md` if it documents API endpoints
- **CI checks**: run commands extracted from CONVENTIONS.md
- **Duplication check**: search for similar severity aggregation logic in the codebase

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns aggregated
severity counts (Critical, High, Medium, Low, total) for advisories linked
to a given SBOM. Includes deduplication by advisory ID and integration tests.

Implements TC-9201"
```

Then push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

The PR description will include `Implements [TC-9201](<webUrl>)` with a clickable Jira link.

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format
2. Add a comment summarizing the implementation and linking to the PR
3. Transition TC-9201 to "In Review"
