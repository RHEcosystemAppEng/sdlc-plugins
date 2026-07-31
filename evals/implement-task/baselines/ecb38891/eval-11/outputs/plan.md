# Implementation Plan for TC-9209

**Task**: Re-process all SPDX SBOMs to extract package supplier information
**Repository**: trustify-backend
**Target Branch**: main
**Task Branch**: TC-9209

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: serena_backend with rust-analyzer

All required sections are present. Proceeding.

## Step 1 -- Parse Task Description

Extracted sections:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Create a data migration re-processing SPDX SBOMs to extract supplier information
- **Files to Modify**: `modules/ingestor/src/graph/sbom/mod.rs`
- **Files to Create**: `migration/src/m0042_backfill_suppliers/mod.rs`
- **API Changes**: none
- **Dependencies**: none

## Step 1.5 -- Verify Description Integrity

Check for a description digest comment on the Jira issue using the marker string `[sdlc-workflow] Description digest:` (per `shared/description-digest-protocol.md`). If no digest comment is found, log a warning and proceed normally (backward compatibility -- tasks created before digest tracking was introduced have no digest comment):

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 4 -- Understand the Code

### Code inspection

Before making any changes, inspect the following files using the Serena instance (`serena_backend`):

1. **`modules/ingestor/src/graph/sbom/mod.rs`** -- use `get_symbols_overview` to understand the module structure, then `find_symbol` with `include_body=true` on the `suppliers()` function to understand its current signature, visibility, and logic. This is the function we need to make public.

2. **`entity/src/sbom.rs`** -- use `get_symbols_overview` to inspect the SBOM entity definition, particularly the `labels` column definition and its type (jsonb). This confirms the filtering mechanism for SPDX vs CycloneDX documents.

3. **`migration/src/m0001_initial/mod.rs`** -- use `get_symbols_overview` and `find_symbol` on the `MigrationTrait` implementation to understand the migration structure pattern (the `up()` method signature, return types, and conventions).

4. **`migration/src/lib.rs`** -- inspect to understand how migrations are registered and discover the module declaration pattern for adding new migrations.

5. **`migration/Cargo.toml`** -- verify that `trustify-module-ingestor` is already listed as a dependency, confirming we can import the `suppliers()` function after making it public.

### Sibling analysis (convention conformance)

Examine `migration/src/m0001_initial/mod.rs` as the primary sibling for the new migration file. Look for:
- Migration struct naming pattern
- `MigrationTrait` implementation pattern
- `up()` and `down()` method signatures
- Error handling patterns in migration code
- How database queries are executed within migrations

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read and extract CI check commands for use in Step 9.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9209
```

## Step 6 -- Implement Changes

### File to Modify: `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public.

- Locate the function signature `fn suppliers(...)` using `find_symbol`
- Change visibility from `fn suppliers(...)` to `pub fn suppliers(...)`
- No changes to the function body -- the extraction logic remains the same
- Add a documentation comment explaining that this function extracts supplier information from SPDX package entries, and noting that it is public to allow reuse by data migrations

### File to Create: `migration/src/m0042_backfill_suppliers/mod.rs`

**Purpose**: Data migration that re-processes SPDX SBOMs to extract and backfill package supplier information.

**Structure** (following `m0001_initial` pattern):

```rust
/// Migration to backfill supplier information for SPDX SBOM packages.
///
/// Re-processes all SPDX SBOM documents to extract the `supplier` field
/// from SPDX package entries and update the corresponding `sbom_package`
/// records. CycloneDX documents are skipped as they already have supplier
/// information populated during ingestion.
pub struct Migration;

impl MigrationTrait for Migration {
    fn name(&self) -> &str {
        "m0042_backfill_suppliers"
    }

    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // ...
    }
}
```

**Database query approach -- FILTERED QUERY**:

The migration MUST use a filtered query to select only SPDX documents. The `sbom` entity's `labels` column (jsonb) supports filtering by document type at the database level:

```rust
// Correct: filtered query -- only loads SPDX documents
let spdx_sboms = sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(&db)
    .await?;
```

This approach is critical because production environments have **hundreds of thousands of CycloneDX documents** alongside a smaller number of SPDX documents. An unfiltered query like `sbom::Entity::find().all(&db)` would load all documents indiscriminately, causing:
- Massive unnecessary I/O fetching hundreds of thousands of CycloneDX records that would be immediately discarded
- Excessive memory consumption materializing ORM entities for non-target records
- Dramatically longer migration execution time

The `labels->>'type' = 'spdx'` filter pushes the subset selection down to PostgreSQL, ensuring only the target SPDX records are transferred and processed.

**Migration logic** (for each SPDX SBOM):

1. Query only SPDX SBOMs using the filtered query on `labels->>'type' = 'spdx'`
2. For each SPDX SBOM, fetch the source document using `SourceDocument::find_by_sbom_id(id)`
3. Parse the source document to extract SPDX package data
4. Call the now-public `suppliers()` function from `trustify-module-ingestor` to extract supplier information
5. Update the corresponding `sbom_package` records with the extracted supplier values

### Module Registration

**File to Modify**: `migration/src/lib.rs`

Add the module declaration for the new migration:

```rust
mod m0042_backfill_suppliers;
```

And register it in the migration list. Note: this file is not listed in "Files to Modify" -- if it requires changes, flag it in Step 9's scope containment check for user approval.

## Step 7 -- Write Tests

Per the Test Requirements:

1. **Test: migration populates supplier information for SPDX SBOMs**
   - Set up a test database with an SPDX SBOM (labels containing `{"type": "spdx"}`) and associated source document with supplier data
   - Run the migration
   - Assert that the `sbom_package` records have supplier fields populated with the expected values (value-based assertions, not just non-null checks)

2. **Test: CycloneDX SBOMs are not affected**
   - Set up a test database with both SPDX and CycloneDX SBOMs
   - Record the CycloneDX `sbom_package` supplier values before migration
   - Run the migration
   - Assert that CycloneDX `sbom_package` records are unchanged (supplier values match pre-migration state)

## Step 8 -- Verify Acceptance Criteria

- [x] The migration re-processes all SPDX SBOM documents and populates supplier fields -- verified by the filtered query selecting SPDX documents and the `suppliers()` extraction logic
- [x] CycloneDX documents are not loaded or processed by the migration -- verified by the `labels->>'type' = 'spdx'` filter at the database level
- [x] The `suppliers()` function in the ingestor is made public for reuse -- change from `fn` to `pub fn`
- [x] The migration follows the existing migration pattern from `m0001_initial` -- struct implements `MigrationTrait` with `up()` method

## Step 9 -- Self-Verification

### Query-scope verification

See `outputs/query-scope.md` for the full analysis. Summary:

- **Target scope**: SPDX SBOMs only (subset of all SBOMs), extracted from the Description's subset-restricting language ("all SPDX SBOMs", "Only SPDX SBOMs need re-processing")
- **Query scope**: Filtered -- `labels->>'type' = 'spdx'` at the database level
- **Rejected**: Unfiltered `Sbom::find()` or `sbom::Entity::find().all()` without a WHERE clause, which would load hundreds of thousands of non-target CycloneDX records in production environments
- **Performance impact**: Unfiltered query would cause unnecessary I/O, excessive memory consumption, and dramatically longer migration time due to loading hundreds of thousands of CycloneDX documents that would be immediately discarded

### Scope containment

Files changed:
- `modules/ingestor/src/graph/sbom/mod.rs` -- listed in Files to Modify (in scope)
- `migration/src/m0042_backfill_suppliers/mod.rs` -- listed in Files to Create (in scope)
- `migration/src/lib.rs` -- NOT listed in Files to Modify or Files to Create. This file needs modification to register the new migration module. Flag for user approval before proceeding.

### Dead parameter detection

No parameters are being removed in this change. The `suppliers()` function signature is only changing visibility (adding `pub`), not modifying parameters.

### Sensitive-pattern check

No secrets, credentials, or environment file references in the changes.

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): backfill SPDX SBOM supplier information

Add data migration m0042 that re-processes SPDX SBOM documents to
extract package supplier information. Makes the ingestor's suppliers()
function public for reuse by the migration. Uses a filtered query on
the labels column to select only SPDX documents, avoiding unnecessary
processing of CycloneDX records.

Implements TC-9209
```

With `--trailer='Assisted-by: Claude Code'`.

### Branch and PR

```
git push -u origin TC-9209
gh pr create --base main --title "feat(migration): backfill SPDX SBOM supplier information" ...
```

PR description includes `Implements [TC-9209](<webUrl>)` with the Jira issue link.
