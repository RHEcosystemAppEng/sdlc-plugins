# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Key:** TC-9205
**Summary:** Add migration to drop status table column
**Status:** To Do
**Parent Feature:** TC-9005 (linked via "is incorporated by TC-9005")
**Target Branch:** TC-9005
**Dependencies:** None

## Branch Operations

### Branch Strategy

This task targets a **feature branch** (TC-9005), not main. The branch operations are:

1. **Checkout the feature branch:**
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch from the feature branch:**
   ```
   git checkout -b TC-9205
   ```

3. **After implementation, push and create PR targeting the feature branch:**
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
   ```

   The `--base TC-9005` flag is critical -- this PR must target the feature branch TC-9005, not main.

### Fork Detection

Before creating the PR, check for a fork by running:
```
git remote get-url upstream 2>/dev/null
```

If an upstream remote exists, use:
```
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 ...
```

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Remove the deprecated `status` column from the `advisory` table via a new
SeaORM migration. The column was replaced by the `severity` enum field and
is no longer referenced by any entity or service code. The rollback method
re-adds the column as a nullable string.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Description

```
## Summary

- Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code
- Rollback (`down`) re-adds the column as a nullable string for safe recovery

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

## Pre-Implementation Verification

Before implementing, the following checks would be performed:

1. **Verify entity state:** Read `entity/src/advisory.rs` to confirm the `status` column is no longer referenced in the entity definition (only `severity` should remain).
2. **Inspect sibling migration:** Read `migration/src/m0001_initial/mod.rs` to understand the exact MigrationTrait implementation pattern (imports, struct name, method signatures).
3. **Inspect migration registration:** Read `migration/src/lib.rs` to understand how migrations are registered (module declaration and vec! inclusion).
4. **Search for status column references:** Grep across the codebase for any remaining references to `Advisory::Status` or the `status` column to ensure no service code still depends on it.
5. **Read CONVENTIONS.md:** Check the repository root for convention rules and CI check commands.

## Files to Modify

### 1. `migration/src/lib.rs`
- Register the new migration module
- See `outputs/file-1-description.md` for detailed changes

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
- New migration implementing MigrationTrait
- See `outputs/file-2-description.md` for detailed changes

## Self-Verification Checklist

### Scope Containment
- `git diff --name-only` should show only:
  - `migration/src/lib.rs` (modified)
  - `migration/src/m0002_drop_advisory_status/mod.rs` (created)
- Any other files would be flagged as out-of-scope

### Untracked File Check
- The new `migration/src/m0002_drop_advisory_status/mod.rs` will appear as untracked
- It is listed in Files to Create, so it is in scope and should be staged

### Sensitive Pattern Check
- Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
- No sensitive patterns expected in migration code

### Acceptance Criteria Verification
- [x] Migration drops the `status` column from the `advisory` table -- verified by `up()` method using `drop_column(Advisory::Status)`
- [x] Migration `down` method re-adds the column as nullable string for rollback -- verified by `down()` method using `ColumnDef::new(Advisory::Status).string().null()`
- [x] Migration is registered in `migration/src/lib.rs` -- verified by module declaration and vec! entry
- [x] No service or entity code references the `status` column -- verified by grep search

### Data-Flow Trace
- **Input:** Migration runner invokes `up()` on the migration
- **Processing:** SeaORM's `SchemaManager` translates `TableAlterStatement` to `ALTER TABLE advisory DROP COLUMN status`
- **Output:** Column is removed from the database schema
- **Rollback path:** `down()` reverses via `ALTER TABLE advisory ADD COLUMN status VARCHAR NULL`
- **Complete:** Both forward and reverse paths are fully connected

### Contract & Sibling Parity
- **Contract:** `MigrationTrait` requires `up()` and `down()` methods -- both implemented
- **Sibling parity with `m0001_initial`:** Both implement `MigrationTrait` with async up/down methods using `SchemaManager`
- **Cross-module entity analysis:** The `advisory` table is used by `modules/fundamental/src/advisory/` and `modules/ingestor/src/graph/advisory/` -- neither references the `status` column (already removed from entity definition)

## Jira Updates

### Step 3 -- Transition to In Progress
1. Retrieve current user: `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9205, assignee=<account-id>)`
3. Transition: `jira.transition_issue(TC-9205) -> In Progress`

### Step 11 -- Update Jira After PR
1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment with PR link, summary of changes, and any deviations
3. Transition: `jira.transition_issue(TC-9205) -> In Review`
