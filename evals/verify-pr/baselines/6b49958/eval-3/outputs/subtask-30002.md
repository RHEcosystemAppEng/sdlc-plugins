## Repository
trustify-backend

## Target Branch
main

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Reviewer **reviewer-a** commented on `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14):

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The `SbomService::list` method filters by `deleted_at IS NULL` on every list query, and this filter will be exercised frequently. A partial index on `deleted_at WHERE deleted_at IS NULL` will optimize these queries by indexing only the non-deleted rows.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` — add a partial index creation step in the `up` method and a corresponding drop index step in the `down` method

## Implementation Notes
- Add the index creation after the `alter_table` call in the `up` method using SeaORM migration's index creation API or raw SQL
- The partial index should be equivalent to: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- In the `down` method, drop the index before dropping the column
- Follow the existing migration patterns in the `migration/src/` directory for index creation conventions

## Acceptance Criteria
- [ ] Migration `m0042_sbom_soft_delete` creates a partial index on `sbom.deleted_at` where `deleted_at IS NULL`
- [ ] The `down` migration drops the index before dropping the `deleted_at` column
- [ ] The index name follows project conventions (e.g., `idx_sbom_not_deleted`)
- [ ] Migration runs successfully against a clean database and in rollback scenarios
