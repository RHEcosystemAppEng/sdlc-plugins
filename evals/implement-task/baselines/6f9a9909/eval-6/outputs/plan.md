# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.

## Pre-Implementation Steps

### Step 0 -- Validate Project Configuration

Read the project CLAUDE.md (trustify-backend) and confirm:
- Repository Registry: contains `trustify-backend` with Serena instance `serena_backend` and path `./`
- Jira Configuration: contains Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: configured with `serena_backend` instance using `rust-analyzer`

All sections present -- proceed.

### Step 0.5 -- Jira Access Initialization

Attempt MCP-based Jira access. Fall back to REST API if MCP fails.

### Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`.

**Parsed sections:**

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add service method and REST endpoint for advisory severity aggregation per SBOM
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed (auto-mount)
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Acceptance Criteria:** 5 criteria (correct response shape, 404 on missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements:** 4 tests (correct counts, 404, empty SBOM, deduplication)
- **Dependencies:** None
- **Target PR:** Not present (standard flow)
- **Bookend Type:** Not present (standard flow)

Capture `webUrl` for PR description linking (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

**GitHub Issue extraction:** Check Jira Configuration for `GitHub Issue custom field: customfield_10747`. Read the field value from the issue. If present, parse and store the reference; if empty, skip.

### Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for full analysis. In this scenario:
1. Retrieve comments on TC-9201
2. Locate the single digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890...`
3. Comment timestamps are identical -- not edited, no warning
4. Format tag is `sha256-md` (not legacy) -- no warning
5. Compute current digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
6. Tags match (both `md`), hex digests match -- proceed silently

### Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

### Step 3 -- Transition to In Progress and Assign

1. Retrieve current user: `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201", "In Progress")`

## Code Understanding Phase

### Step 4 -- Understand the Code

#### 4.1 Inspect existing files using Serena (`serena_backend`)

**Files to Modify:**

1. `modules/fundamental/src/advisory/service/advisory.rs`
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService structure
   - `mcp__serena_backend__find_symbol("AdvisoryService", include_body=true)` to read `fetch` and `list` methods as patterns
   - Understand method signatures: `(&self, sbom_id: Id, tx: &Transactional<'_>)` pattern

2. `modules/fundamental/src/advisory/endpoints/mod.rs`
   - `mcp__serena_backend__get_symbols_overview` to see current route registrations
   - Identify the `Router::new().route(...)` pattern

3. `modules/fundamental/src/advisory/model/mod.rs`
   - `mcp__serena_backend__get_symbols_overview` to see current module declarations
   - Identify the `pub mod ...;` pattern for adding `severity_summary`

**Pattern reference files (siblings):**

4. `modules/fundamental/src/advisory/endpoints/get.rs` -- reference for endpoint handler pattern
   - `mcp__serena_backend__find_symbol` for the GET handler function
   - Note: `Path<Id>` extraction, service call, JSON response

5. `modules/fundamental/src/advisory/model/summary.rs` -- reference for `AdvisorySummary` struct and its `severity` field
   - `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to understand the severity field type

6. `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table
   - `mcp__serena_backend__get_symbols_overview` to understand the join entity

7. `common/src/error.rs` -- AppError pattern
   - `mcp__serena_backend__find_symbol("AppError", include_body=true)` for error handling

**Backward compatibility check:**
- `mcp__serena_backend__find_referencing_symbols` on any existing symbols being modified (e.g., route registration in endpoints/mod.rs)

#### 4.2 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). Per the repo structure file, `CONVENTIONS.md` exists at the root. Read it and extract:
- CI check commands (formatting, linting, compilation)
- Code generation commands
- Naming and structure conventions

#### 4.3 Convention conformance analysis

Analyze siblings for recurring patterns:

- **Naming:** `verb_noun` for methods (e.g., `fetch`, `list`, `search` in AdvisoryService)
- **Error handling:** `Result<T, AppError>` with `.context()` wrapping
- **Endpoint pattern:** `Path<Id>` extraction, call service method, return `Json(result)`
- **Route registration:** `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Response types:** List endpoints use `PaginatedResults<T>`; single-item endpoints return struct directly
- **Test assertions:** `assert_eq!(resp.status(), StatusCode::OK)` pattern

#### 4.4 Documentation file identification

- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating for new endpoint)
- `docs/architecture.md` -- system architecture overview

## Implementation Phase

### Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6 -- Implement Changes

#### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file -- SeveritySummary response struct:

```rust
use serde::Serialize;

/// Summary of advisory severity counts for an SBOM.
///
/// Provides aggregated counts of advisories grouped by severity level,
/// enabling dashboard widgets to render severity breakdowns.
#[derive(Debug, Clone, Serialize, Default)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u32,
    /// Count of high-severity advisories.
    pub high: u32,
    /// Count of medium-severity advisories.
    pub medium: u32,
    /// Count of low-severity advisories.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

Follow sibling pattern from `model/summary.rs` and `model/details.rs` for struct conventions.

#### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:

```rust
pub mod severity_summary;
```

Following the existing pattern of `pub mod summary;` and `pub mod details;` declarations.

#### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService`:

```rust
/// Computes aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts each severity level. Returns a `SeveritySummary`
/// with per-level counts and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Fetch AdvisorySummary for each linked advisory (deduplicate by advisory ID)
    // 4. Count by severity level using the `severity` field on AdvisorySummary
    // 5. Return SeveritySummary with counts and total
}
```

Follow the method signature pattern from existing `fetch` and `list` methods. Use `.context("severity summary")` for error wrapping.

Key implementation details:
- Use `sbom_advisory` entity from `entity/src/sbom_advisory.rs` to find linked advisories
- Deduplicate by advisory ID before counting (acceptance criterion)
- Default all severity levels to 0 (struct derives Default)
- Use the `severity` field from `AdvisorySummary` for classification

#### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler:

```rust
use axum::extract::Path;
use axum::Json;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transactional context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the pattern from `endpoints/get.rs` for parameter extraction and error handling.

#### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route:

```rust
use severity_summary::get_severity_summary;

// In the Router builder, add:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

Follow the existing `Router::new().route(...)` pattern from sibling registrations.

#### 6.6 Documentation impact

- Check whether `docs/api.md` lists REST endpoints. If so, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response documentation.
- No task-level Documentation Updates section is present, so evaluate based on code changes.

### Step 7 -- Write Tests

#### Create `tests/api/advisory_summary.rs`

Four integration tests per Test Requirements. Follow sibling test patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs`.

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories of known severity levels
    // (setup: create SBOM, link advisories with Critical=2, High=1, Medium=3, Low=0)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains the correct counts
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, 2)
    // assert_eq!(body.high, 1)
    // assert_eq!(body.medium, 3)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 6)
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_returns_404_for_missing_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_returns_zeros_for_empty_sbom() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then each advisory is counted only once
    // assert_eq!(body.total, expected_unique_count)
}
```

All tests use value-based assertions (not `.any()` or length-only checks) per skill guidance. Each test has a doc comment and given-when-then structure.

Register the test module in `tests/api/mod.rs` or `tests/Cargo.toml` as needed.

Run tests:

```bash
cargo test -p <crate-name-for-tests>
```

Fix any failures before proceeding.

### Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by `test_advisory_summary_returns_correct_counts` + manual endpoint inspection |
| 2 | Returns 404 when SBOM ID does not exist | Verified by `test_advisory_summary_returns_404_for_missing_sbom` |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_advisory_summary_deduplicates_advisories` |
| 4 | All severity levels default to 0 when no advisories exist | Verified by `test_advisory_summary_returns_zeros_for_empty_sbom` |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient query design (single join query with GROUP BY, no N+1) |

### Step 9 -- Self-Verification

#### Scope containment

Run `git diff --name-only` and compare against:

**Files to Modify:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Any files outside this list require user approval. Possible expected additions: `tests/api/mod.rs` (if test module registration is needed) -- flag for approval.

Note: `server/src/main.rs` is listed as "no changes needed" so it should NOT appear in the diff.

#### Untracked file check

Run `git status --short`, filter `??` entries near modified directories. Flag any referenced untracked files for user approval.

#### Dead parameter detection

Scan modified functions for parameters no longer referenced in function bodies. In this case, we are adding new methods rather than modifying existing ones, so dead parameters are unlikely.

#### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

#### Documentation currency

If `docs/api.md` describes endpoints and was not updated in Step 6, update it now with the new endpoint.

#### Documentation scope preservation

Not applicable -- no documentation sections are being replaced.

#### CI checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md`:
- `cargo fmt --check` (formatting)
- `cargo clippy` (linting)
- `cargo check` (compilation)
- Any other CI commands found

Hard stop on any non-zero exit.

#### Module-level test requirement (Rust)

Run `cargo metadata --no-deps --format-version 1` to resolve crate names for modified files. Run:

```bash
cargo test -p <fundamental-crate-name>
```

Hard stop on failure.

#### Data-flow trace

Trace the new feature's data flow:
1. **Input:** HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter
2. **Processing:** Axum extracts `Path<Id>` -> `severity_summary` service method queries `sbom_advisory` join table -> fetches linked advisories -> deduplicates by advisory ID -> counts by severity level
3. **Output:** `Json<SeveritySummary>` response with `{ critical, high, medium, low, total }`

All stages connected. No incomplete paths.

#### Query-scope verification

The batch query targets advisories linked to a specific SBOM via `sbom_advisory` join table. The query is already scoped by `sbom_id` -- no over-broad query concern.

#### Contract and sibling parity

- **Contract:** `SeveritySummary` implements `Serialize` (required for Axum JSON response). Handler returns `Result<Json<SeveritySummary>, AppError>` matching the endpoint contract.
- **Sibling parity:** Compare with existing `get.rs` endpoint handler -- confirm same error handling, same response pattern, same parameter extraction.
- **Cross-module entity:** `sbom_advisory` entity -- verify our read-only queries are consistent with how other modules interact with this table.
- **Caller-site:** No shared abstractions being consumed beyond standard patterns.

### Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Plus any other approved files (test module registration, docs)

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService.severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated advisory severity counts (critical, high, medium, low, total)
for a given SBOM. Includes integration tests for correct counts, 404
handling, empty SBOM, and deduplication.

Implements TC-9201"
```

#### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If no upstream remote, use default `gh pr create`:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add advisory severity aggregation service method and REST endpoint for SBOMs.

- Add \`SeveritySummary\` response struct with per-severity-level counts
- Add \`AdvisoryService::severity_summary()\` method using sbom_advisory join table
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint
- Add integration tests for correct counts, 404, empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If fork detected, add `-R <upstream-owner/repo> --head <fork-owner>:TC-9201`.

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

### Step 11 -- Update Jira

1. **Set PR custom field:** Update `customfield_10875` on TC-9201 with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment:** Post a comment to TC-9201 with:
   - PR link
   - Summary: Added SeveritySummary model, severity_summary service method, GET endpoint at /api/v2/sbom/{id}/advisory-summary, and 4 integration tests
   - No deviations from the plan
   - Comment ends with the footnote from `shared/comment-footnote.md` using skill name `implement-task`

3. **Transition to In Review:** `jira.transition_issue("TC-9201", "In Review")`
