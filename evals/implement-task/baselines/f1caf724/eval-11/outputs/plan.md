# Implementation Plan: TC-9209

## Task Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously ignored during ingestion. This is a data migration that targets only SPDX documents -- CycloneDX documents already have supplier information and must not be loaded or processed.

## Step 0 -- Validate Project Configuration

Project Configuration in CLAUDE.md verified:
- Repository Registry: present (trustify-backend, serena_backend instance)
- Jira Configuration: present (Project key: TC, Cloud ID, Feature issue type ID)
- Code Intelligence: present (serena_backend with rust-analyzer)

All sections valid. Proceeding.

## Step 1 -- Parse Jira Task

Extracted from TC-9209 structured description:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Create a data migration re-processing all SPDX SBOMs to extract supplier information. Only SPDX SBOMs need re-processing -- CycloneDX documents already have supplier information populated.
- **Files to Modify**: `modules/ingestor/src/graph/sbom/mod.rs`
- **Files to Create**: `migration/src/m0042_backfill_suppliers/mod.rs`
- **API Changes**: none
- **Dependencies**: none

All required sections present. No gaps found.

## Step 1.5 -- Verify Description Integrity

Would fetch comments via `jira.get_issue_comments(TC-9209)` and look for `[sdlc-workflow] Description digest:` marker. If no digest comment is found, log warning and proceed normally (backward compatibility):

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 4 -- Understand the Code

### Code Inspection

Before making any changes, inspect the following files using the serena_backend Serena instance:

1. **`modules/ingestor/src/graph/sbom/mod.rs`** -- use `get_symbols_overview` to understand the module structure, then `find_symbol` with `include_body=true` on the `suppliers()` function to understand the existing SPDX supplier extraction logic and its current visibility (private `fn`).

2. **`migration/src/m0001_initial/mod.rs`** -- use `get_symbols_overview` to understand the existing migration pattern. Read the `MigrationTrait` implementation and the `up()` method to learn the structure new migrations must follow.

3. **`migration/src/lib.rs`** -- use `find_symbol` to check how migrations are registered (likely a vector or array of migration modules) to ensure the new `m0042_backfill_suppliers` module is properly registered.

4. **`entity/src/sbom.rs`** -- use `get_symbols_overview` to inspect the SBOM entity definition, specifically verifying the `labels` column exists as a `jsonb` type and understanding the SeaORM column/entity definition. This is critical for verifying that database-level filtering by document type is possible.

5. **`migration/Cargo.toml`** -- read to verify the existing dependency on `trustify-module-ingestor`, confirming that the migration crate can import the `suppliers()` function once it is made public.

### Convention Conformance Analysis

Sibling files analyzed:
- `migration/src/m0001_initial/mod.rs` -- migration structure conventions
- `modules/ingestor/src/graph/advisory/mod.rs` -- sibling ingestion module patterns

Discovered conventions:
- **Migration structure**: Each migration is a module under `migration/src/` implementing `MigrationTrait` with an `up()` method
- **Error handling**: Uses `Result<T, AppError>` with `.context()` for error wrapping
- **Entity access**: Uses SeaORM entity patterns for database queries
- **Module visibility**: Functions that need cross-crate access use `pub fn`

### Query-Scope Verification (Step 9 brought forward)

**Target scope extraction**: The task Description contains subset-restricting language: "re-processes all SPDX SBOMs" and "Only SPDX SBOMs need re-processing -- CycloneDX documents already have supplier information populated during ingestion." This explicitly targets a subset of all SBOM documents -- only those of type SPDX.

**Database-level filtering verification**: The Implementation Notes state that the `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores metadata about each document. SPDX documents have `{"type": "spdx"}` in their labels, while CycloneDX documents have `{"type": "cyclonedx"}`. This means the database supports filtering by document type at the query level using `labels->>'type' = 'spdx'`.

**Query scope decision**: The migration MUST use a filtered query to select only SPDX documents from the database. An unfiltered query such as `Sbom::find()` or iterating all documents would load hundreds of thousands of CycloneDX records unnecessarily. The Implementation Notes explicitly state: "Production environments have hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents. The migration should only load and process SPDX documents to avoid unnecessary I/O."

**REJECTED approach -- unfiltered query**: Using `Sbom::find()` (which loads all SBOM records) and then discarding CycloneDX documents in application code is explicitly rejected. This approach would:
- Load hundreds of thousands of unnecessary CycloneDX records into memory
- Waste database I/O and network bandwidth
- Significantly increase migration runtime in production
- Violate the task's acceptance criterion that "CycloneDX documents are not loaded or processed by the migration"

**ACCEPTED approach -- filtered query**: Use a SeaORM query with a JSON filter on the `labels` column:
```rust
use sea_orm::prelude::*;
use entity::sbom::{Entity as Sbom, Column as SbomColumn};

// Filter to only SPDX documents at the database level
let spdx_sboms = Sbom::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(&db)
    .await?;
```

This pushes the filter down to PostgreSQL, leveraging the `jsonb` column's native operators. Only SPDX records are transferred from the database to the application, avoiding the I/O cost of loading hundreds of thousands of CycloneDX documents.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9209
```

Branch named after the Jira issue ID (TC-9209), based on Target Branch (main).

## Step 6 -- Implement Changes

### File 1: `modules/ingestor/src/graph/sbom/mod.rs` (MODIFY)

**Change**: Make the `suppliers()` function public by changing its visibility from `fn suppliers(...)` to `pub fn suppliers(...)`.

**Rationale**: The migration crate needs to reuse the existing SPDX supplier extraction logic. The migration crate already depends on `trustify-module-ingestor` in `migration/Cargo.toml`, so making the function public allows direct import without duplicating code.

**Details**:
- Locate the `suppliers()` function using `find_symbol("suppliers")`
- Change `fn suppliers(` to `pub fn suppliers(`
- Add a documentation comment: `/// Extracts supplier information from SPDX package entries.`
- No other changes to the function body or signature

### File 2: `migration/src/m0042_backfill_suppliers/mod.rs` (CREATE)

**Change**: Create a new migration module that re-processes SPDX SBOMs to backfill supplier information.

**Structure** (following the `m0001_initial` migration pattern):
```rust
use sea_orm_migration::prelude::*;
use sea_orm::prelude::*;
use entity::sbom::{Entity as Sbom, Column as SbomColumn};
use trustify_module_ingestor::graph::sbom::suppliers;

/// Migration to backfill package supplier information from SPDX SBOMs.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0042_backfill_suppliers"
    }
}

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // FILTERED QUERY: Select only SPDX documents using the labels jsonb column.
        // This avoids loading hundreds of thousands of CycloneDX documents that
        // already have supplier information populated.
        let spdx_sboms = Sbom::find()
            .filter(Expr::cust("labels->>'type' = 'spdx'"))
            .all(db)
            .await?;

        for sbom in spdx_sboms {
            // Fetch the raw source document for this SBOM
            let source_doc = SourceDocument::find_by_sbom_id(sbom.id)
                .one(db)
                .await?
                .context("source document not found for SBOM")?;

            // Re-parse and extract supplier information using the existing helper
            let supplier_data = suppliers(&source_doc.data)?;

            // Update sbom_package records with extracted supplier values
            for (package_id, supplier) in supplier_data {
                // Update the sbom_package record
                SbomPackage::update_many()
                    .filter(sbom_package::Column::SbomId.eq(sbom.id))
                    .filter(sbom_package::Column::PackageId.eq(package_id))
                    .col_expr(sbom_package::Column::Supplier, Expr::value(supplier))
                    .exec(db)
                    .await?;
            }
        }

        Ok(())
    }
}
```

Key design decisions:
- **Filtered query**: Uses `labels->>'type' = 'spdx'` to filter at the database level, NOT loading all documents
- **Reuses `suppliers()` function**: Imports from the ingestor module instead of duplicating extraction logic
- **Follows migration pattern**: Implements `MigrationTrait` with `up()` method, matching `m0001_initial`

### File 3: `migration/src/lib.rs` (MODIFY -- registration only)

Note: This file is not listed in Files to Modify, so this would be flagged in Step 9's scope containment check. The new migration module needs to be registered in `migration/src/lib.rs` for the migration runner to discover it. This will be flagged for user approval.

## Step 7 -- Write Tests

### Test file: Within `migration/src/m0042_backfill_suppliers/mod.rs` or appropriate test location

**Test 1**: Verify migration populates supplier information for an SPDX SBOM
- Given: An SPDX SBOM document in the database with labels `{"type": "spdx"}` and packages without supplier information
- When: The migration `up()` method runs
- Then: The `sbom_package` records are updated with the extracted supplier values

**Test 2**: Verify CycloneDX SBOMs are not affected by the migration
- Given: A CycloneDX SBOM document in the database with labels `{"type": "cyclonedx"}`
- When: The migration `up()` method runs
- Then: The CycloneDX SBOM's package records are not loaded, not modified, and retain their original values

## Step 8 -- Verify Acceptance Criteria

- [x] The migration re-processes all SPDX SBOM documents and populates supplier fields -- verified by filtered query + supplier extraction
- [x] CycloneDX documents are not loaded or processed by the migration -- verified by `labels->>'type' = 'spdx'` filter at database level
- [x] The `suppliers()` function in the ingestor is made public for reuse -- changed to `pub fn`
- [x] The migration follows the existing migration pattern from `m0001_initial` -- implements `MigrationTrait` with `up()` method

## Step 9 -- Self-Verification

### Scope containment
Files in scope per task description:
- `modules/ingestor/src/graph/sbom/mod.rs` (modify) -- in scope
- `migration/src/m0042_backfill_suppliers/mod.rs` (create) -- in scope
- `migration/src/lib.rs` -- OUT OF SCOPE. Flagged for user approval: needs modification to register the new migration module.

### Query-scope verification
See Step 4 analysis above. The query uses a filtered approach (`labels->>'type' = 'spdx'`) matching the task's target scope (SPDX SBOMs only). No unfiltered query is used. The approach avoids loading hundreds of thousands of CycloneDX documents in production.

### Dead parameter detection
No parameters removed in this change -- not applicable.

### Duplication check
The migration reuses the existing `suppliers()` function from the ingestor module. No duplication of supplier extraction logic.

## Step 10 -- Commit and Push

### Commit message:
```
feat(migration): backfill SPDX SBOM supplier information

Add migration m0042 to re-process SPDX SBOMs and extract package
supplier data that was previously ignored during ingestion. Uses a
filtered query (labels->>'type' = 'spdx') to avoid loading CycloneDX
documents. Makes the suppliers() helper public for cross-crate reuse.

Implements TC-9209
```

With `--trailer='Assisted-by: Claude Code'`.

### Branch and PR:
```
git push -u origin TC-9209
gh pr create --base main --title "feat(migration): backfill SPDX SBOM supplier information" --body "..."
```

PR targets `--base main` (the Target Branch from the task description).

## Step 11 -- Update Jira

- Update `customfield_10875` (Git Pull Request) with PR URL in ADF format
- Add comment summarizing changes made
- Transition TC-9209 to In Review
