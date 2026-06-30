# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` entry with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`), Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend`

Validation passes. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback per the skill definition. REST API equivalents are available via `python3 scripts/jira-client.py`.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description.

### Parsed fields:

- **Repository**: `trustify-backend`
- **Target Branch**: `main`
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Acceptance Criteria**: 5 criteria (200 response shape, 404 handling, deduplication, zero defaults, performance)
- **Test Requirements**: 4 tests (valid counts, 404, zero counts, deduplication)
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: none
- **Review Context**: not present

Capture `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for PR description.

### GitHub Issue extraction

The Jira Configuration lists `GitHub Issue custom field: customfield_10747`. Read this field from the fetched issue response. If present and non-empty, parse the GitHub issue URL to extract `owner/repo#number` for use in the PR description. If absent, skip silently.

## Step 1.5 -- Verify Description Integrity

(See `outputs/digest-match.md` for the detailed walkthrough.)

Summary: The digest comment uses format tag `sha256-md` with a 64-character hex digest. The `created` and `updated` timestamps are identical (no editing detected). The computed digest from the current description matches the stored digest. The check passes silently -- proceed to Step 2.

## Step 2 -- Verify Dependencies

The task has no dependencies listed. Skip this step.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to "In Progress" via `jira.transition_issue("TC-9201", "In Progress")`.

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`**: Use `mcp__serena_backend__get_symbols_overview` to see AdvisoryService structure. Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand the pattern for adding `severity_summary`.
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**: Use `get_symbols_overview` to see existing route registrations and understand the `Router::new().route(...)` pattern.
3. **`modules/fundamental/src/advisory/endpoints/get.rs`**: Use `find_symbol` to read the GET handler implementation -- this is the template for the new endpoint handler.
4. **`modules/fundamental/src/advisory/model/mod.rs`**: Use `get_symbols_overview` to see existing `pub mod` declarations.
5. **`modules/fundamental/src/advisory/model/summary.rs`**: Use `find_symbol` on `AdvisorySummary` to understand the `severity` field used for counting.

### 4.2 Inspect related code

6. **`entity/src/sbom_advisory.rs`**: Use `get_symbols_overview` to understand the SBOM-Advisory join table structure for the query.
7. **`common/src/error.rs`**: Use `find_symbol` on `AppError` to understand error handling patterns.

### 4.3 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure the new method does not conflict.

### 4.4 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). Per the repo structure, it exists. Read it and extract:
- CI check commands (for use in Step 9)
- Code generation commands (if any)
- Naming rules, directory structure, and code patterns

### 4.5 Convention conformance analysis

Analyze sibling files to discover implicit conventions:

**Production code siblings:**
- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- examine endpoint handler patterns
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- examine model struct patterns
- `modules/fundamental/src/sbom/endpoints/get.rs` -- examine cross-module endpoint patterns (since the new route is under `/api/v2/sbom/{id}/...`)

Expected discovered conventions:
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint pattern**: Extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Route registration**: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Model structs**: Derive `Serialize`, `Deserialize`, `Debug`, `Clone`; doc comments on each struct and field
- **Service methods**: Take `&self`, entity ID, and `tx: &Transactional<'_>` as parameters

### 4.6 Test convention analysis

Analyze sibling test files:

**Test siblings:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Expected discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: Check specific field values, not just counts
- **Error cases**: Include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: Tests use a real PostgreSQL test database with fixture data

### 4.7 Documentation file identification

Identify documentation files:
- `docs/api.md` -- REST API reference (may need updating with the new endpoint)
- `docs/architecture.md` -- system architecture overview
- `README.md` -- project readme

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for a given SBOM.
///
/// Provides counts of linked advisories grouped by severity level,
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

### 6.2 Update `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module, following the pattern of existing module declarations.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method following the existing `fetch` and `list` patterns:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Queries the sbom_advisory join table for advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a SeveritySummary with counts per severity level and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not found)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Join with advisory table to get severity field
    // 4. Deduplicate by advisory ID (using DISTINCT or grouping)
    // 5. Count by severity level
    // 6. Build and return SeveritySummary with defaults of 0
}
```

Key implementation details:
- Use `entity::sbom_advisory` join table to find advisories linked to the SBOM
- Join with advisory entity to access the `severity` field from `AdvisorySummary`
- Use `DISTINCT` on advisory ID to deduplicate
- Group by severity level and count
- Return `AppError` with `.context()` wrapping for errors
- Return 404 (via `AppError::NotFound`) when SBOM ID does not exist

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of linked advisories
/// grouped by severity level (Critical, High, Medium, Low) and a total.
pub async fn get_advisory_summary(
    Path(sbom_id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transaction context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Update `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing pattern:

```rust
pub mod severity_summary;

// In the router builder, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

### 6.6 `server/src/main.rs`

No changes needed -- routes auto-mount via module registration.

### 6.7 Code quality practices

- Every new struct (`SeveritySummary`) and public function (`severity_summary`, `get_advisory_summary`) has a documentation comment
- All new code follows `Result<T, AppError>` with `.context()` wrapping
- All new symbols match conventions from sibling analysis

### 6.8 Documentation impact

- Check if `docs/api.md` exists and documents REST endpoints. If so, add documentation for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.
- No configuration or architecture changes, so no other docs need updating.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests following sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`.

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that an SBOM with linked advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories of known severities
    // (set up test fixtures: SBOM + linked advisories with Critical, High, Medium, Low severities)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response status is 200 and counts match expected values
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, <expected>);
    assert_eq!(summary.high, <expected>);
    assert_eq!(summary.medium, <expected>);
    assert_eq!(summary.low, <expected>);
    assert_eq!(summary.total, <expected_total>);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").await;

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all severity counts are zero
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
/// Verifies that duplicate advisory links in the join table are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate links to the same advisory

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Assert that total reflects unique advisories, not duplicate links
    assert_eq!(summary.total, <unique_count>);
}
```

After writing tests, run:

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. **GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }`** -- Verified by the SeveritySummary struct definition and the endpoint handler returning `Json(summary)`. Confirmed by Test 1.
2. **Returns 404 when SBOM ID does not exist** -- Verified by the `severity_summary` service method checking SBOM existence first and returning `AppError::NotFound`. Confirmed by Test 2.
3. **Counts only unique advisories (deduplicates by advisory ID)** -- Verified by using `DISTINCT` on advisory ID in the query. Confirmed by Test 4.
4. **All severity levels default to 0 when no advisories exist** -- Verified by `SeveritySummary` deriving `Default` and the counting logic initializing all levels to 0. Confirmed by Test 3.
5. **Response time under 200ms for SBOMs with up to 500 advisories** -- Verified by using an efficient SQL query with JOIN and GROUP BY rather than N+1 queries. Performance test with representative data volume would confirm.

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create. Expected modified/created files:

- `modules/fundamental/src/advisory/model/severity_summary.rs` (create) -- in scope
- `modules/fundamental/src/advisory/model/mod.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/service/advisory.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create) -- in scope
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify) -- in scope
- `tests/api/advisory_summary.rs` (create) -- in scope

If `docs/api.md` was updated (from Step 6.8 Documentation impact), flag as out-of-scope and request user approval before committing.

### Untracked file check

Run `git status --short`, filter `??` entries, check for proximity to modified directories, search for code references.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to verify no secrets are being committed.

### Documentation currency

Verify `docs/api.md` reflects the new endpoint if it documents REST endpoints.

### Documentation scope preservation

If documentation was modified, verify no use cases were inadvertently narrowed.

### Eval coverage currency

No SKILL.md files are being modified, so this sub-step is skipped.

### Example consistency

If documentation with composite examples was written, cross-check narrative vs data structures.

### Cross-section reference consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` -- referenced in Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent.
- Route registration -- referenced in Files to Modify (`advisory/endpoints/mod.rs`) and Implementation Notes (`advisory/endpoints/mod.rs`) -- consistent.
- `AdvisorySummary` with `severity` field -- referenced in Implementation Notes at `advisory/model/summary.rs` -- consistent with repo structure.

### Duplication check

Search for existing severity aggregation logic in the codebase to ensure no duplication.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md during Step 4.4. Hard stop on any failure.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `sbom_id` from path (input) -> call `AdvisoryService::severity_summary` (processing) -> query `sbom_advisory` join table, join with advisory, deduplicate, count by severity (processing) -> return `Json(SeveritySummary)` (output) -- **COMPLETE**

### Contract and sibling parity

- `SeveritySummary` -- standalone struct, no trait/interface contract to verify
- Sibling parity with `AdvisorySummary`, `AdvisoryDetails`: all derive same traits, use same serialization pattern
- `get_advisory_summary` handler follows same pattern as `get.rs` handler: `Path<Id>` extraction, service call, `Json` response, `AppError` return
- Caller-site parity: new handler calls `AdvisoryService` following same patterns as existing endpoint handlers

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add a new GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, endpoint handler, and integration tests.

Implements TC-9201"
```

Then push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add a service method and REST endpoint that aggregates advisory severity counts
for a given SBOM, returning counts per severity level (Critical, High, Medium, Low)
and a total.

- Add SeveritySummary response struct
- Add severity_summary method to AdvisoryService
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Add integration tests for the new endpoint

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

<Closes owner/repo#N if GitHub Issue field was present>"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add Jira comment** with PR link, summary of changes, and any deviations. The comment includes the required sdlc-workflow footer with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.

3. **Transition TC-9201 to "In Review"** via `jira.transition_issue("TC-9201", "In Review")`.
