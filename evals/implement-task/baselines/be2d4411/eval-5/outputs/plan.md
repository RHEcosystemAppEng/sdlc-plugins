# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

TC-9205 adds a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Target Branch

The task description specifies **Target Branch: TC-9005**. This is a feature branch workflow -- TC-9205 is a sub-task incorporated by TC-9005. The PR must target the feature branch TC-9005, NOT main.

## Branch Operations

1. **Checkout the feature branch (target branch)**:
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch from the feature branch**:
   ```
   git checkout -b TC-9205
   ```

   The task branch is named `TC-9205` (the task issue ID), created from `TC-9005` (the feature branch / target branch).

3. **After implementation, push and create PR targeting TC-9005**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```

   The PR MUST specify `--base TC-9005` to target the feature branch, not main.

## Pre-Implementation Inspection

Before modifying any files, the following inspections would be performed:

1. **Read `migration/src/m0001_initial/mod.rs`** -- understand the existing migration pattern (MigrationTrait implementation, up/down methods, SeaORM usage)
2. **Read `migration/src/lib.rs`** -- understand how migrations are registered in the `migrations()` function vec
3. **Read `entity/src/advisory.rs`** -- verify that the advisory entity does NOT reference a `status` column (confirming it was already removed from the entity definition)
4. **Read `CONVENTIONS.md`** -- check for project-level conventions and CI check commands
5. **Grep for "status" in entity and service code** -- verify no remaining references to the `status` column exist in `modules/fundamental/src/advisory/` or other modules

## Files to Modify

### 1. `migration/src/lib.rs`
- **Change**: Register the new migration module `m0002_drop_advisory_status` in the migration list
- **Details**: Add `mod m0002_drop_advisory_status;` declaration and add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the existing pattern used for `m0001_initial`

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
- **Change**: Create a new migration module implementing `MigrationTrait`
- **Details**: 
  - Implement `up` method that drops the `status` column from the `advisory` table using `TableAlterStatement`
  - Implement `down` method that re-adds the `status` column as a nullable string for rollback
  - Follow the exact pattern from `m0001_initial/mod.rs`

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the `status` column
from the `advisory` table. The column was superseded by the `severity` enum
field and is no longer referenced by any entity or service code.

The down method re-adds the column as a nullable string to support rollback.

Implements TC-9205
```

With the trailer flag:
```
git commit --trailer="Assisted-by: Claude Code" -m "<message above>"
```

## PR Details

- **Title**: `feat(migration): add migration to drop advisory status column`
- **Base branch**: `TC-9005` (the feature branch, NOT main)
- **Head branch**: `TC-9205` (the task branch)
- **Description**: Would include a summary of the migration, link to Jira issue TC-9205, and reference that this is part of the TC-9005 feature branch work

## Jira Updates (would be performed, but skipped in this eval)

1. Transition TC-9205 to "In Progress" and assign to current user
2. After PR creation, update the Git Pull Request custom field (`customfield_10875`) with the PR URL
3. Add a comment summarizing the changes
4. Transition TC-9205 to "In Review"
