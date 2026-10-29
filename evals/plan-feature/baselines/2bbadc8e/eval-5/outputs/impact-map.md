# Repository Impact Map

## Feature: TC-9005 — Drop status table and migrate to enum column

### trustify-backend

changes:
  - Create database migration to define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` foreign key column, and drop `advisory_status` lookup table
  - Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` foreign key field with `status` enum field; remove `entity/src/advisory_status.rs` if present; update `entity/src/lib.rs` to remove advisory_status module registration
  - Update advisory service layer (`modules/fundamental/src/advisory/service/advisory.rs`) to remove `advisory_status` table join from all advisory queries and use the `status` enum column directly
  - Update advisory model structs (`modules/fundamental/src/advisory/model/summary.rs`, `details.rs`) to reflect the new enum-based status field
  - Update advisory list and get endpoints (`modules/fundamental/src/advisory/endpoints/list.rs`, `get.rs`) to filter and return status from the enum column
  - Update advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to write enum values directly instead of inserting into the lookup table
  - Update advisory integration tests (`tests/api/advisory.rs`) to validate enum-based status filtering and ingestion
  - Update internal architecture documentation to reflect the schema change (removal of advisory_status table, addition of enum column)

### Excluded requirements

(none -- all requirements from the Feature description are addressable within the trustify-backend repository)

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migration** -- The database migration adds the `status` enum column and drops the `advisory_status` table. Merging the migration alone would drop the table that existing advisory queries still join, breaking all advisory endpoints. Merging the code changes alone would reference a `status` column that does not yet exist.

2. **Breaking API changes (internal)** -- The SeaORM entity definition change (removing `status_id` FK, adding `status` enum field) is consumed by the advisory service, endpoints, and ingestion pipeline. Merging the entity change without the service/endpoint changes would cause compilation failures.

3. **Tightly coupled feature components** -- The migration, entity definitions, service layer, endpoints, and ingestion pipeline form a dependency chain where no individual change can land on `main` independently without breaking the build or runtime behavior.

**Interdependent tasks:**
- Migration (Task 2) and Entity update (Task 3): entity definitions must match the schema
- Entity update (Task 3) and Service/Endpoints (Task 4): service queries reference entity fields
- Entity update (Task 3) and Ingestion (Task 5): ingestion writes entity fields
- All implementation tasks must land together before merging to `main`

The `workflow:feature-branch` label will be applied to the TC-9005 feature issue.
