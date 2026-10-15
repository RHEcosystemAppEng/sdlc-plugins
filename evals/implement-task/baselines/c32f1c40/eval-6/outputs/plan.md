# Implementation Plan — TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Issue:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001
**Bookend Type:** None
**Target PR:** None

## Step 0 — Validate Project Configuration

Read the project CLAUDE.md and verify the required sections exist:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** — present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** — present, Serena instance `serena_backend` configured with `rust-analyzer`

Validation passes. Proceed.

## Step 0.5 — Jira Access Initialization

Attempt MCP for all Jira operations. Fall back to REST API if MCP fails, per the established protocol.

## Step 1 — Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue(TC-9201)`.

### Parsed Sections

| Section | Content |
|---|---|
| **Repository** | trustify-backend |
| **Target Branch** | main |
| **Description** | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| **Files to Modify** | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| **Files to Create** | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| **API Changes** | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| **Acceptance Criteria** | 5 criteria (severity counts, 404 handling, deduplication, zero defaults, performance) |
| **Test Requirements** | 4 test cases (correct counts, 404, empty SBOM, deduplication) |
| **Dependencies** | None |
| **Target PR** | None |
| **Bookend Type** | None |

### GitHub Issue Extraction

Look up `customfield_10747` (GitHub Issue custom field from Jira Configuration). If populated, extract the owner/repo/number for use in the PR description. If empty, skip.

### Issue Web URL

Capture the `webUrl` from the API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description's "Implements" link.

## Step 1.5 — Verify Description Integrity

See `outputs/digest-match.md` for the detailed verification analysis.

**Result:** Digest comment found, comment unedited, format tags match (`sha256-md`), hex digests match. Proceed silently.

## Step 2 — Verify Dependencies

The task has no dependencies. Proceed.

## Step 3 — Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to the current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 — Understand the Code

### 4.1 Serena Instance

Use `mcp__serena_backend__<tool>` for all code intelligence operations on trustify-backend.

### 4.2 Inspect Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `get_symbols_overview` to see AdvisoryService struct and existing methods (`fetch`, `list`, `search`)
   - `find_symbol` with `include_body=true` on `fetch` and `list` methods to understand the pattern (parameters, return types, transaction handling)
   - Identify how `sbom_advisory` join table is queried

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `get_symbols_overview` to see current route registrations
   - Understand the `Router::new().route()` pattern for registering handlers

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - `get_symbols_overview` to see existing `pub mod` declarations (summary, details)
   - Pattern for registering new model modules

### 4.3 Inspect Related Files

1. **`modules/fundamental/src/advisory/model/summary.rs`**
   - `find_symbol` on `AdvisorySummary` to understand the `severity` field type and values
   - This determines the severity levels available for counting

2. **`modules/fundamental/src/advisory/endpoints/get.rs`**
   - `find_symbol` with `include_body=true` on the GET handler to understand the endpoint pattern (Path extraction, service call, JSON response, error handling)

3. **`entity/src/sbom_advisory.rs`**
   - `get_symbols_overview` to understand the join table schema (columns, relationships)
   - This is the table used to find advisories linked to an SBOM

4. **`common/src/error.rs`**
   - `find_symbol` on `AppError` to understand error handling pattern and `.context()` wrapping

### 4.4 Check Backward Compatibility

- `find_referencing_symbols` on `AdvisoryService` to identify all callers — ensure the new `severity_summary` method does not conflict with existing methods

### 4.5 Convention Conformance Analysis

Examine sibling files for patterns:

- **Endpoint siblings:** `endpoints/get.rs`, `endpoints/list.rs` — extract patterns for Path extraction, service injection, response types, error handling
- **Model siblings:** `model/summary.rs`, `model/details.rs` — extract patterns for struct definition, derives, serde attributes
- **Service siblings:** `service/advisory.rs` existing methods — extract patterns for method signature, transaction handling, query construction
- **Test siblings:** `tests/api/advisory.rs`, `tests/api/sbom.rs` — extract patterns for test setup, HTTP client usage, assertion style, response status checks

Expected conventions:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: `verb_noun` pattern (e.g., `severity_summary`)
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Endpoint pattern: `Path<Id>` extraction, call service, return `Json`
- Model structs: `#[derive(Debug, Clone, Serialize, Deserialize)]`

### 4.6 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract:
- CI check commands for Step 9 verification
- Code generation commands
- Any project-specific naming or structural conventions

### 4.7 Documentation File Identification

Identify relevant documentation files:
- `docs/api.md` — may need updating for the new endpoint
- `README.md` — check if it documents API endpoints
- `docs/architecture.md` — likely no changes needed

## Step 5 — Create Branch

No Target PR and no Bookend Type — use the default flow:

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 — Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct following sibling patterns from `summary.rs` and `details.rs`:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u32,
    /// Count of high-severity advisories.
    pub high: u32,
    /// Count of medium-severity advisories.
    pub medium: u32,
    /// Count of low-severity advisories.
    pub low: u32,
    /// Total count of unique advisories.
    pub total: u32,
}
```

Key decisions:
- Use `#[derive(Default)]` so all fields default to 0 (acceptance criterion: all zeros when no advisories)
- Use `u32` for counts (consistent with typical Rust count types)
- Documentation comments on the struct and every field

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module registration:

```rust
pub mod severity_summary;
```

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService` following the pattern of `fetch` and `list`:

```rust
/// Computes aggregated severity counts for advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Join with advisory table to get severity field
    // Deduplicate by advisory ID
    // Count by severity level
    // Return SeveritySummary with counts and total
}
```

Implementation approach:
- Use the `sbom_advisory` join table from `entity/src/sbom_advisory.rs` to find linked advisories
- Join with advisory data to access the `severity` field from `AdvisorySummary`
- Apply `DISTINCT` or equivalent deduplication by advisory ID (acceptance criterion: deduplicate)
- Group/count by severity level
- Default all unrepresented severity levels to 0 via `SeveritySummary::default()`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern from `endpoints/get.rs`:

```rust
use axum::{extract::Path, Json};

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transaction context */,
) -> Result<Json<SeveritySummary>, AppError> {
    // Call service.severity_summary(id, &tx)
    // Return 404 if SBOM not found (matching existing SBOM endpoint behavior)
    // Return Json(summary) on success
}
```

Key decisions:
- Follow the exact parameter extraction pattern from `get.rs` (`Path<Id>`)
- Return `Json<SeveritySummary>` directly (Axum handles serialization)
- Return 404 via `AppError` with `.context()` when SBOM ID does not exist
- Verify SBOM existence before querying advisories (consistent with existing SBOM endpoints)

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing `Router::new().route()` pattern:

```rust
use severity_summary::get_severity_summary;

// In route registration:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### 6.6 Cross-repo API Contract Verification

Not applicable — this is a backend-only task with no frontend consumer to verify against.

### 6.7 Documentation Impact

- No Documentation Updates section in the task description
- Check `docs/api.md` — if it documents REST endpoints, add an entry for `GET /api/v2/sbom/{id}/advisory-summary`
- Keep documentation updates lightweight and scoped

## Step 7 — Write Tests

### Create `tests/api/advisory_summary.rs`

Following sibling test patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

#### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns correct per-severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories of known severities (e.g., 2 Critical, 1 High, 0 Medium, 3 Low)
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response status is 200 and the body contains { critical: 2, high: 1, medium: 0, low: 3, total: 6 }
}
```

#### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a SBOM ID that does not exist
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response status is 404
}
```

#### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response status is 200 and the body contains { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
}
```

#### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links in sbom_advisory are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM where the same advisory is linked twice
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the advisory is counted only once in the severity total
}
```

Test conventions applied:
- Each test has a `///` documentation comment explaining what it verifies
- Non-trivial tests use given-when-then section comments
- Value-based assertions on actual severity counts (not length-only checks)
- `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` patterns from siblings

Run tests: `cargo test -p <crate-name>` (resolve crate name via `cargo metadata`).

## Step 8 — Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Test 1 validates correct response shape and values |
| Returns 404 for non-existent SBOM ID | Test 2 validates 404 status |
| Counts only unique advisories (deduplicates by advisory ID) | Test 4 validates deduplication |
| All severity levels default to 0 when no advisories exist | Test 3 validates zero defaults |
| Response time under 200ms for SBOMs with up to 500 advisories | Verify query uses indexed joins; measure if test DB has sufficient data |

## Step 9 — Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all files are within the task's Files to Modify and Files to Create:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Flag any out-of-scope files for user approval.

### Untracked File Check

Run `git status --short`, filter `??` entries in modified directories. Flag any referenced or proximity-matched untracked files.

### Dead Parameter Detection

Scan modified functions for unused parameters after implementation. Remove any dead parameters and update callers.

### Sensitive Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Ensure no secrets are in the staged diff.

### Documentation Currency

If `docs/api.md` documents endpoints and was not updated in Step 6, update it now.

### Duplication Check

Search the repository for existing severity aggregation logic or similar counting patterns to avoid duplication.

### CI Checks from CONVENTIONS.md

If CI check commands were extracted from `CONVENTIONS.md` in Step 4, run all of them. Hard stop on any failure.

### Module-Level Test Requirement (Rust)

Resolve the crate name for each modified file via `cargo metadata --no-deps --format-version 1`. Run `cargo test -p <crate-name>` for each crate containing modified files. Hard stop on any failure.

### Contract and Sibling Parity

| Check | Verification |
|---|---|
| **Contract** | Verify `severity_summary` method signature matches AdvisoryService patterns (parameter types, return type, error handling) |
| **Sibling parity** | Verify new endpoint follows same logging, error handling, and response patterns as `get.rs` and `list.rs` |
| **Cross-module entity** | Verify `sbom_advisory` query uses consistent transaction handling and constraint handling as other modules |
| **Caller-site** | Not applicable — this is a new endpoint with no existing callers |

### Data-Flow Trace

Trace the complete data lifecycle:
1. **Input:** HTTP GET request with SBOM ID path parameter
2. **Processing:** Extract path parameter, call AdvisoryService.severity_summary(), query sbom_advisory join table, join with advisory data, deduplicate, count by severity
3. **Output:** JSON response with severity counts

All stages connected. No incomplete paths.

## Step 10 — Commit and Push

### Fork Detection

```bash
git remote get-url upstream 2>/dev/null
```

Determine if working in a fork. Adjust `gh pr create` flags accordingly.

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
404 handling for non-existent SBOMs.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

- Add `SeveritySummary` response model with per-severity counts
- Add `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, deduplicates by advisory ID, and counts by severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning `{ critical, high, medium, low, total }`
- Add integration tests: correct counts, 404 for missing SBOM, zero defaults, deduplication

Implements [TC-9201](<webUrl>)

## Test Plan

- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns correct severity counts for a known SBOM
- [ ] Verify 404 response for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no advisories
- [ ] Verify duplicate advisory links are counted once
- [ ] Verify response time under 200ms for SBOMs with up to 500 advisories
EOF
)"
```

If a GitHub issue reference was extracted in Step 1, append a `Closes <owner>/<repo>#<number>` line to the PR body.

## Step 11 — Update Jira

1. **Set PR custom field** — Update `customfield_10875` (Git Pull Request custom field) on TC-9201 with the PR URL using ADF format:

   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** — Post a comment summarizing the implementation:

   ```
   jira.add_comment(TC-9201, "Implementation complete. PR: <PR-URL>

   Changes:
   - Created SeveritySummary model struct
   - Added severity_summary method to AdvisoryService
   - Added GET /api/v2/sbom/{id}/advisory-summary endpoint
   - Added 4 integration tests covering all acceptance criteria

   No deviations from the plan.

   [sdlc-workflow:implement-task]")
   ```

3. **Transition** — Move TC-9201 to "In Review":

   ```
   jira.transition_issue(TC-9201) → In Review
   ```
