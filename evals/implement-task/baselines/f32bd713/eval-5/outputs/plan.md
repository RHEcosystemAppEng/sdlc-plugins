# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Branch Operations

1. **Checkout the target branch (feature branch TC-9005)**:
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch from TC-9005**:
   ```
   git checkout -b TC-9205
   ```

   The task branch `TC-9205` is created from the feature branch `TC-9005`, NOT from `main`. This is because the task's Target Branch is `TC-9005`.

## Pre-Implementation Verification

Before implementing, verify that:
- The `advisory` entity in `entity/src/advisory.rs` does NOT reference a `status` column (confirming it was already removed from the entity model)
- The existing migration pattern in `migration/src/m0001_initial/mod.rs` is understood for structural reference
- No service or endpoint code references `Advisory::Status` or a `status` field on advisories (search `modules/fundamental/src/advisory/`, `modules/ingestor/src/graph/advisory/`, and `entity/src/advisory.rs`)
- Check for `CONVENTIONS.md` at the repository root and read it if present

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`
- New migration module implementing `MigrationTrait`
- `up` method: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback capability
- Follows the exact pattern from `m0001_initial/mod.rs`

## Files to Modify

### 2. `migration/src/lib.rs`
- Register the new migration module `m0002_drop_advisory_status` in the module declarations
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the `m0001_initial` entry

## Files NOT Modified (scope containment)

The following files are explicitly out of scope:
- `entity/src/advisory.rs` -- The task states the entity already does NOT reference the `status` column; verify but do not modify
- Service/endpoint code in `modules/` -- No changes needed since the column is already unused
- Test files in `tests/api/` -- The Test Requirements mention testing the migration, but the task's Files to Modify/Create sections do not list test files; migration testing would be done via `cargo test -p migration` against existing test infrastructure

## Post-Implementation Verification

1. **Scope containment**: Run `git diff --name-only` and confirm only `migration/src/lib.rs` is modified and `migration/src/m0002_drop_advisory_status/mod.rs` is created
2. **Entity verification**: Confirm `entity/src/advisory.rs` has no `status` column reference
3. **Service code verification**: Grep for `status` references in advisory-related modules to confirm no code depends on the dropped column
4. **Acceptance Criteria check**:
   - Migration drops the `status` column from the `advisory` table
   - Migration `down` method re-adds the column as nullable string for rollback
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the `status` column
5. **CI checks**: If `CONVENTIONS.md` has CI check commands, run them; otherwise run `cargo check` and `cargo test -p migration` (per the Rust module-level test requirement)
6. **Data-flow trace**: Input: migration runner invokes `up()` -> Processing: `TableAlterStatement` drops column -> Output: `advisory` table no longer has `status` column. Rollback: `down()` re-adds nullable string column.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002 that removes the `status` column from the `advisory`
table. The column was replaced by the `severity` enum field in a previous
migration and is no longer referenced by any entity or service code.
The down method re-adds the column as a nullable string to support rollback.

Implements TC-9205

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

With `--trailer="Assisted-by: Claude Code"` flag on the git commit command.

## PR Creation

```
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "$(cat <<'EOF'
## Summary

- Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- The `down` method re-adds the column as a nullable string for rollback support
- Register the new migration in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Run `cargo test -p migration` to verify migration runs successfully
- [ ] Verify rollback (down) re-adds the column
- [ ] Confirm existing advisory queries still work after the column is dropped
EOF
)"
```

Key points:
- The PR targets `--base TC-9005` (the feature branch), NOT `main`
- The branch `TC-9205` was created from `TC-9005`
- Fork detection would be performed first (`git remote get-url upstream 2>/dev/null`) and if a fork is detected, appropriate `-R` and `--head` flags would be added

## Jira Updates

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL
2. Add comment to TC-9205 with PR link, summary of changes, and any deviations
3. Transition TC-9205 to "In Review"
