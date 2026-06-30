# Task 4 — Update advisory service and endpoints to use status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead from all advisory queries, achieving the feature's goal of reducing advisory list endpoint p95 latency by ~40ms. The AdvisorySummary and AdvisoryDetails model structs must also be updated to source status from the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all joins to `advisory_status` table; query `status` column directly for filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` to source status from the entity's `status` enum field instead of a joined table field
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` to source status from the entity's `status` enum field
- `modules/fundamental/src/advisory/model/mod.rs` — update any shared model construction logic that references the advisory_status join
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter handling in GET /api/v2/advisory to filter by enum column
- `modules/fundamental/src/advisory/endpoints/get.rs` — update status retrieval in GET /api/v2/advisory/{id} to use enum column

## Implementation Notes
- In `advisory.rs` (service): remove `use entity::advisory_status` imports and any `.join()` or `.find_also_related()` calls involving the advisory_status entity. Replace with direct column access: `entity::advisory::Column::Status`
- For status filtering: use `entity::advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` pattern instead of subquery or join-based filtering
- The API response shape must remain identical — status is still returned as a string. The `AdvisoryStatusEnum` serialization via `serde::Serialize` should produce the same string values
- Follow the existing query construction patterns in `common/src/db/query.rs` for filter and pagination helpers
- Follow the existing model construction patterns in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) for reference on how models are built from entity query results
- Per docs/constraints.md section 5 (Code Change Rules): inspect all files before modifying to understand current join patterns

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse existing filter infrastructure for enum column filtering
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service layer query patterns without join tables
- `modules/fundamental/src/sbom/model/summary.rs` — reference for model struct construction from entity fields

## Acceptance Criteria
- [ ] Advisory service no longer joins the `advisory_status` table in any query
- [ ] `AdvisorySummary.status` is populated from the entity's `status` enum field
- [ ] `AdvisoryDetails.status` is populated from the entity's `status` enum field
- [ ] GET /api/v2/advisory supports status filtering using the enum column
- [ ] GET /api/v2/advisory/{id} returns status from the enum column
- [ ] API response shape is unchanged — status is still a string field with the same values
- [ ] No remaining imports or references to `advisory_status` entity in the fundamental module

## Test Requirements
- [ ] Advisory list endpoint returns correct status values from the enum column
- [ ] Advisory list endpoint status filter returns matching results
- [ ] Advisory detail endpoint returns correct status value
- [ ] API response body format is unchanged (backward compatible)

## Verification Commands
- `cargo build -p trustify-fundamental` — module compiles
- `cargo test -p trustify-fundamental` — module tests pass
- `grep -r "advisory_status" modules/fundamental/src/` — returns no results

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:d4bc76ab9c9b2b49091191a8fcd5a440b13d413b0c7dfb80e346138f5fd4857e
