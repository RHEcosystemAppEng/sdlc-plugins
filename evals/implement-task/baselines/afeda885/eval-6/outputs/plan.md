# Implementation Plan -- TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` with `rust-analyzer`

All sections validated. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt the user for REST API fallback using `scripts/jira-client.py`.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue:

```
jira.get_issue("TC-9201")
```

Parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`, add `severity_summary` method to `AdvisoryService`, use `sbom_advisory` join table, count by severity from `AdvisorySummary`, register route in `endpoints/mod.rs`, return `Result<T, AppError>` with `.context()`
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 on missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 test cases
- **Target PR**: not present
- **Bookend Type**: not present
- **Dependencies**: None

Capture the issue `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

### GitHub Issue extraction

Check `customfield_10747` on the fetched issue for a GitHub Issue URL. If present, parse `owner/repo#number` for use in the PR description. If absent, skip silently.

## Step 1.5 -- Verify Description Integrity

1. Fetch comments: `jira.get_issue_comments("TC-9201")`
2. Locate digest comment by marker `[sdlc-workflow] Description digest:`
3. Found comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` equals `updated` -- no edit detected, no warning needed
5. Extract stored tag: `sha256-md`, stored hex: `a1b2c3d4...`
6. Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
7. Computed output: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
8. Tags match (`sha256-md` == `sha256-md`), hex digests match
9. **Result: MATCH -- proceed silently.** No user prompt, no alert, no added latency.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency checks required. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Get current user: `jira.user_info()` -- extract `accountId`
2. Assign: `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition: `jira.transition_issue("TC-9201")` to "In Progress"

## Step 4 -- Understand the Code

Using Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

### 4.1 Inspect Files to Modify

1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs`
   - Understand `AdvisoryService` struct and existing methods (`fetch`, `list`, `search`)
   - Identify method signature patterns (parameters, return types, `Transactional` usage)

2. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs`
   - Understand route registration pattern (`Router::new().route(...)`)

3. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs`
   - Understand module registration pattern (`pub mod summary;`, `pub mod details;`)

### 4.2 Inspect Referenced Files

4. `mcp__serena_backend__find_symbol` on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` with `include_body=true`
   - Understand the `severity` field type and structure

5. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs`
   - Study the existing endpoint pattern (path params via `Path<Id>`, service call, JSON response)

6. `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs`
   - Understand the join table structure for SBOM-to-Advisory mapping

7. `mcp__serena_backend__find_symbol` on `AppError` in `common/src/error.rs` with `include_body=true`
   - Understand error handling pattern (`.context()` wrapping)

### 4.3 Check Backward Compatibility

8. `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService`
   - Ensure new method won't conflict with existing callers

### 4.4 Convention Conformance Analysis

Identify sibling files and analyze patterns:

- **Endpoint siblings**: `endpoints/get.rs`, `endpoints/list.rs` -- inspect for route handler patterns
- **Model siblings**: `model/summary.rs`, `model/details.rs` -- inspect for struct definition patterns
- **Service siblings**: `service/advisory.rs` (existing methods) -- inspect for method patterns

Expected discovered conventions:
- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Route registration**: `Router::new().route("/path", get(handler))` pattern
- **Response types**: Structs derive `Serialize, Deserialize, ToSchema` and return via Axum's `Json` extractor
- **Path params**: Extracted via `Path<Id>` extractor
- **Service method signature**: `(&self, id: Id, tx: &Transactional<'_>)` pattern

### 4.5 Test Convention Analysis

Inspect sibling test files in `tests/api/`:

- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Expected discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases**: Include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: Real PostgreSQL test database with fixture data

### 4.6 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (path `./` from Registry). If present, read and extract:
- CI check commands (for Step 9)
- Code generation commands
- Any naming or structural conventions

### 4.7 Documentation File Identification

Identify documentation files:
- `docs/api.md` -- API reference (may need updating for new endpoint)
- `docs/architecture.md` -- system architecture overview
- `README.md` -- project readme

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type). Target Branch is `main`:

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

/// Summary of advisory severity counts for a given SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

Follow the pattern from `model/summary.rs` and `model/details.rs` for derive macros and documentation.

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the existing module registration pattern alongside `pub mod summary;` and `pub mod details;`.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method following the pattern of `fetch` and `list`:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to this SBOM
    // 2. Verify SBOM exists (return 404 if not)
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, read severity from AdvisorySummary
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Error handling: use `.context("Failed to fetch severity summary")` wrapping, matching `common/src/error.rs` patterns.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern from `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service.severity_summary(id, &tx).await
        .context("Fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing registration pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Add `mod severity_summary;` at the top of the file.

### 6.6 Documentation Impact

- Check `docs/api.md` -- if it documents REST endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response schema.
- No changes needed to `server/src/main.rs` (routes auto-mount via module registration).

### 6.7 Code Quality Practices

Verify all new structs and public functions have documentation comments (done above). The `SeveritySummary` struct, its fields, and the handler and service methods all have `///` doc comments.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests following sibling test conventions:

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories of known severities
    // (set up test DB with SBOM and linked advisories)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").send().await;

    // Then the response is 200 with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical);
    assert_eq!(summary.high, expected_high);
    assert_eq!(summary.medium, expected_medium);
    assert_eq!(summary.low, expected_low);
    assert_eq!(summary.total, expected_total);
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that a non-existent SBOM ID returns a 404 status.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/nonexistent-id/advisory-summary").send().await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").send().await;

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
/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").send().await;

    // Then the duplicate is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, expected_unique_count);
}
```

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by Test 1
2. Returns 404 when SBOM ID does not exist -- verified by Test 2
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by Test 4
4. All severity levels default to 0 when no advisories exist -- verified by Test 3 (uses `Default` derive)
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by query design (single join query with GROUP BY, no N+1)

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

Expected modified/created files:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create) -- in scope
- `modules/fundamental/src/advisory/model/mod.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/service/advisory.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create) -- in scope
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify) -- in scope
- `tests/api/advisory_summary.rs` (create) -- in scope

If `docs/api.md` was modified, it is out-of-scope per the task description but justified by documentation impact analysis. Flag for user approval.

### Untracked file check

Run `git status --short`, check for `??` entries in directories with implementation work. Flag any referenced untracked files for user approval.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency

Verify `docs/api.md` reflects the new endpoint if it was updated. No other docs should need changes.

### CI checks from CONVENTIONS.md

Run any CI check commands extracted from `CONVENTIONS.md` in Step 4. If none found, run `cargo build` and `cargo clippy` as standard Rust checks. Fix any failures or warnings before proceeding.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> aggregate by severity -> return `Json<SeveritySummary>` -- **COMPLETE**

### Contract and sibling parity

- `SeveritySummary` struct: no trait/interface contract to implement beyond `Serialize`/`Deserialize`/`ToSchema` (all derived) -- COMPLETE
- Sibling parity with `get.rs` endpoint: path extraction, service call, JSON response, error handling with `.context()` -- all present -- COMPLETE
- Sibling parity with `fetch`/`list` service methods: same signature pattern `(&self, id, tx)`, same return type pattern `Result<T, AppError>` -- COMPLETE

### Duplication check

Search for existing severity aggregation logic in the codebase using `mcp__serena_backend__search_for_pattern` or Grep. Ensure no existing utility already performs this aggregation.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
route registration, and integration tests.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

- New `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning `{ critical, high, medium, low, total }`
- `SeveritySummary` response model with derive macros for serialization and OpenAPI schema
- `AdvisoryService::severity_summary()` method using the `sbom_advisory` join table with deduplication
- Integration tests covering valid SBOM, missing SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If a GitHub Issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL using ADF inlineCard format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint with `SeveritySummary` model, service method, route registration, and integration tests
   - No deviations from the plan
   - Comment ends with the required footnote (horizontal rule + AI-generated attribution with plugin version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition** TC-9201 to "In Review":

```
jira.transition_issue("TC-9201") -> "In Review"
```
