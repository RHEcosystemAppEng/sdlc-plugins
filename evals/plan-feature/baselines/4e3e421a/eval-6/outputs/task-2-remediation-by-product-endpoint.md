## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/remediation/by-product` endpoint to the remediation module created in Task 1. It returns a paginated, per-product remediation breakdown where each product entry includes total, open, in-progress and resolved counts. This supports UC-2 (Filter by product) and the TC-9006 requirement for a per-product breakdown; pagination addresses the customer consideration that large portfolios (>50 products) need paging.

## Files to Modify
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the `/by-product` route
- `modules/fundamental/src/remediation/model/mod.rs` — export the new product model
- `modules/fundamental/src/remediation/service/mod.rs` — add `RemediationService::by_product()` aggregation
- `tests/api/remediation.rs` — add by-product integration tests

## Files to Create
- `modules/fundamental/src/remediation/model/product.rs` — `ProductRemediation` response struct
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler

## API Changes
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}&sort={field}` — NEW: returns `PaginatedResults<ProductRemediation>`:
  `{ "items": [ { "product_id": string, "product_name": string, "total": number, "open": number, "in_progress": number, "resolved": number } ], "total": number }`

## Implementation Notes
- Wrap the response in `PaginatedResults<T>` from `common/src/model/paginated.rs`, matching `GET /api/v2/sbom` in `modules/fundamental/src/sbom/endpoints/list.rs`.
- Apply offset/limit and sorting via the shared helpers in `common/src/db/query.rs` — do not hand-roll pagination.
- "Product" is not a standalone entity in `entity/src/`. Group by the SBOM's product identity (derived from `entity/src/sbom.rs` / `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`); confirm the product key with the feature owner (see impact map "Open questions").
- Reuse the status-derivation function introduced in `RemediationService` by Task 1 so per-product counts are consistent with the summary endpoint.
- Perform the aggregation as a grouped SQL query over `entity/src/sbom_advisory.rs` joined to `entity/src/sbom.rs`; do not aggregate in Rust.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's list endpoint (`endpoints/*.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's service query (`.rs`) scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` use the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/` scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): Conventional Commits with Jira footer and `Assisted-by: Claude Code` trailer (§2.1–2.3); PR with `--base main`, PR link posted to Jira (§3.2–3.3); scope changes to listed files and reuse existing helpers (§5.1–5.4).

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper
- `common/src/db/query.rs` — shared pagination/sorting helpers
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation of a paginated list endpoint
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` — status derivation from Task 1

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/by-product` returns HTTP 200 with `PaginatedResults<ProductRemediation>`
- [ ] Each item includes `total`, `open`, `in_progress`, `resolved`, and `total` = open + in_progress + resolved
- [ ] `offset` and `limit` paginate results; top-level `total` reports the full product count
- [ ] Sum of per-product counts is consistent with `/api/v2/remediation/summary` for the same dataset
- [ ] Products with no correlated vulnerabilities are either omitted or reported with zero counts — behaviour is documented and tested

## Test Requirements
- [ ] Integration test: seed two or more products with distinct vulnerability statuses; assert per-product counts
- [ ] Integration test: pagination with `limit=1` returns one item and correct `total`
- [ ] Integration test: per-product totals reconcile with the summary endpoint
- [ ] Integration test: empty database returns 200 with `items: []` and `total: 0`

## Verification Commands
- `cargo test --test api remediation` — by-product tests pass
- `curl -s "http://localhost:8080/api/v2/remediation/by-product?limit=10" | jq .` — returns paginated product breakdown

## Documentation Updates
- `README.md` — add `GET /api/v2/remediation/by-product` to the API endpoint overview

## Dependencies
- Depends on: Task 1 — Add remediation module and summary endpoint
