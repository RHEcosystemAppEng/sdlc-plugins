# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Linked Issues

- **Parent feature**: TC-9005 (this task is incorporated by TC-9005)

## Branch Operations

1. **Checkout the target branch** (TC-9005, which is a feature branch -- not main):
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch** from the target branch:
   ```
   git checkout -b TC-9205
   ```

3. **After implementation, push and create PR targeting TC-9005**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```

   The PR must target `TC-9005` (the feature branch), not `main`. The `--base TC-9005` flag is mandatory.

   The PR description will include:
   ```
   ## Summary
   - Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
   - Register the new migration in `migration/src/lib.rs`
   - The `down` method re-adds the column as a nullable string for rollback support

   Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
   ```

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the `status`
column from the `advisory` table. The column was replaced by the
`severity` enum field and is no longer referenced by any service or
entity code. The down method re-adds the column as a nullable string
to support rollback.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## Files to Modify

### 1. `migration/src/lib.rs`
- **Action**: Modify existing file
- **Change**: Register the new migration module `m0002_drop_advisory_status` in the migration list
- **Details**: See `outputs/file-1-description.md`

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
- **Action**: Create new file
- **Change**: Implement the migration that drops the `status` column from the `advisory` table
- **Details**: See `outputs/file-2-description.md`

## Pre-Implementation Verification

Before implementing, verify:
1. The `advisory` entity in `entity/src/advisory.rs` does not reference a `status` column (confirming it was already removed from the entity definition)
2. No service code in `modules/fundamental/src/advisory/` or `modules/ingestor/src/graph/advisory/` references a `status` field on the advisory entity
3. The existing migration pattern in `migration/src/m0001_initial/mod.rs` to understand the `MigrationTrait` implementation pattern

## Post-Implementation Verification

1. **Scope containment**: Run `git diff --name-only` and verify only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` are changed
2. **Acceptance criteria check**:
   - Migration drops the `status` column from the `advisory` table
   - Migration `down` method re-adds the column as nullable string for rollback
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the `status` column
3. **Tests**: Run `cargo test` to verify the migration runs successfully
4. **CI checks**: Run any CI check commands from CONVENTIONS.md if present
5. **Sensitive-pattern check**: Scan staged diff for secrets/credentials

## Jira Updates

1. **Transition to In Progress** at the start of implementation
2. **Assign** to current user
3. **After PR creation**:
   - Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
   - Add comment with PR link, summary of changes, and any deviations
   - Transition to **In Review**
