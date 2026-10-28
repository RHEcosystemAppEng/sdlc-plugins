## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation module with model types and service layer for computing vulnerability remediation aggregations. The service queries existing vulnerability-SBOM relationship data (no new database tables) to produce aggregated counts by severity and status, and per-product remediation breakdowns. This is the foundation layer that the remediation REST endpoints (Task 2) will call.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, re-exports model and service
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary`, `SeverityStatusCount`, and `ProductRemediation` structs with Serialize derives
- `modules/fundamental/src/remediation/service/mod.rs` — service module root
- `modules/fundamental/src/remediation/service/remediation.rs` — `RemediationService` with methods `get_summary()` and `get_by_product()` that query existing entities

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` to register the new module
- `modules/fundamental/Cargo.toml` — add any additional dependencies if needed for aggregation queries

## Implementation Notes
- Follow the established domain module pattern: each module under `modules/fundamental/src/` uses the `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/` for the reference implementation.
- The `RemediationSummary` struct should contain a matrix of severity (Critical/High/Medium/Low) crossed with status (Open/In Progress/Resolved), each entry holding a count. Model it as a `Vec<SeverityStatusCount>` where `SeverityStatusCount` has `severity: String`, `status: String`, `count: i64`.
- The `ProductRemediation` struct should contain `product_name: String`, `total: i64`, `open: i64`, `resolved: i64`.
- The service should query existing entities: `sbom` (entity/src/sbom.rs), `advisory` (entity/src/advisory.rs), and `sbom_advisory` (entity/src/sbom_advisory.rs) join table to compute aggregations.
- Use SeaORM query builder for aggregation queries. Reuse `common/src/db/query.rs` helpers for building filtered queries.
- All service methods should return `Result<T, AppError>` using the error type from `common/src/error.rs`, with `.context()` wrapping for error messages.
- The non-functional requirement specifies p95 < 500ms for the summary endpoint. Design queries to compute aggregations in a single SQL query using GROUP BY rather than fetching all records and aggregating in Rust.
- Per Key Conventions: error handling uses `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` — shared query builder helpers for filtering, pagination, and sorting; reuse for building aggregation queries
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper for list endpoints; will be used by the by-product endpoint if pagination is needed
- `common/src/error.rs::AppError` — error enum implementing IntoResponse; use for all service error returns
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference implementation for the service pattern with SeaORM queries

## Acceptance Criteria
- [ ] `RemediationSummary` struct serializes to JSON with severity x status count entries
- [ ] `ProductRemediation` struct serializes to JSON with product name, total, open, and resolved counts
- [ ] `RemediationService::get_summary()` returns aggregated counts grouped by severity and status from existing vulnerability-SBOM data
- [ ] `RemediationService::get_by_product()` returns per-product breakdown from existing data
- [ ] All service methods return `Result<T, AppError>` with proper error context
- [ ] Module is registered in `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Unit test for `RemediationSummary` serialization to JSON
- [ ] Unit test for `ProductRemediation` serialization to JSON
- [ ] Service method tests with mock database state verifying correct aggregation logic

## Dependencies
- None (first task in the backend Epic)
