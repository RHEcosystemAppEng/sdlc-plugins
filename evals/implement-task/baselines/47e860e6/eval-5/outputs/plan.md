# Implementation Plan — TC-9205: Add migration to drop status table column

## Step 0 — Project Configuration validation

The project CLAUDE.md (claude-md-mock.md) includes everything the skill requires:
- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- Code Intelligence: tool naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer)

Result: validation passes, so execution continues.

## Step 1 — Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `TC-9005` (feature-branch workflow; the parent feature is TC-9005, "is incorporated by TC-9005") |
| Target PR | not present, so this is not a review-feedback fix |
| Bookend Type | not present, so this is a normal implementation task, not create-branch/merge-branch |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| API Changes | none |
| Dependencies | None |
| GitHub Issue (customfield_10747) | would be read from the fetched issue. If it has a value, add `Closes <owner>/<repo>#<n>` to the PR body only |
| webUrl | `https://redhat.atlassian.net/browse/TC-9205` (captured from the issue response for the PR link) |

All required sections are present, so there is no need to stop for clarification.

## Step 1.5 — Description integrity
Would fetch comments and look for `[sdlc-workflow] Description digest:`. Then compute the digest with `python3 scripts/sha256-digest.py` and compare. In this eval no comments are available, so the log entry would read: "No description digest found — skipping integrity check."

## Step 2 — Dependencies
"Depends on: None", so there is nothing to verify.

## Step 3 — Jira (simulated, not executed)
- `jira.user_info()` to get the account ID
- `jira.edit_issue(TC-9205, assignee=<accountId>)`
- `jira.transition_issue(TC-9205 → In Progress)`

## Step 4 — Understand the code (would use `mcp__serena_backend__*`)
- `get_symbols_overview("migration/src/lib.rs")` to find the `Migrator` struct and the `MigratorTrait::migrations()` impl
- `get_symbols_overview` / `find_symbol(include_body=true)` on `migration/src/m0001_initial/mod.rs` to get the `Migration` struct, the `MigrationTrait` impl (`up`/`down`) and the `DeriveIden` enums
- Verify the Implementation Notes claim: `get_symbols_overview("entity/src/advisory.rs")` plus `search_for_pattern("status", relative_path="entity/src/advisory.rs")` to confirm the `Model` has no `status` field
- Acceptance check: `search_for_pattern("\\bstatus\\b", paths: modules/, entity/, common/)`. This confirms that no service or entity code reads or writes `advisory.status`. If a reference turns up, stop and report it.
- Symbol deduplication: `search_for_pattern("enum Advisory")` in `migration/src/` checks whether an `Advisory` iden enum already exists (e.g. in m0001_initial). The m0001 enum is private to its module, and each SeaORM migration conventionally declares its own iden enum so that it does not drift when later migrations change. So m0002 declares a local `Advisory { Table, Status }` enum. This is the same crate, so the guidance to make it `pub` and reuse it would also be possible. The local enum was chosen because migrations are meant to be immutable snapshots. This decision is noted in the PR description.
- Read `CONVENTIONS.md` at the repo root (`./CONVENTIONS.md`) to pick up naming rules and the CI check commands. Expected commands: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`, plus tests.
- Documentation files: `README.md`, `CONVENTIONS.md`, `docs/architecture.md`. The change does not touch public APIs, configuration or setup, so no doc updates are expected.
- Sibling conventions are in `conventions.md`.

## Step 5 — Branch operations (feature-branch workflow)
The default flow applies (no Target PR, no Bookend). The base is the Target Branch `TC-9005`, **not** `main`:

```
git checkout TC-9005
git pull
git checkout -b TC-9205
```

## Step 6 — Changes
1. **Create** `migration/src/m0002_drop_advisory_status/mod.rs` (details in `file-1-m0002-drop-advisory-status.md`)
   - `#[derive(DeriveMigrationName)] pub struct Migration;`
   - `up`: `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
   - `down`: `manager.alter_table(Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null()).to_owned()).await`
   - local `#[derive(DeriveIden)] enum Advisory { Table, Status }`
   - doc comments on the module, the struct and the iden enum
2. **Modify** `migration/src/lib.rs` (details in `file-2-migration-lib.md`)
   - add `mod m0002_drop_advisory_status;`
   - append `Box::new(m0002_drop_advisory_status::Migration)` after `Box::new(m0001_initial::Migration)` in the `migrations()` vec. Order matters because SeaORM applies migrations in vector order.

There are no API changes and no OpenAPI changes.

## Step 7 — Tests
Test Requirements: (a) the migration runs against a test DB, (b) rollback re-adds the column, (c) existing advisory queries still work.

The task's Files to Create/Modify list no test file. To stay in scope, (a) and (b) would be implemented as a `#[cfg(test)] mod tests` inside the new file `migration/src/m0002_drop_advisory_status/mod.rs`. The tests use `Migrator::up`/`Migrator::down` against the PostgreSQL test database (the same infrastructure used by `tests/`) and check `information_schema.columns` for `advisory.status`. They assert the actual column values (`data_type = "character varying"`, `is_nullable = "YES"`), not just counts. Each test gets a `///` doc comment and `// Given / // When / // Then` sections.

For (c), running the existing `tests/api/advisory.rs` suite after the migration covers the requirement, and no new code is needed. If the user wants a dedicated new regression test, it belongs in `tests/api/advisory.rs`. That file is **out of scope**, so it would be flagged for user approval in Step 9 rather than added on my own.

Commands: `cargo test -p migration` (crate name resolved via `cargo metadata --no-deps --format-version 1`), then `cargo test -p tests` for the advisory API suite.

## Step 8 — Acceptance criteria
- [x] Drops `status` from `advisory`: `up`
- [x] `down` re-adds it as a nullable string: `ColumnDef::new(Advisory::Status).string().null()`
- [x] Registered in `migration/src/lib.rs`
- [x] No service/entity references: confirmed by the Step 4 search (would stop and report if any are found)

## Step 9 — Self-verification
- Scope containment: `git diff --name-only` should list only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`. The optional new test in `tests/api/advisory.rs` is out of scope and would need user approval.
- Untracked check: the new directory `migration/src/m0002_drop_advisory_status/` is untracked. It is referenced by `mod m0002_drop_advisory_status;` in lib.rs, so it is staged with explicit acknowledgement.
- Sensitive-pattern grep on the staged diff: no matches expected.
- Dead parameters: none (no code removed).
- CI checks from CONVENTIONS.md (fmt, clippy, check). Any non-zero exit is a hard stop.
- Rust module tests: `cargo test -p migration` is a hard stop on failure.
- Data-flow trace: migrator binary/`Migrator::up` → `m0002::up` → `ALTER TABLE advisory DROP COLUMN status` → schema persisted. Rollback runs `ALTER TABLE advisory ADD COLUMN status varchar NULL`. The flow is complete.
- Query-scope: not a batch data operation, so this does not apply.
- Contract & sibling parity: `MigrationTrait` contract (`up`, `down` with `&SchemaManager` → `Result<(), DbErr>`) is satisfied. Parity with m0001: same `DeriveMigrationName`, `#[async_trait::async_trait]`, iden enum style. Cross-module entity: `entity/src/advisory.rs` has no `status`, so it stays consistent. Caller-site: registered in the `migrations()` vec exactly like m0001.

## Step 10 — Commit, push, PR

Commit:
```
git add migration/src/lib.rs migration/src/m0002_drop_advisory_status/mod.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status which drops the unused
advisory.status column (superseded by the severity enum). The down
migration re-adds it as a nullable string to allow rollback.

Implements TC-9205"
```

Push and fork detection:
```
git push -u origin TC-9205
git remote get-url upstream 2>/dev/null
```

PR, targeting the **feature branch TC-9005** (not main):
- No fork: `gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."`
- Fork: `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 ...`

PR body includes:
- Summary bullets of the changes
- A note on the local `Advisory` iden enum (reuse vs duplication rationale)
- `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)`
- `Closes <owner>/<repo>#<n>`, only if customfield_10747 has a value
- `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

## Step 11 — Jira update (simulated)
- `jira.update_issue(TC-9205, {"customfield_10875": {ADF doc with inlineCard url=<PR-URL>}})`
- `jira.add_comment` with the PR link, a summary of the changes, deviations (none, apart from the in-file test placement), and the footnote from `shared/comment-footnote.md` with skill name `implement-task`
- `jira.transition_issue(TC-9205 → In Review)`
