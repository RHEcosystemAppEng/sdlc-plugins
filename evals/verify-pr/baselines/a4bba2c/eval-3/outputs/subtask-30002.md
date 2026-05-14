## Repository
trustify-backend

## Target Branch
main

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Description
Add a partial index on the `deleted_at` column of the `sbom` table to optimize the frequent `deleted_at IS NULL` filter used by the list endpoint. Without this index, every call to `GET /api/v2/sbom` performs a full table scan on the `deleted_at` column, which will degrade as the table grows.

## Review Context
**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation after the `alter_table` call in the `up` method, and add index drop in the `down` method

## Implementation Notes
- Add a partial index using SeaORM migration API or raw SQL: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL`
- The index should be created in the `up` method after the existing `alter_table` call that adds the `deleted_at` column
- The `down` method should drop the index before dropping the column
- If using SeaORM's `Index::create()`, note that partial indexes may require raw SQL via `manager.get_connection().execute_unprepared(...)` depending on SeaORM version support for WHERE clauses on indexes
- Follow existing migration patterns in the codebase for index creation

## Acceptance Criteria
- [ ] Migration `up` creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` with a `WHERE deleted_at IS NULL` condition
- [ ] Migration `down` drops the index before dropping the `deleted_at` column
- [ ] Migration runs successfully against a PostgreSQL database
- [ ] The list endpoint query benefits from the new index (verified by query plan or convention)

## Test Requirements
- [ ] Migration can be applied and rolled back without errors
