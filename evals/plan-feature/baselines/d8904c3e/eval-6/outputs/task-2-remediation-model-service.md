## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add a new remediation module under `modules/fundamental/src/remediation/` following the established model/service/endpoints module pattern. This task creates the model types for remediation aggregation (RemediationSummary, ProductRemediation) and the RemediationService that computes aggregated remediation statistics from existing vulnerability and SBOM relationship data. No new database tables are required -- all aggregations are computed via queries over existing entities.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root, re-exports model and service submodules
- `modules/fundamental/src/remediation/model/mod.rs` -- model submodule root
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary struct with fields: severity (Critical/High/Medium/Low), status (Open/InProgress/Resolved), count; and ProductRemediation struct with fields: product_name, total, open, in_progress, resolved
- `modules/fundamental/src/remediation/service/mod.rs` -- service submodule root
- `modules/fundamental/src/remediation/service/remediation.rs` -- RemediationService with methods: get_summary() returning Vec<RemediationSummary> and get_by_product() returning Vec<ProductRemediation>

## Files to Modify
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` to expose the new module
- `modules/fundamental/Cargo.toml` -- add any additional dependencies if needed

## Implementation Notes
- Follow the established module pattern from `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`: each domain module has `model/`, `service/`, and `endpoints/` subdirectories.
  Per CONVENTIONS.md: follow the model/ + service/ + endpoints/ module structure.
  Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's Rust module structure scope.
- Use SeaORM query builder to aggregate vulnerability counts by severity and status. Reference `common/src/db/query.rs` for shared query builder helpers (filtering, pagination, sorting).
  Per CONVENTIONS.md: use shared query helpers from common/src/db/query.rs for filtering and pagination.
  Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust service file scope.
- All service methods must return `Result<T, AppError>` using `.context()` wrapping for errors. Reference `common/src/error.rs` for the AppError enum.
  Per CONVENTIONS.md: all handlers return Result<T, AppError> with .context() wrapping.
  Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust file scope.
- The aggregation queries must operate on existing tables only: `advisory` (includes severity), `sbom_advisory` (SBOM-advisory join), `sbom` (SBOM entity), and `sbom_package`/`package` (for product-level grouping). Do NOT create new database tables or migrations.
- Non-functional requirement: summary query must achieve p95 < 500ms. Consider query optimization and appropriate use of GROUP BY with indexes on existing tables.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, sorting; reuse for building aggregation queries
- `common/src/model/paginated.rs` -- PaginatedResults<T> response wrapper; reference for response type patterns
- `modules/fundamental/src/advisory/service/advisory.rs` -- AdvisoryService patterns for fetch and list operations; follow as template for RemediationService
- `modules/fundamental/src/advisory/model/summary.rs` -- AdvisorySummary struct includes severity field; reference for severity handling patterns
- `entity/src/advisory.rs` -- Advisory entity definition; use for severity field access
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table; use for joining SBOMs to advisories in aggregation queries

## Acceptance Criteria
- [ ] RemediationSummary struct represents aggregated counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved)
- [ ] ProductRemediation struct represents per-product breakdown with product_name, total, open, in_progress, and resolved counts
- [ ] RemediationService.get_summary() returns correct aggregated counts from existing vulnerability data
- [ ] RemediationService.get_by_product() returns correct per-product breakdown from existing data
- [ ] No new database tables or migrations are created
- [ ] All methods return Result<T, AppError> with proper error context

## Test Requirements
- [ ] Unit test for RemediationService.get_summary() with known test data verifying correct aggregation by severity and status
- [ ] Unit test for RemediationService.get_by_product() with known test data verifying correct per-product breakdown
- [ ] Unit test verifying empty database returns empty/zero-count results without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
