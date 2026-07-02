# Implementation Plan for TC-9205

## Task Summary

**Key**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch -- extracted from the Target Branch section of the task description)
**Dependencies**: None

## Branch Operations

The Target Branch section specifies `TC-9005`, which is a feature branch (not main). Per the skill's Step 5 default flow, the branch operations are:

1. Check out the target branch and pull latest:
   ```
   git checkout TC-9005
   git pull
   ```

2. Create the task branch named after this task's Jira issue ID (TC-9205, distinct from the target branch TC-9005):
   ```
   git checkout -b TC-9205
   ```

The task branch is `TC-9205`. The target (base) branch is `TC-9005`.

## Pre-Implementation Inspection

Before making changes, inspect existing code to understand patterns and verify assumptions:

1. **`migration/src/m0001_initial/mod.rs`** -- Read this file to understand the existing migration pattern: how `MigrationTrait` is implemented, the structure of `up` and `down` methods, how SeaORM's `TableAlterStatement` and `TableCreateStatement` are used, and what imports are needed.

2. **`entity/src/advisory.rs`** -- Verify that the `status` column is no longer referenced in the Advisory entity definition. The task description states the column was replaced by `severity` in a previous migration and is no longer read or written. This must be confirmed before proceeding.

3. **`migration/src/lib.rs`** -- Read this file to understand how migrations are registered. Look at the `migrations()` function and the `vec![]` pattern to see how `m0001_initial` is included, so the new migration can be registered in the same way.

Additional inspection:
- Grep for any remaining references to `Advisory::Status` or the `status` column across the codebase to confirm nothing still depends on it.
- Check `CONVENTIONS.md` at the repository root for CI check commands and coding conventions.

## Files to Modify

### 1. `migration/src/lib.rs`
- Register the new migration module `m0002_drop_advisory_status` in the migration list.
- Add a `mod m0002_drop_advisory_status;` declaration alongside the existing `mod m0001_initial;`.
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the existing `m0001_initial` entry.

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
- Implement `MigrationTrait` with `up` and `down` methods.
- `up`: Drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`.
- `down`: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback.
- Follow the exact pattern from `migration/src/m0001_initial/mod.rs` for structure, imports, and naming.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Remove the `status` column from the `advisory` table via a new migration.
The column was replaced by the `severity` enum field in a previous migration
and is no longer referenced by any service or entity code.

Implements TC-9205
```

The commit command:
```
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Remove the status column from the advisory table via a new migration.
The column was replaced by the severity enum field in a previous migration
and is no longer referenced by any service or entity code.

Implements TC-9205"
```

## Push and PR

Push the branch and open a PR targeting the feature branch TC-9005 (not main):

```
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

Add a database migration that drops the deprecated \`status\` column from the \`advisory\` table. The column was replaced by the \`severity\` enum field and is no longer read or written by any service code.

- New migration \`m0002_drop_advisory_status\` with up (drop column) and down (re-add as nullable string) methods
- Migration registered in \`migration/src/lib.rs\`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test Plan

- [ ] Migration runs successfully against test database
- [ ] Rollback (down) re-adds the column as nullable string
- [ ] Existing advisory queries continue to work after column removal
"
```

Note: `--base TC-9005` ensures the PR targets the feature branch, not main.

## Jira Updates

After PR creation:
1. Update custom field `customfield_10875` with the PR URL (ADF format with inlineCard).
2. Add a Jira comment summarizing the changes and linking the PR.
3. Transition TC-9205 to "In Review".

## Acceptance Criteria Verification

- [x] Migration drops the `status` column from the `advisory` table -- implemented in `up` method
- [x] Migration `down` method re-adds the column as nullable string for rollback -- implemented in `down` method
- [x] Migration is registered in `migration/src/lib.rs` -- added to `migrations()` vec
- [x] No service or entity code references the `status` column -- verified by inspecting `entity/src/advisory.rs` and grepping codebase
