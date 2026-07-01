# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira ID**: TC-9205
**Summary**: Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, NOT main)
**Parent Feature**: TC-9005 (linked via "is incorporated by TC-9005")
**Dependencies**: None

## Branch Operations

### 1. Check out the Target Branch (TC-9005)

The task specifies Target Branch as `TC-9005`. Per Step 5 of the SKILL.md, we check out the target branch first, pull latest, then create the task branch:

```bash
git checkout TC-9005
git pull
```

### 2. Create the Task Branch (TC-9205)

Create a new branch named after this task's Jira issue ID:

```bash
git checkout -b TC-9205
```

The branch name is `TC-9205` (the task ID), NOT `TC-9005` (the feature branch / target branch).

## Pre-Implementation Verification (Step 4)

### Code Understanding

1. **Read `migration/src/m0001_initial/mod.rs`** -- understand the existing migration pattern (MigrationTrait implementation, up/down methods, SeaORM usage)
2. **Read `migration/src/lib.rs`** -- understand how migrations are registered (module declarations, migrations() function, vec pattern)
3. **Read `entity/src/advisory.rs`** -- verify that the `status` column is NOT referenced in the entity definition (confirming the column is deprecated and safe to drop)
4. **Search for `status` references in advisory-related code** -- grep across `modules/fundamental/src/advisory/`, `modules/ingestor/src/graph/advisory/`, and `tests/api/advisory.rs` to confirm no service or entity code references the `status` column
5. **Read `CONVENTIONS.md`** at the repository root for project-level conventions and CI check commands

### Documentation Files Identified

- `README.md` -- repository root documentation
- `CONVENTIONS.md` -- project conventions
- No API documentation files are impacted (this is a database migration, not an API change)

## Files to Create

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the `status` column from the `advisory` table. See `outputs/file-1-description.md` for full details.

## Files to Modify

### File 2: `migration/src/lib.rs`

Register the new migration module in the migration list. See `outputs/file-2-description.md` for full details.

## Acceptance Criteria Verification (Step 8)

1. **Migration drops the `status` column from the `advisory` table** -- Verified by the `up()` method in `m0002_drop_advisory_status/mod.rs` using `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)`
2. **Migration `down` method re-adds the column as nullable string for rollback** -- Verified by the `down()` method using `ColumnDef::new(Advisory::Status).string().null()`
3. **Migration is registered in `migration/src/lib.rs`** -- Verified by adding module declaration and vec entry
4. **No service or entity code references the `status` column** -- Verified by grep search across entity, service, and test files during Step 4

## Self-Verification (Step 9)

### Scope Containment

Run `git diff --name-only` and verify only these files are modified/created:
- `migration/src/m0002_drop_advisory_status/mod.rs` (new file -- in Files to Create)
- `migration/src/lib.rs` (modified -- in Files to Modify)

Any other files would be flagged as out-of-scope.

### Untracked File Check

Run `git status --short` to detect untracked files in the `migration/src/` directory. The new `m0002_drop_advisory_status/mod.rs` file should be staged for commit.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to verify no secrets are present in the migration code.

### Data-Flow Trace

- Migration `up()`: drops column from `advisory` table -- complete (single DDL operation, no data flow beyond schema change)
- Migration `down()`: re-adds column as nullable string -- complete (rollback path, single DDL operation)
- Registration in `lib.rs`: connects migration to the migration runner -- complete

### Contract & Sibling Parity

- **Contract**: `m0002_drop_advisory_status::Migration` implements `MigrationTrait` with both `up()` and `down()` methods -- contract complete
- **Sibling parity with `m0001_initial`**: Both implement `MigrationTrait`, both use `sea_orm_migration::prelude::*`, both follow the same module structure -- parity maintained

### Cross-Module Shared Entity Analysis

- Entity: `advisory` table
- The migration modifies the schema of the `advisory` table, which is used by `modules/fundamental/src/advisory/` and `modules/ingestor/src/graph/advisory/`
- Since we are only dropping a column that is already not referenced by any code (verified in Step 4), no cross-module inconsistencies are introduced

### CI Checks

Run any CI check commands extracted from `CONVENTIONS.md` (e.g., `cargo build`, `cargo clippy`, `cargo fmt --check`). If any fail, fix before proceeding.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

The commit command:

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205"
```

## Push and PR Creation (Step 10)

```bash
git push -u origin TC-9205
```

Create PR targeting the feature branch `TC-9005` (NOT `main`):

```bash
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

- Add migration \`m0002_drop_advisory_status\` that drops the deprecated \`status\` column from the \`advisory\` table
- The column was replaced by the \`severity\` enum field in a prior migration and is no longer read or written by any service code
- Includes rollback support: \`down()\` re-adds the column as a nullable string

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Key points:
- `--base TC-9005` ensures the PR targets the feature branch, not main
- The PR description includes a clickable Jira link using the issue's webUrl
- The commit footer references `TC-9205`
- The commit includes `--trailer="Assisted-by: Claude Code"`

## Jira Updates (Step 11)

1. **Update Git Pull Request custom field** (`customfield_10875`) on TC-9205 with the PR URL in ADF format
2. **Add comment** to TC-9205 with:
   - PR link
   - Summary: Added migration `m0002_drop_advisory_status` to drop the deprecated `status` column from the `advisory` table. Includes rollback support via `down()` method. Migration registered in `lib.rs`.
   - No deviations from the plan.
3. **Transition** TC-9205 to **In Review**
