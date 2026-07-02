# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Impacted Repositories

```
trustify-backend:
  changes:
    - Create database migration: define PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from `advisory_status` join, drop `status_id` FK column, drop `advisory_status` lookup table
    - Update SeaORM entity definitions: modify `entity/src/advisory.rs` to replace `status_id` FK with `status` enum field, remove `entity/src/advisory_status.rs` entity, update `entity/src/lib.rs` exports
    - Update advisory service and model layer: remove `advisory_status` join from all advisory queries in `modules/fundamental/src/advisory/service/advisory.rs`, update `AdvisorySummary` and `AdvisoryDetails` structs to source status from enum column
    - Update advisory ingestion pipeline: modify `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
    - Update advisory integration tests: modify `tests/api/advisory.rs` to reflect new schema (no lookup table setup, enum-based status assertions)
```

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Two atomicity indicators are present:

1. **Coordinated schema migration** — The migration drops the `advisory_status` lookup table and adds a `status` enum column to the `advisory` table. All advisory queries, entity definitions, and the ingestion pipeline must be updated to use the new column in the same deployment. The feature description explicitly states: "Migration must be atomic: if any step fails, the entire migration rolls back."

2. **Breaking API changes (internal)** — Merging the migration without the code changes would break all advisory queries (they still join the now-dropped `advisory_status` table). Merging the code changes without the migration would reference a `status` column that does not exist. The feature description states: "All changes must land together."

**Interdependent tasks:**
- The migration task (enum type creation, column addition, table drop) and the entity/service/ingestion tasks are mutually dependent — neither side functions without the other.
- All intermediate tasks must land on a feature branch and be merged to `main` atomically.

**Label decision:** Apply `workflow:feature-branch` label to TC-9005.

## Jira Field Propagation

- **Priority:** High (inherited from Feature TC-9005, propagated to all created tasks)
- **Fix Versions:** RHTPA 2.0.0 (inherited from Feature TC-9005, propagated to all created tasks)

## additional_fields

```json
{
  "labels": ["ai-generated-jira"],
  "priority": { "name": "High" },
  "fixVersions": [{ "name": "RHTPA 2.0.0" }]
}
```
