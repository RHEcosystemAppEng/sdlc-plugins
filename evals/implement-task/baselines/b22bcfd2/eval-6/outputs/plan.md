# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001 (linked via "is incorporated by")

## Parsed Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint
- **Dependencies**: None
- **Target PR**: None (default flow)
- **Bookend Type**: None (standard implementation)

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains:
1. **Repository Registry** -- present, contains trustify-backend with Serena instance `serena_backend`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, documents `serena_backend` instance with rust-analyzer

All sections are present and complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. Fall back to REST API if MCP fails, following the prompt protocol.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse all structured sections as listed above. Capture the `webUrl` for use in the PR description. Extract GitHub Issue custom field (`customfield_10747`) if present. No Target PR and no Bookend Type -- this is a standard implementation task.

## Step 1.5 -- Verify Description Integrity

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate the comment whose body starts with `[sdlc-workflow] Description digest:`
3. Found comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment edit check: `created` and `updated` timestamps are identical -- comment is unmodified
5. Extract stored digest: format tag `sha256-md`, hex `a1b2c3d4e5f67890...`
6. Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
7. Compare format tags: both `sha256-md` -- tags match
8. Compare hex digests: stored matches computed
9. **Result**: Digests match -- proceed silently to Step 2 without prompting the user

## Step 2 -- Verify Dependencies

The task lists "Dependencies: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code

### 4.1 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the trustify-backend root using `mcp__serena_backend__list_dir`. If present, read it and extract CI check commands and code generation commands. Follow any conventions throughout implementation.

### 4.2 Inspect Files to Modify

Use `mcp__serena_backend__get_symbols_overview` on each file to understand structure:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- inspect AdvisoryService struct and its existing methods (`fetch`, `list`, `search`) to understand the pattern for adding `severity_summary`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- inspect route registration pattern (`Router::new().route(...)`)
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- inspect module registration pattern (`pub mod ...;`)

Use `mcp__serena_backend__find_symbol` with `include_body=true` to read:
- `AdvisoryService::fetch` method body -- to understand the method pattern (parameters, return type, transactional usage)
- `AdvisoryService::list` method body -- for the query/aggregation pattern
- Existing endpoint handler in `modules/fundamental/src/advisory/endpoints/get.rs` -- for Path extraction, service invocation, and JSON response pattern

### 4.3 Inspect Related Entities

Use `mcp__serena_backend__get_symbols_overview` on:
- `entity/src/sbom_advisory.rs` -- understand the join table structure for finding advisories linked to an SBOM
- `modules/fundamental/src/advisory/model/summary.rs` -- inspect the `AdvisorySummary` struct and its `severity` field (needed for counting by severity level)
- `common/src/error.rs` -- inspect `AppError` enum and `.context()` pattern

### 4.4 Inspect Files to Create Locations

Use `mcp__serena_backend__list_dir` on:
- `modules/fundamental/src/advisory/model/` -- confirm directory exists, see existing model files for sibling pattern
- `modules/fundamental/src/advisory/endpoints/` -- confirm directory exists, see existing endpoint files
- `tests/api/` -- confirm directory exists, see existing test files

### 4.5 Convention Conformance Analysis

Examine sibling files for patterns:

**Production code siblings:**
- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- endpoint handler pattern
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- model struct pattern
- `modules/fundamental/src/sbom/service/sbom.rs` -- service method pattern (alternative reference)

**Expected conventions to discover:**
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Service methods: take `&self`, entity ID, and `&Transactional<'_>` parameter
- Endpoint handlers: extract `Path<Id>`, call service, return `Json<T>`
- Model structs: derive `Serialize`, `Deserialize`, possibly `ToSchema` for OpenAPI
- Route registration: `Router::new().route("/path", get(handler_fn))`

### 4.6 Test Convention Analysis

Examine sibling test files:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

**Expected test conventions to discover:**
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Error case pattern: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Test naming: `test_<endpoint>_<scenario>` pattern
- Test setup: database seeding with test fixtures

### 4.7 Documentation File Identification

Look for documentation related to advisory endpoints:
- `docs/api.md` at repository root -- API reference documentation
- `docs/architecture.md` -- system architecture overview
- README files in the advisory module directory

### 4.8 Check for Backward Compatibility

Use `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` -- identify all callers to ensure adding a new method does not affect existing ones
- The route registration function in `endpoints/mod.rs` -- ensure adding a new route does not conflict

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create SeveritySummary Model

**File**: `modules/fundamental/src/advisory/model/severity_summary.rs` (NEW)

Create a `SeveritySummary` struct with fields:
- `critical: u32` (or appropriate integer type matching project conventions)
- `high: u32`
- `medium: u32`
- `low: u32`
- `total: u32`

Derive `Serialize`, `Deserialize`, and any other traits matching sibling model structs (e.g., `ToSchema`, `Debug`, `Clone`). Add a doc comment describing the struct's purpose.

Implement a `Default` trait or constructor that initializes all counts to 0.

### 6.2 Register the Model Module

**File**: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

Add `pub mod severity_summary;` following the existing module registration pattern (alongside `pub mod summary;` and `pub mod details;`).

### 6.3 Add Service Method

**File**: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

Add a `severity_summary` method to `AdvisoryService`:

```rust
/// Computes severity counts for all advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to sbom_id
    // 2. Deduplicate by advisory ID
    // 3. For each unique advisory, fetch its AdvisorySummary and read the severity field
    // 4. Count occurrences of each severity level (Critical, High, Medium, Low)
    // 5. Compute total as sum of all levels
    // 6. Return SeveritySummary with the counts
}
```

Follow the existing `fetch` and `list` method patterns for error handling (`.context("...")` wrapping), transaction usage, and return type.

### 6.4 Create Endpoint Handler

**File**: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (NEW)

Create a GET handler following the pattern in `get.rs`:

```rust
/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns severity counts for all advisories linked to the specified SBOM.
pub async fn severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    // 1. Call service.severity_summary(id, &tx)
    // 2. Return Json(result)
    // Handle 404 for non-existent SBOM IDs consistently with existing endpoints
}
```

Add a doc comment on the handler function.

### 6.5 Register the Route

**File**: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

Add the new route registration:
```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

Follow the existing `Router::new().route(...)` pattern in the file. Import the new endpoint module.

### 6.6 Documentation Impact

After implementing, check if `docs/api.md` or other API documentation files need updating to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Apply lightweight documentation updates if needed.

### 6.7 Code Quality Practices

Verify all new symbols have documentation comments:
- `SeveritySummary` struct -- doc comment describing the response type
- Each field on the struct -- brief doc comments
- `severity_summary` service method -- doc comment describing behavior, parameters, return value
- `severity_summary` endpoint handler -- doc comment describing the HTTP contract

## Step 7 -- Write Tests

**File**: `tests/api/advisory_summary.rs` (NEW)

Follow test conventions discovered in Step 4 (sibling test analysis of `tests/api/advisory.rs` and `tests/api/sbom.rs`).

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisory severities returns correct counts per level.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (seed database with test SBOM and linked advisories: 2 Critical, 1 High, 3 Medium, 0 Low)

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK and the body contains correct counts
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, 2)
    // assert_eq!(body.high, 1)
    // assert_eq!(body.medium, 3)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 6)
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{non-existent-id}/advisory-summary

    // Then the response status is 404 Not Found
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    // (seed database with an SBOM but no advisory links)

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links in the join table are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    // (seed database with an SBOM and an advisory linked via two join table entries)

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, 1) -- not 2
}
```

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

Review each criterion against the implementation:

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by endpoint handler returning `Json<SeveritySummary>` and test 1
2. Returns 404 when SBOM ID does not exist -- verified by error handling in handler and test 2
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by service method deduplication logic and test 4
4. All severity levels default to 0 when no advisories exist -- verified by SeveritySummary defaults and test 3
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by efficient query design (single query with GROUP BY rather than N+1 queries)

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all changed files are within the expected scope:
- `modules/fundamental/src/advisory/service/advisory.rs` -- Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` -- Files to Modify
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- Files to Create
- `tests/api/advisory_summary.rs` -- Files to Create

Flag any out-of-scope files for user approval.

### Untracked File Check

Run `git status --short`, extract `??` entries, filter by proximity to modified directories, and check for code references. Flag any referenced untracked files for user approval.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to detect secrets.

### Documentation Currency

Check that `docs/api.md` (if it exists and documents advisory endpoints) has been updated to include the new endpoint.

### Documentation Scope Preservation

If `docs/api.md` was modified, verify that the replacement text still covers all previously documented use cases.

### Eval Coverage Currency

No SKILL.md files are being modified -- skip.

### Example Consistency

If documentation with examples was written, verify narrative-data consistency.

### Cross-Section Reference Consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` is referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent
- Route registration is in `advisory/endpoints/mod.rs` in both sections -- consistent

### Duplication Check

Search for existing severity aggregation or count methods in the codebase using Grep/Serena to ensure no duplication.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md (if found in Step 4). Hard stop on any failure.

### Data-Flow Trace

Trace the data path for the new feature:
- **Input**: HTTP GET request with SBOM ID in path parameter
- **Processing**: Endpoint handler extracts path param, calls `AdvisoryService::severity_summary`, which queries `sbom_advisory` join table, deduplicates advisories, counts by severity level
- **Output**: JSON response with `SeveritySummary` struct containing counts per severity level and total
- **Status**: COMPLETE -- all stages connected

### Contract & Sibling Parity

- `SeveritySummary` struct: standalone response type, no trait/interface contract to verify
- Sibling parity with `get.rs` endpoint: error handling pattern, response type pattern, path extraction pattern -- all matched
- Sibling parity with `fetch`/`list` service methods: parameter pattern, transactional usage, error wrapping -- all matched

## Step 10 -- Commit and Push

Commit with Conventional Commits format:

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to an
SBOM. Includes SeveritySummary model, AdvisoryService::severity_summary
method, and integration tests covering valid SBOMs, 404 handling, zero
counts, and deduplication.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

- Add GET /api/v2/sbom/{id}/advisory-summary endpoint returning severity counts per level
- Add SeveritySummary response model and AdvisoryService::severity_summary service method
- Add integration tests covering valid responses, 404 handling, zero counts, and deduplication

Implements [TC-9201](<webUrl>)
"
```

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL using ADF inlineCard format
2. Add a comment to TC-9201 with:
   - PR link
   - Summary of changes made (new endpoint, model, service method, tests)
   - Confirmation that no deviations from the plan occurred
   - Skill footer with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`
3. Transition TC-9201 to "In Review"
