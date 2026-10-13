# Implementation Plan: TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously ignored during ingestion. This requires modifying one existing file and creating one new file.

## Files to Modify

### `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public.

- Locate the existing `fn suppliers(...)` function (currently private).
- Change visibility from `fn suppliers(...)` to `pub fn suppliers(...)`.
- No other changes to the function signature or body -- the extraction logic is already correct.
- The migration crate already depends on `trustify-module-ingestor` in `migration/Cargo.toml`, so no dependency changes are needed.

This follows the "Reuse over duplication" principle from the skill: the dependency relationship already exists, so making the function public is preferred over duplicating the supplier extraction logic.

## Files to Create

### `migration/src/m0042_backfill_suppliers/mod.rs`

**Purpose**: A data migration that iterates over SPDX SBOM documents, re-parses them, extracts supplier fields from SPDX package entries, and updates the corresponding `sbom_package` records.

**Structure** (following the pattern from `migration/src/m0001_initial/mod.rs`):

```rust
use sea_orm_migration::prelude::*;
use sea_orm::prelude::*;
use sea_orm::QueryFilter;

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

        // Query ONLY SPDX SBOMs using a filtered database query.
        // Production has hundreds of thousands of CycloneDX records that
        // already have supplier information -- loading them would waste I/O
        // and memory for no benefit.
        let spdx_sboms = sbom::Entity::find()
            .filter(Expr::cust("labels->>'type' = 'spdx'"))
            .all(db)
            .await?;

        for sbom in spdx_sboms {
            // Fetch the raw source document for this SBOM
            let source = SourceDocument::find_by_sbom_id(sbom.id)
                .one(db)
                .await?;

            let Some(source) = source else {
                // No source document available -- skip this SBOM
                continue;
            };

            // Re-parse the SPDX document and extract supplier information
            // using the now-public suppliers() function from the ingestor
            let suppliers = trustify_module_ingestor::graph::sbom::suppliers(&source.data);

            // Update each sbom_package record with the extracted supplier value
            for (package_ref, supplier_value) in suppliers {
                // Find the sbom_package record and update its supplier field
                sbom_package::Entity::update_many()
                    .filter(sbom_package::Column::SbomId.eq(sbom.id))
                    .filter(sbom_package::Column::PackageRef.eq(package_ref))
                    .col_expr(sbom_package::Column::Supplier, Expr::value(supplier_value))
                    .exec(db)
                    .await?;
            }
        }

        Ok(())
    }

    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        // Backfill migrations are not reversible -- supplier data would need
        // to be cleared, but that destroys valid data for documents ingested
        // after this migration.
        Ok(())
    }
}
```

**Key design decisions**:

1. **Filtered query at the database level**: Uses `WHERE labels->>'type' = 'spdx'` to load only SPDX documents. This avoids loading hundreds of thousands of CycloneDX records that already have supplier information populated. See `outputs/query-scope.md` for the full query-scope verification analysis.

2. **Reuse of `suppliers()` function**: Imports the now-public `suppliers()` function from `modules/ingestor/src/graph/sbom/mod.rs` rather than duplicating the SPDX supplier extraction logic. The migration crate already has `trustify-module-ingestor` as a dependency.

3. **Follows existing migration pattern**: Implements `MigrationTrait` with `up()` and `down()` methods, matching the structure in `migration/src/m0001_initial/mod.rs`.

4. **Source document retrieval**: Uses `SourceDocument::find_by_sbom_id(id)` to fetch the raw SPDX document bytes for re-parsing, as specified in the Implementation Notes.

### `migration/src/lib.rs` (registration)

The new migration module must be registered in `migration/src/lib.rs` by adding it to the migration list. This involves:

- Adding `mod m0042_backfill_suppliers;` declaration
- Adding the migration to the `Migrator` struct's migration list

(This file is not listed in Files to Modify, so it would be flagged during Step 9's scope containment check for user approval. It is a necessary out-of-scope change for the migration to be discoverable by the migration runner.)

## Tests

### Test: SPDX SBOM supplier backfill

Verify that the migration populates supplier information for an SPDX SBOM:

1. **Given**: An SPDX SBOM document with package entries containing supplier fields, ingested without supplier extraction (simulating the pre-migration state). The SBOM has `labels: {"type": "spdx"}`.
2. **When**: The migration runs.
3. **Then**: The `sbom_package` records for this SBOM have their supplier fields populated with the values extracted from the SPDX document.

### Test: CycloneDX SBOMs unaffected

Verify that CycloneDX SBOMs are not processed by the migration:

1. **Given**: A CycloneDX SBOM document with `labels: {"type": "cyclonedx"}` and existing supplier information.
2. **When**: The migration runs.
3. **Then**: The CycloneDX SBOM's `sbom_package` records are unchanged. The source document for the CycloneDX SBOM is never fetched (verifiable by asserting no `SourceDocument::find_by_sbom_id` call for its ID, or by confirming its records remain identical).

## Database Query Strategy

The migration queries the `sbom` table with a JSONB filter:

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx'
```

This ensures:
- Only SPDX documents are loaded into memory
- CycloneDX documents (hundreds of thousands in production) are never fetched
- The database handles filtering efficiently, potentially using a GIN index on the `labels` column
- Memory usage is proportional to the number of SPDX documents, not the total SBOM count

## Acceptance Criteria Mapping

| Criterion | How satisfied |
|-----------|--------------|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | Filtered query loads all SPDX SBOMs; loop re-parses each and updates `sbom_package` records |
| CycloneDX documents are not loaded or processed | `WHERE labels->>'type' = 'spdx'` excludes CycloneDX at the database level |
| The `suppliers()` function is made public for reuse | Visibility changed from `fn` to `pub fn` in `mod.rs` |
| The migration follows the existing migration pattern | Implements `MigrationTrait` with `up()`/`down()` matching `m0001_initial` |
