## Repository
trustify-backend

## Target Branch
main

## Description
Add the GET /api/v2/remediation/by-product endpoint to the remediation module created in Task 1. This endpoint returns a per-product breakdown of remediation status, where each product entry includes total, open, in-progress, and resolved vulnerability counts. Products are derived from ingested SBOMs. The endpoint supports pagination for portfolios with many products and filtering by product name.

## Files to Create
- `modules/remediation/src/model/product.rs` — ProductRemediation struct with product name and per-status counts
- `modules/remediation/src/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler

## Files to Modify
- `modules/remediation/src/model/mod.rs` — Add product model declaration
- `modules/remediation/src/endpoints/mod.rs` — Register the by-product route
- `tests/api/remediation.rs` — Add integration tests for the by-product endpoint

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: Returns PaginatedResults<ProductRemediation> with per-product remediation breakdown (product_name, total, open, in_progress, resolved)

## Implementation Notes
- The ProductRemediation model struct should follow the pattern in `modules/remediation/src/model/summary.rs` (created in Task 1) for consistency.
- Use `common/src/model/paginated.rs::PaginatedResults<T>` as the response wrapper, following the list endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs`.
- The aggregation query should join advisory entities with sbom_advisory to group remediation counts by SBOM (product). Use `common/src/db/query.rs` helpers for pagination and sorting.
- Products are identified by their SBOM names — join through `entity/src/sbom.rs` (SBOM entity) and `entity/src/sbom_advisory.rs` (SBOM-Advisory join).
- NFR: Large portfolios (>50 products) require pagination in the product breakdown — PaginatedResults handles this.
- Register the new route in `modules/remediation/src/endpoints/mod.rs` following the existing route registration pattern.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — Standard paginated response wrapper; required for the by-product list endpoint
- `common/src/db/query.rs::query` — Shared query builder helpers for pagination and sorting
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference endpoint for paginated list handler pattern
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference model for product-related struct patterns

## Acceptance Criteria
- [ ] GET /api/v2/remediation/by-product returns a PaginatedResults response with per-product remediation entries
- [ ] Each product entry includes product_name, total, open, in_progress, and resolved counts
- [ ] The endpoint supports pagination (offset, limit parameters)
- [ ] The endpoint returns an empty paginated result when no product data exists
- [ ] Product data is derived from SBOM entities linked to advisories

## Test Requirements
- [ ] Integration test: GET /api/v2/remediation/by-product returns 200 with correct paginated structure
- [ ] Integration test: By-product endpoint returns correct per-product counts when multiple products have different remediation statuses
- [ ] Integration test: By-product endpoint returns empty results when no data exists
- [ ] Integration test: Pagination parameters (offset, limit) work correctly
- [ ] Follow the integration test pattern in `tests/api/sbom.rs`

## Verification Commands
- `cargo test --test api remediation` — All remediation integration tests pass

## Dependencies
- Depends on: Task 1 — Create remediation module with summary endpoint
