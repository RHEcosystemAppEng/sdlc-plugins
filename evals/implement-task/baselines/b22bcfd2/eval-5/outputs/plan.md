# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue:** TC-9205
**Summary:** Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository:** trustify-backend
**Target Branch:** TC-9005 (feature branch, extracted from the Target Branch section of the task description)
**Linked Issues:** is incorporated by TC-9005

## Branch Operations

1. **Check out the target branch (TC-9005):**
   ```
   git checkout TC-9005
   git pull
   ```
   The Target Branch section specifies TC-9005 — this is the feature branch that this task belongs to. We do NOT check out `main`.

2. **Create the task branch from TC-9005:**
   ```
   git checkout -b TC-9205
   ```
   The branch is named after the task issue ID (TC-9205), not the feature branch (TC-9005).

## Pre-Implementation: Code Inspection (Step 4)

Before making any changes, inspect existing code using the Serena instance `serena_backend` (from the Repository Registry):

1. **Inspect `migration/src/lib.rs`** — use `mcp__serena_backend__get_symbols_overview` to understand the current migration registration pattern and how `m0001_initial` is registered in the `migrations()` function.

2. **Inspect `migration/src/m0001_initial/mod.rs`** — use `mcp__serena_backend__find_symbol` with `include_body=true` to read the `MigrationTrait` implementation and understand the `up`/`down` method pattern, imports, and structure.

3. **Verify `entity/src/advisory.rs`** — use `mcp__serena_backend__get_symbols_overview` to confirm that the `Advisory` entity no longer references the `status` column. This is an explicit acceptance criterion.

4. **Search for remaining `status` references** — use `mcp__serena_backend__search_for_pattern` (or Grep as fallback) to search the entire codebase for references to `Advisory::Status` or the `status` column on the advisory table, confirming no service or entity code still uses it.

5. **Check for CONVENTIONS.md** — read `CONVENTIONS.md` at the repository root if it exists, and extract any CI check commands and coding conventions.

6. **Convention conformance analysis** — examine `migration/src/m0001_initial/mod.rs` as a sibling file to understand established patterns for migration modules.

7. **Test convention analysis** — examine `tests/api/advisory.rs` as a sibling test file to understand test patterns for advisory-related tests.

8. **Documentation file identification** — check for README files in `migration/` and the root `README.md` for documentation that might reference the advisory schema.

## Files to Create

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module implementing `MigrationTrait` with:
- `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down` method: re-adds the `status` column as a nullable string for rollback

See `outputs/file-1-description.md` for detailed changes.

## Files to Modify

### File 2: `migration/src/lib.rs`

Register the new migration module `m0002_drop_advisory_status` in the migration list.

See `outputs/file-2-description.md` for detailed changes.

## Verification Steps (Step 8 & 9)

### Acceptance Criteria Verification
- [ ] Migration drops the `status` column from the `advisory` table — verified by reading the `up` method implementation
- [ ] Migration `down` method re-adds the column as nullable string for rollback — verified by reading the `down` method
- [ ] Migration is registered in `migration/src/lib.rs` — verified by reading the updated `migrations()` function
- [ ] No service or entity code references the `status` column — verified by grep/search in Step 4

### Self-Verification
1. **Scope containment:** Run `git diff --name-only` and confirm only `migration/src/lib.rs` is modified and `migration/src/m0002_drop_advisory_status/mod.rs` is created.
2. **Untracked file check:** Run `git status --short` and confirm the new migration file is staged.
3. **Sensitive-pattern check:** Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to confirm no secrets.
4. **Data-flow trace:** Migration up drops column, down re-adds it — complete lifecycle.
5. **Contract & sibling parity:** Verify `MigrationTrait` is fully implemented (both `up` and `down` methods) matching the pattern in `m0001_initial`.
6. **CI checks:** Run any CI commands from CONVENTIONS.md, or fall back to `cargo test` and `cargo build`.

### Test Execution
Run tests as described in Test Requirements:
```
cargo test
```
Verify that migration runs successfully, rollback works, and existing advisory queries still function.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the `status` column
from the `advisory` table. The column was replaced by the `severity` enum
field in a previous migration and is no longer referenced by any service
or entity code.

The down method re-adds the column as a nullable string to support rollback.

Implements TC-9205
```

With trailer:
```
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the status column
from the advisory table. The column was replaced by the severity enum
field in a previous migration and is no longer referenced by any service
or entity code.

The down method re-adds the column as a nullable string to support rollback.

Implements TC-9205"
```

## Push and PR Creation

```
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

- Add migration \`m0002_drop_advisory_status\` that drops the deprecated \`status\` column from the \`advisory\` table
- The column was replaced by the \`severity\` enum field and is no longer referenced by any code
- Includes rollback support via \`down\` method that re-adds the column as nullable string

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Migration runs successfully against a test database
- [ ] Rollback (down) re-adds the column
- [ ] Existing advisory queries still work after column is dropped
- [ ] No service or entity code references the \`status\` column"
```

The PR targets `TC-9005` (the feature branch) via `--base TC-9005`, NOT `main`.

## Jira Updates (Step 11)

1. Update the Git Pull Request custom field (`customfield_10875`) on TC-9205 with the PR URL in ADF format.
2. Add a Jira comment with the PR link and summary of changes.
3. Transition TC-9205 to **In Review**.
