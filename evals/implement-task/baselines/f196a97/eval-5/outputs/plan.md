# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, NOT main)
**Linked Feature**: TC-9005 (parent feature)

## Branch Operations

### 1. Checkout the Target Branch (TC-9005)

The Target Branch field specifies `TC-9005`, which is a feature branch (not `main`). The task branch must be created from this feature branch:

```bash
git checkout TC-9005
git pull
```

### 2. Create the Task Branch (TC-9205)

The task branch is named after this task's Jira issue ID (`TC-9205`), which is distinct from the feature branch (`TC-9005`):

```bash
git checkout -b TC-9205
```

### 3. Push and Create PR Targeting TC-9005

After implementation, push and create a PR that targets the feature branch (`TC-9005`), not `main`:

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary
- Add migration m0002_drop_advisory_status that drops the deprecated status column from the advisory table
- Register the new migration in migration/src/lib.rs

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

The `--base TC-9005` flag is critical -- it ensures the PR targets the feature branch, not `main`.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the deprecated
status column, which was replaced by the severity enum field in a
previous migration. The down method re-adds the column as a nullable
string for rollback safety.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

Full command:
```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the deprecated
status column, which was replaced by the severity enum field in a
previous migration. The down method re-adds the column as a nullable
string for rollback safety.

Implements TC-9205"
```

## Files to Modify

1. **`migration/src/lib.rs`** -- Register the new migration module in the migration list

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** -- Migration that drops the `status` column from the `advisory` table

## Pre-Implementation Inspection (Step 4)

Before making any changes, the following files would be inspected using the `serena_backend` Serena instance (as specified in the Repository Registry):

1. **`migration/src/lib.rs`** -- Understand the current migration registration pattern (use `get_symbols_overview` to see structure, `find_symbol` for the `migrations()` function)
2. **`migration/src/m0001_initial/mod.rs`** -- Understand the sibling migration pattern (use `get_symbols_overview` to see `MigrationTrait` implementation, `up`/`down` methods)
3. **`entity/src/advisory.rs`** -- Verify that the `status` column is no longer referenced in the entity definition (use `get_symbols_overview` and `search_for_pattern` for `status` references)
4. **Advisory service and endpoint files** -- Grep for any remaining references to `status` on the advisory entity:
   - `modules/fundamental/src/advisory/service/advisory.rs`
   - `modules/fundamental/src/advisory/model/summary.rs`
   - `modules/fundamental/src/advisory/model/details.rs`
   - `modules/fundamental/src/advisory/endpoints/*.rs`
5. **`CONVENTIONS.md`** -- Check for project-specific conventions and CI check commands
6. **`tests/api/advisory.rs`** -- Understand test conventions for advisory integration tests

### Convention Conformance Analysis

Sibling analysis would examine `migration/src/m0001_initial/mod.rs` to extract:
- Module structure (mod.rs within a named directory)
- `MigrationTrait` implementation pattern
- `up`/`down` method signatures and return types
- SeaORM migration API usage patterns
- Error handling in migrations

### Documentation Files

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/architecture.md` and `docs/api.md` (referenced in CLAUDE.md)

## Verification Steps (Step 8 and 9)

1. Verify migration drops the `status` column (acceptance criterion 1)
2. Verify `down` method re-adds column as nullable string (acceptance criterion 2)
3. Verify migration is registered in `lib.rs` (acceptance criterion 3)
4. Grep entire codebase for `status` references on advisory entity (acceptance criterion 4)
5. Run `cargo test` to verify tests pass
6. Run `git diff --name-only` to verify scope containment (only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` should be modified/created)
7. Run sensitive-pattern check on staged diff
8. Check CONVENTIONS.md for CI commands and run them
9. Data-flow trace: migration up drops column, down re-adds it -- both paths complete

## Jira Updates (Step 11)

1. Set Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment with PR link and summary of changes
3. Transition TC-9205 to "In Review"
