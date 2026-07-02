# Implementation Plan: TC-9205 — Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code. Removing it reduces confusion and prevents accidental usage.

## Target Branch

**TC-9005** (extracted from the task description's Target Branch section). This is the parent feature branch that incorporates this task — it is not `main`. The task description states:

> **Target Branch**
> TC-9005

All branch operations (checkout, PR base) must reference TC-9005 as the base, not `main`.

## Branch Operations

1. **Check out the target branch** (`TC-9005`):
   ```
   git checkout TC-9005
   git pull
   ```
   The target branch is `TC-9005` as specified in the task description's Target Branch section. We check out the target branch first so that the new task branch is based on the correct parent — the feature branch, not `main`.

2. **Create the task branch** from the target branch:
   ```
   git checkout -b TC-9205
   ```
   The task branch is named after the Jira issue ID (`TC-9205`), per the workflow convention (constraint 3.1). This is distinct from the target branch name (`TC-9005`).

3. **PR targeting**: The PR must target the feature branch `TC-9005` (not `main`), because the task's Target Branch is `TC-9005`:
   ```
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```
   This follows constraint 3.3: `gh pr create` MUST always specify `--base <target-branch>` matching the task's Target Branch value.

## Pre-Implementation Inspection

Before making any changes, the following files would be inspected (Step 4 -- code MUST NOT be modified without first inspecting it):

1. **`migration/src/m0001_initial/mod.rs`** -- the existing migration pattern, to understand:
   - How `MigrationTrait` is implemented (struct definition, `name()`, `up()`, `down()` methods)
   - Import patterns (which SeaORM crate/modules are imported)
   - Error handling patterns in migration methods
   - Whether identifier enums (`DeriveIden`) are defined locally within the migration or imported from the entity crate
   - Module naming conventions for migration directories

2. **`migration/src/lib.rs`** -- to understand:
   - How migrations are registered in the `migrations()` function
   - The module declaration pattern (`mod m0001_initial;`)
   - The `Migrator` struct and its trait implementation
   - The exact registration syntax (`Box::new(m0001_initial::Migration)`)

3. **`entity/src/advisory.rs`** -- to verify the advisory entity no longer references the `status` column (acceptance criterion 4). This is a mandatory verification step before proceeding with the migration.

4. **`CONVENTIONS.md`** at the repository root -- to check for project-specific coding conventions and CI check commands for Step 9 verification.

### Verification Before Implementation

- Confirm that `entity/src/advisory.rs` does NOT contain a `Status` field or column reference
- Search service code (`modules/fundamental/src/advisory/`) for any remaining references to `status` on the advisory entity
- Search query code and ingestion code for advisory status references

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the `status` column from the `advisory` table.

- Implements `MigrationTrait` with:
  - `name()` -- auto-derived via `DeriveMigrationName` from the module path
  - `up()` -- drops the `status` column using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
  - `down()` -- re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback

See `outputs/file-1-description.md` for full details.

## Files to Modify

### 2. `migration/src/lib.rs`

Register the new migration module:
- Add `mod m0002_drop_advisory_status;` declaration alongside the existing `mod m0001_initial;`
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry

See `outputs/file-2-description.md` for full details.

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any service or entity
code.

The down method re-adds the column as a nullable string for rollback
support.

Implements TC-9205
```

The commit would be executed with `--trailer='Assisted-by: Claude Code'` per constraint 2.3:

```
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any service or entity
code.

The down method re-adds the column as a nullable string for rollback
support.

Implements TC-9205"
```

## PR Creation

```
gh pr create \
  --base TC-9005 \
  --title "feat(migration): add migration to drop advisory status column" \
  --body "## Summary
- Add \`m0002_drop_advisory_status\` migration that drops the deprecated \`status\` column from the \`advisory\` table
- Register the new migration in \`migration/src/lib.rs\`
- Include rollback support via \`down()\` that re-adds the column as a nullable string

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

After the PR is created, the PR link would be posted as a comment on the Jira task TC-9205 and the Git Pull Request custom field (`customfield_10875`) would be updated with the PR URL in ADF format.

## Description Integrity Verification (Step 1.5)

Before proceeding with implementation, the description digest would be checked:

1. Fetch issue comments via `jira.get_issue_comments(TC-9205)`
2. Search for comments starting with `[sdlc-workflow] Description digest:`
3. If no digest comment is found, log a warning and proceed normally: "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."
4. If a digest comment is found, extract the tagged digest, compute the current description digest using `python3 scripts/sha256-digest.py`, compare format tags, and compare hex digests. Proceed silently on match; alert user on mismatch.

## Self-Verification Checks

1. **Scope containment**: Verify only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` are changed -- no other files touched (constraint 5.1)
2. **Sensitive pattern check**: Scan staged diff for secrets/credentials
3. **Data-flow trace**: Migration `up` drops the column, migration `down` re-adds it -- complete lifecycle covered
4. **Contract verification**: Verify `MigrationTrait` is fully implemented (`name`, `up`, `down` methods)
5. **Sibling parity**: Compare against `m0001_initial` for consistent patterns (error handling, import style, naming)
6. **Entity verification**: Confirm `entity/src/advisory.rs` has no `status` column reference
7. **Service code verification**: Confirm no service code references `advisory.status`

## Acceptance Criteria Verification

- [ ] Migration drops the `status` column from the `advisory` table -- verified by inspecting `up()` method
- [ ] Migration `down` method re-adds the column as nullable string for rollback -- verified by inspecting `down()` method
- [ ] Migration is registered in `migration/src/lib.rs` -- verified by inspecting lib.rs changes
- [ ] No service or entity code references the `status` column -- verified by grep search across entity and service code
