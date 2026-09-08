## Repository
trustify-backend

## Target Branch
main

## Description
Extend the remediation module with a `GET /api/v2/remediation/by-product` endpoint that returns a per-product breakdown of vulnerability remediation status. Each product entry includes total vulnerability count, open count, and resolved count. The endpoint supports pagination via `PaginatedResults` for large portfolios with more than 50 products. Must handle up to 10,000 tracked vulnerabilities without performance degradation.

## Files to Modify
- `modules/remediation/src/model/mod.rs` — add by_product module declaration
- `modules/remediation/src/service/remediation.rs` — add by-product aggregation method to RemediationService
- `modules/remediation/src/endpoints/mod.rs` — register the by-product route

## Files to Create
- `modules/remediation/src/model/by_product.rs` — ProductRemediation struct with per-product counts
- `modules/remediation/src/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: Returns paginated per-product remediation breakdown with total, open, and resolved counts per product

## Implementation Notes
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Use `PaginatedResults<ProductRemediation>` for the response.
  Applies: task creates `modules/remediation/src/endpoints/by_product.rs` matching the convention's .rs endpoint file scope.

- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs` for pagination support.
  Applies: task modifies `modules/remediation/src/service/remediation.rs` matching the convention's .rs service file scope.

- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping in all handlers.
  Applies: task creates `modules/remediation/src/endpoints/by_product.rs` matching the convention's .rs endpoint file scope.

- The product breakdown query should join SBOM data (representing products) with advisory/vulnerability data via `sbom_advisory`, and group by product (SBOM identifier). Use existing entities: `entity/src/sbom.rs` and `entity/src/sbom_advisory.rs`.
- Support standard pagination parameters (offset, limit) for portfolios exceeding 50 products.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper for product list
- `common/src/db/query.rs::*` — shared query helpers for pagination, filtering, sorting
- `modules/remediation/src/service/remediation.rs::RemediationService` — extend with by-product method (from Task 1)
- `entity/src/sbom.rs` — SBOM entity representing products
- `entity/src/sbom_advisory.rs` — SBOM-advisory join table for vulnerability correlation

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns JSON with per-product remediation breakdown
- [ ] Each product entry includes product name/identifier, total count, open count, and resolved count
- [ ] Response uses `PaginatedResults` wrapper supporting offset and limit parameters
- [ ] Aggregations are computed from existing data without new database tables
- [ ] Endpoint handles large datasets (up to 10,000 vulnerabilities) without performance degradation

## Test Requirements
- [ ] Integration test verifying by-product endpoint returns 200 with correct response structure
- [ ] Test that each product entry includes total, open, and resolved counts
- [ ] Test pagination parameters (offset, limit) work correctly and return appropriate subsets
- [ ] Test with empty dataset returns empty results with total count of zero

## Verification Commands
- `cargo build` — builds successfully
- `cargo test --test remediation` — all remediation integration tests pass

## Dependencies
- Depends on: Task 1 — Create remediation module with summary aggregation endpoint
