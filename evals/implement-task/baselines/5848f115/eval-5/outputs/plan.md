# Implementation Plan for TC-9205

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, extracted from the Target Branch section of the task description)
**Linked Issues**: is incorporated by TC-9005
**Dependencies**: None

## Target Branch Extraction

The task description contains a **Target Branch** section with the value `TC-9005`. This indicates a feature-branch workflow: TC-9205 is a sub-task of the feature TC-9005, and all work must branch from and target that feature branch -- not `main`.

## Branch Operations

### 1. Check out the target branch (TC-9005) and create the task branch

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

The task branch is named `TC-9205` (the task issue ID), branching from `TC-9005` (the feature branch). We do NOT checkout `main` -- we branch from the feature branch TC-9005 because that is where this work belongs.

### 2. Push and open PR targeting the feature branch

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

The PR targets `--base TC-9005` (the feature branch), not `--base main`. This ensures the migration is incorporated into the feature branch alongside other TC-9005 tasks before the feature branch itself is merged to main.

## Code Inspection (Step 4)

Before making any changes, inspect the following files to understand existing patterns:

1. **Read `migration/src/m0001_initial/mod.rs`** -- Examine the existing migration to understand the `MigrationTrait` implementation pattern, including `up` and `down` methods, naming conventions, and SeaORM usage. This is the sibling file referenced in the Implementation Notes.

2. **Read `migration/src/lib.rs`** -- Understand how migrations are registered in the `migrations()` function, specifically the `vec![]` pattern and module imports.

3. **Read `entity/src/advisory.rs`** -- Verify that the `status` column is no longer referenced in the Advisory entity. The task description states this but we must confirm before proceeding.

4. **Search for `status` references** -- Grep across the codebase for any remaining references to `Advisory::Status` or the `status` column on the advisory table to ensure no service or query code still depends on it.

5. **Check for `CONVENTIONS.md`** -- Read `CONVENTIONS.md` at the repository root and extract any CI check commands and coding conventions.

## Files to Modify

### 1. `migration/src/lib.rs`
- Register the new migration module `m0002_drop_advisory_status`
- Add a `mod m0002_drop_advisory_status;` declaration
- Add the migration to the `vec![]` in the `migrations()` function, following the same pattern used for `m0001_initial`

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`
- Implement `MigrationTrait` with:
  - `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
  - `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback
- Follow the exact pattern from `m0001_initial/mod.rs`

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the `status`
column from the `advisory` table. The column was replaced by the
`severity` enum field and is no longer referenced by any entity or
service code.

Implements TC-9205
```

With the trailer flag:

```bash
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the status
column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any entity or
service code.

Implements TC-9205"
```

## PR Details

**Title**: feat(migration): add migration to drop advisory status column

**Base branch**: TC-9005

**Description**:
```
## Summary

Add database migration `m0002_drop_advisory_status` that drops the deprecated `status`
column from the `advisory` table. The column was replaced by the `severity` enum field
in a previous migration and is no longer read or written by any service code.

- New migration file: `migration/src/m0002_drop_advisory_status/mod.rs`
- Updated migration registry: `migration/src/lib.rs`
- Rollback supported: `down` method re-adds the column as a nullable string

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

## Verification Steps

1. Run `cargo test` to ensure all existing tests pass
2. Verify the migration runs against a test database
3. Verify rollback (down) re-adds the column
4. Verify existing advisory queries still work after column drop
5. Run scope containment check: `git diff --name-only` should only show `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`
6. Run sensitive-pattern check on the staged diff
7. Run CI checks from CONVENTIONS.md if present

## Jira Updates

1. Transition TC-9205 to In Progress (Step 3)
2. After PR creation: update `customfield_10875` with the PR URL
3. Add implementation comment to TC-9205 with PR link and summary
4. Transition TC-9205 to In Review
