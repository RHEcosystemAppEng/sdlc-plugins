## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing p95 latency on the advisory list endpoint.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` table join from fetch, list, and search queries; filter directly on `advisory.status` enum column
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source status from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to source status from the enum column
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against enum values
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update single advisory fetch to use enum column

## Implementation Notes
In `modules/fundamental/src/advisory/service/advisory.rs`, the `AdvisoryService` methods (fetch, list, search) currently join the `advisory_status` table to resolve status names. Remove all `advisory_status` join clauses and replace them with direct column access on `advisory.status`. Use the `AdvisoryStatusEnum` from the updated entity definitions.

For status filtering in `modules/fundamental/src/advisory/endpoints/list.rs`, update the query filter to use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` (SeaORM enum comparison) instead of the previous join-based filter.

Follow the existing query builder patterns in `common/src/db/query.rs` for filtering and pagination. The response shape (`PaginatedResults<AdvisorySummary>`) from `common/src/model/paginated.rs` does not change -- the status field in the JSON response remains a string.

All handlers should continue to return `Result<T, AppError>` with `.context()` wrapping per the error handling pattern in `common/src/error.rs`.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper (no changes needed, but verify compatibility)
- `common/src/error.rs` -- `AppError` enum for error handling pattern

## Acceptance Criteria
- [ ] All advisory queries use `advisory.status` enum column directly (no `advisory_status` join)
- [ ] `GET /api/v2/advisory` list endpoint returns advisories with correct status values
- [ ] `GET /api/v2/advisory/{id}` detail endpoint returns advisory with correct status value
- [ ] Status filtering on the list endpoint works correctly with enum values
- [ ] Response shape is unchanged (status remains a string in JSON output)
- [ ] No compile errors across the fundamental module

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status strings
- [ ] Verify advisory detail endpoint returns correct status string
- [ ] Verify status filter parameter correctly filters by enum value
- [ ] Verify pagination continues to work with the updated queries

## Verification Commands
- `cargo check -p trustify-fundamental` -- fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Entity definitions update (service layer depends on updated entity structs)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 2.0.0"}]}

[sdlc-workflow] Description digest: sha256-md:08b2f5d23f76209a122eea0d844eb86e65adbea0714c721c5f49d36795ee42d6
