# Implementation Plan for TC-9205

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch)
**Linked Issues**: is incorporated by TC-9005
**Status**: To Do

## Branch Operations

1. **Checkout the target branch** (TC-9005, a feature branch — not main):
   ```
   git checkout TC-9005
   git pull
   ```
2. **Create the task branch** named after the Jira issue ID:
   ```
   git checkout -b TC-9205
   ```
3. After implementation, **push and open PR targeting TC-9005**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
   ```

The PR base branch is TC-9005 (the feature branch), not main, because that is the value in the Target Branch section.

## Files to Create

| # | File | Action |
|---|------|--------|
| 1 | `migration/src/m0002_drop_advisory_status/mod.rs` | Create |

## Files to Modify

| # | File | Action |
|---|------|--------|
| 2 | `migration/src/lib.rs` | Modify |

## Pre-Implementation Verification

Before making changes, the following verifications would be performed:

1. **Verify entity/src/advisory.rs** does not reference a `status` column — confirming the column is indeed deprecated and safe to drop.
2. **Search across all service and endpoint code** (Grep for `Status` or `status` referencing the advisory entity) to confirm no code reads or writes this column.
3. **Inspect migration/src/m0001_initial/mod.rs** to understand the existing migration pattern (MigrationTrait implementation, `up`/`down` method signatures, use of SeaORM manager).
4. **Check CONVENTIONS.md** at the repository root for any project-specific conventions, CI check commands, or migration-specific rules.

## Implementation Steps

### Step 1: Create migration/src/m0002_drop_advisory_status/mod.rs

Create a new SeaORM migration module that:
- Implements `MigrationTrait` with `up` and `down` methods
- `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down` method: re-adds the `status` column as a nullable string for rollback

See `outputs/file-1-description.md` for full details.

### Step 2: Modify migration/src/lib.rs

Register the new migration module `m0002_drop_advisory_status` in the migrations list:
- Add a `mod m0002_drop_advisory_status;` declaration
- Add the migration to the `vec![]` in the `migrations()` function, following the existing `m0001_initial` entry

See `outputs/file-2-description.md` for full details.

## Self-Verification Checks

1. **Scope containment**: `git diff --name-only` should show only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`.
2. **Untracked file check**: `migration/src/m0002_drop_advisory_status/mod.rs` will appear as untracked — it is expected (Files to Create) and should be staged.
3. **Sensitive-pattern check**: Scan staged diff for secrets or credentials.
4. **Data-flow trace**: Migration up drops column, down re-adds column. Both directions are self-contained database operations with no downstream data flow dependencies.
5. **Contract & sibling parity**: The migration implements `MigrationTrait` — verify `up` and `down` methods match the trait contract. Compare with `m0001_initial/mod.rs` for structural parity.
6. **CI checks**: Run any CI check commands from CONVENTIONS.md (e.g., `cargo check`, `cargo fmt --check`, `cargo clippy`).
7. **Documentation currency**: No public API or configuration changes — documentation updates not required.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the `status` column
from the `advisory` table. The column was replaced by the `severity` enum
field in a previous migration and is no longer referenced by any service
or entity code. The down method re-adds the column as a nullable string
for rollback safety.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Description

```
## Summary
- Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- The `down` method re-adds the column as a nullable string for rollback
- Migration registered in `migration/src/lib.rs`

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

## Jira Updates

1. **Transition**: TC-9205 to "In Progress" at start of implementation
2. **Assign**: Set assignee to current user
3. **Custom field**: Set Git Pull Request custom field (`customfield_10875`) to the PR URL in ADF format
4. **Comment**: Post a comment with the PR link, summary of changes, and any deviations
5. **Transition**: TC-9205 to "In Review" after PR is opened
