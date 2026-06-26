# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, linked via "is incorporated by TC-9005")
**Dependencies**: None

## Target Branch Analysis

The task description contains a **Target Branch** section specifying `TC-9005`. This is a feature branch (not `main`), indicating that TC-9205 is part of a larger feature being developed on the TC-9005 feature branch. All branch operations must use TC-9005 as the base.

## Branch Operations

### 1. Check out the target branch and create task branch

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

**Key point**: We check out `TC-9005` (the Target Branch from the task description), NOT `main`. The task branch is named `TC-9205` (this task's Jira issue ID), not `TC-9005`.

### 2. After implementation, push and open PR

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

**Key point**: The PR targets `--base TC-9005`, NOT `--base main`, because the Target Branch is TC-9005.

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field in a previous migration and is no longer
referenced by any service or entity code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

With the trailer: `--trailer='Assisted-by: Claude Code'`

## Files to Create

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module implementing `MigrationTrait` with `up` (drop column) and `down` (re-add column) methods. See `outputs/file-1-description.md` for detailed changes.

## Files to Modify

### File 2: `migration/src/lib.rs`

Register the new migration module in the migration list. See `outputs/file-2-description.md` for detailed changes.

## Pre-Implementation Inspection (Step 4)

Before making any changes, the following files would be inspected using the Serena instance `serena_backend` (as specified in the Repository Registry):

1. **Existing migration pattern**: Inspect `migration/src/m0001_initial/mod.rs` using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` to understand the `MigrationTrait` implementation pattern (struct definition, `up`/`down` methods, imports, naming).

2. **Entity verification**: Inspect `entity/src/advisory.rs` using `mcp__serena_backend__get_symbols_overview` to confirm the `advisory` entity no longer references a `status` column (and does reference a `severity` field).

3. **Migration registration**: Inspect `migration/src/lib.rs` using `mcp__serena_backend__find_symbol` to see how `m0001_initial` is registered in the `migrations()` function and follow the same pattern.

4. **Reference check**: Use `mcp__serena_backend__search_for_pattern` to search for any remaining references to `Advisory::Status` or `status` column usage across the codebase to confirm no service or entity code still references it.

5. **CONVENTIONS.md**: Check for `CONVENTIONS.md` at the repository root and read it if present. Extract any CI check commands for use in Step 9.

6. **Documentation files**: Identify README files and docs in the migration directory or parent directories that may need updating.

## PR Description

```
## Summary

Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

- New migration with `up` (drop column) and `down` (re-add as nullable string) methods
- Migration registered in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

## Jira Updates (Step 11)

1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format
2. Add comment with PR link, summary of changes, and any deviations
3. Transition TC-9205 to "In Review"
