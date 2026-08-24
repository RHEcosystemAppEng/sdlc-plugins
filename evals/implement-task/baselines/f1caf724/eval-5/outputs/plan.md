# Implementation Plan for TC-9205

## Task Summary

**Jira Issue**: TC-9205 -- Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, not main)
**Task Branch**: TC-9205

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains all required sections:
- Repository Registry: present with trustify-backend entry
- Jira Configuration: present with Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present with serena_backend instance for trustify-backend

Configuration is valid. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed the structured description from TC-9205. All required sections are present:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs`
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs`
- **Implementation Notes**: Present with detailed patterns for SeaORM migration
- **Acceptance Criteria**: 4 criteria defined
- **Test Requirements**: 3 test requirements defined
- **Dependencies**: None

### Target Branch extraction

The Target Branch section specifies **TC-9005**. This is a feature branch (not main), meaning the task is part of a feature-branch workflow. The task branch will be created from TC-9005, and the PR will target TC-9005 as its base.

### GitHub Issue extraction

GitHub Issue custom field (customfield_10747) would be read from the issue's fields. If present, parse and store for PR description. If empty, skip silently.

## Step 1.5 -- Verify Description Integrity

Retrieve all comments on TC-9205 using `jira.get_issue_comments(TC-9205)`.

Search for comments whose body starts with the marker string `[sdlc-workflow] Description digest:`.

- **If no digest comment found**: Log warning and proceed normally -- "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."
- **If digest comment found**: Extract the format-tagged digest, compute current digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9205.txt`, compare format tags and hex digests. On match, proceed silently. On mismatch, alert user and pause.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9205 to current user via `jira.edit_issue(TC-9205, assignee=<account-id>)`
3. Transition TC-9205 to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code

### Code inspection plan

Using the Serena instance `serena_backend` (from Repository Registry), inspect the following files before making any changes:

1. **`migration/src/lib.rs`** (File to Modify) -- Use `mcp__serena_backend__get_symbols_overview` to understand the current migration registration structure. Identify the `migrations()` function and the existing `vec![]` entries to understand the registration pattern.

2. **`migration/src/m0001_initial/mod.rs`** (Sibling migration) -- Use `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` with `include_body=true` to read the existing migration implementation. This is the pattern reference for implementing `MigrationTrait` with `up` and `down` methods.

3. **`entity/src/advisory.rs`** (Referenced in Implementation Notes) -- Use `mcp__serena_backend__get_symbols_overview` to verify that the Advisory entity no longer references the `status` column. This confirms the column is safe to drop.

4. **`migration/src/lib.rs`** -- Use `mcp__serena_backend__find_symbol` to read the `migrations()` function body and understand how modules are registered in the migration list.

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read and extract CI check commands and code generation commands.

### Documentation file identification

- `README.md` at repository root
- `docs/architecture.md` -- system architecture
- `docs/api.md` -- REST API reference (not directly impacted by a migration)

### Convention conformance analysis

Analyze sibling migration files and entity files for conventions. See `outputs/conventions.md` for detailed findings.

## Step 5 -- Create Branch

### Branch operations

Since the Target Branch is **TC-9005** (a feature branch), the branch operations are:

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This checks out the feature branch TC-9005 first, pulls the latest changes, then creates the task branch TC-9205 from it. The task branch name is the Jira issue ID (TC-9205), which is distinct from the target branch (TC-9005).

**Important**: We do NOT checkout main. The Target Branch TC-9005 is used as the base for this task branch.

## Step 6 -- Implement Changes

### Files to Modify

#### 1. `migration/src/lib.rs`

Register the new migration module in the migration list:

- Add `mod m0002_drop_advisory_status;` to the module declarations
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`

See `outputs/file-1-description.md` for detailed changes.

### Files to Create

#### 2. `migration/src/m0002_drop_advisory_status/mod.rs`

Create the migration module implementing `MigrationTrait`:

- Implement `up` method: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- Implement `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback
- Follow the exact pattern from `migration/src/m0001_initial/mod.rs`

See `outputs/file-2-description.md` for detailed changes.

## Step 7 -- Write Tests

Implement the test requirements:

1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

Tests would be added in the migration test infrastructure, following existing patterns from the test setup in `tests/` or inline migration tests.

## Step 8 -- Verify Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table -- verified in `up` method
- [x] Migration `down` method re-adds the column as nullable string for rollback -- verified in `down` method
- [x] Migration is registered in `migration/src/lib.rs` -- verified in lib.rs modification
- [x] No service or entity code references the `status` column -- verified by inspecting `entity/src/advisory.rs`

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` should show only:
  - `migration/src/lib.rs` (Files to Modify)
  - `migration/src/m0002_drop_advisory_status/mod.rs` (Files to Create)
- No out-of-scope files modified.

### Dead parameter detection
No function parameters are being removed in this change.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Duplication check
Search for existing migration drop-column patterns in the repository to ensure no duplication of utilities.

### Query-scope verification
Not applicable -- this is a schema migration, not a batch data operation.

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer used by any service code.

Implements TC-9205
```

### Commit command

```bash
git add migration/src/lib.rs migration/src/m0002_drop_advisory_status/mod.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer used by any service code.

Implements TC-9205"
```

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If upstream exists, use fork-aware PR creation. If not, use default.

### Push and PR creation

```bash
git push -u origin TC-9205
```

Create PR targeting the feature branch TC-9005 (the Target Branch), NOT main:

```bash
gh pr create --base TC-9005 --title "feat(migration): drop advisory status column" --body "## Summary

- Add migration m0002_drop_advisory_status to drop the deprecated status column from the advisory table
- The column was replaced by the severity enum and is no longer referenced by service or entity code
- Migration includes rollback support (re-adds column as nullable string)

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test Plan

- [ ] Migration runs successfully against test database
- [ ] Rollback re-adds the column correctly
- [ ] Existing advisory queries work after column removal"
```

**Key**: The PR uses `--base TC-9005` to target the feature branch, not `--base main`. This ensures the PR is merged into the feature branch where related work for the TC-9005 feature is being aggregated.

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with the PR URL in ADF format
2. Add comment to TC-9205 with PR link, summary of changes, and any deviations
3. Transition TC-9205 to In Review
