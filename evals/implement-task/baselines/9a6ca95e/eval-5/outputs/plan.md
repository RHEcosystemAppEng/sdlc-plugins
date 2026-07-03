# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Target Branch Extraction

The task description specifies **Target Branch: TC-9005**. This is a feature branch (not main), indicating the feature-branch workflow. All branch operations and PR targeting must use TC-9005 as the base.

## Step 4 -- Understand the Code (Pre-Implementation Inspection)

Before making any changes, inspect existing code using the Serena instance `serena_backend` (from the Repository Registry in CLAUDE.md):

1. **Inspect the existing migration pattern**: Read `migration/src/m0001_initial/mod.rs` to understand the `MigrationTrait` implementation pattern, including the `up` and `down` method signatures, how `TableAlterStatement` and `TableCreateStatement` are used, and the import structure.

2. **Verify the advisory entity**: Read `entity/src/advisory.rs` to confirm that the `status` column is no longer referenced in the entity definition. Verify that only the `severity` field is present, confirming safe removal of the column.

3. **Inspect migration registration**: Read `migration/src/lib.rs` to understand how migrations are registered in the `migrations()` function's `vec![]`, and confirm the pattern for adding new migration modules (module declaration and vector entry).

4. **Check for CONVENTIONS.md**: Look for `CONVENTIONS.md` at the repository root. If present, read it and extract any CI check commands and coding conventions.

5. **Search for remaining status column references**: Use `search_for_pattern` or Grep across the codebase for any remaining references to `Advisory::Status` or the `status` column on the advisory table to ensure no service code still depends on it.

6. **Sibling analysis**: Examine `migration/src/m0001_initial/mod.rs` as the sibling migration to discover conventions for migration file structure, naming, imports, and documentation.

7. **Test sibling analysis**: Examine `tests/api/advisory.rs` to understand test patterns for advisory-related functionality, including assertion style, test naming, and database setup.

## Branch Operations

```
git checkout TC-9005
git pull
git checkout -b TC-9205
```

- Check out the feature branch **TC-9005** (the Target Branch from the task description)
- Pull latest changes on that branch
- Create a new task branch named **TC-9205** (the Jira issue ID for this task)

## Files to Modify

### 1. `migration/src/lib.rs`

Register the new migration module `m0002_drop_advisory_status` in the migration list. This involves:
- Adding a `mod m0002_drop_advisory_status;` declaration
- Adding `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the existing pattern of `m0001_initial`

See `outputs/file-1-description.md` for detailed changes.

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module that implements `MigrationTrait` with:
- `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down` method: re-adds the `status` column as a nullable string for rollback

See `outputs/file-2-description.md` for detailed changes.

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that drops the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field and is no longer referenced by any service
or entity code.

Implements TC-9205
```

With flag: `--trailer="Assisted-by: Claude Code"`

## PR Creation

```
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

The PR targets **--base TC-9005** (the feature branch), not main. The PR description includes:
- Summary of changes
- Link to Jira issue: `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)`
- Acceptance criteria checklist

## Verification Steps

Before committing:
- Run `cargo test` to verify the migration compiles and tests pass
- Run `git diff --name-only` to confirm only in-scope files were changed
- Check `git status --short` for untracked files in the migration directory
- Run scope containment check against Files to Modify and Files to Create
- Run sensitive-pattern check on staged diff
- Verify acceptance criteria:
  - Migration drops the `status` column from the `advisory` table
  - Migration `down` method re-adds the column as nullable string for rollback
  - Migration is registered in `migration/src/lib.rs`
  - No service or entity code references the `status` column

## Jira Updates (Post-Implementation)

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL
2. Add comment to TC-9205 with PR link, summary of changes, and any deviations
3. Transition TC-9205 to In Review
