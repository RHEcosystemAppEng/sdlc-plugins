## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/remediation/by-product` endpoint to the remediation module created in Task 1. This endpoint returns a per-product remediation breakdown where each product entry includes total, open, and resolved vulnerability counts. The aggregation joins existing SBOM, package, and advisory entity data to compute product-level remediation status.

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediationBreakdown` struct with per-product counts
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — handler for `GET /api/v2/remediation/by-product`

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — add `pub mod by_product;` declaration
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the by-product route
- `modules/fundamental/src/remediation/service/mod.rs` — add `get_by_product()` method to `RemediationService`

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown. Response shape: `{ items: [{ product_name: string, total: number, open: number, resolved: number }], total: number }`

## Implementation Notes
- Per repo conventions (Module pattern): extend the existing remediation module with additional model and endpoint files following the same `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/advisory/` for a multi-endpoint module example.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's module structure scope.
- Per repo conventions (Error handling): handler must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust endpoint file scope.
- Per repo conventions (Response types): use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the product list since large portfolios (>50 products) may require pagination per customer considerations.
  Applies: task creates `modules/fundamental/src/remediation/model/by_product.rs` matching the convention's Rust model file scope.
- Per repo conventions (Query helpers): use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs` to support pagination and optional filtering by product name.
  Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust service file scope.
- The product breakdown aggregation should join through `entity/src/sbom.rs`, `entity/src/sbom_package.rs`, and `entity/src/sbom_advisory.rs` to correlate products with their vulnerability remediation status.
- Consider pagination for large product portfolios per the customer consideration noting >50 products may require it.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper; use for paginated product list
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` — extend with by-product method following the same query patterns as `get_summary()`
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for querying package/product data

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns a 200 response with per-product breakdown including total, open, and resolved counts
- [ ] The endpoint supports pagination for large product sets
- [ ] The response is computed from existing entity data without new database tables
- [ ] Error responses use the standard `AppError` format

## Test Requirements
- [ ] Verify `GET /api/v2/remediation/by-product` returns 200 with correct response shape
- [ ] Verify per-product counts are accurate (total = open + in_progress + resolved)
- [ ] Verify pagination works correctly for product lists
- [ ] Verify the endpoint returns an empty list when no product data exists

## Verification Commands
- `cargo build` — confirm the project compiles with the new endpoint
- `cargo test` — confirm existing tests still pass

## Dependencies
- Depends on: Task 1 — Create remediation module with summary endpoint
