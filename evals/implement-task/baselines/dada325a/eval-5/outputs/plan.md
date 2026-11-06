# Implementation Plan — TC-9205: Add migration to drop status table column

## Step 0 — Project Configuration validation

The project CLAUDE.md (claude-md-mock.md) has everything the skill needs:
- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142, plus
  Git Pull Request custom field `customfield_10875` and GitHub Issue custom field `customfield_10747`
- Code Intelligence: tool naming `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer)

Result: valid, so execution continues.

## Step 1 — Parsed task sections

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | **TC-9005** (a feature branch, not `main`) |
| Target PR | not present, so this uses the default flow (new branch + new PR) |
| Bookend Type | not present, so this is a normal implementation task |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| API Changes | none |
| Dependencies | None |
| Linked issue | "is incorporated by TC-9005" (the parent feature, whose ID is also the feature branch name) |
| webUrl | `https://redhat.atlassian.net/browse/TC-9205` (would be taken from the `get_issue` response) |
| GitHub Issue (customfield_10747) | the field is configured but the fixture has no value, so it is skipped silently and no `Closes` line is added |

All required sections are present, so there is nothing to ask the user.

## Step 1.5 — Description integrity
I would fetch the comments and look for `[sdlc-workflow] Description digest:`. The fixture has no digest comment, so I would log the warning "No description digest found — skipping integrity check..." and continue.

## Step 2 — Dependencies
"Depends on: None", so there is nothing to check.

## Step 3 — Jira (simulated, not executed)
- `jira.user_info()` → get the account ID
- `jira.edit_issue("TC-9205", assignee=<accountId>)`
- `jira.transition_issue("TC-9205", "In Progress")`

## Step 4 — Understand the code (via `serena_backend`)
- `mcp__serena_backend__get_symbols_overview("migration/src/lib.rs")`: confirm the `Migrator` struct, `impl MigratorTrait for Migrator`, `migrations()` returning `vec![Box::new(m0001_initial::Migration)]`, and the `mod m0001_initial;` declaration.
- `mcp__serena_backend__find_symbol("Migration", relative_path="migration/src/m0001_initial/mod.rs", include_body=true)`: read the sibling pattern for `DeriveMigrationName` and `impl MigrationTrait` with `up`/`down`, and see how Iden enums are declared.
- `mcp__serena_backend__search_for_pattern("Advisory::Status|\"status\"|\\.status\\b", paths: entity/, modules/, common/)`: confirm that no entity or service code references the `status` column (Implementation Note and Acceptance Criterion 4). `entity/src/advisory.rs` must have no `status` field in its `Model`. **If a reference is found, stop and report it to the user** instead of dropping the column.
- `mcp__serena_backend__search_for_pattern("enum Advisory", paths: migration/)`: symbol deduplication for the `Advisory` Iden enum. Migrations are by convention self-contained snapshots, and m0001's Iden enum is module-private. The plan is to declare a local `#[derive(DeriveIden)] enum Advisory { Table, Status }` inside m0002, matching how m0001 declares its own idens, and not to make m0001's enum `pub` and import it. That way later edits to m0001 cannot change m0002's behavior.
- CONVENTIONS.md exists at the repo root (`./CONVENTIONS.md`). I would read it to get the CI check commands (e.g. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) and any codegen commands (e.g. OpenAPI generation). No API changes are expected from this task.
- Documentation files: `README.md`, `docs/architecture.md`. A schema column drop of an already-unused column is unlikely to affect them. I would check whether any doc describes `advisory.status` and flag it if one does. No doc changes are planned because they are not in scope.
- Sibling conventions: see `conventions.md`.

## Step 5 — Branch operations (default flow, feature-branch target)

```
git checkout TC-9005        # the Target Branch (feature branch), NOT main
git pull                    # bring the feature branch up to date
git checkout -b TC-9205     # task branch named after this Jira issue
```

The task branch is created from the feature branch `TC-9005`, not from `main`.

## Step 6 — Changes

| # | File | Action | Detail |
|---|---|---|---|
| 1 | `migration/src/lib.rs` | Modify | Add `mod m0002_drop_advisory_status;` and append `Box::new(m0002_drop_advisory_status::Migration)` after `m0001_initial` in `migrations()`. See `file-1-migration-lib-rs.md`. |
| 2 | `migration/src/m0002_drop_advisory_status/mod.rs` | Create | `Migration` struct implementing `MigrationTrait`. `up` drops `advisory.status` via `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)`. `down` re-adds it as `ColumnDef::new(Advisory::Status).string().null()`. Also contains a local `DeriveIden` enum, doc comments, and `#[cfg(test)]` migration tests. See `file-2-m0002-drop-advisory-status.md`. |

No other files would be touched.

## Step 7 — Tests

The Test Requirements ask for: (a) the migration runs against a test DB, (b) the rollback re-adds the column, and (c) existing advisory queries still work after the drop.

- (a) and (b) are covered by a `#[cfg(test)] mod tests` inside the new file `m0002_drop_advisory_status/mod.rs`, which is in scope. The tests use the same PostgreSQL test DB bootstrap as the repo's integration tests. Every test has a `///` doc comment and Given/When/Then comments, and asserts on values: the column's presence/absence in `information_schema.columns`, and its `data_type` and `is_nullable` after rollback. The tests do not just count rows.
- (c) "Existing advisory queries still work": the existing `tests/api/advisory.rs` integration suite already runs every advisory endpoint against a fully migrated DB. Once m0002 is registered, that suite exercises the dropped-column schema. The plan is to **re-run** `tests/api/advisory.rs`, not edit it. If a dedicated new test there is wanted, that file is **out of scope**, so it would be flagged in Step 9 for user approval and not edited without approval.

Commands:
```
cargo test -p migration
cargo test -p tests --test api   # or the repo's equivalent integration-test invocation, covering tests/api/advisory.rs
```
(The crate names would be resolved with `cargo metadata --no-deps --format-version 1` and not guessed from directory names.)

## Step 8 — Acceptance criteria
- [x] Migration drops `status` from `advisory`: `up` uses `drop_column(Advisory::Status)`
- [x] `down` re-adds it as a nullable string: `ColumnDef::new(Advisory::Status).string().null()`
- [x] Registered in `migration/src/lib.rs`: `mod` declaration plus a `vec![]` entry
- [x] No service or entity code references `status`: checked by the Step 4 search (this is a precondition, so a hit would stop the task)

## Step 9 — Self-verification
- Scope containment: `git diff --name-only` must list exactly `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`.
- Untracked files: the new directory `m0002_drop_advisory_status/` is intended and is referenced by `mod m0002_drop_advisory_status;`, so it is staged explicitly.
- Dead parameters: N/A because no code is removed.
- Sensitive patterns: run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` and expect no matches.
- CI checks: every command extracted from CONVENTIONS.md runs, with a hard stop on any non-zero exit.
- Rust module tests: run `cargo test -p <migration crate>`, with a hard stop on failure.
- Data-flow trace: `Migrator::migrations()` → `m0002::Migration::up` → `ALTER TABLE advisory DROP COLUMN status` → schema without the column → advisory entity/service queries (which never select `status`) still succeed. `down` reverses it with `ALTER TABLE advisory ADD COLUMN status varchar NULL`. The path is complete.
- Query scope: N/A (no batch data iteration).
- Contract and sibling parity: `MigrationTrait` is honored, with `up` and `down` both implemented with signature `async fn(&self, manager: &SchemaManager) -> Result<(), DbErr>`. `DeriveMigrationName` is used like m0001. Cross-module entity: `entity/src/advisory.rs` has no `status` field, which is consistent. Caller-site: the migration is invoked only via `Migrator`, like m0001.

## Step 10 — Commit and push

```
git add migration/src/lib.rs migration/src/m0002_drop_advisory_status/mod.rs
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status which removes the unused
advisory.status column (superseded by the severity enum). The down
migration re-adds it as a nullable string to allow rollback.

Implements TC-9205"
git push -u origin TC-9205
```

Fork detection: run `git remote get-url upstream`.
- No upstream:
  ```
  gh pr create --base TC-9005 --head TC-9205 \
    --title "feat(migration): drop deprecated status column from advisory table" \
    --body "<body below>"
  ```
- Upstream present:
  ```
  gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 ...
  ```

**The PR targets `TC-9005` (the feature branch), not `main`.**

PR body:
```
## Summary
- Add `m0002_drop_advisory_status` migration that drops the deprecated `status` column from the `advisory` table (replaced by the `severity` enum).
- `down` re-adds `status` as a nullable string column for rollback.
- Register the migration in `migration/src/lib.rs`.

## Test plan
- `cargo test -p migration`: migration up drops the column; down re-adds it as nullable varchar.
- Advisory integration tests (`tests/api/advisory.rs`) pass against the migrated schema.

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```
(No `Closes` line, because the GitHub Issue field is empty.)

## Step 11 — Jira (simulated)
- `jira.update_issue("TC-9205", {"customfield_10875": {"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"inlineCard","attrs":{"url":"<PR-URL>"}}]}]}})`
- `jira.add_comment("TC-9205", ...)`: PR link (against feature branch TC-9005), a summary of the changes, and deviations: none. The comment would note that the advisory query regression check relies on the existing `tests/api/advisory.rs` suite because that file is outside scope. It ends with the footnote from `shared/comment-footnote.md` using skill name `implement-task`.
- `jira.transition_issue("TC-9205", "In Review")`
