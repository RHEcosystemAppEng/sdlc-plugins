# Task 3: Add remediation by-product endpoint

**Epic:** TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add the `GET /api/v2/remediation/by-product` endpoint to the remediation module created in Task 2. This endpoint returns a per-product remediation breakdown where each product entry includes total, open, and resolved vulnerability counts. The endpoint enables the frontend dashboard to display product-level remediation progress and supports the product filter use case.

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — ProductRemediation struct with per-product counts
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — add `pub mod by_product;` to expose the new model
- `modules/fundamental/src/remediation/service/mod.rs` — add `by_product()` method to RemediationService for product-level aggregation
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the by-product route

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown. Response shape: `PaginatedResults<ProductRemediation>` where `ProductRemediation = { product_name: string, total: number, open: number, in_progress: number, resolved: number }`

## Implementation Notes
- Extend the remediation module structure created in Task 2.
- Use SeaORM joins across `entity/src/sbom.rs`, `entity/src/sbom_advisory.rs`, and `entity/src/advisory.rs` to aggregate vulnerability counts per product (SBOM).
- Return `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs` to support large portfolios (>50 products per the customer considerations).
- Apply the shared query builder helpers from `common/src/db/query.rs` for pagination and sorting parameters.
- Consider adding pagination support since large portfolios may have many products; use the existing `PaginatedResults` pattern from `common/src/model/paginated.rs`.
- Follow the same error handling pattern as Task 2: `Result<T, AppError>` with `.context()`.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` — PaginatedResults<T> wrapper for paginated list responses
- `modules/fundamental/src/sbom/model/summary.rs` — SbomSummary struct; reference for product/SBOM-level data patterns
- `entity/src/sbom_package.rs` — SBOM-Package join table; useful for product-to-vulnerability traversal

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns per-product remediation breakdown
- [ ] Each product entry includes product_name, total, open, in_progress, and resolved counts
- [ ] Response uses PaginatedResults wrapper to support large product portfolios
- [ ] Pagination parameters (offset, limit) work correctly
- [ ] Aggregations are computed from existing entity data without new database tables

## Test Requirements
- [ ] Integration test verifying the by-product endpoint returns correct per-product counts
- [ ] Integration test verifying pagination works with offset and limit parameters
- [ ] Integration test verifying empty database returns empty product list
- [ ] Integration test verifying a product with no vulnerabilities returns zero counts

## Verification Commands
- `cargo test --test api remediation` — run remediation endpoint tests
- `cargo clippy --all-targets` — verify no lint warnings

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation summary endpoint (module structure created there)
