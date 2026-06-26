## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to use the new `status` enum column instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, which is the primary performance goal of the feature. The AdvisorySummary and AdvisoryDetails structs must expose the status as a string (matching the existing API response shape) derived directly from the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove all joins to `advisory_status` table from fetch, list, and search queries; filter by `advisory.status` enum column directly instead of joining on `status_id`
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source the status field from the enum column instead of a joined table field
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to source the status field from the enum column instead of a joined table field
- `modules/fundamental/src/advisory/model/mod.rs` -- update any shared model type imports or re-exports if they reference the advisory_status entity
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against enum values instead of joined table values
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update single advisory fetch if it joins advisory_status

## Implementation Notes
- In `advisory.rs` (service), remove all `.join()` or `.find_also_related()` calls that reference the `advisory_status` entity. Replace status filtering logic: instead of filtering on a joined column (`advisory_status::Column::Name`), filter directly on `advisory::Column::Status` using the `AdvisoryStatusEnum` value.
- Use the query builder helpers from `common/src/db/query.rs` for filtering and pagination -- these are the existing shared utilities for query construction.
- In `summary.rs` and `details.rs`, the status field should be derived from `advisory::Model::status` (the enum field) rather than from a joined `advisory_status::Model`. The API response format stays the same (status as a string), so use `.to_string()` or `Into<String>` on the enum value.
- In `list.rs`, if there is a status filter query parameter, it should parse the filter value into an `AdvisoryStatusEnum` variant and apply `advisory::Column::Status.eq(variant)`.
- The list endpoint returns `PaginatedResults<AdvisorySummary>` via the wrapper from `common/src/model/paginated.rs` -- this pattern does not change.
- All handlers return `Result<T, AppError>` with `.context()` wrapping per the error handling convention in `common/src/error.rs`.
- Per CONVENTIONS.md §Error Handling (inferred from Key Conventions): use `Result<T, AppError>` with `.context()` wrapping for all service and handler functions. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` service file scope.
- Per CONVENTIONS.md §Module Pattern (inferred from Key Conventions): follow the model/ + service/ + endpoints/ structure. Applies: task modifies files across `modules/fundamental/src/advisory/{model,service,endpoints}/` matching the convention's module structure scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` -- shared filtering, pagination, and sorting utilities already used by advisory queries; continue using these for the updated enum-based filters
- `common/src/model/paginated.rs::PaginatedResults<T>` -- response wrapper for list endpoints; no changes needed, just continue using
- `common/src/error.rs::AppError` -- error type for all handlers; continue using with `.context()`

## Acceptance Criteria
- [ ] No advisory query joins the `advisory_status` table
- [ ] Advisory list endpoint filters by enum column directly
- [ ] Advisory list and get endpoints return the same response shape as before (status as string)
- [ ] All advisory queries use `advisory::Column::Status` instead of `advisory_status::Column::Name`
- [ ] The `modules/fundamental` crate compiles without errors

## Test Requirements
- [ ] Advisory list endpoint returns correct results when filtering by status
- [ ] Advisory get endpoint returns the status field as a string in the response
- [ ] Verify the advisory_status entity is not imported anywhere in the advisory module

## Verification Commands
- `cargo check -p trustify-fundamental` -- fundamental module compiles without errors
- `cargo test -p trustify-fundamental` -- existing tests pass with updated queries

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:dc7284dca1107719da8b09c472cd098f550264c637c863b70fff7dfe2bb48bb0
