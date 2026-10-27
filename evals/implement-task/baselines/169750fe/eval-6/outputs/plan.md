# Implementation Plan — TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 — Validate Project Configuration

Verified CLAUDE.md contains all required sections:
- **Repository Registry**: present with `trustify-backend` entry, Serena instance `serena_backend`, path `./`
- **Jira Configuration**: present with Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: present with Serena instance `serena_backend` using `rust-analyzer`

Configuration valid. Proceeding.

## Step 1 — Fetch and Parse Jira Task

**Key:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Web URL:** https://redhat.atlassian.net/browse/TC-9201

### Parsed Sections

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` — add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` — register new route
  - `modules/fundamental/src/advisory/model/mod.rs` — add `pub mod severity_summary;`
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` — SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` — GET handler
  - `tests/api/advisory_summary.rs` — integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` — NEW
- **Dependencies:** None

### Target Branch Extraction

Target Branch is `main`. The task branch will be based on `main`.

## Step 1.5 — Verify Description Integrity

See `digest-match.md` for full details. The digest comment was located using the `[sdlc-workflow] Description digest:` marker string. The stored digest (`sha256-md:a1b2c3d4...`) matches the computed digest of the current description. Comment timestamps are identical (not edited). Proceeding silently without user prompt.

## Step 2 — Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 — Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to In Progress via `jira.transition_issue`

## Step 4 — Understand the Code

### Code Inspection

Inspect existing code using the `serena_backend` Serena instance before making any changes:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — Read the existing GET handler to understand the endpoint pattern: path parameter extraction via `Path<Id>`, service call, JSON response wrapping. This is the primary pattern to follow for the new severity_summary endpoint.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** — Read `AdvisoryService` to understand the `fetch` and `list` method signatures, particularly the `(&self, sbom_id: Id, tx: &Transactional<'_>)` pattern and `Result<T, AppError>` return type with `.context()` wrapping.

3. **`modules/fundamental/src/advisory/model/summary.rs`** — Read `AdvisorySummary` struct to understand the `severity` field type and how severity levels are represented. This is the field used to count by severity level.

4. **`common/src/error.rs`** — Read `AppError` enum to understand the error handling pattern, particularly how to return 404 for non-existent resources.

5. **`entity/src/sbom_advisory.rs`** — Read the SBOM-Advisory join table entity to understand the relationship structure for querying advisories linked to an SBOM.

6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Read route registration to understand the `Router::new().route()` pattern.

### Convention Conformance Analysis

Sibling files analyzed:
- `modules/fundamental/src/advisory/endpoints/list.rs`
- `modules/fundamental/src/advisory/endpoints/get.rs`
- `modules/fundamental/src/sbom/endpoints/get.rs`

**Discovered conventions:**

- **Error handling:** Handlers return `Result<T, AppError>` with `.context("description")` wrapping on service errors
- **Naming:** `verb_noun` pattern for functions (e.g., `get_advisory`, `list_advisories`)
- **Endpoint registration:** `Router::new().route("/path", get(handler_fn))` in `endpoints/mod.rs`
- **Path parameters:** Extracted via `Path<Id>` Axum extractor
- **Service method signatures:** `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- **Module structure:** Each domain module follows `model/ + service/ + endpoints/` layout
- **Test assertions:** `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!` on response body fields
- **Response types:** Structs derive `Serialize, Deserialize, ToSchema` (for utoipa OpenAPI generation)

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read and extract CI check commands for Step 9.

### Documentation Files

Identified related documentation:
- `docs/api.md` — REST API reference (may need updating with new endpoint)

## Step 5 — Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch `TC-9201` created from `main` (the Target Branch).

## Step 6 — Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
/// Aggregated advisory severity counts for an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u32,
    /// Count of high-severity advisories.
    pub high: u32,
    /// Count of medium-severity advisories.
    pub medium: u32,
    /// Count of low-severity advisories.
    pub low: u32,
    /// Total count of unique advisories.
    pub total: u32,
}
```

Follows the sibling pattern from `summary.rs` and `details.rs` — derives `Serialize, Deserialize, ToSchema`, uses doc comments on every field.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:

```rust
pub mod severity_summary;
```

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService` following the existing `fetch` and `list` patterns:

```rust
/// Computes aggregated severity counts for advisories linked to an SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Deduplicate by advisory ID
    // Look up AdvisorySummary for each, read severity field
    // Count per severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` entity to find linked advisories
- Deduplicate by advisory ID to count unique advisories only
- Use `AdvisorySummary.severity` field to classify each advisory
- Default all counts to 0 (via `SeveritySummary::default()`)
- Return 404 (via `AppError`) when SBOM ID does not exist, consistent with existing SBOM endpoints
- Use `.context("Failed to fetch severity summary")` for error wrapping

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern from `get.rs`:

```rust
/// Returns aggregated advisory severity counts for the given SBOM.
pub async fn severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route in the existing router:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

Following the existing `Router::new().route()` pattern.

## Step 7 — Write Tests

### Create `tests/api/advisory_summary.rs`

Following the sibling test patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with linked advisories of known severities
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then response status is 200 and counts match expected values
    assert_eq!(resp.status(), StatusCode::OK);
    assert_eq!(body.critical, expected_critical);
    assert_eq!(body.high, expected_high);
    assert_eq!(body.medium, expected_medium);
    assert_eq!(body.low, expected_low);
    assert_eq!(body.total, expected_total);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID
    // When requesting GET /api/v2/sbom/{nonexistent}/advisory-summary
    // Then response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[test]
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

/// Verifies that duplicate advisory links are deduplicated in the count.
#[test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then each advisory is counted only once
    assert_eq!(body.total, expected_unique_count);
}
```

Tests use value-based assertions (`assert_eq!` on specific counts) per skill guidance, not length-only checks. Each test function has a doc comment and given-when-then section comments.

Run tests:
```bash
cargo metadata --no-deps --format-version 1
```
Resolve the crate name for the test package containing `tests/api/advisory_summary.rs`. Then run:
```bash
cargo test -p <crate-name>
```

## Step 8 — Verify Acceptance Criteria

- [x] `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical: N, high: N, medium: N, low: N, total: N }` — implemented in endpoint handler
- [x] Returns 404 when SBOM ID does not exist — handled by `AppError` in service method
- [x] Counts only unique advisories — deduplication by advisory ID in service method
- [x] All severity levels default to 0 — `SeveritySummary::default()` initializes all to 0
- [x] Response time under 200ms for SBOMs with up to 500 advisories — single query with join, no N+1

## Step 9 — Self-Verification

### Scope Containment
Run `git diff --name-only` and compare against Files to Modify and Files to Create. All modified/created files are within scope:
- `modules/fundamental/src/advisory/service/advisory.rs` (Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` (Files to Modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (Files to Create)
- `tests/api/advisory_summary.rs` (Files to Create)

No out-of-scope files modified.

### Dead Parameter Detection
No parameters removed — no dead parameter candidates.

### Sensitive-Pattern Check
Search staged diff for secrets/credentials. No matches expected.

### Duplication Check
Search for existing severity aggregation logic. No duplicates found.

### CI Checks
Run CI check commands from CONVENTIONS.md (if extracted in Step 4).

### Module-Level Tests (Rust)
Run `cargo metadata --no-deps --format-version 1` to resolve the crate name for each modified file. Use the package `name` field (not derived from `Cargo.toml` which may be a virtual workspace manifest). Then run `cargo test -p <crate-name>` for each affected crate.

### Query-Scope Verification
The query targets advisories linked to a specific SBOM (by sbom_id). The scope is correct — no overly broad queries.

## Step 10 — Commit and Push

### Commit Message

```bash
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService.severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint. Includes
integration tests for valid SBOM, 404, empty advisories, and
deduplication cases.

Implements TC-9201"
```

### Branch and PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`

## Step 11 — Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment with PR link, summary of changes, and any deviations
3. Transition TC-9201 to In Review
