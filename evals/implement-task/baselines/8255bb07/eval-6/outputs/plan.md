# Implementation Plan: TC-9201 — Add advisory severity aggregation service and endpoint

## Branch Setup

```bash
git checkout main
git pull origin main
git checkout -b TC-9201
```

## Pre-Implementation: Code Inspection

Before modifying any files, inspect the following to understand existing patterns:

1. **Existing endpoint pattern** — read `modules/fundamental/src/advisory/endpoints/get.rs` to understand path param extraction (`Path<Id>`), service call, and JSON response pattern.
2. **Existing service pattern** — read `modules/fundamental/src/advisory/service/advisory.rs` to understand the `fetch` and `list` method signatures (especially `&self, sbom_id: Id, tx: &Transactional<'_>` style).
3. **AdvisorySummary model** — read `modules/fundamental/src/advisory/model/summary.rs` to understand the `severity` field type and structure.
4. **Route registration** — read `modules/fundamental/src/advisory/endpoints/mod.rs` to understand the `Router::new().route(...)` registration pattern.
5. **Model module registration** — read `modules/fundamental/src/advisory/model/mod.rs` to understand how sub-modules are declared.
6. **Join table** — read `entity/src/sbom_advisory.rs` to understand the SBOM-Advisory relationship for querying.
7. **Error handling** — read `common/src/error.rs` to understand `AppError` enum and `.context()` wrapping convention.
8. **Existing integration tests** — read `tests/api/advisory.rs` to understand test setup, assertions, and database fixture patterns.

## Step 1: Create the response model

**Create** `modules/fundamental/src/advisory/model/severity_summary.rs`

- Define `SeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default`, `PartialEq`, `Eq` (following conventions of adjacent model structs).
- Implement a constructor or `Default` so all counts start at 0.

## Step 2: Register the model module

**Modify** `modules/fundamental/src/advisory/model/mod.rs`

- Add `pub mod severity_summary;` to register the new model module alongside existing `summary` and `details` modules.

## Step 3: Add the service method

**Modify** `modules/fundamental/src/advisory/service/advisory.rs`

- Add a `severity_summary` method to `AdvisoryService` following the pattern of `fetch`/`list`:
  - Signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
  - Query the `sbom_advisory` join table to find all advisories linked to the given SBOM ID.
  - Join with the advisory table to get severity values.
  - Deduplicate by advisory ID (use `DISTINCT` or equivalent).
  - Count advisories per severity level (Critical, High, Medium, Low).
  - Return 404 (`AppError`) if the SBOM does not exist, consistent with existing SBOM endpoints.
  - Wrap errors with `.context()` per project convention.

## Step 4: Create the endpoint handler

**Create** `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

- Define an async handler function following the pattern in `get.rs`:
  - Extract path parameter via `Path<Id>` for the SBOM ID.
  - Call `AdvisoryService::severity_summary(sbom_id, tx)`.
  - Return `Json<SeveritySummary>` on success.
  - Return `AppError` on failure (404 for missing SBOM, 500 for unexpected errors).

## Step 5: Register the new route

**Modify** `modules/fundamental/src/advisory/endpoints/mod.rs`

- Add `mod severity_summary;` to import the new handler module.
- Register the route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))` following the existing `Router::new().route(...)` pattern.

## Step 6: Create integration tests

**Create** `tests/api/advisory_summary.rs`

- **Test: valid SBOM with known advisories** — seed the test database with an SBOM linked to advisories of known severities, call `GET /api/v2/sbom/{id}/advisory-summary`, assert correct counts per severity level.
- **Test: non-existent SBOM returns 404** — call the endpoint with a bogus SBOM ID, assert `StatusCode::NOT_FOUND`.
- **Test: SBOM with no advisories returns all zeros** — seed an SBOM with no linked advisories, assert `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`.
- **Test: duplicate advisory links are deduplicated** — seed an SBOM with duplicate advisory links, assert the count reflects unique advisories only.

## Files Summary

| Action | Path |
|--------|------|
| Inspect | `modules/fundamental/src/advisory/endpoints/get.rs` |
| Inspect | `modules/fundamental/src/advisory/service/advisory.rs` |
| Inspect | `modules/fundamental/src/advisory/model/summary.rs` |
| Inspect | `modules/fundamental/src/advisory/model/mod.rs` |
| Inspect | `modules/fundamental/src/advisory/endpoints/mod.rs` |
| Inspect | `entity/src/sbom_advisory.rs` |
| Inspect | `common/src/error.rs` |
| Inspect | `tests/api/advisory.rs` |
| Create | `modules/fundamental/src/advisory/model/severity_summary.rs` |
| Modify | `modules/fundamental/src/advisory/model/mod.rs` |
| Modify | `modules/fundamental/src/advisory/service/advisory.rs` |
| Create | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` |
| Modify | `modules/fundamental/src/advisory/endpoints/mod.rs` |
| Create | `tests/api/advisory_summary.rs` |

No changes needed to `server/src/main.rs` (routes auto-mount via module registration).

## Commit

```bash
git add \
  modules/fundamental/src/advisory/model/severity_summary.rs \
  modules/fundamental/src/advisory/model/mod.rs \
  modules/fundamental/src/advisory/service/advisory.rs \
  modules/fundamental/src/advisory/endpoints/severity_summary.rs \
  modules/fundamental/src/advisory/endpoints/mod.rs \
  tests/api/advisory_summary.rs

git commit \
  -m "feat(advisory): add severity aggregation endpoint for SBOM dashboards

Add SeveritySummary model, AdvisoryService.severity_summary method, and
GET /api/v2/sbom/{id}/advisory-summary endpoint that returns per-severity
advisory counts (critical, high, medium, low, total) for a given SBOM.
Includes integration tests for valid responses, 404 handling, zero-count
defaults, and deduplication.

TC-9201" \
  --trailer='Assisted-by: Claude Code'
```
