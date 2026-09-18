# Implementation Plan -- TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Jira Issue**: TC-9201

---

## Step 0 -- Validate Project Configuration

Verified that CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`), Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured with rust-analyzer

All sections valid. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback. REST API commands are available via `python3 scripts/jira-client.py`.

## Step 1 -- Fetch and Parse Jira Task

Fetch via `jira.get_issue("TC-9201")`. Parsed sections:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add service method and REST endpoint for advisory severity aggregation per SBOM |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs`, `server/src/main.rs` (no changes) |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Acceptance Criteria | 5 items (correct response format, 404 for missing SBOM, deduplication, zero defaults, performance) |
| Test Requirements | 4 tests (correct counts, 404, all zeros, deduplication) |
| Dependencies | None |
| Target PR | Not present (default flow) |
| Bookend Type | Not present (default flow) |
| Review Context | Not present |

Capture `webUrl` from the API response for PR description linking.

Look up GitHub Issue custom field (`customfield_10747`) from the fetched issue fields. If present, parse `owner/repo#number` for use in PR description `Closes` line.

All required sections are present. No missing information. Proceed.

## Step 1.5 -- Verify Description Integrity

(Detailed in `outputs/digest-match.md`)

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate digest comment matching marker `[sdlc-workflow] Description digest:`
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment edit detection: `created` equals `updated` -- comment is unmodified, no warning needed
5. Extract stored digest: format tag `sha256-md`, hex `a1b2c3d4e5f67890...`
6. Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
7. Compare format tags: both `sha256-md` -- tags match
8. Compare hex digests: match confirmed
9. Outcome: proceed silently, no user prompt, no added latency

## Step 2 -- Verify Dependencies

No dependencies listed for TC-9201. Skip dependency verification.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID: `jira.user_info()`
2. Assign task: `jira.edit_issue("TC-9201", assignee=<current-user-account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use `mcp__serena_backend__get_symbols_overview` on each file to understand structure:

- **`modules/fundamental/src/advisory/service/advisory.rs`** -- understand `AdvisoryService` struct, its existing methods (`fetch`, `list`, `search`), method signatures and patterns (especially parameter types like `Id`, `Transactional`)
- **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- understand route registration pattern (`Router::new().route(...)`)
- **`modules/fundamental/src/advisory/model/mod.rs`** -- understand module registration pattern (existing `pub mod` declarations)

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:

- `AdvisoryService::fetch` -- to replicate the service method pattern
- `AdvisoryService::list` -- to understand query patterns
- The handler function in `modules/fundamental/src/advisory/endpoints/get.rs` -- to replicate endpoint pattern
- `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` -- to understand the `severity` field type

### 4.2 Inspect related entities

- Use `mcp__serena_backend__find_symbol` on `sbom_advisory` entity in `entity/src/sbom_advisory.rs` to understand the join table structure
- Check `common/src/error.rs` for `AppError` pattern to replicate error handling

### 4.3 Check backward compatibility

- Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to confirm adding a method won't break existing callers
- Use `mcp__serena_backend__find_referencing_symbols` on the `endpoints/mod.rs` route registration to understand how routes are mounted

### 4.4 Convention conformance analysis

Examine sibling files for patterns:

**Production code siblings:**
- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- endpoint handler patterns
- `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs` -- cross-module endpoint patterns
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- model struct patterns

**Test siblings:**
- `tests/api/advisory.rs` -- test setup, assertion style, database fixture patterns
- `tests/api/sbom.rs` -- cross-module test patterns

**Expected conventions to discover:**
- Naming: `verb_noun` function naming, `PascalCase` structs
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Endpoint pattern: `Path<Id>` extraction, service call, `Json` response
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)`, value-based checks
- Import organization: grouped by crate vs local
- Response serialization: `#[derive(Serialize, Deserialize)]` on response structs

### 4.5 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root (`./CONVENTIONS.md`). If present, read it and extract:
- CI check commands for Step 9 verification
- Code generation commands
- Any project-specific conventions

### 4.6 Documentation file identification

Identify docs to check in Step 9:
- `docs/api.md` -- REST API reference (new endpoint needs documenting)
- `docs/architecture.md` -- may reference module structure
- `README.md` -- check if API endpoints are listed

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file containing the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for a given SBOM.
///
/// Provides counts per severity level and a total, enabling dashboard widgets
/// to render severity breakdowns without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

Derive `Default` to ensure all severity levels default to 0 when no advisories exist (acceptance criterion 4).

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:

```rust
pub mod severity_summary;
```

### 6.3 Add `severity_summary` method to `AdvisoryService`

In `modules/fundamental/src/advisory/service/advisory.rs`, add a method following the existing `fetch`/`list` pattern:

```rust
/// Computes a severity summary for advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to sbom_id
    // 2. Join with advisory table to get severity field
    // 3. Deduplicate by advisory ID (SELECT DISTINCT or GROUP BY)
    // 4. Count per severity level
    // 5. Build and return SeveritySummary with defaults of 0
    //
    // If SBOM does not exist, return 404 error consistent with existing SBOM endpoints
}
```

Key implementation details:
- Use SeaORM query builder following existing patterns in `AdvisoryService`
- Use the `sbom_advisory` join table from `entity/src/sbom_advisory.rs`
- Access `AdvisorySummary.severity` field for severity classification
- Deduplicate by advisory ID to satisfy acceptance criterion 3
- Return `AppError` with `.context()` for error cases
- Return 404 when SBOM ID does not exist (check SBOM existence first, consistent with existing SBOM endpoints)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts per severity level for all advisories
/// linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following existing patterns:

```rust
mod severity_summary;

// In the router builder, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Verify `server/src/main.rs`

Confirm no changes needed -- routes auto-mount via module registration as stated in the task description.

### 6.7 Code quality checks

- All new structs and public functions have documentation comments (using `///`)
- Defensive property access: guard against null severity fields from `AdvisorySummary` using `.unwrap_or_default()` or equivalent
- Error handling uses `Result<T, AppError>` with `.context()` wrapping

### 6.8 Documentation impact

- Update `docs/api.md` with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation
- No `Documentation Updates` section in the task, so check identified doc files and update only those directly impacted

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests following patterns from `tests/api/advisory.rs`:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known linked advisories returns correct
/// severity counts broken down by level.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with advisories of known severities
    //   (e.g., 2 critical, 1 high, 3 medium, 0 low)
    
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    
    // Then the response status is 200
    // And the response body contains:
    //   critical: 2, high: 1, medium: 3, low: 0, total: 6
    assert_eq!(resp.status(), StatusCode::OK);
    assert_eq!(body.critical, 2);
    assert_eq!(body.high, 1);
    assert_eq!(body.medium, 3);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 6);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting a severity summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID
    
    // When requesting GET /api/v2/sbom/{non_existent_id}/advisory-summary
    
    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary with all zero counts.
#[tokio::test]
async fn test_severity_summary_empty() {
    // Given an SBOM with no linked advisories
    
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    
    // Then all severity counts are 0 and total is 0
    assert_eq!(resp.status(), StatusCode::OK);
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated in the count

```rust
/// Verifies that duplicate advisory links in the join table are deduplicated
/// so each advisory is counted only once in the severity summary.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM with a critical advisory linked twice in sbom_advisory
    
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    
    // Then critical count is 1 (not 2) and total is 1
    assert_eq!(resp.status(), StatusCode::OK);
    assert_eq!(body.critical, 1);
    assert_eq!(body.total, 1);
}
```

All tests use value-based assertions (not length-only checks) per skill guidance. Each test has a documentation comment and given-when-then structure. Run tests with:

```bash
cargo test -p trustify-tests
```

or if the test crate name differs, resolve via `cargo metadata --no-deps --format-version 1` to find the correct package name for the `tests/` directory.

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET endpoint returns `{ critical, high, medium, low, total }` | Verified by test 1 (correct response structure and values) and endpoint implementation |
| Returns 404 when SBOM ID does not exist | Verified by test 2 |
| Counts only unique advisories (deduplication) | Verified by test 4 and SQL DISTINCT/GROUP BY in service method |
| All severity levels default to 0 | Verified by test 3 and `#[derive(Default)]` on `SeveritySummary` |
| Response time under 200ms for 500 advisories | Verified by SQL query efficiency (single aggregation query, no N+1) |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

Expected modified/created files:
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)

If `docs/api.md` was updated (documentation impact), flag as out-of-scope and ask for user approval since it is not listed in Files to Modify.

### Untracked file check

Run `git status --short` and check for untracked files in directories with modified files. Flag any referenced or proximity-matched untracked files for user approval.

### Dead parameter detection

Scan modified functions for parameters that are no longer used after the implementation changes. Since we are primarily adding new code (not removing), this is unlikely to surface issues, but verify nonetheless.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation currency

Check `docs/api.md` -- if it documents API endpoints, it needs the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added.

### Documentation scope preservation

Not applicable (no documentation sections are being replaced).

### Duplication check

Search repository for existing severity aggregation or counting logic to avoid duplication. Grep for `severity_summary`, `SeveritySummary`, `severity.*count`, etc.

### CI checks from CONVENTIONS.md

If `CONVENTIONS.md` contains CI check commands, run all of them. Hard stop on any non-zero exit.

### Module-level test requirement (Rust)

Run `cargo metadata --no-deps --format-version 1` to resolve crate names for modified files. Run `cargo test -p <crate-name>` for each crate containing modified files. Hard stop on failure.

### Data-flow trace

Trace the new feature's data flow:
1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with path parameter `id`
2. **Processing**: Axum extracts `Path<Id>`, passes to handler, handler calls `AdvisoryService::severity_summary`, service queries `sbom_advisory` join table with `advisory` join, deduplicates by advisory ID, counts by severity level
3. **Output**: `SeveritySummary` struct serialized as JSON response `{ critical, high, medium, low, total }`

All stages connected. No incomplete paths.

### Query-scope verification

The service method queries advisories linked to a specific SBOM ID (filtered by `sbom_id`). The query scope matches the task's target scope -- no broader-than-necessary queries.

### Contract & sibling parity

| Check | Finding |
|---|---|
| Contract | `SeveritySummary` is a standalone struct (no trait impl required). Endpoint handler follows `Result<Json<T>, AppError>` contract. |
| Sibling parity | Compare with `get.rs` and `list.rs` handlers -- ensure logging, error handling, and response patterns match. |
| Cross-module entity | Uses `sbom_advisory` join table read-only (SELECT) -- no write conflicts with other modules. |
| Caller-site | New endpoint, no existing callers to compare. Service method is new, called only from the new handler. |

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

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
zero-defaults for missing severity levels.

Implements TC-9201"
```

If `docs/api.md` was modified and user-approved, include it in the commit.

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If upstream exists, parse owner/repo for fork-aware PR creation. Otherwise, use default `gh pr create`.

### Push and create PR

```bash
git push -u origin TC-9201
```

Create PR with `--base main`:

```bash
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning severity counts per level
- Add `SeveritySummary` response model with `critical`, `high`, `medium`, `low`, `total` fields
- Add `AdvisoryService::severity_summary` method with deduplication by advisory ID
- Add integration tests for correct counts, 404, empty SBOM, and deduplication

Implements [TC-9201](<webUrl>)

## Test plan

- [ ] Verify endpoint returns correct severity counts for SBOM with known advisories
- [ ] Verify 404 response for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no advisories
- [ ] Verify duplicate advisory links are deduplicated
- [ ] Verify response time acceptable for SBOMs with many advisories
EOF
)"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL using ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with PR link, summary of changes, and any deviations from plan.

3. **Transition** to In Review:

```
jira.transition_issue("TC-9201") -> In Review
```
