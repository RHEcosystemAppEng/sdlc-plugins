# Implementation Plan for TC-9205

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch)
**Parent Feature**: TC-9005
**Bookend Type**: None (standard implementation task)
**Target PR**: None (new PR flow)

## Branch Operations

1. **Checkout target branch**: `git checkout TC-9005` -- this is a feature branch, not main
2. **Pull latest**: `git pull`
3. **Create task branch**: `git checkout -b TC-9205`
4. After implementation, push and create PR:
   - `git push -u origin TC-9205`
   - `gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."`
   - The PR targets the feature branch `TC-9005`, not `main`

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** -- new migration module that drops the deprecated `status` column from the `advisory` table

## Files to Modify

1. **`migration/src/lib.rs`** -- register the new migration module `m0002_drop_advisory_status` in the migration list

## Pre-Implementation Verification

- Verify that `entity/src/advisory.rs` does not reference a `status` column (confirming the column is no longer used by entity code)
- Inspect `migration/src/m0001_initial/mod.rs` to understand the existing migration pattern (MigrationTrait implementation, up/down methods)
- Check `CONVENTIONS.md` at the repository root for CI check commands and coding conventions
- Analyze sibling migration files to discover naming, structure, and error handling conventions

## Implementation Details

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

- Create a new module implementing `MigrationTrait`
- `up` method: use `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the `status` column
- `down` method: re-add the column as `ColumnDef::new(Advisory::Status).string().null()` to support rollback
- Follow the exact structure of `m0001_initial/mod.rs`

### File 2: `migration/src/lib.rs` (MODIFY)

- Add `mod m0002_drop_advisory_status;` declaration
- Add the new migration to the `vec![]` in the `migrations()` function, appended after `m0001_initial`

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Remove the `status` column from the `advisory` table via a new SeaORM
migration. The column was replaced by the `severity` enum field in a
previous migration and is no longer read or written by any service code.

The rollback (`down`) re-adds the column as a nullable string.

Implements TC-9205
```

Commit flag: `--trailer="Assisted-by: Claude Code"`

## PR Details

- **Base branch**: `TC-9005` (feature branch -- NOT main)
- **Head branch**: `TC-9205`
- **Title**: `feat(migration): drop deprecated status column from advisory table`
- **Description**: Includes `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)` with a clickable Jira link
- **Custom field update**: Set `customfield_10875` on TC-9205 with the PR URL in ADF format

## Jira Updates

1. Assign TC-9205 to current user via `jira.user_info()` + `jira.edit_issue()`
2. Transition TC-9205 to "In Progress" before starting
3. After PR creation, update `customfield_10875` with the PR URL
4. Add comment summarizing changes and linking the PR
5. Transition TC-9205 to "In Review"

## Acceptance Criteria Verification

- [ ] Migration drops the `status` column from the `advisory` table -- verified by inspecting the `up()` method
- [ ] Migration `down` method re-adds the column as nullable string for rollback -- verified by inspecting the `down()` method
- [ ] Migration is registered in `migration/src/lib.rs` -- verified by checking the `migrations()` vec
- [ ] No service or entity code references the `status` column -- verified by grepping the codebase

## Test Plan

- Run migration tests against a test PostgreSQL database
- Verify the `up` migration drops the column successfully
- Verify the `down` migration re-adds the column as a nullable string
- Verify existing advisory queries still work after the column is dropped
- Run full CI checks from CONVENTIONS.md before committing
