# Implementation Plan for TC-9205: Add migration to drop status table column

## Target Branch Extraction

The task description contains a **Target Branch** section with value **TC-9005**. This is a feature branch (not `main`), indicating feature-branch workflow. All branch operations and PR targeting must use TC-9005 as the base.

## Branch Operations

### 1. Check out the Target Branch (TC-9005)

```bash
git checkout TC-9005
git pull
```

TC-9005 is the feature branch that this task contributes to. We check it out first so the new task branch is based on the latest feature branch state.

### 2. Create the task branch (TC-9205)

```bash
git checkout -b TC-9205
```

The task branch is named after the Jira issue ID (TC-9205), which is distinct from the Target Branch (TC-9005). The task branch is where implementation work happens.

## Pre-Implementation Code Inspection (Constraint 1.5)

Before making any changes, inspect the following files to understand existing patterns and verify assumptions:

1. **`migration/src/m0001_initial/mod.rs`** -- Read this file to understand the existing migration pattern. This is referenced in the Implementation Notes as the pattern to follow. We need to see how `MigrationTrait` is implemented, how `up` and `down` methods are structured, and what imports are used (SeaORM migration types, entity references, etc.).

2. **`entity/src/advisory.rs`** -- Read this file to verify that the `status` column is no longer referenced in the entity definition. The task description states "The advisory entity in entity/src/advisory.rs no longer references the status column -- verify this before proceeding." This is a prerequisite check before writing the migration.

3. **`migration/src/lib.rs`** -- Read this file to understand how migrations are registered. We need to see the `migrations()` function and its `vec![]` to know the exact pattern for adding the new migration module.

Additionally, inspect sibling files for convention conformance analysis:
- Other files in `migration/src/` to understand module declaration patterns
- `entity/src/lib.rs` to understand entity module registration
- `tests/api/advisory.rs` to understand test patterns for advisory-related functionality

## Files to Create

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the deprecated `status` column from the `advisory` table. Implements `MigrationTrait` with:
- `up` method: drops the `status` column using `TableAlterStatement`
- `down` method: re-adds the column as a nullable string for rollback

See `outputs/file-1-description.md` for detailed implementation.

## Files to Modify

### File 2: `migration/src/lib.rs`

Register the new migration module `m0002_drop_advisory_status` in the migration list. Add the module declaration and append it to the `vec![]` in the `migrations()` function.

See `outputs/file-2-description.md` for detailed changes.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Remove the `status` column that was replaced by the `severity` enum field.
The column is no longer read or written by any service code.

Implements TC-9205
```

The commit command:

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Remove the status column that was replaced by the severity enum field.
The column is no longer read or written by any service code.

Implements TC-9205"
```

This follows:
- **Conventional Commits** (constraint 2.1, 2.2): `feat(migration): <description>` with TC-9205 in the footer
- **Assisted-by trailer** (constraint 2.3): `--trailer="Assisted-by: Claude Code"`

## Push and PR Creation

### Push the branch

```bash
git push -u origin TC-9205
```

### Create PR targeting TC-9005

```bash
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

- Add migration m0002_drop_advisory_status to drop the deprecated \`status\` column from the \`advisory\` table
- Register the new migration in migration/src/lib.rs
- The \`down\` method re-adds the column as a nullable string for rollback

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

The PR uses `--base TC-9005` to target the feature branch, NOT `main`. This is the critical distinction for feature-branch workflow -- the task's work merges into the feature branch, which will later be merged into `main` via a merge-branch bookend task.

## Verification Steps

1. Run `cargo test` to verify the migration compiles and tests pass
2. Verify acceptance criteria:
   - Migration drops the `status` column from the `advisory` table
   - Migration `down` method re-adds the column as nullable string for rollback
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the `status` column
3. Run scope containment check (`git diff --name-only`) to confirm only in-scope files were modified
4. Run sensitive-pattern check on staged diff
