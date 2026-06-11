# Repository Impact Map — TC-9005

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migrations** — The migration creates the `advisory_status_enum` type, adds the `status` column, backfills from the join, drops the `status_id` FK column, and drops the `advisory_status` table. The service layer and endpoints must be updated in lockstep: merging the migration alone would drop the table that existing code still joins, and merging the code changes alone would reference a column that does not yet exist.
2. **Breaking API changes** — All advisory queries currently join `advisory_status`. After the migration drops the table, any code still referencing `status_id` or the join would fail. Conversely, code referencing the new `status` enum column would fail without the migration.
3. **Non-functional requirement explicitly states:** "All changes must land together" — confirming the atomicity constraint.

**Interdependent tasks:** The migration task, entity update task, service/endpoint update task, and test update task are all mutually dependent. Partial delivery of any subset breaks the application.

**Label decision:** Add `workflow:feature-branch` label to the TC-9005 feature issue.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected)
    - Add `status` enum column to `advisory` table and backfill from `status_id` join
    - Drop `status_id` foreign key column from `advisory` table
    - Drop `advisory_status` lookup table
    - Update SeaORM entity `entity/advisory.rs` to replace `status_id` FK with `status` enum column
    - Remove SeaORM entity `entity/advisory_status.rs` (no longer needed — table dropped)
    - Update `AdvisorySummary` and `AdvisoryDetails` models to use enum status directly
    - Update `AdvisoryService` queries to filter/sort by enum column instead of joining `advisory_status`
    - Update advisory list and get endpoints to use new status field
    - Update advisory ingestion pipeline to write enum values directly instead of lookup table insert
    - Update advisory integration tests for new schema (no join, enum filtering)
```
