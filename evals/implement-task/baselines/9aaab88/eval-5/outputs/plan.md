# Implementation Plan for TC-9205

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table in the trustify-backend repository.

## Branch Operations

1. **Checkout the target (feature) branch:**
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch from the feature branch:**
   ```
   git checkout -b TC-9205
   ```

The task branch `TC-9205` is based on the feature branch `TC-9005`, NOT on `main`. The Target Branch field in the task description explicitly specifies `TC-9005`.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the `status` column from the `advisory` table. Follows the existing migration pattern in `migration/src/m0001_initial/mod.rs` by implementing `MigrationTrait` with `up` and `down` methods.

See `outputs/file-1-description.md` for detailed changes.

## Files to Modify

### 2. `migration/src/lib.rs`

Register the new migration module `m0002_drop_advisory_status` in the migration list by adding it to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`.

See `outputs/file-2-description.md` for detailed changes.

## Verification Steps

1. Confirm that `entity/src/advisory.rs` does not reference the `status` column (as stated in Implementation Notes).
2. Grep across service code to ensure no references to the `status` column exist anywhere.
3. Run `cargo build` to ensure compilation succeeds.
4. Run migration tests (`cargo test`) to verify the migration runs and rolls back correctly.
5. Verify acceptance criteria:
   - Migration drops the `status` column from the `advisory` table
   - Migration `down` method re-adds the column as nullable string for rollback
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the `status` column

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the `status` column
from the `advisory` table. The column was replaced by the `severity` enum
field in a previous migration and is no longer referenced by any service
or entity code.

The down method re-adds the column as a nullable string to allow rollback.

Implements TC-9205
```

The commit will include the `--trailer="Assisted-by: Claude Code"` flag.

## PR Creation

The PR targets the feature branch `TC-9005`, NOT `main`:

```
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
```

The PR description will include:
- Summary of changes
- Link to Jira task: `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)`
- The `--base TC-9005` flag to target the feature branch

## Jira Updates (would be performed)

1. Transition TC-9205 to "In Progress" at start
2. Assign to current user
3. After PR creation: update `customfield_10875` (Git Pull Request) with PR URL
4. Add comment with PR link and summary of changes
5. Transition TC-9205 to "In Review"
