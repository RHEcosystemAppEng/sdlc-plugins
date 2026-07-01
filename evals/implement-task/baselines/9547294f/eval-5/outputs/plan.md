# Implementation Plan for TC-9205

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch)
**Parent Feature**: TC-9005
**Bookend Type**: None (standard implementation task)
**Target PR**: None
**Dependencies**: None

## Step 0 — Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID (10142), Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
- **Code Intelligence**: present, with tool naming convention and configured instances

Validation passes. Proceed.

## Step 1 — Fetch and Parse Jira Task

Parsed sections from TC-9205:
- **Repository**: trustify-backend
- **Target Branch**: TC-9005
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs` — register the new migration module
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` — migration that drops the `status` column
- **API Changes**: None
- **Implementation Notes**: Follow existing migration pattern in `m0001_initial/mod.rs`, implement `MigrationTrait`, use SeaORM `TableAlterStatement`, register in `lib.rs`
- **Acceptance Criteria**: 4 items (migration drops column, down re-adds, registered in lib.rs, no code references status)
- **Test Requirements**: 3 items (migration runs, rollback works, existing queries still work)
- **Target PR**: None
- **Bookend Type**: None
- **Dependencies**: None
- **webUrl**: `https://redhat.atlassian.net/browse/TC-9205`

## Step 1.5 — Verify Description Integrity

Would fetch comments on TC-9205 via `jira.get_issue_comments(TC-9205)` and look for a `[sdlc-workflow] Description digest:` comment. If found, compute digest using `python3 scripts/sha256-digest.py` and compare. If no digest comment found, log warning and proceed.

## Step 2 — Verify Dependencies

No dependencies listed. Proceed.

## Step 3 — Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9205 to current user via `jira.edit_issue(TC-9205, assignee=<account-id>)`
3. Transition TC-9205 to "In Progress" via `jira.transition_issue`

## Step 4 — Understand the Code

### Code Inspection

1. Use `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to understand the migration registration pattern
2. Use `mcp__serena_backend__get_symbols_overview` on `migration/src/m0001_initial/mod.rs` to understand the migration trait implementation pattern
3. Use `mcp__serena_backend__find_symbol` on `Advisory` entity in `entity/src/advisory.rs` to verify the `status` column is no longer referenced
4. Use `mcp__serena_backend__search_for_pattern` to search for `Advisory::Status` across the codebase to confirm no code references it
5. Check for `CONVENTIONS.md` at repository root — it exists per the repo structure

### Sibling Analysis

Inspect `migration/src/m0001_initial/mod.rs` as the sibling migration to understand:
- Migration struct naming pattern
- `MigrationTrait` implementation (name, up, down methods)
- SeaORM table alteration patterns
- Import conventions

### Test Sibling Analysis

Inspect `tests/api/advisory.rs` as a sibling test file to understand:
- Integration test setup patterns (database setup, teardown)
- Assertion styles
- Test naming conventions

### Documentation File Identification

- `README.md` at repository root
- `docs/architecture.md` — system architecture
- `docs/api.md` — REST API reference
- `CONVENTIONS.md` at repository root

### CONVENTIONS.md Lookup

Read `CONVENTIONS.md` at repository root and extract:
- CI check commands for Step 9
- Code generation commands
- Any project-specific conventions

## Step 5 — Branch Operations

Since Target Branch is `TC-9005` (a feature branch), not `main`:

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates the task branch `TC-9205` from the feature branch `TC-9005`.

## Step 6 — Implement Changes

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

Create the new migration module implementing `MigrationTrait` with:
- `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down` method: re-adds the `status` column as a nullable string for rollback

### File 2: `migration/src/lib.rs` (MODIFY)

Register the new migration module `m0002_drop_advisory_status` by:
- Adding `mod m0002_drop_advisory_status;` declaration
- Adding `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function

## Step 7 — Write Tests

Write migration tests that verify:
- The migration runs successfully (up)
- The rollback works (down re-adds the column)
- Existing advisory queries still work after the column is dropped

Test file would be added to the migration crate or as an integration test, following the project's test conventions.

## Step 8 — Verify Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table — verified in `m0002_drop_advisory_status/mod.rs` `up` method
- [x] Migration `down` method re-adds the column as nullable string for rollback — verified in `down` method
- [x] Migration is registered in `migration/src/lib.rs` — verified by the `mod` declaration and vec entry
- [x] No service or entity code references the `status` column — verified by searching for `Advisory::Status` across the codebase

## Step 9 — Self-Verification

### Scope Containment
Run `git diff --name-only` and verify only these files are modified/created:
- `migration/src/lib.rs` (modified)
- `migration/src/m0002_drop_advisory_status/mod.rs` (created)
- Test file(s) as appropriate

### Sensitive-Pattern Check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` — expect no matches for a migration task.

### CI Checks from CONVENTIONS.md
Run all CI check commands extracted from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`).

### Data-Flow Trace
- Migration `up`: DDL statement → drops column from advisory table → complete (DDL only, no data flow)
- Migration `down`: DDL statement → re-adds column as nullable string → complete

### Contract & Sibling Parity
- Migration implements `MigrationTrait` — verify `name()`, `up()`, and `down()` methods are all present
- Compare with `m0001_initial/mod.rs` sibling — ensure same structure

## Step 10 — Commit and Push

### Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
`status` column from the advisory table. The column was replaced by
the `severity` enum field and is no longer referenced by any code.

The down method re-adds the column as a nullable string for rollback.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

### Branch Push and PR Creation

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 \
  --title "feat(migration): add migration to drop advisory status column" \
  --body "## Summary

Add database migration (m0002_drop_advisory_status) that drops the deprecated
\`status\` column from the \`advisory\` table. The column was replaced by the
\`severity\` enum field in a previous migration and is no longer referenced.

- Migration \`up\`: drops the \`status\` column
- Migration \`down\`: re-adds it as a nullable string for rollback
- Registered in \`migration/src/lib.rs\`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

**Key branch details:**
- Task branch: `TC-9205`
- PR base (target): `TC-9005` (the feature branch, as specified in Target Branch)
- The PR targets the feature branch, NOT main

## Step 11 — Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) on TC-9205 with the PR URL in ADF format (inlineCard)
2. **Add comment** to TC-9205 with:
   - PR link
   - Summary: Added migration m0002_drop_advisory_status to drop the deprecated `status` column from the advisory table. Migration includes rollback support.
   - No deviations from the plan
   - Comment footer with sdlc-workflow/implement-task version
3. **Transition** TC-9205 to "In Review"
