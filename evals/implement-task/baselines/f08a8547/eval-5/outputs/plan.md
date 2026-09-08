# Implementation Plan: TC-9205

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table in the trustify-backend repository.

## Target Branch and Branch Operations

- **Target Branch**: `TC-9005` (feature branch, not main)
- **Bookend Type**: None
- **Target PR**: None

### Branch operations

1. Check out the feature branch and pull latest:
   ```
   git checkout TC-9005
   git pull
   ```
2. Create a task branch from the feature branch:
   ```
   git checkout -b TC-9205
   ```
3. After implementation, push and open a PR targeting `TC-9005`:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
   ```

The PR targets `TC-9005` (the feature branch), not `main`. This is critical because the Target Branch section specifies `TC-9005`.

### Fork detection

Before creating the PR, check for an `upstream` remote:
```
git remote get-url upstream 2>/dev/null
```
- If upstream exists, use: `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 ...`
- If no upstream, use: `gh pr create --base TC-9005 ...`

## Files to Modify

1. **`migration/src/lib.rs`** -- Register the new migration module `m0002_drop_advisory_status` in the migration list

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** -- Migration that implements `MigrationTrait` with `up` (drop column) and `down` (re-add column) methods

## Pre-Implementation Verification

Before writing code:
- Verify that `entity/src/advisory.rs` no longer references a `status` column (confirming the column is truly deprecated)
- Read `migration/src/m0001_initial/mod.rs` to understand the sibling migration pattern
- Read `migration/src/lib.rs` to understand how migrations are registered
- Check `CONVENTIONS.md` at the repository root for CI checks and naming conventions

## Implementation Approach

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

Create a new migration module following the `m0001_initial/mod.rs` pattern:
- Implement `MigrationTrait` for a new struct (e.g., `Migration`)
- `up` method: use `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down` method: re-add the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback
- Implement the `name()` method following the naming convention from sibling migration

### File 2: `migration/src/lib.rs` (MODIFY)

- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the m0001_initial entry

## Testing

- Run migration against test database to confirm `up` succeeds
- Run migration rollback to confirm `down` re-adds the column as nullable string
- Verify existing advisory queries still work after column is dropped
- Run `cargo test -p migration` (resolve crate name via `cargo metadata --no-deps --format-version 1`)

## Self-Verification Checklist

- [ ] Scope containment: only `migration/src/lib.rs` modified, only `migration/src/m0002_drop_advisory_status/mod.rs` created
- [ ] No sensitive patterns in diff
- [ ] Entity file `entity/src/advisory.rs` confirmed to have no `status` references
- [ ] Migration registered in correct order after m0001_initial
- [ ] `down` method properly restores the column as nullable string
- [ ] CI checks from CONVENTIONS.md pass (formatting, linting, compilation)
- [ ] Rust module-level tests pass: `cargo test -p <migration-crate-name>`

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused `status`
column from the `advisory` table. The column was replaced by the `severity`
enum field and is no longer referenced by any service or entity code.
The down method re-adds the column as a nullable string for rollback safety.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Description

```
## Summary
- Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- Register the new migration in `migration/src/lib.rs`
- Down method re-adds the column as nullable string for safe rollback

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan
- [ ] Migration runs successfully against test database
- [ ] Rollback re-adds the column as nullable string
- [ ] Existing advisory queries still function after column removal
```

**PR targets**: `TC-9005` (feature branch)

## Jira Updates

1. Transition TC-9205 to "In Progress" and assign to current user (Step 3)
2. After PR creation:
   - Set `customfield_10875` (Git Pull Request) to the PR URL using ADF format
   - Add comment with PR link, summary of changes, and any deviations
   - Transition TC-9205 to "In Review"
