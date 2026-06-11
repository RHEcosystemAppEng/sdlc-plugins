# Implementation Plan -- TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Jira Issue**: TC-9201
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001 (linked via "is incorporated by")
**Dependencies**: None

## Step 0 -- Validate Project Configuration

Project Configuration in CLAUDE.md verified:

- **Repository Registry**: Present. `trustify-backend` mapped to Serena instance `serena_backend` at path `./`.
- **Jira Configuration**: Present. Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`) all configured.
- **Code Intelligence**: Present. Tool naming convention documented. `serena_backend` instance configured with `rust-analyzer`.

All required sections are present. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description from TC-9201:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total. |
| Files to Modify | 3 files (see below) |
| Files to Create | 3 files (see below) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Implementation Notes | Follow existing endpoint pattern, AdvisoryService method pattern, sbom_advisory join table, severity field usage, route registration, error handling, response type |
| Acceptance Criteria | 5 criteria (see below) |
| Test Requirements | 4 test cases (see below) |
| Target PR | Not present (standard flow) |
| Bookend Type | Not present (standard flow) |
| Dependencies | None |

**Files to Modify:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
- `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module

**Files to Create:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
- `tests/api/advisory_summary.rs` -- integration tests for the new endpoint

**Issue webUrl**: Captured for PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

**GitHub Issue custom field** (`customfield_10747`): Check the field value on the fetched issue. If a GitHub issue URL is present, extract `owner/repo#number` for the PR description's `Closes` line. If empty, skip silently.

## Step 1.5 -- Verify Description Integrity

See `digest-match.md` for full details. Summary: Digest comment found, format tags match (`sha256-md`), hex hashes match, comment was not edited. Description integrity verified. Proceeding silently.

## Step 2 -- Verify Dependencies

The task lists "Dependencies: None". No dependency checks required. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`.
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`.

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Using Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its methods (`fetch`, `list`, `search`).
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand the method signature pattern (`&self, id: Id, tx: &Transactional<'_>`) and return type pattern.
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method to confirm the query pattern using SeaORM.

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern.
   - Inspect how routes are registered (`Router::new().route("/path", get(handler))`).

3. **`modules/fundamental/src/advisory/model/mod.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see existing module declarations (`pub mod summary;`, `pub mod details;`).

4. **`modules/fundamental/src/advisory/model/summary.rs`** (referenced in Implementation Notes):
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` with `include_body=true` to understand the `severity` field type and structure.

5. **`entity/src/sbom_advisory.rs`** (referenced in Implementation Notes):
   - `mcp__serena_backend__get_symbols_overview` to understand the join table entity structure and available columns.

6. **`modules/fundamental/src/advisory/endpoints/get.rs`** (referenced as pattern to follow):
   - `mcp__serena_backend__get_symbols_overview` to see the handler function signature.
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the handler to understand `Path<Id>` extraction, service call, and JSON response pattern.

7. **`common/src/error.rs`** (referenced for error handling):
   - `mcp__serena_backend__find_symbol` on `AppError` to understand the error enum and `.context()` wrapping pattern.

### 4.2 Check backward compatibility

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers. The new `severity_summary` method is additive -- it does not modify existing methods, so no callers are affected.
- `mcp__serena_backend__find_referencing_symbols` on the advisory endpoints module to confirm how routes are mounted.

### 4.3 Convention conformance analysis (sibling inspection)

**Sibling files for endpoint handlers** (in `modules/fundamental/src/advisory/endpoints/`):
- `get.rs` and `list.rs` -- inspect with `get_symbols_overview` to identify:
  - Handler function signatures
  - Path parameter extraction pattern
  - Service invocation pattern
  - Response wrapping pattern
  - Error handling pattern

**Sibling files for model structs** (in `modules/fundamental/src/advisory/model/`):
- `summary.rs` and `details.rs` -- inspect to identify:
  - Struct derivation macros (`#[derive(Serialize, Deserialize, ...)]`)
  - Field naming conventions
  - Documentation comment style

**Sibling files for service methods** (in `modules/fundamental/src/advisory/service/`):
  - `advisory.rs` -- already inspected above for method patterns.

**Expected discovered conventions:**

- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Path extraction**: Handlers use `Path<Id>` from Axum extractors
- **Response type**: Handlers return struct directly; Axum's `Json` extractor handles serialization
- **Route registration**: `Router::new().route("/path", get(handler))` pattern
- **Struct derives**: `#[derive(Clone, Debug, Serialize, Deserialize, utoipa::ToSchema)]`

### 4.4 Test convention analysis

**Sibling test files** (in `tests/api/`):
- `advisory.rs` and `sbom.rs` -- inspect with `get_symbols_overview` or Read to identify:
  - Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
  - Response validation: Check status code, then deserialize and assert on fields
  - Error cases: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
  - Test naming: `test_<endpoint>_<scenario>` pattern
  - Setup pattern: Real PostgreSQL test database, test fixtures
  - Parameterized tests: Check if `#[rstest]` is used in siblings

**Expected discovered test conventions:**

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` then deserialize JSON body
- **Response validation**: Assert on specific field values, not just structure
- **Error cases**: All endpoint tests include 404 test
- **Test naming**: `test_<feature>_<scenario>` pattern
- **Setup**: Uses test database with seeded data

### 4.5 Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root -- read for CI check commands and project conventions
- `docs/api.md` -- API documentation that may need updating for the new endpoint
- `docs/architecture.md` -- architecture overview

### 4.6 CONVENTIONS.md lookup

Read `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). Extract:
- CI check commands (formatting, linting, compilation)
- Code generation commands (if any)
- Record for use in Step 9's CI verification

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type). Target branch is `main`.

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file -- SeveritySummary response struct:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of advisories at each severity level linked to a given
/// SBOM, along with a total count. Used by dashboard widgets to render severity
/// breakdowns without client-side counting.
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

Follow the derivation macros and documentation style from sibling model files (`summary.rs`, `details.rs`).

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module declaration:

```rust
pub mod severity_summary;
```

Place it alongside existing declarations (`pub mod summary;`, `pub mod details;`).

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService`, following the pattern of `fetch` and `list`:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with per-level counts and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Use the AdvisorySummary's severity field to count by level
    // Deduplicate by advisory ID
    // Return SeveritySummary with counts defaulting to 0

    // 1. Verify SBOM exists (return 404 if not)
    // 2. Query advisories linked to SBOM via sbom_advisory join table
    // 3. Deduplicate by advisory ID using a HashSet or DISTINCT query
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Compute total as sum of all levels
    // 6. Return SeveritySummary struct
}
```

Key implementation details:
- Use `entity::sbom_advisory` to join SBOM to advisories
- Use `AdvisorySummary.severity` field to classify each advisory
- Deduplicate by advisory ID (use SQL `DISTINCT` or Rust `HashSet`)
- Return 404 via `AppError` with `.context()` if SBOM ID does not exist
- Default all severity counts to 0

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New file -- GET handler for `/api/v2/sbom/{id}/advisory-summary`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories at each severity level
/// (Critical, High, Medium, Low) linked to the specified SBOM, plus a total count.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* injected Transactional */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the exact pattern from `modules/fundamental/src/advisory/endpoints/get.rs`:
- Extract path params via `Path<Id>`
- Call the service method
- Return `Json(result)` directly
- Wrap errors with `.context()`

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route in the advisory module's router:

```rust
mod severity_summary;

// In the router builder, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follow the existing `Router::new().route(...)` registration pattern used for other endpoints.

### 6.6 Documentation on new symbols

Verify that every new struct, function, and public method has a documentation comment:
- `SeveritySummary` struct -- documented with purpose and field descriptions
- `severity_summary` service method -- documented with behavior and parameters
- `get_severity_summary` handler -- documented with endpoint description

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Integration tests following the patterns discovered from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (seed test database with SBOM and linked advisories)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then the response should contain correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, /* expected count */);
    assert_eq!(summary.high, /* expected count */);
    assert_eq!(summary.medium, /* expected count */);
    assert_eq!(summary.low, /* expected count */);
    assert_eq!(summary.total, /* expected total */);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{nonexistent-id}/advisory-summary")
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then each advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Assert counts reflect unique advisories, not duplicate links
    assert_eq!(summary.total, /* unique count, not duplicate count */);
}
```

All tests:
- Use doc comments explaining what they verify
- Follow `test_<feature>_<scenario>` naming convention
- Use given-when-then section comments for clarity
- Assert on specific field values (not just structure or length)
- Use `assert_eq!` with `StatusCode` checks per sibling test conventions

Run tests:
```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by `test_advisory_summary_valid_sbom` and response struct definition |
| Returns 404 when SBOM ID does not exist | Verified by `test_advisory_summary_nonexistent_sbom` |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_advisory_summary_deduplication` and service implementation using DISTINCT/HashSet |
| All severity levels default to 0 when no advisories exist | Verified by `test_advisory_summary_no_advisories` and `Default` derive on SeveritySummary |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient SQL query design (single aggregation query rather than N+1) |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` -- in scope (Files to Modify)

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in scope (Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in scope (Files to Create)
- `tests/api/advisory_summary.rs` -- in scope (Files to Create)

No out-of-scope changes expected. The task description confirms `server/src/main.rs` needs no changes (routes auto-mount via module registration).

### Untracked file check

Run `git status --short` to identify untracked files (`??` prefix). Filter by directories containing modified/created files. Search for code references to any untracked files. Flag for user review if found.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

No sensitive patterns expected in this implementation.

### Documentation currency

Check if `docs/api.md` needs updating for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. If the API docs describe available endpoints, add the new endpoint entry.

### Cross-section reference consistency

Verify file paths are consistent across task description sections:

- **AdvisoryService**: Files to Modify lists `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes references `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- **SeveritySummary model**: Files to Create lists `modules/fundamental/src/advisory/model/severity_summary.rs`, Implementation Notes references `modules/fundamental/src/advisory/model/summary.rs` for the existing `AdvisorySummary` (different entity) -- NOT A CONFLICT (different entities)
- **Endpoint handler**: Files to Create lists `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, Implementation Notes references `modules/fundamental/src/advisory/endpoints/get.rs` as the pattern to follow -- CONSISTENT (pattern reference, not same file)

No cross-section inconsistencies detected.

### Duplication check

Search the codebase for existing severity aggregation logic:
- Grep for `severity_summary`, `severity_count`, `severity_aggregat` -- ensure no existing implementation duplicates this.
- Check if any existing utility in `common/` provides aggregation helpers.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. Fix any failures before proceeding. Hard stop on any non-zero exit.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary`:
  - **Input**: HTTP request with SBOM ID path parameter -- CONNECTED (Path<Id> extraction in handler)
  - **Processing**: Handler calls `AdvisoryService::severity_summary()` -- CONNECTED (service method queries DB)
  - **Query**: Service queries `sbom_advisory` join table, joins to advisory severity -- CONNECTED (SeaORM query)
  - **Aggregation**: Counts by severity level, deduplicates -- CONNECTED (in service method)
  - **Output**: Returns `Json<SeveritySummary>` -- CONNECTED (handler returns response)
  - **Status**: COMPLETE

### Contract and sibling parity

- **SeveritySummary** implements `Serialize`, `Deserialize`, `ToSchema` -- matches sibling model structs
- **get_severity_summary** handler follows same pattern as `get.rs` handler -- consistent error handling, response type, path extraction
- **severity_summary** service method follows same pattern as `fetch` and `list` methods -- consistent signature, transaction handling, error wrapping

No parity gaps expected.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService method, endpoint handler,
and integration tests.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts
for a given SBOM, enabling dashboard widgets to render severity breakdowns.

- New `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- `SeveritySummary` response model with per-severity counts and total
- `AdvisoryService::severity_summary()` method with deduplication
- Integration tests for valid SBOM, non-existent SBOM, empty advisories, and deduplication

Implements [TC-9201](<webUrl>)
"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF format:

   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: Added SeveritySummary model, severity_summary service method, GET endpoint at /api/v2/sbom/{id}/advisory-summary, and 4 integration tests
   - Deviations from plan: None
   - Comment ends with the skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition** TC-9201 to "In Review" via `jira.transition_issue`.
