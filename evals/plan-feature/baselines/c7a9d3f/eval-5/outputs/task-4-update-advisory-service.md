# Task 4 -- Update advisory service and query layer for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to query the `advisory.status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on all advisory queries. Update the model structs (`AdvisorySummary`, `AdvisoryDetails`) to carry the enum value, and update the `AdvisoryService` to use the enum column for filtering and selection.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to use `AdvisoryStatusEnum` instead of a joined status string
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to use `AdvisoryStatusEnum` instead of a joined status string
- `modules/fundamental/src/advisory/model/mod.rs` -- update any re-exports or type aliases related to status
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` join from all queries; use `advisory::Column::Status` for filtering and selection; update query builder calls to filter on the enum column directly
- `common/src/db/query.rs` -- update any advisory status filtering logic that references the lookup table join

## Implementation Notes
- In `AdvisoryService`, replace all instances of `.join(advisory_status::Entity)` or equivalent with direct column access on `advisory::Column::Status`.
- For filtering, use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining and filtering on the lookup table.
- The response shape to the frontend must remain identical -- status should still serialize as a string (e.g., "New", "Fixed"). SeaORM's `DeriveActiveEnum` with `string_value` attributes handles this automatically when the enum is serialized with serde.
- Follow the existing query patterns in `modules/fundamental/src/sbom/service/sbom.rs` for list and fetch operations as a reference for how services interact with entities.
- Use the shared query helpers in `common/src/db/query.rs` for pagination and filtering -- check if any status-specific filtering logic exists there and update it.
- The `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs` should continue to work without changes since it is generic over the item type.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` -- reference service pattern for entity queries without joins
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper (no changes needed, but verify compatibility)

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` no longer join the `advisory_status` table
- [ ] `AdvisorySummary` and `AdvisoryDetails` model structs use `AdvisoryStatusEnum` for the status field
- [ ] Advisory responses still include status as a string field (no API shape change)
- [ ] The `advisory_status` join is completely eliminated from the advisory service module
- [ ] The service layer compiles without errors

## Test Requirements
- [ ] `cargo check -p fundamental` compiles successfully
- [ ] Verify that no query in the advisory service references `advisory_status`

## Verification Commands
- `cargo check -p fundamental` -- module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
