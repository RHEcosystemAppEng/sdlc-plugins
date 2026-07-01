# Task 2 — Add remediation service and model layer

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Create the remediation domain module following the established `model/ + service/ + endpoints/` pattern. This task adds the model structs for remediation summary and per-product breakdown, and the service layer that computes aggregations from existing vulnerability and SBOM advisory relationship data. No new database tables are needed — all aggregations are computed by querying the existing `advisory`, `sbom_advisory`, and `sbom` entities.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` struct with counts by severity x status
- `modules/fundamental/src/remediation/model/product.rs` — `ProductRemediation` struct with per-product total/open/resolved counts
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with `get_summary()` and `get_by_product()` methods

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` to register the new module
- `modules/fundamental/Cargo.toml` — add any needed dependencies (if not already present)

## Implementation Notes
- Follow the existing module pattern established by `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`: each domain module has `model/`, `service/`, and `endpoints/` sub-modules.
- The `RemediationSummary` struct should mirror the pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`).
- Use `common/src/db/query.rs` for shared query builder helpers (filtering, pagination, sorting).
- All handlers must return `Result<T, AppError>` with `.context()` wrapping, following the error handling pattern in `common/src/error.rs`.
- Aggregation queries should join `advisory` (which has severity), `sbom_advisory` (join table), and `sbom` (which represents products) to compute remediation counts. No new database tables are permitted per the non-functional requirements.
- Per the p95 < 500ms response time requirement, consider query optimization and ensure efficient aggregation queries.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper for list endpoints
- `common/src/error.rs` — `AppError` enum for consistent error handling
- `entity/src/advisory.rs` — Advisory entity with severity field
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for correlating vulnerabilities to products

## Acceptance Criteria
- [ ] `RemediationSummary` struct exists with fields for counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- [ ] `ProductRemediation` struct exists with fields for product name, total, open, and resolved counts
- [ ] `RemediationService::get_summary()` returns aggregated counts from existing advisory and SBOM data
- [ ] `RemediationService::get_by_product()` returns per-product breakdown from existing SBOM-advisory relationships
- [ ] No new database tables or migrations are created
- [ ] Module is registered in `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Unit tests for `RemediationService::get_summary()` verifying correct aggregation by severity and status
- [ ] Unit tests for `RemediationService::get_by_product()` verifying correct per-product breakdown
- [ ] Test that aggregation handles empty datasets (no advisories, no SBOMs) gracefully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
