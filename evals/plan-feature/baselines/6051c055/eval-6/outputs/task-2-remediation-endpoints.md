## Repository
trustify-backend

## Target Branch
main

## Description
Add REST endpoints for the remediation tracking dashboard feature (TC-9006). This task creates two new endpoints under `/api/v2/remediation/`:

- `GET /api/v2/remediation/summary` — returns aggregated remediation counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — returns per-product remediation breakdown with total, open, and resolved counts per product

Both endpoints follow the established Axum handler pattern used by existing domain modules and are mounted via the server's route registration.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`, registers both endpoint handlers
- `modules/fundamental/src/remediation/endpoints/summary.rs` — handler for `GET /api/v2/remediation/summary`
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — handler for `GET /api/v2/remediation/by-product`

## Files to Modify
- `server/src/main.rs` — mount the remediation module routes alongside existing modules (sbom, advisory, package, search)
- `modules/fundamental/src/remediation/mod.rs` — register the `endpoints` submodule

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns RemediationSummary with severity x status counts
- `GET /api/v2/remediation/by-product` — NEW: returns list of ProductRemediation entries with per-product breakdown

## Implementation Notes
- Follow the endpoint registration pattern from existing modules. See `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration and `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure.
- Each handler should accept the Axum extractor for the service (via dependency injection) and return the appropriate model type.
- The by-product endpoint should support pagination using `PaginatedResults<T>` from `common/src/model/paginated.rs`, consistent with other list endpoints.
- Apply `tower-http` caching middleware configuration on the route builder, following the caching pattern used by existing endpoint modules.
- Mount routes in `server/src/main.rs` following the same pattern as other module mounts (e.g., `.merge(sbom::endpoints::router(...))`).
- The summary endpoint NFR requires p95 < 500ms response time. Consider adding appropriate cache headers.

Per CONVENTIONS.md Section "Endpoint registration": each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md Section "Error handling": all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md Section "Response types": list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern and Axum router setup
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint handler with pagination support
- `modules/fundamental/src/advisory/endpoints/mod.rs` — reference for route registration pattern
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper for the by-product endpoint

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns JSON with aggregated counts by severity and status
- [ ] GET /api/v2/remediation/by-product returns JSON with per-product remediation breakdown including total, open, and resolved counts
- [ ] Both endpoints return proper error responses (AppError) on failure
- [ ] Routes are mounted in server/src/main.rs and accessible
- [ ] The by-product endpoint supports pagination consistent with other list endpoints
- [ ] Summary endpoint response time meets p95 < 500ms NFR

## Test Requirements
- [ ] Verify GET /api/v2/remediation/summary returns 200 with valid JSON when vulnerabilities exist
- [ ] Verify GET /api/v2/remediation/summary returns zero counts when no vulnerabilities exist
- [ ] Verify GET /api/v2/remediation/by-product returns 200 with valid JSON and per-product entries
- [ ] Verify pagination parameters are accepted and applied on the by-product endpoint

## Verification Commands
- `cargo build -p trustify-server` — server compiles with new routes
- `curl http://localhost:8080/api/v2/remediation/summary` — returns valid JSON response

## Dependencies
- Depends on: Task 1 — Create remediation domain models and aggregation service
