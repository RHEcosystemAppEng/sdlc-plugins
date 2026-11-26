# Implementation Plan: TC-9205 — Add migration to drop status table column

Skill: `sdlc-workflow:implement-task` (followed from SKILL.md; dry run, no repo, git, Jira or Serena calls made)

## Step 0: Validate Project Configuration

Checked the project CLAUDE.md (`claude-md-mock.md`):
- `## Repository Registry`: present. Row: `trustify-backend | Rust backend service | serena_backend | ./`
- `## Jira Configuration`: present. Project key TC, Cloud ID 2b9e35e3-..., Feature issue type ID 10142, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- `## Code Intelligence`: present, with the tool naming convention `mcp__<serena-instance>__<tool>`. Instance `serena_backend` (rust-analyzer). Known limitation: indexing takes 30-60s on first use.

Result: all three sections are present. Continue.

## Step 0.5: Jira access
Would use the Atlassian MCP first. If MCP failed, would ask the user about the REST fallback. (Skipped in this dry run.)

## Step 1: Fetch and parse the task (`jira.get_issue("TC-9205")`)

| Section | Value |
|---|---|
| Repository | trustify-backend |
| **Target Branch** | **`TC-9005`** (a feature branch, not `main`) |
| Description | Drop the deprecated `status` column from the `advisory` table |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| API Changes | none |
| Target PR | not present, so this is the default flow (new branch and new PR) |
| Bookend Type | not present, so this is a normal implementation task |
| Dependencies | None |
| Linked | "is incorporated by TC-9005" (parent feature, which matches the feature branch name) |

- `webUrl` captured for the PR link: `https://redhat.atlassian.net/browse/TC-9205`.
- GitHub Issue field `customfield_10747` is configured. Would read it from the issue. If it is empty, skip silently and add no `Closes` line.
- All required sections are present, so there is no need to stop for clarification.

## Step 1.5: Description integrity
Would call `jira.get_issue_comments("TC-9205")` and look for the most recent `[sdlc-workflow] Description digest:` comment. Would then compare it with `python3 scripts/sha256-digest.py /tmp/desc-TC-9205.txt`.
- Match: proceed silently.
- No digest comment: warn and proceed.
- Mismatch: stop and ask the user.

## Step 2: Dependencies
"Depends on: None", so there is nothing to check.

## Step 3: Assign and transition
`jira.user_info()`, then `jira.edit_issue(TC-9205, assignee=<me>)`, then `jira.transition_issue(TC-9205, "In Progress")`.

## Step 4: Understand the code (Serena instance `serena_backend`)
- `get_symbols_overview("migration/src/lib.rs")` to find the `Migrator` struct, its `MigratorTrait` impl, `migrations()`, and the `mod m0001_initial;` declaration.
- `find_symbol("Migrator/migrations", include_body=true)` to see the exact `vec![Box::new(m0001_initial::Migration)]` shape.
- `get_symbols_overview` and `find_symbol(include_body=true)` on `migration/src/m0001_initial/mod.rs` to read the `Migration` struct, `MigrationTrait` impl (`up`/`down`), and how the `Advisory` Iden enum is declared.
- Check the entity, as the notes ask: `get_symbols_overview("entity/src/advisory.rs")` and `search_for_pattern("status", relative_path="entity/src/advisory.rs")`. Confirm that `Model` and `Column` have no `status` field.
- Check acceptance criterion 4 across the repo: `search_for_pattern("advisory.*status|Column::Status|\\.status\\b", paths modules/, entity/, common/)`. Confirm that no service, ingestor, or search code reads or writes `advisory.status`. If any reference exists, stop and report it, because the task assumes there are none.
- Symbol dedup: search `migration/src` for `enum Advisory`. If `m0001_initial` declares `Advisory` privately, follow the migration convention and declare a local `Advisory` Iden enum in the new module (see conventions.md). Do not make the m0001 one `pub`.
- Read `CONVENTIONS.md` at the repo root (`./CONVENTIONS.md` per the Registry path). Extract the CI check commands (likely `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`) and any codegen commands.
- Docs: `README.md` and `CONVENTIONS.md`. The change has no public API or config impact, so no doc updates are expected.
- Sibling analysis: written to `conventions.md`.

## Step 5: Create the branch (default flow, feature-branch target)

```
git checkout TC-9005
git pull
git checkout -b TC-9205
```

The task branch `TC-9205` is cut from the feature branch `TC-9005`, not from `main`.

## Step 6: Implement changes

| # | File | Action | Detail |
|---|---|---|---|
| 1 | `migration/src/m0002_drop_advisory_status/mod.rs` | Create | `Migration` struct (`DeriveMigrationName`), `MigrationTrait` impl. `up` drops `Advisory::Status` through `Table::alter()`. `down` re-adds it as `ColumnDef::new(Advisory::Status).string().null()`. Local `Advisory` Iden enum. Doc comments. See `file-1-m0002-drop-advisory-status.md` |
| 2 | `migration/src/lib.rs` | Modify | Add `mod m0002_drop_advisory_status;` and append `Box::new(m0002_drop_advisory_status::Migration)` after m0001 in `migrations()`. See `file-2-migration-lib-rs.md` |

No other files are touched. `entity/src/advisory.rs` and the service code are only read to check them.

## Step 7: Tests
The Test Requirements ask for: migration up against a test DB, rollback re-adds the column, and existing advisory queries still work.

Scope tension: no test file appears in Files to Modify or Files to Create. Plan:
- Put the migration up/down tests in a `#[cfg(test)] mod tests` inside the new file `migration/src/m0002_drop_advisory_status/mod.rs`, which is in scope. Each test gets a `///` doc comment and Given/When/Then comments.
- The "existing advisory queries still work" check would be covered by running the existing `tests/api/advisory.rs` integration suite unchanged (`cargo test -p tests`, or whatever the crate name resolves to). No edits are made there.
- If the reviewer or user prefers dedicated tests in `tests/` or `migration/tests/`, that is an out-of-scope file. It would be flagged in Step 9 for explicit approval rather than added silently.

Run `cargo test -p migration` (crate name resolved with `cargo metadata --no-deps --format-version 1`). Also run the advisory integration tests.

## Step 8: Acceptance criteria
- [x] `up` drops `status` from `advisory`, via `alter_table(... drop_column(Advisory::Status))`
- [x] `down` re-adds `status` as a nullable string
- [x] Registered in `migration/src/lib.rs` `migrations()` vec, after m0001
- [x] No service or entity references to `status`, confirmed by the Step 4 search. If any are found, stop.

## Step 9: Self-verification
- Scope: `git diff --name-only` should show only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`.
- Untracked check: the new dir `m0002_drop_advisory_status/` is referenced by `mod` in lib.rs. Stage it intentionally.
- Dead parameters: none, since no code is removed from functions.
- Sensitive patterns: none expected.
- Docs currency: no public API or config change.
- CI: run every CONVENTIONS.md CI command. Any non-zero exit is a hard stop.
- Rust module tests: `cargo test -p migration`, plus the crate that holds `tests/api/advisory.rs`.
- Data-flow: schema-only change. The flow is `Migrator::up`, then `m0002::up`, then `ALTER TABLE advisory DROP COLUMN status`, and the reverse on down. Complete.
- Query scope: DDL only, with no record iteration. N/A.
- Contract and sibling parity:
  - Contract: implements both `up` and `down` of `MigrationTrait` with matching signatures `async fn(&self, &SchemaManager) -> Result<(), DbErr>`.
  - Sibling parity: same derive, imports, and Iden style as m0001.
  - Cross-module entity: the advisory entity and services do not use `status`.
  - Caller-site: registered exactly like m0001 in `migrations()`.

## Step 10: Commit and push

Commit message:

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status which removes the unused
advisory.status column (superseded by the severity enum field). The
down migration re-adds the column as a nullable string to allow
rollback. Register the migration in the Migrator after m0001_initial.

Implements TC-9205"
```

Push and open the PR. First run fork detection with `git remote get-url upstream`.

```
git push -u origin TC-9205
# no fork:
gh pr create --base TC-9005 --head TC-9205 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
# fork detected:
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 ...
```

The PR targets **`TC-9005`** (the feature branch from Target Branch), not `main`.

PR body:
```
## Summary
- Add migration `m0002_drop_advisory_status` dropping the deprecated `advisory.status` column
- `down` re-adds the column as nullable string for rollback
- Register migration in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
<Closes owner/repo#N, only if customfield_10747 is set>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Step 11: Update Jira
- `jira.update_issue(TC-9205, {"customfield_10875": {ADF doc with inlineCard url=<PR-URL>}})`
- `jira.add_comment(TC-9205, ...)` with the PR link, a summary of changes, and deviations (test placement, see Step 7). It ends with a rule and the footnote "This comment was AI-generated by [sdlc-workflow/implement-task](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0."
- `jira.transition_issue(TC-9205, "In Review")`
