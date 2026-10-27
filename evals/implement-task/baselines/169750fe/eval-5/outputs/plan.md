# Implementation Plan: TC-9205 — Add migration to drop status table column

## Step 0 — Validate Project Configuration

Verified the project's CLAUDE.md contains:
- **Repository Registry**: `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key `TC`, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: `serena_backend` configured with `rust-analyzer`

All required sections present. Proceeding.

## Step 1 — Parse Task Description

Extracted from TC-9205:

| Field | Value |
|-------|-------|
| Repository | trustify-backend |
| **Target Branch** | **TC-9005** |
| Linked Issues | is incorporated by TC-9005 |

### Target Branch Extraction

The **Target Branch** section specifies `TC-9005`. This is a feature branch (not `main`), meaning this task is part of a feature-branch workflow. The task branch will be based on TC-9005, and the PR will target TC-9005.

### Sections parsed

- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table, replaced by `severity` enum.
- **Files to Modify**: `migration/src/lib.rs`
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs`
- **Implementation Notes**: Follow `m0001_initial/mod.rs` pattern, use SeaORM `TableAlterStatement`, register in `lib.rs`
- **Acceptance Criteria**: 4 criteria covering drop, rollback, registration, and no remaining references
- **Test Requirements**: 3 test cases for migration, rollback, and existing queries
- **Dependencies**: None

## Step 1.5 — Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9205)` and search for the `[sdlc-workflow] Description digest:` marker. If no digest comment is found, log a warning and proceed (backward compatibility). If found, compute digest with `python3 scripts/sha256-digest.py`, compare format tags and hex values, and proceed silently on match or alert user on mismatch.

## Step 2 — Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 — Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` — retrieve current user's account ID
2. `jira.edit_issue(TC-9205, assignee=<account-id>)` — assign task
3. `jira.transition_issue(TC-9205)` → In Progress

## Step 4 — Understand the Code

### Files to inspect before modifying

Using the Serena instance `serena_backend`:

1. **`migration/src/m0001_initial/mod.rs`** — inspect the existing migration pattern: `MigrationTrait` implementation, `up`/`down` method signatures, use of `manager.alter_table()` or `manager.create_table()`. This is the sibling migration and the primary reference for the new migration.
2. **`migration/src/lib.rs`** — inspect the `migrations()` function to understand how migrations are registered in the `vec![]` and what imports are needed.
3. **`entity/src/advisory.rs`** — verify that the `status` column is no longer referenced in the entity definition (confirming it's safe to drop).

### Convention conformance analysis

Sibling analysis of `migration/src/m0001_initial/mod.rs`:
- Implements `MigrationTrait` with async `up` and `down` methods
- Uses `SchemaManager` parameter for DDL operations
- Returns `Result<(), DbErr>`
- Module registered in `lib.rs` via `vec![]` in `migrations()` function

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`) and extract CI check commands and code generation commands if present.

## Step 5 — Create Branch

**Feature-branch workflow detected.** The Target Branch is `TC-9005` (not `main`).

Branch operations:
```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

The task branch is named `TC-9205` (the task issue ID), distinct from the Target Branch `TC-9005` (the feature branch). The task branch is based on TC-9005, not on main.

## Step 6 — Implement Changes

### Files to Modify

1. **`migration/src/lib.rs`** — Add the new migration module to the registration list

### Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** — New migration implementing `MigrationTrait`

Detailed changes are in the file-N-description.md outputs.

## Step 7 — Write Tests

Per Test Requirements:
- Test migration runs successfully against test database
- Test rollback (down) re-adds the column
- Verify existing advisory queries still work after column drop

Tests would be implemented following the integration test patterns in `tests/api/advisory.rs`.

## Step 8 — Verify Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table — implemented via `TableAlterStatement::drop_column`
- [x] Migration `down` method re-adds the column as nullable string — `ColumnDef::new(Advisory::Status).string().null()`
- [x] Migration is registered in `migration/src/lib.rs` — added to `migrations()` vec
- [x] No service or entity code references the `status` column — verified by inspecting `entity/src/advisory.rs`

## Step 9 — Self-Verification

### Scope containment
Modified/created files:
- `migration/src/lib.rs` — listed in Files to Modify ✓
- `migration/src/m0002_drop_advisory_status/mod.rs` — listed in Files to Create ✓

All changes are within scope.

### Dead parameter detection
No parameters removed — not applicable.

### Sensitive-pattern check
No secrets or credentials in the migration code.

### Module-level test requirement (Rust)
Would run `cargo metadata --no-deps --format-version 1` from the workspace root to resolve the package name for the `migration` crate. Use the resolved package `name` field (not derived from the nearest `Cargo.toml`, which may be a virtual workspace manifest). Then run:
```bash
cargo test -p <resolved-migration-crate-name>
```

### Query-scope verification
Not applicable — this is a DDL migration, not a batch data operation.

## Step 10 — Commit and Push

### Commit message
```
feat(migration): add migration to drop advisory status column

The deprecated status column was replaced by the severity enum field
in a previous migration and is no longer referenced by entity or
service code. Removing it prevents accidental usage and reduces
schema confusion.

Implements TC-9205
```

With trailer:
```bash
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

The deprecated status column was replaced by the severity enum field
in a previous migration and is no longer referenced by entity or
service code. Removing it prevents accidental usage and reduces
schema confusion.

Implements TC-9205"
```

### Push and create PR

```bash
git push -u origin TC-9205
```

Create PR targeting the **feature branch TC-9005** (not main):

```bash
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary

- Add database migration `m0002_drop_advisory_status` to drop the deprecated `status` column from the `advisory` table
- Register the new migration in `migration/src/lib.rs`
- The `down` method re-adds the column as a nullable string for rollback support

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Note: `--base TC-9005` ensures the PR targets the feature branch, not main.

## Step 11 — Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment to TC-9205 with PR link and summary of changes
3. Transition TC-9205 → In Review
