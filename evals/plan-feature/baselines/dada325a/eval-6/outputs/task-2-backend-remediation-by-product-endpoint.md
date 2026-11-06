<!-- Jira creation metadata (simulated; not part of the description body) -->
<!-- Summary: Add per-product remediation breakdown endpoint | Simulated key: TC-9104 | Issue type: Task | Parent Epic: TC-9101 (TC-9006: trustify-backend) | Labels: ai-generated-jira | Priority: Major | fixVersions: RHTPA 1.5.0 -->

## Repository
trustify-backend

## Target Branch
main

## Description
Add `GET /api/v2/remediation/by-product` to the remediation module created in Task 1. The endpoint returns a per-product remediation breakdown — each product entry includes `total`, `open`, `in_progress`, and `resolved` counts — to support the dashboard's product view and product-scoped prioritization (TC-9006, UC-2). Because large portfolios (>50 products) are expected, the response is paginated using the shared `PaginatedResults<T>` wrapper. Aggregations are computed from existing SBOM/advisory relationship data (no new tables).

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — export the new by-product model
- `modules/fundamental/src/remediation/service/mod.rs` — add `RemediationService::by_product(query, paginated)`
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the `/by-product` route
- `tests/api/remediation.rs` — add by-product integration tests

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct (`product`, `total`, `open`, `in_progress`, `resolved`)
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler

## API Changes
- `GET /api/v2/remediation/by-product` — NEW: returns `PaginatedResults<ProductRemediation>` = `{ items: [{ product: string, total: u64, open: u64, in_progress: u64, resolved: u64 }], total: u64 }`. Query parameters: `offset`, `limit` (shared pagination), `sort` (e.g., `open:desc`), `severity` (optional filter).

## Implementation Notes
- "Product" is derived from the SBOM entity (`entity/src/sbom.rs`) — group `sbom_advisory` rows by the SBOM's product identifier. Verify at implementation time which SBOM field represents the product (e.g., SBOM name / document product); use that consistently with Task 3's `product` filter.
- Reuse the status/severity derivation introduced in Task 1's `RemediationService` (`modules/fundamental/src/remediation/service/mod.rs`) — extract a shared private helper rather than duplicating the status mapping.
- Pagination, sorting and filtering must use `common/src/db/query.rs` helpers, mirroring how `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` build list queries.
- Aggregate with SQL `GROUP BY` on the product column with `COUNT(*) FILTER (WHERE status = ...)` (or SeaORM equivalent); apply `LIMIT/OFFSET` in the database, not in memory.
- Return an empty `items` list with `total: 0` when no products have correlated vulnerabilities; propagate DB errors via `AppError` rather than returning an empty page.
- Per CONVENTIONS.md §Response types: return `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs` for this list endpoint. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's list endpoint scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Query helpers: use the shared filtering, pagination, and sorting helpers in `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust query scope. Example: `modules/fundamental/src/advisory/endpoints/list.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and wrap fallible calls with `.context()`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust handler scope. Example: `modules/fundamental/src/advisory/endpoints/get.rs`.
- Per CONVENTIONS.md §Endpoint registration: register the new route in the module's `endpoints/mod.rs`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's endpoint registration scope. Example: `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's integration test scope. Example: `tests/api/sbom.rs`.
- Commit rules (docs/constraints.md §2), PR rules (§3: `gh pr create --base main`), and code change rules (§5: scope to listed files, reuse Task 1 helpers, sibling parity with `list.rs` endpoints) apply.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for list endpoints
- `common/src/db/query.rs` — shared filtering/pagination/sorting helpers
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation of a paginated list endpoint
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` (from Task 1) — status/severity aggregation logic to share

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns HTTP 200 with `PaginatedResults<ProductRemediation>`
- [ ] Each item includes `product`, `total`, `open`, `in_progress`, `resolved`, and `total == open + in_progress + resolved`
- [ ] `offset`/`limit` pagination works and `total` reflects the full product count (supports >50 products)
- [ ] Optional `severity` filter restricts counts to the given severity
- [ ] No new database tables or migrations are introduced
- [ ] DB errors return an error response, not an empty page

## Test Requirements
- [ ] Integration test: seed three products with known vulnerability mixes and assert per-product counts
- [ ] Integration test: seed 60 products, request `limit=50` then `offset=50`, assert page sizes and `total == 60`
- [ ] Integration test: `severity=critical` returns only critical counts
- [ ] Integration test: empty database returns `{ items: [], total: 0 }`

## Verification Commands
- `cargo test --test api remediation` — by-product tests pass
- `curl -s 'localhost:8080/api/v2/remediation/by-product?limit=5' | jq '.total'` — returns product count

## Documentation Updates
- `README.md` — add `GET /api/v2/remediation/by-product` to the API endpoint overview

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint
