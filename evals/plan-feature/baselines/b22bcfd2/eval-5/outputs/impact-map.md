# Impact Map: TC-9005 — Drop status table and migrate to enum column

## Workflow Mode

**Feature-branch workflow** selected based on atomicity constraints in the NFRs:
- "Migration must be atomic: if any step fails, the entire migration rolls back"
- "All changes must land together: merging the migration without the code changes would break all advisory queries"

These constraints require all changes to land as a single atomic unit. Direct-to-main would risk partial delivery.

**Label decision**: Apply the `workflow:feature-branch` label to feature issue TC-9005 to indicate feature-branch workflow mode.

## Priority and Fix Version Propagation

- **Priority**: High (inherited from TC-9005, propagated to all tasks via additional_fields)
- **Fix Versions**: RHTPA 2.0.0 (inherited from TC-9005, propagated to all tasks via additional_fields; fixVersion scope config is absent from CLAUDE.md ### Jira Field Defaults, defaulting to 'both')

## Repository Impact

trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) via new SeaORM migration
    - Add `status` enum column to `advisory` table and backfill from existing `status_id` join
    - Drop `status_id` foreign key column from `advisory` table
    - Drop `advisory_status` lookup table
    - Update SeaORM entity `entity/src/advisory.rs` to replace `status_id` relation with `status` enum field
    - Remove `entity/src/advisory_status.rs` entity definition (no longer needed)
    - Update `modules/fundamental/src/advisory/service/advisory.rs` to query `status` column directly instead of joining `advisory_status`
    - Update `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` to use enum status field
    - Update `modules/fundamental/src/advisory/endpoints/list.rs` and `get.rs` to filter/return status from enum column
    - Update `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of lookup table inserts
    - Update `tests/api/advisory.rs` integration tests for new schema

## Ambiguities and Risks

- The CONVENTIONS.md file is listed in the repository structure but its contents are not available; convention-aware enrichment cannot be applied without reviewing the actual convention definitions.
- Zero-downtime migration strategy (concurrent enum type creation, column addition with default) should be validated against PostgreSQL version requirements.

## Summary Comment (Step 6c)

All 7 tasks (5 intermediate + 2 bookend) were created for TC-9005 under feature-branch workflow mode. Priority "High" was inherited from the feature and propagated to all tasks. Fix version "RHTPA 2.0.0" was inherited and propagated to all tasks (fixVersion scope defaults to 'both' since no ### Jira Field Defaults section exists in CLAUDE.md). The `workflow:feature-branch` label should be applied to TC-9005.
