# Repository Impact Map — TC-9005

## Feature: Drop status table and migrate to enum column

### trustify-backend

**changes:**
- Create a new database migration that defines the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds a `status` enum column to the `advisory` table, backfills it from the existing `status_id` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table — all within a single atomic migration
- Update the SeaORM entity definition in `entity/src/advisory.rs` to replace the `status_id` integer foreign key with a `status` enum column mapped to the new `advisory_status_enum` type, and remove the `entity/src/advisory_status.rs` entity file and its registration in `entity/src/lib.rs`
- Update the advisory service in `modules/fundamental/src/advisory/service/advisory.rs` to remove all joins against the `advisory_status` table and query the `status` enum column directly; update `AdvisorySummary` and `AdvisoryDetails` model structs if they reference the join
- Update the advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to filter by the enum column instead of joining the lookup table
- Update the advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly to the `status` column instead of inserting into the lookup table and referencing via foreign key
- Update advisory integration tests in `tests/api/advisory.rs` to reflect the new schema (no join, enum column filtering, direct enum insertion in test fixtures)

### Excluded requirements

None. All requirements from the Feature description are plannable within the trustify-backend repository.

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migration** — The migration adds the `advisory_status_enum` type and `status` column while dropping the `status_id` FK and `advisory_status` table. All code changes (entity definitions, service queries, ingestion pipeline) depend on this migration completing. Merging the migration without the code changes would break all advisory queries (they still reference the dropped table via join), and merging the code changes without the migration would reference a column that does not exist.

2. **Breaking API changes** — The entity definition change (replacing `status_id: i32` with `status: AdvisoryStatusEnum`) is consumed by the service layer, endpoints, and ingestion pipeline. Partial delivery would leave callers referencing a field that no longer exists.

3. **Tightly coupled feature components** — The feature's non-functional requirements explicitly state: "All changes must land together: merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:** All implementation tasks (migration, entity update, service/endpoint queries, ingestion pipeline, integration tests) are interdependent — none can be merged to `main` independently without breaking the application.

The `workflow:feature-branch` label will be applied to the feature issue TC-9005 in Step 6a.

---

## Epic Grouping

**Strategy:** by-sub-feature (from Hierarchy Configuration)

| Epic | Tasks |
|---|---|
| TC-9005: Schema migration | Task 2 (migration), Task 3 (entity definitions) |
| TC-9005: Application logic updates | Task 4 (advisory queries), Task 5 (ingestion pipeline) |
| TC-9005: Validation and documentation | Task 6 (integration tests), Task 7 (documentation) |

---

## Task Creation Log — additional_fields

All created Epics and Tasks will include the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- **priority**: inherited from Feature TC-9005 (priority = "High", not "Undefined")
- **fixVersions**: inherited from Feature TC-9005 (fixVersions = ["RHTPA 2.0.0"]); no `fixVersion scope` setting in Jira Field Defaults, so default scope "both" applies — propagated to tasks
- **labels**: `ai-generated-jira` is mandatory on all AI-created issues

The feature issue TC-9005 will also receive the `workflow:feature-branch` label appended to its existing labels.
