# Implementation Plan: TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Dependencies**: None

## Pre-Implementation Validation

### Step 0 -- Project Configuration Validation
- Repository Registry: present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
- Jira Configuration: present, contains project key `TC`, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: present, with `serena_backend` instance using `rust-analyzer`
- Result: PASS -- all required sections present

### Step 1 -- Task Parsing
- Repository: trustify-backend
- Target Branch: main
- Target PR: not present (standard flow)
- Bookend Type: not present (standard flow)
- Dependencies: none
- GitHub Issue custom field: `customfield_10747` configured, would check for value on fetched issue
- Description integrity: would verify via digest protocol (Step 1.5)

### Step 3 -- Jira Transition
- Would assign to current user via `jira.user_info()` + `jira.edit_issue()`
- Would transition TC-9201 to "In Progress"

---

## Files to Modify

| # | File | Change Summary |
|---|------|---------------|
| 1 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model submodule |
| 2 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 3 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new severity summary route and import the handler module |

## Files to Create

| # | File | Purpose |
|---|------|---------|
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 6 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files NOT Modified (confirmed)

- `server/src/main.rs` -- no changes needed; routes auto-mount via module registration

---

## Step 4 -- Code Understanding

### Sibling Analysis
- **Model siblings**: `summary.rs` (AdvisorySummary with severity field), `details.rs` (AdvisoryDetails) -- both in `modules/fundamental/src/advisory/model/`
- **Service sibling**: `advisory.rs` (AdvisoryService with `fetch`, `list`, `search`) -- in `modules/fundamental/src/advisory/service/`
- **Endpoint siblings**: `list.rs` (GET /api/v2/advisory), `get.rs` (GET /api/v2/advisory/{id}) -- in `modules/fundamental/src/advisory/endpoints/`
- **Cross-domain siblings**: `sbom/` module follows identical model/service/endpoints structure
- **Entity reference**: `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table for the query

### CONVENTIONS.md
- `CONVENTIONS.md` exists at repository root -- would read for CI check commands and code generation commands
- Verification commands would be extracted and run in Step 9

### Documentation Files Identified
- `docs/architecture.md` -- system architecture overview
- `docs/api.md` -- REST API reference (would need updating for new endpoint)
- `README.md` -- repository README

### Reusable Code Identified
- `AdvisorySummary.severity` field in `modules/fundamental/src/advisory/model/summary.rs` -- use this to extract severity from each advisory
- `AppError` in `common/src/error.rs` -- use for error handling
- `PaginatedResults<T>` in `common/src/model/paginated.rs` -- NOT needed (single aggregate response, not a list)
- Query helpers in `common/src/db/query.rs` -- may use for filtering
- `sbom_advisory` entity in `entity/src/sbom_advisory.rs` -- use for the join query

---

## Step 6 -- Implementation Details

### File 1: Model module registration (`model/mod.rs`)
- Add `pub mod severity_summary;` alongside existing `pub mod summary;` and `pub mod details;`

### File 2: Service method (`service/advisory.rs`)
- Add `severity_summary` method to `AdvisoryService`
- Method signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Query logic: join `sbom_advisory` with `advisory` for the given `sbom_id`, extract severity from each linked `AdvisorySummary`, count by severity level, deduplicate by advisory ID
- Return `SeveritySummary` with counts for critical, high, medium, low, and total
- Error handling: return 404 via `AppError` if SBOM does not exist

### File 3: Route registration (`endpoints/mod.rs`)
- Add `mod severity_summary;` to import the handler module
- Add `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))` to the router chain

### File 4: Response struct (`model/severity_summary.rs`)
- Define `SeveritySummary` struct with `#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]`
- Fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- All fields default to 0
- Add documentation comment on the struct

### File 5: Endpoint handler (`endpoints/severity_summary.rs`)
- Define `get_severity_summary` handler function
- Signature: `pub async fn get_severity_summary(Path(id): Path<Id>, State(service): State<AdvisoryService>, tx: Transactional<'_>) -> Result<Json<SeveritySummary>, AppError>`
- Extract path param `id`, call `service.severity_summary(id, &tx)`, return `Json(result)`
- Error handling: propagate `AppError` from service layer
- Documentation comment on the function

### File 6: Integration tests (`tests/api/advisory_summary.rs`)
- Test 1: `test_valid_sbom_severity_counts` -- create SBOM with known advisories at various severity levels, call endpoint, assert exact counts match
- Test 2: `test_nonexistent_sbom_returns_404` -- call endpoint with bogus SBOM ID, assert 404 status
- Test 3: `test_sbom_with_no_advisories_returns_zeros` -- create SBOM with no linked advisories, assert all counts are 0
- Test 4: `test_duplicate_advisories_are_deduplicated` -- create SBOM with duplicate advisory links, assert counts reflect unique advisories only
- All tests use given-when-then section comments
- All tests have `///` documentation comments
- Value-based assertions on exact count values, not just total/length

---

## Step 7 -- Test Execution

- Run: `cargo test -p trustify-fundamental` (for the service/model changes)
- Run: `cargo test --test advisory_summary` (for integration tests)
- Fix any failures before proceeding

## Step 8 -- Acceptance Criteria Verification

| Criterion | Verification Method |
|-----------|-------------------|
| GET endpoint returns severity counts | Integration test `test_valid_sbom_severity_counts` |
| 404 for non-existent SBOM | Integration test `test_nonexistent_sbom_returns_404` |
| Deduplicates by advisory ID | Integration test `test_duplicate_advisories_are_deduplicated` |
| All severity levels default to 0 | Integration test `test_sbom_with_no_advisories_returns_zeros` |
| Response time under 200ms for 500 advisories | Would verify with a load/benchmark test or manual check |

## Step 9 -- Self-Verification Checklist

- [ ] Scope containment: `git diff --name-only` matches Files to Modify + Files to Create
- [ ] Untracked file check: `git status --short` for stray files
- [ ] Dead parameter detection: scan modified functions for unused params
- [ ] Sensitive-pattern check: grep staged diff for secrets/credentials
- [ ] Documentation currency: update `docs/api.md` if it documents endpoints
- [ ] Duplication check: search for existing severity aggregation logic
- [ ] CI checks from CONVENTIONS.md: run all extracted commands
- [ ] Module-level test (Rust): `cargo test -p <crate-name>` for every crate with modified files
- [ ] Data-flow trace: input (HTTP GET with SBOM ID) -> processing (query join table, count severities, deduplicate) -> output (JSON response with counts)
- [ ] Contract & sibling parity: verify handler signature matches sibling `get.rs` pattern, service method matches `fetch`/`list` pattern

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes deduplication by advisory ID and proper 404
handling for non-existent SBOMs.

Implements TC-9201
```

Commit flag: `--trailer="Assisted-by: Claude Code"`

### Branch and PR

- Branch name: `TC-9201`
- Base branch: `main`
- PR title: `feat(advisory): add severity aggregation endpoint for SBOM advisories`
- PR body includes: summary of changes, link to Jira issue `[TC-9201](https://redhat.atlassian.net/browse/TC-9201)`, test plan

## Step 11 -- Jira Update

- Update `customfield_10875` (Git Pull Request) with PR URL in ADF format
- Add comment to TC-9201 with PR link, summary of changes, and confirmation of acceptance criteria
- Transition TC-9201 to "In Review"
