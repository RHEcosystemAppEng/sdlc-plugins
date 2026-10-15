# Repository Impact Map -- TC-9005: Drop status table and migrate to enum column

## trustify-backend

changes:
  - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) and add `status` enum column to `advisory` table with data backfill from existing `status_id` join
  - Update SeaORM entity definitions: add `status` enum field to `entity/advisory.rs`, remove `status_id` foreign key field, remove `entity/advisory_status.rs` entity module
  - Update advisory service layer (`AdvisoryService`) to query the `status` enum column directly instead of joining the `advisory_status` table
  - Update advisory list and get endpoints to filter and return status from the enum column without a join
  - Update advisory ingestion pipeline to write `advisory_status_enum` values directly to the `status` column instead of inserting into the lookup table
  - Create migration to drop `status_id` foreign key column from `advisory` table and drop `advisory_status` lookup table
  - Update integration tests in `tests/api/advisory.rs` to reflect new query structure and enum-based filtering

## Excluded Requirements

None -- all requirements from the Feature description are addressable within the trustify-backend repository.

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators were identified:

1. **Coordinated schema migrations** -- The migration that creates the `advisory_status_enum` type and adds the `status` column must land together with the code changes that consume it. A second migration that drops `status_id` and the `advisory_status` table can only run after all code references are updated. These migrations and code changes form an atomic unit.
2. **Breaking cross-task dependencies** (explicit in non-functional requirements) -- "merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist." This is the textbook definition of an all-or-nothing delivery constraint.

**Interdependent tasks:**
- The enum creation migration (Task 2) must exist before entity definitions (Task 3) and service updates (Task 4) can compile against the new schema
- The service/endpoint updates (Task 4) and ingestion updates (Task 5) must be complete before the drop migration (Task 6) can safely execute
- No individual task can be merged to `main` independently without breaking the build or the database schema

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

## Additional Fields for Created Issues

All created tasks will include:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- **Priority**: "High" -- inherited from Feature TC-9005 (priority is set and not "Undefined", so propagated to all tasks)
- **fixVersions**: ["RHTPA 2.0.0"] -- inherited from Feature TC-9005; no `fixVersion scope` configured in Jira Field Defaults, defaulting to "both" (propagate to tasks)
