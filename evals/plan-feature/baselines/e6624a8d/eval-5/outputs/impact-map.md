# Repository Impact Map

## Feature: TC-9005 — Drop status table and migrate to enum column

### Workflow Mode: feature-branch

**Rationale:** The feature description explicitly states three atomicity constraints:
1. **Coordinated schema migration** — The migration creates an enum type, adds a column, backfills data, drops the FK column, and drops the lookup table. A partial migration (enum column exists but lookup table already dropped, or vice versa) would leave the database in an inconsistent state.
2. **Breaking API changes** — Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column that does not exist.
3. **Cross-cutting refactor** — Entity definitions, service layer, endpoints, and ingestion pipeline all depend on the schema change landing atomically.

These atomicity indicators require all changes to land together. The `workflow:feature-branch` label will be applied to the feature issue.

**Interdependent tasks:**
- The database migration (enum type + column + backfill + FK drop + table drop) must land with the entity definition updates, service/endpoint updates, and ingestion pipeline updates. Any subset would leave the codebase in an inconsistent state.

---

### trustify-backend

changes:
  - Create database migration to define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` foreign key column, and drop `advisory_status` lookup table
  - Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` foreign key with `status` enum column; remove `entity/src/advisory_status.rs` entity and its registration in `entity/src/lib.rs`
  - Update advisory service layer (`modules/fundamental/src/advisory/service/advisory.rs`) to query `status` enum column directly instead of joining `advisory_status` table
  - Update advisory model structs (`modules/fundamental/src/advisory/model/summary.rs`, `details.rs`) to use enum status field instead of joined status
  - Update advisory endpoints (`modules/fundamental/src/advisory/endpoints/list.rs`, `get.rs`) to filter by enum column instead of join
  - Update advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to write enum values directly instead of inserting into lookup table
  - Update advisory integration tests (`tests/api/advisory.rs`) to reflect new schema and query patterns
  - Update internal architecture documentation to reflect schema change

### Excluded requirements

None. All requirements from the Feature description can be planned against the trustify-backend repository.
