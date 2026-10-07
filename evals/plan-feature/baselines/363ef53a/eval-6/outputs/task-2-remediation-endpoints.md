## Repository
trustify-backend

## Target Branch
main

## Description
Create REST endpoints for the remediation module: `GET /api/v2/remediation/summary` returns aggregated counts by severity and status, and `GET /api/v2/remediation/by-product` returns per-product remediation breakdown. Register the routes in the server's main route configuration.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for /api/v2/remediation, configures sub-routes for summary and by-product
- `modules/fundamental/src/remediation/endpoints/summary.rs` — GET /api/v2/remediation/summary handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler

## Files to Modify
- `server/src/main.rs` — mount remediation endpoint routes alongside existing module routes
- `modules/fundamental/src/remediation/mod.rs` — add `pub mod endpoints;` to expose the endpoints sub-module

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — NEW: returns per-product remediation breakdown with total, open, in_progress, and resolved counts per product entry

## Implementation Notes
- Follow the endpoint registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — each endpoint module defines its route handler and the `mod.rs` file registers them under the `/api/v2/remediation` prefix.
- Mount the remediation routes in `server/src/main.rs` following the same pattern used for SBOM and advisory route mounting.
- The summary endpoint handler should call `RemediationService::get_summary()` and return the result serialized as JSON.
- The by-product endpoint should support pagination via `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs`, using query helpers from `common/src/db/query.rs`.
- Per CONVENTIONS.md §Error Handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust handler file scope.
- Per CONVENTIONS.md §Endpoint Registration: register routes in `endpoints/mod.rs` and mount in `server/main.rs`. Applies: task modifies `server/src/main.rs` matching the convention's route mounting scope.
- Per CONVENTIONS.md §Response Types: use `PaginatedResults<T>` for list endpoints. Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Caching: configure `tower-http` caching middleware for the new routes if appropriate for aggregation data. Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's route configuration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow for organizing sub-routes
- `modules/fundamental/src/sbom/endpoints/list.rs` — list endpoint implementation pattern with pagination
- `common/src/error.rs::AppError` — error type for handler return values
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper for by-product endpoint

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns JSON with severity and status breakdowns
- [ ] `GET /api/v2/remediation/by-product` returns paginated product remediation data
- [ ] Remediation routes are registered and accessible in the running server
- [ ] p95 response time for summary endpoint is under 500ms
- [ ] Error responses use the standard `AppError` format

## Test Requirements
- [ ] Verify summary endpoint returns correct JSON structure with severity and status groups
- [ ] Verify by-product endpoint supports pagination parameters (offset, limit)
- [ ] Verify error handling for edge cases (no data, invalid parameters)

## Verification Commands
- `cargo build -p trustify-server` — compiles without errors
- `curl http://localhost:8080/api/v2/remediation/summary` — returns valid JSON response

## Dependencies
- Depends on: Task 1 — Add remediation module with model structs and aggregation service
