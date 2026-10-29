# Implementation Plan: TC-9205 — Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory`
table. The column was replaced by the `severity` enum field in a previous migration and
is no longer read or written by any service code.

## Target Repository

trustify-backend (Serena instance: serena_backend, Path: ./)

## Branch Operations

1. **Checkout the target branch** (feature branch, not main):
   ```
   git checkout TC-9005
   git pull
   ```
2. **Create the task branch** from the feature branch:
   ```
   git checkout -b TC-9205
   ```
3. After implementation and verification, **push and open a PR targeting TC-9005**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
   ```

The PR targets **TC-9005** (the feature branch), NOT main. This is because the task's
Target Branch is TC-9005.

## Files to Modify

### 1. `migration/src/lib.rs`
Register the new migration module in the migration list. Add `mod m0002_drop_advisory_status;`
declaration and append `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]`
returned by the `migrations()` function, following the existing pattern used for
`m0001_initial`.

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
New migration module implementing `MigrationTrait` with:
- `up` method: drops the `status` column from the `advisory` table using
  `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()`
  to allow rollback
- Follows the exact structure of `migration/src/m0001_initial/mod.rs`

## Pre-Implementation Verification

Before implementing, verify:
- `entity/src/advisory.rs` does NOT reference a `status` column (confirming it is safe to drop)
- No service code in `modules/fundamental/src/advisory/` references `status`
- No ingestor code in `modules/ingestor/src/graph/advisory/` references `status`
- Check `CONVENTIONS.md` at the repository root for coding conventions and CI check commands

## Convention Conformance

Analyze sibling migration `migration/src/m0001_initial/mod.rs` to discover:
- Migration struct naming pattern
- `MigrationTrait` implementation pattern
- `name()` method return format
- `up()` and `down()` method signatures and error handling
- Import conventions

## Test Plan

Per Test Requirements:
1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

Tests would be added to the migration crate's test suite or integration tests.

## Self-Verification Checklist

- [ ] Scope containment: only `migration/src/lib.rs` modified and `migration/src/m0002_drop_advisory_status/mod.rs` created
- [ ] No dead parameters introduced
- [ ] No sensitive patterns in diff
- [ ] No references to `status` column remain in entity or service code
- [ ] CI checks from CONVENTIONS.md pass
- [ ] `cargo test -p migration` passes (Rust module-level test requirement)

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

The `status` column on the `advisory` table was replaced by the
`severity` enum field and is no longer read or written by any
service code. This migration removes it to prevent accidental
usage and reduce schema confusion.

The rollback (`down`) re-adds the column as a nullable string.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Details

- **Title**: `feat(migration): drop deprecated status column from advisory table`
- **Base branch**: `TC-9005` (feature branch)
- **Head branch**: `TC-9205`
- **Description**:
  ```
  ## Summary
  - Add database migration `m0002_drop_advisory_status` that drops the deprecated
    `status` column from the `advisory` table
  - Register the new migration in `migration/src/lib.rs`
  - Include rollback support (re-adds column as nullable string)

  Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

  ## Test plan
  - [ ] Migration runs successfully against test database
  - [ ] Rollback (down) re-adds the column
  - [ ] Existing advisory queries still work after column is dropped
  ```

## Jira Updates

1. **Assign** TC-9205 to current user
2. **Transition** TC-9205 to "In Progress" at start
3. **Update** `customfield_10875` (Git Pull Request) with PR URL (in ADF format)
4. **Add comment** to TC-9205 with PR link and summary of changes
5. **Transition** TC-9205 to "In Review" after PR creation
