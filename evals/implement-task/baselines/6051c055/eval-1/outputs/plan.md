# Implementation Plan: TC-9201 — Add advisory severity aggregation service and endpoint

## Target Branch Extraction

The task specifies **Target Branch: main**. All branch operations will use `main` as the base.

## Branch Operations

1. Ensure the local repository is up-to-date:
   ```
   git fetch origin
   git checkout main
   git pull origin main
   ```
2. Create and check out the feature branch:
   ```
   git checkout -b TC-9201
   ```

## Description Digest Verification (Step 1.5)

Check for a description digest comment on TC-9201 to verify the task description has not changed since planning. Query the Jira issue for comments matching the digest protocol format.

**Result:** No digest comment found on TC-9201. Per `shared/description-digest-protocol.md`, when no digest comment is present, proceed with a warning rather than blocking execution (backward compatibility). Log warning: "No description digest found for TC-9201 — proceeding under backward-compatibility allowance."

## Code Inspection Analysis

Before implementing, inspect sibling code to understand existing patterns.

### advisory/endpoints/get.rs
This file contains the existing GET handler for fetching a single advisory by ID. Key patterns observed:
- Handler function signature: `async fn get_advisory(Path(id): Path<Uuid>, State(state): State<AppState>) -> Result<Json<AdvisoryDetails>, AppError>`
- Uses `AdvisoryService` from the service layer, obtained via `state.advisory_service()`
- Returns `Result<Json<T>, AppError>` — Axum's `Json` extractor handles serialization automatically
- 404 handling: calls the service method, then maps `None` to `AppError::NotFound` using `.ok_or_else(|| AppError::NotFound("advisory not found".into()))?`
- The handler is registered as a method route in `endpoints/mod.rs`

### advisory/service/advisory.rs
This file defines `AdvisoryService` with methods like `fetch` and `list`:
- Methods accept `&self` plus query/filter parameters and a database connection reference (`&ConnectionOrTransaction`)
- Returns `Result<T, AppError>` where errors use `.context("descriptive message")` wrapping
- Database queries use SeaORM's `Entity::find()` builder pattern with `.filter()`, `.join()`, `.all(db)` or `.one(db)`
- The `list` method demonstrates pagination via `PaginatedResults`
- The `fetch` method demonstrates single-entity lookup with optional return (`Option<T>`)

### advisory/model/summary.rs
This file defines `AdvisorySummary` which includes a `severity` field. The severity field is an enum (likely `Severity`) with variants for Critical, High, Medium, Low, and None/Unknown. This confirms the severity data is already modeled and available for aggregation.

### common/src/error.rs
This file defines `AppError` enum with variants:
- `NotFound(String)` — maps to HTTP 404
- `BadRequest(String)` — maps to HTTP 400
- `Internal(anyhow::Error)` — maps to HTTP 500
- Implements `From<anyhow::Error>` for automatic conversion
- The `.context()` method (from anyhow) wraps errors with descriptive messages before conversion

## Files to Modify

### 1. modules/fundamental/src/advisory/model/mod.rs
Add `pub mod severity_summary;` to register the new model module alongside existing model modules.

### 2. modules/fundamental/src/advisory/service/advisory.rs
Add `severity_summary` method to `AdvisoryService` that:
- Accepts an SBOM ID (Uuid) and database connection
- Queries the `sbom_advisory` join table to find all advisories linked to the given SBOM
- Joins with advisory data to retrieve severity levels
- Deduplicates by advisory ID (using `.distinct()` or `HashSet`)
- Aggregates counts per severity level (Critical, High, Medium, Low)
- Returns `Result<Option<SeveritySummary>, AppError>` (None when SBOM does not exist)

### 3. modules/fundamental/src/advisory/endpoints/mod.rs
Register the new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))`
Add `mod severity_summary;` at the top.

## Files to Create

### 4. modules/fundamental/src/advisory/model/severity_summary.rs
Define `SeveritySummary` response struct with fields: `critical: u32`, `high: u32`, `medium: u32`, `low: u32`, `total: u32`. Derive `Serialize`, `Deserialize`, `Clone`, `Debug`, `utoipa::ToSchema`.

### 5. modules/fundamental/src/advisory/endpoints/severity_summary.rs
GET handler `get_severity_summary` following the pattern from `get.rs`:
- Signature: `async fn get_severity_summary(Path(id): Path<Uuid>, State(state): State<AppState>) -> Result<Json<SeveritySummary>, AppError>`
- Calls `AdvisoryService::severity_summary(id, &db).await`
- Maps `None` to 404 using `.ok_or_else()`
- Returns `Json(summary)` on success

### 6. tests/api/advisory_summary.rs
Integration tests:
- `test_advisory_summary_valid_sbom` — seed an SBOM with known advisories at various severity levels, assert correct counts
- `test_advisory_summary_not_found` — request with non-existent SBOM UUID, assert 404
- `test_advisory_summary_empty` — SBOM with no linked advisories, assert all zeros and total 0
- `test_advisory_summary_deduplication` — SBOM with duplicate advisory links, assert each advisory counted once

## Commit

```bash
git add \
  modules/fundamental/src/advisory/model/severity_summary.rs \
  modules/fundamental/src/advisory/model/mod.rs \
  modules/fundamental/src/advisory/service/advisory.rs \
  modules/fundamental/src/advisory/endpoints/severity_summary.rs \
  modules/fundamental/src/advisory/endpoints/mod.rs \
  tests/api/advisory_summary.rs

git commit -m "$(cat <<'EOF'
feat(advisory): add severity aggregation endpoint for SBOM dashboards

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for all unique
advisories linked to a given SBOM. This enables dashboard widgets to
render severity breakdowns without client-side counting.

- Add SeveritySummary model struct
- Add severity_summary method to AdvisoryService
- Add GET handler and route registration
- Add integration tests for valid, empty, 404, and dedup cases

Refs: TC-9201
EOF
)" --trailer='Assisted-by: Claude Code'
```

## Post-Commit

1. Push the branch: `git push -u origin TC-9201`
2. Update Jira ticket TC-9201 status to "In Progress" (or "In Review" if opening a PR)
3. Create pull request targeting `main`
