# Implementation Plan — TC-9205: Add migration to drop status table column

## Step 0 – Project Configuration validation

`claude-md-mock.md` contains all required sections under `# Project Configuration`:

- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`
  (also Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`)
- Code Intelligence: tool naming `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer; may need 30–60s to index)

Validation passes — proceed.

## Step 1 – Parsed task (TC-9205)

| Section | Value |
|---|---|
| Repository | `trustify-backend` |
| **Target Branch** | **`TC-9005`** (feature branch — the parent feature TC-9005 "incorporates" this task) |
| Target PR | none → default flow (new task branch + new PR) |
| Bookend Type | none → normal implementation (not a create-branch/merge-branch bookend) |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| API Changes | none |
| Dependencies | None |
| GitHub Issue (customfield_10747) | would be read from the issue; if present, add `Closes <owner>/<repo>#<n>` to the PR body only |
| webUrl | `https://redhat.atlassian.net/browse/TC-9205` (captured from the API response) |

All required sections are present; no clarification needed.

## Step 1.5 – Description integrity

Would fetch comments (`jira.get_issue_comments(TC-9205)`), locate the latest
`[sdlc-workflow] Description digest:` comment, compute the digest with
`python3 scripts/sha256-digest.py /tmp/desc-TC-9205.txt` and compare. If no digest comment
exists, log a warning and continue. (Not executed in this eval.)

## Step 2 – Dependencies

"Depends on: None" — nothing to verify.

## Step 3 – Jira transition (not executed in eval)

`jira.user_info()` → `jira.edit_issue(TC-9205, assignee=<accountId>)` → `jira.transition_issue(TC-9205 → In Progress)`.

## Step 4 – Code understanding (via `serena_backend`)

- `mcp__serena_backend__get_symbols_overview("migration/src/lib.rs")` — locate `Migrator` and `migrations()`.
- `mcp__serena_backend__get_symbols_overview("migration/src/m0001_initial/mod.rs")` and
  `find_symbol("Migration", include_body=true)` — the reference pattern (`DeriveMigrationName`, `MigrationTrait`, `up`/`down`, Iden enums).
- `mcp__serena_backend__find_symbol("Advisory", relative_path="migration/")` — symbol dedup check: is there an existing
  `Advisory` Iden enum (with a `Status` variant) in `m0001_initial` that could be reused?
- `mcp__serena_backend__get_symbols_overview("entity/src/advisory.rs")` — verify (per Implementation Notes and AC #4)
  that the `advisory` entity `Model` has no `status` field / `Column::Status`.
- `mcp__serena_backend__search_for_pattern("Column::Status|\\.status\\b|\"status\"", paths: entity/, modules/, common/)` —
  confirm no service/entity code reads or writes `advisory.status` (AdvisoryService, AdvisorySummary/Details, ingestor advisory graph, search service).
  If any reference is found → stop and report to the user (it would violate AC #4 and the change would break runtime queries).
- Read `CONVENTIONS.md` at repo root (`./CONVENTIONS.md`) — follow naming/test conventions and extract CI check
  commands (e.g. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) for Step 9.
- Docs identified: `README.md`, `docs/architecture.md`, `docs/api.md` — none describe the `advisory.status` column
  or the migration list in a way that needs updating (to be confirmed via `search_for_pattern("status", docs/)`).

Conventions discovered are recorded in `conventions.md`.

## Step 5 – Branch operations

Default flow with a **feature-branch** Target Branch:

```bash
git checkout TC-9005      # the Target Branch (feature branch), NOT main
git pull
git checkout -b TC-9205   # task branch named after this Jira issue
```

## Step 6 – Changes

| # | File | Action | Detail file |
|---|---|---|---|
| 1 | `migration/src/lib.rs` | Modify | `file-1-migration-lib-rs.md` |
| 2 | `migration/src/m0002_drop_advisory_status/mod.rs` | Create | `file-2-m0002-drop-advisory-status-mod-rs.md` |

Summary:
1. `lib.rs`: add `mod m0002_drop_advisory_status;` next to `mod m0001_initial;` and append
   `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in `migrations()` (after m0001, preserving order).
2. New migration `m0002_drop_advisory_status/mod.rs`: `#[derive(DeriveMigrationName)] pub struct Migration;`
   implementing `MigrationTrait`:
   - `up`: `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
   - `down`: `manager.alter_table(Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null()).to_owned()).await`
   - local `#[derive(DeriveIden)] enum Advisory { Table, Status }` (unless an exported equivalent already exists in
     m0001 — SeaORM migrations are conventionally self-contained so they stay frozen in time; decision stated in commit body).
   - Doc comments on the struct, the Iden enum and both methods.

No out-of-scope files are planned. Documentation impact: none expected (internal schema cleanup, no public API change).

## Step 7 – Tests

Test Requirements:
1. Migration runs successfully against a test database
2. Rollback (`down`) re-adds the column
3. Existing advisory queries still work after the column is dropped

Plan: add a `#[cfg(test)] mod tests` inside the new `m0002_drop_advisory_status/mod.rs` (in scope — it is a
listed file) using the project's PostgreSQL test DB bootstrap:
- `test_up_drops_status_column` — run `Migrator::up(&db, None)`; query `information_schema.columns` for
  `table_name='advisory' AND column_name='status'` and `assert_eq!(count, 0)`.
- `test_down_readds_status_column_as_nullable_string` — after up, run `Migrator::down(&db, Some(1))`; assert the
  column exists with `data_type = "character varying"` and `is_nullable = "YES"` (value-based, not just existence).
- `test_advisory_queries_work_after_drop` — after up, run `entity::advisory::Entity::find().all(&db)` (and the
  insert path used by the ingestor) and assert the inserted advisory is returned with expected id/severity values.

Each test gets a `///` doc comment and `// Given / // When / // Then` sections. Tests are distinct in setup/assertion
so they are not parameterized.

**Scope note:** the existing advisory *endpoint* integration tests live in `tests/api/advisory.rs`. Running them
(`cargo test -p tests` / the workspace) validates requirement #3 without modifying them. If the reviewer prefers
a dedicated migration test file under `tests/`, that file is **not** listed in Files to Create and would be flagged
for user approval in Step 9 rather than added silently.

Run: `cargo test -p migration` and the advisory integration tests (`tests/api/advisory.rs`).

## Step 8 – Acceptance Criteria

| AC | Satisfied by |
|---|---|
| Migration drops `status` from `advisory` | `up()` in m0002 + `test_up_drops_status_column` |
| `down` re-adds column as nullable string | `down()` uses `ColumnDef::new(Advisory::Status).string().null()` + rollback test |
| Migration registered in `migration/src/lib.rs` | `mod` decl + `Box::new(m0002_drop_advisory_status::Migration)` in `migrations()` |
| No service/entity code references `status` | Step 4 `search_for_pattern` over `entity/`, `modules/`, `common/` returns no advisory-status references |

## Step 9 – Self-verification

- Scope containment: `git diff --name-only` must show only `migration/src/lib.rs` and
  `migration/src/m0002_drop_advisory_status/mod.rs`.
- Untracked file check: `git status --short` — the new `m0002_drop_advisory_status/` dir is the only expected `??` entry and is referenced by `mod` in lib.rs.
- Dead parameters: no code removed → n/a.
- Sensitive pattern grep on `git diff --cached` — expect none.
- CI checks from CONVENTIONS.md (e.g. `cargo fmt --all -- --check`, `cargo clippy --all-targets --all-features -- -D warnings`, `cargo check`) — hard stop on any non-zero exit.
- Rust module-level tests: resolve crate via `cargo metadata --no-deps --format-version 1` → `migration` crate → `cargo test -p migration`; hard stop on failure.
- Data-flow trace: `Migrator::up` → `migrations()` vec → `m0002::Migration::up` → `ALTER TABLE advisory DROP COLUMN status` → schema persisted; reverse path for `down`. Complete.
- Query scope: DDL only, no batch record iteration → n/a.
- Contract & sibling parity: `MigrationTrait` contract (`up`, `down` with `&SchemaManager` → `Result<(), DbErr>`) honored; parity with m0001 (DeriveMigrationName, Iden enum, `.to_owned()`/`.await`); no shared entity writes; caller-site: registered via the same `Box::new(...::Migration)` pattern as m0001.

## Step 10 – Commit, push, PR

Commit:

```bash
git add migration/src/lib.rs migration/src/m0002_drop_advisory_status/mod.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the advisory.status
column, which was superseded by the severity enum and is no longer read or
written by any service or entity code. The down migration re-adds the column
as a nullable string to allow rollback.

The Advisory Iden enum is declared locally in the migration so the migration
stays self-contained and unaffected by future changes to other migrations.

Implements TC-9205"
```

Fork detection: `git remote get-url upstream 2>/dev/null`.

Push and PR — **base is the feature branch `TC-9005`, not `main`**:

```bash
git push -u origin TC-9205

# no fork:
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "<body>"

# fork detected:
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 --title "..." --body "<body>"
```

PR body:

```markdown
## Summary
- Add migration `m0002_drop_advisory_status` dropping the deprecated `advisory.status` column (replaced by `severity`)
- `down` re-adds `status` as a nullable string for rollback
- Register the migration in `migration/src/lib.rs`

Part of feature branch TC-9005.

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

Closes <owner>/<repo>#<number>   <!-- only if customfield_10747 is populated -->
```

## Step 11 – Jira update (not executed in eval)

- `jira.update_issue(TC-9205, fields={"customfield_10875": {"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"inlineCard","attrs":{"url":"<PR-URL>"}}]}]}})`
- `jira.add_comment(TC-9205, ...)` with PR link, summary of changes, note that the PR targets feature branch `TC-9005`, any deviations (none), ending with the `implement-task` comment footnote from `shared/comment-footnote.md`.
- `jira.transition_issue(TC-9205 → In Review)`.
