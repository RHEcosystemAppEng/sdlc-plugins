# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main

---

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`).
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend`.

Validation passes. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all JIRA operations. If MCP fails, prompt the user for REST API fallback. The REST API equivalents are documented in the skill definition.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns `{ critical, high, medium, low, total }`.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed (auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Acceptance Criteria**: 5 criteria (correct counts, 404 handling, deduplication, defaults to 0, performance)
- **Test Requirements**: 4 tests (valid SBOM, non-existent SBOM, no advisories, deduplication)
- **Dependencies**: None
- **Target PR**: Not present (default flow)
- **Bookend Type**: Not present (default flow)
- **Review Context**: Not present
- **GitHub Issue custom field**: Check `customfield_10747` on the fetched issue for a GitHub issue URL. If present, extract `owner/repo#number` for PR description.

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

All required sections are present. Proceed.

## Step 1.5 -- Verify Description Integrity

1. Fetch comments via `jira.get_issue_comments("TC-9201")`.
2. One comment found with marker `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
3. Comment's `created` and `updated` timestamps are identical -- not edited. No warning.
4. Extract stored digest: tag `sha256-md`, hex `a1b2c3d4e5f67890...`.
5. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` -- output: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
6. Format tags match (both `sha256-md`). Hex digests match.
7. **Result: Match. Proceed silently** -- no user prompt, no added latency.

## Step 2 -- Verify Dependencies

The task has no dependencies. Skip this step.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to In Progress: `jira.transition_issue("TC-9201") -> In Progress`.

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use `mcp__serena_backend__get_symbols_overview` on each file to understand structure:

- **`modules/fundamental/src/advisory/service/advisory.rs`** -- inspect `AdvisoryService` struct and its existing methods (`fetch`, `list`, `search`) to understand the method signature pattern (parameters, return types, error handling).
- **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- inspect route registration pattern (`Router::new().route(...)`) to see how handlers are mounted.
- **`modules/fundamental/src/advisory/model/mod.rs`** -- inspect existing `pub mod` declarations to see the pattern for registering submodules.

### 4.2 Inspect referenced code patterns

Use `mcp__serena_backend__find_symbol` with `include_body=true`:

- **`modules/fundamental/src/advisory/endpoints/get.rs`** -- read the GET handler to understand `Path<Id>` extraction, service invocation, and JSON response pattern.
- **`modules/fundamental/src/advisory/model/summary.rs`** -- read `AdvisorySummary` struct to see the `severity` field type and derivations.
- **`entity/src/sbom_advisory.rs`** -- read the join table entity to understand the relationship between SBOMs and advisories.
- **`common/src/error.rs`** -- read `AppError` to understand error wrapping with `.context()`.

### 4.3 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on:

- `AdvisoryService` -- ensure the new `severity_summary` method does not conflict with existing methods.
- `endpoints/mod.rs` route registration -- ensure no route path conflict with `/api/v2/sbom/{id}/advisory-summary`.

### 4.4 Convention conformance analysis (sibling files)

Examine sibling files for patterns:

- **Sibling endpoint handlers**: `endpoints/get.rs`, `endpoints/list.rs` in the advisory module -- inspect structure, error handling, path parameter extraction.
- **Sibling service methods**: other methods in `advisory.rs` -- inspect signature patterns, transactional usage, return types.
- **Sibling model files**: `model/summary.rs`, `model/details.rs` -- inspect derive macros, serde attributes, field types.

**Expected discovered conventions:**

- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping.
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`).
- **Endpoint pattern**: Extract path via `Path<Id>`, call service, return `Json(result)`.
- **Model structs**: Derive `Serialize`, `Deserialize`, `Debug`, `Clone`; use serde attributes for field naming.
- **Route registration**: `Router::new().route("/path", get(handler))` chained in `endpoints/mod.rs`.

### 4.5 Test convention analysis

Examine sibling test files:

- **`tests/api/advisory.rs`** -- inspect assertion patterns, test naming, setup/teardown.
- **`tests/api/sbom.rs`** -- inspect how SBOM-related endpoints are tested.

**Expected discovered test conventions:**

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- **Response validation**: Check specific field values, not just lengths.
- **Error cases**: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Test naming**: `test_<endpoint>_<scenario>` pattern.

### 4.6 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). Per the repo structure, it exists. Read it and extract:

- Code conventions for implementation.
- CI check commands (formatting, linting, compilation) for Step 9.
- Any code generation commands.

### 4.7 Documentation file identification

Identify documentation files related to the changes:

- `docs/api.md` -- REST API reference (may need updating with new endpoint).
- `docs/architecture.md` -- system architecture (unlikely to need changes for this task).
- `README.md` -- repository root readme (unlikely to need changes).

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
/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u32,
    /// Count of advisories with High severity.
    pub high: u32,
    /// Count of advisories with Medium severity.
    pub medium: u32,
    /// Count of advisories with Low severity.
    pub low: u32,
    /// Total count of unique advisories.
    pub total: u32,
}
```

Follow the derive macro pattern from sibling model files (`summary.rs`, `details.rs`). Default all fields to 0 using `Default` derive or explicit initialization.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:

```rust
pub mod severity_summary;
```

Follow the existing `pub mod` declaration pattern in the file.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService`:

```rust
/// Computes aggregated severity counts for all advisories linked to a given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Join with advisory table to get severity
    // Deduplicate by advisory ID
    // Count by severity level
    // Return SeveritySummary with counts
}
```

Implementation details:
- Use SeaORM to query `sbom_advisory` join table filtered by `sbom_id`.
- Join to advisory entity to access severity field.
- Use `DISTINCT` or `HashSet` to deduplicate by advisory ID.
- Count occurrences of each severity level (Critical, High, Medium, Low).
- Return 0 for any severity level with no advisories.
- Wrap errors with `.context("Failed to compute severity summary")`.
- Return 404 (via AppError) when the SBOM ID does not exist -- verify SBOM existence first, following the pattern in existing SBOM endpoints.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Implement the GET handler:

```rust
/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
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

Follow the exact pattern from `endpoints/get.rs`: extract path params via `Path<Id>`, call service, return `Json(result)`.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follow the existing `Router::new().route(...)` chaining pattern.

### 6.6 Documentation impact

Check `docs/api.md` -- if it documents REST endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response schema.

### 6.7 Code quality checks

- Every new struct, function, and public symbol has a documentation comment.
- Error handling uses `AppError` with `.context()` wrapping.
- Response struct uses standard serde derives matching sibling models.

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Write four integration tests following the discovered test conventions:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test data in PostgreSQL)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response has status 200 and correct counts per severity level
    // Assert on specific field values (critical, high, medium, low, total)
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response has status 404
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response has status 200 and all counts are 0
    // total == 0, critical == 0, high == 0, medium == 0, low == 0
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with the same advisory linked multiple times

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once in the severity summary
}
```

**Test conventions applied:**
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Value-based assertions on `critical`, `high`, `medium`, `low`, `total` fields -- not just length checks.
- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- Test naming follows `test_<endpoint>_<scenario>` pattern.

Run tests:

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Verified by `test_advisory_summary_valid_sbom` |
| 2 | Returns 404 for non-existent SBOM | Verified by `test_advisory_summary_nonexistent_sbom` |
| 3 | Counts only unique advisories | Verified by `test_advisory_summary_deduplication` |
| 4 | Defaults to 0 when no advisories | Verified by `test_advisory_summary_no_advisories` |
| 5 | Response time under 200ms for 500 advisories | Verified by query design (single query with aggregation, no N+1) |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create. Expected files:

- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)

If `docs/api.md` was modified (documentation impact from Step 6.6), flag it as out-of-scope and ask for user approval.

### Untracked file check

Run `git status --short`, extract `??` entries. Check proximity to modified directories. Search for code references to any untracked files (e.g., `include_str!`, `use`, `mod`).

### Dead parameter detection

Review `git diff` for any removed parameter references. The changes are primarily additive (new method, new handler, new struct), so dead parameters are unlikely.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation currency

Verify `docs/api.md` still accurately reflects the API surface if it was not updated in Step 6.6. If the new endpoint is missing, update it now.

### Documentation scope preservation

If `docs/api.md` was modified, verify the replacement text still covers all previously documented endpoints and scenarios.

### Eval coverage currency

No SKILL.md files are being modified. Skip.

### Example consistency

If any documentation with composite examples was written, cross-check narrative against data structures.

### Cross-section reference consistency

Verify file paths are consistent across Files to Modify, Files to Create, and Implementation Notes. All references align in this task description.

### Duplication check

Search for existing severity aggregation logic in the codebase. Grep for `severity_summary`, `severity_count`, or similar patterns. If found, reuse instead of duplicating.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4.6 (e.g., `cargo fmt --check`, `cargo clippy`, `cargo build`). Hard stop on any failure.

### Data-flow trace

```
GET /api/v2/sbom/{id}/advisory-summary
  -> severity_summary handler (parse Path<Id>)
  -> AdvisoryService::severity_summary(sbom_id, tx)
  -> Query sbom_advisory join table + advisory table
  -> Aggregate by severity, deduplicate by advisory ID
  -> Return SeveritySummary struct
  -> Json(SeveritySummary) response
```

All stages connected: input (request) -> processing (service + query) -> output (JSON response). **COMPLETE.**

### Query-scope verification

The query targets advisories linked to a specific SBOM ID via the `sbom_advisory` join table. The scope is correctly narrowed by `sbom_id` -- no unscoped `all()` query.

### Contract and sibling parity

- **Contract verification**: `SeveritySummary` is a standalone struct, not implementing a trait. The handler signature matches the Axum handler contract.
- **Sibling parity**: Compare `severity_summary` endpoint handler against sibling handlers (`get.rs`, `list.rs`). Ensure same error handling, same path parameter extraction, same response pattern.
- **Cross-module shared entity analysis**: The `sbom_advisory` join table is used by the ingestor module for ingestion. Verify the new read-only query follows the same entity access patterns (no conflicting writes).
- **Caller-site parity**: The new handler calls `AdvisoryService` methods following the same pattern as existing handlers.

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Deduplicates advisories by ID and defaults
to 0 for severity levels with no matches.

Implements TC-9201"
```

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If upstream exists, parse `<upstream-owner/repo>` and `<fork-owner>`.

### Push and create PR

```bash
git push -u origin TC-9201
```

Create PR with `gh pr create`:

- `--base main` (target branch)
- Title: `feat(advisory): add severity aggregation endpoint for SBOM advisories`
- Body includes:
  - Summary of changes
  - `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
  - `Closes <owner>/<repo>#<number>` if GitHub Issue custom field was populated

If fork detected, add `-R <upstream-owner/repo> --head <fork-owner>:TC-9201`.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format (inlineCard).

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added `severity_summary` method to `AdvisoryService` and `GET /api/v2/sbom/{id}/advisory-summary` endpoint with integration tests. Returns aggregated severity counts for SBOM-linked advisories.
   - No deviations from the plan.
   - Comment ends with the skill footnote (horizontal rule + "This comment was AI-generated by sdlc-workflow/implement-task v{version}.").

3. **Transition** TC-9201 to **In Review**: `jira.transition_issue("TC-9201") -> In Review`.
