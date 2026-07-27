# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, extracted from the Target Branch section of the task description)
**Linked Issues**: is incorporated by TC-9005

## Target Branch Extraction

The task description contains a **Target Branch** section with value `TC-9005`. This identifies a feature branch (not `main`) as the PR base. All branch operations and PR targeting must use TC-9005 as the base, not main.

## Branch Operations

### 1. Check out the target branch (TC-9005)

```bash
git checkout TC-9005
git pull
```

This checks out the feature branch TC-9005 (the Target Branch from the task description), NOT main. The task is part of a feature branch workflow where multiple tasks are developed against a shared feature branch.

### 2. Create the task branch

```bash
git checkout -b TC-9205
```

The task branch is named `TC-9205` (the task's own Jira issue ID), not TC-9005 (the feature branch). This creates a branch from the TC-9005 feature branch for this specific task's work.

## Pre-Implementation Code Inspection

Before making any changes, inspect the following existing files to understand current patterns and verify assumptions:

### Files to Inspect

1. **`migration/src/m0001_initial/mod.rs`** -- Inspect to understand the existing migration pattern. This file implements `MigrationTrait` with `up` and `down` methods using SeaORM. The new migration must follow the exact same pattern (struct definition, `MigrationTrait` impl, `MigrationName` impl).

2. **`entity/src/advisory.rs`** -- Verify that the `advisory` entity no longer references the `status` column. The task description states this column was replaced by the `severity` enum field. This must be confirmed before proceeding with the drop-column migration.

3. **`migration/src/lib.rs`** -- Inspect to understand how migrations are registered. The file contains a `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>` with entries like `Box::new(m0001_initial::Migration)`. The new migration must be appended here.

### Inspection Approach

Using the Serena instance `serena_backend` (from the Repository Registry in CLAUDE.md):

- `mcp__serena_backend__get_symbols_overview` on `migration/src/m0001_initial/mod.rs` to see its structure
- `mcp__serena_backend__find_symbol` with `include_body=true` on the `Migration` struct and `MigrationTrait` impl to read the exact patterns
- `mcp__serena_backend__get_symbols_overview` on `entity/src/advisory.rs` to verify no `status` column reference exists
- `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to see the migration registration pattern
- `mcp__serena_backend__search_for_pattern` for `status` across the advisory module to confirm no code references the deprecated column

Additionally, check for `CONVENTIONS.md` at the repository root and read it if present to extract CI check commands and coding conventions.

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** -- New migration module that drops the `status` column from the `advisory` table.

## Files to Modify

1. **`migration/src/lib.rs`** -- Register the new migration module in the migration list.

## Implementation Details

See `file-1-description.md` for the new migration file and `file-2-description.md` for the lib.rs modification.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused `status`
column from the `advisory` table. The column was replaced by the `severity`
enum field in a previous migration and is no longer referenced by any
service or entity code.

The `down` method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

The commit command:

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205"
```

## Push and PR Creation

```bash
git push -u origin TC-9205
```

Create a PR targeting the feature branch TC-9005 (NOT main):

```bash
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

- Add migration \`m0002_drop_advisory_status\` that drops the deprecated \`status\` column from the \`advisory\` table
- Register the new migration in \`migration/src/lib.rs\`
- The \`down\` method re-adds the column as a nullable string for rollback support

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

The `--base TC-9005` flag ensures the PR targets the feature branch, not main. This is critical because the task's Target Branch is TC-9005.

## Jira Updates

1. Update the Git Pull Request custom field (`customfield_10875`) with the PR URL
2. Add a comment to TC-9205 summarizing the changes and linking to the PR
3. Transition TC-9205 to In Review

## Verification Steps

1. Run `cargo test` to verify migration compiles and tests pass
2. Verify acceptance criteria:
   - Migration drops the `status` column from the `advisory` table
   - Migration `down` method re-adds the column as nullable string for rollback
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the `status` column
3. Run scope containment check (`git diff --name-only`) to verify only in-scope files were modified
4. Run sensitive-pattern check on staged diff
5. Check for CI commands in `CONVENTIONS.md` and run them if present
