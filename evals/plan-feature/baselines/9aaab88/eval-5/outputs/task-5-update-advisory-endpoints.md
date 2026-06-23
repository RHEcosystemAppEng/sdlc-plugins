## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST endpoints to use the enum-based status filtering instead of the join-based approach. The list endpoint's status filter query parameter must map to `AdvisoryStatusEnum` variants, and the get endpoint must return status from the enum column. The response shape remains unchanged — status is still a string — so this is a transparent optimization for API consumers.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to parse and compare against `AdvisoryStatusEnum` variants; remove any query logic that joins `advisory_status`
- `modules/fundamental/src/advisory/endpoints/get.rs` — update advisory detail retrieval to read status from the enum column; remove any advisory_status join logic
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update imports if the status filter type changes; remove any `advisory_status` entity imports

## Implementation Notes
- In `modules/fundamental/src/advisory/endpoints/list.rs`, the status filter query parameter (e.g., `?status=Fixed`) currently maps to a lookup table join. Update the filter to parse the string into an `AdvisoryStatusEnum` variant and pass it to the service layer.
- Follow the existing endpoint pattern: handlers return `Result<T, AppError>`, list endpoints return `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs`.
- The response serialization should not change — `AdvisoryStatusEnum` variants serialize to their string values (New, Analyzing, Fixed, Rejected) which matches the current API contract.
- Route registration in `modules/fundamental/src/advisory/endpoints/mod.rs` should not need structural changes, only import updates.
- Per CONVENTIONS.md §Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Key Conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint file scope.

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` status filter works with enum column (no join)
- [ ] `GET /api/v2/advisory/{id}` returns status from enum column
- [ ] API response shape is unchanged — status field is still a string
- [ ] No remaining `advisory_status` imports in endpoint modules
- [ ] Endpoints module compiles with `cargo check -p fundamental`

## Test Requirements
- [ ] Advisory list endpoint returns correct results when filtering by each status value (New, Analyzing, Fixed, Rejected)
- [ ] Advisory get endpoint returns correct status string
- [ ] Invalid status filter values return appropriate error response
- [ ] Response JSON shape matches the pre-migration format

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and model layer

[sdlc-workflow] Description digest: sha256-md:8a84d29fb2b7ef5c530f633b701cfd1850b642247e7dbd2a394a2b1878318de9
