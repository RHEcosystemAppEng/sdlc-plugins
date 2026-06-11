# Implementation Plan for TC-9205

## Task Summary

**TC-9205**: Add migration to drop status table column

Drop the deprecated `status` column from the `advisory` table via a new SeaORM database migration. The column was replaced by the `severity` enum field in a prior migration and is no longer referenced by any service or entity code.

## Branch Operations

1. **Checkout base branch**: `git checkout TC-9005` (the feature branch specified as Target Branch)
2. **Create task branch**: `git checkout -b TC-9205` (branch named after the task's own Jira issue ID, created from TC-9005)
3. **After implementation**: Push and open PR targeting the feature branch: `gh pr create --base TC-9005`

## Pre-Implementation Inspection

Before making any changes, inspect the following files to understand existing patterns and verify assumptions:

1. **Read `migration/src/m0001_initial/mod.rs`** -- Understand the existing migration pattern (MigrationTrait implementation, SeaORM API usage, struct naming)
2. **Read `migration/src/lib.rs`** -- Understand how migrations are registered (module declarations, migrations() function, vec![] ordering)
3. **Read `entity/src/advisory.rs`** -- Verify that the `status` column is NOT referenced in the entity definition (confirming it is safe to drop)
4. **Grep for `status` across `modules/` and `entity/`** -- Verify no service or entity code references the `advisory.status` column

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs` (NEW)

A new migration module that drops the `status` column from the `advisory` table. Follows the pattern established by `m0001_initial/mod.rs`.

See `outputs/file-1-description.md` for detailed contents.

## Files to Modify

### 2. `migration/src/lib.rs` (MODIFY)

Register the new `m0002_drop_advisory_status` migration module in the migration list.

See `outputs/file-2-description.md` for detailed changes.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

The status column was replaced by the severity enum field in a previous
migration and is no longer read or written by any service code. Removing
it prevents accidental usage and reduces confusion.

Implements TC-9205
```

With trailer: `--trailer='Assisted-by: Claude Code'`

## PR Details

**Title**: feat(migration): drop deprecated status column from advisory table

**Base branch**: `TC-9005` (the feature branch, NOT main)

**Body**:
```
## Summary
- Add migration m0002_drop_advisory_status that drops the deprecated `status` column from the `advisory` table
- Register the new migration in `migration/src/lib.rs`
- The `down` method re-adds the column as a nullable string for safe rollback

## Jira
Implements [TC-9205](https://<jira-host>/browse/TC-9205)
```

## Acceptance Criteria Verification

- [x] Migration drops the `status` column from the `advisory` table -- implemented in `up()` method using `TableAlterStatement`
- [x] Migration `down` method re-adds the column as nullable string for rollback -- implemented in `down()` method using `ColumnDef::new(Advisory::Status).string().null()`
- [x] Migration is registered in `migration/src/lib.rs` -- added module declaration and entry in `migrations()` vec
- [x] No service or entity code references the `status` column -- verified via grep and entity inspection

## Jira Updates

1. Transition TC-9205 to "In Progress" at start
2. Post PR link as comment on TC-9205 after PR creation
3. Set PR URL on custom field `customfield_10875` (Git Pull Request field)
4. Transition TC-9205 to "In Review" after PR is opened
