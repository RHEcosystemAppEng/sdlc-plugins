# Implementation Plan for TC-9205

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch)
**Linked Issues**: is incorporated by TC-9005
**Dependencies**: None

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- **Repository Registry**: present, contains trustify-backend with Serena instance `serena_backend` and path `./`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence**: present, with tool naming convention `mcp__<serena-instance>__<tool>`

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | TC-9005 |
| Description | Add a database migration that drops the deprecated `status` column from the `advisory` table. |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| Implementation Notes | Follow m0001_initial pattern, use SeaORM TableAlterStatement, register in lib.rs |
| Bookend Type | (none) |
| Target PR | (none) |
| Review Context | (none) |

**Target Branch extraction**: `TC-9005` -- this is a feature branch, not main. The task branch will be based on TC-9005 and the PR will target TC-9005.

**GitHub Issue extraction**: The GitHub Issue custom field (`customfield_10747`) would be read from the Jira issue response. If present, the reference would be included in the PR description.

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9205)` and look for the `[sdlc-workflow] Description digest:` marker. Compute digest and compare if found. Proceed if matching or if no digest comment exists (backward compatibility).

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user via `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9205, assignee=<current-user-account-id>)`
3. Transition: `jira.transition_issue(TC-9205) -> In Progress`

## Step 4 -- Understand the Code

### Files to inspect

1. **`migration/src/lib.rs`** (file to modify): Use `mcp__serena_backend__get_symbols_overview` to understand the structure. Expect a `migrations()` function returning a `Vec` of migration boxes, currently containing `m0001_initial::Migration`.

2. **`migration/src/m0001_initial/mod.rs`** (sibling for conventions): Use `mcp__serena_backend__find_symbol` with `include_body=true` to read the full implementation. This is the pattern reference for the new migration.

3. **`entity/src/advisory.rs`** (verification): Use `mcp__serena_backend__get_symbols_overview` to confirm the `Advisory` entity no longer references a `status` column/field. The task description states it was replaced by `severity`.

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo structure shows it exists. Read it and extract any CI check commands and code generation commands. Follow its conventions.

### Convention conformance analysis

Analyze `migration/src/m0001_initial/mod.rs` as the primary sibling. See conventions.md output for discovered patterns.

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- No API documentation is directly impacted by a database migration

## Step 5 -- Branch Operations

**Default flow (no Target PR, no Bookend Type):**

The Target Branch is `TC-9005`, which is a feature branch. The task branch is named after the Jira issue ID (`TC-9205`) and is based on `TC-9005`.

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates branch `TC-9205` from the feature branch `TC-9005`. The PR created later will target `TC-9005`, not `main`.

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module following the pattern in `m0001_initial/mod.rs`. The migration:
- Implements `MigrationTrait` with `up` and `down` methods
- `up`: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down`: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback

### File 2: Modify `migration/src/lib.rs`

- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the `m0001_initial` entry

### Pre-implementation verification

Before writing code, verify:
- `entity/src/advisory.rs` does NOT reference `status` column (confirms safe to drop)
- The `Advisory` enum/struct in the entity has `Table` and `Status` variants (needed for the migration's column reference)

## Step 7 -- Write Tests

Implement tests as described in Test Requirements:
- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

Tests would be added in the migration crate's test module or in `tests/api/advisory.rs` depending on existing test patterns.

## Step 8 -- Verify Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table (via `up` method)
- [x] Migration `down` method re-adds the column as nullable string for rollback
- [x] Migration is registered in `migration/src/lib.rs`
- [x] No service or entity code references the `status` column (verified in Step 4)

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify only these files are modified/created:
- `migration/src/lib.rs` (modified)
- `migration/src/m0002_drop_advisory_status/mod.rs` (created)

### CI checks
Run CI check commands from CONVENTIONS.md (if any). Run `cargo test -p migration` for Rust module-level test requirement.

### Data-flow trace
Migration data flow: `up` method -> SeaORM `TableAlterStatement` -> PostgreSQL `ALTER TABLE advisory DROP COLUMN status`. Reverse: `down` method -> SeaORM `TableAlterStatement` -> PostgreSQL `ALTER TABLE advisory ADD COLUMN status VARCHAR NULL`. Both paths are complete.

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field in a previous migration and is no longer referenced
by any service or entity code.

The down method re-adds the column as a nullable string for rollback.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

### Fork detection

Run `git remote get-url upstream 2>/dev/null` to detect fork. Adjust PR creation command accordingly.

### Push and PR creation

```bash
git push -u origin TC-9205
```

**PR creation (no fork detected):**

```bash
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "$(cat <<'EOF'
## Summary

- Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- The `down` method re-adds the column as a nullable string for rollback support
- Migration registered in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Migration runs successfully against a test database
- [ ] Rollback (down) re-adds the column
- [ ] Existing advisory queries still work after the column is dropped
EOF
)"
```

Key point: `--base TC-9005` targets the feature branch, NOT main.

**PR creation (fork detected):**

```bash
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:
   ```
   jira.update_issue(TC-9205, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9205 with PR link, summary of changes, and any deviations.

3. **Transition** to In Review: `jira.transition_issue(TC-9205) -> In Review`
