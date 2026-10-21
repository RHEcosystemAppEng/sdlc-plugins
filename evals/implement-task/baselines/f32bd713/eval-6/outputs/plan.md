# Implementation Plan -- TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns
a summary with counts per severity level (Critical, High, Medium, Low) and a total.

**Jira Issue:** TC-9201
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001
**Dependencies:** None

---

## Step 0 -- Validate Project Configuration

Verify the project CLAUDE.md contains:

1. **Repository Registry** -- Present. `trustify-backend` mapped to Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- Present. Project key `TC`, Cloud ID, Feature issue type ID all configured.
3. **Code Intelligence** -- Present. Tool naming convention documented; `serena_backend` instance configured with `rust-analyzer`.

All required sections are present. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Fetch `TC-9201` via `jira.get_issue("TC-9201")`.

### Parsed Sections

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add severity aggregation service and endpoint for SBOM advisory summaries |
| Files to Modify | 3 files (see below) |
| Files to Create | 3 files (see below) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Bookend Type | Not present |
| Target PR | Not present |
| Dependencies | None |

**Files to Modify:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
- `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`

**Files to Create:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
- `tests/api/advisory_summary.rs` -- integration tests

**Acceptance Criteria:**
1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }`
2. Returns 404 when SBOM ID does not exist
3. Counts only unique advisories (deduplicates by advisory ID)
4. All severity levels default to 0 when no advisories exist
5. Response time under 200ms for SBOMs with up to 500 advisories

**Test Requirements:**
1. Valid SBOM with known advisories returns correct severity counts
2. Non-existent SBOM ID returns 404
3. SBOM with no advisories returns all zeros
4. Duplicate advisory links are deduplicated

Capture `webUrl` from API response for PR description linking.

### GitHub Issue Extraction

Check `customfield_10747` on the fetched issue for a GitHub issue URL. If present, parse `owner/repo#number` for use in PR description `Closes` line. If absent, skip silently.

## Step 1.5 -- Verify Description Integrity

(See `digest-match.md` for full details.)

Retrieve comments, locate the digest comment by marker string `[sdlc-workflow] Description digest:`, confirm the comment was not edited (timestamps match), extract format tag `sha256-md` and hex digest, compute current digest via `python3 scripts/sha256-digest.py`, confirm format tags match, confirm hex digests match. **Result: match. Proceed silently.**

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to In Progress via `jira.transition_issue("TC-9201", "In Progress")`.

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Use `mcp__serena_backend__get_symbols_overview` on each file to modify:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Understand `AdvisoryService` structure, existing methods (`fetch`, `list`, `search`), method signatures, and patterns for `&self`, `Id`, and `Transactional<'_>` parameters.

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Understand route registration pattern (`Router::new().route(...)`) and how existing handlers are wired.

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Understand module registration pattern (`pub mod summary;`, `pub mod details;`).

### 4.2 Inspect Reference Files

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:

- `AdvisoryService::fetch` -- understand the method pattern (parameters, return type, error handling with `.context()`)
- `AdvisoryService::list` -- understand the list pattern for reference
- `AdvisorySummary` struct in `model/summary.rs` -- understand the `severity` field type and structure
- `sbom_advisory` entity in `entity/src/sbom_advisory.rs` -- understand the join table columns for SBOM-advisory linking

### 4.3 Inspect Sibling Files for Convention Conformance

Use `mcp__serena_backend__get_symbols_overview` on 2-3 siblings:

- `modules/fundamental/src/advisory/endpoints/get.rs` -- endpoint handler pattern (Path extraction, service call, JSON response)
- `modules/fundamental/src/advisory/endpoints/list.rs` -- alternative endpoint pattern
- `modules/fundamental/src/advisory/model/summary.rs` -- model struct pattern (derives, field types, serialization)

### 4.4 Check Backward Compatibility

Use `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` -- ensure adding a new method does not break existing callers
- The `advisory/endpoints/mod.rs` route registration -- understand how routes are composed

### 4.5 Non-Symbolic Search

Use `mcp__serena_backend__search_for_pattern` for:
- `AppError` usage patterns in endpoint handlers
- `Path<Id>` extraction pattern in existing handlers
- `Json` response pattern in existing handlers
- `StatusCode::NOT_FOUND` or 404 handling patterns

### 4.6 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at repository root (`./CONVENTIONS.md`). The repo structure shows it exists. Read it and extract:
- CI check commands (formatting, linting, compilation)
- Code generation commands (if any)
- Naming and structural conventions

### 4.7 Convention Conformance Analysis

Based on sibling analysis, document discovered conventions:

**Expected conventions (to be confirmed from code):**
- **Error handling:** `Result<T, AppError>` with `.context()` wrapping
- **Naming:** `verb_noun` pattern for methods (e.g., `fetch_advisory`, `list_advisories`)
- **Endpoint pattern:** Extract `Path<Id>`, call service method, return `Json(result)`
- **Model pattern:** `#[derive(Debug, Clone, Serialize, Deserialize)]` on response structs
- **Route registration:** `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Test assertions:** `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Imports:** organized by crate (std, external, local)

### 4.8 Documentation File Identification

Identify docs potentially affected:
- `docs/api.md` -- REST API reference (new endpoint needs documenting)
- `README.md` -- unlikely to need changes for a single endpoint addition

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

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u32,
    /// Number of advisories with High severity.
    pub high: u32,
    /// Number of advisories with Medium severity.
    pub medium: u32,
    /// Number of advisories with Low severity.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

Follow the `Serialize`/`Deserialize` derive pattern from sibling `summary.rs`.

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module, following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Add `severity_summary` method to `AdvisoryService`

In `modules/fundamental/src/advisory/service/advisory.rs`, add:

```rust
/// Computes aggregated severity counts for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts each severity level. Returns a `SeveritySummary`
/// with per-level counts and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to this SBOM
    // 2. Deduplicate by advisory ID
    // 3. For each unique advisory, fetch its severity from AdvisorySummary
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Return SeveritySummary with counts and total
}
```

Follow the same method signature pattern as `fetch` and `list` (takes `&self`, `Id`, `Transactional`). Use `.context()` for error wrapping.

**Key implementation details:**
- Use `sbom_advisory` entity to find advisories linked to the SBOM
- Deduplicate by advisory ID using a `HashSet` or SQL `DISTINCT`
- Access the `severity` field from `AdvisorySummary` struct
- Return `AppError` with `.context()` if the SBOM does not exist (404 case)
- Verify SBOM existence first, returning 404 if not found, to match existing SBOM endpoint behavior

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the exact pattern from `get.rs`: extract `Path<Id>`, call service, return `Json(result)`.

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Add `mod severity_summary;` at the top of the file.

### 6.6 Documentation Impact

Check `docs/api.md` for existing API documentation. If it documents endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response format.

### 6.7 Code Quality Practices

- All new structs and public functions have documentation comments (shown above)
- Defensive property access: use `.unwrap_or_default()` for severity field access from `AdvisorySummary` in case the value is absent
- No new constants or enums to deduplicate (severity levels come from existing data)

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with four test functions:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that an SBOM with linked advisories returns correct per-severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with advisories of known severities (e.g., 2 Critical, 1 High, 0 Medium, 1 Low)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 and the body contains exact severity counts
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, 2);
    // assert_eq!(body.high, 1);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 1);
    // assert_eq!(body.total, 4);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting a severity summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response status is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero and total is zero
    // assert_eq!(body.critical, 0);
    // assert_eq!(body.high, 0);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate links to the same advisory (e.g., same advisory linked twice)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, 1);  // not 2
}
```

**Test conventions applied:**
- Value-based assertions (assert on specific counts, not just lengths)
- Doc comments on every test function
- Given-When-Then structure comments for non-trivial tests
- `assert_eq!(resp.status(), ...)` pattern matching sibling test files
- Test names follow `test_<feature>_<scenario>` pattern

Run tests: `cargo test -p <crate-name>` (resolve crate name via `cargo metadata`).

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | GET endpoint returns severity counts | Test 1 verifies correct counts in response body |
| 2 | Returns 404 for non-existent SBOM | Test 2 verifies 404 status |
| 3 | Counts only unique advisories | Test 4 verifies deduplication; service uses DISTINCT or HashSet |
| 4 | All severity levels default to 0 | Test 3 verifies all-zero response; `SeveritySummary` derives `Default` |
| 5 | Response time under 200ms for 500 advisories | Single query with COUNT/GROUP BY; index on sbom_advisory join table |

## Step 9 -- Self-Verification

### Scope Containment
Run `git diff --name-only` and compare against Files to Modify and Files to Create. Six files expected:
- 3 modified: `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs`
- 3 created: `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs`

Flag any additional modified files for user approval. Register `tests/api/advisory_summary.rs` in `tests/api/mod.rs` or `tests/Cargo.toml` if needed -- this would be an out-of-scope file requiring approval.

### Untracked File Check
Run `git status --short`, filter `??` entries in relevant directories, cross-reference with staged diff.

### Dead Parameter Detection
Scan modified functions for parameters no longer referenced. Not expected for additive changes.

### Sensitive-Pattern Check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- no matches expected.

### Documentation Currency
If `docs/api.md` documents existing endpoints, update it with the new endpoint. Otherwise skip.

### Duplication Check
Search repository for existing severity aggregation logic -- `search_for_pattern("severity_summary")`, `search_for_pattern("severity.*count")`. Ensure no existing utility already provides this functionality.

### CI Checks from CONVENTIONS.md
Run all CI check commands extracted from `CONVENTIONS.md` (formatting, linting, compilation). Hard stop on any failure.

### Module-Level Test Requirement (Rust)
Resolve crate name via `cargo metadata --no-deps --format-version 1` for each modified file. Run `cargo test -p <crate-name>` for each affected crate. Hard stop on test failure.

### Data-Flow Trace
- **Input:** HTTP GET request with SBOM ID path parameter
- **Processing:** Path extraction -> AdvisoryService.severity_summary() -> query sbom_advisory join table -> deduplicate by advisory ID -> count by severity level
- **Output:** JSON response with `{ critical, high, medium, low, total }`
- **Error path:** SBOM not found -> AppError -> 404 response

All stages connected. Flow is complete.

### Contract and Sibling Parity
- **Contract:** `severity_summary` method follows `AdvisoryService` method patterns (same parameter types, return type)
- **Sibling parity:** Handler follows same pattern as `get.rs` (Path extraction, service call, Json response, AppError)
- **Cross-module entity:** Uses `sbom_advisory` join table read-only; no write conflicts with other modules
- **Caller-site:** Route registration follows existing pattern in `endpoints/mod.rs`

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
linked to a given SBOM. Deduplicates by advisory ID and defaults all
counts to zero when no advisories exist.

Implements TC-9201"
git push -u origin TC-9201
```

### Fork Detection
Run `git remote get-url upstream 2>/dev/null`. If upstream exists, use `-R <upstream-owner/repo> --head <fork-owner>:TC-9201`. Otherwise use default `gh pr create`.

### Create Pull Request

```bash
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint returning aggregated severity counts
- Add \`SeveritySummary\` response model with critical, high, medium, low, and total counts
- Add \`AdvisoryService::severity_summary\` method querying sbom_advisory join table with deduplication
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [ ] Verify \`GET /api/v2/sbom/{id}/advisory-summary\` returns correct severity counts for an SBOM with known advisories
- [ ] Verify 404 response for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no linked advisories
- [ ] Verify duplicate advisory links are deduplicated in the count
- [ ] Verify response time under 200ms for SBOMs with up to 500 advisories"
```

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field:** Update `customfield_10875` on TC-9201 with the PR URL in ADF format (inlineCard).

2. **Add comment to TC-9201:**
   - PR link
   - Summary: Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint with `SeveritySummary` response model, `AdvisoryService::severity_summary` method, and integration tests. No deviations from the plan.
   - Comment ends with the skill footnote per `shared/comment-footnote.md`.

3. **Transition TC-9201 to In Review:** `jira.transition_issue("TC-9201", "In Review")`
