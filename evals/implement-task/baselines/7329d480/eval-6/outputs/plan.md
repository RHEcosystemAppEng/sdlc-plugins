# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main

---

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections under `# Project Configuration`:

- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
- **Jira Configuration**: present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`)
- **Code Intelligence**: present, with tool naming convention and configured instance `serena_backend` using `rust-analyzer`

Validation passes. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. Fall back to REST API via `scripts/jira-client.py` if MCP fails, prompting the user for their preference.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add severity aggregation service method and REST endpoint for SBOM advisory severity counts |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs`, `server/src/main.rs` (no changes needed) |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Target PR | None |
| Bookend Type | None |
| Dependencies | None |
| GitHub Issue custom field | Check `customfield_10747` on the fetched issue; extract reference if present |

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for the PR description.

All required sections are present. Proceeding.

## Step 1.5 -- Verify Description Integrity

Fetch comments via `jira.get_issue_comments("TC-9201")`. Locate the comment whose body starts with the marker string `[sdlc-workflow] Description digest:` as defined in `shared/description-digest-protocol.md`.

Found digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

- Comment `created` and `updated` timestamps are identical -- comment was not edited.
- Extracted format tag: `sha256-md`. Extracted hex digest: `a1b2c3d4e5f67890...`
- Computed current description digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` -- output: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tags match (both `sha256-md`). Hex digests match.

Digests match. Proceeding silently.

## Step 2 -- Verify Dependencies

TC-9201 has no dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition TC-9201 to In Progress via `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

### 4.1 Inspect existing files using Serena (`mcp__serena_backend__<tool>`)

**Files to Modify:**

- `modules/fundamental/src/advisory/service/advisory.rs` -- use `get_symbols_overview` to see `AdvisoryService` structure, then `find_symbol` with `include_body=true` on `fetch` and `list` methods to understand the pattern for the new `severity_summary` method.
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- use `get_symbols_overview` to see current route registrations and the pattern for adding a new route.
- `modules/fundamental/src/advisory/model/mod.rs` -- use `get_symbols_overview` to see existing module declarations (e.g., `pub mod summary;`, `pub mod details;`) to understand the pattern for adding `pub mod severity_summary;`.

**Files for reference:**

- `modules/fundamental/src/advisory/endpoints/get.rs` -- use `find_symbol` to read the GET handler pattern (Path extraction, service call, JSON response).
- `modules/fundamental/src/advisory/model/summary.rs` -- use `find_symbol` on `AdvisorySummary` to understand the `severity` field type and structure.
- `entity/src/sbom_advisory.rs` -- use `get_symbols_overview` to understand the join table entity for SBOM-advisory relationships.
- `common/src/error.rs` -- use `find_symbol` on `AppError` to understand error handling patterns.

### 4.2 Convention conformance analysis (sibling analysis)

**Production code siblings:**

- Inspect `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` to identify endpoint handler patterns.
- Inspect `modules/fundamental/src/sbom/service/sbom.rs` to compare service method patterns against `advisory.rs`.
- Inspect `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/advisory/model/summary.rs` to understand response struct conventions.

**Expected discovered conventions:**
- **Error handling**: all handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming**: service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern**: extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Route registration**: `Router::new().route("/path", get(handler))` pattern
- **Response structs**: derive `Serialize, Deserialize, Debug, Clone` with `#[serde(rename_all = "camelCase")]`

### 4.3 Test convention analysis

**Sibling test files:**

- `tests/api/sbom.rs` -- inspect for assertion patterns, test naming, setup/teardown
- `tests/api/advisory.rs` -- inspect for endpoint test patterns, 404 handling tests

**Expected discovered test conventions:**
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: validate key fields from deserialized response body
- **Error cases**: include 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: tests use a shared test database context with fixture data

### 4.4 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read it and extract:
- CI check commands for Step 9 verification
- Code generation commands
- Additional naming or structural conventions

### 4.5 Documentation file identification

Identify documentation files related to the changes:
- `docs/api.md` -- REST API reference (may need update for new endpoint)
- `docs/architecture.md` -- system architecture overview
- `README.md` -- project overview

### 4.6 Check backward compatibility

Use `find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure the new `severity_summary` method does not conflict with existing methods. The new method is additive, so no breaking changes are expected.

## Step 5 -- Create Branch

No Target PR and no Bookend Type. Create a new branch from the target branch:

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
#[derive(Serialize, Deserialize, Debug, Clone, Default)]
#[serde(rename_all = "camelCase")]
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

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method following the pattern of existing `fetch` and `list` methods:

```rust
/// Aggregates advisory severity counts for a given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to the SBOM
    // Join with advisory table to get severity field
    // Deduplicate by advisory ID
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts, defaulting to 0 for missing levels
    // Return 404 AppError if SBOM does not exist
}
```

Key implementation details:
- Use `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- Use `AdvisorySummary.severity` field to classify each advisory
- Deduplicate by advisory ID before counting
- Verify SBOM exists first; return 404 with `.context()` wrapping if not found
- Default all severity levels to 0

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns severity counts for advisories linked to the given SBOM.
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

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation impact

- No **Documentation Updates** section in the task description.
- Check `docs/api.md` for existing endpoint documentation. If it documents REST endpoints, add an entry for `GET /api/v2/sbom/{id}/advisory-summary` with the request/response format.

### 6.7 Code quality practices

Verify all new structs, types, and public functions have documentation comments using `///` Rust doc convention. All new symbols in the implementation above include doc comments.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases, following the conventions from sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`):

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response contains correct counts per severity level and total
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response status is 404 NOT_FOUND
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response contains all zeros: critical=0, high=0, medium=0, low=0, total=0
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then each advisory is counted only once
}
```

All tests use:
- `assert_eq!(resp.status(), StatusCode::OK)` or `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for status verification
- Value-based assertions on the deserialized `SeveritySummary` fields (not just length checks)
- `///` doc comments on every test function
- Given/When/Then section comments for non-trivial tests
- `test_<endpoint>_<scenario>` naming convention matching sibling tests

Run tests after implementation:

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Confirmed by response struct definition and endpoint handler |
| Returns 404 when SBOM ID does not exist | Confirmed by service method returning AppError for missing SBOM, verified by `test_advisory_summary_not_found` |
| Counts only unique advisories (deduplicates by advisory ID) | Confirmed by deduplication logic in service method, verified by `test_advisory_summary_deduplication` |
| All severity levels default to 0 when no advisories exist | Confirmed by `SeveritySummary` using `Default` derive, verified by `test_advisory_summary_empty` |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient query design using database-level aggregation rather than client-side counting |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

**Expected modified/created files:**
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)

If `docs/api.md` was modified (documentation impact from Step 6.6), flag as out-of-scope and explain justification to the user for approval.

### Untracked file check

Run `git status --short`, extract `??` entries, filter by directories containing modified files, and check for code references to any untracked files. Flag any referenced untracked files for user review.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to scan for secrets. Flag any matches.

### Documentation currency

If `docs/api.md` describes existing API endpoints and the new endpoint was not documented in Step 6.6, update it now.

### CI checks from CONVENTIONS.md

If CI check commands were extracted from `CONVENTIONS.md` in Step 4.4, run all of them. Fix any failures before proceeding. If no CI check section was found, run `cargo build` and `cargo clippy` as standard checks and fix any new warnings.

### Data-flow trace

Trace the complete data flow for the new endpoint:

- `GET /api/v2/sbom/{id}/advisory-summary` request received by Axum router
  -> route matched in `endpoints/mod.rs`
  -> `severity_summary::get_severity_summary` handler invoked
  -> path param `id` extracted
  -> `AdvisoryService::severity_summary(id, tx)` called
  -> database query on `sbom_advisory` join table with severity aggregation
  -> `SeveritySummary` struct populated
  -> `Json(summary)` returned as HTTP response

Data-flow trace: **COMPLETE** -- all stages connected from input to output.

### Contract and sibling parity

- `SeveritySummary` is a standalone struct; no trait contract to verify.
- Sibling parity with `AdvisorySummary`, `SbomSummary`: verify the new struct follows the same derive macros and serde attributes.
- The new endpoint handler follows the same pattern as `get.rs` handlers in sibling endpoints.
- Caller-site parity: the handler calls `AdvisoryService` using the same pattern as existing handlers.

### Duplication check

Search for existing severity aggregation logic in the repository to ensure no duplication. Check for similar function names or patterns in the advisory and SBOM modules.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity summary endpoint for SBOM advisories

Add a new GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated advisory severity counts (critical, high, medium, low, total)
for a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"

git push -u origin TC-9201
```

Create a PR targeting the target branch (`main`):

```bash
gh pr create --base main \
  --title "feat(advisory): add severity summary endpoint for SBOM advisories" \
  --body "## Summary

Add a new GET /api/v2/sbom/{id}/advisory-summary endpoint that aggregates
vulnerability advisory severity counts for a given SBOM, returning counts
per severity level (Critical, High, Medium, Low) plus a total.

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Changes

- Added \`SeveritySummary\` response struct in \`advisory/model/severity_summary.rs\`
- Added \`severity_summary()\` method to \`AdvisoryService\`
- Added GET handler in \`advisory/endpoints/severity_summary.rs\`
- Registered new route in \`advisory/endpoints/mod.rs\`
- Added integration tests covering: valid counts, 404 for missing SBOM, empty results, deduplication"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add a comment** to TC-9201 summarizing the implementation:

   - PR link
   - Summary: added `SeveritySummary` model, `severity_summary()` service method, GET endpoint at `/api/v2/sbom/{id}/advisory-summary`, and 4 integration tests
   - No deviations from the plan
   - Comment includes the skill footnote with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`

3. **Transition** TC-9201 to **In Review** via `jira.transition_issue("TC-9201", "In Review")`
