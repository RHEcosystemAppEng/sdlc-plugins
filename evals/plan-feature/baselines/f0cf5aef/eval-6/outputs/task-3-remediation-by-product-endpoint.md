## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Implement the `GET /api/v2/remediation/by-product` endpoint that returns a per-product remediation breakdown. Each product entry includes total, open, and resolved vulnerability counts. This endpoint powers the product-level filtering and drill-down on the remediation tracking dashboard (TC-9006), enabling engineering leads to prioritize fix work for specific products.

## Files to Modify
- `modules/fundamental/src/remediation/endpoints/mod.rs` — add route for the by-product endpoint
- `modules/fundamental/src/remediation/service/mod.rs` — add per-product aggregation query method to `RemediationService`
- `modules/fundamental/src/remediation/model/mod.rs` — register new model struct

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct with product name, total, open, and resolved counts
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown. Response shape: `PaginatedResults<ProductRemediation>` where `ProductRemediation { product_name: String, total: i64, open: i64, in_progress: i64, resolved: i64 }`

## Implementation Notes
- Follow the same handler pattern established in Task 2 for the remediation module.
- The by-product aggregation query should GROUP BY product (derived from SBOM relationships) and compute counts per status.
- Use the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` for the response, since large portfolios (>50 products) may require pagination per the customer considerations in the feature description.
- Apply pagination and sorting support using `common/src/db/query.rs` helpers.
- Product identity comes from the SBOM entity — each SBOM represents a product. Join through `entity/src/sbom.rs` and `entity/src/sbom_advisory.rs` to aggregate vulnerability counts per product.
- No new database tables — aggregate from existing relationships.
- Performance: must handle 10,000+ vulnerabilities across 50+ products within p95 < 500ms.
- Per repo conventions: return `Result<Json<PaginatedResults<ProductRemediation>>, AppError>` with `.context()` error wrapping.

## Reuse Candidates
- `common/src/model/paginated.rs` — `PaginatedResults<T>` for paginated list responses
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` (created in Task 2) to extend with by-product method
- `entity/src/sbom.rs` — SBOM entity for product identification
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for vulnerability correlation

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with per-product remediation breakdown
- [ ] Each product entry includes product_name, total, open, in_progress, and resolved counts
- [ ] Response uses `PaginatedResults<T>` wrapper with pagination support
- [ ] Large portfolios (50+ products) are paginated correctly
- [ ] Counts per product are consistent with the overall summary from Task 2

## Test Requirements
- [ ] Integration test: `GET /api/v2/remediation/by-product` returns 200 with correct structure
- [ ] Integration test: verify per-product counts match expected values for test data with multiple products
- [ ] Integration test: verify pagination works with `offset` and `limit` parameters
- [ ] Integration test: verify response with no products returns empty results

## Verification Commands
- `cargo test --test api remediation` — runs all remediation endpoint integration tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation summary aggregation service and endpoint (extends the remediation module created in Task 2)
