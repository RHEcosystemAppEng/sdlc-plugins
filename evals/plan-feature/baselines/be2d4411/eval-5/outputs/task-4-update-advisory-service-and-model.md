## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query, reducing advisory list endpoint p95 latency by approximately 40ms. Update `AdvisorySummary` and `AdvisoryDetails` structs to populate the status field from the enum column, and update all query logic in `AdvisoryService` to select and filter status directly.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to populate `status` from enum column instead of joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to populate `status` from enum column instead of joined table
- `modules/fundamental/src/advisory/model/mod.rs` — update model module if it contains shared status type aliases or conversion logic
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table joins from all query methods (fetch, list, search); select `status` directly from `advisory` table

## Implementation Notes
- In `AdvisoryService` (`service/advisory.rs`), locate all query builder calls that join `advisory_status` (e.g., `.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())`). Remove these joins and replace status field selection with direct access to `advisory::Column::Status`.
- In `AdvisorySummary` and `AdvisoryDetails`, update the `From` or constructor logic that previously extracted status from joined rows. The status is now a field directly on the `advisory::Model`, so conversion is simpler — e.g., `summary.status = model.status.to_string()` or use the enum directly.
- For status filtering in list/search queries, replace `.filter(advisory_status::Column::Name.eq(status_filter))` with `.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(status_filter)))`.
- All query methods must return `Result<T, AppError>` per the repository's error handling convention, using `.context()` for error wrapping.
- List endpoints that return `PaginatedResults<AdvisorySummary>` must continue to work with the updated summary struct.
- Per repo Key Conventions: error handling uses `Result<T, AppError>` with `.context()` wrapping; list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`; query helpers use `common/src/db/query.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting that should continue to be used
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by list methods
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` as a reference for service query patterns without complex joins

## Acceptance Criteria
- [ ] All `advisory_status` table joins are removed from `AdvisoryService` query methods
- [ ] `AdvisorySummary` and `AdvisoryDetails` populate status from the enum column
- [ ] Status filtering uses the enum column directly (no join)
- [ ] All advisory service methods compile and return correct types
- [ ] Query performance improvement is achievable (join eliminated)

## Test Requirements
- [ ] Verify advisory list query returns correct status values from enum column
- [ ] Verify advisory detail query returns correct status from enum column
- [ ] Verify status filtering works with enum values (New, Analyzing, Fixed, Rejected)
- [ ] Verify error handling is maintained (AppError wrapping with .context())

## Verification Commands
- `cargo build -p trustify-fundamental` — verify the fundamental module compiles
- `cargo test -p trustify-fundamental -- advisory` — run advisory-related unit tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

## Labels
- ai-generated-jira

## additional_fields
- priority: High
- fixVersions: RHTPA 2.0.0

[sdlc-workflow] Description digest: sha256-md:44df62692dcb31284b7bf05e2bcd0447a1b9b83fba702fe830e4cb3aa431815b
