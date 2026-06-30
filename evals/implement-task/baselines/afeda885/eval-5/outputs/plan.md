# Implementation Plan for TC-9205

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Status**: To Do
**Parent Feature**: TC-9005 (linked via "is incorporated by")

## Target Branch

**Target Branch: TC-9005**

The task description specifies `TC-9005` as the Target Branch. This is a feature-branch workflow -- the PR must target the feature branch `TC-9005`, not `main`. All branch operations below reflect this.

## Branch Operations

### 1. Check out the target branch (TC-9005) and pull latest

```bash
git checkout TC-9005
git pull
```

### 2. Create the task branch from TC-9005

```bash
git checkout -b TC-9205
```

The task branch is named `TC-9205` (the task issue ID). It is created from `TC-9005` (the feature branch), not from `main`.

### 3. After implementation, push and create PR targeting TC-9005

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --head TC-9205 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

The `--base TC-9005` flag ensures the PR targets the feature branch, not `main`.

## Files to Inspect Before Modifying

Before making any changes, inspect the following files to understand existing patterns and confirm assumptions:

1. **`migration/src/m0001_initial/mod.rs`** -- the existing migration that serves as the pattern to follow. Inspect the `MigrationTrait` implementation, the `up` and `down` methods, and how `Table::alter` or `Table::create` statements are structured.

2. **`entity/src/advisory.rs`** -- the Advisory entity definition. Verify that the `status` column is no longer referenced in the entity. The task states it was replaced by a `severity` enum field in a previous migration.

3. **`migration/src/lib.rs`** -- the migration registry. Inspect how `m0001_initial` is registered in the `migrations()` function to follow the same pattern for the new migration.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

A new migration module that drops the deprecated `status` column from the `advisory` table.

- Implement `MigrationTrait` with `up` and `down` methods
- `up`: drops the `status` column using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down`: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback
- Follow the exact pattern from `m0001_initial/mod.rs`

## Files to Modify

### 1. `migration/src/lib.rs`

Register the new migration module `m0002_drop_advisory_status` in the migration list.

- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry

## Verification Steps

Before committing, verify:

1. **Entity check**: Confirm `entity/src/advisory.rs` does not reference the `status` column (the task states it was already removed in favor of `severity`)
2. **Scope containment**: Run `git diff --name-only` to confirm only the expected files were modified/created
3. **Untracked file check**: Run `git status --short` to identify any untracked files in the migration directory
4. **Sensitive-pattern check**: Search staged diff for secrets or credentials
5. **Run tests**: `cargo test` to verify the migration compiles and existing tests pass
6. **Acceptance criteria**:
   - Migration drops the `status` column from the `advisory` table
   - Migration `down` method re-adds the column as nullable string for rollback
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the `status` column

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code. The down method re-adds the column as a nullable
string to support rollback.

Implements TC-9205
```

The commit command:

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code. The down method re-adds the column as a nullable
string to support rollback.

Implements TC-9205"
```

## PR Details

**Title**: `feat(migration): drop deprecated status column from advisory table`

**Base branch**: `TC-9005` (the feature branch, NOT main)

**Description**:

```
## Summary

- Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- The column was replaced by the `severity` enum field and is no longer used by any service or entity code
- Migration includes a `down` method that re-adds the column as a nullable string for rollback

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

## Data-Flow Trace

- Migration `up`: `ALTER TABLE advisory DROP COLUMN status` -- single DDL operation, no data flow beyond schema change -- **COMPLETE**
- Migration `down`: `ALTER TABLE advisory ADD COLUMN status VARCHAR NULL` -- single DDL operation for rollback -- **COMPLETE**
- Registration: `lib.rs` includes the migration in the `migrations()` vec, which SeaORM's migrator calls during `up`/`down` -- **COMPLETE**

## Jira Updates (would be performed)

1. Transition TC-9205 to "In Progress" at start
2. Assign to current user
3. After PR creation: update `customfield_10875` (Git Pull Request) with PR URL
4. Add comment with PR link and summary of changes
5. Transition TC-9205 to "In Review"
