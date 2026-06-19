# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Pre-Implementation Checks

### Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- **Repository Registry**: trustify-backend mapped to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
- **Code Intelligence**: Serena MCP server configured with rust-analyzer for trustify-backend

Configuration is valid. Proceed.

### Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. Fall back to REST API via `scripts/jira-client.py` if MCP fails.

### Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parsed fields:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Acceptance Criteria**: 5 criteria (200 response, 404, deduplication, defaults to 0, performance)
- **Test Requirements**: 4 test cases
- **Dependencies**: None
- **Linked Issues**: is incorporated by TC-9001
- **Labels**: ai-generated-jira

Capture `webUrl` for PR description linking.

Check GitHub Issue custom field (customfield_10747) on the issue -- extract if present for PR `Closes` line.

### Step 1.5 -- Verify Description Integrity

(See outputs/digest-match.md for full details.)

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate the digest comment with marker `[sdlc-workflow] Description digest:`
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` == `updated` -- not edited, no warning
5. Format tag: `sha256-md` -- not legacy format, proceed with verification
6. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` -- outputs `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
7. Format tags match (`sha256-md` == `sha256-md`)
8. Hex digests match -- **proceed silently**, no user prompt, no added latency

### Step 2 -- Verify Dependencies

Task has no dependencies. Proceed.

### Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201: `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Code Understanding

### Step 4 -- Understand the Code

#### 4.1 Inspect existing files using Serena (serena_backend)

**Files to modify -- overview and symbol inspection:**

- `modules/fundamental/src/advisory/service/advisory.rs`:
  - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its methods (fetch, list, search)
  - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` and `AdvisoryService::list` to understand the method pattern (parameters, return type, transaction handling)

- `modules/fundamental/src/advisory/endpoints/mod.rs`:
  - `mcp__serena_backend__get_symbols_overview` to see route registration pattern
  - Identify how routes are composed (Router::new().route(...))

- `modules/fundamental/src/advisory/model/mod.rs`:
  - `mcp__serena_backend__get_symbols_overview` to see existing module declarations

**Reference files for pattern extraction:**

- `modules/fundamental/src/advisory/endpoints/get.rs`:
  - `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function to see Path<Id> extraction, service call, JSON return pattern

- `modules/fundamental/src/advisory/model/summary.rs`:
  - `mcp__serena_backend__find_symbol` on `AdvisorySummary` to see the `severity` field type

- `entity/src/sbom_advisory.rs`:
  - `mcp__serena_backend__get_symbols_overview` to understand the join table structure

- `common/src/error.rs`:
  - `mcp__serena_backend__find_symbol` on `AppError` to understand error handling pattern

#### 4.2 Convention conformance analysis

**Sibling analysis targets:**
- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- endpoint patterns
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- model patterns
- `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module endpoint pattern for SBOM-scoped endpoints

**Expected conventions to discover:**
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: service methods as `verb_noun` pattern
- Route registration: `Router::new().route("/path", get(handler))`
- Response types: direct struct return with Axum's Json extractor
- Model structs: derive `Serialize`, `Deserialize`, possibly `ToSchema` for OpenAPI

#### 4.3 Test convention analysis

**Sibling test files:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Examine for:
- Assertion style (`assert_eq!` with StatusCode)
- Response body deserialization pattern
- 404 test pattern
- Test setup (database seeding, test fixtures)
- Test naming convention

#### 4.4 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. Read if present, extract CI check commands and code generation commands.

#### 4.5 Documentation file identification

Look for:
- `docs/api.md` -- API documentation that may need updating for the new endpoint
- `docs/architecture.md` -- architecture overview (likely no changes needed)
- README files in advisory module directories

#### 4.6 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` -- ensure new method does not conflict with existing interface
- Advisory model `mod.rs` -- verify adding a new module declaration is safe

## Implementation

### Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6 -- Implement Changes

#### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

Derive traits will follow the pattern observed in sibling model structs (e.g., `AdvisorySummary`).

#### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module declaration:

```rust
pub mod severity_summary;
```

Follow the existing pattern of module declarations in this file.

#### 6.3 Add `severity_summary` method to `modules/fundamental/src/advisory/service/advisory.rs`

Add a method to `AdvisoryService` following the pattern of `fetch` and `list`:

```rust
/// Computes aggregated severity counts for advisories linked to the given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level (Critical, High,
/// Medium, Low) and a total. Advisories are deduplicated by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to this SBOM
    // 2. Deduplicate by advisory ID
    // 3. For each unique advisory, look up severity from AdvisorySummary
    // 4. Count per severity level
    // 5. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `entity::sbom_advisory` to find advisories linked to the SBOM
- Use the `severity` field from `AdvisorySummary` to categorize
- Deduplicate by advisory ID before counting
- Return 404 (via AppError with context) when SBOM ID does not exist
- All severity levels default to 0 (handled by `SeveritySummary::default()`)

#### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern from `endpoints/get.rs`:

```rust
/// Handles GET /api/v2/sbom/{id}/advisory-summary.
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
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the exact parameter extraction and error handling patterns from sibling endpoint handlers.

#### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing pattern:

```rust
use severity_summary::get_severity_summary;

// Add to the router:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

#### 6.6 Documentation impact

- Check `docs/api.md` for API reference -- add the new endpoint if the file documents endpoints
- No changes to `server/src/main.rs` needed (routes auto-mount via module registration per task description)

#### 6.7 Code quality verification

- All new structs (`SeveritySummary`) have documentation comments
- All new functions (`severity_summary`, `get_severity_summary`) have documentation comments
- Error handling uses `.context()` wrapping consistent with `common/src/error.rs`

### Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels
    // (seed test database with SBOM and linked advisories)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical);
    assert_eq!(summary.high, expected_high);
    assert_eq!(summary.medium, expected_medium);
    assert_eq!(summary.low, expected_low);
    assert_eq!(summary.total, expected_total);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM with duplicate links to the same advisory

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the count reflects unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Verify count matches unique advisory count, not total link count
    assert_eq!(summary.total, expected_unique_count);
}
```

Test conventions follow sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):
- Use `assert_eq!` with `StatusCode` variants
- Deserialize response body and check field values (not just counts)
- Each test function has a `///` doc comment
- Non-trivial tests use given-when-then section comments
- Test naming follows `test_<feature>_<scenario>` pattern

Run `cargo test` and fix any failures before proceeding.

### Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by `test_severity_summary_valid_sbom`
2. Returns 404 when SBOM ID does not exist -- verified by `test_severity_summary_not_found`
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by `test_severity_summary_deduplication`
4. All severity levels default to 0 when no advisories exist -- verified by `test_severity_summary_no_advisories`
5. Response time under 200ms for SBOMs with up to 500 advisories -- verify via test timing or manual check; the query should be efficient using the join table index

### Step 9 -- Self-Verification

#### Scope containment
Run `git diff --name-only` and verify all modified/created files are in the task's Files to Modify and Files to Create lists.

Expected files:
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)

Flag any out-of-scope files for user approval.

#### Untracked file check
Run `git status --short`, check for `??` entries in directories where implementation work occurred. Search for code references to any untracked files.

#### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- should find no matches.

#### Documentation currency
If `docs/api.md` documents REST endpoints and was not already updated in Step 6, update it to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

#### Duplication check
Search the repository for existing severity aggregation logic to ensure no duplication.

#### CI checks from CONVENTIONS.md
Run any CI check commands extracted from CONVENTIONS.md. Hard stop on any failure.

#### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (id) -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> deduplicate -> count by severity -> return `SeveritySummary` as JSON -- **COMPLETE**

#### Contract and sibling parity
- `SeveritySummary` -- standalone struct, no trait implementation required
- Sibling parity with `AdvisorySummary`, `AdvisoryDetails` -- derives match, serialization pattern matches
- Endpoint handler parity with `get.rs`, `list.rs` -- error handling, response type, parameter extraction patterns match

#### Cross-section reference consistency
- `AdvisoryService` referenced in Files to Modify (`service/advisory.rs`) and Implementation Notes (`service/advisory.rs`) -- consistent
- All file paths are consistent across Description, Files to Modify, Files to Create, and Implementation Notes sections

### Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       tests/api/advisory_summary.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       modules/fundamental/src/advisory/model/mod.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns aggregated
severity counts (critical, high, medium, low, total) for advisories linked
to a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"
```

Push and create PR:
```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

- Add \`SeveritySummary\` response model with per-severity counts
- Add \`severity_summary\` method to \`AdvisoryService\`
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint
- Add integration tests for valid SBOM, 404, empty, and deduplication cases

Implements [TC-9201](<webUrl>)
<Closes line if GitHub Issue custom field is populated>"
```

### Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format:
   ```
   jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. Add comment to TC-9201 with:
   - PR link
   - Summary: Added advisory severity aggregation endpoint with SeveritySummary model, AdvisoryService method, GET handler, and integration tests
   - No deviations from plan
   - Comment ends with the standard skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. Transition TC-9201 to In Review:
   ```
   jira.transition_issue("TC-9201") -> In Review
   ```
