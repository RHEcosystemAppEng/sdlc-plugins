## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/remediation/by-product` endpoint to the remediation module created in Task 1. This endpoint returns a per-product remediation breakdown where each product entry includes total, open, and resolved vulnerability counts. The endpoint aggregates data from existing SBOM and advisory relationships, grouping by product (SBOM identity).

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` response struct with per-product counts
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — register `by_product` model submodule
- `modules/fundamental/src/remediation/service/mod.rs` — add by-product aggregation query to `RemediationService`
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register by-product route

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown. Response shape: `{ items: [{ product_name: string, product_id: string, total: number, open: number, in_progress: number, resolved: number }], total: number }`

## Implementation Notes
- Per CONVENTIONS.md §Module Pattern: extend the existing remediation module by adding model and endpoint files following the same structure. See `modules/fundamental/src/advisory/` for multi-endpoint module pattern.
  Applies: task creates `modules/fundamental/src/remediation/model/by_product.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error Handling: handler must return `Result<T, AppError>` with `.context()` wrapping. See `modules/fundamental/src/sbom/endpoints/list.rs` for established handler pattern.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md §Response Types: return `PaginatedResults<ProductRemediation>` to support pagination for large portfolios (>50 products).
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md §Query Helpers: use shared pagination and sorting utilities from `common/src/db/query.rs` for the product list.
  Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` service file scope.
- Group by SBOM/product identity and join through `sbom_advisory` to count vulnerabilities per product
- Support pagination for large portfolios (>50 products) using `PaginatedResults<T>`
- Ensure query performance meets the p95 < 500ms requirement

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder for pagination and sorting
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for paginated lists
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for product/SBOM identity fields
- `entity/src/sbom.rs` — SBOM entity for product grouping
- `entity/src/sbom_advisory.rs` — join table for SBOM-vulnerability correlation

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with per-product remediation breakdown
- [ ] Each product entry includes product name, product ID, total, open, in_progress, and resolved counts
- [ ] Response supports pagination for portfolios with more than 50 products
- [ ] Aggregation computed from existing SBOM and advisory data without new database tables
- [ ] Route registered in remediation `endpoints/mod.rs`

## Test Requirements
- [ ] Integration test in `tests/api/remediation.rs` verifying `GET /api/v2/remediation/by-product` returns 200 with correct response shape
- [ ] Test with multiple products having different vulnerability distributions
- [ ] Test pagination with offset and limit parameters
- [ ] Test with empty dataset returns an empty items array

## Verification Commands
- `cargo test --test api remediation` — runs remediation endpoint integration tests
- `cargo clippy --all-targets` — verifies no lint warnings

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint
