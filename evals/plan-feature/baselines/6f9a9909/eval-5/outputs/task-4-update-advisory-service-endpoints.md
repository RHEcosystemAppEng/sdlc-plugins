# Task 4 — Update advisory service and endpoints for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoint handlers to query the `advisory.status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies status filtering. The response shape remains unchanged (status is still a string in API responses).

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` join from all query methods (fetch, list, search); filter by `advisory.status` enum column directly; update any status-related query builder logic
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to populate `status` field from the enum column instead of the join result
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly if it includes status
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to compare against enum values instead of joined table values
- `modules/fundamental/src/advisory/endpoints/get.rs` — update single-advisory fetch to use enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update module-level imports if needed for the new enum type

## Implementation Notes
- In `advisory.rs` service: remove all `.join()` or `.find_also_related()` calls that reference the `advisory_status` entity. Replace with direct column access on `advisory::Column::Status`.
- For status filtering in list queries, use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` pattern instead of joining and filtering on the lookup table.
- The `AdvisorySummary` and `AdvisoryDetails` structs should map the enum value to a string for API response serialization. SeaORM's `DeriveActiveEnum` with `string_value` attributes handles this — the enum serializes to its string representation automatically.
- Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's handler file scope.
- Per CONVENTIONS.md §Response types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's service query scope.
- Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module directory scope.

### Constraints (from docs/constraints.md)
- §2.1: Every commit MUST reference Jira issue ID in the footer
- §2.2: Commit messages MUST follow Conventional Commits (`refactor(advisory): ...`)
- §2.3: Every commit MUST include `--trailer="Assisted-by: Claude Code"`
- §5.1: Changes MUST be scoped to the files listed in Files to Modify
- §5.3: Implementation MUST follow the patterns referenced in Implementation Notes
- §5.4: Code MUST NOT duplicate existing functionality

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; use these for the updated advisory list query
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; already used by advisory list endpoint
- `common/src/error.rs` — `AppError` enum for error handling; already used in advisory handlers
- `modules/fundamental/src/sbom/service/sbom.rs` — example service implementation showing the project's query-building pattern without unnecessary joins

## Acceptance Criteria
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) returns results without joining `advisory_status` table
- [ ] Advisory detail endpoint (`GET /api/v2/advisory/{id}`) returns results without joining `advisory_status` table
- [ ] Status filtering works correctly using the enum column (e.g., `?status=Fixed` returns only fixed advisories)
- [ ] API response shape is unchanged — `status` field is still a string value
- [ ] No references to `advisory_status` entity remain in the advisory service or endpoint modules
- [ ] Advisory list endpoint p95 latency is reduced (join overhead eliminated)

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values as strings
- [ ] Verify status filter parameter correctly filters by enum value
- [ ] Verify advisory detail endpoint returns correct status for a single advisory
- [ ] Verify error handling returns appropriate `AppError` responses for invalid status filter values

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status
