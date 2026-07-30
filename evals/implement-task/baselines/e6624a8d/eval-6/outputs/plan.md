# Implementation Plan for TC-9201

**Task:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, tool naming convention documented (`mcp__<serena-instance>__<tool>`), `serena_backend` instance configured with `rust-analyzer`

All sections present and complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all Jira operations. If MCP fails, prompt the user with the three options (REST API fallback, skip, retry) as documented in the skill.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates advisory severity counts for an SBOM |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Target PR | Not present |
| Bookend Type | Not present |
| Dependencies | None |

Capture the issue `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

Check the GitHub Issue custom field (`customfield_10747`) for a linked GitHub issue. If present, extract `owner/repo#number` for the PR description's `Closes` line.

## Step 1.5 -- Verify Description Integrity

(See `digest-match.md` for the detailed walkthrough.)

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate the digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890...`
3. Verify comment was not edited (created == updated timestamps) -- OK
4. Extract format tag (`sha256-md`) and hex digest
5. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
6. Compare tags -- both `sha256-md`, tags match
7. Compare hex digests -- match

**Result:** Digests match. Proceed silently.

## Step 2 -- Verify Dependencies

The task lists `Dependencies: None`. No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID: `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify using Serena (serena_backend)

**Advisory service** (`modules/fundamental/src/advisory/service/advisory.rs`):
- `mcp__serena_backend__get_symbols_overview` to see AdvisoryService structure
- `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` to understand the existing fetch method pattern (takes `&self, id: Id, tx: &Transactional<'_>`)
- `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` to see the list method pattern

**Advisory endpoints mod** (`modules/fundamental/src/advisory/endpoints/mod.rs`):
- `mcp__serena_backend__get_symbols_overview` to see how routes are registered
- Understand the `Router::new().route(...)` registration pattern

**Advisory model mod** (`modules/fundamental/src/advisory/model/mod.rs`):
- `mcp__serena_backend__get_symbols_overview` to see existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`)

### 4.2 Inspect reference files for patterns

**Existing endpoint handler** (`modules/fundamental/src/advisory/endpoints/get.rs`):
- `mcp__serena_backend__find_symbol` on the GET handler function to see the full pattern: `Path<Id>` extraction, service call, JSON response, `Result<T, AppError>` return type, `.context()` error wrapping

**Existing model** (`modules/fundamental/src/advisory/model/summary.rs`):
- `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to see the struct layout, especially the `severity` field that we will use for counting

**SBOM-Advisory join table** (`entity/src/sbom_advisory.rs`):
- `mcp__serena_backend__get_symbols_overview` to understand the join entity for linking SBOMs to advisories

### 4.3 Inspect sibling files for convention conformance

**Sibling endpoint files** (for pattern analysis):
- `modules/fundamental/src/advisory/endpoints/list.rs` -- list handler pattern
- `modules/fundamental/src/sbom/endpoints/get.rs` -- another GET-by-ID pattern for cross-module comparison

**Sibling model files:**
- `modules/fundamental/src/advisory/model/details.rs` -- struct naming, serde derives, documentation style

**Error handling:**
- `common/src/error.rs` -- `AppError` enum and `.context()` usage

### 4.4 Convention conformance analysis (expected output)

**Discovered conventions (from sibling analysis):**
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`)
- **Endpoint pattern:** Extract path params via `Path<Id>`, call service method, return `Json(result)` or `Result<Json<T>, AppError>`
- **Route registration:** `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`
- **Model structs:** Derive `Serialize, Deserialize, Clone, Debug` with `#[serde(rename_all = "camelCase")]`
- **Module registration:** New model modules are added as `pub mod <name>;` in `model/mod.rs`
- **Service method signature:** `async fn method_name(&self, param: Type, tx: &Transactional<'_>) -> Result<T, AppError>`
- **Naming:** Service methods follow `verb_noun` pattern (`fetch`, `list`, `severity_summary`)

### 4.5 Test convention analysis

**Sibling test files:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

**Discovered test conventions (expected):**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases:** 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Setup:** Tests hit a real PostgreSQL test database, create test data, then assert
- **Parameterized tests:** Check sibling tests for `#[rstest]` usage; if not used, do not introduce

### 4.6 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md` per the Repository Registry path). If present, read it and extract:
- CI check commands (formatting, linting, compilation commands)
- Code generation commands
- Any additional project conventions

### 4.7 Documentation file identification

Identify documentation files for later documentation-impact evaluation:
- `docs/api.md` -- REST API reference, will need updating for the new endpoint
- `docs/architecture.md` -- system architecture, unlikely to need changes
- `README.md` -- project overview

## Step 5 -- Create Branch

No Target PR and no Bookend Type -- use default flow:

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
/// Summary of advisory severity counts for a given SBOM.
///
/// Aggregates the number of advisories at each severity level, providing
/// a quick overview for dashboard widgets without client-side counting.
#[derive(Clone, Debug, Serialize, Deserialize, utoipa::ToSchema)]
#[serde(rename_all = "camelCase")]
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

Follow existing model conventions discovered in Step 4 (derives, serde rename, documentation comments).

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` alongside existing `pub mod summary;` and `pub mod details;` declarations.

### 6.3 Add `severity_summary` method to AdvisoryService in `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method following the existing `fetch`/`list` pattern:

```rust
/// Computes advisory severity counts for the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not) -- follow existing fetch pattern
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Join with advisory table to get severity field
    // 4. Deduplicate by advisory ID (using DISTINCT or HashSet)
    // 5. Count by severity level using the AdvisorySummary.severity field
    // 6. Return SeveritySummary with counts, defaulting to 0 for missing levels
}
```

Key implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find linked advisories
- Join with the advisory entity to access `AdvisorySummary.severity` for counting
- Use `DISTINCT` on advisory ID to deduplicate
- Handle 404 for non-existent SBOM by checking SBOM existence first
- Wrap errors with `.context("Failed to compute severity summary")`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern from `endpoints/get.rs`:

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
        .context("Failed to retrieve advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route to the existing Router registration:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follow the existing `Router::new().route(...)` registration pattern seen in the file.

### 6.6 Documentation impact

Update `docs/api.md` (if it documents REST endpoints) to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request parameters and response shape.

No changes needed to `server/src/main.rs` (routes auto-mount via module registration, as noted in the task description).

### 6.7 Cross-section reference consistency

Verify file paths are consistent across the task description sections:
- `AdvisoryService` is referenced in both "Files to Modify" (`advisory/service/advisory.rs`) and "Implementation Notes" (`advisory/service/advisory.rs`) -- consistent
- Route registration is in "Files to Modify" (`advisory/endpoints/mod.rs`) and "Implementation Notes" (`advisory/endpoints/mod.rs`) -- consistent
- `AdvisorySummary` struct referenced in "Implementation Notes" (`advisory/model/summary.rs`) -- this is a read-only reference, not a file being modified -- consistent

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Write integration tests following the sibling test conventions discovered in Step 4:

#### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns the correct severity breakdown.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM linked to advisories with known severity levels
    // (set up test SBOM and link advisories with Critical=2, High=3, Medium=1, Low=0)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response should contain the correct severity counts
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, 2)
    // assert_eq!(body.high, 3)
    // assert_eq!(body.medium, 1)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 6)
}
```

#### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response should be 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

#### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all counts should be zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}
```

#### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory-SBOM links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM linked to the same advisory twice (duplicate join table entries)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory should be counted only once
    // assert_eq!(body.total, 1) -- not 2
}
```

All tests use value-based assertions (specific field values, not just collection lengths) per the skill's quality guidance. Each test has a doc comment and given-when-then section comments.

**Run tests:**

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Endpoint implemented in Step 6.4, route registered in Step 6.5, response struct in Step 6.1 |
| Returns 404 when SBOM ID does not exist | Service method checks SBOM existence and returns AppError; tested in Test 2 |
| Counts only unique advisories (deduplicates by advisory ID) | Service uses DISTINCT on advisory ID; tested in Test 4 |
| All severity levels default to 0 when no advisories exist at that level | SeveritySummary::default() returns all zeros; tested in Test 3 |
| Response time under 200ms for SBOMs with up to 500 advisories | Efficient query using JOIN and GROUP BY at the database level rather than in-memory iteration |

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all changed files are in scope:
- `modules/fundamental/src/advisory/service/advisory.rs` -- Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` -- Files to Modify
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- Files to Create
- `tests/api/advisory_summary.rs` -- Files to Create

Flag any additional files (e.g., `docs/api.md` for documentation updates) as out-of-scope and request user approval.

### Untracked file check
Run `git status --short` to find untracked files (prefixed with `??`). Filter by proximity to modified directories. Search for code references to any proximity-matched untracked files.

### Dead parameter detection
Scan modified functions for parameters that are no longer used after changes. If any found, remove them and update all callers.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to check for secrets.

### Documentation currency
Verify that `docs/api.md` includes the new endpoint if it documents existing endpoints. Update if needed.

### Duplication check
Search for existing severity counting or advisory aggregation logic in the repository to avoid duplication.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from `CONVENTIONS.md` (formatting, linting, compilation). Hard stop on any failure.

### Data-flow trace
```
GET /api/v2/sbom/{id}/advisory-summary
  -> Axum route match (endpoints/mod.rs)
  -> severity_summary handler (endpoints/severity_summary.rs)
  -> AdvisoryService::severity_summary (service/advisory.rs)
  -> Query sbom_advisory join table (entity/sbom_advisory.rs)
  -> Count by severity, deduplicate by advisory ID
  -> Return SeveritySummary struct (model/severity_summary.rs)
  -> Axum Json serialization -> HTTP response

Path: request -> route -> handler -> service -> database -> response -- COMPLETE
```

### Contract and sibling parity
- **Contract verification:** SeveritySummary implements Serialize/Deserialize as required by Axum's Json extractor. The handler returns `Result<Json<SeveritySummary>, AppError>` matching the Axum contract.
- **Sibling parity:** Compare with `get.rs` handler -- both extract Path<Id>, call service, return Json. Check that error handling, logging, and response patterns match.

### Query-scope verification
The query targets advisories linked to a specific SBOM via the `sbom_advisory` join table, filtered by `sbom_id`. This correctly scopes to the target SBOM -- no overly broad query.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Add docs/api.md if modified and approved by user

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity summary endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
proper 404 handling for missing SBOMs.

Implements TC-9201"
```

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If upstream exists, parse `<upstream-owner/repo>` and `<fork-owner>` for PR creation.

### Push and create PR

```bash
git push -u origin TC-9201
```

Create PR with `--base main`:

```bash
gh pr create --base main \
  --title "feat(api): add advisory severity summary endpoint" \
  --body "## Summary

- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint returning severity counts
- Add \`SeveritySummary\` response struct with critical, high, medium, low, and total counts
- Add \`severity_summary\` method to \`AdvisoryService\` using \`sbom_advisory\` join table
- Integration tests for valid SBOM, missing SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

Closes <owner/repo#number if GitHub Issue was found>"
```

If fork detected, add `-R <upstream-owner/repo> --head <fork-owner>:TC-9201`.

## Step 11 -- Update Jira

### Set Git Pull Request custom field

Look up field ID from Jira Configuration: `customfield_10875`.

```
jira.update_issue("TC-9201", fields={
  "customfield_10875": {
    "type": "doc",
    "version": 1,
    "content": [{
      "type": "paragraph",
      "content": [{
        "type": "inlineCard",
        "attrs": {"url": "<PR-URL>"}
      }]
    }]
  }
})
```

### Add implementation comment

Post a comment to TC-9201 with:
- PR link
- Summary of changes made (new endpoint, service method, model struct, tests)
- Confirmation of no deviations from the plan
- Skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

### Transition to In Review

```
jira.transition_issue("TC-9201") -> In Review
```
