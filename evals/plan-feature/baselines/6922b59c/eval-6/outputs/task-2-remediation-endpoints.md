## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add REST API endpoints for the vulnerability remediation tracking dashboard. Create
`GET /api/v2/remediation/summary` returning aggregated remediation counts by severity
and status, and `GET /api/v2/remediation/by-product` returning per-product remediation
breakdowns. Register these routes in the server's route tree.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`, configures summary and by-product sub-routes
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler calling `RemediationService::get_summary()`
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — `GET /api/v2/remediation/by-product` handler calling `RemediationService::get_by_product()`

## Files to Modify
- `server/src/main.rs` — mount remediation routes alongside existing module routes (sbom, advisory, package, search)

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns `RemediationSummary` with aggregated counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved), plus top-level totals
- `GET /api/v2/remediation/by-product` — NEW: returns list of `ProductRemediation` entries, each with product name, total, open, and resolved counts

## Implementation Notes
- Follow the endpoint registration pattern from existing modules. See `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration and `server/src/main.rs` for mounting.
  Per CONVENTIONS.md §Endpoint Registration: each module's endpoints/mod.rs registers routes; server/main.rs mounts all modules.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.
- All handlers return `Result<T, AppError>` using the error handling pattern from `common/src/error.rs`.
  Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` file scope.
- The summary endpoint returns a `RemediationSummary` directly (not paginated), since it is a single aggregated response.
- The by-product endpoint should support optional pagination using `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs` to handle large portfolios (>50 products).
  Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` endpoint file scope.
- Use shared query parameter extraction from `common/src/db/query.rs` for any filtering or pagination parameters.
- Non-functional requirement: summary endpoint response time p95 < 500ms. Consider adding `tower-http` caching middleware on the summary route to meet this target.
  Per CONVENTIONS.md §Caching: use `tower-http` caching middleware for endpoint route builders.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern and Axum router configuration
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint handler implementation with query parameters
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for the by-product endpoint
- `common/src/db/query.rs` — shared query parameter handling for filtering and pagination

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns a valid `RemediationSummary` JSON response
- [ ] `GET /api/v2/remediation/by-product` returns a paginated list of `ProductRemediation` entries
- [ ] Both endpoints return appropriate HTTP status codes (200 for success, 500 for server errors)
- [ ] Remediation routes are mounted in `server/src/main.rs`
- [ ] Endpoints handle empty datasets gracefully (return zero counts, not errors)
- [ ] By-product endpoint supports pagination parameters (offset, limit)

## Test Requirements
- [ ] Handler test for `GET /api/v2/remediation/summary` verifying JSON response shape
- [ ] Handler test for `GET /api/v2/remediation/by-product` verifying paginated response shape
- [ ] Test that endpoints return 200 status with valid aggregation data
- [ ] Test that endpoints return empty/zero-count results when no data exists

## Verification Commands
- `cargo check -p trustify-server` — verify route mounting compiles
- `cargo test -p trustify-module-fundamental -- remediation::endpoints` — run endpoint-specific tests

## Documentation Updates
- `README.md` — add remediation endpoints to the API endpoint listing

## Dependencies
- Depends on: Task 1 — Add remediation model structs and aggregation service
