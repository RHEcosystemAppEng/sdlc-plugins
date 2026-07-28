## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/remediation/by-product` endpoint to the remediation module created in Task 1. This endpoint returns a per-product remediation breakdown where each product entry includes total, open, and resolved vulnerability counts. The endpoint supports pagination for portfolios with many products (>50) as noted in the feature's customer considerations.

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` -- ProductRemediation struct with product name/ID, total, open, and resolved counts
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET /api/v2/remediation/by-product handler

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` -- add `pub mod by_product;` to expose the new model
- `modules/fundamental/src/remediation/service/mod.rs` -- add by_product aggregation query method to RemediationService
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- register the by-product route

## API Changes
- `GET /api/v2/remediation/by-product` -- NEW: returns per-product remediation breakdown with pagination. Response shape: `PaginatedResults<ProductRemediation>` where ProductRemediation = `{ product_name: string, product_id: string, total: number, open: number, resolved: number }`

## Implementation Notes
- Follow the endpoint pattern established in Task 1 and existing modules like advisory.
  Per CONVENTIONS.md (Key Conventions -- Response types): list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md (Key Conventions -- Query helpers): use shared filtering, pagination, and sorting from `common/src/db/query.rs` for the paginated product breakdown.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md (Key Conventions -- Error handling): return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.
- The aggregation query should group by product (derived from SBOM-package relationships) and count vulnerability statuses per product.
- Use the existing `sbom_package` and `sbom_advisory` join tables to correlate products with their vulnerability remediation status.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` -- standard paginated response wrapper; use for the by-product endpoint response
- `common/src/db/query.rs::query helpers` -- pagination and sorting utilities; apply to the product list
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` -- the service created in Task 1; extend with the by_product method
- `entity/src/sbom_package.rs` -- SBOM-Package join table; use to correlate products with SBOMs
- `entity/src/package.rs` -- Package entity; source for product identification

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with per-product remediation breakdown
- [ ] Each product entry includes product name/ID, total, open, and resolved counts
- [ ] Response uses `PaginatedResults<ProductRemediation>` format with pagination support
- [ ] Endpoint handles portfolios with >50 products through pagination

## Test Requirements
- [ ] By-product endpoint returns correct per-product counts when multiple products have vulnerabilities
- [ ] By-product endpoint returns empty results when no product data exists
- [ ] Pagination works correctly (offset/limit parameters, total count)

## Verification Commands
- `cargo build` -- project compiles without errors
- `cargo test --test api` -- integration tests pass

## Dependencies
- Depends on: Task 1 -- Add remediation summary aggregation endpoint (establishes the remediation module structure)
