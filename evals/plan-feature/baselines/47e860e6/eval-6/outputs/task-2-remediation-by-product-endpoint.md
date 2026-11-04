## Repository
trustify-backend

## Target Branch
main

## Description
Implement `GET /api/v2/remediation/by-product`, returning a paginated per-product
remediation breakdown (total, open, in-progress, resolved counts for each product).
Feeds the product breakdown and product filter on the `/remediation` dashboard
(TC-9006, UC-2). Pagination is required because large portfolios (>50 products) are
expected (Customer Considerations).

Parent Epic: TC-9006: trustify-backend

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — export the new product breakdown model
- `modules/fundamental/src/remediation/service/mod.rs` — add `RemediationService::by_product()`
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the `/by-product` route
- `tests/api/remediation.rs` — add by-product integration tests

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct (`product`, `total`, `open`, `in_progress`, `resolved`)
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler

## API Changes
- `GET /api/v2/remediation/by-product?offset={n}&limit={n}&sort={field}` — NEW: returns `PaginatedResults<ProductRemediation>` i.e. `{ items: [{ product, total, open, in_progress, resolved }], total }`

## Implementation Notes
- Group by the product identity of the SBOM (verify the product/name field on `entity/src/sbom.rs` and `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` at implementation time) joined through `entity/src/sbom_advisory.rs` to `entity/src/advisory.rs`. Use a grouped SQL query with `COUNT ... FILTER (WHERE status = ...)` (or SeaORM equivalent) so all counts come from one pass.
- Apply pagination and sorting through the shared helpers in `common/src/db/query.rs`; wrap the response in `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Reuse the status/severity types introduced in Task 1 (`modules/fundamental/src/remediation/model/summary.rs`) — do not redefine them.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's list endpoint scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination and sorting from `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust query scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust handler scope. Example: `modules/fundamental/src/advisory/endpoints/list.rs`.
- Per CONVENTIONS.md §Testing: add integration tests to `tests/api/` using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/` scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §2 commit rules (Conventional Commits, Jira footer, `Assisted-by: Claude Code` trailer); §3 PR `--base main` and Jira PR link; §5 scope to listed files, inspect before modifying, no duplication of existing helpers.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for list endpoints
- `common/src/db/query.rs` — pagination/sorting helpers
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference list handler with pagination
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` (from Task 1) — extend rather than create a second service

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with `PaginatedResults` of per-product entries containing `total`, `open`, `in_progress`, `resolved`
- [ ] For each product, `total == open + in_progress + resolved`
- [ ] `offset`/`limit` pagination works and `total` reflects the full product count
- [ ] Products with no correlated vulnerabilities are either omitted or returned with zero counts, consistently and documented in the handler doc comment
- [ ] No new tables or migrations are introduced

## Test Requirements
- [ ] Integration test: two products with different status mixes return correct per-product counts
- [ ] Integration test: pagination (`limit=1`) returns one item and the correct `total`
- [ ] Integration test: empty database returns `{ items: [], total: 0 }` with 200

## Verification Commands
- `cargo test -p tests remediation` — all remediation integration tests pass
- `curl -s 'localhost:8080/api/v2/remediation/by-product?limit=10' | jq .` — returns paginated product breakdown

## Documentation Updates
- `README.md` — add `GET /api/v2/remediation/by-product` to the API endpoint list

## Dependencies
- Depends on: Task 1 — Add remediation module and GET /api/v2/remediation/summary endpoint
