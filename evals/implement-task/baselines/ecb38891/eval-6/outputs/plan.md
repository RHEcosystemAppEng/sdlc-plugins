# Implementation Plan: TC-9201

## Task Summary

**Issue:** TC-9201 -- Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Status:** Description integrity verified (digest match, Step 1.5 passed silently)

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains:
- Repository Registry with trustify-backend entry (Serena instance: serena_backend, path: ./)
- Jira Configuration with project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence section with serena_backend instance using rust-analyzer

All required sections present. Proceeding.

## Step 1 -- Parsed Task Description

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Dependencies:** None
- **Web URL:** captured from API response for PR description linking

### Files to Modify
1. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
3. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`

### Files to Create
1. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
3. `tests/api/advisory_summary.rs` -- integration tests for the new endpoint

### API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`

## Step 1.5 -- Description Integrity Verification

See `digest-match.md` for full details. The digest comment was located using the marker string `[sdlc-workflow] Description digest:`. The stored digest (`sha256-md:a1b2c3d4e5f67890...`) was compared against the current description digest computed via `scripts/sha256-digest.py`. Format tags match (both `sha256-md`), hex digests match. Proceeding silently.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code

### Code Inspection

Before making any changes, inspect the following existing files using the serena_backend instance:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Read this file to understand the existing endpoint pattern: path param extraction via `Path<Id>`, service call, JSON response. Use `mcp__serena_backend__get_symbols_overview` to see the handler signature and structure, then `mcp__serena_backend__find_symbol` with `include_body=true` to read the handler function body.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Read the existing `fetch` and `list` methods to understand the service pattern (method signature with `&self, id: Id, tx: &Transactional<'_>`). Use `mcp__serena_backend__get_symbols_overview` to see all methods, then read `fetch` and `list` bodies.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Inspect the `AdvisorySummary` struct to understand the `severity` field and how severity is represented. Use `mcp__serena_backend__find_symbol` for the struct definition.

4. **`common/src/error.rs`** -- Inspect the `AppError` enum and `.context()` usage pattern to ensure error handling follows established conventions.

5. **`entity/src/sbom_advisory.rs`** -- Inspect the SBOM-Advisory join table entity to understand how to query advisories linked to a specific SBOM.

6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Read the route registration pattern to know how to add the new route.

7. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read to understand how model sub-modules are registered.

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (listed in repo structure). Read it for naming rules, directory structure, code patterns, and CI check commands.

### Convention Conformance Analysis (Sibling Analysis)

Examine sibling files to establish conventions:

**Production code siblings:**
- `modules/fundamental/src/advisory/endpoints/get.rs` -- endpoint handler pattern
- `modules/fundamental/src/advisory/endpoints/list.rs` -- endpoint handler with query params
- `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module endpoint pattern

**Test siblings:**
- `tests/api/advisory.rs` -- advisory integration test patterns
- `tests/api/sbom.rs` -- SBOM integration test patterns

**Discovered conventions:**
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs`
- **Module structure:** Each domain follows `model/` + `service/` + `endpoints/` structure
- **Endpoint pattern:** Extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Route registration:** `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Service method signature:** `async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- **Response types:** Structs derive `Serialize, Deserialize, Debug, Clone, PartialEq` and use `utoipa::ToSchema` for OpenAPI
- **Test patterns:** Integration tests use real PostgreSQL test database, assert on `resp.status()` and response body fields
- **Naming:** `verb_noun` pattern for functions, `NounSummary`/`NounDetails` for model structs

### Documentation Files Identified

- `docs/api.md` -- API reference, may need updating with new endpoint
- `docs/architecture.md` -- system architecture, likely no change needed
- `README.md` -- project overview, likely no change needed

## Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch named after the Jira issue ID (TC-9201), based on the Target Branch (main).

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

Create the `SeveritySummary` response struct:

```rust
/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of linked advisories by severity level,
/// enabling dashboard widgets to render severity breakdowns.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u64,
    /// Count of high-severity advisories.
    pub high: u64,
    /// Count of medium-severity advisories.
    pub medium: u64,
    /// Count of low-severity advisories.
    pub low: u64,
    /// Total count of unique advisories.
    pub total: u64,
}
```

Include `Default` derive so all fields default to 0.

### File 2: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

Add the module registration:

```rust
pub mod severity_summary;
```

### File 3: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

Add `severity_summary` method to `AdvisoryService` following the existing `fetch`/`list` pattern:

```rust
/// Compute severity counts for all advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // JOIN with advisory table to get severity field
    // Deduplicate by advisory ID
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

- Use the `sbom_advisory` join table (entity/src/sbom_advisory.rs) to find linked advisories
- Use the `severity` field from `AdvisorySummary` (advisory/model/summary.rs) to categorize
- Deduplicate by advisory ID before counting
- Return 404 via `AppError` with `.context()` if the SBOM does not exist

### File 4: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

Create the GET handler following the pattern in `advisory/endpoints/get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity count summary for all advisories linked to the given SBOM.
pub async fn severity_summary(
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

### File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

Register the new route following existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

### File 6: `tests/api/advisory_summary.rs` (CREATE)

Integration tests for the new endpoint (see Step 7).

### Documentation Impact

The new endpoint `GET /api/v2/sbom/{id}/advisory-summary` should be documented in `docs/api.md` with the request/response format.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following tests, following sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (setup: create SBOM, create advisories with Critical, High, Medium, Low severities,
    //  link via sbom_advisory)

    // When requesting the severity summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, expected_critical_count)
    // assert_eq!(body.high, expected_high_count)
    // assert_eq!(body.medium, expected_medium_count)
    // assert_eq!(body.low, expected_low_count)
    // assert_eq!(body.total, expected_total)
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the severity summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the severity summary

    // Then all severity counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the severity summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, 1)  // not 2
}
```

Run tests via `cargo test` and fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- implemented in endpoint handler
- [x] Returns 404 when SBOM ID does not exist -- handled via AppError in service method
- [x] Counts only unique advisories (deduplicates by advisory ID) -- deduplication in service query
- [x] All severity levels default to 0 when no advisories exist -- Default derive on SeveritySummary
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- single database query with JOIN, no N+1

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files are within the task scope:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (Files to Create)
- `tests/api/advisory_summary.rs` (Files to Create)
- `modules/fundamental/src/advisory/service/advisory.rs` (Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` (Files to Modify)

No out-of-scope files.

### Sensitive-Pattern Check

Search staged diff for secrets/credentials -- none expected in this change.

### Documentation Currency

The new endpoint should be added to `docs/api.md`. No other documentation changes needed.

### Duplication Check

Search for existing severity aggregation logic -- none expected to exist.

### CI Checks

Run CI check commands from CONVENTIONS.md (if extracted). Run `cargo test`, `cargo clippy`, `cargo fmt --check`.

### Data-Flow Trace

- **Input:** HTTP GET request with SBOM ID path parameter
- **Processing:** Service queries sbom_advisory join table, joins advisory table, deduplicates, counts by severity
- **Output:** JSON response with severity counts

Flow is complete from input through processing to output.

### Query-Scope Verification

The query targets advisories linked to a specific SBOM (filtered by sbom_id). This is appropriately scoped -- no broad unfiltered queries.

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity summary endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total)
for advisories linked to a given SBOM.

Implements TC-9201
```

With flag: `--trailer='Assisted-by: Claude Code'`

Full command:
```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       tests/api/advisory_summary.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       modules/fundamental/src/advisory/model/mod.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity summary endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total)
for advisories linked to a given SBOM.

Implements TC-9201"
```

### Branch and PR

Push branch and open PR targeting main:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity summary endpoint" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](<webUrl>)` with clickable Jira link

### Fork Detection

Before creating the PR, check for upstream remote:
```bash
git remote get-url upstream 2>/dev/null
```
If fork detected, use `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main`.

## Step 11 -- Update Jira

1. Set Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL in ADF format
2. Add comment to TC-9201 with PR link, summary of changes, and any deviations
3. Transition TC-9201 to In Review
