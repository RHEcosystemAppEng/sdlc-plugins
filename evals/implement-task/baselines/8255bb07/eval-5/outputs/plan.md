# Implementation Plan for TC-9205

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Status**: To Do
**Linked Issues**: is incorporated by TC-9005
**Repository**: trustify-backend
**Target Branch**: TC-9005

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from the task description:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (feature branch -- not main)
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module in the migration list
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column from the `advisory` table
- **Implementation Notes**: Follow existing migration pattern in `m0001_initial/mod.rs`, use SeaORM's `TableAlterStatement`, implement `MigrationTrait` with `up`/`down` methods
- **Acceptance Criteria**: 4 items (migration drops column, down re-adds as nullable string, registered in lib.rs, no code references status column)
- **Test Requirements**: 3 items (migration runs, rollback works, existing queries work)
- **Dependencies**: None
- **Bookend Type**: not present
- **Target PR**: not present
- **GitHub Issue custom field**: customfield_10747 -- would check for value on the fetched issue; not available in this eval

The Target Branch is `TC-9005`, which is a feature branch (not `main`). This means:
- The task branch will be created from `TC-9005`
- The PR will target `TC-9005` using `--base TC-9005`

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9205)` and look for a digest comment starting with `[sdlc-workflow] Description digest:`. Compare stored digest against computed digest of the current description. (Skipped in this eval -- no external service calls.)

## Step 2 -- Verify Dependencies

The task has no dependencies. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign the task
3. `jira.transition_issue(TC-9205)` to transition to "In Progress"

## Step 4 -- Understand the Code

### Files to inspect

Using Serena instance `serena_backend` (from Repository Registry):

1. **`migration/src/lib.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to understand the migration registration structure. Expect to find a `migrations()` function returning a `Vec<Box<dyn MigrationTrait>>` that currently contains `m0001_initial::Migration`.

2. **`migration/src/m0001_initial/mod.rs`** -- Use `mcp__serena_backend__find_symbol` with `include_body=true` to read the existing migration implementation and understand the pattern (struct definition, `MigrationTrait` impl with `up` and `down` methods).

3. **`entity/src/advisory.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to verify that the `Advisory` entity no longer references a `status` column. Confirm only `severity` (or other fields) are present.

4. **Sibling analysis**: `m0001_initial/mod.rs` is the primary sibling for the new migration file. Would inspect its structure to discover conventions.

5. **Check backward compatibility**: Use `mcp__serena_backend__search_for_pattern` to search for any remaining references to `Advisory::Status` or `advisory.status` across the codebase to confirm the column is truly unused.

### CONVENTIONS.md lookup

The repository has a `CONVENTIONS.md` file at the root (visible in the directory tree). Would read it using `mcp__serena_backend__list_dir` and then reading the file to extract:
- Naming conventions
- CI check commands (for Step 9)
- Code generation commands

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- No API docs are directly affected by a migration-only change

### Convention conformance analysis

See `outputs/conventions.md` for the full list of discovered conventions.

### Test convention analysis

Sibling test files in `tests/api/`:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Would inspect these to understand:
- Assertion style (`assert_eq!` with `StatusCode`)
- Database setup/teardown patterns
- Test naming conventions

## Step 5 -- Create Branch

Since this is the default flow (no Target PR, no Bookend Type), and the Target Branch is `TC-9005`:

```
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates a task branch `TC-9205` from the feature branch `TC-9005`.

## Step 6 -- Implement Changes

### File 1: `migration/src/lib.rs` (MODIFY)

Add the new migration module declaration and register it in the migrations list.

Changes:
1. Add `mod m0002_drop_advisory_status;` module declaration alongside existing `mod m0001_initial;`
2. Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after `m0001_initial::Migration`

See `outputs/file-1-description.md` for detailed changes.

### File 2: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

Create a new migration module that:
1. Defines a `Migration` struct
2. Implements `MigrationTrait` with:
   - `name()` returning a descriptive migration name
   - `up()` that drops the `status` column from the `advisory` table using `TableAlterStatement`
   - `down()` that re-adds the `status` column as a nullable string for rollback

See `outputs/file-2-description.md` for detailed changes.

### Documentation impact

This is a migration-only change with no public API, CLI, or configuration changes. No documentation updates are required.

## Step 7 -- Write Tests

The test requirements specify:
1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

These tests would be executed using `cargo test` against a real PostgreSQL test database, following the project's integration test pattern. The migration tests would typically be part of the migration crate's test suite or the integration test suite.

Since the task's "Files to Create" and "Files to Modify" sections do not list a test file, the tests would be run by executing the migration against the test database and verifying advisory queries still work -- this is an integration-level verification rather than a new test file. Would run:

```
cargo test -p migration
cargo test -p fundamental -- advisory
```

## Step 8 -- Verify Acceptance Criteria

1. Migration drops the `status` column from the `advisory` table -- SATISFIED by the `up()` method using `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)`
2. Migration `down` method re-adds the column as nullable string for rollback -- SATISFIED by `down()` using `ColumnDef::new(Advisory::Status).string().null()`
3. Migration is registered in `migration/src/lib.rs` -- SATISFIED by adding to the `vec![]` in `migrations()`
4. No service or entity code references the `status` column -- Would verify via `mcp__serena_backend__search_for_pattern` or grep for `Advisory::Status`, `status` in entity/service code

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` would show:
  - `migration/src/lib.rs` -- in Files to Modify
  - `migration/src/m0002_drop_advisory_status/mod.rs` -- in Files to Create
- Both files are in scope. No out-of-scope changes.

### Untracked file check
- `migration/src/m0002_drop_advisory_status/mod.rs` is a new file (untracked) but is listed in Files to Create -- should be staged.

### Sensitive-pattern check
- No passwords, API keys, secrets, or .env files in the migration code.

### Documentation currency
- No public APIs, configuration options, or setup steps were changed. No documentation updates needed.

### Data-flow trace
- `up()`: drops column from `advisory` table -- a DDL operation, no data flow beyond schema change. Complete.
- `down()`: re-adds column as nullable string -- DDL operation, rollback path. Complete.
- Migration registration in `lib.rs` -- connects migration to the migration runner. Complete.

### Contract & sibling parity
- `Migration` struct implements `MigrationTrait` -- all required methods (`name()`, `up()`, `down()`) are implemented.
- Sibling parity with `m0001_initial::Migration`: same trait implementation pattern, same async method signatures. Parity maintained.

### Cross-section reference consistency
- `migration/src/lib.rs` referenced in both "Files to Modify" and "Implementation Notes" -- consistent.
- `migration/src/m0002_drop_advisory_status/mod.rs` referenced in "Files to Create" -- consistent with "Implementation Notes" pattern reference.
- `entity/src/advisory.rs` referenced in "Implementation Notes" for verification only -- consistent.

### Duplication check
- The migration is unique (drops a specific column). No duplication with existing code.

## Step 10 -- Commit and Push

### Branch operations
1. Already on branch `TC-9205` (created from `TC-9005` in Step 5)
2. Stage files:
   ```
   git add migration/src/lib.rs migration/src/m0002_drop_advisory_status/mod.rs
   ```
3. Commit:
   ```
   git commit --trailer="Assisted-by: Claude Code" -m "refactor(migration): drop deprecated status column from advisory table

   Add migration m0002 that removes the unused status column from the advisory
   table. The column was replaced by the severity enum field and is no longer
   referenced by any service or entity code.

   Implements TC-9205"
   ```
4. Push:
   ```
   git push -u origin TC-9205
   ```
5. Create PR targeting the feature branch `TC-9005`:
   ```
   gh pr create --base TC-9005 --title "refactor(migration): drop deprecated status column from advisory table" --body "## Summary

   - Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
   - Register the new migration in `migration/src/lib.rs`
   - The `down` method re-adds the column as a nullable string for safe rollback

   Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

   ## Test plan

   - [ ] Run `cargo test -p migration` to verify migration executes successfully
   - [ ] Verify rollback re-adds the column as nullable string
   - [ ] Run advisory endpoint tests to confirm no regressions"
   ```

### Commit message

```
refactor(migration): drop deprecated status column from advisory table

Add migration m0002 that removes the unused status column from the advisory
table. The column was replaced by the severity enum field and is no longer
referenced by any service or entity code.

Implements TC-9205
```

### PR target

The PR targets **TC-9005** (the feature branch), NOT `main`. This is because the task's Target Branch is `TC-9005`.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9205 with the PR URL in ADF format (inlineCard).
2. **Add comment** to TC-9205 with:
   - PR link
   - Summary: Added migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table. Registered the migration in `lib.rs`. The `down` method supports rollback by re-adding the column as a nullable string.
   - No deviations from the plan.
   - Footer with sdlc-workflow/implement-task version link.
3. **Transition** TC-9205 to "In Review".
