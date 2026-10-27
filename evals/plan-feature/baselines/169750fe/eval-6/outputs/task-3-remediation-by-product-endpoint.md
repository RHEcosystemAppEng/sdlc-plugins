## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add the `GET /api/v2/remediation/by-product` endpoint that returns per-product remediation breakdown. Each product entry includes total, open, in-progress, and resolved vulnerability counts. The endpoint delegates to `RemediationService::get_by_product()` and returns paginated results.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — handler for GET /api/v2/remediation/by-product

## Files to Modify
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the by-product route

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: returns `PaginatedResults<ProductRemediation>` with per-product breakdown

## Implementation Notes
- Add the route in `modules/fundamental/src/remediation/endpoints/mod.rs` alongside the summary route created in Task 2.
- Return `PaginatedResults<ProductRemediation>` using the shared paginated response wrapper from `common/src/model/paginated.rs`.
- Accept standard pagination query parameters (offset, limit) using the query builder helpers from `common/src/db/query.rs`.
- Per Key Conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's response type scope.
- Per Key Conventions: shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's query helper scope.
- Large portfolios (>50 products) may require pagination — the `PaginatedResults<T>` wrapper handles this.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — example paginated list endpoint
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper
- `common/src/db/query.rs` — filtering and pagination helpers

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with paginated JSON body
- [ ] Each product entry contains product name, total, open, in-progress, and resolved counts
- [ ] Standard pagination parameters (offset, limit) are supported
- [ ] Route is registered in `modules/fundamental/src/remediation/endpoints/mod.rs`

## Test Requirements
- [ ] Handler returns paginated results with correct product breakdown
- [ ] Pagination parameters produce correct offsets and limits
- [ ] Empty product list returns valid empty paginated response

## Verification Commands
- `cargo check -p trustify-fundamental` — verify compilation
- `cargo test -p trustify-fundamental remediation` — run remediation tests

## Dependencies
- Depends on: Task 1 — Remediation summary model and service
