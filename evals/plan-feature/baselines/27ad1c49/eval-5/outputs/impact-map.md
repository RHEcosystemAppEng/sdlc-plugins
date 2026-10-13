# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Feature Summary

Replace the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table, eliminating unnecessary join overhead on advisory queries and simplifying the schema.

## Repositories Impacted

### trustify-backend

#### Changes Needed

1. **Database migration** — Create a new migration that defines the `advisory_status_enum` PostgreSQL enum type, adds a `status` enum column to the `advisory` table, backfills from the existing `status_id` foreign key join, drops the `status_id` column, and drops the `advisory_status` table. Migration must be atomic and reversible.

2. **SeaORM entity definitions** — Update `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` enum field mapped to `advisory_status_enum`. Remove `entity/src/advisory_status.rs` entity. Update `entity/src/lib.rs` to remove the `advisory_status` module registration.

3. **Advisory service and endpoints** — Update `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly instead of joining the `advisory_status` table. Update `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` to use the new field. Update `modules/fundamental/src/advisory/model/summary.rs` and `modules/fundamental/src/advisory/model/details.rs` to source status from the enum column.

4. **Advisory ingestion pipeline** — Update `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly to the `status` column instead of inserting into the lookup table and referencing via foreign key.

#### Workflow Mode Decision

**Mode: feature-branch**

Rationale: The feature has explicit atomicity constraints. The non-functional requirements state that "all changes must land together" because merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist. A partial merge would leave the database in an inconsistent state. Feature-branch mode ensures all tasks are developed on a single branch and merged atomically.

#### Label Decision

**Add label: `workflow:feature-branch`** to the Jira feature issue TC-9005. This label signals that all child tasks target the feature branch (TC-9005) rather than main, and that a merge-branch bookend task will deliver all changes to main atomically.

## Inherited Field Values

The following field values from TC-9005 will be propagated to all child tasks:

| Field | Value | Propagation Rule |
|---|---|---|
| Priority | High | All child tasks inherit the parent feature's priority |
| Fix Versions | RHTPA 2.0.0 | All child tasks inherit the parent feature's fixVersions |
