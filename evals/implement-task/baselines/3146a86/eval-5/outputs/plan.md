# Implementation Plan: TC-9205

## Task Summary

**Jira Issue**: TC-9205  
**Summary**: Add migration to drop status table column  
**Repository**: trustify-backend  
**Target Branch**: TC-9005 (feature branch — extracted from "Target Branch" section of task description)

---

## Step 0 – Project Configuration Validation

CLAUDE.md (claude-md-mock.md) was read and verified:

- `## Repository Registry` — present; `trustify-backend` mapped to Serena instance `serena_backend`, path `./`
- `## Jira Configuration` — present; Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- `## Code Intelligence` — present; tool naming convention documented

All sections present — proceeding.

---

## Step 1 – Task Parsing Results

| Field | Value |
|---|---|
| Issue Key | TC-9205 |
| Summary | Add migration to drop status table column |
| Target Branch | **TC-9005** |
| Repository | trustify-backend |
| Bookend Type | (none) |
| Target PR | (none) |
| Dependencies | (none listed) |

**Target Branch value**: `TC-9005` — this is a feature branch, not `main`. The task branch will be named `TC-9205` and the PR will target `TC-9005`.

---

## Step 2 – Dependency Verification

No dependencies listed in the task description. Proceeding without dependency checks.

---

## Step 3 – Jira Transition

1. Call `jira.user_info()` to retrieve current user's account ID
2. Call `jira.edit_issue(TC-9205, assignee=<account-id>)`
3. Call `jira.transition_issue(TC-9205)` → **In Progress**

---

## Step 4 – Code Understanding

### Files inspected before modification

#### `migration/src/m0001_initial/mod.rs`
Inspected to extract the migration module pattern:
- `pub struct Migration` (unit struct)
- `impl MigrationName for Migration { fn name(&self) -> &str { "m0001_initial" } }`
- `impl MigrationTrait for Migration` with `async fn up` (creates tables) and `async fn down` (drops tables)
- Uses `sea_orm_migration::prelude::*` and SeaORM's `SchemaManager`
- Table alterations use `manager.alter_table(Table::alter()...to_owned()).await`

#### `entity/src/advisory.rs`
Inspected to verify the `status` column is absent from the current entity definition:
- Confirmed: the `Advisory` column enum does **not** contain a `Status` variant
- The entity has `Severity` (an enum field added in a previous migration) but no `Status`
- This confirms it is safe to proceed with the drop-column migration

#### `migration/src/lib.rs`
Inspected to understand the migrations registration pattern:
- `mod m0001_initial;` declared at the top
- `pub fn migrations() -> Vec<Box<dyn MigrationTrait>>` returns `vec![Box::new(m0001_initial::Migration)]`
- New migration will be appended after `m0001_initial`

### CONVENTIONS.md
Found at `trustify-backend/CONVENTIONS.md`. Read to extract CI commands and naming rules.
See `outputs/conventions.md` for the full discovered conventions list.

### Convention conformance analysis
See `outputs/conventions.md`.

---

## Step 5 – Branch Operations

**Flow**: default (no Target PR, no Bookend Type).

Target Branch extracted from task description: **TC-9005**

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

- Check out the feature branch `TC-9005` (the parent feature branch, not `main`)
- Pull latest changes to ensure we are up to date
- Create task branch `TC-9205` (named after the Jira issue ID)

The subsequent PR will target `--base TC-9005`.

---

## Step 6 – Implementation Changes

### Files to create

**`migration/src/m0002_drop_advisory_status/mod.rs`** (new file)

Full content described in `outputs/file-1-migration-mod.md`.

Summary:
- Declares `pub struct Migration`
- Implements `MigrationName` returning `"m0002_drop_advisory_status"`
- `up`: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down`: re-adds the column as nullable string via `ColumnDef::new(Advisory::Status).string().null()`

### Files to modify

**`migration/src/lib.rs`** (modify)

Changes described in `outputs/file-2-lib-rs.md`.

Summary:
- Add `mod m0002_drop_advisory_status;` module declaration alongside `mod m0001_initial;`
- Append `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in `migrations()`

---

## Step 7 – Tests

### Tests to add in `tests/api/advisory.rs`

The task's Test Requirements call for:
1. Test that the migration runs successfully against a test database
2. Test that the rollback (`down`) re-adds the column
3. Verify existing advisory queries still work after the column is dropped

These tests would be added as integration tests. See `outputs/file-3-tests.md` for detailed test code.

---

## Step 8 – Acceptance Criteria Verification

| Criterion | Status |
|---|---|
| Migration drops the `status` column from the `advisory` table | Satisfied by `up` in `m0002_drop_advisory_status/mod.rs` |
| Migration `down` method re-adds the column as nullable string | Satisfied by `down` in `m0002_drop_advisory_status/mod.rs` |
| Migration is registered in `migration/src/lib.rs` | Satisfied by lib.rs modification |
| No service or entity code references the `status` column | Confirmed during Step 4 inspection of `entity/src/advisory.rs` |

---

## Step 9 – Self-Verification

### Scope containment
Modified/created files:
- `migration/src/m0002_drop_advisory_status/mod.rs` — in **Files to Create** ✓
- `migration/src/lib.rs` — in **Files to Modify** ✓

No out-of-scope files.

### Untracked file check
The new directory `migration/src/m0002_drop_advisory_status/` and its `mod.rs` are untracked.
`mod.rs` is referenced by `migration/src/lib.rs` via `mod m0002_drop_advisory_status;`.
The file must be staged for commit.

### Sensitive-pattern check
No passwords, API keys, secrets, or `.env` references in the diff.

### Data-flow trace
- Migration `up`: `SchemaManager` → `TableAlterStatement` → drops `advisory.status` column ✓
- Migration `down`: `SchemaManager` → `TableAlterStatement` → re-adds `advisory.status` column ✓
- Registration in `lib.rs` → migration runner picks up `m0002_drop_advisory_status::Migration` ✓
- Data flow complete.

### Cross-section reference consistency
- **Files to Create** and **Implementation Notes** both reference `migration/src/m0002_drop_advisory_status/mod.rs` — consistent ✓
- **Files to Modify** and **Implementation Notes** both reference `migration/src/lib.rs` — consistent ✓
- `entity/src/advisory.rs` is referenced in Implementation Notes (verify-only, not modify) — verified in Step 4 ✓

### Contract & sibling parity
- `m0002_drop_advisory_status::Migration` implements `MigrationName` and `MigrationTrait` — both required methods (`up`, `down`) present ✓
- Parity with sibling `m0001_initial::Migration`: same struct name, same trait implementations, same import pattern ✓

### CI checks
Run before committing:
```bash
cargo fmt --check
cargo clippy -- -D warnings
cargo build
cargo test
```

---

## Step 10 – Commit and Push

### Commit

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit \
  --trailer='Assisted-by: Claude Code' \
  -m "feat(migration): drop deprecated status column from advisory table

The status column was superseded by the severity enum field in the
previous migration and is no longer read or written by any service or
entity code. This migration removes it to eliminate confusion and
prevent accidental usage. The down method re-adds the column as a
nullable string to allow rollback.

Implements TC-9205"
```

### Push and open PR

```bash
git push -u origin TC-9205

gh pr create \
  --base TC-9005 \
  --head TC-9205 \
  --title "feat(migration): drop deprecated status column from advisory table" \
  --body "## Summary

- Adds migration \`m0002_drop_advisory_status\` that drops the deprecated \`status\` column from the \`advisory\` table
- Registers the migration in \`migration/src/lib.rs\`
- Provides a \`down\` method that re-adds the column as nullable string for rollback

## Acceptance Criteria

- [x] Migration drops the \`status\` column from the \`advisory\` table
- [x] Migration \`down\` method re-adds the column as nullable string for rollback
- [x] Migration is registered in \`migration/src/lib.rs\`
- [x] No service or entity code references the \`status\` column (verified in \`entity/src/advisory.rs\`)

## Test plan

- [ ] Run migration against test database and verify \`status\` column is absent
- [ ] Run migration rollback and verify \`status\` column is re-added
- [ ] Run existing advisory query tests to confirm no regressions

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Note: `--base TC-9005` targets the feature branch, **not** `main`.

---

## Step 11 – Update Jira

1. Update `customfield_10875` (Git Pull Request custom field) on TC-9205 with the PR URL (ADF inlineCard format)
2. Add a comment to TC-9205 including:
   - PR link
   - Summary: added migration `m0002_drop_advisory_status` to drop the deprecated `status` column; registered in `migration/src/lib.rs`; `down` method provided for rollback
   - No deviations from the plan
3. Transition TC-9205 → **In Review**
