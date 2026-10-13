## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Create the remediation domain module with model structs and an aggregation service that computes remediation statistics from existing advisory and SBOM relationship data. The service provides two query methods: one returning a severity-by-status matrix (Critical/High/Medium/Low x Open/In Progress/Resolved) and another returning per-product remediation breakdowns (total, open, resolved counts per product). No new database tables are needed — all aggregations are computed from existing entities.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — Remediation module root, re-exports model and service submodules
- `modules/fundamental/src/remediation/model/mod.rs` — Model submodule root, re-exports summary and product breakdown structs
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` struct with severity-by-status counts and `RemediationStatus` enum (Open, InProgress, Resolved)
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct with product name, total, open, in-progress, and resolved counts
- `modules/fundamental/src/remediation/service/mod.rs` — Service submodule root, re-exports `RemediationService`
- `modules/fundamental/src/remediation/service/remediation.rs` — `RemediationService` with methods `summarize()` and `by_product()` that query existing entities

## Files to Modify
- `modules/fundamental/src/lib.rs` — Add `pub mod remediation;` to register the new module

## Implementation Notes
Follow the existing domain module pattern used by `sbom`, `advisory`, and `package` modules under `modules/fundamental/src/`.

- Model structs should derive `Serialize`, `Deserialize`, `Debug`, and `Clone` consistent with existing models like `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`
- The aggregation service should accept a database connection pool and use SeaORM queries against the existing `advisory` entity (`entity/src/advisory.rs`) and `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to compute status counts
- Use the shared query builder helpers from `common/src/db/query.rs` for filtering and pagination support in the by-product query
- Return `Result<T, AppError>` from all service methods, wrapping errors with `.context()` per the error handling pattern in `common/src/error.rs`
- The `by_product` method should return `PaginatedResults<ProductRemediation>` using the wrapper from `common/src/model/paginated.rs` to support large portfolios (>50 products)

Per CONVENTIONS.md §Module Pattern: structure the remediation module as model/ + service/ + endpoints/. Applies: task creates `modules/fundamental/src/remediation/mod.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping in all service methods. Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; reuse for by-product queries
- `common/src/model/paginated.rs::PaginatedResults<T>` — Paginated response wrapper; use for by-product breakdown results
- `common/src/error.rs::AppError` — Application error enum; use for all service error returns
- `entity/src/advisory.rs` — Advisory entity; query for severity and status data
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table; use for correlating vulnerabilities with SBOMs/products

## Acceptance Criteria
- [ ] `RemediationSummary` struct contains counts grouped by severity (Critical, High, Medium, Low) and status (Open, InProgress, Resolved)
- [ ] `ProductRemediation` struct contains product name, total vulnerability count, open count, in-progress count, and resolved count
- [ ] `RemediationService::summarize()` returns a `RemediationSummary` computed from existing advisory and SBOM data
- [ ] `RemediationService::by_product()` returns `PaginatedResults<ProductRemediation>` with per-product breakdown
- [ ] No new database tables or migrations are created
- [ ] All service methods return `Result<T, AppError>`

## Test Requirements
- [ ] Unit test for `RemediationService::summarize()` with mock data verifying correct severity-by-status grouping
- [ ] Unit test for `RemediationService::by_product()` verifying correct per-product aggregation and pagination
- [ ] Unit test verifying empty dataset returns zero counts, not errors
