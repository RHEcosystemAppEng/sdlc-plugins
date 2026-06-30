# Repository Impact Map — TC-9005

## Feature

**TC-9005**: Drop status table and migrate to enum column

## Workflow Mode

**feature-branch**

### Rationale

The following atomicity indicators require all changes to land together:

1. **Coordinated schema migrations** — The migration creates the `advisory_status_enum` PostgreSQL type, adds the `status` enum column, backfills it from `status_id`, drops the `status_id` FK column, and drops the `advisory_status` lookup table. The code changes (entity definitions, service layer, endpoints, ingestion pipeline) depend on this schema change being present. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column (`status`) that does not exist.

2. **Breaking API changes** — The entity, service, and endpoint code must switch from a join-based status lookup to a direct enum column read. These changes are tightly coupled to the schema migration and cannot function independently.

**Decision**: `feature-branch` mode. The `workflow:feature-branch` label will be applied to the feature issue.

### Interdependent tasks

- The database migration task creates the enum type/column and drops the old table — all subsequent tasks depend on this schema.
- The entity update task removes the `advisory_status` entity and modifies the `advisory` entity — the service and endpoint tasks depend on these updated entities.
- The service/endpoint tasks and the ingestion pipeline task all depend on both the migration and entity changes.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create database migration to add advisory_status_enum type, add status enum column to advisory table, backfill from status_id join, drop status_id FK column, and drop advisory_status lookup table
    - Update SeaORM entity definition for advisory (entity/src/advisory.rs) to replace status_id FK with status enum column
    - Remove SeaORM entity definition for advisory_status (entity/src/advisory_status.rs) and deregister from entity/src/lib.rs
    - Update AdvisoryService (modules/fundamental/src/advisory/service/advisory.rs) to query status directly instead of joining advisory_status table
    - Update AdvisorySummary and AdvisoryDetails models (modules/fundamental/src/advisory/model/) to source status from the enum column
    - Update advisory list and get endpoints (modules/fundamental/src/advisory/endpoints/) to remove status join from query construction
    - Update advisory ingestion pipeline (modules/ingestor/src/graph/advisory/mod.rs) to write enum values directly instead of lookup table inserts
    - Update advisory integration tests (tests/api/advisory.rs) to reflect new schema and removed join
```

## Priority and Fix Version Propagation

- **Priority**: High — will be propagated to all created tasks
- **Fix Versions**: RHTPA 2.0.0 — will be propagated to all created tasks (fixVersion scope defaults to "both" since no Jira Field Defaults section is configured)
