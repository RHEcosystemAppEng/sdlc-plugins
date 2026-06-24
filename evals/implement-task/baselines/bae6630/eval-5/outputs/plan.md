# Implementation Plan for TC-9205

## Task Summary

**Jira Issue**: TC-9205 — Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, extracted from the Target Branch section of the task description)
**Task Branch**: TC-9205 (named after the Jira issue ID, distinct from the Target Branch TC-9005)
**Parent Feature**: TC-9005 (linked via "is incorporated by TC-9005")

## Pre-Implementation Inspection

Before making any changes, inspect the existing codebase to understand current patterns and verify assumptions:

1. **Read `migration/src/m0001_initial/mod.rs`** — Understand the existing migration pattern: how `MigrationTrait` is implemented, what `up` and `down` methods look like, and how SeaORM migration APIs are used. This is the sibling file referenced in the Implementation Notes.
2. **Read `entity/src/advisory.rs`** — Verify that the `status` column is no longer referenced in the Advisory entity definition, as stated in the Implementation Notes. This confirms it is safe to drop the column.
3. **Read `migration/src/lib.rs`** — Understand how migrations are registered in the `migrations()` function and where the new migration module should be added.

## Branch Operations

1. **Check out the Target Branch (TC-9005)**:
   ```
   git checkout TC-9005
   git pull
   ```
   The Target Branch is TC-9005, NOT main. This is a feature branch workflow where TC-9205 is a sub-task of the TC-9005 feature.

2. **Create the task branch (TC-9205)**:
   ```
   git checkout -b TC-9205
   ```
   The task branch is named TC-9205, matching the Jira issue ID. This is distinct from TC-9005 (the Target Branch / feature branch).

3. **Push and open PR targeting TC-9005**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --head TC-9205 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
   ```
   The PR MUST use `--base TC-9005` to target the feature branch, NOT `--base main`.

## Files to Modify

### 1. `migration/src/lib.rs`
- Register the new migration module `m0002_drop_advisory_status` in the `migrations()` function
- Add `mod m0002_drop_advisory_status;` declaration
- Append `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the pattern of the existing `m0001_initial` entry

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
- Implement `MigrationTrait` for a `Migration` struct following the pattern in `migration/src/m0001_initial/mod.rs`
- `up` method: use `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the `status` column
- `down` method: re-add the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback
- Include proper documentation comments on the struct and methods

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Remove the unused `status` column from the `advisory` table via a new
SeaORM migration. The column was replaced by the `severity` enum field
in m0001_initial and is no longer read or written by any service code.

The migration includes a rollback method that re-adds the column as a
nullable string.

Implements TC-9205
```

The commit command:
```
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Remove the unused status column from the advisory table via a new
SeaORM migration. The column was replaced by the severity enum field
in m0001_initial and is no longer read or written by any service code.

The migration includes a rollback method that re-adds the column as a
nullable string.

Implements TC-9205"
```

## PR Details

- **Title**: `feat(migration): drop deprecated status column from advisory table`
- **Base branch**: TC-9005 (the Target Branch, NOT main)
- **Head branch**: TC-9205 (the task branch)
- **Description**: Includes `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)` with a clickable Jira link

## Verification Steps

Before committing:
1. Verify `entity/src/advisory.rs` does not reference `status` column
2. Run `cargo test` to ensure migration compiles and existing tests pass
3. Run scope containment check (`git diff --name-only`) to confirm only in-scope files are modified
4. Run sensitive-pattern check on staged diff
5. Check for untracked files in affected directories
