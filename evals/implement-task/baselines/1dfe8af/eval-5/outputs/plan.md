# Implementation Plan for TC-9205

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, linked via "is incorporated by TC-9005")
**Bookend Type**: None (standard implementation task)
**Target PR**: None (new branch and PR)
**Dependencies**: None

## Target Branch Analysis

The task description contains a **Target Branch** section with value `TC-9005`. This means:

- TC-9205 is part of a feature-branch workflow under feature TC-9005
- The task branch must be created FROM TC-9005, not from main
- The PR must target TC-9005 as its base branch, not main

## Branch Operations

### Step 1: Check out the target branch (TC-9005)

```bash
git checkout TC-9005
git pull
```

This checks out the **feature branch** TC-9005, NOT main. The Target Branch field explicitly specifies TC-9005 as the base.

### Step 2: Create the task branch

```bash
git checkout -b TC-9205
```

The task branch is named after the Jira issue ID (TC-9205), which is distinct from the feature branch (TC-9005).

### Step 3: After implementation, push and open PR targeting TC-9005

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --head TC-9205 --title "feat(migration): add migration to drop advisory status column" --body "## Summary
- Add migration m0002_drop_advisory_status that drops the deprecated status column from the advisory table
- Register the new migration in migration/src/lib.rs
- Migration includes rollback support (down method re-adds column as nullable string)

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Note: `--base TC-9005` is critical. This ensures the PR targets the feature branch, not main.

## Files to Modify

1. **`migration/src/lib.rs`** -- Register the new migration module in the migration list

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** -- Migration that drops the `status` column from the `advisory` table

## Pre-Implementation Inspection (Step 4)

Before making any changes, inspect the following files using the Serena instance `serena_backend` (from the Repository Registry):

1. **`migration/src/lib.rs`** -- Use `get_symbols_overview` to understand the current migration registration pattern
2. **`migration/src/m0001_initial/mod.rs`** -- Use `get_symbols_overview` and `find_symbol` with `include_body=true` to read the `MigrationTrait` implementation and understand the pattern for `up` and `down` methods
3. **`entity/src/advisory.rs`** -- Use `get_symbols_overview` to verify the Advisory entity no longer references the `status` column (as stated in Implementation Notes)
4. **Sibling analysis**: Examine m0001_initial/mod.rs as the sibling migration to discover conventions
5. **CONVENTIONS.md**: Check for `./CONVENTIONS.md` at the repository root (listed in the repo structure)
6. **Documentation files**: Check README.md at the repo root for any migration-related documentation

Additionally, search for any remaining references to the `status` column in advisory-related code:
- Use `search_for_pattern` on the serena_backend instance to search for `Advisory::Status` or `status` in advisory service/model/endpoint files
- Verify no service or entity code still references the column

## Implementation Details

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

Create a new migration module following the pattern in `m0001_initial/mod.rs`:

- Implement `MigrationTrait` with `up` and `down` methods
- `up` method: Use `TableAlterStatement` to drop the `status` column from the `advisory` table
  - `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down` method: Re-add the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback
- Include proper documentation comments on the struct and trait implementation
- Follow naming and import conventions from m0001_initial

### File 2: `migration/src/lib.rs` (MODIFY)

- Add `mod m0002_drop_advisory_status;` module declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the pattern of m0001_initial

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any service code.

Implements TC-9205
```

With the trailer flag:
```bash
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any service code.

Implements TC-9205"
```

## PR Details

- **Title**: `feat(migration): add migration to drop advisory status column`
- **Base branch**: `TC-9005` (the feature branch -- NOT main)
- **Head branch**: `TC-9205` (the task branch)
- **Description**:
  ```
  ## Summary
  - Add migration m0002_drop_advisory_status that drops the deprecated status column from the advisory table
  - Register the new migration in migration/src/lib.rs
  - Migration includes rollback support (down method re-adds column as nullable string)

  ## Jira
  Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
  ```

## Jira Updates (Step 11)

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format
2. Add comment to TC-9205 with PR link and summary of changes
3. Transition TC-9205 to "In Review"

## Verification Steps (Step 9)

1. **Scope containment**: Verify only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` are changed
2. **Sensitive pattern check**: Scan staged diff for secrets/credentials
3. **Data-flow trace**: Migration up drops column, down re-adds it -- complete lifecycle
4. **Contract verification**: Verify MigrationTrait is fully implemented (up + down methods)
5. **Sibling parity**: Verify m0002 follows the same patterns as m0001
6. **CI checks**: Run any CI commands from CONVENTIONS.md, or fall back to `cargo test` and `cargo check`
