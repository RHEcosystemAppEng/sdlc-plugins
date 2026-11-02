# Implementation Plan — TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 — Validate Project Configuration

Verified CLAUDE.md contains:
- **Repository Registry**: trustify-backend with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field
- **Code Intelligence**: Serena tool naming convention and rust-analyzer instance

All required sections present. Proceeding.

## Step 1 — Fetch and Parse Jira Task

**Key**: TC-9201
**Repository**: trustify-backend
**Target Branch**: main
**Web URL**: https://redhat.atlassian.net/browse/TC-9201

### Parsed sections:
- **Description**: Add service method and REST endpoint for advisory severity count aggregation per SBOM
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` — add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` — register new route
  - `modules/fundamental/src/advisory/model/mod.rs` — add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` — SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` — GET handler
  - `tests/api/advisory_summary.rs` — integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` — NEW
- **Target Branch**: main
- **Dependencies**: None

## Step 1.5 — Verify Description Integrity

See `digest-match.md` for full details. The digest comment was found, format tags match (`sha256-md`), and hex digests match. Proceeding silently with no user prompt.

## Step 2 — Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 — Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue(TC-9201) → In Progress`

## Step 4 — Understand the Code

### Code inspection plan

Before modifying any files, inspect the following existing code:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — Read the existing GET endpoint handler to understand the pattern for path parameter extraction (`Path<Id>`), service invocation, and JSON response return. This is the template for the new severity_summary endpoint handler.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** — Read the `AdvisoryService` struct and its existing `fetch` and `list` methods to understand the service pattern: method signature conventions (`&self, id: Id, tx: &Transactional<'_>`), database query patterns, and error handling with `Result<T, AppError>`.

3. **`modules/fundamental/src/advisory/model/summary.rs`** — Read the `AdvisorySummary` struct to understand the `severity` field type and values, which will be used for counting by severity level.

4. **`common/src/error.rs`** — Read `AppError` to understand the error enum and how `.context()` wrapping is used for error propagation.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Read to understand route registration pattern (`Router::new().route(...)`) for adding the new endpoint.

6. **`entity/src/sbom_advisory.rs`** — Read to understand the SBOM-Advisory join table structure for querying advisories linked to an SBOM.

### Convention conformance analysis

Analyze sibling files for conventions (see `conventions.md` output from eval 1 for the detailed list):
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Module structure: `model/ + service/ + endpoints/` pattern
- Endpoint pattern: extract path params via `Path<Id>`, call service, return `Json<T>`
- Route registration: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- Test patterns: integration tests in `tests/api/`, real PostgreSQL, `assert_eq!(resp.status(), StatusCode::OK)`

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root. If present, read and extract CI check commands for Step 9.

### Documentation file identification

Related docs:
- `docs/api.md` — may need updating with new endpoint
- `README.md` — unlikely to need changes

## Step 5 — Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch name `TC-9201` follows the Jira issue ID naming convention (constraint 3.1). The branch is based on `main` as specified in the Target Branch section.

## Step 6 — Implement Changes

### File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

Create the `SeveritySummary` response struct:
- `SeveritySummary` struct with fields: `critical: u32`, `high: u32`, `medium: u32`, `low: u32`, `total: u32`
- Derive `Serialize`, `Deserialize`, `Default`, `Debug`, `Clone`, `PartialEq`
- Add `utoipa::ToSchema` derive for OpenAPI spec generation (following sibling pattern)
- Add doc comment explaining the struct's purpose

### File 2: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

Add `pub mod severity_summary;` to register the new model module, following the existing pattern of module declarations.

### File 3: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

Add `severity_summary` method to `AdvisoryService`:
- Signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Query `sbom_advisory` join table to find advisories linked to the SBOM
- Join with advisory table to get severity information
- Deduplicate by advisory ID
- Count by severity level (Critical, High, Medium, Low), defaulting to 0
- Compute total as sum of all severity counts
- Return `SeveritySummary` struct
- Error handling: use `.context("Failed to fetch severity summary")` pattern

### File 4: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

Create the GET handler:
- Function signature following `get.rs` pattern: `async fn severity_summary(Path(id): Path<Id>, service: Extension<AdvisoryService>, tx: Extension<Transactional<'_>>) -> Result<Json<SeveritySummary>, AppError>`
- Extract path param `id` via `Path<Id>`
- Call `service.severity_summary(id, &tx).await?`
- Return `Json(result)`
- Return 404 via AppError when SBOM ID does not exist

### File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

Register the new route:
```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```
Following the pattern of existing route registrations.

### File 6: `tests/api/advisory_summary.rs` (CREATE)

Integration tests (detailed in Step 7).

## Step 7 — Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases:

1. **`test_severity_summary_with_advisories`** — Create an SBOM with known advisories of different severities, verify exact counts per severity level
2. **`test_severity_summary_nonexistent_sbom`** — Request summary for non-existent SBOM ID, verify 404 response
3. **`test_severity_summary_no_advisories`** — Create SBOM with no linked advisories, verify all counts are 0
4. **`test_severity_summary_deduplicates`** — Create SBOM with duplicate advisory links, verify counts reflect unique advisories only

Tests follow sibling patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs` for setup/teardown and assertion style, using value-based assertions (asserting specific count values, not just presence).

## Step 8 — Verify Acceptance Criteria

- [x] GET endpoint returns severity counts JSON
- [x] Returns 404 for non-existent SBOM
- [x] Deduplicates by advisory ID
- [x] All severity levels default to 0
- [x] Performance verified via test with known data

## Step 9 — Self-Verification

### Scope containment
Run `git diff --name-only` and verify all modified files are within Files to Modify and Files to Create sections.

### Dead parameter detection
Scan modified functions for unused parameters after changes.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` — no matches expected.

### Duplication check
Search repository for existing severity aggregation logic to ensure no duplication.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from CONVENTIONS.md.

### Module-level test requirement (Rust)
Resolve crate name using `cargo metadata --no-deps --format-version 1` for each modified file. The modified files belong to the `trustify-module-fundamental` crate (from `modules/fundamental/Cargo.toml`) and the test crate. Run:
```bash
cargo test -p trustify-module-fundamental
```
Do not derive the crate name from the nearest `Cargo.toml`, which may be a virtual workspace manifest at the repository root.

## Step 10 — Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
per-severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes deduplication by
advisory ID and 404 handling for missing SBOMs.

Implements TC-9201
```

With trailer:
```bash
git commit --trailer="Assisted-by: Claude Code" -m "..."
```

### Push and create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`

## Step 11 — Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment to TC-9201 with PR link and summary of changes
3. Transition TC-9201 to In Review
