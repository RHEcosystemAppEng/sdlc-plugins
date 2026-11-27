# Implementation Plan — TC-9205: Add migration to drop status table column

Skill: `sdlc-workflow:implement-task` (SKILL.md followed directly; no external calls were made — every Jira/git/Serena action below is the action that *would* be performed).

## Step 0 – Project Configuration validation
The project CLAUDE.md (claude-md-mock.md) has:
- `## Repository Registry` — `trustify-backend`, Serena instance `serena_backend`, path `./` — OK
- `## Jira Configuration` — Project key TC, Cloud ID, Feature issue type ID 10142 (also PR field `customfield_10875`, GitHub Issue field `customfield_10747`) — OK
- `## Code Intelligence` — naming convention `mcp__<serena-instance>__<tool>` — OK

Validation passes, so execution continues.

## Step 1 – Parse task and resolve mode
| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | **TC-9005** (the parent feature branch; the task "is incorporated by TC-9005") |
| Target PR | absent |
| Bookend Type | absent |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| Dependencies | None |

**Mode resolution:** there is no Target PR and no Bookend Type, so the mode is **default**. It runs Steps 1–11. The branch is created from `TC-9005` and the PR targets `TC-9005`, not `main`. Because the Target Branch is a feature branch, this task is one of several on the feature branch. It is **not** a create-branch bookend, so I do not create or push the `TC-9005` branch. A separate bookend task has already done that.

GitHub Issue field (`customfield_10747`): I would read it from the issue. The fixture has no value, so I skip it and add no `Closes` line.

## Step 1.5 – Description integrity
I would fetch the comments and look for `[sdlc-workflow] Description digest:`. The fixture has none, so I log "No description digest found — skipping integrity check" and continue.

## Step 2 – Dependencies
"Depends on: None", so there is nothing to check.

## Step 3 – Jira
`jira.user_info()` → `jira.edit_issue(TC-9205, assignee=<me>)` → `jira.transition_issue(TC-9205, In Progress)`.

## Step 4 – Understand the code (using `serena_backend`)
- `mcp__serena_backend__get_symbols_overview("migration/src/lib.rs")`: confirm `pub struct Migrator`, `impl MigratorTrait for Migrator`, `fn migrations() -> Vec<Box<dyn MigrationTrait>>`, and `mod m0001_initial;`
- `mcp__serena_backend__find_symbol("Migrator/migrations", include_body=true)`: read the `vec![Box::new(m0001_initial::Migration)]` pattern
- `mcp__serena_backend__get_symbols_overview("migration/src/m0001_initial/mod.rs")`, then `find_symbol` on `Migration`, `up`, `down`, and the `Advisory` Iden enum: this is the sibling pattern
- **Verification required by the Implementation Notes**: `mcp__serena_backend__find_symbol("Model", relative_path="entity/src/advisory.rs", include_body=true)` confirms that the entity has no `status` field. `mcp__serena_backend__search_for_pattern("status", paths: entity/, modules/fundamental/src/advisory/, modules/ingestor/src/graph/advisory/, modules/search/, common/src/db/)` confirms that no service, ingestor, search or query helper reads or writes `advisory.status` (string literals such as `"status"` in raw SQL or filter maps included). If a reference is found, **stop and report it**, because the task assumes none exist and AC4 would fail.
- Read `CONVENTIONS.md` at the repo root and extract the CI check commands (for Step 9 check 14) and any codegen commands.
- Documentation files: `README.md`, `CONVENTIONS.md`, `docs/architecture.md`. None describe individual columns, so no doc impact is expected. `docs/api.md` is unaffected because API response shapes do not change (AdvisorySummary uses `severity`).
- Convention analysis: see `conventions.md`.

## Step 5 – Branch operations (default mode, Target Branch = TC-9005)
```
git checkout TC-9005
git pull
git checkout -b TC-9205
```
I would not check out or branch from `main`, and I would not push `TC-9005` itself.

## Step 6 – Implementation
| # | File | Action | Detail file |
|---|---|---|---|
| 1 | `migration/src/m0002_drop_advisory_status/mod.rs` | **Create**: `Migration` struct (`DeriveMigrationName`), `MigrationTrait` impl with `up` (alter_table drop_column `Advisory::Status`) and `down` (alter_table add_column `ColumnDef::new(Advisory::Status).string().null()`), a local `Advisory` Iden enum (`Table`, `Status`), doc comments, and an inline `#[cfg(test)]` module with the migration tests | `file-1-m0002-drop-advisory-status-mod.md` |
| 2 | `migration/src/lib.rs` | **Modify**: add `mod m0002_drop_advisory_status;` and append `Box::new(m0002_drop_advisory_status::Migration)` after `m0001_initial` in `migrations()` | `file-2-migration-lib-rs.md` |

Reuse: SeaORM's `sea_orm_migration::prelude::*` (re-exported via the crate prelude, as m0001 does). There is no new helper. I declare the `Advisory` Iden enum locally in the new module rather than importing it from m0001. That follows SeaORM convention (each migration is a frozen snapshot), and m0001's enum may not have a `Status` variant or may be private. I would record this choice in the commit body.

## Step 7 – Tests
The tests go inside the new file, as a `#[cfg(test)] mod tests`, which keeps them within the declared Files to Create:
1. `/// Verifies the up migration removes the status column from advisory.`: apply migrations against a test PostgreSQL DB, then assert that `information_schema.columns` returns no `status` row for `advisory`. The value-based check compares the column name list.
2. `/// Verifies the down migration re-adds status as a nullable text column.`: run `up`, then `Migrator::down(&db, Some(1))`, then assert that the column exists with `data_type == "character varying"` and `is_nullable == "YES"`.
3. Existing advisory queries: run the existing `tests/api/advisory.rs` integration suite, which boots against the migrated DB, plus `cargo test -p` for the fundamental/ingestor crates. No new test file is planned there. Adding one would be an out-of-scope file under check 1 and would need user approval.

Given/When/Then comments and `///` doc comments go on every test. There are two cases with different assertions, so I would not parameterize them, and siblings do not use `rstest` anyway.

Potential scope flag: if `migration/Cargo.toml` lacks dev-dependencies for an async test runtime and a DB connection (`tokio` with `macros` and `rt-multi-thread`, `sea-orm` with `sqlx-postgres`), the tests need them. That would make `migration/Cargo.toml` an **out-of-scope file that needs user approval** before it is committed. If the user declines, the fallback is to put the migration tests in the existing `tests/` crate, which also needs approval.

## Step 8 – Acceptance criteria
- [x] `up` drops `advisory.status`: `drop_column(Advisory::Status)`
- [x] `down` re-adds it as a nullable string: `ColumnDef::new(Advisory::Status).string().null()`
- [x] Registered in `migration/src/lib.rs` `migrations()` after m0001
- [x] No service or entity code references `status`: confirmed by the Step 4 Serena search (a stop condition if not)

## Step 9 – Self-verification (expected results)
- 1 Scope containment: PASS if only the 2 files changed. FLAGGED if `migration/Cargo.toml` (test dev-dependencies) is needed, in which case I ask for approval.
- 2 Untracked files: the new `m0002_drop_advisory_status/` directory is the declared file, so PASS
- 3 Sensitive patterns: run on both the working tree and the index, PASS
- 4 Dead parameters: no parameters removed, does not fire
- 5 Duplication: Grep for `drop_column` / `Advisory::Status` across `migration/`. No overlap, PASS
- 6 Documentation currency: schema-only change, no public API or config change, does not fire. PASS is still expected if checked.
- 10 Cross-section references: the paths agree across Files to Create/Modify and the Implementation Notes (`m0002_drop_advisory_status`, `migration/src/lib.rs`, `entity/src/advisory.rs`), PASS
- 11 Data-flow trace: migration runner → `Migrator::migrations()` → `m0002::up` → ALTER TABLE. Rollback is `Migrator::down` → `m0002::down`. Complete, PASS
- 12 Query scope: DDL only, not a batch record iteration. Does not fire, or PASS.
- 13 Contract & sibling parity: Contract: `MigrationTrait` `up` and `down` with `&SchemaManager` → `Result<(), DbErr>`, PASS. Sibling parity with m0001 (DeriveMigrationName, `#[async_trait::async_trait]`, `manager.*().await`), PASS. Cross-module entity: `advisory` is shared by fundamental, ingestor and search; the Serena search confirms none use `status`, PASS. Caller-site: registered like m0001, PASS
- 14 CI checks: every command from CONVENTIONS.md (typically `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`), hard stop on failure
- 15 Module tests (Rust): `cargo metadata --no-deps --format-version 1` resolves `migration/src/*` → package `migration`, so I run `cargo test -p migration`. I also run the `tests` package (`cargo test -p tests`, or whatever name metadata reports) to confirm the advisory API tests still pass.
- 16 Validated values: does not fire

## Step 10 – Commit, push, PR
Commit:
```
git add migration/src/lib.rs migration/src/m0002_drop_advisory_status/mod.rs
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the advisory.status
column, superseded by the severity enum field. The down migration re-adds
it as a nullable string column so the change can be rolled back. The
Advisory Iden enum is declared locally in the migration (not imported from
m0001_initial) so each migration remains a frozen schema snapshot.

Implements TC-9205"
```
Fork detection: `git remote get-url upstream`.
Push and PR:
```
git push -u origin TC-9205
gh pr create --base TC-9005 --head TC-9205 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
# fork variant: gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 ...
```
The PR body starts with `Implements [TC-9205](https://<site>.atlassian.net/browse/TC-9205)`, using the issue's `webUrl`. It then has a summary of the changes and the test results. There is no `Closes` line because the GitHub Issue field is empty. The PR **targets `TC-9005`**, not `main`. The feature branch is merged to main later by the merge-branch bookend task.

## Step 11 – Jira
- Set `customfield_10875` to the PR URL as ADF (`inlineCard`).
- Add a comment with the PR link, a summary of the changes (new migration m0002 plus its registration), and deviations (any approved out-of-scope file such as `migration/Cargo.toml`, plus the local Iden enum choice). It ends with the rule and the "This comment was AI-generated by sdlc-workflow/implement-task v0.14.0." footnote.
- Transition TC-9205 to **In Review**.
