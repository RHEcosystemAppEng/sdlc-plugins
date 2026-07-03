## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add a new remediation sub-module under modules/fundamental with model types and an aggregation service. The service computes remediation status counts from existing advisory and SBOM entity data without creating new database tables. It aggregates vulnerability counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved), and also provides per-product breakdowns with total, open, and resolved counts.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- module declaration and re-exports
- `modules/fundamental/src/remediation/model/mod.rs` -- model module declaration
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary and ProductRemediation structs
- `modules/fundamental/src/remediation/service/mod.rs` -- RemediationService with aggregation query logic

## Files to Modify
- `modules/fundamental/src/lib.rs` -- register the new remediation sub-module
- `modules/fundamental/Cargo.toml` -- add any required dependencies for the remediation module

## API Changes
- NEW internal service: `RemediationService::get_summary()` -- returns aggregated counts by severity and status
- NEW internal service: `RemediationService::get_by_product()` -- returns per-product remediation breakdown

## Implementation Notes
- Follow the existing module pattern in modules/fundamental/src/: each domain has model/ + service/ + endpoints/ sub-directories. See `modules/fundamental/src/sbom/` for the established structure.
- Model structs (RemediationSummary, ProductRemediation) should follow the pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary).
- The aggregation service should query across existing entities: `entity/src/advisory.rs` (Advisory entity with severity), `entity/src/sbom.rs` (SBOM entity), and `entity/src/sbom_advisory.rs` (SBOM-Advisory join table).
- Use the shared query helpers from `common/src/db/query.rs` for filtering and pagination support.
- All service methods must return `Result<T, AppError>` using the error type from `common/src/error.rs`, with `.context()` wrapping per project convention.
- No new database tables -- compute all aggregations from existing entity relationships using SeaORM queries.
- p95 response time target is < 500ms for summary queries; consider efficient SQL aggregation rather than in-memory processing.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` -- shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults<T>` -- response wrapper for list endpoints (use for by-product endpoint if paginated)
- `common/src/error.rs::AppError` -- standard error type with IntoResponse implementation
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- reference pattern for service implementation that queries advisory data

## Acceptance Criteria
- [ ] RemediationSummary struct contains counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved)
- [ ] ProductRemediation struct contains per-product breakdown with total, open, and resolved counts
- [ ] RemediationService::get_summary() returns correct aggregated counts from existing advisory/SBOM data
- [ ] RemediationService::get_by_product() returns correct per-product breakdown
- [ ] No new database tables or migrations are created
- [ ] All methods return Result<T, AppError> with proper error context

## Test Requirements
- [ ] Unit test for RemediationService::get_summary() verifying correct aggregation across severity levels and statuses
- [ ] Unit test for RemediationService::get_by_product() verifying correct per-product breakdown
- [ ] Test that empty dataset returns zero counts without errors
- [ ] Test that aggregation handles up to 10,000 vulnerability records without performance degradation

## Verification Commands
- `cargo build -p trustify-fundamental` -- verify the module compiles
- `cargo test -p trustify-fundamental -- remediation` -- run remediation-related tests

## Dependencies
- None (first task in the backend Epic)
