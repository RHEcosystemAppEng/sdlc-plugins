## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add the `GET /api/v2/remediation/summary` endpoint that returns aggregated vulnerability remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). The endpoint delegates to `RemediationService::get_summary()` and returns the result as JSON.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for remediation endpoints
- `modules/fundamental/src/remediation/endpoints/summary.rs` — handler for GET /api/v2/remediation/summary

## Files to Modify
- `server/src/main.rs` — mount the remediation endpoint routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns `RemediationSummary` with severity × status count matrix

## Implementation Notes
- Follow the endpoint registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — register routes in the module's `endpoints/mod.rs` and mount in `server/src/main.rs`.
- The handler should accept optional query parameters for date range filtering (to support the 30-day trend view in the frontend).
- Use the `AppError` error type for handler return values, matching the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per Key Conventions: endpoint registration follows the pattern where each module's `endpoints/mod.rs` registers routes and `server/main.rs` mounts all modules.
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per Key Conventions: handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust error handling scope.
- Non-functional requirement: p95 response time < 500ms. Consider using `tower-http` caching middleware on this route as done in other endpoint route builders.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `modules/fundamental/src/sbom/endpoints/list.rs` — example list handler with query parameters
- `common/src/error.rs::AppError` — error handling pattern

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with JSON body containing severity × status counts
- [ ] Endpoint is registered in `server/src/main.rs`
- [ ] Handler uses `RemediationService::get_summary()` for data retrieval
- [ ] Optional date range query parameters are accepted

## Test Requirements
- [ ] Handler returns 200 with valid JSON for a successful request
- [ ] Handler returns appropriate error codes for invalid query parameters

## Verification Commands
- `cargo check -p trustify-server` — verify compilation with new route
- `cargo test -p trustify-fundamental remediation` — run remediation tests

## Dependencies
- Depends on: Task 1 — Remediation summary model and service
