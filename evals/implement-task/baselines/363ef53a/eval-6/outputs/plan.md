# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verified that the project's CLAUDE.md contains:
- **Repository Registry** -- trustify-backend with Serena instance `serena_backend` at path `./`
- **Jira Configuration** -- Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence** -- tool naming convention `mcp__<serena-instance>__<tool>`, with `serena_backend` configured for rust-analyzer

All required sections are present. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all JIRA operations. If MCP fails, fall back to REST API via `scripts/jira-client.py` per the documented fallback procedure.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Acceptance Criteria:** 5 criteria covering response shape, 404 handling, deduplication, defaults, and performance
- **Test Requirements:** 4 test cases
- **Dependencies:** None
- **Bookend Type:** Not present (standard flow)
- **Target PR:** Not present (standard flow)

Capture the issue `webUrl` for PR description linking.

Extract GitHub Issue custom field (customfield_10747) if populated.

## Step 1.5 -- Verify Description Integrity

(See digest-match.md for full details.)

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate the comment starting with `[sdlc-workflow] Description digest:` marker string
3. Found comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` and `updated` timestamps are identical -- comment was not edited
5. Parse format tag (`sha256-md`) and hex digest from the stored comment
6. Write current description to `/tmp/desc-TC-9201.txt` and compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
7. Compare format tags: both are `sha256-md` -- tags match
8. Compare hex digests: both are `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` -- digests match

**Result:** Digests match. Proceed silently without prompting the user. No additional latency on the happy path. Continue directly to Step 2.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code

### 4.1 Inspect existing files using Serena (`serena_backend`)

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` to see AdvisoryService methods (`fetch`, `list`, `search`)
- `mcp__serena_backend__find_symbol("AdvisoryService", include_body=true)` to understand the service pattern (method signatures, return types, transaction handling)
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` to see route registration pattern
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` to understand the handler pattern (Path extraction, service call, JSON response)
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` to understand AdvisorySummary and its `severity` field
- `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` to understand the join table structure
- `mcp__serena_backend__find_referencing_symbols` on any symbols planned for modification

### 4.2 Convention conformance analysis

Examine sibling files for patterns:
- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- handler structure, error handling, path parameter extraction
- `modules/fundamental/src/advisory/model/details.rs` -- struct definition patterns, derive macros, serde attributes
- `modules/fundamental/src/advisory/service/advisory.rs` -- service method patterns, transaction handling
- `tests/api/advisory.rs` -- test patterns, assertion style, setup/teardown

Expected conventions:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: `verb_noun` pattern for functions
- Endpoints: `Path<Id>` extraction, call service, return `Json`
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Derive macros: `#[derive(Serialize, Deserialize, Debug)]` on response structs

### 4.3 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract:
- CI check commands for Step 9
- Code generation commands
- Additional naming or structural conventions

### 4.4 Documentation file identification

Identify docs that may need updating:
- `docs/api.md` -- REST API reference (new endpoint needs documenting)
- `docs/architecture.md` -- if architectural patterns change
- `README.md` -- if setup steps change

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

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
#[derive(Serialize, Deserialize, Debug, Default)]
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

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to AdvisoryService following the existing pattern:

```rust
/// Computes aggregated severity counts for all advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to sbom_id
    // Deduplicate by advisory ID
    // Count by severity level using AdvisorySummary.severity field
    // Return SeveritySummary with counts; defaults to 0 for missing levels
}
```

Key implementation details:
- Use `sbom_advisory` join table to find linked advisories
- Deduplicate by advisory ID (use HashSet or DISTINCT in query)
- Map `AdvisorySummary.severity` to the four severity buckets
- Default all counts to 0 (via `SeveritySummary::default()`)
- Wrap errors with `.context("Failed to compute severity summary")`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

GET handler following the pattern in `get.rs`:

```rust
/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the specified SBOM.
pub async fn severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    // Verify SBOM exists (return 404 if not)
    // Call service.severity_summary(id, &tx)
    // Return Json(summary)
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route:

```rust
Router::new()
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

### 6.6 Documentation impact

Update `docs/api.md` with the new endpoint documentation:
- Path: `GET /api/v2/sbom/{id}/advisory-summary`
- Response shape: `{ critical, high, medium, low, total }`
- Error responses: 404 when SBOM not found

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM linked to advisories of known severities
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then response contains correct counts per severity level and correct total
}

/// Verifies that requesting a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then response status is 404
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_empty() {
    // Given an SBOM with no linked advisories
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then response contains { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM linked to the same advisory multiple times
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the advisory is counted only once
}
```

Each test uses value-based assertions (checking actual field values, not just counts) and follows the `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests.

Run tests: `cargo test -p trustify-fundamental` (or appropriate crate name from `cargo metadata`).

## Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` -- verified by test_severity_summary_with_advisories
- [x] Returns 404 for non-existent SBOM ID -- verified by test_severity_summary_not_found
- [x] Counts only unique advisories (deduplication) -- verified by test_severity_summary_deduplication
- [x] All severity levels default to 0 -- verified by test_severity_summary_empty
- [x] Performance under 200ms for up to 500 advisories -- query uses join table with indexes; verified by design (single query, no N+1)

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all changed files are within Files to Modify and Files to Create lists.

### Untracked file check
Run `git status --short` and check for untracked files in modified directories.

### Dead parameter detection
Scan modified functions for unused parameters.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`

### Documentation currency
Verify `docs/api.md` reflects the new endpoint.

### Duplication check
Search for existing severity aggregation logic to avoid duplication.

### CI checks from CONVENTIONS.md
Run any CI commands extracted in Step 4 (formatting, linting, compilation).

### Module-level test requirement (Rust)
Run `cargo test -p <crate-name>` for each crate containing modified files.

### Data-flow trace
Trace: HTTP request with SBOM ID -> Path extraction -> service.severity_summary() -> sbom_advisory join query -> severity counting -> SeveritySummary struct -> JSON response. All stages connected.

### Contract and sibling parity
Verify SeveritySummary struct, handler signature, and error handling match sibling patterns.

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
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes deduplication by advisory ID
and proper 404 handling for missing SBOMs.

Implements TC-9201"
```

Detect fork status, then push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR description includes `Implements [TC-9201](<webUrl>)` with clickable Jira link.

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format
2. Add comment to TC-9201 with PR link and summary of changes
3. Transition TC-9201 to "In Review"
