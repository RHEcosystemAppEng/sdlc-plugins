## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the existing soft-delete migration. Queries filtering by `deleted_at IS NULL` will be frequent (every default list query filters out soft-deleted records), and a partial index will optimize these lookups. The index should be added within the same migration file that adds the `deleted_at` column.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add a partial index on `sbom.deleted_at` in the `up` method and drop it in the `down` method

## Implementation Notes
- Add the index creation after the `alter_table` call in the `up` method
- Use SeaORM's `Index::create()` API or a raw SQL statement for the partial index:
  ```sql
  CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
  ```
- In the `down` method, drop the index before dropping the column:
  ```sql
  DROP INDEX IF EXISTS idx_sbom_not_deleted;
  ```
- Follow the existing migration index patterns in earlier migration files (check `migration/src/m0001_initial/mod.rs` and other migrations for index creation conventions)

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index on `sbom.deleted_at` where `deleted_at IS NULL`
- [ ] The migration `down` method drops the partial index before dropping the `deleted_at` column
- [ ] The index name follows the project's naming convention for indexes

## Test Requirements
- [ ] Verify the migration applies successfully (up and down) without errors

## Review Context
**Original review comment (ID: 30002) by reviewer-a on `migration/src/m0042_sbom_soft_delete/mod.rs` line 14:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Target PR
https://github.com/trustify/trustify-backend/pull/744
