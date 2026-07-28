# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verified from the project's CLAUDE.md:

1. **Repository Registry** -- present: trustify-backend, Serena Instance: serena_backend, Path: ./
2. **Jira Configuration** -- present: Project key (TC), Cloud ID, Feature issue type ID (10142), Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
3. **Code Intelligence** -- present: tool naming convention `mcp__<serena-instance>__<tool>`, instance serena_backend with rust-analyzer

All required sections exist. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt the user for REST API fallback.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`.

Parsed fields:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed (routes auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`, use `Path<Id>` extractor, call service, return JSON. Use `sbom_advisory` join table. Use `AdvisorySummary.severity` field. Return `AppError` with `.context()`. Return struct directly via Axum's `Json`.
- **Acceptance Criteria**: 5 items (correct JSON shape, 404 for missing SBOM, deduplication by advisory ID, default zeros, response time < 200ms)
- **Test Requirements**: 4 tests (valid SBOM counts, 404, no advisories, deduplication)
- **Target PR**: not present (standard flow)
- **Bookend Type**: not present (standard flow)
- **Dependencies**: None

Capture `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for PR description.

Check GitHub Issue custom field (customfield_10747) -- extract reference if present.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the full procedure. Summary:

1. Fetch comments on TC-9201.
2. Locate digest comment starting with `[sdlc-workflow] Description digest:`.
3. Comment found: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
4. Comment `created` equals `updated` -- not edited, no warning needed.
5. Format tag is `sha256-md` (not legacy untagged format) -- no legacy warning.
6. Compute current digest with `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`.
7. Compare format tags: both `sha256-md` -- tags match.
8. Compare hex digests: match confirmed.
9. **Outcome**: Proceed silently. Description integrity verified.

## Step 2 -- Verify Dependencies

Dependencies: None. No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID: `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use `mcp__serena_backend__get_symbols_overview` on:

- `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` structure, existing `fetch` and `list` methods
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
- `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration pattern

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:

- `AdvisoryService::fetch` and `AdvisoryService::list` -- understand method signature pattern (parameters, return type, transaction handling)
- Existing endpoint handler in `modules/fundamental/src/advisory/endpoints/get.rs` -- understand `Path<Id>` extraction, service call, JSON response pattern

### 4.2 Inspect reference files

- `entity/src/sbom_advisory.rs` -- understand the join table structure for SBOM-advisory relationships
- `modules/fundamental/src/advisory/model/summary.rs` -- understand `AdvisorySummary` struct, specifically the `severity` field
- `common/src/error.rs` -- understand `AppError` enum and `.context()` wrapping pattern
- `modules/fundamental/src/sbom/endpoints/get.rs` -- understand 404 handling for non-existent SBOMs (reference for consistent error behavior)

### 4.3 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to confirm adding a new method won't break existing callers.

### 4.4 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root. If present, read it and extract CI check commands. If not present, proceed normally.

### 4.5 Convention conformance analysis

**Identify siblings and examine patterns:**

- **Endpoint siblings**: `endpoints/get.rs`, `endpoints/list.rs` in the advisory module
  - Extract path params via `Path<Id>`
  - Call service method
  - Return `Result<Json<T>, AppError>`
  - Error wrapping with `.context()`
- **Service method siblings**: `AdvisoryService::fetch`, `AdvisoryService::list`
  - Method signature pattern: `&self, id: Id, tx: &Transactional<'_>`
  - Return `Result<T, AppError>`
- **Model siblings**: `summary.rs`, `details.rs` in advisory/model
  - Derive macros: `#[derive(Serialize, Deserialize, Debug, Clone)]` (typical for Axum response types)
  - Field naming and structure

### 4.6 Test convention analysis

**Identify sibling test files**: `tests/api/advisory.rs`, `tests/api/sbom.rs`

Examine patterns:
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Response validation: check specific field values, not just collection lengths
- Error cases: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Test naming: `test_<endpoint>_<scenario>` pattern
- Setup: test database seeding, test SBOM/advisory creation fixtures

### 4.7 Documentation file identification

Identify documentation files:
- `README.md` at repository root
- `docs/api.md` (API reference from CLAUDE.md)
- `docs/architecture.md` (architecture overview)

Record for documentation impact evaluation in Step 6.

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file: `SeveritySummary` response struct.

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Provides a breakdown of advisory counts by severity level,
/// enabling dashboard widgets to render severity distributions
/// without client-side counting.
#[derive(Serialize, Deserialize, Debug, Clone, Default)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u64,
    /// Count of advisories with High severity.
    pub high: u64,
    /// Count of advisories with Medium severity.
    pub medium: u64,
    /// Count of advisories with Low severity.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}
```

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the existing module registration pattern.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Following the pattern of `fetch` and `list` methods:

```rust
/// Computes aggregated severity counts for all advisories linked to the given SBOM.
///
/// Deduplicates advisories by advisory ID before counting. Returns a
/// `SeveritySummary` with counts per severity level and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to sbom_id
    // 2. Deduplicate by advisory ID (use DISTINCT or HashSet)
    // 3. For each unique advisory, fetch its AdvisorySummary and read the severity field
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Return SeveritySummary with counts and total
    // Error handling: wrap with .context("Failed to compute severity summary for SBOM")
}
```

Key implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- Deduplicate by advisory ID before counting (acceptance criterion: unique advisories only)
- Use `AdvisorySummary.severity` field to categorize counts
- All severity levels default to 0 (struct derives `Default`)
- Wrap errors with `.context()` matching `common/src/error.rs` pattern

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
/// Returns 404 if the SBOM ID does not exist.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transaction */,
) -> Result<Json<SeveritySummary>, AppError> {
    // 1. Verify SBOM exists (return 404 if not, consistent with existing SBOM endpoints)
    // 2. Call service.severity_summary(id, &tx).await.context("...")
    // 3. Return Json(summary)
}
```

### 6.5 Register the new route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add route registration following the existing `Router::new().route("/path", get(handler))` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation impact

- Update `docs/api.md` if it documents REST endpoints, adding the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with request/response schemas.
- No changes needed to `server/src/main.rs` (routes auto-mount via module registration).

### 6.7 Code quality verification

- Every new struct (`SeveritySummary`) has documentation comments
- Every new public function (`severity_summary`, `get_severity_summary`) has documentation comments
- One-line descriptions explain what each symbol is and what it's for

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following tests, following sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories of known severities (e.g., 2 Critical, 1 High, 0 Medium, 3 Low)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And the response body contains { critical: 2, high: 1, medium: 0, low: 3, total: 6 }
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that a non-existent SBOM ID returns a 404 status code.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{non-existent-id}/advisory-summary

    // Then the response status is 404 NOT_FOUND
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And the response body contains { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
}
```

### Test 4: Duplicate advisory links are deduplicated in the count

```rust
/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And the total count reflects unique advisories only (not duplicated counts)
}
```

All tests use `assert_eq!(resp.status(), StatusCode::OK)` / `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` pattern from sibling test files. Tests assert on specific field values, not just counts.

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Verified by test_advisory_summary_valid_sbom |
| Returns 404 for non-existent SBOM ID | Verified by test_advisory_summary_not_found |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by test_advisory_summary_deduplication |
| All severity levels default to 0 when no advisories exist | Verified by test_advisory_summary_no_advisories |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by implementation approach (single query with GROUP BY, no N+1 queries) |

## Step 9 -- Self-Verification

### 9.1 Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create.

Expected modified files:
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

Expected created files:
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

If any out-of-scope files appear (e.g., `docs/api.md` from documentation impact), flag and ask for user approval.

### 9.2 Untracked file check

Run `git status --short`, extract `??` entries. Filter by proximity to directories containing modified files. Search for code references to untracked files (e.g., `include_str!`, imports). Flag any referenced untracked files for user confirmation.

### 9.3 Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to scan for secrets.

### 9.4 Documentation currency

Check if `docs/api.md` describes the advisory endpoints and needs updating with the new `/api/v2/sbom/{id}/advisory-summary` endpoint.

### 9.5 Cross-section reference consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` referenced in Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent.
- `AdvisorySummary` referenced in Implementation Notes (`advisory/model/summary.rs`) -- this is a read-only reference, not a file being modified -- consistent.

### 9.6 Duplication check

Search the repository for existing severity aggregation or counting logic using Grep/Serena. Confirm no existing utility already provides this functionality.

### 9.7 CI checks from CONVENTIONS.md

Run any CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on any failure.

### 9.8 Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary`:
  - Input: HTTP request with SBOM ID path parameter
  - Processing: endpoint handler extracts path param -> calls `AdvisoryService::severity_summary` -> queries `sbom_advisory` join table -> fetches advisory severities -> deduplicates -> counts by level
  - Output: JSON response with `SeveritySummary` struct
  - **COMPLETE** -- all stages connected

### 9.9 Contract and sibling parity

- `SeveritySummary` -- standalone struct, no trait/interface contract to implement
- Sibling parity with `get.rs` endpoint: Path extraction, service call, Json response, AppError error handling -- all present
- Sibling parity with `AdvisoryService::fetch`/`list`: same signature pattern (`&self, id, tx`) -- consistent

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
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes deduplication by advisory
ID and proper 404 handling for non-existent SBOMs.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
```

Check for fork (upstream remote). Then create PR:

```bash
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint returning aggregated severity counts
- Add \`SeveritySummary\` response model with critical, high, medium, low, and total fields
- Add \`AdvisoryService::severity_summary\` method with deduplication by advisory ID
- Add integration tests covering valid SBOM, 404, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test Plan

- [x] Valid SBOM with known advisories returns correct severity counts
- [x] Non-existent SBOM ID returns 404
- [x] SBOM with no advisories returns all zeros
- [x] Duplicate advisory links are deduplicated in the count"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (customfield_10875) with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with PR link, summary of changes, and any deviations from the plan. Include the skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`).

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue("TC-9201") -> In Review
```
