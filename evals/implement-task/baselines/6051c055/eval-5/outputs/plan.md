# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

- **Key:** TC-9205
- **Summary:** Add migration to drop status table column
- **Repository:** trustify-backend
- **Linked Issues:** is incorporated by TC-9005

## Target Branch Extraction

The task description includes a **Target Branch** section with the value `TC-9005`. This
identifies TC-9005 as the feature branch that this task's PR must target. This is NOT main --
TC-9005 is a feature branch created for the parent feature, and all tasks incorporated by
TC-9005 must branch from and merge back into that feature branch.

## Branch Operations

### 1. Check out the target branch (TC-9005)

```bash
git checkout TC-9005
git pull
```

The target branch is TC-9005 (the feature branch), NOT main. The skill extracts the Target
Branch value from the task description and uses it as the base for the new task branch.

### 2. Create the task branch (TC-9205)

```bash
git checkout -b TC-9205
```

The task branch is named after the Jira task issue ID (TC-9205), which is distinct from
the target branch (TC-9005). This follows the convention that task branches are named
after the Jira task issue ID.

### 3. Open PR targeting TC-9005

After implementation and commit, push and open a PR with `--base TC-9005`:

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "$(cat <<'EOF'
## Summary
- Add m0002_drop_advisory_status migration that drops the deprecated status column from the advisory table
- Register the new migration module in migration/src/lib.rs

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
EOF
)"
```

The `--base TC-9005` ensures the PR targets the feature branch, not main.

## Code Inspection (Step 4)

Before making any changes, inspect the following existing files to understand patterns and
confirm assumptions from the task description:

1. **`migration/src/m0001_initial/mod.rs`** -- Inspect this file to understand the existing
   migration pattern. This is referenced in the Implementation Notes as the pattern to follow.
   Look for the `MigrationTrait` implementation, the `up()` and `down()` method signatures,
   and how SeaORM's schema alteration API is used.

2. **`entity/src/advisory.rs`** -- Verify that the advisory entity no longer references the
   `status` column. The task description states this was already removed in a prior migration,
   and we must confirm before proceeding to avoid breaking entity-column alignment.

3. **`migration/src/lib.rs`** -- Inspect to understand how migrations are registered. Look
   for the `migrations()` function and the `vec![]` that lists all migration modules. The new
   migration module must be added to this list.

Additionally, inspect 2-3 sibling migration files (if they exist beyond m0001_initial) to
discover conventions for naming, structure, and error handling patterns.

## Files to Modify

1. **`migration/src/lib.rs`** -- Register the new migration module `m0002_drop_advisory_status`
   in the migration list.

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** -- New migration that drops the
   `status` column from the advisory table using SeaORM's `TableAlterStatement`.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Remove the status column from the advisory table. The column was replaced
by the severity enum field in a previous migration and is no longer
referenced by any entity or service code.

Implements TC-9205
```

With the trailer flag:

```bash
git commit --trailer='Assisted-by: Claude Code' -m "$(cat <<'EOF'
feat(migration): drop deprecated status column from advisory table

Remove the status column from the advisory table. The column was replaced
by the severity enum field in a previous migration and is no longer
referenced by any entity or service code.

Implements TC-9205
EOF
)"
```

The commit message follows Conventional Commits format with:
- **Type:** `feat` (new migration capability)
- **Scope:** `migration`
- **Footer:** `Implements TC-9205` referencing the Jira task issue ID
- **Trailer:** `Assisted-by: Claude Code` added via `--trailer` flag

## Verification Steps

1. Run `cargo test` to verify the migration compiles and existing tests pass.
2. Verify acceptance criteria:
   - Migration drops the status column from the advisory table (check `up()` method)
   - Migration down method re-adds the column as nullable string (check `down()` method)
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the status column (grep for `status` in entity/service code)
3. Run `git diff --name-only` to verify scope containment -- only the two expected files should appear.
4. Run sensitive-pattern check on staged diff.
