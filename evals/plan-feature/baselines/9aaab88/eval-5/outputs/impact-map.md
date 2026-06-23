# Impact Map: TC-9005 — Drop status table and migrate to enum column

## Workflow Mode Decision

**Mode**: feature-branch

**Rationale**: The feature description contains explicit atomicity constraints that mandate feature-branch workflow:

1. "Migration must be atomic: if any step fails, the entire migration rolls back — a partial migration (enum column exists but lookup table is already dropped, or vice versa) would leave the database in an inconsistent state"
2. "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist"

These atomicity indicators mean the migration, entity changes, service layer updates, endpoint updates, and ingestion pipeline changes must all land in a single merge to main. A direct-to-main workflow would risk partial delivery (e.g., migration merged but entity code still references old schema). Feature-branch mode ensures all changes are developed on branch TC-9005 and merged atomically.

**Label**: Apply `workflow:feature-branch` label to feature issue TC-9005.

## Changes

### Database Migration
- Create new migration `migration/src/m0002_advisory_status_enum/mod.rs` to:
  - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected)
  - Add `status` enum column to `advisory` table
  - Backfill `status` from existing `status_id` join
  - Drop `status_id` foreign key column
  - Drop `advisory_status` lookup table
- Update `migration/src/lib.rs` to register the new migration module

### Entity Layer
- Update `entity/src/advisory.rs` to replace `status_id: i32` foreign key with `status: AdvisoryStatusEnum` enum column
- Remove `entity/src/advisory_status.rs` (the lookup table entity is no longer needed)
- Update `entity/src/lib.rs` to remove the `advisory_status` module export

### Service Layer
- Update `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly instead of joining `advisory_status`
- Update `modules/fundamental/src/advisory/model/summary.rs` to populate status from enum column
- Update `modules/fundamental/src/advisory/model/details.rs` to populate status from enum column

### Endpoints
- Update `modules/fundamental/src/advisory/endpoints/list.rs` to filter by enum column instead of join
- Update `modules/fundamental/src/advisory/endpoints/get.rs` to read status from enum column

### Ingestion Pipeline
- Update `modules/ingestor/src/graph/advisory/mod.rs` to write enum value directly instead of inserting into lookup table

### Tests
- Update `tests/api/advisory.rs` to validate advisory status returned as string from enum column, verify status filtering works without join

## Task Summary

| Task | Title | Type |
|---|---|---|
| 1 | Create feature branch TC-9005 from main | bookend: create-branch |
| 2 | Create advisory status enum migration | intermediate |
| 3 | Update SeaORM entity definitions for enum status | intermediate |
| 4 | Update advisory service and model layer | intermediate |
| 5 | Update advisory endpoints for enum status filtering | intermediate |
| 6 | Update advisory ingestion pipeline for enum status | intermediate |
| 7 | Add integration tests for enum status migration | intermediate |
| 8 | Merge feature branch TC-9005 to main | bookend: merge-branch |
