# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer referenced by any entity or service code.

## Branch Operations

### Target Branch

The task specifies **Target Branch: TC-9005**. This is a feature branch (not `main`), meaning the work is part of a larger feature (TC-9005) being developed on a dedicated branch.

### Branch Creation

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates the task branch `TC-9205` based off the feature branch `TC-9005`.

### PR Targeting

The PR must target the feature branch `TC-9005`, not `main`:

```bash
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
```

The `--base TC-9005` flag is critical because the Target Branch is a feature branch, not `main`. The PR description will include:

```
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

## Files to Create

1. `migration/src/m0002_drop_advisory_status/mod.rs` -- new migration module

## Files to Modify

1. `migration/src/lib.rs` -- register the new migration module

## Pre-Implementation Verification

Before implementing:
- Verify `entity/src/advisory.rs` does not reference the `status` column (confirmed per task description)
- Review `migration/src/m0001_initial/mod.rs` to understand the migration pattern (sibling analysis)
- Check `migration/src/lib.rs` to understand the migration registration pattern
- Look for CONVENTIONS.md at the repository root and extract any CI verification commands

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Remove the `status` column from the `advisory` table via a new SeaORM
migration. The column was replaced by the `severity` enum field and is
no longer read or written by any service code.

Implements TC-9205
```

With the trailer: `--trailer="Assisted-by: Claude Code"`

## Self-Verification Checklist

- Scope containment: only `migration/src/lib.rs` modified and `migration/src/m0002_drop_advisory_status/mod.rs` created
- Entity verification: confirm `entity/src/advisory.rs` has no `status` column reference
- Migration registration: confirm the new migration appears in the `migrations()` vec in `lib.rs`
- Rollback support: confirm `down` method re-adds the column as nullable string
- Run `cargo test` to verify migration compiles and tests pass
- Run any CI checks from CONVENTIONS.md if present

## Jira Updates

1. Transition TC-9205 to "In Progress" at start
2. Assign to current user
3. After PR creation, update Git Pull Request custom field (`customfield_10875`) with PR URL (in ADF format)
4. Add comment with PR link and summary of changes
5. Transition TC-9205 to "In Review"
