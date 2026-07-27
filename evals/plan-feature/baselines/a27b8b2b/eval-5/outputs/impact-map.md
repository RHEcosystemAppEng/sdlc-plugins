# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## trustify-backend

### Changes

- Create a reversible database migration that: defines `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds `status` enum column to `advisory` table, backfills the new column from the existing `advisory_status` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table
- Update the SeaORM entity definition in `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` field using the new enum type, and remove `entity/src/advisory_status.rs`
- Update `modules/fundamental/src/advisory/service/advisory.rs` to remove all `advisory_status` table joins and query the `status` enum column directly for fetch, list, and search operations
- Update `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` to use the new `status` column for filtering and response mapping
- Update `modules/fundamental/src/advisory/model/summary.rs` and `modules/fundamental/src/advisory/model/details.rs` to source the status field from the enum column instead of the joined lookup table
- Update `modules/ingestor/src/graph/advisory/mod.rs` to write the `advisory_status_enum` value directly on insert instead of writing to the lookup table and referencing via foreign key
- Update `entity/src/lib.rs` to remove the `advisory_status` module export
- Update `tests/api/advisory.rs` to reflect the new schema (direct enum status instead of joined lookup table)

### Excluded Requirements

None — all requirements from the Feature description are addressable within the trustify-backend repository.

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale — atomicity indicators identified:**

1. **Coordinated schema migration** — the migration adds the `advisory_status_enum` type and `status` column while dropping the `status_id` FK column and `advisory_status` table. Code that still joins the lookup table would break if the migration runs first, and code referencing the new `status` column would break if the migration has not run.
2. **Cross-cutting refactor** — the entity definition change (`advisory.rs` replacing `status_id` with `status`) cascades through the service layer, endpoints, model structs, and ingestion pipeline. Partial delivery would leave the codebase with incompatible entity definitions.
3. **Tightly coupled components** — the Feature description explicitly states: "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:**
- The migration task must land before entity/service/endpoint/ingestion tasks can function
- Entity updates must align with service/endpoint changes (both reference the same `status` field)
- Ingestion pipeline changes depend on the new enum type existing in the schema

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.
