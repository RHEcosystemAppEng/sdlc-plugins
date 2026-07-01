# Repository Impact Map — TC-9005

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migration** — The migration adds the `advisory_status_enum` type and `status` column, backfills data, drops the `status_id` FK column, and drops the `advisory_status` table. The code changes (entity definitions, service layer, endpoints, ingestor) depend on the new column existing and the old table being gone. Merging the migration without the code changes breaks all advisory queries (they still join the now-dropped table). Merging the code changes without the migration references a column that does not exist.

2. **Breaking API changes (internal)** — The SeaORM entity change removes the `advisory_status` entity and changes the `advisory` entity's status field from a relation to an enum column. All service-layer and endpoint code that currently joins `advisory_status` would break if only partially updated.

**Interdependent tasks:** All intermediate tasks (migration, entity update, service/query update, ingestion pipeline update, endpoint/test update) are mutually dependent and must land together on the feature branch before merging to main.

**Label decision:** Apply `workflow:feature-branch` label to feature issue TC-9005.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected)
    - Add `status` enum column to `advisory` table, backfill from `status_id` join
    - Drop `status_id` foreign key column from `advisory` table
    - Drop `advisory_status` lookup table
    - Update SeaORM entity `entity/advisory.rs` to replace `status_id` relation with `status` enum field
    - Remove SeaORM entity file for `advisory_status` (currently implied by the lookup table)
    - Update `AdvisorySummary` and `AdvisoryDetails` model structs to use enum status directly
    - Update `AdvisoryService` query logic to remove `advisory_status` join and filter on enum column
    - Update advisory list and get endpoint handlers to use new status field
    - Update advisory ingestion pipeline to write enum status values directly instead of lookup table inserts
    - Update advisory integration tests to reflect new schema (no join, enum filtering)
```
