# Implementation Plan — TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information. This is a data migration that targets only SPDX documents, reusing the existing `suppliers()` function from the ingestor module.

## Step 0 — Validate Project Configuration

CLAUDE.md contains the required sections: Repository Registry (trustify-backend with serena_backend), Jira Configuration (project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field), and Code Intelligence (tool naming convention, serena_backend instance). Validation passes.

## Step 1 — Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Jira issue ID**: TC-9209
- **webUrl**: https://redhat.atlassian.net/browse/TC-9209

### Extracted sections

- **Files to Modify**: `modules/ingestor/src/graph/sbom/mod.rs`
- **Files to Create**: `migration/src/m0042_backfill_suppliers/mod.rs`
- **API Changes**: none
- **Dependencies**: none

## Step 1.5 — Verify Description Integrity

No digest comment found — skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 4 — Understand the Code

### Code inspection

Before modifying any files, inspect the following:

1. **`modules/ingestor/src/graph/sbom/mod.rs`** — Read using `mcp__serena_backend__get_symbols_overview` to find the `suppliers()` function, confirm it is private (`fn suppliers(...)`) and understand its signature, parameters, and return type. Use `mcp__serena_backend__find_symbol(name_path_pattern="suppliers", include_body=true)` to read the full function body.

2. **`entity/src/sbom.rs`** — Inspect the SBOM entity to confirm the `labels` column exists and is of type `jsonb`. Verify that the labels structure supports filtering by `{"type": "spdx"}` at the database query level.

3. **`migration/src/m0001_initial/mod.rs`** — Read the existing migration pattern using `mcp__serena_backend__get_symbols_overview` to understand the `MigrationTrait` implementation, `up()` method structure, and how migrations interact with the database.

4. **`migration/src/lib.rs`** — Inspect to understand how migrations are registered (the new m0042 migration must be added to the migration list).

5. **`migration/Cargo.toml`** — Verify that the migration crate already depends on `trustify-module-ingestor`, confirming we can import the `suppliers()` function after making it public.

### Convention conformance analysis

Examine sibling migration files (m0001_initial) for patterns:
- Migration structure: `MigrationTrait` with `up()` and `down()` methods
- Error handling: `Result<(), DbErr>` return types
- Database operations: SeaORM query patterns

### CONVENTIONS.md lookup

Check `CONVENTIONS.md` at the repository root for CI check commands and code generation commands to run during Step 9 verification.

## Step 5 — Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9209
```

## Step 6 — Implement Changes

### File to Modify: `modules/ingestor/src/graph/sbom/mod.rs`

Change the visibility of the `suppliers()` function from private to public:

```rust
// Before:
fn suppliers(...) -> ... {

// After:
pub fn suppliers(...) -> ... {
```

This is the only change to this file — the function body remains unchanged.

### File to Create: `migration/src/m0042_backfill_suppliers/mod.rs`

Create the migration module following the `m0001_initial` pattern:

1. Implement `MigrationTrait` with an `up()` method.
2. **Query only SPDX SBOMs** using a filtered query on the `labels` jsonb column:
   ```sql
   SELECT id FROM sbom WHERE labels->>'type' = 'spdx'
   ```
   This filters at the database level, loading only SPDX documents. CycloneDX documents (hundreds of thousands in production) are never fetched.
3. For each SPDX SBOM ID:
   a. Fetch the source document using `SourceDocument::find_by_sbom_id(id)`
   b. Re-parse the SPDX document
   c. Extract supplier information using the now-public `suppliers()` function from `trustify_module_ingestor::graph::sbom`
   d. Update the corresponding `sbom_package` records with the extracted supplier values
4. Process in batches to avoid memory pressure on large datasets.

### File to Modify: `migration/src/lib.rs`

Register the new migration module `m0042_backfill_suppliers` in the migration list.

**Note on scope**: `migration/src/lib.rs` is not listed in Files to Modify in the task description. This is an out-of-scope file that requires modification for the migration to be registered. This would be flagged during Step 9's scope containment check for user approval.

## Step 7 — Write Tests

Per the Test Requirements:

1. **Test: migration populates supplier information for an SPDX SBOM**
   - Set up a test SPDX SBOM in the test database with known supplier data
   - Run the migration
   - Assert that `sbom_package` records have populated supplier fields with specific expected values

2. **Test: CycloneDX SBOMs are not affected by the migration**
   - Set up both an SPDX SBOM and a CycloneDX SBOM in the test database
   - Run the migration
   - Assert that only the SPDX SBOM's packages have updated supplier fields
   - Assert that the CycloneDX SBOM's packages remain unchanged

## Step 8 — Verify Acceptance Criteria

- [x] The migration re-processes all SPDX SBOM documents and populates supplier fields — done via filtered query and `suppliers()` reuse
- [x] CycloneDX documents are not loaded or processed by the migration — ensured by `WHERE labels->>'type' = 'spdx'` filter
- [x] The `suppliers()` function in the ingestor is made public for reuse — changed to `pub fn`
- [x] The migration follows the existing migration pattern from `m0001_initial` — implements `MigrationTrait`

## Step 9 — Self-Verification

### Query-scope verification

See `query-scope.md` for detailed analysis. The task targets "all SPDX SBOMs" — a subset of all SBOMs. The `labels` jsonb column supports database-level filtering. The plan uses `WHERE labels->>'type' = 'spdx'` rather than loading all documents, avoiding unnecessary I/O for the hundreds of thousands of CycloneDX documents in production.

### Scope containment

- `modules/ingestor/src/graph/sbom/mod.rs` — in scope (Files to Modify)
- `migration/src/m0042_backfill_suppliers/mod.rs` — in scope (Files to Create)
- `migration/src/lib.rs` — **out of scope** — flag for user approval (needed to register the new migration)

### Dead parameter detection

No parameters removed — not applicable.

### Symbol deduplication

The `suppliers()` function already exists in `modules/ingestor/src/graph/sbom/mod.rs`. The plan reuses it by making it public rather than duplicating the extraction logic.

### Module-level test requirement (Rust)

Run `cargo metadata --no-deps --format-version 1` from the workspace root to resolve the crate names for affected modules. Run:

```bash
cargo test -p trustify-module-ingestor
cargo test -p trustify-migration
```

## Step 10 — Commit and Push

```bash
git add modules/ingestor/src/graph/sbom/mod.rs migration/src/m0042_backfill_suppliers/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add SPDX supplier backfill migration

Add m0042_backfill_suppliers migration that re-processes SPDX SBOMs to
extract package supplier information. Uses filtered query on labels
column to process only SPDX documents, avoiding unnecessary I/O for
CycloneDX records. Reuses the existing suppliers() function from the
ingestor module (made public).

Implements TC-9209"
git push -u origin TC-9209
gh pr create --base main --title "feat(migration): add SPDX supplier backfill migration" --body "..."
```
