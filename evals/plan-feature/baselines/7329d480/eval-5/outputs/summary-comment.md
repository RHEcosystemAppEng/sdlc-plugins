# Implementation Plan: TC-9005 — Drop status table and migrate to enum column

## Tasks

| # | Summary | Repository | Target Branch | Dependencies |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | trustify-backend | main | None |
| 2 | Write database migration for advisory status enum | trustify-backend | TC-9005 | Task 1 |
| 3 | Update SeaORM entity definitions for advisory status enum | trustify-backend | TC-9005 | Task 1, Task 2 |
| 4 | Update advisory service, model, and endpoints to use status enum | trustify-backend | TC-9005 | Task 1, Task 3 |
| 5 | Update advisory ingestion pipeline for direct enum writes | trustify-backend | TC-9005 | Task 1, Task 3 |
| 6 | Update advisory integration tests for status enum | trustify-backend | TC-9005 | Task 1, Task 4, Task 5 |
| 7 | Update internal architecture documentation for schema change | trustify-backend | main | None |
| 8 | Merge feature branch TC-9005 to main | trustify-backend | main | Tasks 2, 3, 4, 5, 6 |

## Repositories

- **trustify-backend** — all 8 tasks target this repository

## Architecture

The plan replaces the `advisory_status` lookup table with a PostgreSQL `advisory_status_enum` type and a direct `status` column on the `advisory` table. Changes span five areas:

1. **Database migration** — creates enum type, adds column, backfills from FK join, drops FK and lookup table
2. **SeaORM entities** — replaces `status_id` FK with `status` enum column, removes `advisory_status` entity
3. **Advisory service/endpoints** — removes all status table joins, filters by enum column directly
4. **Ingestion pipeline** — writes enum values directly instead of lookup table inserts
5. **Integration tests** — updates fixtures and assertions for enum-based status

## Workflow

**Mode: feature-branch** — The `workflow:feature-branch` label will be applied to TC-9005. All implementation tasks (2-6) target the `TC-9005` feature branch and are delivered atomically via a single merge to `main` (Task 8). This is required because the migration and code changes are interdependent: merging either without the other would leave the application in a broken state.

## Propagated Fields

All tasks are created with:
- **Priority**: High
- **Fix Versions**: RHTPA 2.0.0
- **Labels**: ai-generated-jira

```
additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 2.0.0"}] }
```
