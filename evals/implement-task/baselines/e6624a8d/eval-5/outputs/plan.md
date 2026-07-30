# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Prerequisites and Validation

### Project Configuration (Step 0)
- Repository Registry: trustify-backend with Serena instance `serena_backend` -- verified present
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID -- verified present
- Code Intelligence: Serena instance `serena_backend` with rust-analyzer -- verified present

### Dependencies (Step 2)
- No dependencies listed -- proceed immediately

### Jira Transitions (Step 3)
- Would retrieve current user via `jira.user_info()`
- Would assign TC-9205 to current user via `jira.edit_issue`
- Would transition TC-9205 to "In Progress" via `jira.transition_issue`

### Description Integrity (Step 1.5)
- Would fetch comments on TC-9205 and look for `[sdlc-workflow] Description digest:` comment
- Would verify digest matches current description if found

## Branch Operations (Step 5)

### Target Branch
The task specifies **Target Branch: TC-9005**, which is a feature branch (not main). This means TC-9205 is part of a larger feature (TC-9005) using the feature-branch workflow.

### Branch Creation
```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates branch `TC-9205` off the feature branch `TC-9005`, not off `main`.

## Code Understanding (Step 4)

### Files to Inspect
1. **`migration/src/m0001_initial/mod.rs`** -- sibling migration to understand the pattern (structure, imports, trait implementation)
2. **`migration/src/lib.rs`** -- understand how migrations are registered (module declarations, `migrations()` function)
3. **`entity/src/advisory.rs`** -- verify that the `status` column is no longer referenced in the Advisory entity definition

### Sibling Analysis
- Would use `mcp__serena_backend__get_symbols_overview` on `migration/src/m0001_initial/mod.rs` to understand migration structure
- Would use `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to understand registration
- Would use `mcp__serena_backend__search_for_pattern` to search for any remaining references to `Advisory::Status` or the `status` column across the codebase

### Documentation Files
- `CONVENTIONS.md` at repository root -- would read for CI check commands and coding conventions
- `README.md` at repository root -- unlikely to need updates for a migration

### CONVENTIONS.md
- Would read `CONVENTIONS.md` and extract CI verification commands for Step 9

## Files to Modify

### 1. `migration/src/lib.rs`
- Add module declaration: `mod m0002_drop_advisory_status;`
- Add migration to the `migrations()` function's `vec![]`: `Box::new(m0002_drop_advisory_status::Migration)`

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
- New migration implementing `MigrationTrait`
- `up` method: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback

## Verification (Steps 7-9)

### Tests (Step 7)
Per Test Requirements:
- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

These would be run via `cargo test` in the migration crate and/or the integration test suite.

### Acceptance Criteria Verification (Step 8)
1. Migration drops the `status` column from the `advisory` table -- verified by the `up` method implementation
2. Migration `down` method re-adds the column as nullable string for rollback -- verified by the `down` method implementation
3. Migration is registered in `migration/src/lib.rs` -- verified by the module declaration and `vec![]` entry
4. No service or entity code references the `status` column -- verified by codebase search in Step 4

### Self-Verification (Step 9)
- **Scope containment**: `git diff --name-only` would show only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` -- both in scope
- **Untracked file check**: `migration/src/m0002_drop_advisory_status/mod.rs` is a new file and would be flagged for staging
- **Sensitive-pattern check**: migration code contains no secrets or credentials
- **CI checks from CONVENTIONS.md**: would run all extracted CI check commands
- **Data-flow trace**: Migration is a DDL operation -- data flow is: `up` called by migration runner -> drops column -> complete. `down` called by rollback -> re-adds column -> complete. Both paths are complete.
- **Contract verification**: `MigrationTrait` requires `up` and `down` methods -- both implemented
- **Sibling parity**: follows same pattern as `m0001_initial` migration
- **Query-scope verification**: The migration targets a specific column (`status`) on a specific table (`advisory`) -- scope is precise

## Commit and Push (Step 10)

### Commit Message
```
feat(migration): add migration to drop advisory status column

Drop the deprecated `status` column from the `advisory` table. The column
was replaced by the `severity` enum field and is no longer referenced by
any service or entity code.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

### PR Creation
Since Target Branch is `TC-9005` (a feature branch), the PR targets the feature branch:

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

The PR description would include:
- Summary of changes
- `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)` (clickable link)

### Fork Detection
- Would check `git remote get-url upstream 2>/dev/null`
- If fork detected: `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 ...`
- If no fork: `gh pr create --base TC-9005 ...`

## Jira Update (Step 11)

- Would update custom field `customfield_10875` (Git Pull Request) with the PR URL in ADF format
- Would add a comment to TC-9205 summarizing the changes and linking the PR
- Would transition TC-9205 to "In Review"
- Comment would include the sdlc-workflow plugin version footer
