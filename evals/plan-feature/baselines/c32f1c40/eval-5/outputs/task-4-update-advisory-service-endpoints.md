## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and HTTP endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove all `advisory_status` table joins from fetch, list, and search queries; select `advisory.status` enum column directly; update any status-based filtering to use `WHERE advisory.status = <enum_value>` instead of joining
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to derive `status` from the enum column field instead of a joined relation
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to derive `status` from the enum column field instead of a joined relation
- `modules/fundamental/src/advisory/model/mod.rs` -- update any re-exports or type references if the status type changed
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update list handler to filter by enum value directly; remove any query parameters that reference the status_id
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update get handler to return status from enum field
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- verify route registration does not reference advisory_status; update if needed
- `modules/search/src/service/mod.rs` -- check for advisory status references in full-text search indexing/queries and update to use the enum column if present

## Implementation Notes
- Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. Maintain this pattern in updated query code.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Module pattern: maintain the `model/ + service/ + endpoints/` structure. Do not merge service logic into endpoint handlers.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module directory pattern scope.
- Per CONVENTIONS.md §Response types: list endpoints must continue to return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's list endpoint scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting utilities from `common/src/db/query.rs` for the updated advisory queries.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's service layer scope.
- Per CONVENTIONS.md §Endpoint registration: verify `modules/fundamental/src/advisory/endpoints/mod.rs` route registration remains correct after removing status-related query parameter handling.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` scope.
- The status filter on the list endpoint should use SeaORM's `ColumnTrait::eq()` with the `AdvisoryStatusEnum` value instead of a subquery or join
- Remove all `use` statements referencing the `advisory_status` entity from service and endpoint files
- The API response shape must remain identical -- status is still returned as a string. The SeaORM `DeriveActiveEnum` serialization handles this automatically

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; reuse these for the updated advisory queries instead of writing custom query logic
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper already used by advisory list endpoint
- `common/src/error.rs` -- `AppError` enum for error handling pattern
- `modules/fundamental/src/sbom/service/sbom.rs` -- `SbomService` as a reference for service query patterns that do not use lookup table joins

## Acceptance Criteria
- [ ] `AdvisoryService::list` no longer joins the `advisory_status` table
- [ ] `AdvisoryService::fetch` no longer joins the `advisory_status` table
- [ ] Advisory list endpoint supports filtering by status using the enum value directly
- [ ] Advisory get endpoint returns status as a string from the enum column
- [ ] API response shape for advisory list and get endpoints is unchanged (status field is still a string)
- [ ] No references to `advisory_status` entity remain in the advisory service or endpoint modules
- [ ] Search service is updated if it references advisory status
- [ ] `cargo check -p fundamental` compiles without errors

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values from the enum column
- [ ] Verify advisory list endpoint filters by status correctly (e.g., `?status=Fixed`)
- [ ] Verify advisory get endpoint returns the correct status string
- [ ] Verify the API response JSON shape is unchanged (backward compatible)

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles without errors
- `cargo check -p search` -- search module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
