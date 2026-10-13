# Implementation Plan for TC-9205

## Task Summary

**Jira Issue**: TC-9205 -- Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch)
**Linked Issues**: is incorporated by TC-9005

## Target Branch Extraction

The task description contains a **Target Branch** section with value `TC-9005`. This is a
feature branch (not `main`), indicating that TC-9205 is part of a feature-branch workflow
where multiple tasks are incorporated into a shared feature branch. All branch operations
must use TC-9005 as the base.

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:
- **Repository Registry**: present, maps `trustify-backend` to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present, includes Project key (TC), Cloud ID, Feature issue type ID (10142), Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
- **Code Intelligence**: present, `serena_backend` configured with `rust-analyzer`

All sections validated. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9205:
- **Repository**: trustify-backend
- **Target Branch**: TC-9005
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table.
- **Files to Modify**: `migration/src/lib.rs`
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs`
- **Implementation Notes**: Follow m0001_initial pattern, use SeaORM TableAlterStatement, register in lib.rs
- **Acceptance Criteria**: 4 items (migration drops column, down re-adds, registered in lib.rs, no stale references)
- **Test Requirements**: 3 items (migration runs, rollback works, existing queries work)
- **Dependencies**: None
- **Bookend Type**: not present (normal task)
- **Target PR**: not present (new PR flow)

Capture `webUrl` from API response: `https://redhat.atlassian.net/browse/TC-9205`

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user's account ID
2. Call `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign
3. Call `jira.transition_issue(TC-9205)` to transition to In Progress

## Step 4 -- Understand the Code

### Code inspection plan

Use the Serena instance `serena_backend` (from Repository Registry) to inspect code:

1. **Inspect `migration/src/lib.rs`**: Call `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to understand the migration registration structure. Then use `mcp__serena_backend__find_symbol` with `include_body=true` to read the `migrations()` function and see how `m0001_initial` is registered in the `vec![]`.

2. **Inspect `migration/src/m0001_initial/mod.rs`**: Call `mcp__serena_backend__get_symbols_overview` to see the MigrationTrait implementation pattern. Use `find_symbol` to read the `up` and `down` method bodies and understand the exact SeaORM API usage.

3. **Verify advisory entity**: Inspect `entity/src/advisory.rs` using `mcp__serena_backend__get_symbols_overview` to confirm the `status` column is NOT referenced. This satisfies acceptance criterion 4.

4. **Check for stale references**: Use `mcp__serena_backend__search_for_pattern` to search for `Advisory::Status` and `status` column references across the codebase to ensure no service or entity code still references it.

5. **Check backward compatibility**: Use `mcp__serena_backend__find_referencing_symbols` on the `migrations()` function to understand how the migration list is consumed.

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo structure shows `CONVENTIONS.md` exists. Read it and extract any CI check commands and code generation commands for use in Step 9.

### Convention conformance analysis

Analyze sibling files for established patterns:
- **Sibling migration**: `migration/src/m0001_initial/mod.rs` -- the only existing migration module. Inspect its structure using `get_symbols_overview` to extract naming, error handling, and implementation patterns.
- **Sibling entity**: `entity/src/advisory.rs` and `entity/src/sbom.rs` -- inspect for SeaORM entity patterns and column naming conventions.

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- No API docs directly related to migration code

## Step 5 -- Branch Operations

**This is the critical branching step.** The Target Branch is `TC-9005`, NOT `main`.

```bash
# Check out the TARGET BRANCH (feature branch TC-9005)
git checkout TC-9005
git pull

# Create a new task branch named after the Jira issue
git checkout -b TC-9205
```

This creates task branch `TC-9205` from the feature branch `TC-9005`. The task branch
is distinct from the feature branch -- it will be merged back into TC-9005 via PR.

## Step 6 -- Implement Changes

### File to Create: `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module following the pattern in `m0001_initial/mod.rs`:
- Implement `MigrationTrait` with `up` and `down` methods
- `up`: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down`: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback
- Include proper documentation comments on the migration struct and methods

### File to Modify: `migration/src/lib.rs`

- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the existing `m0001_initial` entry pattern

## Step 7 -- Write Tests

Implement tests per Test Requirements:
- Test migration `up` runs successfully against test database
- Test migration `down` (rollback) re-adds the column
- Verify existing advisory queries work after column drop

Tests would go in the migration crate's test module or integration test directory, following the existing test patterns.

## Step 8 -- Verify Acceptance Criteria

1. Migration drops the `status` column -- verified by `up` method implementation
2. Migration `down` re-adds as nullable string -- verified by `down` method implementation
3. Migration registered in `lib.rs` -- verified by mod declaration and vec entry
4. No service/entity code references `status` column -- verified by Step 4 codebase search

## Step 9 -- Self-Verification

- Scope containment: `git diff --name-only` should show only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`
- Sensitive-pattern check: scan staged diff for secrets
- CI checks from CONVENTIONS.md: run extracted verification commands
- Module-level Rust test: `cargo test -p <migration-crate-name>`
- Duplication check: search for similar migration patterns

## Step 10 -- Commit and Push

### Commit message

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

Add database migration m0002_drop_advisory_status that drops the deprecated
status column from the advisory table. The column was replaced by the severity
enum field and is no longer referenced by any service or entity code.

The down method re-adds the column as a nullable string to support rollback.

Implements TC-9205"
```

### Fork detection

Run `git remote get-url upstream 2>/dev/null` to detect fork setup. Handle both fork and non-fork cases.

### Push and create PR

Push the task branch and create a PR targeting the feature branch TC-9005:

```bash
git push -u origin TC-9205
```

**Non-fork case:**
```bash
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "$(cat <<'EOF'
## Summary

- Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- Register the new migration in `migration/src/lib.rs`
- Include rollback support (down method re-adds column as nullable string)

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
EOF
)"
```

**Fork case (if upstream remote detected):**
```bash
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

The PR targets `--base TC-9005` (the feature branch), NOT `--base main`.

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL using ADF format
2. Add comment to TC-9205 with PR link, summary of changes, and any deviations
3. Transition TC-9205 to In Review

## Key Branch Operation Summary

| Operation | Value | Rationale |
|-----------|-------|-----------|
| Checkout base | `git checkout TC-9005` | Target Branch from task description is TC-9005 |
| Create task branch | `git checkout -b TC-9205` | Named after the Jira task issue ID |
| PR base | `--base TC-9005` | PR targets the feature branch, not main |
| Commit trailer | `--trailer="Assisted-by: Claude Code"` | Required by skill Step 10 |
| Commit footer | `Implements TC-9205` | Conventional Commits with Jira reference |
