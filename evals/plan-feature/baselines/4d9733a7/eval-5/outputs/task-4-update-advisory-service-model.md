## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies the query logic.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from query methods (fetch, list, search); replace with direct `advisory.status` column access; update status filtering to use enum comparison instead of FK-based join filtering
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source the `status` field from the advisory entity's enum column instead of a joined lookup value
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source the `status` field from the advisory entity's enum column instead of a joined lookup value
- `modules/fundamental/src/advisory/model/mod.rs` — update any re-exports or shared type references related to advisory status

## Implementation Notes
- In `AdvisoryService`, replace query patterns like `.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())` with direct column access on `advisory::Column::Status`.
- For status filtering in list/search queries, replace `.filter(advisory_status::Column::Name.eq(status_name))` with `.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(status_name)))`.
- The `AdvisorySummary` and `AdvisoryDetails` structs may need to change how they construct the status field — instead of reading from a joined `advisory_status` row, read directly from the advisory entity's `status` field and convert the enum to a string for the API response.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all service methods.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting utilities from `common/src/db/query.rs` for advisory list queries.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Module Pattern: maintain the `model/ + service/ + endpoints/` directory structure.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Response Types: ensure list methods continue to return `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/model/summary.rs` matching the convention's Rust model file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for advisory list queries after removing the join
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; continue using for advisory list responses
- `common/src/error.rs` — `AppError` enum for consistent error handling across service methods
- `modules/fundamental/src/sbom/service/sbom.rs` — reference implementation of a service that queries entities without joins; follow the same patterns

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` no longer join the `advisory_status` table
- [ ] Status filtering works using the enum column directly
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly populate the status field from the enum column
- [ ] The advisory list endpoint returns identical response shapes (status as a string) — no user-facing API change
- [ ] The modules/fundamental crate compiles without errors

## Test Requirements
- [ ] Verify advisory list query returns correct status values from the enum column
- [ ] Verify advisory status filtering works with each enum variant (New, Analyzing, Fixed, Rejected)
- [ ] Verify that the API response shape for advisory list and detail endpoints remains unchanged

## Verification Commands
- `cargo check -p trustify-fundamental` — verify the fundamental module compiles
- `cargo test -p trustify-fundamental` — run existing unit tests to verify no regressions

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
