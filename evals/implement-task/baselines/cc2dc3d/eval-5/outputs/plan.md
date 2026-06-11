# Implementation Plan for TC-9205: Add migration to drop status table column

## Step 1 -- Fetch and Parse Jira Task

Parsed from the task description:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (a feature branch, NOT main)
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module in the migration list
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column from the `advisory` table
- **Implementation Notes**: Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs`; use SeaORM's `TableAlterStatement`; register in `lib.rs`; `down` method should re-add column as nullable string
- **Acceptance Criteria**: Migration drops `status` column; `down` re-adds as nullable string; migration registered in `lib.rs`; no service/entity code references `status` column
- **Test Requirements**: Migration runs successfully; rollback re-adds the column; existing advisory queries still work
- **Dependencies**: None
- **Linked Issues**: is incorporated by TC-9005
- **Bookend Type**: not present
- **Target PR**: not present

## Step 4 -- Understand the Code

Before making any changes, inspect the existing code to understand patterns and confirm assumptions:

1. **Read `migration/src/m0001_initial/mod.rs`** -- Examine the existing migration to understand the pattern for implementing `MigrationTrait`, including the `up` and `down` methods, how `Migration` struct is defined, and how `MigrationName` trait is implemented. This is the primary pattern reference cited in Implementation Notes.

2. **Read `entity/src/advisory.rs`** -- Verify that the `advisory` entity no longer references a `status` column, confirming it is safe to drop. The entity should only reference `severity` (the replacement field).

3. **Read `migration/src/lib.rs`** -- Understand how migrations are registered in the `migrations()` function, specifically the `vec![]` pattern and how `m0001_initial` is referenced, so the new migration can be registered identically.

4. **Identify sibling files for convention analysis** -- The sibling for the new migration file is `m0001_initial/mod.rs`. Examine its structure to discover conventions around naming, imports, error handling, and migration trait implementation.

5. **Check for CONVENTIONS.md** at the repository root for any explicit project conventions and CI check commands.

6. **Documentation file identification** -- Check for README files in `migration/` directory and root-level docs.

## Step 5 -- Create Branch (Feature Branch Flow)

The Target Branch is **TC-9005** (a feature branch). The task branch must be created from this feature branch, NOT from main.

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

Key distinctions:
- **TC-9005** is the feature branch (Target Branch) -- this is what we check out first
- **TC-9205** is the task branch -- this is the new branch we create for this task's work
- These are DISTINCT identifiers; TC-9005 is the parent feature, TC-9205 is this specific task

## Step 6 -- Files to Modify

### File 1: `migration/src/lib.rs` (modify)
- Add `mod m0002_drop_advisory_status;` module declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the existing pattern of `m0001_initial`

### File 2: `migration/src/m0002_drop_advisory_status/mod.rs` (create)
- Create new migration module implementing `MigrationTrait`
- Define `Migration` struct
- Implement `MigrationName` trait returning the migration name
- Implement `up` method: use `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the `status` column
- Implement `down` method: re-add the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback support
- Follow patterns from `m0001_initial/mod.rs` for imports, structure, and error handling

## Step 7 -- Tests

- Test that the migration `up` runs successfully against a test database
- Test that the rollback `down` re-adds the `status` column as a nullable string
- Verify that existing advisory queries still work after the column is dropped

## Step 10 -- Commit and Push

### Commit message (Conventional Commits format):

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that drops the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field and is no longer used by any service code.

The down method re-adds the column as a nullable string for rollback.

Implements TC-9205
```

With trailer: `--trailer='Assisted-by: Claude Code'`

### Push and create PR:

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

The PR must target `--base TC-9005` (the feature branch), NOT `--base main`, because the Target Branch for this task is TC-9005.

PR description will include:
- Summary of changes
- `Implements [TC-9205](<webUrl>)` with clickable Jira link
- Reference to acceptance criteria

## Step 11 -- Update Jira

- Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format
- Add comment to TC-9205 summarizing the changes and linking the PR
- Transition TC-9205 to **In Review**
