# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Status**: To Do
**Parent Feature**: TC-9005 (is incorporated by)
**Target Branch**: TC-9005 (feature branch)
**Dependencies**: None

## Branch Operations

1. **Checkout the target branch** (feature branch for TC-9005):
   ```
   git checkout TC-9005
   git pull
   ```
2. **Create a task branch** from the feature branch:
   ```
   git checkout -b TC-9205
   ```
   This creates the task branch `TC-9205` based off the `TC-9005` feature branch, since the Target Branch is `TC-9005` (not `main`).

3. **After implementation, push and create PR**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```
   The PR targets the `TC-9005` feature branch (not `main`), matching the Target Branch from the task description.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the unused `status`
column from the `advisory` table. The column was replaced by the `severity`
enum field in a previous migration and is no longer referenced by any
service or entity code.

The `down` method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Description

```
## Summary

Add a database migration (`m0002_drop_advisory_status`) that drops the deprecated `status` column from the `advisory` table. The column was previously replaced by the `severity` enum field and is no longer read or written by any service code.

- New migration module `m0002_drop_advisory_status` with `up` (drop column) and `down` (re-add as nullable string) methods
- Migration registered in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test Plan

- [ ] Verify migration compiles: `cargo build -p migration`
- [ ] Test migration runs against test database: `cargo test -p migration`
- [ ] Test rollback (down) re-adds the column
- [ ] Verify existing advisory queries still work after column is dropped
```

## Files to Modify

1. **`migration/src/lib.rs`** — Register the new migration module in the migration list

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** — Migration that drops the `status` column from the `advisory` table

## Pre-implementation Verification

Before implementing, verify the following:
- The `advisory` entity in `entity/src/advisory.rs` does NOT reference a `status` column (confirming it is safe to drop)
- The existing migration pattern in `migration/src/m0001_initial/mod.rs` uses `MigrationTrait` with `up` and `down` methods
- No service code in `modules/fundamental/src/advisory/` references the `status` column

## Self-Verification Checks

- **Scope containment**: Only `migration/src/lib.rs` (modify) and `migration/src/m0002_drop_advisory_status/mod.rs` (create) should appear in `git diff --name-only`
- **Untracked file check**: The new `mod.rs` file must be staged for commit
- **Sensitive-pattern check**: No secrets expected in migration code
- **Data-flow trace**: Migration up drops column, migration down re-adds column — both paths complete
- **Contract verification**: `MigrationTrait` requires both `up()` and `down()` methods — both implemented
- **Sibling parity**: Follow the same pattern as `m0001_initial/mod.rs`

## Jira Updates

1. **Transition**: To Do -> In Progress (at start)
2. **Assign**: Assign to current user
3. **After PR creation**:
   - Set Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
   - Add comment with PR link, summary of changes
   - Transition: In Progress -> In Review
