## Repository
trustify-backend

## Target Branch
main

## Description
Expose the remediation aggregations from Task 1 as REST endpoints for TC-9006: `GET /api/v2/remediation/summary` (counts by severity x status) and `GET /api/v2/remediation/by-product` (paginated per-product breakdown). Register the routes in the remediation module and mount the module in the server. These endpoints are consumed by the trustify-ui remediation dashboard (summary cards and product filter).

## Files to Modify
- `server/src/main.rs` — mount the remediation module routes alongside existing modules
- `README.md` — add the new remediation endpoints to the API overview

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation/*`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler
- `tests/api/remediation.rs` — integration tests for the remediation endpoints

## API Changes
- `GET /api/v2/remediation/summary` — NEW: query param `product` (optional string). Response `RemediationSummary`: `{ total: number, by_status: { open: number, in_progress: number, resolved: number }, by_severity: [{ severity: "critical"|"high"|"medium"|"low", open: number, in_progress: number, resolved: number, total: number }] }`
- `GET /api/v2/remediation/by-product` — NEW: query params `offset`, `limit` (optional), `sort` (optional). Response `PaginatedResults<ProductRemediation>`: `{ items: [{ product_id: string, product_name: string, total: number, open: number, in_progress: number, resolved: number }], total: number }`

## Implementation Notes
- Mirror route registration in `modules/fundamental/src/advisory/endpoints/mod.rs` and handler shape in `modules/fundamental/src/advisory/endpoints/list.rs` / `get.rs`.
- Mount in `server/src/main.rs` the same way the `sbom`, `advisory`, and `package` modules are mounted.
- Handlers call `RemediationService::summary` / `RemediationService::by_product` from Task 1; no aggregation logic in handlers.
- Caching: the summary is portfolio-wide and relatively expensive — configure the `tower-http` caching middleware in the route builder (as existing endpoint route builders do) with a short max-age to help meet the p95 < 500ms target.
- Per CONVENTIONS.md §Endpoint registration: register routes in `modules/fundamental/src/remediation/endpoints/mod.rs` and mount the module in `server/src/main.rs`; see `modules/fundamental/src/sbom/endpoints/mod.rs`.
  Applies: task modifies `server/src/main.rs` matching the convention's Rust endpoint-registration (`endpoints/mod.rs`, `server/src/main.rs`) scope.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust (`.rs`) handler scope.
- Per CONVENTIONS.md §Response types: the by-product list endpoint returns `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust list-endpoint scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit the PostgreSQL test database and assert with `assert_eq!(resp.status(), StatusCode::OK)`; follow `tests/api/advisory.rs`.
  Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/*.rs` integration-test scope.
- Constraints (docs/constraints.md): §5.1 scope to listed files; §5.2 inspect existing endpoint modules before writing; §5.4 reuse `PaginatedResults` and query helpers; §5.8 parity with sibling endpoints on caching and error handling; §2.1–2.3 commit rules; §3.3 PR `--base main`.

## Reuse Candidates
- `modules/fundamental/src/advisory/endpoints/mod.rs` — route registration pattern
- `modules/fundamental/src/advisory/endpoints/list.rs` — paginated list handler pattern
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper
- `tests/api/advisory.rs` — integration test structure and DB fixtures

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with the `RemediationSummary` shape including all four severities
- [ ] `GET /api/v2/remediation/summary?product=<name>` returns counts restricted to that product
- [ ] `GET /api/v2/remediation/by-product` returns 200 with `PaginatedResults<ProductRemediation>` and honors `offset`/`limit`
- [ ] Routes are mounted in `server/src/main.rs` and reachable in the running server
- [ ] Summary endpoint p95 < 500ms with 10,000 tracked vulnerabilities in the test dataset
- [ ] README lists the new endpoints

## Test Requirements
- [ ] Integration test: summary endpoint returns 200 and correct counts for a seeded dataset
- [ ] Integration test: summary with `product` filter returns filtered counts
- [ ] Integration test: by-product endpoint pagination and per-product counts
- [ ] Integration test: empty dataset returns 200 with zero counts
- [ ] Performance check: summary endpoint against a 10,000-vulnerability fixture stays under 500ms p95

## Verification Commands
- `cargo test --test api remediation` — remediation integration tests pass
- `curl -s localhost:8080/api/v2/remediation/summary | jq .by_severity` — returns four severity entries

## Documentation Updates
- `README.md` — add `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` to the API endpoint list

## Dependencies
- Depends on: Task 1 — Remediation aggregation model and service
