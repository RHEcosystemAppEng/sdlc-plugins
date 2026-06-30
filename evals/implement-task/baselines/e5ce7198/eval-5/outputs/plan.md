# Implementation Plan for TC-9205

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer referenced by any service code.

## Branch Operations

1. **Checkout the feature branch**: `git checkout TC-9005` -- The task's Target Branch is `TC-9005` (a feature branch, not `main`), so we must first check out this branch as the base.
2. **Create task branch**: `git checkout -b TC-9205` -- Create the task branch from TC-9005, named after the Jira task issue ID per convention.
3. **Push and open PR**: After implementation, push the branch and create a PR targeting the feature branch:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```

## Pre-Implementation Inspection

Before making any changes, the following files must be inspected (constraint 5.2 -- code must not be modified without first inspecting it):

1. **`entity/src/advisory.rs`** -- Verify the entity no longer references the `status` column (as stated in Implementation Notes).
2. **`migration/src/m0001_initial/mod.rs`** -- Inspect the existing migration to understand the pattern for implementing `MigrationTrait` (the `up` and `down` methods, use statements, module structure).
3. **`migration/src/lib.rs`** -- Inspect the current migration registration to understand the `vec![]` pattern and determine where to add the new migration module.
4. **Sibling check across advisory service/model code** -- Grep for any remaining references to `status` in `modules/fundamental/src/advisory/` to confirm no code reads or writes the column.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`
- New migration module implementing `MigrationTrait`
- `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down` method: re-adds the column as a nullable string for rollback
- Follows the pattern from `m0001_initial/mod.rs`

## Files to Modify

### 2. `migration/src/lib.rs`
- Register the new `m0002_drop_advisory_status` migration module
- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the existing `m0001_initial` entry

## Commit Message

```
feat(migration): add migration to drop advisory status column

Drop the deprecated `status` column from the `advisory` table. The column
was replaced by the `severity` enum field in a previous migration and is
no longer read or written by any service code.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Description

```
## Summary
- Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- Register the new migration in `migration/src/lib.rs`
- Migration includes a rollback (`down`) method that re-adds the column as a nullable string

## Jira
Implements [TC-9205](https://<jira-host>/browse/TC-9205)
```

## PR Target

The PR targets `--base TC-9005` (the feature branch), NOT `main`, because the task's Target Branch is `TC-9005`.

## Post-PR Jira Updates

1. Post PR link as a comment on TC-9205
2. Set the Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format
3. Transition TC-9205 to "In Review"

## Acceptance Criteria Verification

- [ ] Migration drops the `status` column from the `advisory` table -- verified by inspecting the `up` method
- [ ] Migration `down` method re-adds the column as nullable string for rollback -- verified by inspecting the `down` method
- [ ] Migration is registered in `migration/src/lib.rs` -- verified by inspecting the module declaration and `migrations()` vec
- [ ] No service or entity code references the `status` column -- verified by grepping `entity/src/advisory.rs` and advisory service/model files
