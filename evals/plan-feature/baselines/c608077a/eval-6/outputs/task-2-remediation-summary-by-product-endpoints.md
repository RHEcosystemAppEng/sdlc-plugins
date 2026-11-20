## Repository
trustify-backend

## Target Branch
main

## Description
Expose the two MVP aggregation endpoints required by TC-9006: `GET /api/v2/remediation/summary` (aggregated counts by severity x status) and `GET /api/v2/remediation/by-product` (per-product remediation breakdown). Endpoints wrap the `RemediationService` delivered in Task 1, are registered in a new `endpoints/` submodule of the remediation module, and are mounted in the Axum server.

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — add `pub mod endpoints;`
- `server/src/main.rs` — mount the remediation routes alongside the existing sbom/advisory/package modules

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation` (summary, by-product), including caching configuration
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler (offset/limit pagination)
- `tests/api/remediation.rs` — integration tests for the remediation endpoints

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns `RemediationSummary` — counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) plus per-status totals
- `GET /api/v2/remediation/by-product?offset={n}&limit={n}` — NEW: returns `PaginatedResults<ProductRemediation>` — each entry includes product, `total`, `open`, `in_progress`, `resolved`

## Implementation Notes
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` (registers `/api/v2/sbom`) and `modules/fundamental/src/advisory/endpoints/mod.rs`; handler bodies should mirror `modules/fundamental/src/sbom/endpoints/list.rs` (list with pagination) and `modules/fundamental/src/sbom/endpoints/get.rs` (single object response).
- Mount the new router in `server/src/main.rs` the same way existing modules are mounted.
- Summary endpoint performance target p95 < 500ms: apply `tower-http` caching middleware in the route builder (short TTL, e.g. 60s) following the existing caching configuration in endpoint route builders; heavy lifting stays in the SQL aggregation from Task 1.
- Serialize enum/status values with stable snake_case keys (`open`, `in_progress`, `resolved`) and severity keys matching `AdvisorySummary` severity values; the frontend (Task 4) maps them to display labels.
- Per CONVENTIONS.md §Endpoint registration: register routes in the module's `endpoints/mod.rs` and mount the module in `server/src/main.rs`. Applies: task modifies `server/src/main.rs` matching the convention's endpoint registration scope. Example: `modules/fundamental/src/advisory/endpoints/mod.rs`.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust handler `.rs` scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Response types: the by-product list endpoint returns `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's list endpoint scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Caching: configure `tower-http` caching in the remediation route builder. Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's endpoint route builder scope. Example: `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` against the real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/*.rs` scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md): §5.1 scope to listed files; §5.2 inspect before modifying; §5.4 reuse existing route/handler patterns; §5.8 parity with sibling endpoints (error handling, caching, logging); §2.1–2.3 commit rules; §3.1–3.3 PR rules (`--base main`).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration and caching configuration pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — paginated list handler pattern
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper
- `tests/api/sbom.rs` — integration test structure and DB seeding pattern

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with counts for all 12 severity x status combinations plus totals
- [ ] `GET /api/v2/remediation/by-product` returns 200 with a `PaginatedResults` body whose items contain `total`, `open`, `in_progress`, `resolved` per product
- [ ] `by-product` honors `offset`/`limit` and reports the correct `total` for portfolios with >50 products
- [ ] Both routes are mounted in `server/src/main.rs` and reachable under `/api/v2/remediation`
- [ ] Summary endpoint responds within p95 < 500ms on a dataset of 10,000 tracked vulnerabilities

## Test Requirements
- [ ] Integration test: `GET /api/v2/remediation/summary` on seeded data returns 200 and expected counts per cell
- [ ] Integration test: `GET /api/v2/remediation/summary` on an empty database returns 200 with all-zero counts
- [ ] Integration test: `GET /api/v2/remediation/by-product` returns correct per-product counts for two seeded products
- [ ] Integration test: `GET /api/v2/remediation/by-product?limit=1` returns one item and correct `total`

## Verification Commands
- `cargo test --test api remediation` — remediation integration tests pass
- `curl -s http://localhost:8080/api/v2/remediation/summary | jq .` — returns the aggregated summary JSON

## Documentation Updates
- `README.md` — list the new `/api/v2/remediation/summary` and `/api/v2/remediation/by-product` endpoints in the API overview

## Dependencies
- Depends on: Task 1 — Add remediation model and aggregation service
