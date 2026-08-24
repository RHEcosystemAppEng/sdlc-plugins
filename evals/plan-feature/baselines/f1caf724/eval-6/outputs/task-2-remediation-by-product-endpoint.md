## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add the `GET /api/v2/remediation/by-product` endpoint to the remediation module created in Task 1. This endpoint returns a per-product remediation breakdown where each product entry includes total, open, and resolved vulnerability counts. The endpoint supports pagination for portfolios with large numbers of products (>50) and enables engineering leads to prioritize fix work per product.

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — `RemediationByProduct` struct with product name, total, open, in_progress, and resolved counts
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — handler for `GET /api/v2/remediation/by-product`

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — add `pub mod by_product;` to expose the new model
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the by-product route
- `modules/fundamental/src/remediation/service/mod.rs` — add `get_by_product()` method to `RemediationService`

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown. Response shape: `PaginatedResults<RemediationByProduct>` where each entry has `{ product_name: string, total: number, open: number, in_progress: number, resolved: number }`

## Implementation Notes
- Follow the same handler and service patterns established in Task 1 for the remediation module.
  Per CONVENTIONS.md §Module Pattern: extend the existing remediation model/ and endpoints/ with the new by-product files.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's module structure scope.
- Return `PaginatedResults<RemediationByProduct>` to support pagination for large portfolios (>50 products), consistent with other list endpoints.
  Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task creates `modules/fundamental/src/remediation/model/by_product.rs` matching the convention's `.rs` model file scope.
- Use `common/src/db/query.rs` for pagination and optional filtering parameters.
  Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` service file scope.
- Handler must return `Result<Json<PaginatedResults<RemediationByProduct>>, AppError>`.
  Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all error paths.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` handler file scope.
- The aggregation query groups by product (derived from SBOM-to-product relationships) and counts vulnerabilities by status.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper; use directly for the by-product list
- `common/src/db/query.rs::query` — shared query builder; reuse for pagination and sorting
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` — extend with the by-product aggregation method (created in Task 1)
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for paginated list endpoint handler pattern

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns a 200 response with per-product remediation breakdown
- [ ] Each product entry includes product_name, total, open, in_progress, and resolved counts
- [ ] Response uses `PaginatedResults` wrapper with pagination support (offset/limit)
- [ ] Products with no vulnerabilities are excluded from the response (or show zero counts, consistent with the summary endpoint)
- [ ] Route is registered in the remediation module's endpoint configuration

## Test Requirements
- [ ] Integration test verifying `GET /api/v2/remediation/by-product` returns 200 with correct JSON structure
- [ ] Integration test verifying per-product counts are accurate against known test data with multiple products
- [ ] Integration test verifying pagination parameters (offset, limit) work correctly
- [ ] Integration test verifying empty database returns empty paginated result

## Verification Commands
- `cargo test --test api remediation` — verify integration tests pass
- `cargo clippy --all-targets` — verify no lint warnings in new code

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint
