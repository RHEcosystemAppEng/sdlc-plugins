# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Branch Operations

### 1. Checkout Target Branch

The task specifies **Target Branch: TC-9005**. This is a feature branch, not main.

```bash
git checkout TC-9005
git pull
```

### 2. Create Task Branch

Create a new branch named after the task issue ID, branching from TC-9005:

```bash
git checkout -b TC-9205
```

**Important**: The branch is created from TC-9005 (the target/feature branch), NOT from main. The task branch is named TC-9205 (the task ID), NOT TC-9005 (the feature branch).

### 3. Push and Create PR

After implementation, push and create a PR targeting the feature branch:

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

The PR targets `--base TC-9005` (the feature branch), NOT `--base main`.

## Pre-Implementation Analysis

### Step 4 -- Understand the Code

Before making any changes, the following inspections would be performed:

1. **Inspect `migration/src/lib.rs`** using Serena (`mcp__serena_backend__get_symbols_overview`) to understand the current migration registration pattern and how `m0001_initial` is registered in the `migrations()` function.

2. **Inspect `migration/src/m0001_initial/mod.rs`** (sibling analysis) using Serena (`mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` with `include_body=true`) to understand the exact pattern for implementing `MigrationTrait`, including the `up` and `down` method signatures, the `name()` method, and how SeaORM's `SchemaManager` is used.

3. **Verify `entity/src/advisory.rs`** using Serena or Read to confirm that the `status` column is NOT referenced in the entity definition (the task says it was already removed). This satisfies the acceptance criterion: "No service or entity code references the status column."

4. **Search for `status` references** using `mcp__serena_backend__search_for_pattern` or Grep across the codebase to confirm no service code references `Advisory::Status` or the `status` column, ensuring the migration is safe.

5. **Check `CONVENTIONS.md`** at the repository root -- the repo structure shows a `CONVENTIONS.md` file exists. Read it for naming rules, CI check commands, and any migration-specific conventions.

6. **Inspect sibling test files** in `tests/api/advisory.rs` to understand test conventions for advisory-related tests.

7. **Documentation file identification**: Check `README.md`, `docs/architecture.md`, `docs/api.md` for any references to the `status` column that may need updating.

## Files to Modify

### File 1: `migration/src/lib.rs`

**Change**: Register the new migration module `m0002_drop_advisory_status` in the migration list.

- Add a `mod m0002_drop_advisory_status;` declaration alongside the existing `mod m0001_initial;`
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the `m0001_initial` entry

## Files to Create

### File 2: `migration/src/m0002_drop_advisory_status/mod.rs`

**Change**: Create a new migration module that drops the `status` column from the `advisory` table.

- Implement `MigrationTrait` following the exact pattern from `m0001_initial/mod.rs`
- Implement `name()` returning a descriptive migration name (e.g., `"m0002_drop_advisory_status"`)
- Implement `up()` method that drops the `status` column using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- Implement `down()` method that re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any service code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

With the trailer: `--trailer="Assisted-by: Claude Code"`

## PR Details

```bash
gh pr create \
  --base TC-9005 \
  --title "feat(migration): add migration to drop advisory status column" \
  --body "## Summary

- Add database migration m0002_drop_advisory_status to drop the deprecated status column from the advisory table
- Register the new migration in migration/src/lib.rs
- The down method re-adds the column as nullable string for rollback support

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Run migration against test database and verify status column is dropped
- [ ] Run rollback and verify status column is re-added as nullable string
- [ ] Run existing advisory queries and verify they still work after migration
- [ ] Run cargo test to verify no regressions"
```

## Self-Verification Checks

1. **Scope containment**: `git diff --name-only` should show only `migration/src/lib.rs` (modified) and `migration/src/m0002_drop_advisory_status/mod.rs` (created)
2. **Untracked file check**: Verify `m0002_drop_advisory_status/mod.rs` is staged
3. **Sensitive-pattern check**: Scan staged diff for secrets/credentials
4. **Duplication check**: Search for any existing migration that drops the status column
5. **Data-flow trace**: Migration up drops column, down re-adds it -- complete lifecycle
6. **Contract verification**: `MigrationTrait` requires `name()`, `up()`, `down()` -- all implemented
7. **Sibling parity**: Compare against `m0001_initial` for pattern consistency
8. **CI checks**: Run commands from CONVENTIONS.md (e.g., `cargo build`, `cargo clippy`, `cargo fmt --check`)
9. **Entity verification**: Confirm `entity/src/advisory.rs` does not reference `status` column

## Jira Updates

1. Assign task to current user and transition to In Progress (Step 3)
2. After PR creation, update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
3. Add comment with PR link and summary of changes
4. Transition task to In Review
