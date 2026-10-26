# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

The project CLAUDE.md (claude-md-mock.md) contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`)
3. **Code Intelligence** -- present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` with `rust-analyzer`

Configuration is valid. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes:** Follow existing patterns in `endpoints/get.rs`, `AdvisoryService`, use `sbom_advisory` join table, `AdvisorySummary.severity` field, register route in `endpoints/mod.rs`, return `AppError` with `.context()`, return struct directly for JSON serialization
- **Acceptance Criteria:** 5 criteria (200 response shape, 404 on missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements:** 4 tests (correct counts, 404, empty SBOM, deduplication)
- **Dependencies:** None
- **Target PR:** Not present (default flow)
- **Bookend Type:** Not present (default flow)
- **GitHub Issue:** Not extracted (field not populated)
- **Web URL:** Would be captured from `jira.get_issue` response (e.g., `https://redhat.atlassian.net/browse/TC-9201`)

All required sections are present. No gaps.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for full details.

**Result:** Digest match -- proceed silently. The stored digest comment (`sha256-md:a1b2c3d4e5f67890...`) matches the computed digest from the current description. The comment was not edited (created == updated). No user prompt or warning needed.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user's account ID.
2. Call `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign the task.
3. Call `jira.transition_issue(TC-9201)` to transition to "In Progress".

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using Serena instance `serena_backend` (tool prefix: `mcp__serena_backend__`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `get_symbols_overview` to see `AdvisoryService` struct and its methods (`fetch`, `list`, `search`)
   - `find_symbol("fetch", include_body=true)` to understand the method signature pattern (`&self, id: Id, tx: &Transactional<'_>`) and return type
   - This establishes the pattern for the new `severity_summary` method

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `get_symbols_overview` to see route registration pattern
   - Confirm `Router::new().route(...)` pattern for adding new routes

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - `get_symbols_overview` to see existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`)
   - Pattern for adding `pub mod severity_summary;`

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** (reference pattern)
   - `find_symbol` on the handler function to understand path extraction (`Path<Id>`), service invocation, JSON response pattern

### 4.2 Inspect Reference Files

5. **`modules/fundamental/src/advisory/model/summary.rs`**
   - `find_symbol("AdvisorySummary", include_body=true)` to understand the `severity` field type and structure

6. **`entity/src/sbom_advisory.rs`**
   - `get_symbols_overview` to understand the SBOM-Advisory join table structure for querying

7. **`common/src/error.rs`**
   - `find_symbol("AppError", include_body=true)` to understand error handling and `.context()` wrapping

### 4.3 Sibling Convention Analysis

Examine siblings for convention conformance:

- **Endpoint siblings:** `endpoints/get.rs`, `endpoints/list.rs` -- handler signature, extractor usage, error wrapping
- **Model siblings:** `model/summary.rs`, `model/details.rs` -- struct naming, derives (`Serialize`, `Deserialize`, `Debug`), field documentation
- **Service siblings:** `service/advisory.rs` methods -- parameter patterns, return types, transaction handling
- **Test siblings:** `tests/api/advisory.rs`, `tests/api/sbom.rs` -- test setup, assertion style, naming

Expected conventions:
- **Error handling:** `Result<T, AppError>` with `.context("description")`
- **Naming:** `verb_noun` for functions (e.g., `severity_summary`), PascalCase for types
- **Endpoint pattern:** `async fn handler(Path(id): Path<Id>, ...) -> Result<Json<T>, AppError>`
- **Test assertions:** `assert_eq!(resp.status(), StatusCode::OK)`, value-based assertions on response body
- **Derives:** `#[derive(Serialize, Deserialize, Debug, Clone)]` on response structs

### 4.4 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (path `./` from Registry). Read it if present and extract CI check commands for Step 9.

### 4.5 Documentation File Identification

- `docs/api.md` -- may need updating with new endpoint
- `docs/architecture.md` -- likely no change needed
- `README.md` -- likely no change needed

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for a given SBOM.
///
/// Aggregates unique advisories linked to an SBOM by their severity level,
/// providing counts for each level and a total count.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u64,
    /// Count of advisories with High severity.
    pub high: u64,
    /// Count of advisories with Medium severity.
    pub medium: u64,
    /// Count of advisories with Low severity.
    pub low: u64,
    /// Total count of unique advisories.
    pub total: u64,
}
```

Key decisions:
- Derive `Default` so all counts start at 0 (acceptance criterion: zero defaults)
- Use `u64` for counts (consistent with aggregation types)
- Documentation comments on struct and each field

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

```rust
/// Computes a severity summary for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table for advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts advisories per severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Deduplicate by advisory ID
    // For each unique advisory, fetch its severity from AdvisorySummary
    // Aggregate counts by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

Key implementation details:
- Follow the `fetch` method pattern for parameters and error handling
- Use `sbom_advisory` entity to find linked advisories
- Deduplicate by advisory ID (acceptance criterion)
- Use `.context("Failed to compute severity summary")` for error wrapping
- Return 404 via `AppError` if the SBOM ID does not exist (check SBOM existence first, matching existing SBOM endpoint behavior)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories by severity level
/// for the specified SBOM.
pub async fn severity_summary(
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

Key decisions:
- Follow `get.rs` handler pattern exactly
- Extract `Path<Id>` for the SBOM ID
- Return `Json<SeveritySummary>` directly (Axum handles serialization)
- Use `.context()` for error wrapping

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

Import the new module at the top of the file.

### 6.6 Documentation Impact

- Check `docs/api.md` for endpoint documentation -- add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with request/response format
- No changes needed to `server/src/main.rs` (routes auto-mount via module registration)

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that an SBOM with linked advisories of known severities returns
/// the correct count for each severity level.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with linked advisories at known severity levels
    // (e.g., 2 Critical, 1 High, 3 Medium, 0 Low)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And the response body contains exact severity counts:
    //   critical: 2, high: 1, medium: 3, low: 0, total: 6
    assert_eq!(resp.status(), StatusCode::OK);
    assert_eq!(body.critical, 2);
    assert_eq!(body.high, 1);
    assert_eq!(body.medium, 3);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 6);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting a severity summary for a non-existent SBOM ID
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a severity summary
/// where all counts are zero.
#[tokio::test]
async fn test_severity_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that when an SBOM has duplicate links to the same advisory,
/// the severity summary counts each advisory only once.
#[tokio::test]
async fn test_severity_summary_deduplicates() {
    // Given an SBOM with duplicate links to the same advisory
    // (e.g., same advisory linked twice, both Critical)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    assert_eq!(body.critical, 1);
    assert_eq!(body.total, 1);
}
```

Test conventions followed:
- Value-based assertions (not just length checks) -- per skill guidance
- Doc comments on every test function
- Given-when-then section comments for non-trivial tests
- `assert_eq!(resp.status(), StatusCode::OK)` pattern from siblings
- Test naming: `test_<feature>_<scenario>`

After writing tests, run: `cargo test -p fundamental` (or the appropriate crate name from `cargo metadata`).

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Test 1 validates exact field names and types |
| Returns 404 for non-existent SBOM | Test 2 validates 404 status |
| Counts only unique advisories (deduplicates) | Test 4 validates deduplication; implementation uses distinct advisory IDs |
| All severity levels default to 0 | Test 3 validates all-zero response; `SeveritySummary` derives `Default` |
| Response time under 200ms for 500 advisories | Ensured by efficient query (single JOIN + GROUP BY, no N+1); validated via test timing or load test |

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and compare against Files to Modify and Files to Create. Expected modified/created files:
- `modules/fundamental/src/advisory/service/advisory.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/model/mod.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create) -- in scope
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create) -- in scope
- `tests/api/advisory_summary.rs` (create) -- in scope

If `docs/api.md` was updated (documentation impact), flag as out-of-scope and ask user for approval.

### Untracked file check
Run `git status --short` and check for untracked files in modified directories.

### Dead parameter detection
No parameters are being removed -- this is additive code only.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency
Check `docs/api.md` -- if it documents existing endpoints, the new endpoint should be added (handled in Step 6.6).

### Duplication check
Search for existing severity aggregation logic (`search_for_pattern("severity_summary")`, `search_for_pattern("severity.*count")`) to ensure no duplication.

### CI checks from CONVENTIONS.md
Run any CI check commands extracted from `CONVENTIONS.md` in Step 4. Common Rust checks:
- `cargo fmt --check`
- `cargo clippy -- -D warnings`
- `cargo check`

### Module-level test requirement (Rust)
Run `cargo metadata --no-deps --format-version 1` to resolve crate names for modified files, then run:
- `cargo test -p <fundamental-crate-name>` (for service, model, endpoint files)
- `cargo test -p <test-crate-name>` (for integration tests, if separate)

### Data-flow trace
- **Input:** HTTP GET request with SBOM ID path parameter
- **Processing:** Path extraction -> AdvisoryService.severity_summary() -> query sbom_advisory join table -> deduplicate by advisory ID -> count by severity level -> build SeveritySummary
- **Output:** JSON response `{ critical, high, medium, low, total }` or 404 error
- All stages connected. Complete data flow.

### Contract and sibling parity
- **Contract:** Handler returns `Result<Json<SeveritySummary>, AppError>` -- consistent with Axum handler contract
- **Sibling parity:** Matches `get.rs` handler pattern (Path extraction, service call, JSON response, error wrapping)
- **Cross-module entity:** Uses `sbom_advisory` join table read-only -- no write conflicts
- **Caller-site:** Route registration follows existing pattern in `endpoints/mod.rs`

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to an
SBOM. Includes SeveritySummary model, AdvisoryService.severity_summary()
method, and integration tests covering correct counts, 404 handling,
empty results, and deduplication.

Implements TC-9201"

git push -u origin TC-9201
```

Then create a PR:
```bash
gh pr create --base main \
  --title "feat(advisory): add severity aggregation endpoint" \
  --body "## Summary
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint returning severity counts per level
- Add SeveritySummary response model and AdvisoryService.severity_summary() method
- Add integration tests for correct counts, 404, empty SBOM, and deduplication

Implements [TC-9201](<webUrl>)

## Test plan
- [ ] Verify endpoint returns correct severity counts for SBOM with known advisories
- [ ] Verify 404 for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no advisories
- [ ] Verify deduplication of advisory links"
```

Check for upstream remote first (fork detection) and adjust `gh pr create` flags accordingly.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added severity aggregation endpoint GET /api/v2/sbom/{id}/advisory-summary with SeveritySummary model, service method, and 4 integration tests
   - No deviations from plan
   - Comment ends with footnote per `shared/comment-footnote.md`

3. **Transition** TC-9201 to "In Review":
   ```
   jira.transition_issue(TC-9201) -> In Review
   ```
