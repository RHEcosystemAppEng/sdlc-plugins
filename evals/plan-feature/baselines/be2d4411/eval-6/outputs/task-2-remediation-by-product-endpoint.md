## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/remediation/by-product` endpoint to the remediation module created in Task 1. This endpoint returns a per-product remediation breakdown where each product entry includes total, open, and resolved vulnerability counts. The response supports pagination for portfolios with more than 50 products.

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — ProductRemediation struct with per-product counts
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — add `pub mod by_product` declaration
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register by-product route
- `modules/fundamental/src/remediation/service/remediation.rs` — add by-product aggregation query method

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown. Response shape: `PaginatedResults<ProductRemediation>` where `ProductRemediation = { product_name: string, total: number, open: number, in_progress: number, resolved: number }`

## Implementation Notes
- Follow the same handler pattern established in Task 1's summary endpoint for consistency within the remediation module.
  Per CONVENTIONS.md: follow model/service/endpoints module structure for new domain modules.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust module file scope.
- Use `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs` as the response wrapper to support pagination for large portfolios (>50 products).
  Per CONVENTIONS.md: list endpoints return PaginatedResults<T>.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's .rs endpoint file scope.
- Use shared filtering and pagination helpers from `common/src/db/query.rs` for offset/limit query parameters.
- Join through `entity/src/sbom.rs` (SBOM entity, which represents products) and `entity/src/sbom_advisory.rs` (SBOM-Advisory join) to compute per-product aggregations.
- Handler must return `Result<T, AppError>` with `.context()` wrapping per the project error handling convention.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — paginated response wrapper
- `common/src/db/query.rs::query` — shared query builder with pagination support
- `entity/src/sbom.rs` — SBOM entity representing products
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table
- `modules/fundamental/src/remediation/endpoints/summary.rs` — sibling endpoint for pattern consistency

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns HTTP 200 with paginated per-product breakdown
- [ ] Each product entry includes product_name, total, open, in_progress, and resolved counts
- [ ] Response supports offset/limit pagination parameters
- [ ] Endpoint returns empty paginated result when no product data exists

## Test Requirements
- [ ] Integration test verifying by-product endpoint returns 200 with expected response shape
- [ ] Integration test verifying correct per-product counts with multiple products seeded
- [ ] Integration test verifying pagination parameters (offset, limit) work correctly

## Verification Commands
- `cargo test --test api remediation` — run remediation endpoint integration tests
- `cargo clippy --all-targets` — verify no linting warnings in new code

## Dependencies
- Depends on: Task 1 — Create remediation module with summary aggregation endpoint

[sdlc-workflow] Description digest: sha256-md:cd2451c7df92cbfcf9fc84692520db4e88970461377bd824bc8b453f9ca8f6c4
