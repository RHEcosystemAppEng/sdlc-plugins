# Implementation Plan: TC-9205 — Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Branch Operations

1. **Checkout the target branch** (TC-9005 is a feature branch, not main):
   ```
   git checkout TC-9005
   git pull
   ```
2. **Create the task branch** from the feature branch:
   ```
   git checkout -b TC-9205
   ```
3. **After implementation, push and open PR targeting the feature branch**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```

The PR targets `TC-9005` (the feature branch), not `main`, because the task's Target Branch field specifies `TC-9005`.

## Files to Modify

| # | File | Action | Description |
|---|------|--------|-------------|
| 1 | `migration/src/lib.rs` | Modify | Register the new migration module `m0002_drop_advisory_status` in the migration list |

## Files to Create

| # | File | Action | Description |
|---|------|--------|-------------|
| 2 | `migration/src/m0002_drop_advisory_status/mod.rs` | Create | Migration that drops the `status` column from the `advisory` table with rollback support |

## Pre-Implementation Verification

Before implementing, verify that the `advisory` entity in `entity/src/advisory.rs` no longer references the `status` column, as stated in the Implementation Notes. Use Serena (`mcp__serena_backend__get_symbols_overview`) or Read to inspect the entity file.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the `status`
column from the `advisory` table. The column was replaced by the
`severity` enum field and is no longer referenced by any service or
entity code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

The commit would include `--trailer="Assisted-by: Claude Code"`.

## PR Description

```
## Summary

- Add migration `m0002_drop_advisory_status` to drop the deprecated `status` column from the `advisory` table
- The `down` method re-adds the column as a nullable string for rollback support
- Migration registered in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

The PR targets branch `TC-9005` (the parent feature branch).

## Jira Updates

1. Transition TC-9205 to **In Progress** at start
2. Assign to current user
3. After PR creation:
   - Set Git Pull Request custom field (`customfield_10875`) to the PR URL (using ADF inlineCard format)
   - Add comment with PR link, summary of changes
   - Transition TC-9205 to **In Review**

## Acceptance Criteria Verification

- [x] Migration drops the `status` column from the `advisory` table (implemented in `up` method)
- [x] Migration `down` method re-adds the column as nullable string for rollback (implemented in `down` method)
- [x] Migration is registered in `migration/src/lib.rs` (added to `vec![]` in `migrations()`)
- [x] No service or entity code references the `status` column (verified in pre-implementation step)

## Test Verification

Tests would be run with `cargo test` to verify:
- The migration runs successfully against a test database
- The rollback (down) re-adds the column
- Existing advisory queries still work after the column is dropped
