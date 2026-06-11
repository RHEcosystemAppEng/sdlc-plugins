# Implementation Plan — TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

---

## Step 0 — Validate Project Configuration

Verify CLAUDE.md contains the required sections:

- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present with Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: present with `serena_backend` instance using `rust-analyzer`

All sections valid. Proceed.

## Step 1 — Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue(TC-9201)`. Parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs` |
| Files to Create | `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Dependencies | None |
| Target PR | Not present |
| Bookend Type | Not present |

Capture the issue `webUrl` for PR description linking.

Check GitHub Issue custom field (`customfield_10747`) — extract owner/repo/number if present.

## Step 1.5 — Verify Description Integrity

Fetch issue comments. Locate the digest comment by searching for the marker `[sdlc-workflow] Description digest:`. One comment found:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

- Comment `created` equals `updated` — not edited after posting.
- Stored tag: `sha256-md`, computed tag: `sha256-md` — tags match.
- Stored hex matches computed hex — **digests match**.
- **Proceed silently** to Step 2 with no user prompt.

## Step 2 — Verify Dependencies

Task has no dependencies listed. Proceed.

## Step 3 — Transition to In Progress and Assign

1. Retrieve current user via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<accountId>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 — Understand the Code

### 4.1 Inspect files to modify

Using `mcp__serena_backend__<tool>`:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** — `get_symbols_overview` to see the AdvisoryService struct, its `fetch` and `list` methods. Then `find_symbol` with `include_body=true` on `list` to understand the query pattern (takes `&self`, SBOM-related params, `tx: &Transactional<'_>`).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — `get_symbols_overview` to see route registration patterns. Examine how existing routes are registered (`Router::new().route("/path", get(handler))`).

3. **`modules/fundamental/src/advisory/model/mod.rs`** — `get_symbols_overview` to see existing module declarations (`pub mod summary;`, `pub mod details;`).

### 4.2 Inspect reference files for patterns

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — `find_symbol` on the handler function to understand path parameter extraction (`Path<Id>`), service invocation, and JSON response pattern.

2. **`modules/fundamental/src/advisory/model/summary.rs`** — `find_symbol` on `AdvisorySummary` to understand the struct shape and see the `severity` field used for counting.

3. **`entity/src/sbom_advisory.rs`** — `get_symbols_overview` to understand the SBOM-Advisory join table structure.

4. **`common/src/error.rs`** — `find_symbol` on `AppError` to understand error handling pattern and `.context()` wrapping.

### 4.3 Convention conformance analysis

Identify sibling files for pattern analysis:

- **Endpoint siblings**: `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs` — examine patterns for handler signatures, error handling, response types.
- **Model siblings**: `advisory/model/summary.rs`, `advisory/model/details.rs` — examine derive macros, field types, serde configuration.
- **Service siblings**: `advisory/service/advisory.rs` existing methods — examine method signatures, transaction handling, query building.

**Expected conventions:**
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: service methods follow `verb_noun` pattern
- Endpoint handlers: extract path params via `Path<Id>`, call service, return `Json<T>`
- Structs: derive `Serialize, Deserialize, Debug, Clone`

### 4.4 Test convention analysis

Inspect sibling test files:
- `tests/api/advisory.rs` — assertion style, test naming, setup/teardown patterns
- `tests/api/sbom.rs` — response shape validation, error case coverage

**Expected test conventions:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Real PostgreSQL test database
- Test naming: `test_<endpoint>_<scenario>`

### 4.5 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read and extract CI check commands for Step 9. If absent, proceed normally.

### 4.6 Documentation file identification

Check for:
- `docs/api.md` — API documentation that may need updating with the new endpoint
- `README.md` — may reference API capabilities
- `docs/architecture.md` — likely no changes needed

### 4.7 Backward compatibility check

Use `find_referencing_symbols` on any symbols being modified (e.g., if modifying `AdvisoryService` struct definition) to ensure changes do not break existing callers.

## Step 5 — Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 — Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM, enabling dashboard
/// widgets to render severity breakdowns without client-side counting.
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
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}
```

Derive `Default` so all fields initialize to 0 when no advisories exist.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module declaration:

```rust
pub mod severity_summary;
```

### 6.3 Add `severity_summary` method to `modules/fundamental/src/advisory/service/advisory.rs`

Add a method to `AdvisoryService` following the existing `fetch`/`list` pattern:

```rust
/// Computes severity counts for all unique advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query the sbom_advisory join table to find advisories linked to this SBOM
    // Join with advisory table to get severity
    // Deduplicate by advisory ID
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` join table (from `entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- Use `AdvisorySummary.severity` field to categorize
- Deduplicate by advisory ID to count only unique advisories
- Return 404 (`AppError` with context) when the SBOM ID does not exist, consistent with existing SBOM endpoints

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `advisory/endpoints/get.rs`:

```rust
use axum::{extract::Path, Json};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all unique advisories linked to the
/// specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transactional context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following existing patterns:

```rust
mod severity_summary;

// In the router function, add:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation impact

Review `docs/api.md` and update with the new endpoint:
- `GET /api/v2/sbom/{id}/advisory-summary` — returns `{ critical: N, high: N, medium: N, low: N, total: N }`

### 6.7 Code quality checks

- All new structs and public functions have documentation comments
- Error handling uses `Result<T, AppError>` with `.context()` wrapping
- Response type uses `Json<SeveritySummary>` for Axum serialization

## Step 7 — Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases, following conventions from sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns the correct
/// severity breakdown per level and a correct total count.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM linked to advisories with known severity levels
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then response status is 200 OK
    // Then response body contains correct counts per severity level
    // Then total equals sum of all severity counts
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns HTTP 404, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then response status is 404 NOT_FOUND
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary with
/// all severity counts at zero and a total of zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then response body has critical=0, high=0, medium=0, low=0, total=0
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links to the same SBOM are deduplicated
/// in the severity count, preventing inflated totals.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then counts reflect unique advisories only (duplicates not double-counted)
}
```

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 — Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Validated by test 1 — response contains critical, high, medium, low, total fields |
| Returns 404 for non-existent SBOM | Validated by test 2 |
| Counts only unique advisories | Validated by test 4 — deduplication by advisory ID |
| All severity levels default to 0 | Validated by test 3 — SBOM with no advisories returns zeros |
| Response time under 200ms for up to 500 advisories | Verified by query design — single database query with GROUP BY, no N+1 |

## Step 9 — Self-Verification

### Scope containment

Run `git diff --name-only` and verify all changed files are within scope:

**Expected files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` (created)
- `modules/fundamental/src/advisory/model/mod.rs` (modified)
- `modules/fundamental/src/advisory/service/advisory.rs` (modified)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (created)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified)
- `tests/api/advisory_summary.rs` (created)

Flag any out-of-scope files for user approval.

### Untracked file check

Run `git status --short`, filter for `??` entries. Check proximity to modified directories and search for code references to any untracked files.

### Sensitive-pattern check

Search staged diff for secrets: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`

### Documentation currency

Check if `docs/api.md` needs updating with the new endpoint (if not already done in Step 6).

### Duplication check

Search for existing severity counting or aggregation logic in the repository that could be reused.

### CI checks from CONVENTIONS.md

Run any CI check commands extracted in Step 4. Hard stop on any non-zero exit.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param -> call `AdvisoryService.severity_summary()` -> query `sbom_advisory` join table -> aggregate by severity -> return `Json<SeveritySummary>` — **COMPLETE**

### Contract & sibling parity

- `SeveritySummary` struct: standalone struct, no trait implementation needed
- Sibling parity with `get.rs` handler: error handling pattern, path extraction, JSON response — verify consistency
- Caller-site parity: new endpoint, no existing callers to compare

## Step 10 — Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService.severity_summary() method, and
GET /api/v2/sbom/{id}/advisory-summary endpoint that returns per-severity
counts (critical, high, medium, low) with a total. Includes integration tests
for valid SBOM, missing SBOM (404), empty advisory list, and deduplication.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

- Add \`SeveritySummary\` response struct in \`advisory/model/severity_summary.rs\`
- Add \`severity_summary()\` method to \`AdvisoryService\` that queries the \`sbom_advisory\` join table and aggregates by severity level
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint returning \`{ critical, high, medium, low, total }\`
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](<webUrl>)
"
```

## Step 11 — Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL using ADF inlineCard format
2. Add comment to TC-9201 with PR link, summary of changes, and note of no deviations from plan
3. Transition TC-9201 to "In Review"
