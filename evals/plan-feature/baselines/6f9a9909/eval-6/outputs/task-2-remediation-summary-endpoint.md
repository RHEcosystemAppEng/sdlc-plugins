## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/remediation/summary` endpoint that returns aggregated vulnerability remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). This endpoint serves the summary cards on the frontend remediation dashboard. The p95 response time must be under 500ms per non-functional requirements.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- endpoint submodule root with route registration for the remediation module
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET handler for `/api/v2/remediation/summary`

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` -- register the endpoints submodule
- `server/src/main.rs` -- mount the remediation module routes alongside existing modules (sbom, advisory, search)

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns `RemediationSummary` with aggregated counts by severity x status

## Implementation Notes
Per CONVENTIONS.md "Endpoint registration": each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`.
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

Per CONVENTIONS.md "Caching": use `tower-http` caching middleware in the endpoint route builder to meet the p95 < 500ms response time requirement. See existing endpoint route builders for cache configuration patterns.
Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` endpoint scope.

Per CONVENTIONS.md "Error handling": handler must return `Result<Json<RemediationSummary>, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` file scope.

Relevant constraints from `docs/constraints.md`:
- Per SS5.3: Implementation must follow the patterns referenced in these Implementation Notes.
- Per SS5.2: Inspect existing endpoint code before writing new handlers.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- reference implementation for route registration pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference implementation for GET list handler with response serialization
- `common/src/error.rs::AppError` -- error type for handler return signatures

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns HTTP 200 with JSON body containing aggregated counts
- [ ] Response includes counts for all four severity levels (Critical, High, Medium, Low)
- [ ] Response includes counts for all three status values (Open, In Progress, Resolved)
- [ ] Endpoint is registered and reachable via the Axum router
- [ ] Route is mounted in `server/src/main.rs`

## Test Requirements
- [ ] Verify endpoint returns 200 with valid RemediationSummary JSON
- [ ] Verify response structure matches the RemediationSummary model schema
- [ ] Verify endpoint handles empty dataset (no vulnerabilities) gracefully

## Verification Commands
- `cargo test --test api remediation` -- runs remediation endpoint integration tests (after Task 4)
- `cargo build` -- verifies compilation with new endpoint

## Dependencies
- Depends on: Task 1 -- Add remediation data models and aggregation service

## Parent Epic
TC-9007
