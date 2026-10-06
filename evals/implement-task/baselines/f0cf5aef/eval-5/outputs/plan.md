# Implementation Plan for TC-9205

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add migration to drop status table column
**Target Branch**: TC-9005 (feature branch, NOT main)
**Repository**: trustify-backend
**Linked Issues**: is incorporated by TC-9005

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md for trustify-backend contains all required sections:
1. **Repository Registry** -- present with trustify-backend entry (Serena instance: serena_backend, Path: ./)
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present with tool naming convention and serena_backend instance

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9205:
- **Repository**: trustify-backend
- **Target Branch**: TC-9005
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column
- **Implementation Notes**: Follow m0001_initial pattern, use SeaORM TableAlterStatement, register in migrations() vec
- **Acceptance Criteria**: 4 items (drop column, rollback re-adds, registration, no stale references)
- **Test Requirements**: 3 items (migration runs, rollback works, existing queries unaffected)
- **Dependencies**: None
- **Bookend Type**: Not present (standard flow)
- **Target PR**: Not present (standard flow)

### Target Branch Extraction

The Target Branch is **TC-9005**. This is a feature branch (not main). The task branch will be created from TC-9005 and the PR will target TC-9005.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user account ID
2. Call `jira.edit_issue("TC-9205", assignee=<account-id>)` to assign
3. Call `jira.transition_issue("TC-9205")` to transition to In Progress

## Step 4 -- Understand the Code

### Files to inspect using Serena (serena_backend instance)

1. **`migration/src/lib.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see structure, then `mcp__serena_backend__find_symbol` to read the `migrations()` function body. Understand how m0001_initial is registered in the vec.

2. **`migration/src/m0001_initial/mod.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the sibling migration's structure (MigrationTrait implementation, up/down methods). This is the primary sibling for convention analysis.

3. **`entity/src/advisory.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to verify the Advisory entity no longer references a `status` column. Confirm the `Advisory::Status` enum variant exists for use in the migration's alter table statement, or determine the correct column identifier.

4. **CONVENTIONS.md** -- Check for `./CONVENTIONS.md` at the repository root using `mcp__serena_backend__list_dir`. If present, read it and extract CI check commands and code generation commands for Step 9.

### Convention Conformance Analysis

Analyze `migration/src/m0001_initial/mod.rs` as the sibling file. See outputs/conventions.md for discovered conventions.

### Documentation File Identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root (if present)
- No API docs are affected (this is a migration, not an endpoint change)

## Step 5 -- Create Branch (Feature Branch Flow)

Since the Target Branch is **TC-9005** (not main), checkout TC-9005 first, then create the task branch:

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

The task branch is named **TC-9205** (the task issue ID), branched from TC-9005.

## Step 6 -- Implement Changes

### File 1: CREATE `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module that implements `MigrationTrait` with:
- `up` method: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback

Follow the exact pattern from `m0001_initial/mod.rs` (imports, struct declaration, MigrationTrait impl, MigrationName impl).

See outputs/file-1-description.md for detailed changes.

### File 2: MODIFY `migration/src/lib.rs`

Register the new migration module in the migration list:
- Add `mod m0002_drop_advisory_status;` declaration
- Add the migration to the `vec![]` in the `migrations()` function, following the pattern of m0001_initial

See outputs/file-2-description.md for detailed changes.

## Step 7 -- Write Tests

Implement tests per Test Requirements:
- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

Note: These tests would likely be integration tests requiring a PostgreSQL test database. The test approach depends on the project's existing test infrastructure observed in m0001_initial.

## Step 8 -- Verify Acceptance Criteria

1. Migration drops the `status` column from the `advisory` table -- verified by up() implementation
2. Migration `down` method re-adds the column as nullable string -- verified by down() implementation
3. Migration is registered in `migration/src/lib.rs` -- verified by lib.rs modification
4. No service or entity code references the `status` column -- verified by inspecting entity/src/advisory.rs and searching codebase

## Step 9 -- Self-Verification

1. **Scope containment**: `git diff --name-only` should show only `migration/src/lib.rs` (modified) and `migration/src/m0002_drop_advisory_status/mod.rs` (created)
2. **Sensitive-pattern check**: scan diff for secrets/credentials
3. **Dead parameter detection**: no parameters removed in this change
4. **CI checks from CONVENTIONS.md**: run any CI commands extracted in Step 4
5. **Module-level test (Rust)**: run `cargo test -p migration` (or the correct crate name from `cargo metadata`)
6. **Data-flow trace**: Migration up drops column, down re-adds it -- complete lifecycle
7. **Query-scope verification**: The migration targets the specific `advisory` table and `status` column -- scope is correct
8. **Contract & sibling parity**: MigrationTrait fully implemented (up + down + name)

## Step 10 -- Commit and Push

### Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code. The down method re-adds the column as a nullable
string to support rollback.

Implements TC-9205
```

### Commit Command

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "$(cat <<'EOF'
feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code. The down method re-adds the column as a nullable
string to support rollback.

Implements TC-9205
EOF
)"
```

### Push and Create PR

```bash
git push -u origin TC-9205
```

### Fork Detection

Run `git remote get-url upstream 2>/dev/null` to detect fork. Assuming no fork:

### Create PR targeting TC-9005

```bash
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "$(cat <<'EOF'
## Summary

- Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- The `down` method re-adds the column as a nullable string to support rollback
- Register the new migration in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Verify migration runs successfully against a test database
- [ ] Verify rollback (down) re-adds the column as nullable string
- [ ] Verify existing advisory queries still work after the column is dropped
- [ ] Confirm no service or entity code references the `status` column
EOF
)"
```

Key points:
- **--base TC-9005**: The PR targets the feature branch TC-9005, NOT main
- The branch pushed is TC-9205 (the task issue ID)
- The commit includes `--trailer="Assisted-by: Claude Code"`

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with the PR URL in ADF format
2. Add comment to TC-9205 with PR link and summary of changes
3. Transition TC-9205 to In Review
