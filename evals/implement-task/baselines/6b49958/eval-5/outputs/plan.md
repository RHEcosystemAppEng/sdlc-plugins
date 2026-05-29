# Implementation Plan for TC-9205

## Target Branch Extraction

From the task description's **Target Branch** section, the value is **TC-9005**. This is a feature branch (not `main`), indicating that TC-9205 is part of a feature-branch workflow. The task's linked issue ("is incorporated by TC-9005") confirms that TC-9005 is the parent feature. All branch operations and PR targeting must use TC-9005 as the base.

## Branch Operations

```bash
# Step 5: Check out the target branch (TC-9005), NOT main
git checkout TC-9005
git pull

# Create the task branch named after the Jira issue ID (TC-9205)
git checkout -b TC-9205
```

The task branch is **TC-9205** (the task issue ID). The target branch is **TC-9005** (the feature branch). These are distinct: TC-9205 branches off TC-9005, not off main.

## Code Inspection (Step 4)

Before implementing, the following files would be read and analyzed:

1. **`migration/src/m0001_initial/mod.rs`** -- Read this sibling migration file to understand the existing migration pattern: how `MigrationTrait` is implemented, the structure of `up()` and `down()` methods, import conventions, and how SeaORM migration primitives are used. This is the primary convention source.

2. **`migration/src/lib.rs`** -- Read this file to understand how migrations are registered in the `migrations()` function's `vec![]`, what the import style is, and the ordering convention for migration modules.

3. **`entity/src/advisory.rs`** -- Read this file to verify that the `status` column is no longer referenced in the entity definition, confirming it is safe to drop. Search for any `Status` enum variant or field reference in the Advisory entity.

4. **`migration/Cargo.toml`** -- Check for any dependencies or feature flags relevant to migrations.

Additionally, use Grep across the repository to search for any remaining references to `Advisory::Status` or the `status` column in service code, to confirm the acceptance criterion that no code references the column.

## Files to Create

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs`

A new migration module that drops the `status` column from the `advisory` table. The file follows the pattern established in `m0001_initial/mod.rs`:

- Implements `MigrationTrait` with `up()` and `down()` methods
- `up()` uses `TableAlterStatement` to drop the `status` column from the `advisory` table
- `down()` re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback
- Uses the same import structure and naming conventions as the sibling migration

See `outputs/file-1-description.md` for detailed implementation.

## Files to Modify

### File 2: `migration/src/lib.rs`

Register the new migration module by:
- Adding a `mod m0002_drop_advisory_status;` declaration
- Adding `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function

See `outputs/file-2-description.md` for detailed implementation.

## Commit

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Remove the status column that was replaced by the severity enum field
in a previous migration. The column is no longer read or written by
any service code.

Implements TC-9205"
```

## Push and PR Creation

```bash
git push -u origin TC-9205

gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "$(cat <<'EOF'
## Summary
- Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- The `down()` method re-adds the column as a nullable string for safe rollback
- Register the new migration in `migration/src/lib.rs`

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
EOF
)"
```

Key points:
- The PR targets **`--base TC-9005`** (the feature branch), NOT `--base main`
- The branch pushed is TC-9205 (the task branch)
- The commit message follows Conventional Commits with `Implements TC-9205` in the footer
- The commit includes `--trailer='Assisted-by: Claude Code'`

## Jira Updates (Step 11)

1. Update the Git Pull Request custom field (`customfield_10875`) on TC-9205 with the PR URL in ADF format
2. Add a comment to TC-9205 summarizing the changes and linking the PR
3. Transition TC-9205 to **In Review**

## Self-Verification Checklist

- [ ] Scope containment: only `migration/src/m0002_drop_advisory_status/mod.rs` (created) and `migration/src/lib.rs` (modified) are changed -- matches Files to Create and Files to Modify
- [ ] No references to `Advisory::Status` or `status` column remain in entity or service code
- [ ] Migration `up()` drops the column
- [ ] Migration `down()` re-adds the column as nullable string
- [ ] Migration is registered in lib.rs
- [ ] Commit message references TC-9205
- [ ] PR targets TC-9005 (the feature branch)
