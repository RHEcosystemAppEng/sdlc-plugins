# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue:** TC-9205
**Summary:** Add a database migration that drops the deprecated `status` column from the `advisory` table
**Repository:** trustify-backend
**Target Branch:** TC-9005 (feature branch, linked via "is incorporated by TC-9005")
**Bookend Type:** None
**Target PR:** None

## Target Branch Extraction

The task description contains a **Target Branch** section with value `TC-9005`. This is a feature branch (not `main`), indicating this task is part of a feature-branch workflow. The parent feature issue is TC-9005. All branch operations and PR targeting must use TC-9005 as the base.

## Pre-Implementation Inspection

Before making any changes, inspect the following existing files to understand current patterns and confirm assumptions:

1. **`migration/src/m0001_initial/mod.rs`** -- Inspect to understand the existing migration pattern: how `MigrationTrait` is implemented, the structure of `up` and `down` methods, and how SeaORM schema operations are used. This serves as the template for the new migration.

2. **`entity/src/advisory.rs`** -- Verify that the `status` column is no longer referenced in the entity definition. The task description states the column was replaced by the `severity` enum field. Confirm no `Status` variant exists in the `Column` enum or `ActiveModel`.

3. **`migration/src/lib.rs`** -- Inspect to understand how migrations are registered: the module declaration pattern and the `vec![]` in the `migrations()` function where the new migration must be added.

4. **`CONVENTIONS.md`** -- Check for any project-level conventions, CI check commands, or code generation commands that must be followed.

## Branch Operations

### Step 1: Check out the target branch (TC-9005)
```bash
git checkout TC-9005
git pull
```

### Step 2: Create the task branch from TC-9005
```bash
git checkout -b TC-9205
```

This creates branch `TC-9205` (named after the task issue ID) from the feature branch `TC-9005`. The task branch TC-9205 is distinct from the target branch TC-9005.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`
- New migration module that drops the `status` column from the `advisory` table
- Implements `MigrationTrait` with:
  - `up` method: uses `TableAlterStatement` to drop the `status` column via `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
  - `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback capability
- Follows the exact pattern established in `m0001_initial/mod.rs`
- See `outputs/file-1-description.md` for detailed implementation

## Files to Modify

### 2. `migration/src/lib.rs`
- Add `mod m0002_drop_advisory_status;` module declaration
- Add the new migration to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`
- See `outputs/file-2-description.md` for detailed changes

## Files to Verify (read-only, no modifications)

### 3. `entity/src/advisory.rs`
- Confirm that the `status` column is no longer referenced
- Verify that no `Status` variant exists in the entity's `Column` enum
- This validates the task's precondition that the column is safe to drop

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002 that removes the `status` column from the `advisory`
table. The column was replaced by the `severity` enum field in a previous
migration and is no longer read or written by any service code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

With trailer: `--trailer='Assisted-by: Claude Code'`

## PR Creation

Create a pull request targeting the feature branch TC-9005 (NOT main):

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

- Add migration m0002 to drop the deprecated \`status\` column from the \`advisory\` table
- The column was replaced by the \`severity\` enum field and is no longer used
- Includes rollback support (down method re-adds the column as nullable string)

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Test that the migration runs successfully against a test database
- [ ] Test that the rollback (down) re-adds the column
- [ ] Verify that existing advisory queries still work after the column is dropped
"
```

Key points:
- `--base TC-9005` ensures the PR targets the feature branch, not main
- The PR description includes a clickable Jira link using the issue's webUrl
- The task branch `TC-9205` is pushed as the head branch

## Jira Updates

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9205 with the PR URL in ADF format
2. **Add comment** to TC-9205 with PR link, summary of changes, and confirmation that no deviations from the plan occurred
3. **Transition** TC-9205 to "In Review"

## Acceptance Criteria Verification

- [x] Migration drops the `status` column from the `advisory` table -- implemented in `m0002_drop_advisory_status/mod.rs` `up` method
- [x] Migration `down` method re-adds the column as nullable string for rollback -- implemented in `down` method with `ColumnDef::new(Advisory::Status).string().null()`
- [x] Migration is registered in `migration/src/lib.rs` -- added to module declarations and `migrations()` vec
- [x] No service or entity code references the `status` column -- verified by inspecting `entity/src/advisory.rs`

## Self-Verification Checklist

- **Scope containment:** Only `migration/src/lib.rs` (modify) and `migration/src/m0002_drop_advisory_status/mod.rs` (create) are changed, matching the task's Files to Modify and Files to Create sections
- **Sensitive-pattern check:** No passwords, API keys, or secrets in the migration code
- **Data-flow trace:** Migration up drops column -> migration down restores column -- complete lifecycle
- **Contract verification:** `MigrationTrait` requires `up` and `down` methods -- both implemented
- **Sibling parity:** Follows same pattern as `m0001_initial/mod.rs`
- **Duplication check:** No existing migration performs the same operation
