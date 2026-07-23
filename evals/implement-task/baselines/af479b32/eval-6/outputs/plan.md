# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID.
3. **Code Intelligence** -- present, tool naming convention documented (`mcp__<serena-instance>__<tool>`), with `serena_backend` configured for `trustify-backend` using `rust-analyzer`.

All required sections are present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Determine the access method for JIRA operations. Attempt MCP first; if MCP fails, prompt the user for REST API fallback.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description.

**Parsed fields:**

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Bookend Type | (none) |
| Target PR | (none) |
| Dependencies | None |

**Web URL**: Captured from the API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

**GitHub Issue**: Look up `customfield_10747` from the issue fields. If present, parse the GitHub issue URL and store as `owner/repo#number` for the PR description's `Closes` line. If absent, skip silently.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the full procedure. Summary:

1. Fetch comments on TC-9201.
2. Locate the digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
3. Comment edit detection: `created` equals `updated` -- comment is unmodified. No warning.
4. Extract stored digest: format tag `sha256-md`, hex digest `a1b2c3d4e5f67890...`.
5. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`.
6. Compare format tags: both `sha256-md` -- tags match.
7. Compare hex digests: match confirmed. Proceed silently.

## Step 2 -- Verify Dependencies

The task has no dependencies. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`.

## Step 4 -- Understand the Code

Using the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

### 4.1 Inspect Files to Modify

- **`modules/fundamental/src/advisory/service/advisory.rs`**: Use `mcp__serena_backend__get_symbols_overview` to see the `AdvisoryService` structure, then `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand the pattern for adding `severity_summary`.
- **`modules/fundamental/src/advisory/endpoints/mod.rs`**: Inspect route registration pattern with `get_symbols_overview`. Understand how routes are added via `Router::new().route(...)`.
- **`modules/fundamental/src/advisory/model/mod.rs`**: Check existing `pub mod` declarations to understand how new model modules are registered.

### 4.2 Inspect Sibling Files (Convention Conformance Analysis)

- **Sibling endpoints**: Inspect `modules/fundamental/src/advisory/endpoints/get.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` to understand the handler pattern (path param extraction, service calls, JSON responses, error handling).
- **Sibling models**: Inspect `modules/fundamental/src/advisory/model/summary.rs` and `modules/fundamental/src/advisory/model/details.rs` to understand struct patterns, derive macros, and the `severity` field on `AdvisorySummary`.
- **Sibling service methods**: Inspect existing `fetch` and `list` methods in `advisory.rs` for parameter patterns (`&self, id: Id, tx: &Transactional<'_>`).
- **Entity join table**: Inspect `entity/src/sbom_advisory.rs` to understand the SBOM-Advisory join table structure.

### 4.3 Backward Compatibility

Use `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., the `AdvisoryService` impl block, the endpoint module's route registration) to ensure changes do not break callers.

### 4.4 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If found, read it and extract CI check commands for use in Step 9. Follow any naming rules, directory structure conventions, and code patterns throughout implementation.

### 4.5 Test Convention Analysis

Inspect sibling test files:
- **`tests/api/advisory.rs`**: Examine assertion patterns, response validation, error case coverage, test naming, setup/teardown.
- **`tests/api/sbom.rs`**: Check for additional patterns (404 handling, empty result testing).

Record discovered conventions for use in Step 7.

### 4.6 Documentation File Identification

Identify documentation files related to the changes:
- `README.md` at the repository root
- `docs/api.md` (referenced in CLAUDE.md) for API documentation
- `docs/architecture.md` for architecture overview

### Expected Discovered Conventions

**Production code conventions (from sibling analysis):**
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`)
- **Endpoint pattern**: Extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Route registration**: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Model structs**: Derive `Serialize`, `Deserialize`, `Debug`, `Clone`; add doc comments
- **Response types**: Return structs directly; Axum's `Json` extractor handles serialization

**Test conventions (from sibling test analysis):**
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases**: Include 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file: `SeveritySummary` response struct.

```rust
/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of advisories at each severity level linked to a given
/// SBOM, enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Clone, Debug, Serialize, Deserialize)]
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

Include a `Default` implementation that initializes all fields to 0.

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to the existing module declarations.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Following the pattern of existing `fetch` and `list` methods:

```rust
/// Computes a severity summary for all advisories linked to a given SBOM.
///
/// Uses the `sbom_advisory` join table to find advisories associated with the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts for Critical, High, Medium, and Low,
/// plus a total count.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to the SBOM
    // 2. Join with advisory table to get severity information
    // 3. Deduplicate by advisory ID
    // 4. Count by severity level using AdvisorySummary.severity field
    // 5. Return SeveritySummary with counts; default 0 for levels with no advisories
    // 6. Return 404 (via AppError) if the SBOM ID does not exist
}
```

Implementation details:
- Use the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` to join SBOMs to advisories
- Load `AdvisorySummary` structs and read the `severity` field
- Deduplicate by advisory ID before counting
- Return `AppError` with `.context()` if the SBOM is not found, consistent with existing SBOM endpoints

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler following the pattern from `get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary of all advisories linked to the specified SBOM,
/// with counts per severity level (Critical, High, Medium, Low) and a total.
pub async fn severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route to the existing router registration:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

Import the new endpoint module at the top of the file.

### 6.6 Documentation Impact

- No `Documentation Updates` section in the task description.
- Check `docs/api.md` for API reference documentation. If the file documents REST endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response schema.
- `server/src/main.rs` requires no changes (routes auto-mount via module registration).

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases, following discovered test conventions (assertion style, naming, error case coverage):

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM linked to advisories with known severity levels
    // (setup: seed test DB with SBOM and linked advisories at Critical, High, Medium, Low)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").send().await;

    // Then the response is 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, <expected_critical_count>);
    assert_eq!(summary.high, <expected_high_count>);
    assert_eq!(summary.medium, <expected_medium_count>);
    assert_eq!(summary.low, <expected_low_count>);
    assert_eq!(summary.total, <expected_total_count>);
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").send().await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories
    // (setup: seed test DB with SBOM but no advisory links)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").send().await;

    // Then the response is 200 OK with all zeros
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
/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    // (setup: seed test DB with SBOM and duplicate sbom_advisory entries)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").send().await;

    // Then the response counts each advisory only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Assert total equals number of unique advisories, not total link count
    assert_eq!(summary.total, <expected_unique_count>);
}
```

Run tests:

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by test 1 -- endpoint returns correct JSON shape with counts |
| Returns 404 for non-existent SBOM ID | Verified by test 2 -- 404 status code returned |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by test 4 -- duplicate links produce correct unique count |
| All severity levels default to 0 when no advisories exist | Verified by test 3 -- all-zero response for empty SBOM |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by query design -- single SQL query with GROUP BY, no N+1; performance validated during integration test execution |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files match the task's Files to Modify and Files to Create:

**Expected files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` (created)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (created)
- `tests/api/advisory_summary.rs` (created)
- `modules/fundamental/src/advisory/service/advisory.rs` (modified)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified)
- `modules/fundamental/src/advisory/model/mod.rs` (modified)

Any out-of-scope files require user approval before committing.

### Untracked File Check

Run `git status --short`, extract `??` entries, filter by proximity to implementation directories, search for code references, and flag any untracked files that are referenced by code or in modified directories.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches and do not proceed until resolved.

### Documentation Currency

Check if `docs/api.md` needs updating with the new endpoint. If the endpoint was added but the API docs were not updated in Step 6, update them now.

### Documentation Scope Preservation

If `docs/api.md` was modified, verify that the replacement text still covers all previously documented endpoints and scenarios.

### Cross-Section Reference Consistency

Verify file paths are consistent across all task description sections:
- `AdvisoryService` -- Files to Modify: `service/advisory.rs`, Implementation Notes: `service/advisory.rs` -- consistent.
- `SeveritySummary` -- Files to Create: `model/severity_summary.rs`, Implementation Notes: references `model/summary.rs` for the existing `AdvisorySummary` (different entity) -- no conflict.
- Route registration -- Files to Modify: `endpoints/mod.rs`, Implementation Notes: `endpoints/mod.rs` -- consistent.

### Duplication Check

Search the repository for existing severity aggregation or counting logic to ensure the new code does not duplicate existing utilities.

### CI Checks from CONVENTIONS.md

If CONVENTIONS.md was found and contains CI check commands, run all of them. Hard stop on any failure.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService.severity_summary(id, tx)` -> query `sbom_advisory` join table -> join advisory entity -> deduplicate by advisory ID -> count by severity -> build `SeveritySummary` -> return `Json(summary)` -- **COMPLETE**

### Contract and Sibling Parity

- **Contract verification**: `severity_summary` handler returns `Result<Json<SeveritySummary>, AppError>` -- matches the Axum handler contract used by all sibling endpoints.
- **Sibling parity**: Compare with `get.rs` and `list.rs` handlers:
  - Error handling via `.context()` -- matches.
  - Path param extraction via `Path<Id>` -- matches.
  - Service call pattern -- matches.
  - Response type (`Json<T>`) -- matches.

## Step 10 -- Commit and Push

### Fork Detection

```bash
git remote get-url upstream 2>/dev/null
```

Determine whether working in a fork and set PR creation flags accordingly.

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary method,
endpoint handler, and integration tests.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes (new endpoint, model, service method, tests)
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- `Closes <owner>/<repo>#<number>` if a GitHub issue reference was extracted in Step 1

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format (inlineCard).
2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint with `SeveritySummary` model, `AdvisoryService.severity_summary` service method, and integration tests covering valid SBOMs, 404 handling, empty advisories, and deduplication.
   - Deviations from plan: (none expected)
   - Comment ends with the skill footnote (horizontal rule + "This comment was AI-generated by sdlc-workflow/implement-task v0.13.4.")
3. **Transition** TC-9201 to "In Review".
