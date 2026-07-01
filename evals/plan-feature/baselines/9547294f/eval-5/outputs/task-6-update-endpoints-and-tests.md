# Task 6 — Update advisory endpoints and integration tests

**Priority:** High
**Fix Versions:** RHTPA 2.0.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint handlers to work with the new enum-based status column and update integration tests to verify the advisory list and detail endpoints return correct results with the new schema. Ensure the API response shape remains identical (status as a string) so that no downstream consumers are broken.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to use the enum column instead of the join; ensure query parameters for status filtering map to `AdvisoryStatusEnum` variants
- `modules/fundamental/src/advisory/endpoints/get.rs` — update detail response construction if it directly references the advisory_status join
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any routes reference advisory_status-related handlers
- `tests/api/advisory.rs` — update integration tests to verify: (1) advisory list returns correct status strings, (2) status filter query parameter works with enum values, (3) advisory detail includes correct status

## Implementation Notes
- The API response shape must remain unchanged — `status` is still a string field in the JSON response. The enum-to-string conversion should happen in the model layer (Task 4), so endpoint handlers may not need significant changes beyond removing any `advisory_status` join setup
- For status filter query parameters, parse the incoming string to `AdvisoryStatusEnum` and pass it to the service layer
- Per CONVENTIONS.md Key Conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs` (Response types convention). Follow the existing test pattern using `assert_eq!(resp.status(), StatusCode::OK)` (Testing convention).
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.
- Per CONVENTIONS.md Key Conventions: use `tower-http` caching middleware patterns in endpoint route builders (Caching convention).
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint file scope.
- Follow the endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` for list handler implementation without join-based filtering
- Integration tests should verify that the response JSON shape is identical to the pre-migration shape (status is a plain string, not an object)

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint handler pattern with pagination and filtering
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for detail endpoint handler pattern
- `tests/api/sbom.rs` — reference for integration test patterns (test setup, assertions, status code checks)
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by list endpoints

## Acceptance Criteria
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) returns correct results with status as a string
- [ ] Status filter query parameter works correctly with enum-based filtering
- [ ] Advisory detail endpoint (`GET /api/v2/advisory/{id}`) returns correct status string
- [ ] API response shape is identical to pre-migration shape (no breaking changes)
- [ ] All advisory integration tests pass

## Test Requirements
- [ ] Integration test: `GET /api/v2/advisory` returns advisory list with status strings (New, Analyzing, Fixed, Rejected)
- [ ] Integration test: `GET /api/v2/advisory?status=Fixed` returns only advisories with Fixed status
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns advisory detail with correct status string
- [ ] Integration test: verify response JSON shape matches pre-migration format (status is a string, not an object or enum key)

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory integration tests pass
- `cargo test` — full test suite passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7
