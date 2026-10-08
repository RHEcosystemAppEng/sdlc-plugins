# Implementation Plan for TC-9205

## Task Summary

**Jira ID**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005
**Linked Issues**: is incorporated by TC-9005
**Status**: To Do

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142
- Code Intelligence: Serena instance `serena_backend` with rust-analyzer

Configuration is valid. Proceeding.

## Step 1 -- Parse Task Description

Parsed sections:
- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (feature branch, not main)
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration implementation
- **Implementation Notes**: Follow m0001_initial pattern, use SeaORM TableAlterStatement, implement MigrationTrait with up/down
- **Acceptance Criteria**: 4 items (drop column, rollback re-adds, registered in lib.rs, no remaining status references)
- **Test Requirements**: 3 items (migration runs, rollback works, queries still work)
- **Dependencies**: None
- **Bookend Type**: Not present (standard implementation task)
- **Target PR**: Not present (new branch and PR)
- **GitHub Issue custom field**: customfield_10747 (would check for linked GitHub issue)

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign task
3. `jira.transition_issue(TC-9205, "In Progress")` to update status

## Step 4 -- Understand the Code

### Serena inspection

Using `mcp__serena_backend__get_symbols_overview` on:
- `migration/src/lib.rs` -- understand current migration registration pattern
- `migration/src/m0001_initial/mod.rs` -- understand existing migration implementation (sibling)
- `entity/src/advisory.rs` -- verify `status` column is no longer referenced

Using `mcp__serena_backend__find_symbol` with `include_body=true` on:
- The `migrations()` function in `migration/src/lib.rs`
- The `MigrationTrait` implementation in `m0001_initial/mod.rs`

Using `mcp__serena_backend__search_for_pattern` to:
- Search for any remaining references to `Advisory::Status` or `status` column usage across the codebase
- Check for CONVENTIONS.md at repository root

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root. The repo structure shows it exists at `trustify-backend/CONVENTIONS.md`. Would read it and extract any CI check commands and code generation commands.

### Documentation file identification

Relevant docs:
- `README.md` at repo root
- `CONVENTIONS.md` at repo root
- No API docs affected (this is a migration, not an endpoint change)

### Convention conformance analysis

Sibling analysis target: `migration/src/m0001_initial/mod.rs` -- the only existing migration and the direct pattern to follow. See `outputs/conventions.md` for full convention analysis.

## Step 5 -- Create Branch

**Branch operations (critical -- feature branch workflow):**

The Target Branch is `TC-9005` (a feature branch), NOT `main`. This task is part of a feature that uses a feature branch workflow.

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This checks out the parent feature branch TC-9005 first, then creates the task branch TC-9205 from it.

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module following the m0001_initial pattern. See `outputs/file-1-description.md` for detailed implementation.

### File 2: Modify `migration/src/lib.rs`

Register the new migration module in the migrations list. See `outputs/file-2-description.md` for detailed changes.

## Step 7 -- Write Tests

The test requirements specify:
1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

These would be integration tests that require a PostgreSQL test database. Would add tests in the migration crate or in `tests/api/advisory.rs` depending on existing test infrastructure. See `outputs/file-3-description.md` for details.

## Step 8 -- Verify Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table -- implemented in up() method
- [x] Migration `down` method re-adds the column as nullable string for rollback -- implemented in down() method
- [x] Migration is registered in `migration/src/lib.rs` -- added to vec![] in migrations()
- [x] No service or entity code references the `status` column -- verified via codebase search (entity/src/advisory.rs no longer has status field)

## Step 9 -- Self-Verification

### Scope containment
Would run `git diff --name-only` and verify only these files were modified/created:
- `migration/src/lib.rs` (modified -- in scope)
- `migration/src/m0002_drop_advisory_status/mod.rs` (created -- in scope)

### Sensitive-pattern check
Would run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- no secrets expected in migration code.

### CI checks from CONVENTIONS.md
Would run any CI check commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`, `cargo check`).

### Module-level test requirement (Rust)
Would resolve crate name via `cargo metadata` for the migration crate and run:
```bash
cargo test -p <migration-crate-name>
```

### Data-flow trace
- Input: Migration runner invokes `up()` method
- Processing: `TableAlterStatement` drops the `status` column from `advisory` table
- Output: Column removed from database schema
- Rollback: `down()` re-adds column as nullable string
Complete data flow confirmed.

### Query-scope verification
The migration targets a specific column (`status`) on a specific table (`advisory`). The ALTER TABLE statement is correctly scoped -- no broad/unfiltered operations.

### Contract & sibling parity
- Contract: `MigrationTrait` requires `name()`, `up()`, and `down()` methods -- all implemented
- Sibling parity: follows same pattern as `m0001_initial` for struct definition, trait implementation, and error handling
- Cross-module entity: `advisory` table -- verified no other active code references the `status` column
- Caller-site: migration runner calls migrations in order from `migrations()` vec -- new entry appended correctly

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code. The down method re-adds the column as a nullable
string to support rollback.

Implements TC-9205
```

With `--trailer="Assisted-by: Claude Code"`.

### Fork detection

Would run `git remote get-url upstream 2>/dev/null` to check for fork setup.

### Push and PR creation

```bash
git push -u origin TC-9205
```

**PR targets TC-9005 (the feature branch), NOT main:**

```bash
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "$(cat <<'EOF'
## Summary

- Add `m0002_drop_advisory_status` migration that drops the deprecated `status` column from the `advisory` table
- The `down` method re-adds the column as a nullable string for rollback support
- Migration registered in `migration/src/lib.rs`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Migration runs successfully against a test database
- [ ] Rollback (down) re-adds the column as nullable string
- [ ] Existing advisory queries still work after the column is dropped
EOF
)"
```

The `--base TC-9005` flag ensures the PR targets the feature branch, not main.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (customfield_10875) with the PR URL using ADF format:
   ```
   jira.update_issue(TC-9205, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9205 with PR link, summary of changes, and confirmation that all acceptance criteria are met.

3. **Transition** to In Review:
   ```
   jira.transition_issue(TC-9205, "In Review")
   ```
