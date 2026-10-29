# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Jira Issue**: TC-9201

---

## Step 0 -- Validate Project Configuration

Verified the project's CLAUDE.md contains:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena
   instance `serena_backend` and path `./`.
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID,
   Feature issue type ID (10142), Git Pull Request custom field (customfield_10875),
   GitHub Issue custom field (customfield_10747).
3. **Code Intelligence** -- present, documents the `mcp__<serena-instance>__<tool>`
   naming convention with `serena_backend` configured for rust-analyzer.

All required sections present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all Jira operations. Fall back to REST API via
`scripts/jira-client.py` if MCP fails, after prompting the user.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`.

### Parsed sections

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add severity aggregation service + endpoint for SBOM advisory summary |
| Files to Modify | 4 files (see below) |
| Files to Create | 3 files (see below) |
| API Changes | GET /api/v2/sbom/{id}/advisory-summary (NEW) |
| Acceptance Criteria | 5 criteria |
| Test Requirements | 4 test cases |
| Dependencies | None |
| Target PR | Not present |
| Bookend Type | Not present |
| Review Context | Not present |

**Files to Modify:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`
- `server/src/main.rs` (no changes needed per description)

**Files to Create:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

**webUrl**: captured from API response for use in PR description.

**GitHub Issue custom field**: check customfield_10747 on the issue. If present,
extract the GitHub issue reference for the PR description `Closes` line.

## Step 1.5 -- Verify Description Integrity

Digest comment found. Format tags match (`sha256-md`). Hex digests match.
**Proceed silently.** (See `outputs/digest-match.md` for full detail.)

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID via `jira.user_info()`.
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<accountId>)`.
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`.

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use `mcp__serena_backend__get_symbols_overview` on each file to modify:

- **`advisory/service/advisory.rs`** -- understand `AdvisoryService` struct and its
  existing methods (`fetch`, `list`, `search`). Identify the method signature pattern
  (takes `&self`, entity ID, `&Transactional<'_>`; returns `Result<T, AppError>`).
- **`advisory/endpoints/mod.rs`** -- understand route registration pattern
  (`Router::new().route(...)` chains).
- **`advisory/model/mod.rs`** -- see existing `pub mod` declarations to follow
  the same pattern when adding `pub mod severity_summary;`.

### 4.2 Inspect referenced code for patterns

- Use `mcp__serena_backend__find_symbol` on `AdvisoryService` with `include_body=true`
  to read the `fetch` and `list` methods for the service method signature pattern.
- Use `mcp__serena_backend__find_symbol` on `AdvisorySummary` to see the `severity`
  field and understand the data model.
- Read `advisory/endpoints/get.rs` to understand the endpoint handler pattern:
  path param extraction via `Path<Id>`, service call, JSON response.
- Read `entity/src/sbom_advisory.rs` to understand the join table structure for
  linking SBOMs to advisories.
- Use `mcp__serena_backend__find_referencing_symbols` on any symbols to be modified.

### 4.3 Check for reusable utilities

- Search for existing severity-related constants or enums (e.g., `SEVERITY_ORDER`,
  severity level definitions) via `mcp__serena_backend__search_for_pattern` or Grep.
- Check `common/src/error.rs` for `AppError` usage patterns.
- Check `common/src/model/paginated.rs` for response type patterns (this endpoint
  does not paginate, but good to understand the convention).

### 4.4 CONVENTIONS.md lookup

Read `CONVENTIONS.md` at the repository root. Extract:
- CI check commands (linting, formatting, compilation checks)
- Code generation commands (if any)
- Naming rules, directory structure, test conventions

### 4.5 Convention conformance analysis

Examine sibling files for patterns:

**Production siblings:**
- `advisory/endpoints/get.rs` and `advisory/endpoints/list.rs` -- handler patterns
- `advisory/service/advisory.rs` -- service method patterns
- `sbom/model/summary.rs` -- response struct patterns

**Test siblings:**
- `tests/api/advisory.rs` and `tests/api/sbom.rs` -- integration test patterns,
  assertion style, setup/teardown

Output discovered conventions for use in Steps 6 and 7.

### 4.6 Documentation file identification

Identify docs that may need updating:
- `docs/api.md` -- REST API reference (new endpoint)
- `docs/architecture.md` -- system architecture (if advisory module is described)
- `README.md` -- if it documents API endpoints

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
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Debug, Clone, Default, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u32,
    /// Number of high-severity advisories.
    pub high: u32,
    /// Number of medium-severity advisories.
    pub medium: u32,
    /// Number of low-severity advisories.
    pub low: u32,
    /// Total number of unique advisories.
    pub total: u32,
}
```

Follow the struct pattern from `SbomSummary` / `AdvisorySummary` siblings.
Include `Serialize` and `ToSchema` derives to match the project convention.

### 6.2 Register the new model module

In `modules/fundamental/src/advisory/model/mod.rs`, add:

```rust
pub mod severity_summary;
```

Following the existing `pub mod summary;` and `pub mod details;` pattern.

### 6.3 Add `severity_summary` method to `AdvisoryService`

In `modules/fundamental/src/advisory/service/advisory.rs`, add:

```rust
/// Computes aggregated severity counts for advisories linked to a given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Deduplicate by advisory ID
    // Fetch severity from each advisory's AdvisorySummary
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use the `sbom_advisory` join table to find linked advisories
- Deduplicate by advisory ID to satisfy acceptance criterion
- Use `.context()` error wrapping matching existing pattern
- Return 404 via AppError when the SBOM ID does not exist (check SBOM exists first)
- Default all severity counts to 0 (the `Default` derive on `SeveritySummary` handles this)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Define the GET handler:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
pub async fn severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service.severity_summary(id, &tx).await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the pattern in `advisory/endpoints/get.rs`:
- Extract path params via `Path<Id>`
- Call service method
- Return `Json(result)` directly
- Error handling via `Result<T, AppError>` with `.context()`

### 6.5 Register the new route

In `modules/fundamental/src/advisory/endpoints/mod.rs`, add:

```rust
mod severity_summary;
```

And register the route in the router chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

Following the existing route registration pattern.

### 6.6 Documentation impact

- Check `docs/api.md` -- if it documents REST endpoints, add the new
  `GET /api/v2/sbom/{id}/advisory-summary` endpoint with request/response schema.
- No changes needed to `server/src/main.rs` per the task description (routes
  auto-mount via module registration).

### 6.7 Code quality verification

- Every new struct, function, and method has a doc comment.
- Defensive property access: guard against null/empty severity fields on advisory
  data using `.unwrap_or_default()` or pattern matching.
- No new symbols duplicate existing ones (verify `SeveritySummary` does not
  conflict with existing names via symbol search).

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with 4 test cases:

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (setup: ingest SBOM + link advisories with Critical, High, Medium, Low severities)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, <expected>)
    // assert_eq!(body.high, <expected>)
    // assert_eq!(body.medium, <expected>)
    // assert_eq!(body.low, <expected>)
    // assert_eq!(body.total, <expected>)
}
```

Value-based assertions on each severity count, not just length checks.

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting severity summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}
```

### Test 4: Deduplication of advisory links

```rust
/// Verifies that duplicate advisory links are deduplicated in severity counts.
#[tokio::test]
async fn test_severity_summary_deduplicates() {
    // Given an SBOM with the same advisory linked multiple times

    // When requesting the advisory summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, 1) (not 2+)
    // assert specific severity count reflects single occurrence
}
```

All tests use doc comments and given-when-then structure. Follow sibling test
patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs` for setup,
teardown, and assertion style.

Run tests:

```bash
cargo test -p trustify-tests
```

(or whichever package contains `tests/api/`, resolved via `cargo metadata`)

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET endpoint returns `{ critical, high, medium, low, total }` | Implemented in handler + verified by Test 1 |
| Returns 404 for non-existent SBOM ID | AppError handling + verified by Test 2 |
| Counts only unique advisories (deduplicates) | Service method deduplicates by advisory ID + verified by Test 4 |
| All severity levels default to 0 | `Default` derive on struct + verified by Test 3 |
| Response time under 200ms for 500 advisories | Single SQL query with join -- architecture review confirms feasibility |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and verify all modified/created files are within:
- Files to Modify (4 files)
- Files to Create (3 files)

Flag any out-of-scope files for user approval.

### Untracked file check

Run `git status --short` to identify untracked files. Check for references to
any untracked files in the staged diff.

### Dead parameter detection

Scan modified functions for parameters no longer referenced in the function body.
Remove any dead parameters and update all callers.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation currency

Verify `docs/api.md` reflects the new endpoint if it documents REST endpoints.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md:
- `cargo fmt --check`
- `cargo clippy -- -D warnings`
- `cargo check`

Hard stop on any failure.

### Module-level test requirement (Rust)

Run tests for every crate containing modified files:

```bash
cargo test -p fundamental
cargo test -p trustify-tests
```

(Package names resolved via `cargo metadata --no-deps --format-version 1`.)

### Duplication check

Search for overlapping functions or logic. Verify `SeveritySummary` does not
duplicate an existing struct. Verify the service method does not duplicate
existing aggregation logic.

### Data-flow trace

**Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID
path parameter.

**Processing**:
1. Axum extracts `Path<Id>` from URL
2. Handler calls `AdvisoryService::severity_summary(id, tx)`
3. Service queries `sbom_advisory` join table for the given SBOM ID
4. Service deduplicates by advisory ID
5. Service fetches severity from each advisory via `AdvisorySummary.severity`
6. Service counts by severity level, builds `SeveritySummary`

**Output**: JSON response `{ critical: N, high: N, medium: N, low: N, total: N }`
with HTTP 200, or HTTP 404 if SBOM not found.

All stages connected. No incomplete paths.

### Contract and sibling parity

- **Contract**: handler returns `Result<Json<SeveritySummary>, AppError>` consistent
  with all other endpoint handlers.
- **Sibling parity**: new endpoint follows the same error handling, response wrapping,
  and logging patterns as `get.rs` and `list.rs` in the advisory endpoints module.
- **Cross-module entity**: read-only query against `sbom_advisory` -- no write
  conflicts with ingestor module.
- **Caller-site**: not applicable (new endpoint, no existing callers).

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns aggregated
severity counts (critical, high, medium, low, total) for advisories linked
to a given SBOM. Includes deduplication by advisory ID and 404 handling for
non-existent SBOMs.

Implements TC-9201"
```

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

Determine if working in a fork. Adjust `gh pr create` flags accordingly.

### Push and create PR

```bash
git push -u origin TC-9201

gh pr create --base main \
  --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" \
  --body "## Summary
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint returning aggregated severity counts
- New \`SeveritySummary\` response struct with critical/high/medium/low/total counts
- Service method queries sbom_advisory join table with deduplication by advisory ID
- Integration tests covering happy path, 404, empty SBOM, and deduplication

Implements [TC-9201](<webUrl>)

## Test Plan
- [x] Valid SBOM with known advisories returns correct severity counts
- [x] Non-existent SBOM ID returns 404
- [x] SBOM with no advisories returns all zeros
- [x] Duplicate advisory links are deduplicated"
```

(If GitHub Issue custom field was populated, append `Closes <owner>/<repo>#<number>`
to the PR description body.)

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** on TC-9201 using ADF format:

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
Implementation complete for TC-9201.

PR: <PR-URL>

Changes:
- Created SeveritySummary response struct
- Added severity_summary method to AdvisoryService
- Created GET /api/v2/sbom/{id}/advisory-summary endpoint handler
- Registered new route in advisory endpoints
- Added 4 integration tests (happy path, 404, empty, deduplication)

No deviations from the plan.
```

(With the skill footnote appended per `shared/comment-footnote.md`.)

3. **Transition** TC-9201 to "In Review":

```
jira.transition_issue("TC-9201") -> In Review
```
