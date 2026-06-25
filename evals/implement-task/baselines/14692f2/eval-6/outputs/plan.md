# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:
- **Repository Registry**: Present -- `trustify-backend` mapped to `serena_backend` at path `./`
- **Jira Configuration**: Present -- Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
- **Code Intelligence**: Present -- `serena_backend` instance with `rust-analyzer`

All sections present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all Jira operations. If MCP fails, prompt the user for REST API fallback. Record the access method for consistent use throughout the skill.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add severity aggregation service and REST endpoint for SBOM advisory severity counts |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Target PR | Not present |
| Bookend Type | Not present |
| Dependencies | None |

Capture `webUrl` from the issue response for PR description linking.

Check GitHub Issue custom field (`customfield_10747`) -- extract the GitHub issue reference if present. Store as `<owner>/<repo>#<number>` for PR description.

## Step 1.5 -- Verify Description Integrity

(Detailed in `outputs/digest-match.md`)

1. Fetch comments via `jira.get_issue_comments("TC-9201")`.
2. Locate the digest comment matching marker `[sdlc-workflow] Description digest:`.
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Check comment edit timestamps: `created` == `updated` -- not edited, no warning.
5. Extract stored digest: format tag = `md`, hex = `a1b2c3d4e5f67890...`.
6. Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`.
7. Compare format tags: both `sha256-md` -- tags match.
8. Compare hex digests: **match** -- description unmodified since planning.
9. **Outcome**: Proceed silently. No user prompt needed.

## Step 2 -- Verify Dependencies

Task has no dependencies (`Dependencies: None`). Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Get current user's account ID: `jira.user_info()`
2. Assign task: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition: `jira.transition_issue("TC-9201")` to "In Progress"

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Using `mcp__serena_backend__<tool>`:

- **`modules/fundamental/src/advisory/service/advisory.rs`**: Use `get_symbols_overview` to understand `AdvisoryService` structure. Use `find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand their pattern (parameters, return type, error handling, transactional context).

- **`modules/fundamental/src/advisory/endpoints/mod.rs`**: Use `get_symbols_overview` to see current route registrations. Understand the `Router::new().route()` pattern used for existing endpoints.

- **`modules/fundamental/src/advisory/model/mod.rs`**: Use `get_symbols_overview` to see existing `pub mod` declarations for the model submodules.

### 4.2 Inspect reference files for patterns

- **`modules/fundamental/src/advisory/endpoints/get.rs`**: Inspect the existing GET handler pattern -- path parameter extraction via `Path<Id>`, service invocation, JSON response, error handling with `AppError` and `.context()`.

- **`modules/fundamental/src/advisory/model/summary.rs`**: Inspect the `AdvisorySummary` struct, especially the `severity` field that will be used for counting.

- **`entity/src/sbom_advisory.rs`**: Inspect the join table entity to understand how SBOMs link to advisories.

- **`common/src/error.rs`**: Inspect `AppError` enum and its `IntoResponse` implementation to understand error patterns.

### 4.3 Convention conformance analysis

Identify sibling files for each file being modified/created:

- **Endpoint siblings**: `endpoints/get.rs`, `endpoints/list.rs` -- examine handler signatures, error wrapping, response types.
- **Model siblings**: `model/summary.rs`, `model/details.rs` -- examine struct patterns, derive macros, serialization attributes.
- **Service siblings**: `service/advisory.rs` existing methods -- examine method signatures, transactional patterns, query patterns.
- **SBOM endpoint siblings**: `modules/fundamental/src/sbom/endpoints/get.rs`, `list.rs` -- compare cross-module endpoint patterns.

Record discovered conventions:
- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Response types**: Single-resource endpoints return the struct directly via `Json<T>`; list endpoints return `PaginatedResults<T>`
- **Route registration**: `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`
- **Path params**: Extracted via `Path<Id>` extractor
- **Transactions**: Service methods take `&Transactional<'_>` as final parameter

### 4.4 Test convention analysis

Inspect sibling test files:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Record test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases**: Tests include 404 cases with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: Tests hit a real PostgreSQL test database
- **Parameterized tests**: Check if sibling tests use `#[rstest]` -- if not, do not introduce

### 4.5 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root (`./CONVENTIONS.md`). If present, read and extract:
- CI check commands for Step 9
- Code generation commands
- Project-specific conventions

### 4.6 Documentation file identification

Identify related documentation files:
- `docs/api.md` -- API reference (may need update for new endpoint)
- `docs/architecture.md` -- architecture overview
- `README.md` -- project readme

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
use serde::Serialize;
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Provides aggregated counts of advisories grouped by severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, ToSchema)]
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
```

Follow existing model patterns from `summary.rs` and `details.rs` for derive macros and attribute usage.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module registration:

```rust
pub mod severity_summary;
```

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService`, following the same pattern as `fetch` and `list`:

```rust
/// Computes aggregated severity counts for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// specified SBOM, deduplicates by advisory ID, and counts per severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to sbom_id
    // 2. Join with advisory table to get severity field
    // 3. Deduplicate by advisory ID
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Return SeveritySummary with counts and total
    // Use .context("Fetching severity summary") for error wrapping
}
```

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New file: GET handler for `/api/v2/sbom/{id}/advisory-summary`.

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    // 1. Verify SBOM exists (return 404 if not)
    // 2. Call service.severity_summary(id, &tx)
    // 3. Return Json(summary)
    // Use .context() for error wrapping, matching get.rs pattern
}
```

Follow the pattern in `endpoints/get.rs` for path parameter extraction, service invocation, and response handling.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route in the router:

```rust
use severity_summary::get_severity_summary;

// Add to existing Router::new() chain:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### 6.6 Verify `server/src/main.rs`

Per task description: no changes needed -- routes auto-mount via module registration.

### 6.7 Documentation impact

- Check `docs/api.md` for API reference -- add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation.
- No architectural changes, so `docs/architecture.md` does not need updating.

## Step 7 -- Write Tests

### 7.1 Create `tests/api/advisory_summary.rs`

Integration tests following sibling test patterns:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with known advisories at various severity levels
    // (seed test database with SBOM and linked advisories)

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct severity counts
    // assert_eq!(resp.status(), StatusCode::OK)
    // Deserialize body and assert specific counts per severity level
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary endpoint

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no advisories returns all-zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary endpoint

    // Then all severity counts are 0 and total is 0
    // assert_eq!(summary.critical, 0)
    // assert_eq!(summary.high, 0)
    // assert_eq!(summary.medium, 0)
    // assert_eq!(summary.low, 0)
    // assert_eq!(summary.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary endpoint

    // Then the advisory is counted only once
    // Verify total reflects unique count, not duplicate count
}
```

Every test function has a doc comment. Non-trivial tests use given-when-then section comments. Assertion style follows sibling tests (`assert_eq!` on status code, then body deserialization with value-based assertions).

### 7.2 Run tests

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding. If the same test fails 3 times with the same error, stop and ask the user for guidance.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by `test_advisory_summary_with_known_advisories` |
| Returns 404 for non-existent SBOM ID | Verified by `test_advisory_summary_not_found` |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_advisory_summary_deduplication` |
| All severity levels default to 0 when no advisories exist | Verified by `test_advisory_summary_empty` |
| Response time under 200ms for up to 500 advisories | Verified by inspection of query pattern (single JOIN + GROUP BY, no N+1); performance testing recommended for production validation |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against expected files:

**Files to Modify**:
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create**:
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Any out-of-scope modifications (e.g., doc updates to `docs/api.md`) are flagged for user approval.

### Untracked file check

Run `git status --short` and check for `??` entries in directories where implementation work occurred. Flag any untracked files referenced by code (e.g., via `include_str!`).

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Verify no secrets are staged.

### Documentation currency

Check if `docs/api.md` needs updating for the new endpoint. If it was not already updated in Step 6, update it now.

### Duplication check

Search for existing severity aggregation or summary functions in the codebase to ensure no duplication.

### CI checks from CONVENTIONS.md

Run any CI check commands extracted from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`, `cargo build`). Hard stop on any failure.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> join `advisory` table -> deduplicate by ID -> count by severity -> return `SeveritySummary` as JSON -- **COMPLETE**

### Contract & sibling parity

- `SeveritySummary` struct: no trait/interface to implement beyond `Serialize` -- contract satisfied.
- Sibling parity with `get.rs` handler: error handling pattern, path extraction, service call pattern -- verify match.
- Cross-module shared entity analysis: `sbom_advisory` join table is read-only in this task (SELECT/query only) -- no mutation patterns to verify against.

### Cross-section reference consistency

- `AdvisoryService` referenced in both "Files to Modify" (`service/advisory.rs`) and "Implementation Notes" (`service/advisory.rs`) -- consistent.
- All file paths consistent across sections.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add SeveritySummary model, AdvisoryService.severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated advisory severity counts (critical, high, medium, low, total)
for a given SBOM. Includes integration tests for happy path, 404,
empty SBOM, and deduplication scenarios.

Implements TC-9201"

git push -u origin TC-9201
```

Create PR:

```bash
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory
severity counts for a given SBOM, enabling dashboard widgets to render severity
breakdowns without client-side counting.

- New `SeveritySummary` response model with critical/high/medium/low/total counts
- New `AdvisoryService::severity_summary()` method querying the sbom_advisory join table
- New `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- Integration tests covering happy path, 404, empty SBOM, and deduplication

Implements [TC-9201](<webUrl>)

## Test Plan

- [ ] `cargo test --test advisory_summary` passes
- [ ] Manual verification: GET /api/v2/sbom/{valid-id}/advisory-summary returns correct counts
- [ ] Manual verification: GET /api/v2/sbom/{invalid-id}/advisory-summary returns 404
- [ ] CI pipeline passes (fmt, clippy, build, tests)
EOF
)"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF inlineCard format.

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: Added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
   - No deviations from the plan
   - Include footnote with plugin version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`

3. **Transition** TC-9201 to "In Review" via `jira.transition_issue`.
