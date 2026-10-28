# Implementation Plan: TC-9205

## Task Summary

**Jira ID**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005
**Status**: To Do
**Linked Issues**: is incorporated by TC-9005

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:

1. **Repository Registry** -- present with trustify-backend entry (Serena instance: serena_backend, Path: ./)
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID (10142)
3. **Code Intelligence** -- present with tool naming convention and serena_backend instance

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed fields from the task description:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module in the migration list
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column from the `advisory` table
- **Implementation Notes**: Follow existing m0001_initial pattern; implement MigrationTrait with up/down; use SeaORM TableAlterStatement; register in lib.rs migrations() vec
- **Acceptance Criteria**: 4 items (drop column, rollback, registration, no stale references)
- **Test Requirements**: 3 items (migration runs, rollback works, existing queries still work)
- **Bookend Type**: not present
- **Target PR**: not present
- **Dependencies**: None

### Target Branch extraction

Target Branch is **TC-9005**. This is a feature branch (not main). The task branch will be based on this branch, and the PR will target this branch.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue("TC-9205", assignee=<account-id>)` to assign
3. `jira.transition_issue("TC-9205")` to In Progress

## Step 4 -- Understand the Code

### Files to inspect

1. **migration/src/lib.rs** -- understand current migration registration pattern (how migrations() vec is structured, what imports exist)
2. **migration/src/m0001_initial/mod.rs** -- sibling migration to analyze for conventions (this is the primary convention source)
3. **entity/src/advisory.rs** -- verify the `status` column is no longer referenced in the entity definition

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root (trustify-backend/CONVENTIONS.md). The repo structure shows this file exists. Would read it for naming rules, directory structure, code patterns, test conventions, and CI check commands.

### Convention conformance analysis

Analyze `m0001_initial/mod.rs` as the sibling migration file. See outputs/conventions.md for full convention analysis.

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- No migration-specific documentation identified in the repo structure

## Step 5 -- Create Branch

This is the **default flow** (no Target PR, no Bookend Type).

**Branch operations:**

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

- Check out the **target branch** TC-9005 (the feature branch)
- Pull latest changes from remote
- Create a new **task branch** named TC-9205 (the task's Jira issue ID)

The task branch name is TC-9205 (the task issue ID), NOT TC-9005 (the feature/target branch).

## Step 6 -- Implement Changes

### Files to modify

1. **migration/src/lib.rs** -- Add `mod m0002_drop_advisory_status;` declaration and register `m0002_drop_advisory_status::Migration` in the `migrations()` function's `vec![]`. See outputs/file-1-description.md.

### Files to create

1. **migration/src/m0002_drop_advisory_status/mod.rs** -- New migration module implementing `MigrationTrait` with `up()` and `down()` methods. See outputs/file-2-description.md.

### Pre-implementation verification

Before implementing, verify that `entity/src/advisory.rs` does NOT reference a `status` column -- the task states it was already removed in favor of `severity`. This confirms the migration is safe.

## Step 7 -- Write Tests

Test requirements from the task:
1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

These are integration tests that require a PostgreSQL test database. Following the project convention (tests in `tests/api/`), these would be run via `cargo test`. The migration framework's test harness handles migration up/down testing.

## Step 8 -- Verify Acceptance Criteria

1. Migration drops the `status` column from the `advisory` table -- verified by `up()` method using `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)`
2. Migration `down` method re-adds the column as nullable string for rollback -- verified by `down()` method using `ColumnDef::new(Advisory::Status).string().null()`
3. Migration is registered in `migration/src/lib.rs` -- verified by adding to `vec![]` in `migrations()`
4. No service or entity code references the `status` column -- verified by inspecting `entity/src/advisory.rs` and grepping codebase

## Step 9 -- Self-Verification

1. **Scope containment**: `git diff --name-only` should show only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` -- both are in scope
2. **Sensitive-pattern check**: No secrets or credentials expected in migration code
3. **Duplication check**: Search for existing drop-column migrations or similar patterns
4. **CI checks from CONVENTIONS.md**: Run any CI commands found in CONVENTIONS.md
5. **Module-level test requirement (Rust)**: Run `cargo test -p migration` for the migration crate
6. **Data-flow trace**: Migration up drops column, down re-adds it -- complete lifecycle
7. **Contract & sibling parity**: Verify MigrationTrait is fully implemented (both up and down methods)

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the unused status
column, which was replaced by the severity enum field. The down method
re-adds the column as a nullable string for rollback safety.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

### Push and PR

```bash
git push -u origin TC-9205
```

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If no fork detected:

```bash
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "$(cat <<'EOF'
## Summary

- Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- The column was replaced by the `severity` enum field and is no longer referenced by any service or entity code
- Migration includes rollback support: `down()` re-adds the column as a nullable string

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
EOF
)"
```

Key points:
- **PR targets TC-9005** (the feature branch) via `--base TC-9005`
- The task branch is **TC-9205**
- The commit references **TC-9205** in the footer

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format
2. Add comment to TC-9205 with PR link, summary of changes, and any deviations
3. Transition TC-9205 to In Review
