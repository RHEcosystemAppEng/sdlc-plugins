## Repository
trustify-backend

## Target Branch
main

## Description
Extend the remediation module created in Task 1 to add the `GET /api/v2/remediation/by-product` endpoint. This endpoint returns a per-product remediation breakdown where each product entry includes total, open, in-progress, and resolved vulnerability counts. The response uses `PaginatedResults<T>` to support large portfolios (the Feature's customer consideration notes that portfolios with >50 products require pagination).

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` -- ProductRemediation struct with product_name, total, open, in_progress, resolved fields
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET /api/v2/remediation/by-product handler

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` -- add `pub mod by_product;` declaration
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- register by-product route
- `modules/fundamental/src/remediation/service/remediation.rs` -- add by_product aggregation method to RemediationService

## API Changes
- `GET /api/v2/remediation/by-product` -- NEW: returns paginated per-product remediation breakdown with total, open, in_progress, and resolved counts per product

## Implementation Notes
- Extend `RemediationService` in `service/remediation.rs` with a `by_product()` method that aggregates vulnerability counts per product using SeaORM joins across `sbom`, `sbom_advisory`, and `package` entities.

- Return `PaginatedResults<ProductRemediation>` using the pagination wrapper from `common/src/model/paginated.rs`.
  Per CONVENTIONS.md section "Response types": list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` scope.

- Use `common/src/db/query.rs` helpers for pagination parameters (limit, offset) and sorting.
  Per CONVENTIONS.md section "Query helpers": shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` scope.

- The handler should return `Result<Json<PaginatedResults<ProductRemediation>>, AppError>` with `.context()` wrapping.
  Per CONVENTIONS.md section "Error handling": all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` scope.

- Reference `modules/fundamental/src/sbom/endpoints/list.rs` as the established pattern for a paginated list endpoint with query parameter handling.

- Customer consideration: large portfolios (>50 products) require pagination. Ensure `limit` and `offset` query parameters are supported via the query helpers.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` -- standard pagination wrapper for the response
- `common/src/db/query.rs` -- shared pagination, filtering, and sorting query helpers
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference paginated list endpoint implementation showing the query parameter and response pattern
- `entity/src/package.rs` -- Package entity for product identification in join queries
- `entity/src/sbom_package.rs` -- SBOM-Package join table for correlating products to SBOMs and their advisories

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with paginated per-product remediation data
- [ ] Each product entry includes product_name, total, open, in_progress, and resolved counts
- [ ] Pagination works correctly with limit and offset query parameters
- [ ] Response includes total count for pagination metadata
- [ ] Endpoint handles large portfolios (>50 products) via pagination without performance degradation

## Test Requirements
- [ ] Integration test verifying by-product endpoint returns 200 with correct response shape
- [ ] Integration test verifying pagination parameters (limit, offset) are respected
- [ ] Integration test verifying product counts match expected seeded test data
- [ ] Integration test verifying response with no products returns empty paginated result

## Verification Commands
- `cargo build` -- verify compilation
- `cargo test --test remediation` -- run remediation integration tests

## Documentation Updates
- Backend API documentation -- add reference for `GET /api/v2/remediation/by-product` endpoint with request/response examples including pagination parameters

## Dependencies
- Depends on: Task 1 -- Add remediation module with summary aggregation endpoint
