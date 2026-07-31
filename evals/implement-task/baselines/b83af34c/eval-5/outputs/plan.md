# Implementation Plan for TC-9205

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch)
**Status**: To Do
**Parent Feature**: TC-9005

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- **Repository Registry**: present with trustify-backend entry (Serena instance: serena_backend, Path: ./)
- **Jira Configuration**: present with Project key (TC), Cloud ID, Feature issue type ID (10142)
- **Code Intelligence**: present with tool naming convention and configured instances

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9205 description:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (this is a feature branch, NOT main)
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- the migration itself
- **Implementation Notes**: Follow m0001_initial pattern, use SeaORM TableAlterStatement, implement MigrationTrait with up/down
- **Acceptance Criteria**: 4 items (drop column, down method, registered, no remaining references)
- **Test Requirements**: 3 items (migration runs, rollback works, existing queries work)
- **Dependencies**: None
- **Bookend Type**: not present (normal implementation task)
- **Target PR**: not present (new PR flow)

The webUrl would be captured as: `https://redhat.atlassian.net/browse/TC-9205`

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9205, "In Progress")` to update status

## Step 4 -- Understand the Code

Would inspect:
1. `migration/src/lib.rs` via `mcp__serena_backend__get_symbols_overview` to see migration registration structure
2. `migration/src/m0001_initial/mod.rs` via `mcp__serena_backend__find_symbol` to understand the MigrationTrait pattern
3. `entity/src/advisory.rs` via `mcp__serena_backend__get_symbols_overview` to confirm no `status` column reference remains
4. Check for `CONVENTIONS.md` at repository root (it exists per repo structure)
5. Sibling analysis on `m0001_initial/mod.rs` for migration conventions

Documentation files identified:
- `README.md` (repository root)
- `CONVENTIONS.md` (repository root)
- `docs/architecture.md`
- `docs/api.md`

## Step 5 -- Branch Operations

**This is the critical step for Target Branch handling.**

The Target Branch is `TC-9005` (a feature branch). The skill MUST:

1. Checkout the target branch (TC-9005), NOT main:
   ```
   git checkout TC-9005
   git pull
   ```

2. Create a new task branch named after the Jira issue ID (TC-9205), branching from TC-9005:
   ```
   git checkout -b TC-9205
   ```

The task branch `TC-9205` is distinct from the feature branch `TC-9005`. The task branch is created FROM the feature branch.

**NOT what happens**: We do NOT checkout main. We do NOT branch from main.

## Step 6 -- Implement Changes

### File 1 (Create): `migration/src/m0002_drop_advisory_status/mod.rs`

Create the migration module implementing MigrationTrait with:
- `up` method: drops the `status` column from the `advisory` table using SeaORM's TableAlterStatement
- `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback
- Follow the pattern from `m0001_initial/mod.rs`

### File 2 (Modify): `migration/src/lib.rs`

Add the new migration module to the migration list:
- Add `mod m0002_drop_advisory_status;` declaration
- Add the migration to the `vec![]` in the `migrations()` function, following the m0001_initial pattern

## Step 7 -- Write Tests

Implement tests per Test Requirements:
- Test that the migration runs successfully (up method)
- Test that the rollback (down method) re-adds the column
- Verify existing advisory queries still work after the column is dropped

Tests would be placed in the migration test infrastructure or `tests/api/advisory.rs`.

## Step 8 -- Verify Acceptance Criteria

Check each criterion:
1. Migration drops the `status` column -- verified by up method implementation
2. Migration down method re-adds as nullable string -- verified by down method
3. Migration is registered in lib.rs -- verified by lib.rs modification
4. No service or entity code references status column -- verified during Step 4

## Step 9 -- Self-Verification

Run scope containment, untracked file check, sensitive pattern check, CI checks from CONVENTIONS.md, data-flow trace, and contract/sibling parity checks.

## Step 10 -- Commit and Push

### Commit Message
```
feat(migration): drop deprecated status column from advisory table

The status column was replaced by the severity enum field in a previous
migration and is no longer read or written by any service code. Removing
it reduces confusion and prevents accidental usage.

Implements TC-9205
```

With `--trailer="Assisted-by: Claude Code"`.

### Push and PR Creation

**Critical: PR targets TC-9005, NOT main.**

1. Push the task branch:
   ```
   git push -u origin TC-9205
   ```

2. Check for fork (upstream remote detection):
   ```
   git remote get-url upstream 2>/dev/null
   ```

3. Create PR targeting the feature branch TC-9005 (NOT main):

   **No fork detected:**
   ```
   gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
   ```

   **Fork detected:**
   ```
   gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
   ```

   PR description body would include:
   ```
   ## Summary
   - Add database migration to drop the deprecated `status` column from the `advisory` table
   - Register the new migration module in the migration list
   - The column was replaced by the `severity` enum and is no longer used

   Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
   ```

**Key points about branch operations:**
- Task branch name: `TC-9205` (the task ID)
- Feature branch name: `TC-9005` (the parent feature branch)
- These are DISTINCT branches
- The task branch is created FROM TC-9005
- The PR targets TC-9005 via `--base TC-9005`
- The PR does NOT target main

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format
2. Add comment to TC-9205 with PR link, summary of changes, and any deviations
3. Transition TC-9205 to "In Review"
