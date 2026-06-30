# Repository Impact Map

## TC-9005: Drop status table and migrate to enum column

trustify-backend:
  changes:
    - Create database migration: define `advisory_status_enum` PostgreSQL enum type, add `status` enum column to `advisory` table, backfill from `advisory_status` join, drop `status_id` FK column, drop `advisory_status` lookup table
    - Update SeaORM entity definitions: add `AdvisoryStatusEnum` Rust enum to `entity/src/advisory.rs`, remove `status_id` field, delete `entity/src/advisory_status.rs`
    - Update advisory service and endpoints: remove `advisory_status` table join from all advisory queries in `modules/fundamental/src/advisory/`, filter directly on `advisory.status` enum column
    - Update advisory ingestion pipeline: write `AdvisoryStatusEnum` values directly to `advisory.status` in `modules/ingestor/src/graph/advisory/mod.rs`, remove lookup table insert
    - Update integration tests: modify `tests/api/advisory.rs` to validate enum-based status, remove `advisory_status` table seeding

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** This feature exhibits two atomicity indicators that require all changes to land together:

1. **Coordinated schema migration** (indicator #1): The migration drops the `advisory_status` table and adds the `status` enum column. If the migration lands without the code changes, all advisory queries will fail because they still join the now-dropped `advisory_status` table. If the code changes land without the migration, they reference an `advisory.status` column that does not exist.

2. **Cross-cutting refactor** (indicator #3): The entity definition change (removing `advisory_status.rs`, adding `AdvisoryStatusEnum`) propagates to the service layer, endpoints, and ingestion pipeline. Partial delivery of any subset would leave the codebase with compile errors or runtime failures.

**Interdependent tasks:**
- Task 2 (migration) <-> Task 3 (entity definitions): entity definitions reference the enum type created by the migration
- Task 3 (entity definitions) <-> Task 4 (service/endpoints): service layer depends on the updated entity structs
- Task 3 (entity definitions) <-> Task 5 (ingestion pipeline): ingestion uses the new enum type from entity definitions
- Task 4 (service/endpoints) <-> Task 6 (integration tests): tests validate the updated endpoint behavior

The `workflow:feature-branch` label will be applied to the TC-9005 feature issue.
