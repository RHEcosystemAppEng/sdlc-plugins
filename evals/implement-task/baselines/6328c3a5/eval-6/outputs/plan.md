# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

---

## Pre-Implementation Steps

### Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena
   instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature
   issue type ID
3. **Code Intelligence** -- present with tool naming convention
   `mcp__serena_backend__<tool>`

All sections valid. Proceed.

### Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates
  vulnerability advisory severity counts for a given SBOM
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs`
  - `modules/fundamental/src/advisory/endpoints/mod.rs`
  - `modules/fundamental/src/advisory/model/mod.rs`
  - `server/src/main.rs` (no changes needed)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs`
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
  - `tests/api/advisory_summary.rs`
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None
- **GitHub Issue custom field**: check `customfield_10747` on the issue; extract
  if present

Capture the issue `webUrl` for PR description linking.

### Step 1.5 -- Verify Description Integrity

(See `digest-match.md` for the full analysis.)

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate comment with marker `[sdlc-workflow] Description digest:`
3. Found: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` equals `updated` -- no edit warning
5. Format tag is `sha256-md` (not legacy) -- proceed with comparison
6. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
7. Format tags match (`sha256-md` == `sha256-md`)
8. Hex digests match -- **proceed silently**

### Step 2 -- Verify Dependencies

Task has no dependencies listed. Proceed.

### Step 3 -- Transition to In Progress and Assign

1. Get current user: `jira.user_info()`
2. Assign task: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition: `jira.transition_issue("TC-9201")` to "In Progress"

---

## Code Understanding (Step 4)

### 4.1 -- Inspect Files to Modify

Use `mcp__serena_backend__get_symbols_overview` on each file to understand
existing structure:

**`modules/fundamental/src/advisory/service/advisory.rs`**
- Inspect `AdvisoryService` struct and its methods (`fetch`, `list`, `search`)
- Understand method signatures: `&self`, parameters, return types
- Note the `Transactional` pattern used for database transactions

**`modules/fundamental/src/advisory/endpoints/mod.rs`**
- Inspect route registration pattern (`Router::new().route(...)`)
- Understand how handlers are imported and registered

**`modules/fundamental/src/advisory/model/mod.rs`**
- Inspect existing `pub mod` declarations to understand module registration pattern

### 4.2 -- Inspect Reference Files (Implementation Notes)

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:

- `modules/fundamental/src/advisory/endpoints/get.rs` -- reference pattern for
  endpoint handler (Path extraction, service call, JSON response)
- `modules/fundamental/src/advisory/model/summary.rs` -- `AdvisorySummary`
  struct with `severity` field (needed for counting)
- `entity/src/sbom_advisory.rs` -- join table entity for SBOM-Advisory
  relationships
- `common/src/error.rs` -- `AppError` enum and `.context()` pattern

### 4.3 -- Check Backward Compatibility

Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to
identify all callers and ensure adding a new method won't break existing code.

### 4.4 -- Convention Conformance Analysis

Examine sibling files for patterns:

- **Endpoints**: `get.rs`, `list.rs` in the advisory endpoints directory
  - Naming: handler functions use `verb_noun` pattern
  - Error handling: `Result<Json<T>, AppError>` with `.context()`
  - Path extraction: `Path(id): Path<Id>`
- **Models**: `summary.rs`, `details.rs` in the advisory model directory
  - Derive macros: `#[derive(Serialize, Deserialize, Debug)]`
  - Documentation comments on structs and fields
- **Services**: `advisory.rs` service methods
  - Pattern: `async fn method(&self, param: Type, tx: &Transactional<'_>) -> Result<T, AppError>`
- **Tests**: `tests/api/advisory.rs`
  - Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`
  - Response parsing pattern
  - Test naming convention

### 4.5 -- CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root. If present, read and extract:
- Code conventions to follow during implementation
- CI check commands for Step 9 verification
- Code generation commands if any

### 4.6 -- Documentation File Identification

Identify related documentation:
- `docs/api.md` -- REST API reference (may need updating for new endpoint)
- `docs/architecture.md` -- system architecture overview
- `README.md` at repo root

---

## Branch Creation (Step 5)

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

---

## Implementation (Step 6)

### 6.1 -- Create `severity_summary.rs` Model

**File**: `modules/fundamental/src/advisory/model/severity_summary.rs`

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Provides counts of unique advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns.
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u32,
    /// Count of advisories with High severity.
    pub high: u32,
    /// Count of advisories with Medium severity.
    pub medium: u32,
    /// Count of advisories with Low severity.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

Key decisions:
- Use `u32` for counts (non-negative integers, sufficient range)
- Derive `Default` so all fields initialize to 0
- Derive `Serialize`/`Deserialize` for JSON conversion
- Add doc comments on the struct and every field

### 6.2 -- Register Model Module

**File**: `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the existing module registration
pattern (alongside `pub mod summary;` and `pub mod details;`).

### 6.3 -- Add `severity_summary` Service Method

**File**: `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method to `AdvisoryService`:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts for each level and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Fetch AdvisorySummary for each linked advisory
    // 4. Deduplicate by advisory ID using a HashSet
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Implementation details:
- First verify SBOM existence to return 404 for non-existent SBOMs (matching
  existing SBOM endpoint behavior)
- Use `sbom_advisory` entity to find linked advisory IDs
- Use `HashSet` for deduplication by advisory ID
- Match severity string values against "Critical", "High", "Medium", "Low"
- Use `.context("Failed to compute advisory severity summary")` for error wrapping
- Unwrap severity with `.unwrap_or_default()` for defensive access

### 6.4 -- Create Endpoint Handler

**File**: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts per severity level for all
/// advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Retrieving advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the pattern from `get.rs`:
- Extract path parameter via `Path<Id>`
- Call service method
- Return `Json(result)`
- Wrap errors with `.context()`

### 6.5 -- Register Route

**File**: `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing registration pattern:

```rust
mod severity_summary;

// In the router builder:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 -- Documentation Impact

Check `docs/api.md` for API documentation. If it documents REST endpoints, add
an entry for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with:
- Path and method
- Path parameters (`id` -- SBOM identifier)
- Response schema (`{ critical, high, medium, low, total }`)
- Error responses (404 when SBOM not found)

---

## Test Implementation (Step 7)

**File**: `tests/api/advisory_summary.rs`

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels
    // (set up test data: SBOM + linked advisories with specific severities)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, <expected_critical>);
    assert_eq!(body.high, <expected_high>);
    assert_eq!(body.medium, <expected_medium>);
    assert_eq!(body.low, <expected_low>);
    assert_eq!(body.total, <expected_total>);
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting a summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    // Assert that the total reflects unique advisories, not total links
    assert_eq!(body.total, <expected_unique_count>);
}
```

Run tests: `cargo test -p trustify-fundamental` (or the appropriate crate name
resolved via `cargo metadata`).

---

## Acceptance Criteria Verification (Step 8)

| Criterion | Verification Method |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns severity counts | Test 1 asserts correct response shape and values |
| Returns 404 for non-existent SBOM | Test 2 asserts 404 status code |
| Counts only unique advisories | Test 4 verifies deduplication with duplicate links |
| All severity levels default to 0 | Test 3 asserts all-zero response for SBOM with no advisories |
| Response time under 200ms for up to 500 advisories | Verify via query analysis; single join query should meet this |

---

## Self-Verification (Step 9)

### Scope Containment

Run `git diff --name-only` and verify all changed files are within scope:

**Expected modified files**:
- `modules/fundamental/src/advisory/service/advisory.rs` (in Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (in Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` (in Files to Modify)

**Expected created files**:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (in Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (in Files to Create)
- `tests/api/advisory_summary.rs` (in Files to Create)

`server/src/main.rs` is listed with "no changes needed" -- verify it was not modified.

Flag any out-of-scope files for user approval.

### Untracked File Check

Run `git status --short`, filter untracked files (`??`) near modified
directories. Check if any are referenced by staged changes. Flag for user
approval.

### Dead Parameter Detection

Scan modified functions for parameters no longer referenced after changes. Since
we are only adding new methods (not modifying existing function bodies), this is
unlikely to surface issues.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation Currency

If `docs/api.md` documents existing endpoints and was not updated in Step 6,
update it now for the new endpoint.

### Duplication Check

Search for existing severity aggregation logic or similar counting functions
in the codebase. If found, refactor to reuse.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` (if found). Hard stop
on any failure.

### Module-Level Test Requirement (Rust)

Run `cargo metadata --no-deps --format-version 1` to resolve the crate name
for modified files. Run `cargo test -p <crate-name>` for each affected crate.
Hard stop on failure.

### Data-Flow Trace

```
Input:  GET /api/v2/sbom/{id}/advisory-summary
        --> Path parameter extraction (sbom_id)
Process: --> AdvisoryService.severity_summary(sbom_id, tx)
              --> Verify SBOM exists (404 if not)
              --> Query sbom_advisory join table
              --> Fetch advisory severities
              --> Deduplicate by advisory ID
              --> Count by severity level
Output:  --> Json(SeveritySummary { critical, high, medium, low, total })
         --> HTTP 200 with JSON body
```

All stages connected. Complete data flow from request to response.

### Contract & Sibling Parity

- **Contract**: `SeveritySummary` implements `Serialize` for JSON response.
  Handler returns `Result<Json<SeveritySummary>, AppError>` matching Axum
  contract.
- **Sibling parity**: Compare with `get.rs` handler -- same error handling,
  same extraction pattern, same response wrapping.
- **Cross-module entity**: Uses `sbom_advisory` join table (read-only query),
  no write conflicts.
- **Caller-site**: New endpoint, no existing callers to compare.

---

## Commit and Push (Step 10)

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Add docs/api.md if updated

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes deduplication by advisory ID and 404 handling for missing SBOMs.

Implements TC-9201"
```

### Fork Detection

```bash
git remote get-url upstream 2>/dev/null
```

Determine push strategy based on whether upstream remote exists.

### Push and Create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes
- Link to Jira task: `Implements [TC-9201](<webUrl>)`
- GitHub issue `Closes` line if `customfield_10747` was populated
- Description of new endpoint, response format, and test coverage

---

## Update Jira (Step 11)

1. **Set Git Pull Request custom field** (`customfield_10875`) with the PR URL
   in ADF format:
   ```
   jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint with
     `SeveritySummary` response model, `AdvisoryService.severity_summary`
     method, and integration tests covering correct counts, 404 handling,
     zero-advisory case, and deduplication
   - No deviations from the plan
   - Comment ends with the skill footnote from `shared/comment-footnote.md`

3. **Transition** TC-9201 to "In Review":
   ```
   jira.transition_issue("TC-9201") --> In Review
   ```
