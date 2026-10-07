# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (extracted from the Target Branch section of the task description)
**Linked Issues**: is incorporated by TC-9005

The Target Branch section specifies `TC-9005`, which is a feature branch (not `main`). This means TC-9205 is part of a feature-branch workflow where tasks are incorporated into the parent feature branch TC-9005. All branch operations must use TC-9005 as the base.

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:
- Repository Registry: present, lists `trustify-backend` with Serena instance `serena_backend` at path `./`
- Jira Configuration: present, contains Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present, with tool naming convention `mcp__<serena-instance>__<tool>`

All sections validated. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9205:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | **TC-9005** |
| Description | Add a database migration that drops the deprecated `status` column from the `advisory` table |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| Implementation Notes | Follow pattern in `m0001_initial/mod.rs`, use SeaORM `TableAlterStatement` |
| Acceptance Criteria | 4 items (drop column, rollback, registration, no references) |
| Test Requirements | 3 items (migration runs, rollback works, queries still work) |
| Dependencies | None |
| Bookend Type | Not present (standard flow) |
| Target PR | Not present (standard flow) |

### Target Branch Extraction

The **Target Branch** section contains `TC-9005`. This is the feature branch that TC-9205 contributes to. All branch and PR operations will use TC-9005 as the base branch, not `main`.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign the task
3. `jira.transition_issue(TC-9205)` to transition to In Progress

## Step 4 -- Understand the Code (Inspection Phase)

### Files to inspect before making any changes:

1. **`migration/src/m0001_initial/mod.rs`** -- Read this file to understand the existing migration pattern. This is the reference migration cited in Implementation Notes. Inspect:
   - How `MigrationTrait` is implemented
   - The structure of `up()` and `down()` methods
   - How SeaORM table/column operations are invoked
   - Import patterns and module structure

2. **`entity/src/advisory.rs`** -- Read this file to verify that the `status` column is no longer referenced in the Advisory entity definition. The task explicitly states: "The `advisory` entity in `entity/src/advisory.rs` no longer references the `status` column -- verify this before proceeding."

3. **`migration/src/lib.rs`** -- Read this file to understand:
   - How migrations are registered in the `migrations()` function
   - The pattern for adding new migration modules to the `vec![]`
   - Import and module declaration patterns

4. **Sibling analysis for conventions** -- Use `get_symbols_overview` (via `mcp__serena_backend__get_symbols_overview`) on `migration/src/m0001_initial/mod.rs` to understand the migration struct and trait implementation pattern.

5. **CONVENTIONS.md lookup** -- Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`) and read it if present. Extract CI check commands and code generation commands.

6. **Documentation file identification** -- Check for README files in `migration/` and repository root. Identify any architecture docs that describe migration patterns.

### Convention conformance analysis

Would analyze `migration/src/m0001_initial/mod.rs` as the primary sibling to extract:
- Naming conventions for migration modules (`m####_descriptive_name`)
- Struct naming pattern for migration types
- Error handling in migration methods
- Import organization
- How enum variants map to table/column names

## Step 5 -- Branch Operations

**Target Branch is TC-9005 (not main).** Per the skill specification, the task branch is checked out from the Target Branch.

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates a new branch `TC-9205` (named after the task issue ID) based on `TC-9005` (the feature branch). The task branch name is TC-9205, distinct from the Target Branch TC-9005.

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module following the pattern from `m0001_initial/mod.rs`. See `outputs/file-1-description.md` for detailed changes.

### File 2: Modify `migration/src/lib.rs`

Register the new migration module. See `outputs/file-2-description.md` for detailed changes.

## Step 7 -- Write Tests

Implement tests per Test Requirements:
- Test that the migration runs successfully
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

## Step 8 -- Verify Acceptance Criteria

Verify each criterion:
1. Migration drops the `status` column from the `advisory` table
2. Migration `down` method re-adds the column as nullable string for rollback
3. Migration is registered in `migration/src/lib.rs`
4. No service or entity code references the `status` column (verified in Step 4)

## Step 9 -- Self-Verification

- **Scope containment**: `git diff --name-only` should show only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`
- **Sensitive-pattern check**: scan staged diff for secrets/credentials
- **Duplication check**: search for existing drop-column migrations
- **CI checks**: run commands from CONVENTIONS.md if present; otherwise `cargo check`, `cargo fmt --check`, `cargo clippy`
- **Module-level test**: `cargo test -p migration`
- **Contract & sibling parity**: verify `MigrationTrait` is fully implemented

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field and is no longer referenced by any entity or
service code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

### Commit command

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer='Assisted-by: Claude Code' -m "$(cat <<'EOF'
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field and is no longer referenced by any entity or
service code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
EOF
)"
```

### Push and PR

```bash
git push -u origin TC-9205
```

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If no fork detected:

```bash
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "$(cat <<'EOF'
## Summary

- Add `m0002_drop_advisory_status` migration that drops the deprecated `status` column from the `advisory` table
- The `down` method re-adds the column as a nullable string for rollback support
- Register the new migration in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Test that the migration runs successfully against a test database
- [ ] Test that the rollback (down) re-adds the column
- [ ] Verify that existing advisory queries still work after the column is dropped
EOF
)"
```

The PR targets `--base TC-9005` (the feature branch), NOT `--base main`. This ensures the task's changes are merged into the feature branch TC-9005, which will later be merged to main via a merge-branch bookend task.

If fork detected (upstream remote exists):

```bash
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL
2. Add comment to TC-9205 with PR link and summary of changes
3. Transition TC-9205 to In Review
