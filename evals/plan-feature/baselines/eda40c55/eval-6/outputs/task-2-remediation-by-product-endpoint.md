## Repository
trustify-backend

## Target Branch
main

## Description
Add a per-product remediation breakdown endpoint at `GET /api/v2/remediation/by-product`. This endpoint returns remediation status aggregated by product, with each product entry including total, open, and resolved vulnerability counts. The aggregation uses existing SBOM-package-advisory relationships to correlate vulnerabilities with products.

This is the second of two backend endpoints supporting the vulnerability remediation tracking dashboard (TC-9006).

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` -- `ProductRemediationBreakdown` struct with fields: product_name (String), product_id (Uuid), total (i64), open (i64), in_progress (i64), resolved (i64); and `ByProductResponse` wrapping a Vec of breakdowns
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- Handler for `GET /api/v2/remediation/by-product`

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` -- Export `by_product` sub-module
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- Register the `/by-product` route
- `modules/fundamental/src/remediation/service/mod.rs` -- Add `get_by_product()` method to `RemediationService`

## API Changes
- `GET /api/v2/remediation/by-product` -- NEW: Returns per-product remediation breakdown. Response shape: `{ items: [{ product_name: string, product_id: string, total: number, open: number, in_progress: number, resolved: number }] }`

## Implementation Notes
- Product identification comes from SBOM metadata. Join `sbom` -> `sbom_package` -> `sbom_advisory` to correlate products with their vulnerability status.
- Use the SBOM entity from `entity/src/sbom.rs` and the join tables `entity/src/sbom_package.rs` and `entity/src/sbom_advisory.rs` for the aggregation query.
- Support pagination for large portfolios (>50 products) using `PaginatedResults<T>` from `common/src/model/paginated.rs` and query helpers from `common/src/db/query.rs`.
- Per CONVENTIONS.md §Module Pattern: add the new endpoint and model files within the existing remediation module structure created in Task 1.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` on database queries. See `modules/fundamental/src/sbom/endpoints/list.rs` for the pattern.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs` to support paginated product listings.
  Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` -- Reuse for constructing the product aggregation query with pagination and sorting
- `common/src/model/paginated.rs::PaginatedResults` -- Use for paginated response wrapper on the by-product endpoint
- `entity/src/sbom.rs` -- SBOM entity; source of product identification
- `entity/src/sbom_package.rs` -- SBOM-Package join table; needed for product-vulnerability correlation
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table; needed for vulnerability status

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with per-product remediation breakdown
- [ ] Each product entry includes product_name, product_id, total, open, in_progress, and resolved counts
- [ ] Endpoint supports pagination for portfolios with >50 products
- [ ] Aggregation uses existing entity relationships without new database tables

## Test Requirements
- [ ] Unit test for `RemediationService::get_by_product()` verifying correct per-product aggregation
- [ ] Verify response includes all products with correlated vulnerabilities
- [ ] Verify pagination works correctly with offset and limit parameters
- [ ] Verify empty database returns empty items array

## Verification Commands
- `cargo test --test api remediation` -- Expected: all remediation endpoint tests pass
- `cargo build` -- Expected: clean build with no warnings

## Dependencies
- Depends on: Task 1 -- Add remediation summary aggregation service and endpoint (provides the remediation module structure)
