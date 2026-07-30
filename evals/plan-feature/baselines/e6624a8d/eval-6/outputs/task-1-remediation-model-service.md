## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation domain module with model structs and an aggregation service. The service computes remediation status counts by querying existing vulnerability and SBOM relationship data — no new database tables are required. The model defines `RemediationSummary` (aggregated counts by severity and status) and `ProductRemediation` (per-product breakdown with total, open, and resolved counts). This is the data layer that the API endpoints (Task 2) will expose.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, re-exports model and service
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` struct with fields: severity (Critical/High/Medium/Low), status (Open/In Progress/Resolved), count
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct with fields: product_name, total, open, in_progress, resolved
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with methods: `get_summary()`, `get_by_product()`

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` to register the new module
- `modules/fundamental/Cargo.toml` — add any needed dependencies (if applicable)

## Implementation Notes
- Follow the existing module pattern: each domain module uses `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/` for a complete example.
  Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ directory structure.
  Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's Rust module file scope.
- Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping for error messages. See `common/src/error.rs` for the `AppError` enum.
  Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` file scope.
- The aggregation service must compute counts from existing tables — use `entity/src/advisory.rs` (Advisory entity with severity field) and `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) for vulnerability-SBOM relationships.
- Use `common/src/db/query.rs` shared query builder helpers for any filtering or pagination logic.
- Non-functional requirement: the summary aggregation must be efficient enough for p95 < 500ms response time. Consider using SQL aggregation queries rather than loading all records into memory.
- Non-functional requirement: no new database tables — compute all aggregations from existing vulnerability and SBOM relationship data.
- Per docs/constraints.md §5.4: do not duplicate existing functionality — reuse query helpers from `common/src/db/query.rs`.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` — shared filtering, pagination, and sorting helpers; use for any query construction in the remediation service
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper for list endpoints; the service should return data compatible with this wrapper
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service that queries advisories; reference its query patterns for accessing advisory/vulnerability data
- `entity/src/advisory.rs` — Advisory entity with severity field; use for severity-based aggregation
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table; use for correlating vulnerabilities with SBOMs/products

## Acceptance Criteria
- [ ] `RemediationSummary` struct is defined with severity (Critical/High/Medium/Low), status (Open/In Progress/Resolved), and count fields
- [ ] `ProductRemediation` struct is defined with product_name, total, open, in_progress, and resolved fields
- [ ] `RemediationService::get_summary()` returns aggregated counts grouped by severity and status
- [ ] `RemediationService::get_by_product()` returns per-product remediation breakdown
- [ ] No new database tables or migrations are created
- [ ] Module is registered in `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Unit test: `RemediationService::get_summary()` returns correct aggregation for known test data
- [ ] Unit test: `RemediationService::get_by_product()` returns correct per-product counts
- [ ] Unit test: empty dataset returns zero counts without error

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental -- remediation` — unit tests pass

## Dependencies
- None (this is the foundational task)
