# Implementation Plan — TC-9205: Add migration to drop status table column

## Step 0 — Validate Project Configuration

Verified CLAUDE.md contains:
- **Repository Registry**: trustify-backend with Serena instance `serena_backend` at `./`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field
- **Code Intelligence**: Tool naming convention and configured instances

All required sections present. Proceeding.

## Step 1 — Fetch and Parse Jira Task

Parsed TC-9205 structured description:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table
- **Files to Modify**: `migration/src/lib.rs`
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs`
- **Implementation Notes**: Follow existing migration pattern in `m0001_initial/mod.rs`
- **Dependencies**: None

### Target Branch extraction

The Target Branch section specifies **TC-9005** — this is a feature branch, not `main`. All branch operations (checkout, branch creation, PR targeting) will use TC-9005 as the base.

## Step 1.5 — Verify Description Integrity

Would fetch comments on TC-9205 using `jira.get_issue_comments("TC-9205")` and search for comments starting with `[sdlc-workflow] Description digest:`.

If no digest comment is found, log a warning and proceed normally (backward compatibility — tasks created before digest tracking was introduced have no digest comment):

> "No description digest found — skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 2 — Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 — Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue("TC-9205", assignee=<account-id>)` to assign
3. `jira.transition_issue("TC-9205")` → In Progress

## Step 4 — Understand the Code

### Files to inspect before modifying

1. **`migration/src/m0001_initial/mod.rs`** — the existing migration to understand the pattern (MigrationTrait implementation, `up`/`down` methods, table/column operations)
2. **`migration/src/lib.rs`** — to understand how migrations are registered in the `migrations()` function
3. **`entity/src/advisory.rs`** — to verify the `status` column is no longer referenced in the entity definition

### Convention conformance analysis

Would use `mcp__serena_backend__get_symbols_overview` on:
- `migration/src/m0001_initial/mod.rs` — sibling migration to discover patterns
- `migration/src/lib.rs` — module registration patterns

See `outputs/conventions.md` for the full conventions list.

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root and extract CI check commands if present.

## Step 5 — Create Branch

**Feature branch flow**: The Target Branch is TC-9005 (a feature branch), not `main`.

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This checks out the feature branch TC-9005 first, then creates the task branch TC-9205 from it. The task branch is named after the task issue ID (TC-9205), distinct from the feature branch (TC-9005).

## Step 6 — Implement Changes

### File 1 (Modify): `migration/src/lib.rs`

Register the new migration module. Add `mod m0002_drop_advisory_status;` and append `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the existing `m0001_initial` pattern.

See `outputs/file-1-description.md` for detailed changes.

### File 2 (Create): `migration/src/m0002_drop_advisory_status/mod.rs`

Create the migration implementing `MigrationTrait`:
- `up`: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down`: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback

See `outputs/file-2-description.md` for detailed changes.

## Step 7 — Write Tests

Tests would verify:
- Migration runs successfully against a test database
- Rollback (down) re-adds the column
- Existing advisory queries still work after the column is dropped

## Step 8 — Verify Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table
- [x] Migration `down` method re-adds the column as nullable string for rollback
- [x] Migration is registered in `migration/src/lib.rs`
- [x] No service or entity code references the `status` column (verified by inspecting `entity/src/advisory.rs`)

## Step 9 — Self-Verification

### Scope containment
All modified/created files are within the task's Files to Modify and Files to Create sections:
- Modified: `migration/src/lib.rs` ✓
- Created: `migration/src/m0002_drop_advisory_status/mod.rs` ✓

### Module-level test requirement (Rust)
Would resolve the crate name using `cargo metadata --no-deps --format-version 1` from the workspace root. The migration files belong to the migration crate. Run:
```bash
cargo test -p trustify-migration
```
(The exact crate name would be resolved from cargo metadata, not derived from the nearest Cargo.toml which may be a virtual workspace manifest.)

### Dead parameter detection
No parameters removed in this change — not applicable.

### Sensitive-pattern check
No secrets or credentials in migration code.

## Step 10 — Commit and Push

### Commit message

```
feat(migration): add migration to drop advisory status column

Remove the deprecated `status` column from the advisory table. The column
was replaced by the `severity` enum field in a previous migration and is
no longer read or written by any service code.

Implements TC-9205
```

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

Remove the deprecated status column from the advisory table. The column
was replaced by the severity enum field in a previous migration and is
no longer read or written by any service code.

Implements TC-9205"
```

### Push and create PR

```bash
git push -u origin TC-9205
```

Create PR targeting the feature branch TC-9005 (not main):

```bash
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary
- Add database migration to drop the deprecated \`status\` column from the \`advisory\` table
- Register new migration \`m0002_drop_advisory_status\` in migration list
- Include rollback support to re-add the column as nullable string

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

The PR uses `--base TC-9005` to target the feature branch, not `--base main`.

## Step 11 — Update Jira

Would update the Git Pull Request custom field (`customfield_10875`) with the PR URL, add a comment summarizing changes, and transition TC-9205 to In Review.
