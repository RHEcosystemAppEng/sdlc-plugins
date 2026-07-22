# Plan Summary — TC-9005: Drop status table and migrate to enum column

## Tasks Created

| # | Summary | Type | Repository | Target Branch |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | Bookend (create-branch) | trustify-backend | main |
| 2 | Add database migration for advisory status enum conversion | Implementation | trustify-backend | TC-9005 |
| 3 | Update SeaORM entity definitions for advisory status | Implementation | trustify-backend | TC-9005 |
| 4 | Update advisory service, model, and endpoint layers | Implementation | trustify-backend | TC-9005 |
| 5 | Update advisory ingestion pipeline | Implementation | trustify-backend | TC-9005 |
| 6 | Update advisory integration tests | Implementation | trustify-backend | TC-9005 |
| 7 | Update internal architecture documentation | Documentation | trustify-backend | TC-9005 |
| 8 | Merge feature branch TC-9005 to main | Bookend (merge-branch) | trustify-backend | main |

**Total**: 8 tasks (2 bookend, 5 implementation, 1 documentation)

## Repositories Affected
- **trustify-backend** — all changes are scoped to this repository

## Workflow Mode
- **Mode**: `feature-branch`
- **Rationale**: The migration is atomic — the database schema change (dropping `advisory_status` table, adding `advisory_status_enum` column) and the code changes (entity definitions, service layer, ingestion pipeline) are mutually dependent. Merging the migration without code changes breaks all advisory queries (they still join the now-dropped table). Merging code changes without the migration references a column that does not exist. The Feature's Non-Functional Requirements explicitly state: "Migration must be atomic" and "All changes must land together."
- **Label**: `workflow:feature-branch` will be applied to feature issue TC-9005

## Inherited Field Propagation
- **Priority**: High — inherited from Feature TC-9005 and propagated to all created tasks
- **Fix Versions**: RHTPA 2.0.0 — inherited from Feature TC-9005 and propagated to all created tasks (fixVersion scope defaults to "both" since no Jira Field Defaults configuration restricts it)

## Architecture Summary
The plan replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. A single atomic migration handles the full conversion (enum type creation, column addition, data backfill, FK removal, table drop). Downstream changes update the SeaORM entity definitions, advisory service/model/endpoint layers, and the ingestion pipeline to use the new enum column directly. Integration tests are updated to match the new schema. The API response shape is unchanged — status remains a string value in JSON responses.
