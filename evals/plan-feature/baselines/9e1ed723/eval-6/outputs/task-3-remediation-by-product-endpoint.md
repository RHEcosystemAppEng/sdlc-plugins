# Task 3 — Add GET /api/v2/remediation/by-product endpoint

**Summary:** Add GET /api/v2/remediation/by-product per-product remediation breakdown endpoint
**Parent Epic:** TC-9006: trustify-backend (Epic group "trustify-backend")

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Implement `GET /api/v2/remediation/by-product`. It returns a per-product remediation breakdown in which each product entry has total, open, and resolved counts (TC-9006 requirement 2). The dashboard uses it for the product breakdown and to fill the product filter dropdown (UC-2). The feature notes that large portfolios (>50 products) may need pagination, so the endpoint is paginated with `PaginatedResults<T>`.

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — export the new `ProductRemediation` model
- `modules/fundamental/src/remediation/service/mod.rs` — add `RemediationService::by_product()` aggregation
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the `/by-product` route
- `tests/api/remediation.rs` — add by-product integration tests

## Files to Create
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation { product: String, total: u64, open: u64, in_progress: u64, resolved: u64 }`
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler

## API Changes
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}&sort={field}` — NEW: returns `PaginatedResults<ProductRemediation>` = `{ "items": [ { "product": string, "total": u64, "open": u64, "in_progress": u64, "resolved": u64 } ], "total": u64 }`

## Implementation Notes
- Builds on the remediation module created in Task 2. Follow the same handler and service layout as `modules/fundamental/src/remediation/endpoints/summary.rs`.
- Paginate and sort with the shared helpers in `common/src/db/query.rs` and return `PaginatedResults<T>` from `common/src/model/paginated.rs`, the same way `modules/fundamental/src/sbom/endpoints/list.rs` does.
- "Product" is not a separate entity in `entity/src/`. Derive the product identity from the SBOM (`entity/src/sbom.rs`, e.g., the SBOM name/product metadata exposed by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`). Group across SBOM versions of the same product. Confirm the product attribute during implementation and record the choice in the PR (see impact map Open questions).
- Group in SQL (`GROUP BY product`) joining `sbom` → `sbom_advisory` → `advisory`. No new tables.
- `total = open + in_progress + resolved` for each item. The feature lists only total/open/resolved, but `in_progress` is included so the counts add up and match the summary endpoint.
- Per CONVENTIONS.md §Response types: return `PaginatedResults<T>` for list endpoints. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust list-endpoint (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Query helpers: use `common/src/db/query.rs` for pagination and sorting. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust service/query (`.rs`) scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/advisory/endpoints/list.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's integration-test (`tests/api/*.rs`) scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.3 `gh pr create --base TC-9006`; §5.1–5.8 code change rules; §1.4–1.6 implement-task scope rules.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — paginated response wrapper
- `common/src/db/query.rs` — pagination/sorting helpers
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM listing queries; reuse its product/name projection
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` (from Task 2) — reuse the status/severity derivation so both endpoints count the same way

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns 200 with `PaginatedResults<ProductRemediation>`
- [ ] Each product entry includes total, open, and resolved counts (and in_progress), with `total = open + in_progress + resolved`
- [ ] `offset`/`limit` pagination works and `total` reports the number of products
- [ ] The sum of per-product counts matches `/api/v2/remediation/summary` totals under the same counting rule
- [ ] No new database tables or migrations

## Test Requirements
- [ ] Integration test: an empty database returns `{ items: [], total: 0 }`
- [ ] Integration test: seeded data for 3 products returns correct per-product counts
- [ ] Integration test: pagination with `limit=2` over 3 products returns 2 items and `total = 3`; `offset=2` returns the remaining item
- [ ] Integration test: multiple SBOM versions of the same product are combined into one product entry

## Verification Commands
- `cargo test --test api remediation` — all remediation tests pass
- `curl -s "http://localhost:8080/api/v2/remediation/by-product?limit=10" | jq '.total'` — returns the product count

## Documentation Updates
- `README.md` — add `/api/v2/remediation/by-product` to the API endpoint overview (Task 8 covers the full documentation)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary endpoint
