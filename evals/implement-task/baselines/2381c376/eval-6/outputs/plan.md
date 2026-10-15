# Implementation Plan for TC-9201

**Task:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured with rust-analyzer

All sections are present and complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all Jira operations. Fall back to REST API via `scripts/jira-client.py` if MCP fails, with user confirmation.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

| Section | Value |
|---------|-------|
| **Repository** | trustify-backend |
| **Target Branch** | main |
| **Description** | Add severity aggregation service method and REST endpoint for SBOM advisory summaries |
| **Files to Modify** | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| **Files to Create** | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| **API Changes** | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| **Target PR** | None |
| **Bookend Type** | None |
| **Dependencies** | None |

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

Check the GitHub Issue custom field (`customfield_10747`) -- extract the GitHub issue reference if present, store as `<owner>/<repo>#<number>` for the PR description.

All required sections are present. Proceed.

## Step 1.5 -- Verify Description Integrity

(See `outputs/digest-match.md` for full details.)

1. Fetch comments on TC-9201
2. Locate the digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890...`
3. Comment `created` equals `updated` -- not edited, no warning
4. Extract stored digest: format tag `sha256-md`, hex digest `a1b2c3...`
5. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
6. Format tags match (both `sha256-md`)
7. Hex digests match

**Result:** Match. Proceed silently -- no user prompt required.

## Step 2 -- Verify Dependencies

The task specifies "Depends on: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Using `mcp__serena_backend__get_symbols_overview` on each file:

- **`modules/fundamental/src/advisory/service/advisory.rs`** -- understand `AdvisoryService` struct and its existing methods (`fetch`, `list`, `search`). Identify the method signature pattern (takes `&self`, entity ID, `tx: &Transactional<'_>`).
- **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- understand route registration pattern (`Router::new().route(...)` calls).
- **`modules/fundamental/src/advisory/model/mod.rs`** -- understand how submodules are registered (`pub mod summary;`, `pub mod details;`).

### 4.2 Inspect sibling/reference files

Using `mcp__serena_backend__find_symbol` with `include_body=true`:

- **`modules/fundamental/src/advisory/endpoints/get.rs`** -- read the GET handler to understand the endpoint pattern: path param extraction via `Path<Id>`, service call, JSON response.
- **`modules/fundamental/src/advisory/model/summary.rs`** -- read `AdvisorySummary` struct to understand the `severity` field type and structure.
- **`entity/src/sbom_advisory.rs`** -- understand the join table structure for SBOM-advisory relationships.
- **`common/src/error.rs`** -- understand `AppError` enum and `.context()` wrapping pattern.

### 4.3 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` -- confirm adding a new method won't break existing callers
- The advisory endpoints `mod.rs` -- understand how routes are composed

### 4.4 Convention conformance analysis

Examine 2-3 sibling files to identify conventions:

**Production code conventions (from advisory/endpoints/get.rs, sbom/endpoints/get.rs):**
- Naming: `verb_noun` pattern for handler functions (e.g., `get_advisory`)
- Error handling: `Result<T, AppError>` return type with `.context("descriptive message")`
- Path params: `Path<Id>` extractor
- Response: Return struct directly, Axum's `Json` handles serialization
- Imports: grouped by std, external crates, internal modules

**Test conventions (from tests/api/advisory.rs, tests/api/sbom.rs):**
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)`
- Response validation: deserialize body and assert on specific field values
- Error cases: test 404 for non-existent resources
- Setup: use test database infrastructure

### 4.5 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract CI check commands for Step 9. If not present, proceed normally.

### 4.6 Documentation file identification

Identify documentation files related to the changes:
- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating for new endpoint)
- `docs/architecture.md` -- system architecture overview

## Step 5 -- Create Branch

No Target PR and no Bookend Type -- use default flow:

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
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of linked advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

Follow the pattern from `summary.rs` and `details.rs` in the same model directory. Derive `Serialize`, `Deserialize`, `ToSchema` to match existing model conventions.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module registration:

```rust
pub mod severity_summary;
```

Following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService`:

```rust
/// Computes an aggregate severity summary for all advisories linked to the given SBOM.
///
/// Returns counts of unique advisories at each severity level (Critical, High,
/// Medium, Low) and a total count. Deduplicates by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to this SBOM
    // 2. Join with advisory table to get severity field
    // 3. Deduplicate by advisory ID
    // 4. Count by severity level
    // 5. Return SeveritySummary with counts and total
}
```

Follow the same pattern as `fetch` and `list` methods:
- Same parameter signature pattern (`&self`, ID, transactional reference)
- Use `.context()` for error wrapping
- Use the `sbom_advisory` join table from `entity/src/sbom_advisory.rs`
- Use `AdvisorySummary.severity` field to categorize counts
- Ensure deduplication by advisory ID (use `DISTINCT` or `HashSet`)
- Default all counts to 0 when no advisories exist at a level
- Return 404 (`AppError`) when the SBOM ID does not exist -- verify SBOM existence first, matching existing SBOM endpoint behavior

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns an aggregated severity summary of all advisories linked to the
/// specified SBOM, with counts per severity level and a total.
pub async fn get_advisory_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the endpoint pattern from `get.rs`:
- Extract path params via `Path<Id>`
- Call the service method
- Return `Json` wrapped response
- Use `Result<T, AppError>` with `.context()`

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route, following the existing `Router::new().route(...)` pattern:

```rust
mod severity_summary;

// In the router builder:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

### 6.6 Verify server/main.rs

Per the task description: "no changes needed (routes auto-mount via module registration)". Confirm this by inspecting `server/main.rs` to verify advisory module routes are automatically included.

### 6.7 Code quality checks

- All new structs, functions, and public methods have documentation comments using `///`
- Defensive property access: use `.unwrap_or_default()` or `match` for severity field values that might be null/unexpected
- No new symbols that duplicate existing ones (search for existing severity-related constants or enums)

### 6.8 Documentation impact

- Check if `docs/api.md` documents REST endpoints -- if so, add entry for `GET /api/v2/sbom/{id}/advisory-summary`
- No Documentation Updates section in the task, so only update docs directly impacted

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following tests, following sibling test patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (set up test SBOM with linked advisories: 2 critical, 3 high, 1 medium, 0 low)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, 2)
    // assert_eq!(body.high, 3)
    // assert_eq!(body.medium, 1)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 6)
}

/// Verifies that requesting a summary for a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate links to the same advisory

    // When requesting the advisory summary

    // Then the advisory is counted only once
    // (e.g., one critical advisory linked twice still shows critical: 1, total: 1)
}
```

**Test conventions applied:**
- Value-based assertions on specific field values (not just length checks)
- `///` doc comments on every test function
- Given-when-then section comments for non-trivial tests
- `assert_eq!` with `StatusCode` matching sibling test patterns
- Separate test functions per case (not parameterized, following sibling test patterns)

Run tests: `cargo test -p <crate-name>` for each affected crate.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|-----------|-------------|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Endpoint implemented, response struct matches, test validates correct counts |
| Returns 404 when SBOM ID does not exist | Service checks SBOM existence first, test validates 404 response |
| Counts only unique advisories (deduplicates by advisory ID) | Service uses DISTINCT or HashSet deduplication, test validates with duplicate links |
| All severity levels default to 0 when no advisories exist | SeveritySummary derives Default, test validates all-zero response |
| Response time under 200ms for SBOMs with up to 500 advisories | Single query with JOIN and GROUP BY avoids N+1; index on sbom_advisory join table ensures performance |

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all modified/created files match the Files to Modify and Files to Create sections. Expected files:
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)

Flag any out-of-scope files for user approval (e.g., if `docs/api.md` was updated).

### Untracked file check
Run `git status --short`, filter `??` files in directories with modified files, check for references in staged diff.

### Dead parameter detection
Scan modified functions for unused parameters after changes.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency
Verify `docs/api.md` reflects the new endpoint if it documents REST endpoints.

### Duplication check
Search repository for existing severity aggregation logic, severity counting utilities, or similar helper functions. Refactor to reuse if found.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from `CONVENTIONS.md` (if found). Hard stop on any failure.

### Module-level test requirement (Rust)
Run `cargo metadata --no-deps --format-version 1` to resolve crate names for modified files. Run `cargo test -p <crate-name>` for each affected crate. Hard stop on failure.

### Data-flow trace
Trace the complete data flow:
1. **Input:** HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter
2. **Processing:** Endpoint handler extracts `Path<Id>` -> calls `AdvisoryService::severity_summary` -> queries `sbom_advisory` join table -> joins advisory table -> deduplicates by advisory ID -> counts by severity level -> constructs `SeveritySummary`
3. **Output:** JSON response `{ critical, high, medium, low, total }` or 404 error

All stages connected. Flow is complete.

### Contract & sibling parity
- **Contract:** `SeveritySummary` implements `Serialize`/`Deserialize`/`ToSchema` as required by Axum JSON responses. Handler returns `Result<Json<T>, AppError>` matching endpoint contract.
- **Sibling parity:** New endpoint follows same error handling (`.context()`), response pattern (`Json` wrapper), and route registration pattern as `get.rs` and `list.rs`.
- **Cross-module entity:** `sbom_advisory` join table used read-only; no write concerns.
- **Caller-site:** No shared abstraction calls introduced.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint

Add SeveritySummary model, AdvisoryService.severity_summary method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated advisory severity counts (critical, high, medium, low, total)
for a given SBOM. Includes integration tests for the happy path,
404 on missing SBOM, empty advisory list, and deduplication.

Implements TC-9201"
```

### Fork detection

Check for upstream remote:
```bash
git remote get-url upstream 2>/dev/null
```

If no upstream remote, use default `gh pr create`:

```bash
git push -u origin TC-9201

gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning aggregated advisory severity counts per SBOM
- Add `SeveritySummary` response model with critical/high/medium/low/total fields
- Add `AdvisoryService::severity_summary` method with advisory deduplication
- Add integration tests covering happy path, 404, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns correct severity counts for an SBOM with known advisories
- [ ] Verify 404 response for a non-existent SBOM ID
- [ ] Verify all-zero response for an SBOM with no advisories
- [ ] Verify duplicate advisory links are deduplicated in counts
- [ ] Verify response time under 200ms for SBOMs with up to 500 advisories
EOF
)"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL using ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 summarizing:
   - PR link
   - Changes: added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
   - No deviations from the plan

3. **Transition** TC-9201 to "In Review"
