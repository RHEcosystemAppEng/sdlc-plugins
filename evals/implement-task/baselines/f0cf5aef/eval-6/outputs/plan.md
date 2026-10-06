# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Serena Instance**: serena_backend (rust-analyzer)

---

## Step 0 -- Validate Project Configuration

Verified in CLAUDE.md (claude-md-mock.md):

- **Repository Registry**: present, contains trustify-backend with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present with Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
- **Code Intelligence**: present with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` for trustify-backend with rust-analyzer

All sections valid. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: follow existing endpoint pattern, use `Path<Id>`, call service, return JSON; follow `severity_summary` method pattern; use `sbom_advisory` join table; use `AdvisorySummary.severity` field for counting; register route in endpoints/mod.rs; return `AppError` with `.context()`
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 test cases
- **Target PR**: none
- **Bookend Type**: none
- **Dependencies**: none

Also capture `webUrl` for the Jira issue link in the PR description.

No GitHub Issue custom field value to extract (not mentioned in task).

## Step 1.5 -- Verify Description Integrity

See `digest-match.md` for full details. Summary:

1. Fetched comments on TC-9201.
2. Located one comment matching marker `[sdlc-workflow] Description digest:`.
3. Comment `created` and `updated` timestamps are identical -- not edited.
4. Stored digest: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
5. Computed digest of current description using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`.
6. Format tags match (`sha256-md` == `sha256-md`).
7. Hex digests match.

**Result**: Match. Proceed silently without prompting user.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID via `jira.user_info()`.
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to In Progress via `jira.transition_issue`.

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Using `mcp__serena_backend__get_symbols_overview` on:

- `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService struct, existing methods (`fetch`, `list`, `search`), their signatures, and how they use `Transactional`
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern (`Router::new().route(...)`)
- `modules/fundamental/src/advisory/model/mod.rs` -- understand module declarations

### 4.2 Inspect reference files (Implementation Notes)

Using `mcp__serena_backend__find_symbol` with `include_body=true`:

- `modules/fundamental/src/advisory/endpoints/get.rs` -- read the existing GET handler to understand path param extraction via `Path<Id>`, service call pattern, JSON response
- `modules/fundamental/src/advisory/model/summary.rs` -- read `AdvisorySummary` struct, especially the `severity` field type
- `entity/src/sbom_advisory.rs` -- read the join table entity to understand how SBOM-advisory relationships are modeled
- `common/src/error.rs` -- read `AppError` enum and `.context()` pattern

### 4.3 Check backward compatibility

Using `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` -- verify no callers will break from adding a new method (adding a method is non-breaking for callers)
- `modules/fundamental/src/advisory/endpoints/mod.rs` route registration -- confirm pattern for adding new routes

### 4.4 Convention conformance analysis

Examine sibling files in the same module for patterns:

**Endpoint siblings** (`endpoints/get.rs`, `endpoints/list.rs`):
- Handler functions use `async fn` with `Path<Id>` extractor
- Return `Result<Json<T>, AppError>`
- Call service methods with `.context("...")`
- Route registration: `Router::new().route("/path", get(handler))`

**Model siblings** (`model/summary.rs`, `model/details.rs`):
- Structs derive `Serialize, Deserialize, Debug, Clone`
- Documentation comments on struct and fields
- Public fields

**Service siblings** (`service/advisory.rs` methods):
- Methods take `&self, id: Id, tx: &Transactional<'_>`
- Return `Result<T, AppError>`
- Use SeaORM query builder with `.context()`

**Test siblings** (`tests/api/advisory.rs`):
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test both success and error cases
- Use test database setup

### 4.5 Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root (check for CI commands)
- `docs/api.md` -- REST API reference (may need updating for new endpoint)

### 4.6 CONVENTIONS.md lookup

Read `CONVENTIONS.md` at repository root via Serena. Extract CI check commands (formatting, linting, clippy, compilation) for use in Step 9. Also look for code generation commands.

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

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates unique advisories linked to a given SBOM, grouped by
/// severity level (Critical, High, Medium, Low), with a total count.
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

Follow sibling model patterns (derive macros, doc comments, public fields).

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:

```rust
pub mod severity_summary;
```

### 6.3 Add `severity_summary` method to `AdvisoryService`

In `modules/fundamental/src/advisory/service/advisory.rs`, add:

```rust
/// Computes severity counts for all unique advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the specified SBOM, deduplicates by advisory ID, and groups counts by
/// severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to sbom_id
    // Deduplicate by advisory ID
    // Fetch AdvisorySummary for each, read severity field
    // Count by severity level, build SeveritySummary with defaults of 0
    // Return 404 if SBOM does not exist
}
```

Key implementation details:
- Use `sbom_advisory` entity to find linked advisories
- Deduplicate by advisory ID before counting
- Read `severity` field from `AdvisorySummary`
- Default all counts to 0 (struct derives `Default`)
- Return 404 via `AppError` if SBOM ID not found (check SBOM exists first)
- Wrap errors with `.context("severity_summary")`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* extracted service */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing pattern:

```rust
mod severity_summary;

// In the router builder:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation impact

- No Documentation Updates section in the task.
- Check `docs/api.md` -- if it documents REST endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with request/response format.
- Keep documentation update lightweight and scoped.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with four test cases:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM linked to advisories with known severities
    // (e.g., 2 Critical, 1 High, 0 Medium, 3 Low)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then response status is 200
    // And response body contains { critical: 2, high: 1, medium: 0, low: 3, total: 6 }
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{non-existent-id}/advisory-summary

    // Then response status is 404
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then response body contains { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once in the severity totals
}
```

Follow sibling test conventions: use `assert_eq!(resp.status(), StatusCode::OK)` pattern, value-based assertions on response fields, test database setup.

Run tests:
```bash
cargo test -p <crate-name>
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Verified by test_severity_summary_with_known_advisories -- asserts all fields present with correct values |
| Returns 404 for non-existent SBOM | Verified by test_severity_summary_nonexistent_sbom |
| Counts only unique advisories | Verified by test_severity_summary_deduplicates_advisories -- inserts duplicate links, asserts single count |
| All severity levels default to 0 | Verified by test_severity_summary_no_advisories -- SBOM with no advisories returns all zeros |
| Response time under 200ms for up to 500 advisories | Verify via query analysis -- ensure the query uses indexed joins on sbom_advisory and groups at the database level rather than fetching all records to application code |

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all modified files are in the Files to Modify/Create lists. Flag any out-of-scope files for user approval.

### Untracked file check
Run `git status --short`, check for untracked files in modified directories.

### Dead parameter detection
Check modified functions for unused parameters after changes.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency
Verify `docs/api.md` reflects the new endpoint if it was updated.

### Duplication check
Search repository for existing severity aggregation logic to ensure no duplication.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted in Step 4 (cargo fmt, cargo clippy, cargo check, etc.). Hard stop on any failure.

### Module-level test requirement (Rust)
Run `cargo test -p <crate-name>` for every crate containing modified files. Resolve crate names via `cargo metadata --no-deps --format-version 1`.

### Data-flow trace
Trace: HTTP GET request -> Axum path extraction -> severity_summary handler -> AdvisoryService.severity_summary() -> SeaORM query on sbom_advisory join table -> count and group by severity -> SeveritySummary struct -> JSON serialization -> HTTP response. All stages connected.

### Contract and sibling parity
- Verify handler return type matches `Result<Json<T>, AppError>` pattern
- Verify service method signature matches sibling methods
- Verify error handling uses `.context()` consistently

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated advisory severity counts (critical, high, medium, low, total)
for a given SBOM. Includes SeveritySummary model, AdvisoryService method,
and integration tests.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](<webUrl>)` with clickable Jira link
- Closes line for GitHub issue if applicable

### Fork detection
Check for upstream remote via `git remote get-url upstream 2>/dev/null`. If present, use `-R <upstream-owner/repo> --head <fork-owner>:<branch>` flags. If not, use default `gh pr create`.

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format:
   ```
   jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. Add comment to TC-9201 with PR link, summary of changes, and any deviations.

3. Transition TC-9201 to In Review:
   ```
   jira.transition_issue -> In Review
   ```
