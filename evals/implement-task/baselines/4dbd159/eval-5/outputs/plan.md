# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Parsed Task Fields

- **Jira Issue**: TC-9205
- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (feature branch, NOT main)
- **Linked Issues**: is incorporated by TC-9005
- **Bookend Type**: none
- **Target PR**: none
- **Dependencies**: none

## Branch Operations

1. **Check out the target branch** (TC-9005 -- the feature branch, not main):
   ```
   git checkout TC-9005
   git pull
   ```
2. **Create the task branch** from TC-9005:
   ```
   git checkout -b TC-9205
   ```
3. After implementation, push and create PR targeting TC-9005:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```

**Critical**: The PR must target `--base TC-9005`, not `main`. The task is incorporated by the TC-9005 feature, so the PR feeds into the feature branch.

## Files to Create

1. `migration/src/m0002_drop_advisory_status/mod.rs` -- new migration module that drops the `status` column from the `advisory` table

## Files to Modify

1. `migration/src/lib.rs` -- register the new migration module in the migration list

## Pre-Implementation Verification

- Verify that `entity/src/advisory.rs` does NOT reference a `status` column (confirming the entity has already been updated)
- Read `migration/src/m0001_initial/mod.rs` to understand the existing migration pattern (MigrationTrait, up/down methods)
- Read `migration/src/lib.rs` to understand how migrations are registered in the `migrations()` function
- Check `CONVENTIONS.md` at the repository root for project conventions and CI check commands
- Search for any remaining references to `Advisory::Status` or `status` column in service/entity code

## Implementation Steps

### Step 1: Create migration module

Create `migration/src/m0002_drop_advisory_status/mod.rs` implementing `MigrationTrait` with:
- `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback

### Step 2: Register migration

Modify `migration/src/lib.rs`:
- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in `migrations()` function, after the m0001_initial entry

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the status column
from the advisory table. The column was replaced by the severity enum
field in a previous migration and is no longer referenced by any service
or entity code.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Details

- **Base branch**: TC-9005 (NOT main)
- **Head branch**: TC-9205
- **Title**: feat(migration): drop deprecated status column from advisory table
- **Description**: Would include:
  - Summary of the migration changes
  - Link to Jira: `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)`
  - Note about rollback support via the `down` method

## Jira Updates

1. Transition TC-9205 to In Progress (Step 3)
2. Assign to current user (Step 3)
3. After PR creation:
   - Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format
   - Add comment with PR link, summary of changes
   - Transition to In Review

## Acceptance Criteria Verification

- [ ] Migration drops the `status` column from the `advisory` table -- verified by `up` method implementation
- [ ] Migration `down` method re-adds the column as nullable string for rollback -- verified by `down` method implementation
- [ ] Migration is registered in `migration/src/lib.rs` -- verified by lib.rs modification
- [ ] No service or entity code references the `status` column -- verified by pre-implementation search

## Test Requirements

- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped
