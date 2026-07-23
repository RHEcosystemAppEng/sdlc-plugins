# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## trustify-backend

### Changes

- Create a new SeaORM migration that atomically: creates the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds a `status` enum column to the `advisory` table, backfills the column from the existing `advisory_status` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table
- Update the SeaORM entity definition in `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` field of type `AdvisoryStatusEnum`, and define the Rust enum with `DeriveActiveEnum`
- Remove the `entity/src/advisory_status.rs` entity module and its export from `entity/src/lib.rs`
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to remove all joins to the `advisory_status` table and query the `status` enum column directly
- Update advisory list and get endpoint handlers in `modules/fundamental/src/advisory/endpoints/` to use the enum column for status filtering
- Update `AdvisorySummary` and `AdvisoryDetails` model structs to source status from the enum field instead of a joined relation
- Update shared query helpers in `common/src/db/query.rs` if advisory status filtering logic is implemented there
- Update advisory ingestion logic in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into the lookup table
- Update advisory integration tests in `tests/api/advisory.rs` to work with the new schema (status as enum column, no lookup table)

### Excluded Requirements

None. All requirements from the Feature description can be planned against the trustify-backend repository.

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migrations** -- The database migration adds the `status` enum column and drops the `status_id` FK column and the `advisory_status` lookup table. All application code (entity definitions, service layer, ingestion pipeline, tests) depends on the migration completing first. Merging any code change without the migration would reference a column (`status`) that does not exist; merging the migration without the code changes would break all advisory queries that still join the now-dropped `advisory_status` table.

2. **Tightly coupled feature components** -- The entity definition change (removing `status_id`, adding `status` enum) is consumed by the service layer, endpoints, and ingestion pipeline. None of these changes function independently. The Feature's non-functional requirements explicitly state: "All changes must land together: merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:**
- Migration (Task 2) must land before entity definitions (Task 3)
- Entity definitions (Task 3) must land before service/endpoints (Task 4) and ingestion (Task 5)
- Tests (Task 6) must land after service/endpoints (Task 4) and ingestion (Task 5)
- All intermediate tasks must be merged into the feature branch before the final merge to main

The `workflow:feature-branch` label will be applied to the TC-9005 feature issue.

---

## Epic Grouping

**Strategy:** by-sub-feature (from Hierarchy Configuration in CLAUDE.md)

| Epic | Label | Tasks |
|---|---|---|
| Epic 1 | TC-9005: Schema migration | Task 2 (migration), Task 3 (entity definitions) |
| Epic 2 | TC-9005: Advisory code updates | Task 4 (service/endpoints), Task 5 (ingestion), Task 6 (tests) |
| Epic 3 | TC-9005: Documentation | Task 7 (documentation) |

---

## Task Creation Log — additional_fields

The following `additional_fields` are applied to every created task and epic, inherited from the Feature issue TC-9005:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

**Priority:** "High" -- inherited from Feature TC-9005 (priority is set, not "Undefined").

**fixVersions:** "RHTPA 2.0.0" -- inherited from Feature TC-9005. The Feature has a non-empty fixVersions array, and no `fixVersion scope` setting exists in Jira Field Defaults (CLAUDE.md), so the default scope "both" applies -- fixVersions are propagated to tasks.

**Feature issue label update:** After all tasks are created, the `workflow:feature-branch` label is appended to TC-9005's existing labels: `["ai-generated-jira", "workflow:feature-branch"]`.

---

## Documentation Signals

Extracted from Feature description "Documentation Considerations" section:

- **Doc impact type:** Updates to existing content
- **Details:** Update internal architecture docs to reflect schema change. No external API documentation changes needed. Reference material: SeaORM enum mapping documentation.

A documentation task (Task 7) will be generated.

---

## Testing Readiness Template

No `docs/testing-readiness.md` file found in the trustify-backend repository. No cross-cutting testing tasks will be generated.

---

*This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.4.*
