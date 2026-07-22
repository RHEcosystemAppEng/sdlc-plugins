# Implementation Plan: TC-9205 — Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Repository

trustify-backend

## Branch Operations

1. **Checkout target branch**: `git checkout TC-9005` — the Target Branch is a feature branch (TC-9005), not main.
2. **Pull latest**: `git pull`
3. **Create task branch**: `git checkout -b TC-9205` — branch named after the Jira issue ID, created from TC-9005.
4. **Push and PR**: After implementation, push TC-9205 and create a PR targeting `TC-9005` (the feature branch):
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
   ```
   The PR description will include `Implements [TC-9205](<webUrl>)` with the Jira issue URL.

## Files to Modify

| # | File | Action | Description |
|---|------|--------|-------------|
| 1 | `migration/src/lib.rs` | Modify | Register the new migration module `m0002_drop_advisory_status` in the migration list |

## Files to Create

| # | File | Action | Description |
|---|------|--------|-------------|
| 2 | `migration/src/m0002_drop_advisory_status/mod.rs` | Create | Migration that drops the `status` column from the `advisory` table, with rollback support |

## Pre-Implementation Verification

- Verify that `entity/src/advisory.rs` does NOT reference a `status` column — the task notes this column was already removed from the entity definition.
- Read `migration/src/m0001_initial/mod.rs` to understand the existing migration pattern (MigrationTrait implementation, up/down methods, use of SeaORM Table/Column types).
- Read `migration/src/lib.rs` to understand how migrations are registered in the `migrations()` function.
- Check `CONVENTIONS.md` at repository root for any additional conventions or CI check commands.

## Implementation Steps

### Step 1: Create migration module (`migration/src/m0002_drop_advisory_status/mod.rs`)

Create a new migration file following the pattern established in `m0001_initial/mod.rs`:
- Implement `MigrationTrait` with `up()` and `down()` methods
- `up()`: Use `TableAlterStatement` to drop the `status` column from the `advisory` table
- `down()`: Re-add the `status` column as a nullable string to support rollback
- Use SeaORM's `Table::alter()`, `Advisory::Table`, and `Advisory::Status` identifiers

### Step 2: Register migration in `migration/src/lib.rs`

- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry

### Step 3: Write tests

- Test that the migration runs successfully (up method)
- Test that the rollback re-adds the column (down method)
- Verify existing advisory queries still work after the column is dropped

### Step 4: Self-verification

- Run `git diff --name-only` and confirm only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` are changed
- Run `cargo test` to verify all tests pass
- Run any CI check commands from CONVENTIONS.md
- Verify no sensitive patterns in the diff

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the `status`
column from the `advisory` table. The column was replaced by the
`severity` enum field and is no longer used by any service code.

The down method re-adds the column as a nullable string for rollback.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Details

- **Base branch**: TC-9005 (feature branch)
- **Head branch**: TC-9205
- **Title**: `feat(migration): drop deprecated status column from advisory table`
- **Description**: Includes summary of changes, link to Jira issue, and acceptance criteria verification.

## Jira Updates

1. Transition TC-9205 to "In Progress" at start
2. Assign to current user
3. After PR creation: update Git Pull Request custom field (`customfield_10875`) with PR URL
4. Add comment with PR link and summary of changes
5. Transition TC-9205 to "In Review"
