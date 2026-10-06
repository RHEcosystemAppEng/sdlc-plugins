## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/remediation/by-product` endpoint that returns a per-product breakdown of vulnerability remediation status. Each product entry includes total, open, and resolved counts. This endpoint serves the product filter and per-product view on the frontend remediation dashboard.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET handler for `/api/v2/remediation/by-product`

## Files to Modify
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- register the by-product route alongside the summary route

## API Changes
- `GET /api/v2/remediation/by-product` -- NEW: returns list of `ProductRemediation` entries with per-product total, open, and resolved counts

## Implementation Notes
Per CONVENTIONS.md "Endpoint registration": add the by-product route to the existing `endpoints/mod.rs` route registration. Follow the pattern established in Task 2 for the summary endpoint.
Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

Per CONVENTIONS.md "Response types": use `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs` for the response to support pagination for portfolios with many products (>50 per customer considerations).
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md "Query helpers": use shared pagination and sorting helpers from `common/src/db/query.rs` to support offset/limit and sort parameters.
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md "Error handling": handler must return `Result<Json<PaginatedResults<ProductRemediation>>, AppError>`.
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.

Relevant constraints from `docs/constraints.md`:
- Per SS5.3: Implementation must follow the patterns referenced in these Implementation Notes.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` -- paginated response wrapper for list endpoints
- `common/src/db/query.rs` -- shared query builder for pagination and sorting
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference implementation for a paginated GET list endpoint

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns HTTP 200 with paginated JSON body
- [ ] Each product entry includes product identifier, total count, open count, and resolved count
- [ ] Endpoint supports pagination parameters (offset, limit)
- [ ] Endpoint handles large product counts (>50) without degradation
- [ ] Route is registered in the remediation endpoints module

## Test Requirements
- [ ] Verify endpoint returns 200 with valid paginated ProductRemediation JSON
- [ ] Verify pagination parameters (offset, limit) are respected
- [ ] Verify response includes correct counts per product
- [ ] Verify endpoint handles empty dataset (no products) gracefully

## Verification Commands
- `cargo test --test api remediation` -- runs remediation endpoint integration tests (after Task 4)
- `cargo build` -- verifies compilation with new endpoint

## Dependencies
- Depends on: Task 1 -- Add remediation data models and aggregation service
- Depends on: Task 2 -- Add remediation summary endpoint (shared endpoint module)

## Parent Epic
TC-9007
