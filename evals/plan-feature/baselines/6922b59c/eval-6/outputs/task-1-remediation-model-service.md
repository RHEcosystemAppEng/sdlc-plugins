## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add the remediation domain module with model structs and an aggregation service for
computing vulnerability remediation status across ingested SBOMs. The service queries
existing vulnerability and SBOM relationship data to produce aggregated counts by
severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved), as well
as per-product breakdowns. No new database tables are required — all aggregations are
computed from existing entity relationships.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation domain module root
- `modules/fundamental/src/remediation/model/mod.rs` — model sub-module root, re-exports structs
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` and `SeverityStatusCount` structs for the summary endpoint response
- `modules/fundamental/src/remediation/model/product.rs` — `ProductRemediation` struct for the by-product endpoint response
- `modules/fundamental/src/remediation/service/mod.rs` — service sub-module root
- `modules/fundamental/src/remediation/service/remediation.rs` — `RemediationService` with `get_summary()` and `get_by_product()` aggregation methods

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` to register the new domain module
- `modules/fundamental/Cargo.toml` — add any new dependencies if required

## Implementation Notes
- Follow the established domain module pattern: each module has `model/` + `service/` + `endpoints/` sub-modules. See `modules/fundamental/src/sbom/` for the reference implementation.
  Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure for the remediation module.
  Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's Rust module file scope.
- Use `Result<T, AppError>` with `.context()` wrapping for all service methods, consistent with the error handling pattern in `common/src/error.rs`.
  Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's `.rs` file scope.
- Use the shared query builder helpers from `common/src/db/query.rs` for filtering and pagination in aggregation queries.
- The `RemediationSummary` struct should contain a `Vec<SeverityStatusCount>` where each entry has `severity: String`, `status: String`, and `count: i64` fields, plus top-level `total_open`, `total_in_progress`, and `total_resolved` counts.
- The `ProductRemediation` struct should contain `product_name: String`, `total: i64`, `open: i64`, `resolved: i64` fields.
- Aggregation queries join existing entities: `sbom` -> `sbom_advisory` -> `advisory` to compute counts grouped by severity and status fields from `AdvisorySummary`.
- Non-functional requirement: summary aggregation must achieve p95 < 500ms. Use efficient SQL GROUP BY queries rather than in-memory aggregation.
- No new database tables — compute all aggregations from existing `sbom`, `advisory`, `sbom_advisory` entity relationships.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering, pagination, and sorting; use for building aggregation queries
- `common/src/model/paginated.rs::PaginatedResults` — standard response wrapper for paginated list endpoints; use for by-product endpoint if pagination is needed
- `common/src/error.rs::AppError` — error enum with `IntoResponse` implementation; use for all service error returns
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct design and serialization patterns
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service implementation patterns including database query construction

## Acceptance Criteria
- [ ] `RemediationSummary` struct is defined with severity/status counts and top-level totals
- [ ] `SeverityStatusCount` struct has `severity`, `status`, and `count` fields
- [ ] `ProductRemediation` struct has `product_name`, `total`, `open`, and `resolved` fields
- [ ] `RemediationService` has a `get_summary()` method that returns aggregated counts by severity and status
- [ ] `RemediationService` has a `get_by_product()` method that returns per-product remediation breakdowns
- [ ] Service queries use existing entity relationships (sbom, advisory, sbom_advisory) without creating new tables
- [ ] All service methods use `Result<T, AppError>` error handling pattern
- [ ] The remediation module is registered in `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Unit test for `RemediationService::get_summary()` verifying correct severity/status grouping
- [ ] Unit test for `RemediationService::get_by_product()` verifying correct product breakdown calculation
- [ ] Verify all model structs implement `Serialize` and `Deserialize`
- [ ] Verify service returns empty results gracefully when no vulnerability data exists

## Verification Commands
- `cargo check -p trustify-module-fundamental` — verify compilation of the new module
- `cargo test -p trustify-module-fundamental -- remediation` — run remediation-specific tests

## Dependencies
- None (first task in the implementation sequence)
