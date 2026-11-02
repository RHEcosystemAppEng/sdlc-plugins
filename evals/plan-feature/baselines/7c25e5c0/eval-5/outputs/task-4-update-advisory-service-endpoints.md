## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing p95 latency by ~40ms on the advisory list endpoint.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — update `AdvisoryService` methods (`fetch`, `list`, `search`) to query `advisory.status` directly instead of joining `advisory_status` table; remove `advisory_status` join clauses; update status filter predicates to compare against `AdvisoryStatusEnum` values
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the list endpoint handler to use the enum column for status filtering; remove any `advisory_status` join in the query builder
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get endpoint handler to read status from the enum column; remove `advisory_status` join
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to populate `status` field from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to populate `status` field from the enum column

## Implementation Notes
- In `advisory.rs` (service), replace `advisory_status::Entity::find()` joins with direct column access: `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` for filtering
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for query construction using `common/src/db/query.rs` helpers
- The `AdvisorySummary` and `AdvisoryDetails` structs should continue to expose `status` as a `String` in the API response (serialize the enum to string) — no user-facing API change
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping for error propagation.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's service query scope.

## Acceptance Criteria
- [ ] `AdvisoryService::list` queries `advisory.status` directly without joining `advisory_status`
- [ ] `AdvisoryService::fetch` reads status from the enum column
- [ ] `AdvisoryService::search` supports status filtering via enum comparison
- [ ] List endpoint returns advisory status as a string in the response (unchanged API shape)
- [ ] Get endpoint returns advisory status from the enum column
- [ ] No references to `advisory_status` table or entity remain in the advisory module

## Test Requirements
- [ ] Advisory list with status filter returns correct results using enum column
- [ ] Advisory detail endpoint returns correct status string
- [ ] Status filtering works for all four enum values (New, Analyzing, Fixed, Rejected)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update entity definitions (service layer uses updated entity types)
