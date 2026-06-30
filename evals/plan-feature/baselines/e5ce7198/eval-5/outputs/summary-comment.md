# Implementation Plan: TC-9005 — Drop status table and migrate to enum column

## Tasks

| # | Task | Repository | Target Branch | Dependencies |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | trustify-backend | main | None |
| 2 | Database migration: create enum type, backfill, drop lookup table | trustify-backend | TC-9005 | Task 1 |
| 3 | Update SeaORM entity definitions for advisory status enum | trustify-backend | TC-9005 | Task 1, Task 2 |
| 4 | Update advisory service and endpoints to use enum column | trustify-backend | TC-9005 | Task 1, Task 3 |
| 5 | Update advisory ingestion pipeline to write enum values | trustify-backend | TC-9005 | Task 1, Task 3 |
| 6 | Update advisory integration tests for enum-based status | trustify-backend | TC-9005 | Task 1, Task 4, Task 5 |
| 7 | Merge feature branch TC-9005 to main | trustify-backend | main | Task 2, Task 3, Task 4, Task 5, Task 6 |

## Repositories Affected

- **trustify-backend** -- all changes are within this single repository

## Architecture Summary

This feature replaces the `advisory_status` lookup table with a PostgreSQL enum column (`advisory_status_enum`) directly on the `advisory` table. The migration creates the enum type with values (New, Analyzing, Fixed, Rejected), backfills from the existing join, drops the foreign key and lookup table. Entity definitions, the advisory service layer, HTTP endpoints, the ingestion pipeline, and integration tests are all updated to use the new enum column. The API response shape is unchanged -- status remains a string in JSON output. The expected outcome is a ~40ms reduction in p95 latency on the advisory list endpoint by eliminating the unnecessary join.

## Workflow Mode

**workflow:feature-branch** -- This label will be applied to the TC-9005 feature issue. The feature-branch workflow was selected because the migration drops a table that existing code depends on, and the code changes reference a column that does not exist until the migration runs. All changes must land together to avoid breaking main. Bookend tasks (Task 1: create-branch, Task 7: merge-branch) bracket the intermediate implementation tasks.

## Inherited Fields

Inherited fields propagated to tasks: priority=High, fixVersion=RHTPA 2.0.0
