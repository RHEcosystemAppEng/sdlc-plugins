# Implementation Plan — TC-9205: Add migration to drop status table column

## Step 0 – Project Configuration validation
The project CLAUDE.md (claude-md-mock.md) contains all required sections:
- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`,
  Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- Code Intelligence: naming convention `mcp__<serena-instance>__<tool>`; instance `serena_backend` (rust-analyzer, may need 30-60s to index)

Validation passes, so execution continues.

## Step 1 – Parsed task
| Section | Value |
|---|---|
| Repository | trustify-backend |
| **Target Branch** | **`TC-9005`** (feature branch, not `main`) |
| Target PR | none, so the default flow applies (new branch + new PR) |
| Bookend Type | none, so this is a normal implementation task (not `create-branch`/`merge-branch`) |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| API Changes | none |
| Dependencies | None |
| Linked issue | is incorporated by TC-9005 (parent feature, and also the feature branch name) |
| webUrl | `https://redhat.atlassian.net/browse/TC-9205` (captured from the issue response) |
| GitHub Issue (customfield_10747) | read from issue; if empty, skip silently (no `Closes` line) |

All required sections are present, so no clarification is needed.

## Step 1.5 – Description integrity
Would call `jira.get_issue_comments(TC-9205)` and look for the latest `[sdlc-workflow] Description digest:` comment, then compute the digest with `python3 scripts/sha256-digest.py /tmp/desc-TC-9205.txt` and compare. If they match, proceed silently. If they don't match, stop and ask the user. If no digest comment exists, warn and proceed. (Not executed in this eval.)

## Step 2 – Dependencies
"Depends on: None", so there is nothing to verify.

## Step 3 – Jira transition (not executed in eval)
- `jira.user_info()` returns the accountId
- `jira.edit_issue(TC-9205, assignee=<accountId>)`
- `jira.transition_issue(TC-9205, "In Progress")`

## Step 4 – Understand the code (via `mcp__serena_backend__*`)
- `get_symbols_overview("migration/src/lib.rs")`: confirm the `Migrator` struct, the `MigratorTrait` impl, `migrations()` returning `vec![Box::new(m0001_initial::Migration)]`, and the `mod m0001_initial;` declaration.
- `find_symbol("Migration", relative_path="migration/src/m0001_initial/mod.rs", include_body=true)`: confirm the `DeriveMigrationName` + `MigrationTrait` pattern, the `up`/`down` signatures, and how the `DeriveIden` enums (e.g. `Advisory`) are declared.
- **Verify Implementation Note:** `get_symbols_overview("entity/src/advisory.rs")` + `find_symbol("Model", include_body=true)`: confirm the advisory entity `Model` has no `status` field (only `severity`, etc.).
- `search_for_pattern("status", paths: entity/, modules/, common/)` restricted to advisory contexts (`advisory::Column::Status`, `.status`, `"status"` in advisory queries/ingestor `graph/advisory/mod.rs`, `AdvisorySummary`/`AdvisoryDetails`): confirm no service, entity or ingestor code reads or writes the column (Acceptance Criterion 4). If any reference is found, **stop and report** to the user, because the task premise would be invalid.
- Symbol dedup: `search_for_pattern("enum Advisory")` in `migration/`. If m0001 defines a private `Advisory` iden enum, follow the SeaORM convention that each migration is self-contained and declares its own local iden enum. Migrations must stay frozen in time, so I would not export m0001's enum and couple the two migrations. I would note this rationale in the PR description.
- CONVENTIONS.md at repo root (`./CONVENTIONS.md`): read it, extract the CI check commands (e.g. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) and any codegen commands (e.g. OpenAPI generation; not expected to change for a migration).
- Docs: README.md and docs/architecture.md. Check whether they enumerate migrations or the advisory schema. Expect no doc change.
- Sibling analysis results: see `conventions.md`.

## Step 5 – Branch operations (feature-branch workflow)
Target Branch is `TC-9005`, so branch off the feature branch, **not main**:
```
git checkout TC-9005
git pull
git checkout -b TC-9205
```
(If `TC-9005` does not exist on the remote, stop and tell the user that the create-branch bookend task for TC-9005 must be completed first. Do not fall back to main.)

## Step 6 – Implementation
1. **Create** `migration/src/m0002_drop_advisory_status/mod.rs` (see `file-2-migration-m0002-drop-advisory-status.md`)
   - `#[derive(DeriveMigrationName)] pub struct Migration;`
   - `up`: `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
   - `down`: `manager.alter_table(Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null()).to_owned()).await`
   - local `#[derive(DeriveIden)] enum Advisory { Table, Status }`
   - doc comments on the struct, the enum, and each method
   - `#[cfg(test)] mod tests` covering the test requirements (up/down against a test DB)
2. **Modify** `migration/src/lib.rs` (see `file-1-migration-lib-rs.md`)
   - add `mod m0002_drop_advisory_status;`
   - append `Box::new(m0002_drop_advisory_status::Migration)` after `m0001_initial` in `migrations()`

No other files are touched (scope containment).

## Step 7 – Tests
- Tests for up/down live inside the new migration module (`#[cfg(test)]`), which is within the "Files to Create" scope.
- "Existing advisory queries still work" is verified by running the existing integration suite `tests/api/advisory.rs` (and `tests/api/search.rs`, `tests/api/sbom.rs`, which join advisories) against the migrated test DB. No modification is needed. If a new test in `tests/api/advisory.rs` were desired, it is out of scope and would be flagged for user approval rather than added.
- Run: `cargo test -p migration` and `cargo test -p tests` (crate names resolved via `cargo metadata --no-deps --format-version 1`, not by guessing from the directory).

## Step 8 – Acceptance criteria
- [x] up drops `advisory.status` (file-2 `up`)
- [x] down re-adds it as a nullable string (file-2 `down`)
- [x] registered in `migration/src/lib.rs` (file-1)
- [x] no service/entity references (verified in Step 4 search; re-verified in Step 9)

## Step 9 – Self-verification
- Scope: `git diff --name-only` must list exactly `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`.
- Untracked check: `git status --short` should show only the new `m0002_drop_advisory_status/` dir, which is referenced by `mod` in lib.rs, so stage it.
- Sensitive-pattern grep on the staged diff: expect no matches.
- Dead parameters: N/A (nothing removed from function bodies).
- CI checks from CONVENTIONS.md: run each one; any non-zero exit is a hard stop.
- Rust module-level tests: `cargo test -p migration`; hard stop on failure.
- Data-flow trace: migrator startup runs `Migrator::migrations()`, which includes m0002, then `up` runs, then the column is gone. The entity/service layer is unaffected because there is no `status` field. Rollback: `down` re-adds the nullable column. The path is complete.
- Query-scope: N/A (DDL only, no batch record iteration).
- Contract & sibling parity:
  - Contract: `MigrationTrait` requires `up` (and `down` is optional, but the task requires it). Both are implemented with the `async fn(&self, &SchemaManager) -> Result<(), DbErr>` signature.
  - Sibling parity: matches m0001 (`DeriveMigrationName`, `#[async_trait::async_trait]`, `use sea_orm_migration::prelude::*`, `DeriveIden` enum).
  - Cross-module entity: `advisory` table is used by entity/ingestor/fundamental, and none of them use `status`.
  - Caller-site: `Migrator::migrations()` is the only consumer. Ordering is preserved (m0001 before m0002).

## Step 10 – Commit, push, PR
Commit:
```
git add migration/src/lib.rs migration/src/m0002_drop_advisory_status/mod.rs
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status which removes the unused
advisory.status column (superseded by the severity enum). The down
migration re-adds it as a nullable string to allow rollback.

Implements TC-9205"
git push -u origin TC-9205
```
Fork detection: `git remote get-url upstream 2>/dev/null`
- Fork detected: `gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body ...`
- No fork: `gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body ...`

**The PR targets `TC-9005` (the feature branch), not `main`.**

PR body:
```
## Summary
- Add migration `m0002_drop_advisory_status` dropping the deprecated `advisory.status` column
- `down` re-adds the column as nullable string for rollback
- Register migration in `migration/src/lib.rs`
- Migration declares its own local `Advisory` iden enum (migrations are self-contained; not shared with m0001)

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
Part of feature TC-9005 (feature branch)

Closes <owner>/<repo>#<number>   <- only if customfield_10747 is populated

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Step 11 – Jira update (not executed in eval)
- `jira.update_issue(TC-9205, fields={"customfield_10875": {"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"inlineCard","attrs":{"url":"<PR-URL>"}}]}]}})`
- `jira.add_comment(TC-9205, ...)` with the PR link (targeting TC-9005), a summary of changes, deviations (none; tests placed inline in the migration module), and the footnote from `shared/comment-footnote.md` with skill name `implement-task`.
- `jira.transition_issue(TC-9205, "In Review")`
