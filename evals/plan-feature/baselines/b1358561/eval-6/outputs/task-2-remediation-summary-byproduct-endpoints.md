**Summary:** Add GET /api/v2/remediation/summary and /api/v2/remediation/by-product endpoints
**Parent Epic:** TC-9101 (TC-9006: trustify-backend)
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Major | **fixVersions:** RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Expose the remediation aggregations from Task 1 over REST so the remediation dashboard (TC-9006) can render summary cards and the per-product breakdown. Register the new `/api/v2/remediation` route group and mount it in the server.

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — expose the new `endpoints` module
- `server/src/main.rs` — mount the remediation routes alongside sbom/advisory/package

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler
- `tests/api/remediation.rs` — integration tests for remediation endpoints

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns `RemediationSummary` `{ totals: { open, in_progress, resolved, total }, by_severity: [{ severity, open, in_progress, resolved, total }] }`
- `GET /api/v2/remediation/by-product?offset=&limit=` — NEW: returns `PaginatedResults<ProductRemediation>` `{ items: [{ product_name, total, open, in_progress, resolved }], total }`

## Implementation Notes
- Mirror the endpoint structure in `modules/fundamental/src/advisory/endpoints/mod.rs` (route registration) and `modules/fundamental/src/advisory/endpoints/list.rs` / `get.rs` (handler shape, extracting pagination query params, calling the service).
- Handlers call `RemediationService::summary()` and `RemediationService::by_product()` from `modules/fundamental/src/remediation/service/remediation.rs` (Task 1).
- Per CONVENTIONS.md §Endpoint registration: register routes in `modules/fundamental/src/remediation/endpoints/mod.rs` and mount the module in `server/src/main.rs` the same way the sbom/advisory modules are mounted.
  Applies: task modifies `server/src/main.rs` matching the convention's Rust endpoint registration (`endpoints/mod.rs`, `server/main.rs`) scope.
- Per CONVENTIONS.md §Error handling: handlers return `Result<Json<T>, AppError>` with `.context()` wrapping; see `modules/fundamental/src/advisory/endpoints/get.rs`.
  Applies: task modifies `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust handler `.rs` scope.
- Per CONVENTIONS.md §Response types: `by-product` returns `PaginatedResults<ProductRemediation>` (`common/src/model/paginated.rs`).
  Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's Rust list endpoint `.rs` scope.
- Per CONVENTIONS.md §Caching: configure short-lived `tower-http` cache headers in the route builder for the summary endpoint to help meet p95 < 500ms; follow the cache configuration in existing endpoint route builders (e.g., `modules/fundamental/src/sbom/endpoints/mod.rs`).
  Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Testing: add `tests/api/remediation.rs` as an integration test against the PostgreSQL test DB using `assert_eq!(resp.status(), StatusCode::OK)`; follow `tests/api/advisory.rs`.
  Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/` integration test scope.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules.

## Reuse Candidates
- `modules/fundamental/src/advisory/endpoints/mod.rs` — route registration pattern
- `modules/fundamental/src/advisory/endpoints/list.rs` — paginated list handler pattern
- `tests/api/advisory.rs` — integration test setup and assertion pattern

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with severity x status counts and per-status totals
- [ ] `GET /api/v2/remediation/by-product` returns 200 with a `PaginatedResults` body, honoring `offset` and `limit`
- [ ] Routes are registered in `modules/fundamental/src/remediation/endpoints/mod.rs` and mounted in `server/src/main.rs`
- [ ] Enum values in responses are `snake_case` (`in_progress`, `critical`, ...)
- [ ] Summary endpoint p95 latency < 500ms with 10,000 tracked vulnerabilities

## Test Requirements
- [ ] Integration test: summary endpoint returns 200 and correct counts for seeded data
- [ ] Integration test: summary endpoint returns 200 with zero counts on an empty dataset
- [ ] Integration test: by-product endpoint returns correct per-product counts and pagination (`offset`/`limit`, `total`)

## Verification Commands
- `cargo test --test api remediation` — all remediation integration tests pass
- `curl -s localhost:8080/api/v2/remediation/summary | jq .totals` — returns open/in_progress/resolved/total counts

## Documentation Updates
- `README.md` — list the new `/api/v2/remediation/*` endpoints in the API overview (if the README enumerates endpoints)

## Dependencies
- Depends on: Task 1 — Add remediation domain module with summary and per-product aggregation service
