# Implementation Plan: TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Jira URL**: https://redhat.atlassian.net/browse/TC-9201

---

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`), plus custom fields for Git Pull Request (`customfield_10875`) and GitHub Issue (`customfield_10747`)
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured with `rust-analyzer`

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add service method and REST endpoint for advisory severity aggregation per SBOM |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs`, `server/src/main.rs` (no changes) |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Acceptance Criteria | 5 criteria (severity counts response, 404 for missing SBOM, deduplication, zero defaults, performance) |
| Test Requirements | 4 tests (valid counts, 404, all zeros, deduplication) |
| Dependencies | None |
| Target PR | Not present |
| Bookend Type | Not present |
| Review Context | Not present |

Capture the issue `webUrl` for PR description linking.

Check the GitHub Issue custom field (`customfield_10747`) on the fetched issue. If it contains a URL, parse it to `<owner>/<repo>#<number>` for the PR description's `Closes` line. If empty, skip silently.

## Step 1.5 -- Verify Description Integrity

Fetch comments via `jira.get_issue_comments("TC-9201")`. Locate the comment matching the marker `[sdlc-workflow] Description digest:`. One digest comment found with body: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.

- Comment `created` and `updated` timestamps are identical -- comment was not edited
- Format tag: `sha256-md` (markdown format)
- No legacy format issue

Compute digest of the current description using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`. Output: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.

Tags match (`sha256-md` == `sha256-md`). Hex digests match. Description is unmodified. Proceed silently -- no user prompt, no delay.

## Step 2 -- Verify Dependencies

No dependencies listed. Skip.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID via `jira.user_info()`
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use `mcp__serena_backend__get_symbols_overview` on:

- `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` structure, existing methods (`fetch`, `list`, `search`), method signatures, parameter types
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern, how existing routes are mounted
- `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration pattern for model submodules

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:

- `AdvisoryService::fetch` -- understand the method pattern (parameters, return type, transaction usage)
- `AdvisoryService::list` -- understand list query pattern
- Route registration in `endpoints/mod.rs` -- understand `Router::new().route()` pattern

### 4.2 Inspect reference files

Use `mcp__serena_backend__get_symbols_overview` on:

- `modules/fundamental/src/advisory/endpoints/get.rs` -- understand endpoint handler pattern (path extraction, service call, JSON response)
- `modules/fundamental/src/advisory/model/summary.rs` -- understand `AdvisorySummary` struct, especially the `severity` field
- `entity/src/sbom_advisory.rs` -- understand the join table structure for SBOM-to-advisory linking
- `common/src/error.rs` -- understand `AppError` enum and `.context()` usage

### 4.3 Inspect sibling files for convention conformance

Use `mcp__serena_backend__get_symbols_overview` on 2-3 sibling files:

- `modules/fundamental/src/sbom/endpoints/get.rs` -- sibling endpoint handler
- `modules/fundamental/src/sbom/service/sbom.rs` -- sibling service (`SbomService`)
- `modules/fundamental/src/sbom/model/summary.rs` -- sibling model struct

### 4.4 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). Per the repo structure, it exists. Read it and extract:

- Naming rules, directory structure conventions
- CI check commands (from a "CI checks" section, if present)
- Code generation commands (if any)

Record extracted verification commands for use in Step 9.

### 4.5 Convention conformance analysis

Record discovered conventions from sibling analysis:

**Expected discovered conventions:**

- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` for wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern**: Path params via `Path<Id>`, call service method, return `Json<T>`
- **Route registration**: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Response types**: List endpoints use `PaginatedResults<T>`; single-item endpoints return the struct directly
- **Module registration**: Model submodules registered via `pub mod <name>;` in `model/mod.rs`
- **Transaction pattern**: Service methods take `&self, id: Id, tx: &Transactional<'_>`

### 4.6 Test convention analysis

Inspect sibling test files:

- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

**Expected discovered test conventions:**

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: Endpoint tests validate response body fields directly
- **Error cases**: Tests include 404 checks with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern
- **Setup**: Tests use a real PostgreSQL test database with fixture data

### 4.7 Documentation file identification

Identify documentation files for potential updates:

- `docs/api.md` -- REST API reference (may need update for new endpoint)
- `docs/architecture.md` -- system architecture (unlikely to need changes)
- `README.md` -- project readme

## Step 5 -- Create Branch

No Target PR, no Bookend Type -- use default flow:

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

/// Summary of advisory severity counts for an SBOM, grouped by severity level.
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u64,
    /// Count of advisories with High severity.
    pub high: u64,
    /// Count of advisories with Medium severity.
    pub medium: u64,
    /// Count of advisories with Low severity.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}

impl Default for SeveritySummary {
    fn default() -> Self {
        Self {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        }
    }
}
```

### 6.2 Register model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method following the existing `fetch`/`list` pattern:

- Signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Query the `sbom_advisory` join table for advisories linked to the given SBOM ID
- Join with the advisory table to get severity information
- Use `AdvisorySummary`'s `severity` field to categorize each advisory
- Deduplicate by advisory ID (use `DISTINCT` or `GROUP BY` in the query)
- Count occurrences per severity level (Critical, High, Medium, Low)
- Return `SeveritySummary` with counts and total
- Return 404 via `AppError` with `.context()` if SBOM ID does not exist (check SBOM existence first)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Implement the GET handler following the pattern in `endpoints/get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity count summary for all advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the new route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the route registration following the existing pattern:

```rust
mod severity_summary;

// In the router function, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation impact

Check `docs/api.md` -- if it documents REST endpoints, add an entry for `GET /api/v2/sbom/{id}/advisory-summary` with the request/response schema.

### 6.7 Code quality verification

Verify:
- All new public structs and functions have documentation comments (`///`)
- Error handling uses `AppError` with `.context()` wrapping
- Response struct derives `Serialize`, `Deserialize`, `ToSchema`

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following tests, following sibling test conventions (assertion style, naming, setup patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs`):

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that querying advisory summary for an SBOM with known advisories
/// returns the correct count per severity level.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories of known severities seeded in the database
    // (e.g., 2 Critical, 3 High, 1 Medium, 0 Low)

    // When requesting the advisory summary endpoint
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response status is 200 and counts match
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary endpoint
    let resp = client.get("/api/v2/sbom/nonexistent-id/advisory-summary").await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts set to zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM that exists but has no linked advisories

    // When requesting the advisory summary endpoint
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate SBOM-advisory links are deduplicated so each
/// advisory is counted only once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM linked to the same advisory multiple times in the join table

    // When requesting the advisory summary endpoint
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, 1); // not 2+ despite duplicate links
}
```

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Verified by test 1 -- response contains `critical`, `high`, `medium`, `low`, `total` fields |
| 2 | Returns 404 for non-existent SBOM ID | Verified by test 2 |
| 3 | Counts only unique advisories | Verified by test 4 -- deduplication via DISTINCT/GROUP BY in query |
| 4 | Severity levels default to 0 | Verified by test 3 -- SBOM with no advisories returns all zeros |
| 5 | Response time under 200ms for 500 advisories | Verified by efficient SQL query with JOIN and GROUP BY rather than client-side iteration |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create. Expected modified/created files:

- `modules/fundamental/src/advisory/model/severity_summary.rs` (create) -- in scope
- `modules/fundamental/src/advisory/model/mod.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/service/advisory.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create) -- in scope
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify) -- in scope
- `tests/api/advisory_summary.rs` (create) -- in scope

If `docs/api.md` was updated, flag as out-of-scope and ask user for approval.

### Untracked file check

Run `git status --short`, check for `??` entries in directories where implementation work occurred. Flag any referenced untracked files for user confirmation.

### Dead parameter detection

Review `git diff` for any functions where removed lines contained the only reference to a parameter. Not expected for this task (additive changes only).

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`. No secrets expected.

### Documentation currency

If `docs/api.md` describes existing endpoints and the new endpoint was not added in Step 6, update it now.

### Duplication check

Search for existing severity aggregation or count-by-severity logic in the codebase. Ensure the new `severity_summary` method does not duplicate existing functionality.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on any non-zero exit.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> join advisory table -> group by severity -> return `SeveritySummary` -> serialize to JSON response -- **COMPLETE**

### Contract and sibling parity

- **Contract verification**: `SeveritySummary` has no trait to implement beyond `Serialize`/`Deserialize`/`ToSchema` -- all derived. Handler returns `Result<Json<SeveritySummary>, AppError>` matching the Axum handler contract.
- **Sibling parity**: Compare against `get.rs` endpoint handler -- both use `Path<Id>` extraction, `State<Service>`, `Transactional`, and return `Result<Json<T>, AppError>`. Pattern is consistent.
- **Cross-module shared entity**: The `sbom_advisory` join table is also used by the ingestor module. Verify that the read query pattern (SELECT with JOIN) is consistent with how other modules query this table.

## Step 10 -- Commit and Push

Commit with Conventional Commits format:

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"
```

Check for fork (upstream remote). Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint returning severity counts per SBOM
- Add \`SeveritySummary\` response model with critical/high/medium/low/total fields
- Add \`AdvisoryService::severity_summary\` method with deduplication
- Add integration tests covering valid counts, 404, empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF `inlineCard` format
2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added advisory severity aggregation endpoint (`GET /api/v2/sbom/{id}/advisory-summary`) with `SeveritySummary` model, `AdvisoryService::severity_summary` method, and integration tests
   - No deviations from the plan
   - Comment ends with the skill footnote (horizontal rule + "This comment was AI-generated by sdlc-workflow/implement-task v{version}.")
3. **Transition** TC-9201 to **In Review**
