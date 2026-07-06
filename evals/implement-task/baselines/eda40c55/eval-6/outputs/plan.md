# Implementation Plan: TC-9201

## Task Summary

**Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

## Step 0 — Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** — present with Project key `TC`, Cloud ID, Feature issue type ID, and custom fields
3. **Code Intelligence** — present with `serena_backend` instance using `rust-analyzer`

All prerequisites satisfied. Proceed.

## Step 0.5 — JIRA Access Initialization

Attempt MCP first for all Jira operations. If MCP fails, prompt the user for REST API fallback per the documented protocol.

## Step 1 — Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` — returns `{ critical, high, medium, low, total }` |
| Acceptance Criteria | 5 criteria (see task description) |
| Test Requirements | 4 test cases (see task description) |
| Dependencies | None |
| Target PR | Not present (default flow) |
| Bookend Type | Not present (default flow) |

Capture the issue `webUrl` for use in the PR description.

Check for GitHub Issue custom field (`customfield_10747`) — extract if present, skip silently if empty.

## Step 1.5 — Verify Description Integrity

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate the digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890...`
3. Comment `created` equals `updated` — no edit warning needed
4. Format tag is `sha256-md` (not legacy untagged) — proceed with comparison
5. Write current description to `/tmp/desc-TC-9201.txt`, compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
6. Tags match (`sha256-md` = `sha256-md`), hex digests match — proceed silently

## Step 2 — Verify Dependencies

No dependencies listed. Skip.

## Step 3 — Transition to In Progress and Assign

1. Retrieve current user account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 — Understand the Code

### 4.1 — Inspect files to modify

Using `mcp__serena_backend__get_symbols_overview` on:

- **`modules/fundamental/src/advisory/service/advisory.rs`** — identify `AdvisoryService` struct and existing methods (`fetch`, `list`, `search`). These will serve as patterns for the new `severity_summary` method. Understand the method signature: `&self, <params>, tx: &Transactional<'_>`.
- **`modules/fundamental/src/advisory/endpoints/mod.rs`** — identify route registration pattern: `Router::new().route("/path", get(handler))`. Understand how existing routes are mounted.
- **`modules/fundamental/src/advisory/model/mod.rs`** — identify existing `pub mod` declarations (`summary`, `details`). The new `severity_summary` module will be added here.

### 4.2 — Inspect referenced code

Using `mcp__serena_backend__find_symbol` with `include_body=true` on:

- **`AdvisorySummary`** in `modules/fundamental/src/advisory/model/summary.rs` — examine the `severity` field type and possible values (Critical, High, Medium, Low).
- **`sbom_advisory`** entity in `entity/src/sbom_advisory.rs` — understand the join table structure linking SBOMs to advisories.
- **Existing endpoint handler** in `modules/fundamental/src/advisory/endpoints/get.rs` — understand the pattern for Path param extraction, service calls, and JSON response.
- **`AppError`** in `common/src/error.rs` — understand error handling with `.context()` wrapping.

### 4.3 — Convention conformance analysis

Identify sibling files for each file being modified/created:

**Service siblings** (in `advisory/service/`):
- Examine `advisory.rs` existing methods for naming, error handling, transaction usage

**Endpoint siblings** (in `advisory/endpoints/`):
- Examine `get.rs` and `list.rs` for handler signature, extractors (`Path<Id>`), return types, error wrapping

**Model siblings** (in `advisory/model/`):
- Examine `summary.rs` and `details.rs` for struct shape, derive macros (`Serialize`, `Deserialize`), field documentation

**Test siblings** (in `tests/api/`):
- Examine `advisory.rs` and `sbom.rs` for test setup, assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)`), naming conventions

**Expected discovered conventions:**
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: Service methods follow `verb_noun` pattern
- Endpoint handlers: extract `Path<Id>`, call service, return `Json(result)`
- Test naming: `test_<endpoint>_<scenario>`
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Derive macros on model structs: `#[derive(Serialize, Deserialize, Debug)]`

### 4.4 — CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root. If present, read and extract CI check commands for Step 9. If not present, proceed normally.

### 4.5 — Documentation file identification

Look for:
- `README.md` at repository root
- `docs/api.md` (API reference)
- `docs/architecture.md` (architecture overview)

Record for documentation-impact evaluation in Step 6.

## Step 5 — Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 — Implement Changes

### 6.1 — Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for advisories linked to an SBOM.
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

Key decisions:
- Derive `Default` so all counts initialize to 0 (satisfies acceptance criterion: "All severity levels default to 0")
- Use `u32` for counts (non-negative, sufficient range)
- Add doc comments on the struct and every field

### 6.2 — Register model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` alongside existing module declarations (`summary`, `details`).

### 6.3 — Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Following the existing `fetch`/`list` method pattern:

```rust
/// Aggregates advisory severity counts for a given SBOM, deduplicating by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists — return 404 if not found
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Deduplicate by advisory ID (use DISTINCT or a HashSet)
    // 4. For each unique advisory, fetch its severity from AdvisorySummary
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` entity to find advisories linked to the SBOM
- Use `AdvisorySummary.severity` field for counting
- Deduplicate by advisory ID (acceptance criterion: "Counts only unique advisories")
- Return 404 when SBOM ID does not exist (use `.context()` error wrapping pattern)

### 6.4 — Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Following the pattern in `get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the given SBOM.
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

### 6.5 — Register the new route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the route following the existing `Router::new().route()` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Import the new endpoint module at the top of the file.

### 6.6 — Documentation impact

- No Documentation Updates section in the task
- Check if `docs/api.md` documents advisory endpoints — if so, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- Keep updates lightweight and scoped

### 6.7 — Code quality verification

- Verify all new structs and public functions have documentation comments
- Verify naming follows `verb_noun` pattern discovered in convention analysis

## Step 7 — Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases, following the sibling test conventions discovered in Step 4:

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that querying an SBOM with known advisories returns correct per-severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories of known severities (Critical: 2, High: 1, Medium: 3, Low: 0)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK and the body contains correct counts
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(summary.critical, 2);
    // assert_eq!(summary.high, 1);
    // assert_eq!(summary.medium, 3);
    // assert_eq!(summary.low, 0);
    // assert_eq!(summary.total, 6);
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting a non-existent SBOM ID returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response status is 404 Not Found
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns zero counts across all severity levels.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero and total is zero
    // assert_eq!(summary.critical, 0);
    // assert_eq!(summary.high, 0);
    // assert_eq!(summary.medium, 0);
    // assert_eq!(summary.low, 0);
    // assert_eq!(summary.total, 0);
}
```

### Test 4: Duplicate advisories are deduplicated

```rust
/// Verifies that duplicate advisory links for the same advisory ID are counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the count reflects unique advisories only (not duplicated)
}
```

All tests follow discovered conventions:
- Use `assert_eq!(resp.status(), StatusCode::...)` pattern
- Follow `test_<endpoint>_<scenario>` naming
- Include doc comments on every test function
- Use given-when-then section comments for non-trivial tests
- Assert on specific values, not just collection lengths

Run `cargo test` and fix any failures before proceeding.

## Step 8 — Verify Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| 1 | `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical, high, medium, low, total }` | Test 1 validates correct response shape and values |
| 2 | Returns 404 when SBOM ID does not exist | Test 2 validates 404 response |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Test 4 validates deduplication |
| 4 | All severity levels default to 0 when no advisories exist | Test 3 validates zero defaults |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient query design (single query with COUNT/GROUP BY rather than N+1) |

## Step 9 — Self-Verification

### Scope containment

Run `git diff --name-only` and verify all changed/created files match the task scope:

**Expected files:**
- `modules/fundamental/src/advisory/service/advisory.rs` (modified)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified)
- `modules/fundamental/src/advisory/model/mod.rs` (modified)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (created)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (created)
- `tests/api/advisory_summary.rs` (created)

Flag any out-of-scope files for user approval.

### Untracked file check

Run `git status --short`, filter untracked files (`??`) by proximity to modified directories. Check for code references in new files. Flag any referenced untracked files for user approval.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` — flag any matches.

### Documentation currency

Verify `docs/api.md` (if it exists) reflects the new endpoint. Update if needed.

### Duplication check

Search repository for existing severity aggregation logic to ensure no duplication.

### CI checks from CONVENTIONS.md

Run any CI commands extracted from CONVENTIONS.md. If none found, run `cargo build` and `cargo clippy` as standard checks.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` request
  - Input: HTTP request with SBOM ID path parameter
  - Processing: Endpoint handler extracts ID, calls `AdvisoryService.severity_summary()`, which queries `sbom_advisory` join table, deduplicates, counts by severity
  - Output: JSON response with `SeveritySummary` struct
  - **COMPLETE** — all stages connected

### Contract & sibling parity

- `SeveritySummary` — standalone struct, no trait/interface to implement
- Sibling parity with `AdvisorySummary`, `AdvisoryDetails`: derive macros match, serialization pattern matches
- Endpoint handler parity with `get.rs`: extractor pattern matches, error handling matches, return type matches

## Step 10 — Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity summary aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated advisory severity counts (critical, high, medium, low, total)
for a given SBOM. Includes deduplication by advisory ID and proper 404
handling for non-existent SBOMs.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity summary aggregation endpoint" --body "..."
```

PR description includes:
- `Implements [TC-9201](<webUrl>)` with clickable Jira link
- Summary of changes
- If GitHub issue reference was extracted in Step 1, include `Closes <owner>/<repo>#<number>`

## Step 11 — Update Jira

1. Update the Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL using ADF inlineCard format
2. Add a Jira comment with:
   - PR link
   - Summary of changes made (new endpoint, service method, model, tests)
   - Any deviations from the plan
   - Comment footer with plugin version and skill attribution link
3. Transition TC-9201 to "In Review"
