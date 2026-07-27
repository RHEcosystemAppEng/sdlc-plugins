# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main

---

## Step 0 -- Validate Project Configuration

Verify that the project's CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key `TC`, Cloud ID, Feature issue type ID `10142`
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured with rust-analyzer

All sections validated. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all Jira operations. If MCP fails, prompt user for REST API fallback.

## Step 1 -- Fetch and Parse Jira Task

Fetch `TC-9201` via `jira.get_issue(TC-9201)`.

Parsed sections:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, returning counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing endpoint pattern, use `sbom_advisory` join table, count by severity level, return `AppError` with `.context()` wrapping
- **Acceptance Criteria**: 5 items covering correct response shape, 404 handling, deduplication, zero defaults, and performance
- **Test Requirements**: 4 test cases covering valid counts, 404, empty SBOM, and deduplication
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: none
- **Linked Issues**: is incorporated by TC-9001

Capture the issue `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for PR description.

Check `GitHub Issue custom field: customfield_10747` from Jira Configuration. If populated, parse the GitHub issue reference for use in the PR description `Closes` line.

## Step 1.5 -- Verify Description Integrity

See `digest-match.md` for full details. Summary:

1. Fetch comments via `jira.get_issue_comments(TC-9201)`.
2. Locate the single comment matching marker `[sdlc-workflow] Description digest:`.
3. Confirm the comment's `created` and `updated` timestamps are identical -- comment was not edited.
4. Extract stored digest: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
5. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`.
6. Format tags match (`sha256-md`). Hex digests match.
7. **Result**: proceed silently. No user prompt, no latency added.

## Step 2 -- Verify Dependencies

The task lists `Dependencies: None`. No dependency checks required. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue(TC-9201, assignee=<accountId>)`.
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`.

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using `mcp__serena_backend__<tool>`:

- `get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService structure, find `fetch` and `list` methods as patterns for the new `severity_summary` method.
- `get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern.
- `get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- see existing module declarations.

### 4.2 Inspect Pattern References

- `find_symbol` with `include_body=true` on `AdvisoryService::fetch` and `AdvisoryService::list` in `advisory.rs` -- learn the method signature pattern (`&self, id: Id, tx: &Transactional<'_>`).
- `get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand the endpoint handler pattern (path extraction, service call, JSON response).
- `find_symbol` on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` -- inspect the `severity` field for counting.
- `get_symbols_overview` on `entity/src/sbom_advisory.rs` -- understand the join table structure for SBOM-advisory relationships.
- `get_symbols_overview` on `common/src/error.rs` -- verify `AppError` patterns for error handling.

### 4.3 Convention Conformance Analysis

Identify sibling files:

- **Endpoint siblings**: `endpoints/get.rs`, `endpoints/list.rs` -- examine for route handler patterns, parameter extraction, response types.
- **Model siblings**: `model/summary.rs`, `model/details.rs` -- examine for struct definition patterns, derive macros, serialization annotations.
- **Service siblings**: the existing methods in `service/advisory.rs` -- examine for query building, transaction handling, error wrapping.

Expected discovered conventions:
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Naming**: Service methods use `verb_noun` pattern.
- **Route registration**: `Router::new().route("/path", get(handler))` pattern.
- **Response types**: Structs derive `Serialize` and are returned via Axum's `Json` extractor.

### 4.4 Test Convention Analysis

Inspect sibling test files:
- `tests/api/advisory.rs` -- examine assertion patterns, response validation, error case coverage.
- `tests/api/sbom.rs` -- examine test setup, database seeding patterns.

Expected discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- **Error cases**: Tests include 404 checks with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Test naming**: `test_<endpoint>_<scenario>` pattern.

### 4.5 Documentation File Identification

Look for:
- `docs/api.md` (referenced in CLAUDE.md)
- `README.md` at repository root
- `CONVENTIONS.md` at repository root (if present, extract CI check commands)

### 4.6 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root. If present, read and extract:
- Naming rules, directory structure conventions
- CI check commands for Step 9

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
use serde::Serialize;

/// Summary of advisory severity counts for a given SBOM.
///
/// Provides counts per severity level (Critical, High, Medium, Low) and a total,
/// enabling dashboard widgets to render severity breakdowns without client-side counting.
#[derive(Debug, Clone, Serialize)]
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

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module declaration:

```rust
pub mod severity_summary;
```

### 6.3 Add `severity_summary` Method to AdvisoryService

In `modules/fundamental/src/advisory/service/advisory.rs`, add a new method following the `fetch`/`list` pattern:

```rust
/// Computes an advisory severity summary for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Join with advisory table to get severity information
    // Deduplicate by advisory ID
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find linked advisories.
- Join with advisory data to access the `severity` field from `AdvisorySummary`.
- Deduplicate by advisory ID before counting (acceptance criterion).
- Default all severity counts to 0 when no advisories exist at that level.
- Wrap errors with `.context()` following the `AppError` pattern in `common/src/error.rs`.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns an advisory severity summary for the specified SBOM, with counts
/// per severity level and a total.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transactional context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

- Extract path params via `Path<Id>` (matching existing pattern).
- Call `AdvisoryService::severity_summary`.
- Return 404 when SBOM ID does not exist (consistent with existing SBOM endpoints).
- Return the struct directly via `Json` extractor.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation Impact

Check whether `docs/api.md` needs updating to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. If so, add the endpoint documentation with request/response format.

### 6.7 Code Quality Verification

Ensure all new structs and public functions have documentation comments:
- `SeveritySummary` struct and its fields
- `severity_summary` service method
- `get_severity_summary` endpoint handler

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases, following the conventions discovered in sibling test files:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response contains correct counts per severity level and total
}

/// Verifies that a non-existent SBOM ID returns a 404 status.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response status is 404 NOT_FOUND
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response contains all zeros: critical=0, high=0, medium=0, low=0, total=0
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory ID linked multiple times)
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then each advisory is counted only once in the severity totals
}
```

Each test follows the project's patterns:
- Uses `assert_eq!(resp.status(), StatusCode::OK)` or `StatusCode::NOT_FOUND`
- Deserializes the response body and validates specific field values
- Uses doc comments explaining what each test verifies
- Uses given-when-then section comments for non-trivial tests

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

Walk through each acceptance criterion:

1. `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by `test_advisory_summary_valid_sbom`
2. Returns 404 when SBOM ID does not exist -- verified by `test_advisory_summary_not_found`
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by `test_advisory_summary_deduplication`
4. All severity levels default to 0 when no advisories exist -- verified by `test_advisory_summary_empty`
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by query design using indexed join table; performance test can be added if needed

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files match the task specification:
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)

Flag any out-of-scope files for user approval.

### Untracked File Check

Run `git status --short`, extract `??` entries, filter by proximity to implementation directories, and check for code references. Flag any referenced untracked files.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to detect any secrets.

### Documentation Currency

Verify that `docs/api.md` reflects the new endpoint if it was not already updated in Step 6.

### Cross-Section Reference Consistency

Verify file paths are consistent across all sections of the task description. In particular, note that the task references `AdvisoryService` in both "Files to Modify" (`modules/fundamental/src/advisory/service/advisory.rs`) and "Implementation Notes" (same path) -- these are consistent.

### Duplication Check

Search for existing severity aggregation or counting logic in the repository to ensure no duplication.

### CI Checks from CONVENTIONS.md

Run any CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on any failure.

### Data-Flow Trace

Trace the complete data flow:
- **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter
- **Processing**: Endpoint handler extracts ID, calls `AdvisoryService::severity_summary`, which queries `sbom_advisory` join table, joins with advisory data, deduplicates, counts by severity
- **Output**: JSON response with `SeveritySummary` struct containing severity counts and total

All stages connected -- COMPLETE.

### Contract and Sibling Parity

- Verify `get_severity_summary` handler follows the same `Result<Json<T>, AppError>` return type as sibling handlers.
- Verify `severity_summary` service method follows the same signature pattern as `fetch` and `list`.
- Verify error handling uses `.context()` wrapping consistently with siblings.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService::severity_summary method,
and integration tests.

Implements TC-9201"
```

Detect fork by checking for `upstream` remote. Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- `Closes <owner>/<repo>#<number>` if a GitHub issue reference was extracted

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format.
2. Add a Jira comment summarizing changes made, linking to the PR, noting any deviations (if any). Include the skill footnote with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.
3. Transition TC-9201 to "In Review".
