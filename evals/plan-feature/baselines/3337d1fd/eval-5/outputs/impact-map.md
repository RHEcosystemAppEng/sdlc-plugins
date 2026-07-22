# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Feature Fields (Inherited)
- **Priority**: High
- **Fix Versions**: RHTPA 2.0.0

## Workflow Mode
- **Mode**: feature-branch
- **Label**: `workflow:feature-branch` to be applied to feature issue TC-9005

## Rationale for Feature-Branch Mode
The feature exhibits multiple atomicity indicators requiring all changes to land together:
1. **Coordinated schema migration**: The database migration drops the `advisory_status` table and adds an `advisory_status_enum` column. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column that does not exist.
2. **Tightly coupled components**: Entity definitions, service layer, ingestion pipeline, and integration tests all depend on the schema change. Partial delivery leaves the codebase in an inconsistent state where the ORM entities reference either a non-existent table or a non-existent column.

## Impact Map

```
trustify-backend:
  changes:
    - Create atomic database migration: create advisory_status_enum PostgreSQL enum type, add status column to advisory table, backfill from advisory_status join, drop status_id FK column, drop advisory_status table
    - Update SeaORM entity definitions: replace status_id FK in advisory.rs with status enum column, define AdvisoryStatusEnum, remove advisory_status.rs entity
    - Update advisory service and query layer: remove advisory_status table joins from all advisory queries (fetch, list, search), read status directly from enum column
    - Update advisory model structs: update AdvisorySummary and AdvisoryDetails to source status from enum column
    - Update advisory endpoints: update status filtering to use enum column directly
    - Update advisory ingestion pipeline: write enum values directly instead of inserting into lookup table
    - Update integration tests: update test data setup and assertions to use enum status values
    - Update internal architecture documentation to reflect schema change
```

## Excluded Requirements
None — all requirements from the Feature description are addressable with the available repository structure and specification detail.
