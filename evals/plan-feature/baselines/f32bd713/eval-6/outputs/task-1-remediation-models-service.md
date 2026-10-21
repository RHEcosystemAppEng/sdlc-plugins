## Repository
trustify-backend

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Target Branch
main

## Description
Add the remediation domain module with data models and an aggregation service that computes vulnerability remediation statistics from existing vulnerability and SBOM relationship data. This module provides the data layer for the remediation tracking dashboard (TC-9006). The service aggregates counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved), and computes per-product remediation breakdowns -- all without creating new database tables.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root, re-exports model and service
- `modules/fundamental/src/remediation/model/mod.rs` -- model module root
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary and RemediationByProduct structs
- `modules/fundamental/src/remediation/service/mod.rs` -- service module root
- `modules/fundamental/src/remediation/service/remediation.rs` -- RemediationService with aggregation methods

## Files to Modify
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` declaration to register the new module
- `modules/fundamental/Cargo.toml` -- add any new dependencies if required for aggregation queries

## Implementation Notes
- Follow the existing domain module pattern used by `sbom/`, `advisory/`, and `package/` modules: each has `model/` + `service/` + `endpoints/` subdirectories. This task creates `model/` and `service/`; endpoints are added in Task 2.
  Per CONVENTIONS.md section Module Pattern: follow model/ + service/ + endpoints/ directory structure.
  Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's Rust module pattern scope.
- RemediationSummary struct should contain a vector of groups, each with `severity: String`, `status: String`, and `count: i64` fields.
- RemediationByProduct struct should contain `product: String`, `total: i64`, `open: i64`, `in_progress: i64`, `resolved: i64` fields.
- RemediationService should query existing tables (`advisory`, `sbom_advisory`, `sbom`, `package`) to compute aggregations. Use SeaORM query patterns consistent with existing services.
- All service methods must return `Result<T, AppError>` using the error type from `common/src/error.rs`, with `.context()` wrapping on fallible operations.
  Per CONVENTIONS.md section Error Handling: all handlers return Result<T, AppError> with .context() wrapping.
  Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust handler scope.
- Use shared query builder helpers from `common/src/db/query.rs` for filtering and sorting support in the service layer.
- The non-functional requirement specifies p95 < 500ms for the summary endpoint and handling up to 10,000 tracked vulnerabilities -- design queries with appropriate indexing and avoid N+1 patterns.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` -- shared query builder helpers for filtering, pagination, and sorting; use for building aggregation queries
- `common/src/model/paginated.rs::PaginatedResults<T>` -- response wrapper for paginated list results; use for by-product endpoint response in Task 2
- `common/src/error.rs::AppError` -- error enum implementing IntoResponse; use for all Result return types
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- reference for how severity fields are modeled in existing code
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- reference for service pattern with database queries

## Acceptance Criteria
- [ ] `RemediationSummary` struct defined with counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- [ ] `RemediationByProduct` struct defined with total, open, in_progress, resolved counts per product
- [ ] `RemediationService` implemented with methods to compute both aggregation types from existing database tables
- [ ] No new database tables or migrations created -- all data computed from existing `advisory`, `sbom_advisory`, `sbom`, and `package` tables
- [ ] All service methods return `Result<T, AppError>` with proper error context
- [ ] Module registered in `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Unit tests for `RemediationService` aggregation logic verifying correct grouping by severity x status
- [ ] Unit tests verifying correct per-product breakdown computation
- [ ] Test that empty dataset returns zero counts without errors
- [ ] Test that service methods propagate database errors correctly via `AppError`

## Verification Commands
- `cargo build -p trustify-fundamental` -- verify the module compiles without errors
- `cargo test -p trustify-fundamental -- remediation` -- run remediation module unit tests

## Dependencies
- None (first task in the dependency chain)
