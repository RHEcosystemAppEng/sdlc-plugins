# Implementation Plan: TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously
ignored during ingestion. This involves making an existing private function public and
creating a data migration that queries only SPDX documents.

## Files to Modify

### `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public.

- Locate the existing `fn suppliers(...)` function (currently private).
- Change the visibility from `fn suppliers(...)` to `pub fn suppliers(...)`.
- No changes to the function body or signature — only the visibility modifier.
- This allows the migration crate to import and reuse the existing SPDX supplier
  extraction logic, following the DRY principle. The migration crate already depends
  on `trustify-module-ingestor` in `migration/Cargo.toml`, so no new dependency is needed.

## Files to Create

### `migration/src/m0042_backfill_suppliers/mod.rs`

**Purpose**: Data migration that iterates over SPDX SBOM documents, re-parses them,
extracts supplier information, and updates `sbom_package` records.

**Structure** (follows existing pattern from `m0001_initial/mod.rs`):

```rust
use sea_orm_migration::prelude::*;

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

        // Query ONLY SPDX SBOMs using the labels jsonb column filter.
        // CRITICAL: Do NOT use Sbom::find() or an unfiltered query.
        // Production has hundreds of thousands of CycloneDX documents
        // alongside a smaller number of SPDX documents. Loading all
        // documents would cause massive unnecessary I/O and memory
        // pressure, potentially causing OOM or timeout in production.
        let spdx_sboms = sbom::Entity::find()
            .filter(
                Expr::cust("labels->>'type' = 'spdx'")
            )
            .all(db)
            .await?;

        for sbom_record in spdx_sboms {
            // Fetch the raw source document bytes for this SBOM
            let source = SourceDocument::find_by_sbom_id(sbom_record.id)
                .one(db)
                .await?;

            let Some(source) = source else {
                log::warn!("No source document found for SBOM {}", sbom_record.id);
                continue;
            };

            // Re-parse the SPDX document and extract supplier information
            // using the now-public suppliers() function from the ingestor
            let supplier_data = suppliers(&source.data);

            // Update sbom_package records with extracted supplier values
            for (package_ref, supplier_value) in supplier_data {
                sbom_package::Entity::update_many()
                    .filter(sbom_package::Column::SbomId.eq(sbom_record.id))
                    .filter(sbom_package::Column::PackageRef.eq(package_ref))
                    .col_expr(sbom_package::Column::Supplier, Expr::value(supplier_value))
                    .exec(db)
                    .await?;
            }
        }

        Ok(())
    }
}
```

**Key design decisions**:

1. **Filtered database query**: The migration queries `sbom` with
   `WHERE labels->>'type' = 'spdx'` to load only SPDX documents. This is critical
   because production environments have hundreds of thousands of CycloneDX records.
   An unfiltered `Sbom::find()` or `Document::all()` would load all records into memory,
   causing severe performance degradation: unnecessary disk I/O reading hundreds of
   thousands of CycloneDX source documents that don't need processing, excessive memory
   consumption from holding all document data, and potential OOM kills or migration
   timeouts in production.

2. **Reuse of `suppliers()` function**: The migration imports the now-public `suppliers()`
   function from the ingestor module rather than duplicating the SPDX supplier extraction
   logic. The dependency already exists in `migration/Cargo.toml`.

3. **Per-SBOM processing**: Each SPDX SBOM is processed individually: fetch source document,
   parse it, extract suppliers, update `sbom_package` records. This avoids loading all source
   documents into memory simultaneously.

### `migration/src/lib.rs`

**Change**: Register the new migration module.

- Add `mod m0042_backfill_suppliers;` to the module declarations.
- Add `Box::new(m0042_backfill_suppliers::Migration)` to the migration list in the
  `Migrator` implementation (following the pattern of existing migration registrations).

## Database Query Strategy

The migration queries the database as follows:

1. **Primary query** — fetch SPDX SBOMs only:
   ```sql
   SELECT * FROM sbom WHERE labels->>'type' = 'spdx'
   ```
   This uses the `labels` jsonb column on the `sbom` entity (`entity/src/sbom.rs`) which
   stores document metadata. SPDX documents have `{"type": "spdx"}` while CycloneDX
   documents have `{"type": "cyclonedx"}`. Filtering at the database level ensures only
   the relevant subset is loaded.

2. **Per-SBOM source fetch** — for each SPDX SBOM, retrieve its raw document:
   ```sql
   SELECT * FROM source_document WHERE sbom_id = $1
   ```
   Using `SourceDocument::find_by_sbom_id(id)` as noted in the Implementation Notes.

3. **Per-package update** — for each extracted supplier, update the package record:
   ```sql
   UPDATE sbom_package SET supplier = $1 WHERE sbom_id = $2 AND package_ref = $3
   ```

## Tests

### Test 1: SPDX supplier backfill

- Seed an SPDX SBOM with source document containing packages with supplier fields
- Run the migration
- Verify `sbom_package` records now have supplier values populated
- Assert on specific supplier values, not just presence

### Test 2: CycloneDX documents unaffected

- Seed a CycloneDX SBOM with source document (labels: `{"type": "cyclonedx"}`)
- Run the migration
- Verify the CycloneDX SBOM's `sbom_package` records are unchanged
- This confirms the filtered query correctly excludes non-SPDX documents

## Acceptance Criteria Verification

- [x] The migration re-processes all SPDX SBOM documents and populates supplier fields
  -- achieved via filtered query on `labels->>'type' = 'spdx'` and per-document processing
- [x] CycloneDX documents are not loaded or processed by the migration
  -- achieved via database-level filtering; CycloneDX records never enter application memory
- [x] The `suppliers()` function in the ingestor is made public for reuse
  -- visibility changed from `fn` to `pub fn`
- [x] The migration follows the existing migration pattern from `m0001_initial`
  -- implements `MigrationTrait` with `up()` method, registered in `lib.rs`
