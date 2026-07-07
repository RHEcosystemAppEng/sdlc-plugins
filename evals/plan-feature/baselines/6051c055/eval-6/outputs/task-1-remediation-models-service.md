## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation domain module with model structs and an aggregation service layer. This module provides the data layer for the vulnerability remediation tracking dashboard (TC-9006). The service computes aggregated remediation counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved) from existing vulnerability and SBOM relationship data, without creating new database tables.

The module follows the established `model/ + service/` pattern used by existing domain modules (sbom, advisory, package) under `modules/fundamental/src/`.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, re-exports model and service submodules
- `modules/fundamental/src/remediation/model/mod.rs` — model submodule root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary struct with counts grouped by severity x status
- `modules/fundamental/src/remediation/model/by_product.rs` — ProductRemediation struct with per-product total, open, and resolved counts
- `modules/fundamental/src/remediation/service/mod.rs` — service submodule root
- `modules/fundamental/src/remediation/service/remediation.rs` — RemediationService with aggregation query methods

## Files to Modify
- `modules/fundamental/src/lib.rs` — register the new `remediation` module
- `modules/fundamental/Cargo.toml` — add dependencies if needed for aggregation queries

## Implementation Notes
- Follow the existing module pattern established by `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`: each domain has `model/` for data structs and `service/` for business logic.
- Use SeaORM query builder for aggregation queries against existing entity tables (`entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`). The advisory entity already has a severity field (see `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`).
- All service methods must return `Result<T, AppError>` with `.context()` wrapping, per the error handling pattern in `common/src/error.rs`.
- Use the shared query builder helpers from `common/src/db/query.rs` for any filtering or pagination support.
- The NFR requires p95 < 500ms for the summary endpoint with up to 10,000 vulnerabilities. Design aggregation queries to minimize round-trips — prefer a single SQL query with GROUP BY over multiple sequential queries.
- No new database tables or migrations — compute all aggregations from existing vulnerability, advisory, and SBOM relationship data.

Per CONVENTIONS.md Section "Module pattern": follow the `model/ + service/ + endpoints/` structure for the new remediation module.
Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's `.rs` module file scope.

Per CONVENTIONS.md Section "Error handling": all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md Section "Response types": list-style responses use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering, pagination, and sorting; reuse for aggregation query construction
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper; use for by-product endpoint if it supports pagination
- `common/src/error.rs::AppError` — standard error type; use for all Result return types
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for severity field structure and enum values
- `entity/src/advisory.rs` — advisory entity definition with severity data needed for aggregation
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for correlating vulnerabilities with SBOMs

## Acceptance Criteria
- [ ] RemediationSummary struct models aggregated counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved)
- [ ] ProductRemediation struct models per-product breakdown with total, open, and resolved counts
- [ ] RemediationService computes aggregations from existing database tables without creating new tables
- [ ] All service methods return Result<T, AppError> with proper error context
- [ ] Module is registered in modules/fundamental/src/lib.rs
- [ ] Aggregation queries handle the case where no vulnerability data exists (return zero counts)

## Test Requirements
- [ ] Unit test RemediationSummary serialization produces expected JSON shape
- [ ] Unit test ProductRemediation serialization produces expected JSON shape
- [ ] Unit test RemediationService returns zero counts when no vulnerabilities exist
- [ ] Unit test aggregation correctly groups by severity and status

## Verification Commands
- `cargo build -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental -- remediation` — all remediation unit tests pass

## Dependencies
- None (first task in the backend sequence)
