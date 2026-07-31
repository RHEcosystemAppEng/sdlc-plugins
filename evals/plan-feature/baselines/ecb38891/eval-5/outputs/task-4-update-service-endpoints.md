## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies the status filtering logic. The advisory list endpoint's p95 latency should improve by approximately 40ms due to the eliminated join.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source status from the enum column instead of a joined relation; change the status field type from a string resolved via join to the `AdvisoryStatusEnum` (or its string representation)
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct similarly to use the enum status field
- `modules/fundamental/src/advisory/model/mod.rs` -- update module-level re-exports if status-related types changed
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove all `advisory_status` table joins from fetch, list, and search queries; replace `WHERE advisory_status.name = ?` filters with `WHERE advisory.status = ?` enum comparisons; update any `SelectModel` or `JoinType` references that involved `advisory_status`
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update the list handler to use enum-based status filtering in query parameters
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update the get handler to return status from the enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- update route registration if status filter parameter types changed
- `common/src/db/query.rs` -- update shared query helpers if advisory status filtering logic exists here

## Implementation Notes
- The response shape must remain identical to the current API -- status is still returned as a string (e.g., `"Fixed"`). Use `serde::Serialize` on `AdvisoryStatusEnum` to produce the same string values. Verify the serialized output matches the current format.
- In `AdvisoryService`, replace patterns like:
  ```rust
  .join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())
  .filter(advisory_status::Column::Name.eq(status_filter))
  ```
  with:
  ```rust
  .filter(advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(status_filter)))
  ```
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for query construction without joins
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure
- Error handling: use `Result<T, AppError>` with `.context()` wrapping per the project convention in `common/src/error.rs`
- All list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Use the shared query helpers in `common/src/db/query.rs` for filtering, pagination, and sorting

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` -- reference for query construction pattern without joins
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for list endpoint handler pattern
- `common/src/db/query.rs` -- shared filtering, pagination, and sorting helpers
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper

## Acceptance Criteria
- [ ] `AdvisoryService::list` queries `advisory.status` enum column directly without joining `advisory_status`
- [ ] `AdvisoryService::fetch` queries `advisory.status` enum column directly without joining `advisory_status`
- [ ] `AdvisorySummary` struct populates status from the enum column
- [ ] `AdvisoryDetails` struct populates status from the enum column
- [ ] Advisory list endpoint supports filtering by status using the enum column
- [ ] Advisory get endpoint returns status from the enum column
- [ ] API response shape is unchanged -- status is still returned as a string
- [ ] No references to `advisory_status` table or entity remain in the advisory module
- [ ] `cargo check -p fundamental` compiles without errors

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values as strings
- [ ] Verify advisory list endpoint with status filter returns only matching advisories
- [ ] Verify advisory get endpoint returns correct status for a specific advisory
- [ ] Verify no `advisory_status` join appears in generated SQL queries

## Verification Commands
- `cargo check -p fundamental` -- compiles without errors
- `cargo test -p fundamental` -- all existing tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions (service layer uses the updated entity types)
