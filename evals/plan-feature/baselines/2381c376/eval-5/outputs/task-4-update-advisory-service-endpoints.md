## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and all advisory endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from every advisory query, which is the primary performance goal of the feature (reducing advisory list endpoint p95 latency by ~40ms). All queries in `AdvisoryService`, all model structs (`AdvisorySummary`, `AdvisoryDetails`), and all endpoint handlers (list, get) must be updated. Integration tests must be updated to verify the new query structure.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- Update `AdvisorySummary` struct to use `AdvisoryStatusEnum` instead of a joined status string
- `modules/fundamental/src/advisory/model/details.rs` -- Update `AdvisoryDetails` struct to use `AdvisoryStatusEnum` instead of a joined status string
- `modules/fundamental/src/advisory/model/mod.rs` -- Update module re-exports if status-related types changed
- `modules/fundamental/src/advisory/service/advisory.rs` -- Remove all `advisory_status` table joins from `fetch`, `list`, and `search` queries; query the `status` column directly
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Update status filtering to use `WHERE status = <enum_value>` instead of joining the lookup table
- `modules/fundamental/src/advisory/endpoints/get.rs` -- Update to read status from the direct enum field
- `tests/api/advisory.rs` -- Update integration tests to reflect new query structure and enum-based status filtering

## Implementation Notes
- In `AdvisoryService::list()` and `AdvisoryService::fetch()`, remove `.join(advisory_status::Entity)` calls and any `.column(advisory_status::Column::Name)` projections
- Replace status filter conditions: change `advisory_status::Column::Name.eq(status_value)` to `advisory::Column::Status.eq(AdvisoryStatusEnum::from(status_value))`
- The `AdvisorySummary` and `AdvisoryDetails` structs should derive `status` directly from the `advisory::Model` instead of a separate join result
- The external API response shape must remain identical -- status is still returned as a string. Use `serde` `rename` or `Display` trait on `AdvisoryStatusEnum` to serialize as the same string values
- Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure for the advisory module.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` for all error handling in updated service methods.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Response types: list endpoint returns `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs` for updated advisory queries.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust file scope.
- Per CONVENTIONS.md §Testing: update integration tests in `tests/api/` using the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test directory scope.
- See `modules/fundamental/src/sbom/service/sbom.rs` for a reference service implementation that queries entity fields directly without a lookup join

## Reuse Candidates
- `common/src/db/query.rs::filtering` -- shared query builder helpers for filtering, pagination, and sorting; reuse for updated advisory queries
- `common/src/model/paginated.rs::PaginatedResults` -- response wrapper for list endpoints; already in use, ensure continued usage
- `common/src/error.rs::AppError` -- error type for all service/endpoint returns; ensure .context() wrapping on updated queries
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference for service query patterns without lookup joins

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` (fetch, list, search) no longer join the `advisory_status` table
- [ ] `AdvisorySummary` and `AdvisoryDetails` read status from the direct `advisory.status` enum column
- [ ] Advisory list endpoint supports filtering by status using the enum column (`WHERE status = 'Fixed'`)
- [ ] Advisory get endpoint returns the status from the enum column
- [ ] External API response shape is unchanged -- status field still serializes as a string
- [ ] All existing integration tests pass with the updated query structure
- [ ] No references to `advisory_status` entity remain in the fundamental module

## Test Requirements
- [ ] Update `tests/api/advisory.rs` to test status filtering with enum values (New, Analyzing, Fixed, Rejected)
- [ ] Verify advisory list endpoint returns correct results when filtering by each status value
- [ ] Verify advisory get endpoint returns the correct status string for an advisory
- [ ] Verify that the response JSON shape is identical to the pre-migration format (status is a string, not an enum object)
- [ ] Add a test that creates an advisory with a specific status and verifies it round-trips correctly through the API

## Verification Commands
- `cargo test -p fundamental -- advisory` -- advisory module unit tests pass
- `cargo test --test advisory` -- advisory integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for new schema
