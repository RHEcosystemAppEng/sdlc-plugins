# Implementation Plan for TC-9205: Add migration to drop status table column

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Validation passes. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed fields from TC-9205:

| Field | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | TC-9005 |
| Description | Add a database migration that drops the deprecated `status` column from the `advisory` table |
| Files to Modify | `migration/src/lib.rs` |
| Files to Create | `migration/src/m0002_drop_advisory_status/mod.rs` |
| Implementation Notes | Follow pattern in `m0001_initial/mod.rs`; use `MigrationTrait` with `up`/`down`; use `TableAlterStatement` |
| Acceptance Criteria | 4 items (see task) |
| Test Requirements | 3 items (see task) |
| Target PR | (none) |
| Bookend Type | (none) |
| Dependencies | None |
| GitHub Issue | (none -- custom field not populated) |

- **Target Branch**: `TC-9005` (a feature branch, NOT main)
- **webUrl**: `https://redhat.atlassian.net/browse/TC-9205` (captured for PR description)

No required section is missing. No Target PR. No Bookend Type. Proceed.

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9205)` and look for a comment starting with `[sdlc-workflow] Description digest:`. If found, compute digest of the description and compare. If not found, log warning and proceed.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user: `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9205, assignee=<account-id>)`
3. Transition: `jira.transition_issue(TC-9205) -> In Progress`

## Step 4 -- Understand the Code

### Files to inspect

1. **`migration/src/m0001_initial/mod.rs`** -- sibling migration, primary pattern reference. Use `mcp__serena_backend__get_symbols_overview` to see its structure (structs, impl blocks, functions). Then `mcp__serena_backend__find_symbol` with `include_body=true` on the `MigrationTrait` impl to read the `up` and `down` methods.

2. **`migration/src/lib.rs`** -- registration file. Use `mcp__serena_backend__get_symbols_overview` to see how migrations are listed (the `migrations()` function returning a `Vec<Box<dyn MigrationTrait>>`).

3. **`entity/src/advisory.rs`** -- verify the `status` column is no longer referenced. Use `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__search_for_pattern` for `Status` or `status` to confirm no remaining references.

4. **Advisory service/endpoint code** -- use `mcp__serena_backend__search_for_pattern` to search for `status` references in `modules/fundamental/src/advisory/` and `modules/ingestor/src/graph/advisory/` to confirm no service code references the column.

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo structure shows a `CONVENTIONS.md` file exists. Read it for naming rules, directory structure, code patterns, test conventions, and CI check commands. Extract any verification commands for use in Step 9.

### Convention conformance analysis

Analyze `migration/src/m0001_initial/mod.rs` as the primary sibling. Conventions discovered are documented in `outputs/conventions.md`.

### Documentation file identification

- `README.md` at repo root
- `CONVENTIONS.md` at repo root
- No API docs directly related to migrations

## Step 5 -- Create Branch

**Branch operations (default flow -- no Target PR, no Bookend Type):**

```
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This checks out the feature branch TC-9005 first, pulls latest, then creates the task branch TC-9205 from it. The PR will target TC-9005 (not main).

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module implementing `MigrationTrait`. See `outputs/file-1-description.md` for full details.

### File 2: Modify `migration/src/lib.rs`

Register the new migration module. See `outputs/file-2-description.md` for full details.

## Step 7 -- Write Tests

Implement tests per the Test Requirements. See `outputs/file-3-description.md` for test details.

Note: The test requirements call for integration tests against a test database. These would be added alongside the migration or in the existing test infrastructure, following the sibling test patterns.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| Migration drops the `status` column from the `advisory` table | The `up()` method uses `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)` |
| Migration `down` method re-adds the column as nullable string for rollback | The `down()` method uses `Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null())` |
| Migration is registered in `migration/src/lib.rs` | Module added to `mod` declarations and instance added to `migrations()` vec |
| No service or entity code references the `status` column | Verified via search in Step 4 -- `entity/src/advisory.rs` no longer has `Status` variant; service/endpoint code does not reference it |

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` should show only:
  - `migration/src/lib.rs` (modified)
  - `migration/src/m0002_drop_advisory_status/mod.rs` (created)
- Both are within scope per Files to Modify and Files to Create.

### Sensitive-pattern check
- Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches for a migration file.

### CI checks from CONVENTIONS.md
- Run any CI check commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`, `cargo check`).
- Hard stop on any failure.

### Module-level test requirement (Rust)
- Run `cargo metadata --no-deps --format-version 1` to resolve the crate name for the migration package.
- Run `cargo test -p <migration-crate-name>` to verify all migration tests pass.

### Data-flow trace
- Input: Migration runner invokes `up()` method
- Processing: SeaORM `TableAlterStatement` drops the `status` column from `advisory` table
- Output: Database schema updated, column removed
- Rollback path: `down()` re-adds the column as nullable string
- Flow is complete -- no disconnected stages.

### Query-scope verification
- The migration targets all rows in the `advisory` table (column drop is DDL, not DML). This is correct -- dropping a column affects the entire table schema, not a subset of rows. No scope mismatch.

### Contract & sibling parity
- **Contract**: `MigrationTrait` requires `up()` and `down()` methods returning `Result<(), DbErr>`. Both implemented.
- **Sibling parity**: Matches `m0001_initial/mod.rs` pattern for struct definition, `MigrationName` impl, and `MigrationTrait` impl.
- **Cross-module entity**: The `advisory` table is used by `entity/src/advisory.rs` and queried by advisory service code. The entity no longer references `status`, and service code does not query it.
- **Caller-site**: The migration is invoked by the migration runner via the `migrations()` vec in `lib.rs`. Registration follows the same pattern as `m0001_initial`.

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field in a previous migration and is no longer
referenced by any entity or service code. The down method re-adds
the column as a nullable string to support rollback.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

### Push and PR

```
git push -u origin TC-9205
```

### Fork detection

Run `git remote get-url upstream 2>/dev/null` to check for fork.

### PR creation (assuming no fork)

```
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "$(cat <<'EOF'
## Summary

- Add `m0002_drop_advisory_status` migration that drops the deprecated `status` column from the `advisory` table
- The `down` method re-adds the column as a nullable string for rollback support
- Migration registered in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Verify migration runs successfully against a test database
- [ ] Verify rollback (down) re-adds the column
- [ ] Verify existing advisory queries still work after column is dropped
EOF
)"
```

Key: the PR targets `TC-9005` (the feature branch), NOT `main`.

If a fork is detected, the command would be:
```
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9205 --base TC-9005 ...
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format:
   ```
   jira.update_issue(TC-9205, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9205:
   - PR link
   - Summary: Created migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table. The `down` method supports rollback by re-adding the column as a nullable string. Migration registered in `lib.rs`.
   - No deviations from the plan.
   - Comment ends with the footnote from `shared/comment-footnote.md` using skill name `implement-task`.

3. **Transition**: `jira.transition_issue(TC-9205) -> In Review`
