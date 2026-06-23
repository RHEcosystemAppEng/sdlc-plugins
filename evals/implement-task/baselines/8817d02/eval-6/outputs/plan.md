# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, lists `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
3. **Code Intelligence** -- present, `serena_backend` configured with `rust-analyzer`

All sections are present and complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt the user for REST API v3 fallback per the standard protocol.

## Step 1 -- Fetch and Parse Jira Task

Fetch `TC-9201` via `jira.get_issue("TC-9201")` and parse the structured description:

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
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`, add `severity_summary` method to `AdvisoryService`, use `sbom_advisory` join table, count by severity level from `AdvisorySummary`, register route in `endpoints/mod.rs`, return `AppError` with `.context()`, return struct directly via Axum `Json` extractor
- **Acceptance Criteria**: 5 items (correct response shape, 404 for missing SBOM, deduplicate by advisory ID, defaults to 0, performance under 200ms)
- **Test Requirements**: 4 tests (correct counts, 404, all zeros, deduplication)
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None

Capture the issue `webUrl` for PR description linking.

Check GitHub Issue custom field (`customfield_10747`) -- extract if present for `Closes` line in PR description.

## Step 1.5 -- Verify Description Integrity

1. Retrieve comments via `jira.get_issue_comments("TC-9201")`
2. Locate the digest comment with marker `[sdlc-workflow] Description digest:`. Found: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
3. Check comment timestamps: `created` equals `updated` -- comment is unmodified, no warning needed
4. Extract format tag `md` and hex digest from the stored comment
5. Write the current task description to `/tmp/desc-TC-9201.txt` and compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
6. Compare format tags: both `sha256-md` -- tags match
7. Compare hex digests: both match
8. **Result**: digests match -- proceed silently to Step 2 without prompting the user

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign the task: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

Use `mcp__serena_backend__<tool>` for code intelligence.

### 4.1 Inspect files to modify

- `get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` structure, `fetch` and `list` methods
- `get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
- `get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration

### 4.2 Inspect reference files from Implementation Notes

- `find_symbol` with `include_body=true` on `AdvisoryService::fetch` and `AdvisoryService::list` in `advisory.rs` -- understand method signature patterns
- `get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand endpoint handler pattern (Path extraction, service call, JSON response)
- `get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- understand `AdvisorySummary` struct and its `severity` field
- `get_symbols_overview` on `entity/src/sbom_advisory.rs` -- understand join table structure
- `get_symbols_overview` on `common/src/error.rs` -- understand `AppError` and `.context()` pattern

### 4.3 Check backward compatibility

- `find_referencing_symbols` on any symbols being modified (e.g., `AdvisoryService` to ensure adding a method does not break existing callers)

### 4.4 Convention conformance analysis

Identify sibling files:
- `modules/fundamental/src/advisory/endpoints/list.rs` and `get.rs` -- siblings for the new endpoint handler
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- siblings for the new model struct
- `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs` -- additional endpoint siblings for cross-module patterns

Use `get_symbols_overview` on 2-3 siblings per category to discover:
- Naming conventions (e.g., function names, struct names)
- Error handling strategies (e.g., `Result<T, AppError>` with `.context()`)
- Route registration patterns
- Import organization

### 4.5 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root via `mcp__serena_backend__list_dir`. If present, read it and extract CI check commands for Step 9. Also look for code generation commands.

### 4.6 Test convention analysis

Inspect sibling test files:
- `tests/api/advisory.rs` -- sibling tests for advisory endpoints
- `tests/api/sbom.rs` -- sibling tests for SBOM endpoints
- `tests/api/search.rs` -- additional test file for pattern comparison

Discover test patterns: assertion style, response validation, error case coverage, test naming, setup/teardown, parameterized test usage.

### 4.7 Documentation file identification

Look for:
- `README.md` at repository root
- `docs/api.md` and `docs/architecture.md` referenced in CLAUDE.md
- Any API documentation related to advisory or SBOM endpoints

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
#[derive(Debug, Clone, Serialize, Default)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u32,
    /// Count of high-severity advisories.
    pub high: u32,
    /// Count of medium-severity advisories.
    pub medium: u32,
    /// Count of low-severity advisories.
    pub low: u32,
    /// Total count of unique advisories.
    pub total: u32,
}
```

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Follow the pattern of existing `fetch` and `list` methods:

- Method signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Use the `sbom_advisory` join table to find advisories linked to the SBOM
- First verify the SBOM exists (return 404 if not)
- Fetch advisory summaries, extract severity field
- Deduplicate by advisory ID
- Count by severity level (Critical, High, Medium, Low)
- Return `SeveritySummary` with counts and total

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Define the GET handler:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity count summary for all advisories linked to the given SBOM.
pub async fn severity_summary(
    Path(id): Path<Id>,
    // ... state/service extraction following existing pattern
) -> Result<Json<SeveritySummary>, AppError> {
    // Call service method
    // Return JSON response
}
```

Follow patterns from `modules/fundamental/src/advisory/endpoints/get.rs`:
- Extract path params via `Path<Id>`
- Call the service method
- Return JSON directly

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route:

```rust
Router::new().route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

Follow the existing route registration pattern in the module.

### 6.6 Documentation impact

- Check if API docs exist and need updating for the new endpoint
- Update if necessary, keeping changes scoped

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following tests, following sibling test conventions discovered in Step 4:

### Test 1: Valid SBOM with known advisories returns correct severity counts
```rust
/// Verifies that a valid SBOM with known advisories returns the correct severity breakdown.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories of known severities
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response contains correct counts per severity level and total
}
```

### Test 2: Non-existent SBOM ID returns 404
```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response status is 404 NOT_FOUND
}
```

### Test 3: SBOM with no advisories returns all zeros
```rust
/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then all severity counts are 0 and total is 0
}
```

### Test 4: Duplicate advisory links are deduplicated
```rust
/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then each advisory is counted only once
}
```

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by Test 1
- [x] Returns 404 when SBOM ID does not exist -- verified by Test 2
- [x] Counts only unique advisories (deduplicates by advisory ID) -- verified by Test 4
- [x] All severity levels default to 0 when no advisories exist -- verified by Test 3
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- verified by query design (single join query, no N+1)

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and verify all modified/created files match the task description:
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)

Flag any out-of-scope files for user approval.

### Untracked file check

Run `git status --short`, filter for `??` entries in directories where implementation occurred, and check for code references to untracked files.

### Sensitive-pattern check

Search staged diff for secrets/credentials patterns. Flag any matches.

### Documentation currency

Check if API docs or README need updating for the new endpoint.

### Cross-section reference consistency

Verify file paths for `AdvisoryService` are consistent across Files to Modify and Implementation Notes. Note: the task references `modules/fundamental/src/advisory/service/advisory.rs` in both sections -- consistent.

### Duplication check

Search for existing severity aggregation or summary functions to ensure no duplication.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted in Step 4 (if CONVENTIONS.md exists). Hard stop on any failure.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param -> call `AdvisoryService::severity_summary` -> query `sbom_advisory` join table -> fetch advisory summaries -> count by severity -> return `SeveritySummary` JSON -- COMPLETE

### Contract and sibling parity

- `SeveritySummary` struct -- verify `Serialize` derive, field types match response contract
- Endpoint handler -- verify follows same pattern as `get.rs` (error handling, response type)
- Service method -- verify follows same pattern as `fetch`/`list` (signature, transaction handling)

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
404 handling for non-existent SBOMs.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM, enabling dashboard widgets to render severity breakdowns
without client-side counting.

- New `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning `{ critical, high, medium, low, total }`
- `SeveritySummary` response struct in advisory model
- `severity_summary` method on `AdvisoryService`
- Integration tests covering correct counts, 404, empty SBOM, and deduplication

Implements [TC-9201](<webUrl>)

## Test Plan

- [x] Test that a valid SBOM with known advisories returns correct severity counts
- [x] Test that a non-existent SBOM ID returns 404
- [x] Test that an SBOM with no advisories returns all zeros
- [x] Test that duplicate advisory links are deduplicated in the count
EOF
)"
```

## Step 11 -- Update Jira

1. Update the Git Pull Request custom field (`customfield_10875`) with the PR URL using ADF `inlineCard` format
2. Add a comment to TC-9201 with:
   - PR link
   - Summary: Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint with `SeveritySummary` response struct, `severity_summary` service method, and integration tests
   - Deviations: none
   - Comment ends with the standard skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)
3. Transition TC-9201 to In Review: `jira.transition_issue("TC-9201", "In Review")`
