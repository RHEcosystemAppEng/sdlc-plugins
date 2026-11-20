# Implementation Plan — TC-9205: Add migration to drop status table column

## Step 0 — Project Configuration validation

The project CLAUDE.md (claude-md-mock.md) contains all required sections:
- Repository Registry: `trustify-backend` → Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`,
  Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- Code Intelligence: tool naming convention `mcp__<serena-instance>__<tool>`; limitation: rust-analyzer
  may take 30-60s to index on first use

Validation passes — proceed.

## Step 1 — Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | **TC-9005** (feature branch — feature-branch workflow, not main) |
| Target PR | not present |
| Bookend Type | not present (normal implementation task) |
| Dependencies | None |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| GitHub Issue (customfield_10747) | would be read from the issue; if empty, skipped (not present in fixture) |

All required sections are present (Repository, Target Branch, Description, Files to Modify,
Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies).
The task is linked as "is incorporated by TC-9005" — TC-9005 is the parent feature whose ID
is the feature branch name.

## Step 1.5 — Description integrity (would do)

`jira.get_issue_comments(TC-9205)`, find most recent comment starting with
`[sdlc-workflow] Description digest:`, compute digest with `python3 scripts/sha256-digest.py`
and compare. If no digest comment: warn and proceed. (Not executed in eval.)

## Step 2 — Dependencies

"Depends on: None" — nothing to verify. (Optionally confirm the feature branch `TC-9005`
exists on the remote, which implies the create-branch bookend task for TC-9005 is Done.)

## Step 3 — Jira (would do)

1. `jira.user_info()` → account ID
2. `jira.edit_issue(TC-9205, assignee=<accountId>)`
3. `jira.transition_issue(TC-9205 → In Progress)`

## Step 4 — Understand the code (Serena instance `serena_backend`)

- `mcp__serena_backend__get_symbols_overview("migration/src/lib.rs")` — locate `Migrator` struct,
  `MigratorTrait` impl, `migrations()` function and existing `mod m0001_initial;` declaration.
- `mcp__serena_backend__get_symbols_overview("migration/src/m0001_initial/mod.rs")` and
  `find_symbol("Migration", include_body=true)` — read the `MigrationTrait` impl (`up`/`down`),
  `DeriveMigrationName`, and the `Iden` enum pattern used for table/column identifiers.
- `mcp__serena_backend__find_symbol("Advisory", relative_path="migration/src/m0001_initial/mod.rs")`
  — check whether an `Advisory` `Iden` enum with a `Status` variant already exists (symbol
  deduplication; see conventions.md).
- Verify Implementation Note: `get_symbols_overview("entity/src/advisory.rs")` /
  `find_symbol("Model", relative_path="entity/src/advisory.rs", include_body=true)` — confirm there is
  no `status` field on the entity (only `severity`).
- `mcp__serena_backend__search_for_pattern` for `Advisory::Status`, `advisory::Column::Status`,
  `"status"` and `.status` in `modules/`, `entity/`, `common/`, `tests/` — confirm no service,
  ingestor, search or entity code references the column (Acceptance Criterion 4). If any reference
  is found, stop and report to the user (it would be out of scope to modify it).
- CONVENTIONS.md lookup: read `./CONVENTIONS.md` (exists at repo root per repo-backend.md),
  extract CI check commands (e.g., `cargo fmt --check`, `cargo clippy ...`, `cargo check`) and any
  code-generation commands for use in Step 9.
- Documentation files: `README.md`, `CONVENTIONS.md`, `docs/architecture.md` — check whether they
  describe the advisory schema / `status` column. A dropped column is not a public API change;
  expected no doc updates.
- Sibling analysis — see `conventions.md`.

## Step 5 — Branch operations (feature-branch workflow)

Target Branch is `TC-9005`, so the task branch is created from the feature branch, NOT main:

```
git checkout TC-9005
git pull
git checkout -b TC-9205
```

## Step 6 — Implement changes

| # | File | Action | Detail file |
|---|---|---|---|
| 1 | `migration/src/m0002_drop_advisory_status/mod.rs` | Create | `file-1-m0002-drop-advisory-status-migration.md` |
| 2 | `migration/src/lib.rs` | Modify | `file-2-migration-lib-registration.md` |

Summary:
1. New migration module implementing `MigrationTrait`:
   - `up`: `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
   - `down`: `manager.alter_table(Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null()).to_owned()).await`
   - Local `#[derive(DeriveIden)] enum Advisory { Table, Status }` (migrations conventionally keep
     their own frozen identifier enums rather than importing entity code, since the entity no longer
     has a `Status` column), with doc comments on the struct and enum.
2. `lib.rs`: add `mod m0002_drop_advisory_status;` and append
   `Box::new(m0002_drop_advisory_status::Migration)` after `m0001_initial` in the `migrations()` vec
   (order matters — SeaORM applies migrations in vec order).

No API changes, no OpenAPI changes, no documentation updates expected.

## Step 7 — Tests

Test Requirements ask for migration up/down tests and verification that advisory queries still
work. However, Files to Create / Files to Modify do not list a test file. Plan:

- Add the migration up/down tests as a `#[cfg(test)] mod tests` inside the new file
  `migration/src/m0002_drop_advisory_status/mod.rs` (in scope — the file is in Files to Create),
  if sibling `m0001_initial` / CONVENTIONS.md show in-module test usage or the migration crate has a
  test-DB helper. Tests (each with `///` doc comment and Given/When/Then comments):
  1. `/// Verifies that applying migrations drops the status column from the advisory table.`
     — run `Migrator::up(&db, None)`, query `information_schema.columns` for
     `table_name='advisory' AND column_name='status'`, `assert_eq!(count, 0)`.
  2. `/// Verifies that rolling back m0002 re-adds status as a nullable string column.`
     — `Migrator::up`, then `Migrator::down(&db, Some(1))`, query `information_schema.columns`
     and `assert_eq!((data_type, is_nullable), ("character varying".into(), "YES".into()))`
     (value-based assertion, not just existence).
- "Existing advisory queries still work" — verified by running the existing integration suite
  `tests/api/advisory.rs` (which runs against a migrated PostgreSQL test DB) unchanged.
- If the project convention places migration tests elsewhere (e.g., `tests/` crate), that file is
  outside the listed scope — flag it to the user in Step 9 scope containment rather than silently
  adding it.
- Parameterized tests not used: the two tests have different actions/assertions (Meszaros heuristic).

Run: `cargo test -p migration` and `cargo test -p tests` (advisory integration tests).

## Step 8 — Acceptance Criteria

- [x] Migration drops `status` from `advisory` — `up` method.
- [x] `down` re-adds column as nullable string — `ColumnDef::new(Advisory::Status).string().null()`.
- [x] Registered in `migration/src/lib.rs` — `mod` + vec entry.
- [x] No service/entity code references `status` — verified via Step 4 searches.

## Step 9 — Self-verification

- Scope containment: `git diff --name-only` must show only `migration/src/lib.rs` and
  `migration/src/m0002_drop_advisory_status/mod.rs`.
- Untracked file check: `git status --short`; the new `m0002_drop_advisory_status/` directory is
  referenced via `mod` in lib.rs — stage it intentionally.
- Dead parameter detection: N/A (no code removed).
- Sensitive-pattern check on `git diff --cached`.
- Duplication check: confirm no other migration already drops `advisory.status`; reuse of `Advisory`
  Iden enum assessed (local frozen enum is the convention).
- CI checks from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`)
  — hard stop on any non-zero exit.
- Rust module-level tests: resolve crate via `cargo metadata --no-deps --format-version 1` (package
  `migration`), run `cargo test -p migration`.
- Data-flow trace: migrator binary/server startup → `Migrator::migrations()` → `m0002::up` →
  `ALTER TABLE advisory DROP COLUMN status` → schema; rollback path `down` → `ADD COLUMN status varchar NULL`. Complete.
- Query-scope verification: N/A (DDL, no batch record iteration).
- Contract & sibling parity: `MigrationTrait` requires `up` and `down` — both implemented with
  `DeriveMigrationName`; parity with `m0001_initial` structure; cross-module entity: `entity/src/advisory.rs`
  has no `status` — consistent; caller-site: registration follows `Box::new(<module>::Migration)` pattern.

## Step 10 — Commit and PR

Commit:

```
git add migration/src/lib.rs migration/src/m0002_drop_advisory_status/mod.rs
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the advisory.status
column, superseded by the severity enum field. The down migration re-adds
it as a nullable string to allow rollback.

Implements TC-9205"
```

Fork detection: `git remote get-url upstream 2>/dev/null`.

Push and PR — base is the feature branch `TC-9005`, NOT main:

```
git push -u origin TC-9205
# no fork:
gh pr create --base TC-9005 --head TC-9205 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
# fork detected:
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 --title "..." --body "..."
```

PR body:

```
## Summary
- Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from `advisory`
- `down` re-adds `status` as a nullable string for rollback
- Register the migration in `migration/src/lib.rs`

Part of feature TC-9005 (targets feature branch `TC-9005`).

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

(`Closes <owner>/<repo>#<n>` appended only if customfield_10747 holds a GitHub issue URL.)

## Step 11 — Jira update (would do)

- `jira.update_issue(TC-9205, fields={"customfield_10875": {ADF doc with inlineCard url=<PR-URL>}})`
- `jira.add_comment(TC-9205, ...)` — PR link, summary, deviations (none expected; note test placement
  decision), ending with the footnote from `shared/comment-footnote.md` (skill `implement-task`).
- `jira.transition_issue(TC-9205 → In Review)`
