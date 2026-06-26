# Implementation Plan: TC-9201 -- Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.

## Pre-Implementation Steps

### Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID
- Code Intelligence: Tool naming convention `mcp__serena_backend__<tool>`

All present -- proceed.

### Step 0.5 -- JIRA Access Initialization

Attempt MCP for all JIRA operations. Fall back to REST API if MCP fails.

### Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add severity aggregation service and REST endpoint
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes**: Follow existing patterns in advisory endpoints and service
- **Acceptance Criteria**: 5 items
- **Test Requirements**: 4 items
- **Dependencies**: None
- **Target PR**: Not present (default flow)
- **Bookend Type**: Not present (default flow)
- **GitHub Issue custom field**: Check `customfield_10747` for linked GitHub issue

Capture the issue's `webUrl` for use in the PR description.

### Step 1.5 -- Verify Description Integrity

(See digest-match.md for full details.)

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate comment starting with `[sdlc-workflow] Description digest:`
3. Found: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` == `updated` -- not edited, no warning
5. Not legacy format (tagged `sha256-md`) -- no legacy warning
6. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
7. Format tags match (both `sha256-md`), hex digests match
8. **Proceed silently** -- no user prompt, no delay

### Step 2 -- Verify Dependencies

Task has no dependencies ("Depends on: None"). Proceed immediately.

### Step 3 -- Transition to In Progress and Assign

1. Get current user: `jira.user_info()`
2. Assign task: `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition: `jira.transition_issue("TC-9201")` to In Progress

## Understanding the Code (Step 4)

### Code Inspection via Serena

Use `mcp__serena_backend__<tool>` for code intelligence:

1. **Inspect files to modify:**
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` struct and its methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration

2. **Read specific symbols:**
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to see the pattern for service methods (takes `&self, id: Id, tx: &Transactional<'_>`)
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` in `model/summary.rs` to see the `severity` field
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the GET handler in `endpoints/get.rs` to see endpoint pattern (Path extraction, service call, JSON response)

3. **Check references:**
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to confirm how it's injected into handlers
   - Check `entity/src/sbom_advisory.rs` for the join table structure linking SBOMs to advisories

4. **Pattern search:**
   - `mcp__serena_backend__search_for_pattern` for `Router::new().route` in endpoints/mod.rs to understand route registration
   - `mcp__serena_backend__search_for_pattern` for `AppError` usage in handlers

### Sibling Convention Analysis

**Sibling endpoint files** (from `modules/fundamental/src/advisory/endpoints/`):
- `get.rs` -- GET handler pattern: extract `Path<Id>`, call service, return `Json(result)`
- `list.rs` -- list handler pattern

**Sibling model files** (from `modules/fundamental/src/advisory/model/`):
- `summary.rs` -- `AdvisorySummary` struct with `severity` field
- `details.rs` -- `AdvisoryDetails` struct

**Sibling service files** (from `modules/fundamental/src/sbom/service/`):
- `sbom.rs` -- `SbomService` with `fetch`, `list`, `ingest` methods

**Expected discovered conventions:**
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: service methods follow `verb_noun` pattern
- Response: return struct directly, Axum `Json` handles serialization
- Route registration: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`

### Test Convention Analysis

**Sibling test files** (from `tests/api/`):
- `advisory.rs` -- advisory endpoint integration tests
- `sbom.rs` -- SBOM endpoint integration tests

**Expected discovered test conventions:**
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Error cases: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Test naming: `test_<endpoint>_<scenario>` pattern
- Integration tests hit a real PostgreSQL test database

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (trustify-backend). Read it and extract:
- CI check commands (for Step 9 verification)
- Code generation commands (if any)
- Any additional naming or structural conventions

### Documentation File Identification

Look for:
- `docs/api.md` -- API documentation (may need updating for new endpoint)
- `docs/architecture.md` -- architecture overview
- `README.md` at repository root

## Branch Creation (Step 5)

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Implementation (Step 6)

### File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Provides per-severity-level counts (Critical, High, Medium, Low) and a total,
/// enabling dashboard widgets to render severity breakdowns without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: usize,
    /// Count of advisories with High severity.
    pub high: usize,
    /// Count of advisories with Medium severity.
    pub medium: usize,
    /// Count of advisories with Low severity.
    pub low: usize,
    /// Total count of unique advisories across all severity levels.
    pub total: usize,
}
```

### File 2: Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration for the new model:

```rust
pub mod severity_summary;
```

### File 3: Add `severity_summary` method to `AdvisoryService`

Modify `modules/fundamental/src/advisory/service/advisory.rs`:

- Add a `severity_summary` method following the same pattern as `fetch` and `list`
- Method signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- For each linked advisory, read its `AdvisorySummary` to get the `severity` field
- Deduplicate by advisory ID (to satisfy acceptance criterion: "counts only unique advisories")
- Count by severity level (Critical, High, Medium, Low)
- Default all severity counts to 0 when no advisories exist at that level (handled by `Default` derive)
- Return 404 (`AppError`) when the SBOM ID does not exist, consistent with existing SBOM endpoints

### File 4: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
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

### File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing pattern:

```rust
use severity_summary::get_severity_summary;

// Add to the Router:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### File 6: Verify `server/src/main.rs`

Confirm no changes needed -- routes auto-mount via module registration as stated in the task description.

### Code Quality Checks

- All new structs (`SeveritySummary`) have documentation comments
- All new public functions (`get_severity_summary`, `severity_summary`) have documentation comments
- Error handling uses `Result<T, AppError>` with `.context()` wrapping
- Follow sibling conventions for naming, imports, and module structure

### Documentation Impact

- Check `docs/api.md` for API endpoint documentation -- add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- No architectural changes, so `docs/architecture.md` does not need updating

## Write Tests (Step 7)

### File 7: Create `tests/api/advisory_summary.rs`

Write integration tests following the sibling test conventions discovered in Step 4:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with known advisory links at various severity levels
    // (set up test SBOM and advisories in the test database)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response should contain correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical);
    assert_eq!(summary.high, expected_high);
    assert_eq!(summary.medium, expected_medium);
    assert_eq!(summary.low, expected_low);
    assert_eq!(summary.total, expected_total);
}

/// Verifies that a non-existent SBOM ID returns a 404 response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").await;

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then counts should reflect unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Verify total matches unique advisory count, not total link count
    assert_eq!(summary.total, expected_unique_count);
}
```

Run tests:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Verify Acceptance Criteria (Step 8)

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by test_advisory_summary_returns_correct_counts |
| Returns 404 when SBOM ID does not exist | Verified by test_advisory_summary_not_found |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by test_advisory_summary_deduplicates |
| All severity levels default to 0 when no advisories exist | Verified by test_advisory_summary_empty |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by query design using joins rather than N+1 queries; confirm with manual test if needed |

## Self-Verification (Step 9)

### Scope Containment

Run `git diff --name-only` and verify all modified/created files match:

**Files to Modify:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

If `docs/api.md` was modified (documentation impact), flag as out-of-scope and ask user to approve.

### Untracked File Check

Run `git status --short` and check for `??` entries in directories where implementation occurred. Flag any untracked files referenced by code.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation Currency

Verify `docs/api.md` covers the new endpoint if it documents existing endpoints.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`, `cargo build`). Hard stop on any failure.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (id) -> call `AdvisoryService::severity_summary(id)` -> query `sbom_advisory` join table -> load `AdvisorySummary` for each linked advisory -> deduplicate by advisory ID -> count by severity level -> return `SeveritySummary` JSON -- **COMPLETE**

### Contract & Sibling Parity

- `SeveritySummary` -- no trait/interface contract to implement (standalone response struct with Serialize/Deserialize)
- Sibling parity with `get.rs` handler: error handling with `.context()`, `Result<Json<T>, AppError>` return type, `Path<Id>` extraction -- verify all present
- Caller-site parity: no shared abstraction calls to verify (this is a new endpoint)

### Cross-Section Reference Consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` is referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent
- Route registration in both Files to Modify (`endpoints/mod.rs`) and Implementation Notes (`endpoints/mod.rs`) -- consistent

### Duplication Check

Search for existing severity aggregation or counting logic in the repository. If found, refactor to reuse it.

## Commit and Push (Step 10)

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary response
model, AdvisoryService.severity_summary method, and integration tests.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

Add a new `GET /api/v2/sbom/{id}/advisory-summary` endpoint that aggregates advisory severity counts for a given SBOM, returning Critical, High, Medium, and Low counts plus a total.

### Changes
- **New model**: `SeveritySummary` response struct in `modules/fundamental/src/advisory/model/severity_summary.rs`
- **New endpoint**: GET handler in `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- **Service method**: `severity_summary` added to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`
- **Route registration**: New route registered in `modules/fundamental/src/advisory/endpoints/mod.rs`
- **Integration tests**: 4 test cases covering correct counts, 404, empty SBOM, and deduplication

Implements [TC-9201](<webUrl>)
EOF
)"
```

If a GitHub issue was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Update Jira (Step 11)

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
   - No deviations from the plan
   - Comment footer with plugin version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue("TC-9201") -> In Review
```
