# Task 1: Add remediation models and aggregation service

Parent Epic: TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation module's data models and aggregation service. The service queries existing SBOM, advisory, and vulnerability entity relationships to compute remediation statistics grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). No new database tables are created; all data is aggregated from existing entity tables (`sbom`, `advisory`, `sbom_advisory`, `package`, `sbom_package`). The service exposes two methods: one for portfolio-wide summary counts and one for per-product breakdowns.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, re-exports model and service submodules
- `modules/fundamental/src/remediation/model/mod.rs` — model submodule root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary`, `SeverityStatusCount`, and `ProductRemediation` response structs
- `modules/fundamental/src/remediation/service/mod.rs` — service submodule root
- `modules/fundamental/src/remediation/service/remediation.rs` — `RemediationService` with `summary()` and `by_product()` aggregation methods

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` to register the new module

## API Changes
- None (service layer only; endpoints added in Task 2)

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/` — each domain module has `model/` + `service/` + `endpoints/` subdirectories. See `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/` for reference.
- Per CONVENTIONS.md §Module Pattern: structure the remediation module with `model/`, `service/`, and `endpoints/` subdirectories mirroring the sbom module layout. Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's .rs module scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` from all service methods and use `.context()` for error wrapping. Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Response Types: use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the `by_product()` method to support pagination for large portfolios. Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs` in the aggregation queries. Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's .rs scope.
- Aggregation queries should join `sbom_advisory` with `advisory` (for severity) and compute counts using SQL GROUP BY. Use SeaORM query builder following patterns in `modules/fundamental/src/advisory/service/advisory.rs`.
- The `RemediationSummary` struct should contain a `Vec<SeverityStatusCount>` where each entry has `severity: String`, `status: String`, `count: i64`.
- `ProductRemediation` should contain `product_name: String`, `total: i64`, `open: i64`, `in_progress: i64`, `resolved: i64`.
- Respect the p95 < 500ms requirement by keeping aggregation queries efficient — use indexed columns and avoid N+1 patterns.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering and pagination; reuse for aggregation query construction
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper; reuse for `by_product()` return type
- `common/src/error.rs::AppError` — standard error type; reuse for service error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for SeaORM aggregation query patterns and service structure
- `entity/src/advisory.rs` — advisory entity with severity field; join target for severity-based aggregation
- `entity/src/sbom_advisory.rs` — SBOM-advisory join entity; used to correlate vulnerabilities with SBOMs

## Acceptance Criteria
- [ ] `RemediationSummary` struct contains aggregated counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- [ ] `ProductRemediation` struct contains per-product total, open, in_progress, and resolved counts
- [ ] `RemediationService::summary()` returns correct aggregation from existing entity data without creating new database tables
- [ ] `RemediationService::by_product()` returns paginated per-product breakdown using `PaginatedResults<ProductRemediation>`
- [ ] All service methods return `Result<T, AppError>` with proper error context
- [ ] Module compiles and is exported from `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Unit tests for `RemediationService::summary()` verifying correct grouping and counting logic
- [ ] Unit tests for `RemediationService::by_product()` verifying per-product aggregation and pagination
