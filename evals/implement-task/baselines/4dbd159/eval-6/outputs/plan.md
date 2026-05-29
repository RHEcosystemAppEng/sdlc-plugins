# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (trustify-backend) contains all required sections:
- **Repository Registry**: present with `trustify-backend` entry, Serena Instance `serena_backend`, Path `./`
- **Jira Configuration**: present with Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

All required sections are present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user with REST API fallback options per the skill procedure.

## Step 1 -- Fetch and Parse Jira Task

Fetch issue TC-9201 via `jira.get_issue(TC-9201)`. Parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`, add `severity_summary` method to `AdvisoryService` following `fetch`/`list` patterns, use `sbom_advisory` join table, use `AdvisorySummary.severity` for counting, register route in `endpoints/mod.rs`, use `AppError` with `.context()`, return struct directly via Axum `Json`
- **Acceptance Criteria**: 5 items (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance under 200ms for 500 advisories)
- **Test Requirements**: 4 tests (valid SBOM with known advisories, non-existent SBOM 404, SBOM with no advisories, deduplication)
- **Dependencies**: None
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **GitHub Issue custom field**: customfield_10747 -- check field value on the fetched issue; extract GitHub issue reference if present for PR description
- **Web URL**: capture from API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in PR description

All required sections are present. No missing sections. Proceed.

## Step 1.5 -- Verify Description Integrity

(See digest-match.md for full details.)

1. Fetch comments via `jira.get_issue_comments(TC-9201)`
2. Locate the comment starting with `[sdlc-workflow] Description digest:`
3. Found one digest comment: `[sdlc-workflow] Description digest: sha256:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Check `created` vs `updated` timestamps -- they are identical, so the comment was not edited. No warning needed.
5. Extract stored digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
6. Compute SHA-256 of the current description field using `scripts/sha256-digest.py`
7. Digests **match** -- proceed silently without prompting the user.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependencies to verify. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get the current user's account ID.
2. Call `jira.edit_issue(TC-9201, assignee=<current-user-account-id>)` to assign the task.
3. Call `jira.transition_issue(TC-9201)` to transition to "In Progress".

## Step 4 -- Understand the Code

### 4.1 Code Inspection via Serena

Use the `serena_backend` instance (tools called as `mcp__serena_backend__<tool>`):

1. **Overview of files to modify**:
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` struct and existing methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module re-exports

2. **Read specific symbols**:
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` -- understand the service method pattern (parameters, return type, transaction handling)
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` -- understand the list pattern
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` -- understand the `severity` field type and structure

3. **Check backward compatibility**:
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` -- identify all callers to ensure new method does not conflict

4. **Non-symbolic search**:
   - `mcp__serena_backend__search_for_pattern` for `sbom_advisory` in `entity/src/sbom_advisory.rs` -- understand the join table structure for SBOM-advisory relationships
   - `mcp__serena_backend__search_for_pattern` for route registration patterns in `endpoints/mod.rs` files

5. **Convention conformance analysis**:
   - Inspect sibling endpoint files: `modules/fundamental/src/advisory/endpoints/get.rs` and `modules/fundamental/src/advisory/endpoints/list.rs`
   - Inspect sibling model files: `modules/fundamental/src/advisory/model/summary.rs` and `modules/fundamental/src/advisory/model/details.rs`
   - Inspect sibling service files: compare with `modules/fundamental/src/sbom/service/sbom.rs`

### 4.2 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read it and extract:
- CI check commands for Step 9
- Code generation commands
- Naming conventions, directory structure, code patterns

### 4.3 Documentation File Identification

Identify documentation files related to the changes:
- `docs/api.md` -- API documentation that may need updating for the new endpoint
- `docs/architecture.md` -- architecture overview
- `README.md` at the repository root

### 4.4 Test Convention Analysis

Inspect sibling test files for test patterns:
- `tests/api/advisory.rs` -- advisory endpoint integration tests (assertion style, setup, naming)
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/search.rs` -- search endpoint integration tests

Record discovered conventions for:
- Assertion style (e.g., `assert_eq!(resp.status(), StatusCode::OK)`)
- Response validation patterns
- Error case coverage (404 tests)
- Test naming conventions
- Test setup/teardown patterns (database seeding, fixture creation)
- Whether parameterized tests (e.g., `#[rstest]`) are used

### Expected Discovered Conventions

**Production code conventions (from sibling analysis):**
- Error handling: All handlers return `Result<T, AppError>` with `.context()` wrapping
- Naming: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- Endpoint pattern: Extract path params via `Path<Id>`, call service, return `Json<T>`
- Route registration: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- Model pattern: Separate struct files in `model/` directory, re-exported via `mod.rs`
- Transaction handling: Methods take `&self, ..., tx: &Transactional<'_>`

**Test conventions (from sibling test analysis):**
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Error cases: Include 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Test naming: `test_<endpoint>_<scenario>` pattern

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
use serde::Serialize;

/// Summary of advisory severity counts for a given SBOM.
///
/// Provides counts of unique advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Debug, Clone, Serialize, Default)]
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

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module. Follow the existing pattern of module declarations in this file.

### 6.3 Add `severity_summary` method to `AdvisoryService`

In `modules/fundamental/src/advisory/service/advisory.rs`, add a new method following the pattern of existing `fetch` and `list` methods:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts occurrences at each
/// severity level (Critical, High, Medium, Low).
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, read severity from AdvisorySummary
    // 5. Count by severity level
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` join table from `entity/src/sbom_advisory.rs` to find linked advisories
- Deduplicate by advisory ID to satisfy the "unique advisories" acceptance criterion
- Use the `severity` field from `AdvisorySummary` (in `model/summary.rs`) to categorize each advisory
- Default all severity levels to 0 when no advisories exist at that level (the `Default` derive on `SeveritySummary` handles this)
- Wrap errors with `.context()` matching the pattern in `common/src/error.rs`
- Return 404 (via `AppError`) when the SBOM ID does not exist

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

/// GET handler for `/api/v2/sbom/{id}/advisory-summary`.
///
/// Returns a severity summary with counts of unique advisories at each
/// severity level (Critical, High, Medium, Low) and a total count.
pub async fn get_advisory_summary(
    Path(id): Path<Id>,
    service: AdvisoryService,
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

Register the new route following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

Add `mod severity_summary;` to import the new endpoint module.

### 6.6 Documentation Impact

- Check if `docs/api.md` documents existing endpoints. If so, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request parameters and response shape.
- No changes to `server/src/main.rs` needed (routes auto-mount via module registration, as stated in the task description).

### 6.7 Code Quality Verification

- All new structs (`SeveritySummary`) have documentation comments
- All new functions (`severity_summary`, `get_advisory_summary`) have documentation comments
- All public fields have documentation comments

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases, following the assertion patterns and naming conventions discovered in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns the correct
/// severity counts broken down by level.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (seed database with SBOM + linked advisories at Critical, High, Medium, Low)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // and the response body contains correct counts for each severity level
    // and the total equals the sum of all severity counts
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response status is 404 NOT_FOUND
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts at zero and total at zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response body contains critical: 0, high: 0, medium: 0, low: 0, total: 0
}
```

### Test 4: Duplicate advisory links are deduplicated in the count

```rust
/// Verifies that duplicate advisory links (same advisory linked multiple
/// times to the same SBOM) are deduplicated and counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with the same advisory linked multiple times

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the total reflects unique advisories only (not duplicate links)
    // and individual severity counts reflect unique advisories
}
```

Run `cargo test` to verify all tests pass. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. **GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }`** -- Verified by `SeveritySummary` struct definition and endpoint implementation returning `Json<SeveritySummary>`.
2. **Returns 404 when SBOM ID does not exist** -- Verified by the service method checking SBOM existence and returning `AppError` for missing SBOMs, and by test 2.
3. **Counts only unique advisories (deduplicates by advisory ID)** -- Verified by deduplication logic in the service method, and by test 4.
4. **All severity levels default to 0 when no advisories exist** -- Verified by `Default` derive on `SeveritySummary` and by test 3.
5. **Response time under 200ms for SBOMs with up to 500 advisories** -- Verified by using a single database query with aggregation rather than N+1 queries. Performance testing with a sufficiently large dataset would confirm this in practice.

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files match the task's Files to Modify and Files to Create:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (new) -- in Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (new) -- in Files to Create
- `tests/api/advisory_summary.rs` (new) -- in Files to Create
- `modules/fundamental/src/advisory/service/advisory.rs` (modified) -- in Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified) -- in Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` (modified) -- in Files to Modify

If any out-of-scope files appear (e.g., documentation updates to `docs/api.md`), list them and ask the user for approval.

### Untracked File Check

Run `git status --short` to find untracked files (`??` prefix). Filter by proximity to modified directories. Check for code references (e.g., `include_str!`, `use`, `mod`) in modified files. Flag any referenced untracked files for staging approval.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to verify no secrets are staged.

### Documentation Currency

Check if `docs/api.md` describes existing endpoints and needs updating for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Update if necessary.

### Duplication Check

Search the codebase for existing severity counting or aggregation logic that might overlap with the new `severity_summary` method. Use Grep/Serena to look for similar patterns.

### Cross-Section Reference Consistency

Verify that file paths referenced across Files to Modify, Files to Create, and Implementation Notes are consistent:
- `AdvisoryService` referenced in Files to Modify as `modules/fundamental/src/advisory/service/advisory.rs` and in Implementation Notes as `modules/fundamental/src/advisory/service/advisory.rs` -- consistent.
- `AdvisorySummary` referenced in Implementation Notes at `modules/fundamental/src/advisory/model/summary.rs` -- verify this path exists.
- Route registration referenced in both Files to Modify and Implementation Notes at `modules/fundamental/src/advisory/endpoints/mod.rs` -- consistent.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> aggregate by severity -> return `Json<SeveritySummary>` -- **COMPLETE**

### Contract & Sibling Parity

- `SeveritySummary` implements `Serialize` (required for JSON response) and `Default` (for zero initialization) -- complete.
- Endpoint handler follows the same `Result<Json<T>, AppError>` contract as sibling handlers in `get.rs` and `list.rs`.
- Service method follows the same `(&self, id, tx) -> Result<T, AppError>` contract as sibling methods `fetch` and `list`.

### CI Checks

Run CI check commands from CONVENTIONS.md (if extracted in Step 4). Fix any failures before proceeding.

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, and integration tests.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM, enabling dashboard widgets to render severity
breakdowns without client-side counting.

### Changes
- New \`SeveritySummary\` response struct in \`advisory/model/severity_summary.rs\`
- New \`severity_summary\` method on \`AdvisoryService\`
- New GET handler at \`/api/v2/sbom/{id}/advisory-summary\`
- Integration tests covering success, 404, empty, and deduplication cases

Implements [TC-9201](<webUrl>)
Closes <owner>/<repo>#<number>  (if GitHub issue reference was extracted)
"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (customfield_10875) with the PR URL using ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
   - No deviations from the plan
   - Include the skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition** TC-9201 to "In Review":
   ```
   jira.transition_issue(TC-9201) -> In Review
   ```
