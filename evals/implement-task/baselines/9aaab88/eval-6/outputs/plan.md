# Implementation Plan -- TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001
**Dependencies**: None

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>`

Validation passes. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. Fall back to REST API if MCP fails, following the prompt flow defined in the skill.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing endpoint pattern, use `sbom_advisory` join table, use `AdvisorySummary.severity` field for counting, return `AppError` with `.context()` wrapping
- **Acceptance Criteria**: 5 items (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 items (valid counts, 404, empty SBOM, deduplication)
- **Bookend Type**: not present (standard implementation flow)
- **Target PR**: not present (standard flow)
- **Dependencies**: None

Capture `webUrl` for the Jira issue (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

Check the **GitHub Issue custom field** (`customfield_10747`) -- extract value if present for use in PR description.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the full description of this step.

Summary: The digest comment is found with marker `[sdlc-workflow] Description digest:`. The stored digest is `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`. The comment's `created` and `updated` timestamps are identical (no edit detected). The computed digest from `scripts/sha256-digest.py` matches the stored digest (both format tag `md` and hex value match). **Result: proceed silently** -- no user prompt, no additional latency.

## Step 2 -- Verify Dependencies

The task has no dependencies (`Dependencies: None`). Skip this step.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID: `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

### 4.1 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root using `mcp__serena_backend__list_dir` or Read/Glob. The repo structure shows `CONVENTIONS.md` exists. Read it and extract:
- CI check commands (for Step 9)
- Code generation commands (if any)
- Project conventions

### 4.2 Inspect Files to Modify

Use Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- `get_symbols_overview` to see `AdvisoryService` structure, then `find_symbol` with `include_body=true` on `fetch` and `list` methods to understand the pattern for the new `severity_summary` method
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- `get_symbols_overview` to see current route registration pattern
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read to see existing module declarations

### 4.3 Inspect Related Files (Implementation Notes references)

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- `find_symbol` on the GET handler to understand `Path<Id>` extraction, service call, and JSON response pattern
2. **`entity/src/sbom_advisory.rs`** -- `get_symbols_overview` to understand the join table structure
3. **`modules/fundamental/src/advisory/model/summary.rs`** -- `find_symbol` on `AdvisorySummary` to see the `severity` field type
4. **`common/src/error.rs`** -- `find_symbol` on `AppError` to understand error handling pattern

### 4.4 Check Backward Compatibility

Use `find_referencing_symbols` on any symbols being modified (e.g., `AdvisoryService`, the endpoints `mod.rs` router) to ensure changes don't break existing callers.

### 4.5 Convention Conformance Analysis

Examine sibling files for conventions:
- **Sibling endpoints**: `endpoints/get.rs`, `endpoints/list.rs` -- handler signature, error wrapping, response type
- **Sibling models**: `model/summary.rs`, `model/details.rs` -- struct definition patterns, derive macros, documentation
- **Sibling services**: `service/advisory.rs` existing methods -- method signature, transaction handling, return types

Expected discovered conventions:
- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern
- **Route registration**: `Router::new().route("/path", get(handler))` pattern
- **Response types**: List endpoints use `PaginatedResults<T>`, single-item endpoints return direct JSON
- **Derive macros**: Model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone` (and possibly `utoipa::ToSchema`)

### 4.6 Test Convention Analysis

Examine sibling test files:
- **`tests/api/advisory.rs`** -- assertion patterns, setup/teardown, test naming
- **`tests/api/sbom.rs`** -- similar patterns for SBOM-related endpoint tests

Expected discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases**: 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: Uses test database with seeded fixtures

### 4.7 Documentation File Identification

Identify documentation files related to the code being modified:
- `docs/api.md` -- REST API reference (may need updating for new endpoint)
- `docs/architecture.md` -- system architecture overview
- `README.md` -- project readme
- Any OpenAPI spec files if they exist

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns.
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq)]
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

Follow derive macro conventions discovered from sibling model files (`summary.rs`, `details.rs`). Add documentation comments on the struct and each field.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module declaration:

```rust
pub mod severity_summary;
```

Place it alphabetically among existing module declarations to follow the established pattern.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService`, following the pattern of existing `fetch` and `list` methods:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with counts for critical, high, medium, and low
/// severities plus a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, read the severity field from AdvisorySummary
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find linked advisories
- Access the `severity` field from `AdvisorySummary` (`model/summary.rs`)
- Deduplicate by advisory ID to satisfy acceptance criterion
- Default all counts to 0 when no advisories exist at a given level
- Wrap errors with `.context()` matching `common/src/error.rs` pattern
- Return 404 (via `AppError`) when SBOM ID does not exist

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a JSON summary of advisory severity counts for the given SBOM,
/// with counts per severity level and a total.
pub async fn get_severity_summary(
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

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route in the router, following the existing registration pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Add the appropriate `use` or `mod` statement for the new handler module.

### 6.6 No changes needed for `server/src/main.rs`

The task description confirms routes auto-mount via module registration.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test functions, following conventions discovered from sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (seed test data with specific severity distribution)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 and the body contains correct counts
    // per severity level, with total matching the sum of individual counts
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 404
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains critical=0, high=0, medium=0, low=0, total=0
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory-SBOM links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate links to the same advisory

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once in the severity tally
}
```

All tests use `assert_eq!` on specific values (not just lengths), follow the `test_<endpoint>_<scenario>` naming convention, and include doc comments explaining what each test verifies.

Run tests:

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Test 1 validates response structure and values |
| Returns 404 for non-existent SBOM | Test 2 validates 404 response |
| Counts only unique advisories (deduplication) | Test 4 validates deduplication |
| All severity levels default to 0 | Test 3 validates all-zero response |
| Response time under 200ms for 500 advisories | Verify via test timing or manual check with seeded data |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files are in scope:

**Expected files:**
- `modules/fundamental/src/advisory/service/advisory.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/model/mod.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create) -- in scope
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create) -- in scope
- `tests/api/advisory_summary.rs` (create) -- in scope

If any out-of-scope files appear, list them and ask the user to approve.

### Untracked File Check

Run `git status --short` to detect untracked files (`??` prefix). Filter by proximity to modified directories. Check for code references (e.g., `include_str!`, `use`, import statements). Flag any referenced untracked files for user approval.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation Currency

Check if `docs/api.md` needs updating to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. If so, add the endpoint documentation.

### Documentation Scope Preservation

If docs were modified, verify replaced text still covers all original use cases.

### Duplication Check

Search the repository for existing severity aggregation, counting, or summary logic that could be reused. Use Grep/Serena to look for similar function names or patterns.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on any failure.

### Data-Flow Trace

Trace the complete data flow:
- **Input**: HTTP GET request with SBOM ID as path parameter
- **Processing**: Endpoint handler extracts ID -> calls `AdvisoryService.severity_summary()` -> service queries `sbom_advisory` join table -> deduplicates advisories -> counts by severity level
- **Output**: JSON response with `{ critical, high, medium, low, total }`

Verify all stages are connected: request parsing -> service call -> database query -> aggregation -> response serialization. Expected result: **COMPLETE**.

### Contract & Sibling Parity

- **Contract verification**: `SeveritySummary` struct implements `Serialize`/`Deserialize` as required by Axum's `Json` extractor
- **Sibling parity**: Compare the new endpoint against existing `get.rs` and `list.rs` handlers for error handling, logging, and configuration patterns
- **Cross-module shared entity**: The `sbom_advisory` join table is used by the ingestor module -- verify our query pattern matches

### Cross-Section Reference Consistency

Verify file paths are consistent across Files to Modify, Files to Create, and Implementation Notes. Check that `AdvisoryService` is referenced at `service/advisory.rs` consistently.

## Step 10 -- Commit and Push

Commit with Conventional Commits format:

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation service and endpoint

Add SeveritySummary response struct, AdvisoryService.severity_summary()
method, and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes integration tests for valid responses, 404 handling,
empty SBOMs, and deduplication.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main \
  --title "feat(advisory): add severity aggregation endpoint" \
  --body "## Summary

- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint that returns advisory severity counts per SBOM
- Add \`SeveritySummary\` response struct with critical, high, medium, low, and total counts
- Add \`severity_summary\` method to \`AdvisoryService\` using the \`sbom_advisory\` join table
- Add integration tests covering valid response, 404, empty SBOM, and deduplication scenarios

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [ ] Integration tests pass (\`cargo test\`)
- [ ] Endpoint returns correct severity counts for an SBOM with known advisories
- [ ] Endpoint returns 404 for a non-existent SBOM ID
- [ ] Endpoint returns all-zero counts for an SBOM with no advisories
- [ ] Duplicate advisory links are deduplicated in the count
- [ ] Response time is under 200ms for SBOMs with up to 500 advisories"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field**: Update `customfield_10875` on TC-9201 with the PR URL in ADF format (inlineCard)

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint with `SeveritySummary` response struct, `AdvisoryService.severity_summary()` method, and integration tests
   - No deviations from the plan
   - Comment ends with the skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition** TC-9201 to **In Review**: `jira.transition_issue("TC-9201", "In Review")`
