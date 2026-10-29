## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms. The public API response shape remains unchanged -- status continues to be returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove the `advisory_status` table join from `fetch`, `list`, and `search` query methods; select `status` column directly from the `advisory` table
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source the `status` field from the enum column instead of the joined table field
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to source the `status` field from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` -- update any shared model imports or type aliases for the status field
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter logic to use `WHERE advisory.status = <enum_value>` instead of joining advisory_status
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update advisory detail query to use enum column
- `tests/api/advisory.rs` -- update integration tests to validate enum-based status filtering and correct response shape

## Implementation Notes
- The advisory list endpoint currently joins `advisory_status` for filtering and display. Replace all `advisory_status` join paths with direct column access on `advisory.status`
- For status filtering in the list endpoint, use SeaORM's enum comparison: `Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of `advisory_status::Column::Name.eq("Fixed")`
- Ensure the API response serialization converts the enum to its string representation (e.g., `"Fixed"`) to maintain backward compatibility with the frontend
- Per CONVENTIONS.md §Module Pattern: maintain the model/ + service/ + endpoints/ structure for the advisory module.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error Handling: all endpoint handlers must return `Result<T, AppError>` with `.context()` wrapping on fallible operations.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint handler scope.
- Per CONVENTIONS.md §Response Types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's list endpoint scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting utilities from `common/src/db/query.rs` for the updated status filter.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's query builder scope.
- Per CONVENTIONS.md §Testing: integration tests must hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers (filtering, pagination, sorting) to use for the updated status filter
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper used by list endpoints
- `common/src/error.rs` -- `AppError` enum for error handling in endpoint handlers
- `modules/fundamental/src/sbom/service/sbom.rs` -- existing service demonstrating the query pattern without lookup table joins (reference for the target pattern)

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` (fetch, list, search) no longer join the `advisory_status` table
- [ ] Advisory list endpoint filters by `advisory.status` enum column directly
- [ ] Advisory list endpoint returns paginated results with status as a string (unchanged API response shape)
- [ ] Advisory get endpoint returns advisory details with status from the enum column
- [ ] Status filter on advisory list endpoint correctly filters by each enum value (New, Analyzing, Fixed, Rejected)
- [ ] No references to `advisory_status` table remain in the advisory module code
- [ ] Integration tests pass with the new enum-based queries

## Test Requirements
- [ ] Integration test: `GET /api/v2/advisory` returns advisories with correct status strings
- [ ] Integration test: `GET /api/v2/advisory?status=Fixed` filters correctly using the enum column
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns advisory details with correct status
- [ ] Integration test: verify each status enum value (New, Analyzing, Fixed, Rejected) can be used as a filter
- [ ] Integration test: verify the response shape is identical to the pre-migration format (backward compatibility)

## Verification Commands
- `cargo test -p fundamental -- advisory` -- advisory module unit tests pass
- `cargo test --test advisory` -- advisory integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
