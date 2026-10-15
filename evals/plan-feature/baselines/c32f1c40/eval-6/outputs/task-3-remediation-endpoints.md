## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add REST endpoints for the vulnerability remediation tracking dashboard. Implements `GET /api/v2/remediation/summary` for aggregated remediation counts by severity and status, and `GET /api/v2/remediation/by-product` for per-product remediation breakdown. These endpoints are consumed by the frontend remediation dashboard.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for /api/v2/remediation, mounts summary and by-product handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET /api/v2/remediation/summary handler returning aggregated counts
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- GET /api/v2/remediation/by-product handler returning per-product breakdown

## Files to Modify
- `server/src/main.rs` -- mount the remediation module routes alongside existing module routes (sbom, advisory, search)

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns aggregated vulnerability remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). Response shape: `{ entries: RemediationSummaryEntry[], totals: { open: number, in_progress: number, resolved: number } }`
- `GET /api/v2/remediation/by-product` -- NEW: returns per-product remediation breakdown. Response shape: `PaginatedResults<ProductRemediation>` where each entry has product name, total, open, and resolved counts. Supports pagination and sorting query parameters.

## Implementation Notes
- Per backend conventions: each module's `endpoints/mod.rs` registers routes, and `server/main.rs` mounts all modules. Follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration.
- Per backend conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. See `modules/fundamental/src/sbom/endpoints/get.rs` for the handler pattern.
- Per backend conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Apply this to the by-product endpoint.
- Per backend conventions: use `common/src/db/query.rs` for filtering, pagination, and sorting in the by-product endpoint.
- Per backend conventions: configure `tower-http` caching middleware on the endpoint route builders. See existing endpoint configurations for the caching pattern.
- Per NFR: summary endpoint response time must be p95 < 500ms. Ensure the aggregation query is efficient -- use a single query with GROUP BY rather than multiple round trips.
- Per NFR: must handle up to 10,000 tracked vulnerabilities without performance degradation. Use server-side pagination for the by-product endpoint.
- Constraints: per docs/constraints.md section 2, commit messages must follow Conventional Commits format and reference TC-9006. Per section 5, changes must be scoped to the files listed.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern for Axum. Follow the same structure for remediation routes.
- `modules/fundamental/src/sbom/endpoints/list.rs` -- GET handler pattern with pagination. Reference for by-product endpoint implementation.
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET handler pattern for single-entity retrieval. Reference for summary endpoint.
- `common/src/db/query.rs` -- shared query builder helpers. Use for by-product endpoint filtering and pagination.
- `common/src/model/paginated.rs` -- PaginatedResults<T> wrapper. Use for by-product endpoint response.

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns aggregated counts grouped by severity and status
- [ ] GET /api/v2/remediation/by-product returns paginated per-product remediation breakdown
- [ ] Summary endpoint returns correct totals for open, in-progress, and resolved
- [ ] By-product endpoint supports pagination query parameters (offset, limit)
- [ ] By-product endpoint supports sorting query parameters
- [ ] Routes are registered in server/src/main.rs and accessible at the documented paths
- [ ] Error responses follow the AppError format used by other endpoints

## Test Requirements
- [ ] Verify summary endpoint returns 200 with correct JSON structure
- [ ] Verify by-product endpoint returns 200 with PaginatedResults structure
- [ ] Verify by-product endpoint pagination works correctly
- [ ] Verify both endpoints return empty results (not errors) when no vulnerability data exists

## Verification Commands
- `cargo build -p trustify-server` -- compiles without errors
- `cargo test -p trustify-server -- remediation` -- all remediation endpoint tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 2 -- Add remediation data models and aggregation service
