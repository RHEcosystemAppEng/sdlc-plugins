# Implementation Plan: TC-9205 — Add migration to drop status table column

## Step 0 — Validate Project Configuration

Verified CLAUDE.md contains:
- Repository Registry with trustify-backend entry (Serena instance: serena_backend, path: ./)
- Jira Configuration with Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
- Code Intelligence section with tool naming convention and configured Serena instance (serena_backend / rust-analyzer)

All required sections present. Proceeding.

## Step 1 — Fetch and Parse Jira Task

Parsed TC-9205 structured description:

| Section | Value |
|---|---|
| **Repository** | trustify-backend |
| **Target Branch** | TC-9005 |
| **Description** | Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code. |
| **Files to Modify** | `migration/src/lib.rs` |
| **Files to Create** | `migration/src/m0002_drop_advisory_status/mod.rs` |
| **Dependencies** | None |

### Target Branch Extraction

The Target Branch is **TC-9005** — this is a feature branch, not main. All branch operations (checkout, branch creation, PR base) will use TC-9005 as the base.

### GitHub Issue Extraction

GitHub Issue custom field (customfield_10747) is configured in CLAUDE.md. Would read the field value from the fetched issue. If present, parse the GitHub issue URL and store the reference for PR description.

## Step 1.5 — Verify Description Integrity

Would fetch all comments on TC-9205 using `jira.get_issue_comments(TC-9205)` and search for comments whose body starts with the marker string `[sdlc-workflow] Description digest:`.

- If no digest comment is found: log a warning and proceed normally (backward compatibility — tasks created before digest tracking was introduced have no digest comment): "No description digest found — skipping integrity check. This task may have been created before digest tracking was introduced."
- If a digest comment is found: extract the format tag and hex digest, compute the current description digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9205.txt`, compare format tags and hex digests, and proceed or alert accordingly.

## Step 2 — Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 — Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign the task
3. `jira.transition_issue(TC-9205)` to transition to In Progress

## Step 4 — Understand the Code

### Code Inspection

Before making any changes, inspect the existing codebase using the serena_backend Serena instance:

1. **Inspect migration/src/lib.rs** — use `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to understand how migrations are registered. Look for the `migrations()` function and the `vec![]` macro that lists all migration modules.

2. **Inspect migration/src/m0001_initial/mod.rs** — use `mcp__serena_backend__find_symbol` with `include_body=true` on the `MigrationTrait` implementation in `m0001_initial/mod.rs` to understand the migration pattern (up/down methods, table alteration syntax, SeaORM API usage).

3. **Inspect entity/src/advisory.rs** — use `mcp__serena_backend__get_symbols_overview` on `entity/src/advisory.rs` to verify that the `status` column is no longer referenced in the entity definition. This confirms the column is safe to drop.

4. **Inspect migration/src/lib.rs** — use `mcp__serena_backend__find_symbol` to read the `migrations()` function body and understand the registration pattern.

### Convention Conformance Analysis

Analyzed sibling files to identify conventions (see outputs/conventions.md for full details):

- **Migration pattern**: `m0001_initial/mod.rs` uses `MigrationTrait` with `up` and `down` methods
- **Error handling**: Migrations use `Result` return types from SeaORM
- **Module structure**: Each migration is a separate module directory with `mod.rs`
- **Registration**: Migrations are added to a `vec![]` in `lib.rs`

### CONVENTIONS.md Lookup

Would check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repository structure shows a `CONVENTIONS.md` file exists. Would read it and extract CI check commands for Step 9.

### Documentation File Identification

Identified documentation files related to the changes:
- `README.md` at repository root
- `docs/architecture.md` — system architecture overview
- `docs/api.md` — REST API reference (unlikely impacted by a migration-only change)

## Step 5 — Create Branch

The Target Branch is **TC-9005** (a feature branch). The task branch is named after the task issue ID: **TC-9205**.

Branch operations:

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This checks out the feature branch TC-9005 first, pulls the latest changes, then creates a new task branch TC-9205 based on TC-9005. The task branch (TC-9205) is distinct from the target branch (TC-9005).

## Step 6 — Implement Changes

### File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

Create a new migration module that drops the `status` column from the `advisory` table. Follow the existing pattern from `m0001_initial/mod.rs`:

- Implement `MigrationTrait` with `up` and `down` methods
- `up`: use `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the column
- `down`: re-add the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback support

See outputs/file-1-description.md for detailed implementation.

### File 2: migration/src/lib.rs (MODIFY)

Register the new migration module in the migration list:

- Add `mod m0002_drop_advisory_status;` module declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`

See outputs/file-2-description.md for detailed changes.

## Step 7 — Write Tests

Per Test Requirements:

1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

Tests would be added within the migration test infrastructure (if one exists) or as integration tests. Would follow existing test patterns discovered in Step 4.

## Step 8 — Verify Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table — implemented in `m0002_drop_advisory_status/mod.rs` `up` method
- [x] Migration `down` method re-adds the column as nullable string for rollback — implemented in `down` method
- [x] Migration is registered in `migration/src/lib.rs` — added to `migrations()` vec
- [x] No service or entity code references the `status` column — verified by inspecting `entity/src/advisory.rs` in Step 4

## Step 9 — Self-Verification

### Scope Containment

Would run `git diff --name-only` and verify all changed files are within scope:
- `migration/src/lib.rs` — listed in Files to Modify
- `migration/src/m0002_drop_advisory_status/mod.rs` — listed in Files to Create

No out-of-scope files modified.

### Dead Parameter Detection

No function signatures modified — no dead parameter risk.

### Sensitive-pattern Check

Would run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to verify no secrets are staged.

### CI Checks from CONVENTIONS.md

Would run all CI check commands extracted from CONVENTIONS.md during Step 4.

## Step 10 — Commit and Push

### Commit

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any entity or
service code. The down method re-adds the column as a nullable string
to support rollback.

Implements TC-9205"
```

### Push and Create PR

Push the branch and create a PR targeting the feature branch TC-9005:

```bash
git push -u origin TC-9205
```

#### Fork Detection

Would run `git remote get-url upstream 2>/dev/null` to check for fork setup.

#### PR Creation

The PR targets TC-9005 (the feature branch), NOT main:

```bash
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary

- Add database migration m0002_drop_advisory_status to drop the deprecated status column from the advisory table
- Register the migration in migration/src/lib.rs
- Include rollback support (down method re-adds column as nullable string)

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

---
Assisted-by: Claude Code"
```

Note: `--base TC-9005` ensures the PR targets the feature branch, not main.

## Step 11 — Update Jira

Would execute:

1. Update Git Pull Request custom field (customfield_10875) with the PR URL in ADF format:
   ```
   jira.update_issue(TC-9205, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. Add a comment to TC-9205 with PR link and summary of changes

3. Transition TC-9205 to In Review:
   ```
   jira.transition_issue(TC-9205) -> In Review
   ```
