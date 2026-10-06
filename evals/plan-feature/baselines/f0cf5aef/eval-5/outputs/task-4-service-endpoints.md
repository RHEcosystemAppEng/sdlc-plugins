## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, endpoints, and search service to use the new `status` enum column instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing advisory list endpoint p95 latency by approximately 40ms. The response shape remains identical — status is still returned as a string to callers.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from `fetch`, `list`, and `search` methods; query the `status` column directly on the `advisory` table; update any `select_also` or `find_also_related` calls that join `advisory_status`
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source the `status` field from the enum column instead of a joined relation; remove any `From<(advisory::Model, advisory_status::Model)>` conversion implementations
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to summary; remove joined model references
- `modules/fundamental/src/advisory/model/mod.rs` — remove `use` or `mod` imports related to `advisory_status` entity
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filtering in the list endpoint to use `WHERE advisory.status = <enum_value>` instead of a join-based filter; update any filter parameter parsing to construct enum comparisons
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get endpoint to read status from the enum column; remove any join logic for status display
- `common/src/db/query.rs` — update shared query builder helpers if advisory status filtering logic exists here (e.g., a status filter that constructs a join condition)
- `modules/search/src/service/mod.rs` — update search indexing if advisory status is indexed for full-text search; change from join-based status extraction to direct enum column read

## Implementation Notes
- In `advisory.rs` service: replace patterns like `Advisory::find().find_also_related(AdvisoryStatus)` with `Advisory::find()` and access `model.status` directly as an `AdvisoryStatusEnum` value.
- For status filtering in endpoints: convert the filter parameter string (e.g., `"Fixed"`) to `AdvisoryStatusEnum::Fixed` and use `.filter(advisory::Column::Status.eq(status_enum_value))`.
- The `AdvisorySummary` and `AdvisoryDetails` structs likely construct from a tuple of `(advisory::Model, Option<advisory_status::Model>)` — change this to construct from `advisory::Model` directly, using `model.status.to_string()` or similar for the string representation.
- Per CONVENTIONS.md §Error handling: maintain `Result<T, AppError>` with `.context()` wrapping for all updated handler functions.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust file scope.
- Per CONVENTIONS.md §Module pattern: the advisory module follows `model/ + service/ + endpoints/` structure — maintain this organization.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust file scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` — ensure the response wrapper is preserved.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust file scope.
- Per CONVENTIONS.md §Query helpers: shared filtering, pagination, and sorting use `common/src/db/query.rs` — check if status filtering is implemented there.
  Applies: task modifies `common/src/db/query.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs` — existing advisory service methods show the established query patterns to update
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service methods that query without joins (SBOM queries may show the pattern for direct column access)
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination patterns
- `modules/fundamental/src/sbom/model/summary.rs` — reference for model struct construction without join tuples

## Acceptance Criteria
- [ ] Advisory service `fetch` method queries `status` column directly without joining `advisory_status`
- [ ] Advisory service `list` method supports status filtering via enum column comparison
- [ ] Advisory service `search` method uses direct status column access
- [ ] `AdvisorySummary` struct includes status as a string derived from the enum column
- [ ] `AdvisoryDetails` struct includes status as a string derived from the enum column
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) supports `?status=Fixed` filtering via enum column
- [ ] Advisory get endpoint (`GET /api/v2/advisory/{id}`) returns status from enum column
- [ ] No references to `advisory_status` entity or table remain in the fundamental module
- [ ] No references to `advisory_status` entity remain in the search module
- [ ] Response shape is unchanged — API consumers see no difference in the status field format
- [ ] `cargo check -p fundamental -p search` compiles without errors

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values from enum column
- [ ] Verify advisory list endpoint status filtering works with each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Verify advisory get endpoint returns correct status string
- [ ] Verify no join-related SQL is generated for advisory queries (check query logs or generated SQL)

## Verification Commands
- `cargo check -p fundamental -p search` — compiles without errors
- `grep -r "advisory_status" modules/ common/` — returns no matches
- `cargo test -p fundamental` — all existing tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
