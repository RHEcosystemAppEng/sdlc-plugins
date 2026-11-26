# Implementation Plan — TC-9205: Add migration to drop status table column

## Step 0 — Project Configuration validation

The project CLAUDE.md (claude-md-mock.md) contains all required sections:

- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`, Git Pull Request field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: `mcp__<serena-instance>__<tool>` naming, instance `serena_backend` (rust-analyzer)

Validation passes — proceed.

## Step 1 — Parsed task

| Section | Value |
|---|---|
| Key | TC-9205 |
| Repository | trustify-backend |
| Target Branch | **TC-9005** (feature-branch workflow — the parent feature issue, TC-9205 "is incorporated by TC-9005") |
| Target PR | not present |
| Bookend Type | not present (normal implementation task, not a create-branch/merge-branch bookend) |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| API Changes | none |
| Dependencies | None |
| GitHub Issue (customfield_10747) | would be read from the fetched issue; if empty, skip `Closes ...` line |
| webUrl | `https://redhat.atlassian.net/browse/TC-9205` (captured from issue response) |

All required sections are present; no clarification needed.

## Step 1.5 — Description integrity

Would fetch comments, locate the latest `[sdlc-workflow] Description digest:` comment, compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9205.txt`, and compare. If no digest comment exists, log a warning and proceed.

## Step 2 — Dependencies

"Depends on: None" — nothing to verify.

## Step 3 — Jira assignment / transition

- `jira.user_info()` → account ID
- `jira.edit_issue(TC-9205, assignee=<accountId>)`
- `jira.transition_issue(TC-9205 → In Progress)`

## Step 4 — Understand the code (via `serena_backend`)

- `mcp__serena_backend__get_symbols_overview("migration/src/lib.rs")` — confirm `Migrator` struct and `MigratorTrait::migrations()` returning `vec![Box::new(m0001_initial::Migration)]`
- `mcp__serena_backend__get_symbols_overview("migration/src/m0001_initial/mod.rs")` + `find_symbol("Migration", include_body=true)` — sibling pattern for `DeriveMigrationName`, `MigrationTrait`, `up`/`down`, `DeriveIden` enums
- `mcp__serena_backend__find_symbol("Advisory", relative_path="entity/src/advisory.rs", include_body=true)` — verify the entity `Model` has no `status` field (Implementation Notes require this verification)
- `mcp__serena_backend__search_for_pattern("status", paths: modules/, entity/, common/)` scoped to advisory code — confirm no service/entity/query references to the advisory `status` column (AC #4). If any reference is found, stop and report to the user before writing the migration.
- `mcp__serena_backend__search_for_pattern("enum Advisory|Advisory::Status")` in `migration/` — symbol deduplication: check whether an `Advisory` `DeriveIden` enum already exists. In SeaORM, iden enums are conventionally private per migration module, so the new migration defines its own local `Advisory { Table, Status }` enum (sharing the m0001 private enum would couple migrations, which is discouraged since old migrations must remain frozen).
- Read `CONVENTIONS.md` at repo root — extract CI check commands (e.g. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) for Step 9.
- Documentation candidates: `README.md`, `CONVENTIONS.md`, `docs/architecture.md` — no doc impact expected (schema-internal change; no public API change).

Conventions discovered are listed in `conventions.md`.

## Step 5 — Branch operations (feature-branch workflow)

Target Branch is `TC-9005` (not `main`), and there is no Target PR or Bookend Type, so the default flow applies with the feature branch as base:

```
git checkout TC-9005
git pull
git checkout -b TC-9205
```

The task branch `TC-9205` is created from the feature branch `TC-9005`, **not** from `main`.

## Step 6 — Changes

| # | File | Action | Detail file |
|---|---|---|---|
| 1 | `migration/src/m0002_drop_advisory_status/mod.rs` | Create | `file-1-m0002-drop-advisory-status.md` |
| 2 | `migration/src/lib.rs` | Modify | `file-2-migration-lib-registration.md` |

Summary:
1. New migration module `m0002_drop_advisory_status` implementing `MigrationTrait`:
   - `up`: `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
   - `down`: `manager.alter_table(Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null()).to_owned()).await`
   - local `#[derive(DeriveIden)] enum Advisory { Table, Status }` with doc comments
   - inline `#[cfg(test)]` tests (see Step 7)
2. `migration/src/lib.rs`: add `mod m0002_drop_advisory_status;` and append `Box::new(m0002_drop_advisory_status::Migration)` after `m0001_initial` in `migrations()` vec.

No other files are touched (no entity changes — the entity already lacks `status`).

## Step 7 — Tests

Test Requirements:
1. Migration runs successfully against a test database
2. Rollback (`down`) re-adds the column
3. Existing advisory queries still work after the column is dropped

Plan:
- Tests 1 & 2 are placed in a `#[cfg(test)] mod tests` inside `migration/src/m0002_drop_advisory_status/mod.rs` (within the Files to Create scope), using the project's PostgreSQL test DB bootstrap, running `Migrator::up`, inspecting `information_schema.columns` for `advisory.status`, then `Migrator::down(db, Some(1))` and asserting the column is back with `is_nullable = 'YES'` and `data_type = 'character varying'` (value-based assertions, not just counts).
- Test 3 is covered by the existing integration suite `tests/api/advisory.rs` (which runs against a fully-migrated DB, now including m0002) — run it unchanged: `cargo test -p tests --test advisory` (or the actual package name resolved via `cargo metadata`). No new file in `tests/` is created because it is not listed in Files to Create; if the reviewer wants a dedicated regression test there, it will be flagged as an out-of-scope addition for user approval.
- Every test has a `///` doc comment and Given/When/Then sections.

Run: `cargo test -p migration` and `cargo test -p <tests-crate>` (advisory tests).

## Step 8 — Acceptance criteria

| AC | How satisfied |
|---|---|
| Migration drops `status` from `advisory` | `up()` drop_column |
| `down` re-adds nullable string | `ColumnDef::new(Advisory::Status).string().null()` |
| Registered in `migration/src/lib.rs` | `Box::new(m0002_drop_advisory_status::Migration)` in vec |
| No service/entity code references `status` | verified via Serena search in Step 4 |

## Step 9 — Self-verification

- Scope containment: `git diff --name-only` must show only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`.
- Untracked file check: `git status --short` — only the new `m0002_drop_advisory_status/mod.rs` (it is referenced by `mod` in lib.rs and is in scope).
- Sensitive-pattern check on `git diff --cached` — none expected.
- CI checks from CONVENTIONS.md (e.g. `cargo fmt --check`, `cargo clippy ...`, `cargo check`) — hard stop on any non-zero exit.
- Module-level Rust tests: resolve crate names via `cargo metadata --no-deps --format-version 1` → `cargo test -p migration`.
- Data-flow trace: Migrator::migrations() → m0002 `up` → ALTER TABLE advisory DROP COLUMN status → schema; rollback path `down` → ADD COLUMN status VARCHAR NULL. Complete.
- Query-scope: not a batch data operation — N/A.
- Contract & sibling parity: `MigrationTrait` requires `up` and `down` — both implemented; `DeriveMigrationName` derive matches m0001; registration matches m0001; no cross-module entity writes; caller-site N/A.
- Dead parameters / validated-value overrides: N/A.

## Step 10 — Commit and PR

Commit:

```
git add migration/src/lib.rs migration/src/m0002_drop_advisory_status/mod.rs
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the advisory.status
column, which was superseded by the severity enum and is no longer read or
written by service or entity code. The down migration re-adds the column as
a nullable string to allow rollback.

Implements TC-9205"
```

Push and PR (fork detection first via `git remote get-url upstream`):

```
git push -u origin TC-9205
# no fork:
gh pr create --base TC-9005 --head TC-9205 --title "feat(migration): drop deprecated status column from advisory table" --body "<body>"
# fork detected:
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 ...
```

The PR targets the feature branch **`TC-9005`**, not `main`.

PR body:

```
## Summary
- Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- `down` re-adds `status` as a nullable string for rollback
- Register the migration in `migration/src/lib.rs`

## Test plan
- [ ] `cargo test -p migration` (up/down migration tests)
- [ ] Advisory integration tests in `tests/api/advisory.rs` pass against the migrated schema

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
Closes <owner>/<repo>#<number>   <- only if customfield_10747 is populated

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Step 11 — Jira update

- `jira.update_issue(TC-9205, fields={"customfield_10875": {"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"inlineCard","attrs":{"url":"<PR-URL>"}}]}]}})`
- `jira.add_comment(TC-9205, ...)` — PR link, summary of changes, deviations (none; note that test #3 relies on existing integration suite), ending with the footnote from `shared/comment-footnote.md` for skill `implement-task`.
- `jira.transition_issue(TC-9205 → In Review)`
