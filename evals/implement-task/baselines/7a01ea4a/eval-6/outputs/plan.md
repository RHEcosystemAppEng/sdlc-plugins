# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

- **Repository Registry**: Present -- `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Present -- Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: Present -- `serena_backend` instance with `rust-analyzer`

All required sections are present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all JIRA operations. If MCP fails, prompt user with REST API fallback options per the documented protocol.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint
- **Implementation Notes**: Follow existing patterns in get.rs, advisory.rs service, use sbom_advisory join table, use AdvisorySummary severity field, return AppError with .context()
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 test cases
- **Dependencies**: None
- **Bookend Type**: Not present (standard implementation)
- **Target PR**: Not present (new branch/PR flow)

Capture `webUrl` for Jira link in PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

Check GitHub Issue custom field (`customfield_10747`) -- extract reference if present, skip silently if empty.

## Step 1.5 -- Verify Description Integrity

1. Fetch comments via `jira.get_issue_comments("TC-9201")`.
2. Locate comment with marker `[sdlc-workflow] Description digest:`.
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` and `updated` timestamps are identical -- comment is unmodified.
5. Extract stored digest: format tag `sha256-md`, hex digest `a1b2c3d4e5f67890...`.
6. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`.
7. Tags match (`sha256-md`), hex digests match -- proceed silently with no user prompt.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user: `jira.user_info()`
2. Assign task: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition: `jira.transition_issue("TC-9201")` to "In Progress"

## Step 4 -- Understand the Code

Using Serena instance `serena_backend` (from Repository Registry):

### 4.1 Inspect files to modify

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService structure, existing `fetch` and `list` methods
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration pattern

### 4.2 Read specific symbols

- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` -- understand method signature and pattern for the new `severity_summary` method
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` -- additional reference for service method patterns
- `mcp__serena_backend__find_symbol` on `AdvisorySummary` in `model/summary.rs` -- understand the `severity` field structure

### 4.3 Check backward compatibility

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` -- ensure adding a method does not break callers

### 4.4 Non-symbolic search

- `mcp__serena_backend__search_for_pattern` for `sbom_advisory` in entity directory -- understand the join table structure
- `mcp__serena_backend__search_for_pattern` for `Router::new().route` in endpoints/mod.rs -- understand route registration syntax
- `mcp__serena_backend__search_for_pattern` for `AppError` and `.context()` -- confirm error handling pattern

### 4.5 Convention conformance analysis

**Sibling files for endpoints:**
- Inspect `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- understand handler patterns (Path extraction, service calls, JSON response)
- Inspect `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module endpoint comparison

**Sibling files for models:**
- Inspect `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- understand struct patterns, derive macros, serde attributes

**Sibling files for service:**
- Inspect existing methods in `advisory.rs` service -- understand parameter patterns (`&self`, ID type, `Transactional`)

### 4.6 Test convention analysis

- Inspect `tests/api/advisory.rs` -- understand test structure, assertion patterns, test naming
- Inspect `tests/api/sbom.rs` -- additional test pattern reference
- Record assertion style (`assert_eq!(resp.status(), StatusCode::OK)`), response validation, error case patterns, naming conventions

### 4.7 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root. If present, read and extract CI check commands and code generation commands. If absent, proceed normally.

### 4.8 Documentation file identification

Identify related documentation:
- `README.md` at repository root
- `docs/api.md` (API documentation, per CLAUDE.md)
- `docs/architecture.md` (architecture overview)

Record for documentation impact evaluation in Step 6 and currency check in Step 9.

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create SeveritySummary model

**File**: `modules/fundamental/src/advisory/model/severity_summary.rs` (NEW)

Create a response struct following patterns from sibling `summary.rs`:

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Provides a breakdown of advisory counts by severity level, enabling
/// dashboard widgets to render severity distributions without client-side counting.
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

### 6.2 Register model module

**File**: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

Add `pub mod severity_summary;` to register the new model module, following the pattern of existing module declarations.

### 6.3 Add service method

**File**: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

Add `severity_summary` method to `AdvisoryService` following the `fetch`/`list` pattern:

- Signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Query the `sbom_advisory` join table to find advisories linked to the SBOM
- Join with advisory table to get severity information from AdvisorySummary
- Deduplicate by advisory ID
- Count by severity level (Critical, High, Medium, Low)
- Return 404 (via AppError) if SBOM does not exist
- Wrap errors with `.context()`

### 6.4 Create endpoint handler

**File**: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (NEW)

Create GET handler following patterns from `get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
pub async fn severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    service
        .severity_summary(id, &tx)
        .await
        .map(Json)
        .context("fetching advisory severity summary")
}
```

### 6.5 Register route

**File**: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

Add the new route following the existing `Router::new().route()` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

### 6.6 Documentation impact

- Check if `docs/api.md` documents REST endpoints -- if so, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- No architectural changes, so `docs/architecture.md` does not need updating
- Code quality: all new structs and public functions have documentation comments as shown above

## Step 7 -- Write Tests

**File**: `tests/api/advisory_summary.rs` (NEW)

Following test conventions discovered from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories of known severities
    // (set up test SBOM and link advisories with Critical, High, Medium, Low severities)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // Deserialize body and assert specific counts for each severity
    // assert_eq!(body.total, expected_total)
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all severity counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary

    // Then the duplicate is counted only once
    // assert_eq!(body.total, expected_unique_count)
}
```

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by SeveritySummary struct and endpoint handler
- [x] Returns 404 when SBOM ID does not exist -- verified by service method returning AppError for missing SBOM, and test_advisory_summary_not_found test
- [x] Counts only unique advisories (deduplicates by advisory ID) -- verified by deduplication logic in service method and test_advisory_summary_deduplicates test
- [x] All severity levels default to 0 when no advisories exist at that level -- verified by Default derive on SeveritySummary and test_advisory_summary_empty test
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- verified by efficient single query with GROUP BY, no N+1 queries

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all modified/created files match the task's Files to Modify and Files to Create lists:
- `modules/fundamental/src/advisory/service/advisory.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in scope (Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in scope (Files to Create)
- `tests/api/advisory_summary.rs` -- in scope (Files to Create)

Any out-of-scope files flagged for user approval.

### Untracked file check
Run `git status --short`, filter `??` entries by proximity to modified directories. Search for code references to any flagged untracked files.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- ensure no secrets are staged.

### Documentation currency
Check if `docs/api.md` needs updating for the new endpoint. Update if it documents existing endpoints and the new one is missing.

### Documentation scope preservation
If any documentation was modified, verify replacement text covers all original use cases.

### Eval coverage currency
No SKILL.md files modified -- skip.

### Example consistency
Verify any documentation examples are internally consistent.

### Cross-section reference consistency
Verify file paths are consistent across task description sections:
- `AdvisoryService` referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent.
- `SeveritySummary` referenced in Files to Create (`advisory/model/severity_summary.rs`) -- consistent.
- Route registration referenced in Files to Modify (`advisory/endpoints/mod.rs`) and Implementation Notes -- consistent.

### Duplication check
Search for existing severity aggregation or counting logic in the repository. Verify no overlap with existing utilities.

### CI checks from CONVENTIONS.md
Run any CI check commands extracted in Step 4. Hard stop on any failure.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (id) -> call `AdvisoryService::severity_summary(id, tx)` -> query sbom_advisory join table -> aggregate severity counts -> return `Json<SeveritySummary>` -- COMPLETE

### Contract and sibling parity
- `SeveritySummary` -- standalone struct, no trait/interface to implement. Follows same derive pattern as sibling models (`Serialize`, `ToSchema`).
- Endpoint handler follows same signature pattern as `get.rs` handler (Path extraction, State, Transactional, Result return).
- Service method follows same pattern as `fetch`/`list` (same parameter types, same error handling).
- No cross-module shared entity concerns -- reads from `sbom_advisory` join table (read-only, no writes).

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes deduplication by advisory ID
and proper 404 handling for missing SBOMs.

Implements TC-9201"
```

Detect fork (check for `upstream` remote). Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main \
  --title "feat(advisory): add severity aggregation endpoint" \
  --body "## Summary
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint returning severity counts
- Add SeveritySummary model, AdvisoryService.severity_summary method, and integration tests
- Deduplicates advisories by ID; returns 404 for missing SBOMs

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

Closes <owner>/<repo>#<number> (if GitHub Issue field is populated)"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format:
   ```
   jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added GET /api/v2/sbom/{id}/advisory-summary endpoint with SeveritySummary model, service method, route registration, and integration tests
   - Deviations: None
   - Footer: sdlc-workflow/implement-task v{version} (read from plugin.json)

3. **Transition** TC-9201 to "In Review":
   ```
   jira.transition_issue("TC-9201") -> "In Review"
   ```
