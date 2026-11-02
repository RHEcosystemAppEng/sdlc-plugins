# Repository Impact Map — TC-9005

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration creates an enum type, adds a column, backfills data, drops the foreign key column, and drops the lookup table. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column (`status`) that does not exist.
2. **Breaking API changes** — The entity definitions, service layer, and endpoints must all switch from `status_id` FK join to the `status` enum column simultaneously. Partial delivery leaves the codebase referencing either the old or new schema, breaking at runtime.
3. **Tightly coupled feature components** — The ingestion pipeline must write enum values directly instead of inserting into the lookup table. This change is only valid after the migration runs and only functional if the entity layer matches.

**Interdependent tasks:** Tasks 2 (migration), 3 (entities), 4 (service/endpoints), 5 (ingestion), and 6 (tests) are all interdependent — none can be merged independently to `main` without breaking advisory functionality.

**Label decision:** Apply `workflow:feature-branch` label to feature issue TC-9005.

---

## trustify-backend

### Changes

- Create database migration: define `advisory_status_enum` PostgreSQL type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from `advisory_status` join, drop `status_id` FK column, drop `advisory_status` table
- Update SeaORM entity definitions: modify `entity/src/advisory.rs` to replace `status_id: i32` with `status: AdvisoryStatusEnum`, remove `entity/src/advisory_status.rs` (if it exists) or remove advisory_status references from `entity/src/lib.rs`
- Update `AdvisoryService` methods (`fetch`, `list`, `search`) to query `advisory.status` directly instead of joining `advisory_status`
- Update advisory endpoints (`list.rs`, `get.rs`) to return status from the enum column
- Update advisory ingestion pipeline to write `advisory_status_enum` values directly instead of inserting into the lookup table
- Update integration tests in `tests/api/advisory.rs` to validate enum-based status filtering and ingestion

### Excluded Requirements

None — all requirements are within scope of the trustify-backend repository.

---

## Task Creation Log

### Inherited Field Propagation

| Field | Feature Value | Propagated to Tasks | Reason |
|---|---|---|---|
| Priority | High | Yes | Feature priority is set (not "Undefined") — inherited by all created tasks |
| fixVersions | RHTPA 2.0.0 | Yes | Feature has non-empty fixVersions and fixVersion scope defaults to "both" (no explicit scope in Jira Field Defaults) |

### additional_fields for all created issues

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

### Epic Grouping

No level-1 issue type (Epic) is available — tasks are created directly under the Feature (Feature → Task hierarchy).

---

## Task Summary

| # | Slug | Repository | Target Branch | Type | Dependencies |
|---|---|---|---|---|---|
| 1 | create-feature-branch | trustify-backend | main | Bookend (create-branch) | None |
| 2 | migration-enum-column | trustify-backend | TC-9005 | Implementation | Task 1 |
| 3 | update-entity-definitions | trustify-backend | TC-9005 | Implementation | Task 1, Task 2 |
| 4 | update-advisory-service-endpoints | trustify-backend | TC-9005 | Implementation | Task 1, Task 3 |
| 5 | update-ingestion-pipeline | trustify-backend | TC-9005 | Implementation | Task 1, Task 3 |
| 6 | update-integration-tests | trustify-backend | TC-9005 | Implementation | Task 1, Task 4, Task 5 |
| 7 | update-architecture-documentation | trustify-backend | TC-9005 | Documentation | Task 4, Task 5, Task 6 |
| 8 | merge-feature-branch | trustify-backend | main | Bookend (merge-branch) | Tasks 2, 3, 4, 5, 6 |

### Description Digests

Digests are recorded in separate `task-N-digest.md` files in the outputs directory. Each contains a `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>` marker computed from the task description content.
