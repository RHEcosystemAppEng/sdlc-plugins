# Implementation Plan -- TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured with `rust-analyzer`

Validation passes. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all JIRA operations. Fall back to REST API (`scripts/jira-client.py`) if MCP fails, following the prompt protocol in the skill definition.

## Step 1 -- Fetch and Parse Jira Task

Fetch `TC-9201` via `jira.get_issue("TC-9201")` and parse the structured description:

| Section | Value |
|---|---|
| **Repository** | trustify-backend |
| **Target Branch** | main |
| **Description** | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total. |
| **Files to Modify** | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| **Files to Create** | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| **API Changes** | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| **Bookend Type** | Not present |
| **Target PR** | Not present |
| **Dependencies** | None |

Capture the issue `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

Check the GitHub Issue custom field (`customfield_10747`) -- extract the GitHub issue reference if present.

## Step 1.5 -- Verify Description Integrity

(See digest-match.md for full details.)

Digest comment found, unedited, format tags match (`sha256-md`), hex digests match. Proceeding silently -- no user interaction needed.

## Step 2 -- Verify Dependencies

The task has no dependencies (`Depends on: None`). Skip dependency verification.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to "In Progress": `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

Using the Serena instance `serena_backend` (from the Repository Registry), inspect the codebase:

### 4.1 Overview of files to modify

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` struct and existing methods (`fetch`, `list`, `search`)
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration pattern

### 4.2 Read specific symbols

- `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` -- understand the method signature pattern (takes `&self, id: Id, tx: &Transactional<'_>`)
- `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` -- understand the list method pattern
- `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` -- understand the struct that contains the `severity` field
- `mcp__serena_backend__find_symbol("AppError", include_body=true)` -- understand error handling pattern

### 4.3 Check backward compatibility

- `mcp__serena_backend__find_referencing_symbols("AdvisoryService")` -- identify all consumers of the service

### 4.4 Inspect related entities and patterns

- `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` -- understand the join table structure for SBOM-Advisory relationships
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand existing endpoint handler pattern (Path extraction, service call, JSON response)
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- understand the AdvisorySummary struct and its severity field

### 4.5 Convention conformance analysis

Examine sibling files for patterns:

- **Endpoint siblings**: `endpoints/get.rs`, `endpoints/list.rs` -- handler function signatures, Path extraction, error handling, return types
- **Model siblings**: `model/summary.rs`, `model/details.rs` -- struct definition, derive macros, serialization attributes
- **Service siblings**: `service/advisory.rs` existing methods -- method signatures, transaction handling, query patterns
- **Test siblings**: `tests/api/advisory.rs`, `tests/api/sbom.rs` -- test setup, assertion patterns, status code checks

Expected convention discoveries:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: `verb_noun` pattern for functions
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Derive macros on models: `#[derive(Debug, Clone, Serialize, Deserialize)]`
- Route registration: `Router::new().route("/path", get(handler))`

### 4.6 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it for naming rules, directory structure, code patterns, test conventions, and CI check commands. Extract verification commands for use in Step 9.

### 4.7 Documentation file identification

Identify documentation files for documentation-impact evaluation:
- `docs/api.md` -- API documentation
- `docs/architecture.md` -- architecture overview
- `README.md` at repository root

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
/// Aggregated advisory severity counts for an SBOM.
///
/// Provides a breakdown of linked advisory counts by severity level,
/// enabling dashboard widgets to render severity distributions without
/// client-side counting.
#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]
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

Follow derive macro patterns from sibling model files (`summary.rs`, `details.rs`). Include documentation comments on the struct and every field.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:

```rust
pub mod severity_summary;
```

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService`, following the existing method pattern:

```rust
/// Compute aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories linked to `sbom_id`,
/// deduplicates by advisory ID, and counts occurrences of each severity level.
/// Returns a `SeveritySummary` with counts defaulting to 0 for levels with no advisories.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query advisories linked to the SBOM via sbom_advisory join table
    // Deduplicate by advisory ID
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts, total = sum of all levels
}
```

Implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- Join with advisory table to get severity information
- Use `AdvisorySummary.severity` field for severity classification
- Deduplicate by advisory ID before counting
- Default all severity counts to 0
- Return 404 (`AppError`) when the SBOM ID does not exist, consistent with existing SBOM endpoints
- Wrap errors with `.context()` per the project's error handling convention

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern from `endpoints/get.rs`:

```rust
/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// enabling dashboard severity breakdown widgets.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the exact extraction pattern from sibling endpoint handlers. Use defensive guards on any external data access.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route in the existing router:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follow the registration pattern of existing routes in this file.

### 6.6 Symbol deduplication check

Before declaring the `SeveritySummary` struct, search the codebase for existing symbols with similar names (`SeveritySummary`, `severity_summary`, `AdvisorySeverity`). If found, reuse rather than duplicate.

### 6.7 Documentation impact

- No **Documentation Updates** section in the task description.
- Check `docs/api.md` -- if it documents REST endpoints, add an entry for `GET /api/v2/sbom/{id}/advisory-summary`.
- Other docs (`docs/architecture.md`, `README.md`) unlikely to need updates for a new endpoint.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases, following the test patterns discovered from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that an SBOM with linked advisories returns accurate severity counts
/// broken down by level.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (set up test data: SBOM + linked advisories with various severities)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, <expected>)
    // assert_eq!(body.high, <expected>)
    // assert_eq!(body.medium, <expected>)
    // assert_eq!(body.low, <expected>)
    // assert_eq!(body.total, <expected>)
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID returns
/// HTTP 404, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary with all
/// severity counts at zero.
#[tokio::test]
async fn test_severity_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}
```

### Test 4: Duplicate advisory links are deduplicated in the count

```rust
/// Verifies that duplicate advisory-SBOM links are deduplicated, ensuring each
/// advisory is counted only once in the severity summary.
#[tokio::test]
async fn test_severity_summary_deduplicates() {
    // Given an SBOM with duplicate links to the same advisory

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, 1) (not 2)
    // assert specific severity level count reflects deduplication
}
```

All tests use value-based assertions (asserting on actual severity counts, not just collection lengths). Each test has a documentation comment and given-when-then section comments.

Run tests:

```bash
cargo test -p <crate-name-for-tests>
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by test 1 and struct definition |
| Returns 404 when SBOM ID does not exist | Verified by test 2 |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by test 4 and service implementation |
| All severity levels default to 0 when no advisories exist | Verified by test 3 |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient query design (single join query with GROUP BY) |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create. Expected modified/created files:

- `modules/fundamental/src/advisory/service/advisory.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/model/mod.rs` (modify) -- in scope
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create) -- in scope
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create) -- in scope
- `tests/api/advisory_summary.rs` (create) -- in scope

Flag any out-of-scope files for user approval.

### Untracked file check

Run `git status --short`, filter `??` entries in modified directories, check for references in the staged diff.

### Dead parameter detection

Scan modified functions for parameters no longer referenced. The main modification is adding a new method to `AdvisoryService` -- no existing parameters are removed, so no dead parameters expected.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Verify no secrets are present in the diff.

### Documentation currency

If `docs/api.md` describes REST endpoints, verify it includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Update if missing.

### Documentation scope preservation

No documentation sections are being replaced -- only additions. No use-case coverage loss expected.

### Duplication check

Search for existing severity aggregation logic in the repository. Grep for `severity_summary`, `SeveritySummary`, `severity.*count`, `advisory.*summary` to ensure no duplication.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` (if found). If none found, run:

```bash
cargo fmt --check
cargo clippy -- -D warnings
cargo check
```

### Module-level test requirement (Rust)

Resolve the crate name for each modified file using `cargo metadata --no-deps --format-version 1`. Run tests for each affected crate:

```bash
cargo test -p <crate-name>
```

Hard stop on any failure.

### Data-flow trace

Trace the complete data flow:
1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter
2. **Processing**: Axum extracts `Path(id)`, calls `AdvisoryService::severity_summary(id, tx)`, which queries `sbom_advisory` join table, joins with advisory severity data, deduplicates by advisory ID, counts by severity level
3. **Output**: `SeveritySummary` struct serialized as JSON response `{ critical, high, medium, low, total }`

All stages are connected. No incomplete paths.

### Query-scope verification

The query targets advisories linked to a specific SBOM (filtered by `sbom_id`). The scope is correctly constrained -- no broad unfiltered queries.

### Contract & sibling parity

| Check | Result |
|---|---|
| **Contract** | `severity_summary` method follows `AdvisoryService` method signature pattern (`&self, id, tx -> Result<T, AppError>`) |
| **Sibling parity** | Handler follows same extraction, service call, JSON return pattern as `get.rs` and `list.rs` |
| **Cross-module entity** | Uses `sbom_advisory` join table read-only -- no write conflicts with other modules |
| **Caller-site** | No shared abstractions being called differently from existing callers |

## Step 10 -- Commit and Push

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

Determine fork vs non-fork flow.

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add tests/api/advisory_summary.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add modules/fundamental/src/advisory/model/mod.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"
```

### Push and create PR

```bash
git push -u origin TC-9201
```

Create PR with `--base main`:

```bash
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning severity counts (critical, high, medium, low, total)
- Add `SeveritySummary` response model with per-level counts
- Add `AdvisoryService::severity_summary` method with deduplication by advisory ID
- Add integration tests covering valid SBOM, missing SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [ ] Verify endpoint returns correct severity counts for an SBOM with known advisories
- [ ] Verify 404 response for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no advisories
- [ ] Verify duplicate advisory links are deduplicated in counts
- [ ] Run full CI pipeline
EOF
)"
```

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201:

```
Implementation complete. PR: <PR-URL>

Changes:
- Created SeveritySummary response model
- Added AdvisoryService::severity_summary method with SBOM-advisory join and deduplication
- Created GET /api/v2/sbom/{id}/advisory-summary endpoint handler
- Added 4 integration tests (valid SBOM, 404, empty, deduplication)

No deviations from the plan.
```

(With skill footnote appended per `shared/comment-footnote.md`.)

3. **Transition** TC-9201 to "In Review":

```
jira.transition_issue("TC-9201") -> In Review
```
