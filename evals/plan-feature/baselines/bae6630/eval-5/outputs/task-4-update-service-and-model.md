## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service and model layer to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join that adds ~40ms p95 latency to advisory list queries. The `AdvisorySummary` and `AdvisoryDetails` structs must be updated to carry the enum value, and all advisory queries in `AdvisoryService` must be rewritten to filter and select on the `status` column.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — Change the status field from a joined string to `AdvisoryStatusEnum` from the entity crate
- `modules/fundamental/src/advisory/model/details.rs` — Change the status field from a joined string to `AdvisoryStatusEnum`
- `modules/fundamental/src/advisory/model/mod.rs` — Update re-exports if needed for the enum type
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove the `advisory_status` join from `fetch`, `list`, and `search` queries; use `advisory::Column::Status` directly for filtering and selection

## Implementation Notes
In `modules/fundamental/src/advisory/service/advisory.rs`, the existing queries join `advisory_status` via `status_id` to retrieve the human-readable status string. Replace these joins with direct column access:

- For list queries: remove `.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())` and select `advisory::Column::Status` directly.
- For filter queries: replace `advisory_status::Column::Name.eq(filter_value)` with `advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(filter_value))`.

In `modules/fundamental/src/advisory/model/summary.rs`, the `AdvisorySummary` struct currently has a `status: String` field populated from the join. Change it to `status: AdvisoryStatusEnum` and derive `Serialize` on the enum so it serializes to the same string values (New, Analyzing, Fixed, Rejected) preserving API compatibility.

Follow the query builder patterns in `common/src/db/query.rs` for filtering and the response wrapper pattern in `common/src/model/paginated.rs` for list responses.

## Acceptance Criteria
- [ ] `AdvisorySummary.status` field is `AdvisoryStatusEnum` type
- [ ] `AdvisoryDetails.status` field is `AdvisoryStatusEnum` type
- [ ] `AdvisoryService` queries no longer join `advisory_status` table
- [ ] Status filtering on the advisory list query uses `advisory::Column::Status` directly
- [ ] API response JSON for status field remains unchanged (same string values: New, Analyzing, Fixed, Rejected)
- [ ] Module compiles with `cargo check -p fundamental`

## Test Requirements
- [ ] Advisory service list query returns correct status values without the join
- [ ] Advisory service filter by status returns correct filtered results
- [ ] Status field serializes to the same string values as before (API compatibility)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

## Digest
[sdlc-workflow] Description digest: sha256-md:7ef2c4f4cf16a85e7972e43d1516dfcbbdd1bd3bbc97a9c5a9846171dfbb5030
