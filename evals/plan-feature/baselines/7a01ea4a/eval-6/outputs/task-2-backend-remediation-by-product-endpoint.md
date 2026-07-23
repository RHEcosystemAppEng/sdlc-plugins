# Task 2: Add per-product remediation breakdown endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the remediation module created in Task 1 to add a per-product remediation breakdown endpoint. This endpoint returns remediation status for each product, including total, open, and resolved vulnerability counts. Products are derived from existing SBOM data -- each SBOM represents a product. The endpoint supports the dashboard's product-level drill-down and filtering requirements (TC-9006).

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` -- `ProductRemediation` struct with product name, total, open, in_progress, and resolved counts
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- `GET /api/v2/remediation/by-product` handler

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` -- add `pub mod by_product;` declaration
- `modules/fundamental/src/remediation/service/remediation.rs` -- add `get_by_product()` method to `RemediationService`
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- register the by-product route
- `tests/api/remediation.rs` -- add integration tests for the by-product endpoint

## API Changes
- `GET /api/v2/remediation/by-product` -- NEW: returns per-product remediation breakdown. Response shape: `PaginatedResults<ProductRemediation>` where each entry includes `{ product_name: string, product_id: string, total: number, open: number, in_progress: number, resolved: number }`

## Implementation Notes
- Use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the response since this endpoint returns a list of products that may need pagination (NFR: large portfolios with >50 products may require pagination).
  - Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the Rust endpoint file scope.
- Use the shared query builder helpers from `common/src/db/query.rs` for pagination and sorting support.
  - Applies: task modifies `modules/fundamental/src/remediation/service/remediation.rs` matching the Rust service file scope.
- Products are identified via SBOM data. Use the `sbom` entity (`entity/src/sbom.rs`) and `sbom_package` join table (`entity/src/sbom_package.rs`) to correlate products with vulnerabilities.
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for the list endpoint structure.
- Follow the error handling pattern: `Result<T, AppError>` with `.context()` wrapping.
- NFR: must handle up to 10,000 tracked vulnerabilities without performance degradation.

## Reuse Candidates
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper; use directly for the by-product response
- `common/src/db/query.rs` -- shared query builder helpers; reuse for pagination and sorting
- `modules/fundamental/src/sbom/model/summary.rs` -- `SbomSummary` struct; reference for how product/SBOM data is structured
- `entity/src/sbom.rs` -- SBOM entity; needed for product identification
- `entity/src/sbom_package.rs` -- SBOM-Package join table; needed for product-vulnerability correlation

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns HTTP 200 with paginated per-product remediation breakdown
- [ ] Each product entry includes product_name, product_id, total, open, in_progress, and resolved counts
- [ ] Pagination support works correctly (offset/limit query parameters)
- [ ] Response correctly aggregates vulnerabilities per product from existing SBOM and advisory data
- [ ] Endpoint handles portfolios with >50 products via pagination

## Test Requirements
- [ ] Integration test: `GET /api/v2/remediation/by-product` returns 200 with expected response shape
- [ ] Integration test: per-product counts correctly aggregate vulnerabilities associated with each SBOM/product
- [ ] Integration test: pagination works correctly (offset, limit parameters)
- [ ] Integration test: empty result set returns valid paginated response with zero items

## Verification Commands
- `cargo test --test api remediation` -- expected: all remediation integration tests pass

## Dependencies
- Depends on: Task 1 -- Create remediation module with summary aggregation endpoint
