## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Create the remediation domain model and service layer for aggregating vulnerability remediation status. The model defines types for the severity × status matrix (Critical/High/Medium/Low × Open/In Progress/Resolved), and the service queries existing vulnerability and SBOM relationship data to compute aggregated counts. No new database tables are required — aggregation is computed from existing `advisory`, `sbom_advisory`, and related entity tables.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary struct with severity × status counts
- `modules/fundamental/src/remediation/model/by_product.rs` — ProductRemediation struct with per-product breakdown
- `modules/fundamental/src/remediation/service/mod.rs` — service module root
- `modules/fundamental/src/remediation/service/remediation.rs` — RemediationService with summary and by-product aggregation

## Files to Modify
- `modules/fundamental/src/lib.rs` — register the new remediation module
- `modules/fundamental/Cargo.toml` — add any needed dependencies for the remediation module

## Implementation Notes
- Follow the established module pattern: `model/ + service/ + endpoints/` as seen in `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`.
- The `RemediationSummary` struct should mirror the response shape: a matrix of counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved).
- The `ProductRemediation` struct includes fields: product name, total count, open count, in-progress count, resolved count.
- `RemediationService` queries should use the shared query builder helpers from `common/src/db/query.rs` for filtering and pagination.
- Aggregate from existing entity tables (`entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`) — the non-functional requirement states no new database tables.
- Per Key Conventions: all service methods return `Result<T, AppError>` using `.context()` wrapping from `common/src/error.rs`.
Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust module pattern scope.
- Per Key Conventions: list-style queries should return `PaginatedResults<T>` from `common/src/model/paginated.rs` for the by-product endpoint.
Applies: task creates `modules/fundamental/src/remediation/model/by_product.rs` matching the convention's response type scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults<T>` — standard paginated response wrapper
- `common/src/error.rs::AppError` — error enum with IntoResponse implementation
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — example service pattern to follow for aggregation queries

## Acceptance Criteria
- [ ] `RemediationSummary` struct represents a severity × status count matrix (4 severities × 3 statuses)
- [ ] `ProductRemediation` struct includes product name, total, open, in-progress, and resolved counts
- [ ] `RemediationService::get_summary()` returns aggregated counts from existing entity data
- [ ] `RemediationService::get_by_product()` returns per-product breakdown
- [ ] No new database tables or migrations are created
- [ ] Service methods return `Result<T, AppError>` with proper error context

## Test Requirements
- [ ] Unit tests for `RemediationSummary` and `ProductRemediation` struct construction
- [ ] Service tests verifying correct aggregation from mock entity data
- [ ] Verify no new migration files are created

## Verification Commands
- `cargo check -p trustify-fundamental` — verify compilation
- `cargo test -p trustify-fundamental remediation` — run remediation tests

## Dependencies
- None (first task)
