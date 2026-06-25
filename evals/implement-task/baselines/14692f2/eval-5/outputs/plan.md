# Implementation Plan for TC-9205

## Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer referenced by any service or entity code.

## Branch Operations

1. **Checkout the target branch** (feature branch, not main):
   ```
   git checkout TC-9005
   git pull
   ```
2. **Create the task branch** from the feature branch:
   ```
   git checkout -b TC-9205
   ```
3. After implementation, **push and open a PR targeting the feature branch**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
   ```

The PR targets `TC-9005` (the feature branch), NOT `main`. This is because the task's Target Branch is `TC-9005`.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the `status` column from the `advisory` table. Details in `outputs/file-1-description.md`.

## Files to Modify

### 2. `migration/src/lib.rs`

Register the new migration module `m0002_drop_advisory_status` in the migration list. Details in `outputs/file-2-description.md`.

## Pre-Implementation Verification

Before implementing:
- Verify that `entity/src/advisory.rs` does NOT reference a `status` column (confirming it was already removed from the entity definition).
- Read `migration/src/m0001_initial/mod.rs` to understand the existing migration pattern (MigrationTrait implementation, up/down methods, SeaORM table alter statements).
- Check `CONVENTIONS.md` at the repository root for CI check commands and code conventions.
- Identify sibling migration files for convention conformance analysis.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

The status column on the advisory table was replaced by the severity enum
field in a previous migration and is no longer read or written by any
service code. This migration removes it to reduce confusion and prevent
accidental usage.

Implements TC-9205
```

With `--trailer="Assisted-by: Claude Code"`.

## PR Description

```markdown
## Summary

- Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- Register the new migration in `migration/src/lib.rs`
- The `down` method re-adds the column as a nullable string for rollback support

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

The PR is created with `--base TC-9005` to target the feature branch.

## Testing Strategy

- Test that the migration runs successfully against a test database (up migration)
- Test that the rollback (down) re-adds the column as a nullable string
- Verify that existing advisory queries still work after the column is dropped

## Acceptance Criteria Verification

1. Migration drops the `status` column from the `advisory` table -- verified by the `up` method implementation using `TableAlterStatement::drop_column`
2. Migration `down` method re-adds the column as nullable string for rollback -- verified by the `down` method using `ColumnDef::new(Advisory::Status).string().null()`
3. Migration is registered in `migration/src/lib.rs` -- verified by adding the module to the `vec![]` in the `migrations()` function
4. No service or entity code references the `status` column -- verified by grepping the codebase for references to `Advisory::Status` or `status` column usage in advisory-related code
