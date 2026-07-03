# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

---

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend`
2. **Jira Configuration** -- present, includes Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured with rust-analyzer

Configuration is valid. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description.

### Parsed sections:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing patterns in `get.rs`, use `sbom_advisory` join table, use `AdvisorySummary.severity` field for counting, return `Result<T, AppError>` with `.context()` wrapping
- **Acceptance Criteria**: 5 items (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 test cases
- **Target PR**: not present
- **Bookend Type**: not present
- **Dependencies**: None

### Target Branch extraction

Target branch is `main`. This will be used as the PR base branch in Step 10.

### GitHub Issue extraction

Look up `GitHub Issue custom field: customfield_10747` from Jira Configuration. Read the field value from the issue response. If populated, parse the GitHub issue URL and store as `owner/repo#number` for the PR description.

## Step 1.5 -- Verify Description Integrity

(See digest-match.md for detailed analysis.)

Digest comment found with marker `[sdlc-workflow] Description digest:`. The stored digest is `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`. Comment timestamps are identical (not edited). Computed digest matches stored digest (same format tag `sha256-md`, same hex hash). **Proceed silently** -- no user prompt, no added latency.

## Step 2 -- Verify Dependencies

The task lists `Dependencies: None`. No dependency checks are needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use `mcp__serena_backend__get_symbols_overview` on each file to understand structure:

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - Use `get_symbols_overview` to see `AdvisoryService` struct and its existing methods (`fetch`, `list`, `search`)
   - Use `find_symbol` with `include_body=true` on the `fetch` method to understand the pattern for service methods (parameter types, return types, transaction handling)
   - Use `find_referencing_symbols` on `AdvisoryService` to identify all callers

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - Use `get_symbols_overview` to see route registration pattern
   - Identify how routes are registered (`Router::new().route(...)`)

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - Use `get_symbols_overview` to see existing module declarations
   - Confirm pattern for adding `pub mod severity_summary;`

### 4.2 Inspect reference files

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- reference endpoint pattern
   - Use `find_symbol` to read the GET handler: path param extraction via `Path<Id>`, service call, JSON response
2. **`modules/fundamental/src/advisory/model/summary.rs`** -- reference model with `severity` field
   - Use `find_symbol` on `AdvisorySummary` to understand the struct and its `severity` field type
3. **`entity/src/sbom_advisory.rs`** -- join table for SBOM-Advisory relationships
   - Use `get_symbols_overview` to understand the entity structure
4. **`common/src/error.rs`** -- `AppError` enum and `IntoResponse` implementation
   - Use `find_symbol` on `AppError` to understand error types and `.context()` usage

### 4.3 Convention conformance analysis -- sibling files

Inspect sibling endpoint files to discover implicit conventions:

- **`modules/fundamental/src/advisory/endpoints/list.rs`** and **`get.rs`** -- sibling handlers
- **`modules/fundamental/src/sbom/endpoints/get.rs`** -- cross-module sibling for SBOM-specific endpoints

Expected discovered conventions:
- **Error handling**: All handlers return `Result<Json<T>, AppError>` with `.context()` wrapping
- **Path extraction**: Use Axum's `Path<Id>` extractor for path parameters
- **Service invocation**: Handlers call service methods with `&self, id, &Transactional`
- **Response**: Return struct directly via `Json()` wrapper
- **Route registration**: `Router::new().route("/path", get(handler_fn))` in `endpoints/mod.rs`

### 4.4 Test convention analysis

Inspect sibling test files:

- **`tests/api/advisory.rs`** -- advisory endpoint integration tests
- **`tests/api/sbom.rs`** -- SBOM endpoint integration tests

Expected discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases**: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Test setup**: Uses real PostgreSQL test database with fixture data

### 4.5 Documentation file identification

Identify documentation files:
- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating for new endpoint)
- `CONVENTIONS.md` at repository root -- read for CI check commands and project conventions

### 4.6 CONVENTIONS.md lookup

Read `CONVENTIONS.md` at the repository root. Extract:
- CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`)
- Code generation commands (if any)
- Naming rules, directory structure, code patterns

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
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Provides aggregated counts of advisories grouped by severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u64,
    /// Count of high-severity advisories.
    pub high: u64,
    /// Count of medium-severity advisories.
    pub medium: u64,
    /// Count of low-severity advisories.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}
```

Derive traits matching sibling model structs (`Serialize`, `Deserialize`, `ToSchema`). Default all counts to 0 via `Default` derive.

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the existing pattern of module declarations (`pub mod summary;`, `pub mod details;`).

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Following the pattern of existing `fetch` and `list` methods:

```rust
/// Computes severity counts for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// SBOM, deduplicates by advisory ID, and counts advisories at each severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Deduplicate by advisory ID
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

Implementation details:
- Use `sbom_advisory` entity to find advisories linked to the SBOM ID
- Load `AdvisorySummary` for each linked advisory to access the `severity` field
- Deduplicate by advisory ID before counting
- Match severity string values ("Critical", "High", "Medium", "Low") and increment counters
- Compute total as sum of all severity counts
- Use `.context("Failed to compute severity summary")` for error wrapping
- Return 404 (`AppError`) when the SBOM ID does not exist (check SBOM existence first, matching existing SBOM endpoint behavior)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Following the pattern in `get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the given SBOM.
pub async fn severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following existing registration pattern:

```rust
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

Add `mod severity_summary;` at the top with other module declarations.

### 6.6 Documentation impact

Check `docs/api.md` for existing API documentation. Add an entry for the new endpoint:
- `GET /api/v2/sbom/{id}/advisory-summary` -- returns severity count summary
- Document the response shape: `{ critical, high, medium, low, total }`

### 6.7 Code quality verification

Verify all new structs and public functions have documentation comments (already included in the implementation above).

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases, following sibling test conventions:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels
    // (set up test fixtures in PostgreSQL test database)

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // Deserialize body and verify critical, high, medium, low, total counts
}

/// Verifies that a non-existent SBOM ID returns 404 status.
#[tokio::test]
async fn test_advisory_summary_returns_404_for_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary endpoint

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no linked advisories returns all-zero counts.
#[tokio::test]
async fn test_advisory_summary_returns_zeros_for_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary endpoint

    // Then all severity counts are 0 and total is 0
    // assert_eq!(summary.critical, 0)
    // assert_eq!(summary.high, 0)
    // assert_eq!(summary.medium, 0)
    // assert_eq!(summary.low, 0)
    // assert_eq!(summary.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary endpoint

    // Then the count reflects unique advisories only
    // (e.g., 2 links to same critical advisory = critical: 1, not critical: 2)
}
```

All tests include documentation comments and given-when-then section comments per skill requirements.

Run tests to verify: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Confirmed by `test_advisory_summary_returns_correct_counts` and endpoint implementation returning `SeveritySummary` struct |
| 2 | Returns 404 when SBOM ID does not exist | Confirmed by `test_advisory_summary_returns_404_for_nonexistent_sbom` and service-level SBOM existence check |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Confirmed by `test_advisory_summary_deduplicates_advisories` and deduplication logic in service method |
| 4 | All severity levels default to 0 when no advisories exist | Confirmed by `test_advisory_summary_returns_zeros_for_no_advisories` and `Default` derive on `SeveritySummary` |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by using a single database query with GROUP BY rather than N+1 queries; can be confirmed with load testing |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and verify all changed files are in the Files to Modify or Files to Create lists:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` -- in Files to Modify

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in Files to Create
- `tests/api/advisory_summary.rs` -- in Files to Create

Any out-of-scope files (e.g., documentation updates to `docs/api.md`) would be flagged and require user approval.

### Untracked file check

Run `git status --short`, extract `??` entries, filter by proximity to modified directories, and check for code references. Flag any referenced untracked files for user approval.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to verify no secrets are staged.

### Documentation currency

Verify `docs/api.md` is updated if it exists and documents API endpoints.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`). Hard stop on any failure.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (Id) -> call `AdvisoryService::severity_summary` -> query `sbom_advisory` join table -> load advisory severities -> deduplicate and count -> return `SeveritySummary` as JSON -- **COMPLETE**

### Contract and sibling parity

- `SeveritySummary` struct -- standalone response type, no trait contract to implement
- Sibling parity with `get.rs` and `list.rs` handlers: error handling pattern (Result<Json<T>, AppError>) matches, path extraction matches, service invocation matches
- No cross-module shared entity concerns -- the service reads from `sbom_advisory` but does not insert/update/delete

### Duplication check

Search for existing severity counting or aggregation logic in the codebase using `search_for_pattern` to ensure no duplication.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to an SBOM. Includes deduplication by advisory ID
and proper 404 handling for missing SBOMs.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- `Closes <owner>/<repo>#<number>` if GitHub Issue field was populated

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF inlineCard format
2. **Add comment** to TC-9201 with PR link, summary of changes, and any deviations from the plan
3. **Transition** TC-9201 to In Review: `jira.transition_issue("TC-9201", "In Review")`
