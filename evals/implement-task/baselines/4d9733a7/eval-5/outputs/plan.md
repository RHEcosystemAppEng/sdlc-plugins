# Implementation Plan for TC-9205

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Parent Feature**: TC-9005 (linked via "is incorporated by TC-9005")
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch -- extracted from the Target Branch section of the task description)

The Target Branch section in the task description specifies `TC-9005`. This is a feature branch, not `main`. All branching and PR operations must reference this feature branch accordingly.

## Step 1 -- Parse Task Description

Parsed sections from the TC-9205 task description:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module in the migration list
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column from the `advisory` table
- **Implementation Notes**: Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs`; use SeaORM's `TableAlterStatement`; register migration in `migration/src/lib.rs`
- **Dependencies**: None

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user via `jira.user_info()`
2. Assign TC-9205 to the current user via `jira.edit_issue(TC-9205, assignee=<accountId>)`
3. Transition TC-9205 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code

### 4.1 Inspect existing files before modifying

Before making any changes, read and analyze the following files to understand current patterns and verify preconditions:

1. **`migration/src/m0001_initial/mod.rs`** -- Read this file to understand the existing migration pattern. This is the reference migration cited in the Implementation Notes. It implements `MigrationTrait` with `up` and `down` methods using SeaORM's migration API. Examine the struct definition, the `MigrationName` implementation, and how `up`/`down` are structured. Use `mcp__serena_backend__get_symbols_overview` to see the file's structure, then `mcp__serena_backend__find_symbol` with `include_body=true` to read the `Migration` struct and its trait implementations.

2. **`migration/src/lib.rs`** -- Read this file to understand how migrations are registered. The file contains a `Migrator` struct implementing `MigratorTrait` with a `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>`. The existing entry for `m0001_initial` shows the registration pattern.

3. **`entity/src/advisory.rs`** -- Read this file to verify that the Advisory entity no longer references the `status` column. The task description states the column was replaced by the `severity` enum field. Confirm that no `Status` variant exists in the entity's `Column` enum before proceeding with the migration. This verification is required by the Acceptance Criteria ("No service or entity code references the `status` column").

### 4.2 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. The repository structure shows a `CONVENTIONS.md` file exists. Read it and extract:
- CI check commands for verification in Step 9
- Coding conventions to follow during implementation

### 4.3 Convention conformance analysis (sibling analysis)

Identify sibling files for each file being modified or created:

- **For `migration/src/m0002_drop_advisory_status/mod.rs`** (new migration): The sibling is `migration/src/m0001_initial/mod.rs`. Inspect its structure to discover migration conventions (struct naming, trait implementations, identifier enum patterns).
- **For `migration/src/lib.rs`**: Inspect the existing module declarations and `migrations()` function to understand the registration pattern.

### 4.4 Documentation file identification

Identify documentation files related to migration code:
- `README.md` at repository root
- `CONVENTIONS.md` at repository root

## Step 5 -- Create Branch

The Target Branch is **TC-9005** (the feature branch), NOT `main`. Check out TC-9005, pull latest, and create a task branch named after this task's Jira issue ID (TC-9205):

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

The task branch is named `TC-9205` (this task's issue ID). It branches from `TC-9005` (the feature branch specified in the Target Branch section).

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module that drops the deprecated `status` column from the `advisory` table, following the pattern established in `migration/src/m0001_initial/mod.rs`.

The migration will:

- Import `sea_orm_migration::prelude::*`
- Define a `Migration` unit struct
- Implement `MigrationName` for `Migration`, returning `"m0002_drop_advisory_status"`
- Implement `MigrationTrait` for `Migration` with:
  - `up` method: Uses `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the `status` column
  - `down` method: Re-adds the column via `manager.alter_table(Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null()).to_owned()).await` for rollback
- Define a local `#[derive(Iden)]` enum `Advisory` with `Table` and `Status` variants (self-contained identifiers, following the SeaORM migration pattern where migrations do not import from the entity crate)
- Add module-level and method-level doc comments

### File 2: Modify `migration/src/lib.rs`

Register the new migration module in the migration list:

- Add `mod m0002_drop_advisory_status;` module declaration after `mod m0001_initial;`
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry, maintaining sequential execution order

## Step 7 -- Write Tests

Per the Test Requirements:

- Test that the migration runs successfully against a test database (apply `up`)
- Test that the rollback (`down`) re-adds the column as a nullable string
- Verify that existing advisory queries still work after the column is dropped

Tests will use the existing integration test infrastructure with a real PostgreSQL test database, following patterns in `tests/api/advisory.rs`.

## Step 8 -- Verify Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table -- verified by the `up` method using `drop_column(Advisory::Status)`
- [x] Migration `down` method re-adds the column as nullable string for rollback -- verified by `ColumnDef::new(Advisory::Status).string().null()`
- [x] Migration is registered in `migration/src/lib.rs` -- verified by adding to the `migrations()` vec
- [x] No service or entity code references the `status` column -- verified by inspecting `entity/src/advisory.rs` in Step 4

## Step 9 -- Self-Verification

- **Scope containment**: Run `git diff --name-only` to verify only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` are changed
- **Untracked file check**: Run `git status --short` to check for untracked files in `migration/src/` directory
- **Sensitive-pattern check**: Run grep on staged diff for passwords, API keys, secrets
- **CI checks from CONVENTIONS.md**: Run all CI check commands extracted during Step 4
- **Data-flow trace**: Migration `up` drops column; `down` re-adds it -- both paths complete
- **Contract verification**: `MigrationTrait` requires both `up` and `down` -- both implemented
- **Sibling parity**: New migration matches `m0001_initial` structure (struct + MigrationName + MigrationTrait + Iden enum)
- **Duplication check**: Grep for overlapping migration or column-drop logic elsewhere

## Step 10 -- Commit and Push

Commit using Conventional Commits format with the Assisted-by trailer:

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by
the severity enum field and is no longer referenced by any entity or
service code. The down method re-adds the column as a nullable
string to support rollback.

Implements TC-9205"
```

Push the branch and open a PR targeting the feature branch TC-9005:

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary

- Add m0002_drop_advisory_status migration to drop the deprecated status column from the advisory table
- Register the new migration in migration/src/lib.rs
- The down method re-adds the column as nullable string for rollback

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

The PR targets `--base TC-9005` (the feature branch specified in the Target Branch section), NOT `--base main`.

## Step 11 -- Update Jira

1. Update the Git Pull Request custom field (`customfield_10875`) on TC-9205 with the PR URL (using ADF inlineCard format)
2. Add a Jira comment with PR link, summary of changes, and confirmation of acceptance criteria
3. Transition TC-9205 to "In Review"
