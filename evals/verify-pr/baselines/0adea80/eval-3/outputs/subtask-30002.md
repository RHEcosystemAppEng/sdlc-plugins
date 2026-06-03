## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The `list` endpoint filters by `deleted_at IS NULL` on every request, and without an index this filter requires a full table scan. A partial index (`WHERE deleted_at IS NULL`) provides efficient lookup for the common case where most SBOMs are not deleted.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add a partial index on `deleted_at` in the `up` migration and drop it in the `down` migration

## Implementation Notes
- Add the index creation after the `alter_table` call in the `up` method
- Use SeaORM's `Index::create()` API to create the partial index, or use a raw SQL statement for the partial index since SeaORM's index builder may not support `WHERE` clauses directly:
  ```rust
  manager.get_connection().execute_unprepared(
      "CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL"
  ).await?;
  ```
- In the `down` method, drop the index before dropping the column:
  ```rust
  manager.get_connection().execute_unprepared(
      "DROP INDEX IF EXISTS idx_sbom_not_deleted"
  ).await?;
  ```
- Follow existing migration patterns in the `migration/src/` directory for index creation

## Acceptance Criteria
- [ ] The `up` migration creates a partial index `idx_sbom_not_deleted` on `sbom(deleted_at) WHERE deleted_at IS NULL`
- [ ] The `down` migration drops the `idx_sbom_not_deleted` index before dropping the `deleted_at` column
- [ ] The migration runs successfully against a PostgreSQL test database
- [ ] The `list` endpoint query benefits from the index when filtering by `deleted_at IS NULL`

## Test Requirements
- [ ] Existing migration tests pass with the added index
- [ ] The `test_list_sboms_include_deleted` and `test_delete_sbom_returns_204` tests continue to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Classification:** code change request (upgraded from suggestion via convention check)
**Convention evidence:** Migration pattern for index creation on filtered columns. The PR adds a `filter(sbom::Column::DeletedAt.is_null())` query in `list.rs`, making `deleted_at` a frequently-filtered column that warrants an index in the migration. Applies: PR modifies `migration/src/m0042_sbom_soft_delete/mod.rs` matching the convention's migration file scope.
**Original comment:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```
