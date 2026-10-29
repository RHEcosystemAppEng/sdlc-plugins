# Implementation Plan: TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously
ignored during ingestion. The migration iterates over SPDX SBOM documents only, re-parses
each source document, extracts the `supplier` field from SPDX package entries, and updates
the corresponding `sbom_package` records.

---

## Files to Modify

### `modules/ingestor/src/graph/sbom/mod.rs`

**Change:** Make the `suppliers()` function public.

- Locate the existing private function `fn suppliers(...)`.
- Change the visibility from `fn suppliers(...)` to `pub fn suppliers(...)`.
- No changes to the function body or signature beyond visibility.
- Verify via `find_referencing_symbols` that no existing callers are broken by the
  visibility change (making a private function public is backward-compatible; no callers
  need updating).

---

## Files to Create

### `migration/src/m0042_backfill_suppliers/mod.rs`

**Purpose:** Data migration that re-processes SPDX SBOMs to backfill supplier information.

**Structure (following `m0001_initial/mod.rs` pattern):**

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
        // This is critical: production has hundreds of thousands of CycloneDX
        // documents. Loading all SBOMs and filtering in application code would
        // cause excessive memory usage and unnecessary I/O.
        let spdx_sboms = sbom::Entity::find()
            .filter(Expr::cust("labels->>'type' = 'spdx'"))
            .all(db)
            .await?;

        for sbom in spdx_sboms {
            // Fetch the raw source document bytes
            let source = SourceDocument::find_by_sbom_id(sbom.id)
                .one(db)
                .await?;

            let Some(source) = source else {
                log::warn!("No source document for SBOM {}, skipping", sbom.id);
                continue;
            };

            // Re-parse the SPDX document and extract supplier information
            // using the now-public suppliers() function from the ingestor module
            let suppliers = trustify_module_ingestor::graph::sbom::suppliers(&source.data);

            // Update sbom_package records with extracted supplier values
            for (package_ref, supplier_value) in suppliers {
                sbom_package::Entity::update_many()
                    .filter(sbom_package::Column::SbomId.eq(sbom.id))
                    .filter(sbom_package::Column::PackageRef.eq(&package_ref))
                    .col_expr(sbom_package::Column::Supplier, Expr::value(&supplier_value))
                    .exec(db)
                    .await?;
            }
        }

        Ok(())
    }

    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        // Supplier backfill is not reversible in a meaningful way
        Ok(())
    }
}
```

**Key design decisions:**

1. **Filtered database query:** The migration uses `Expr::cust("labels->>'type' = 'spdx'")` to
   filter at the database level. This ensures only SPDX documents are loaded from the database.
   An unfiltered query such as `Sbom::find().all(db)` followed by application-level filtering
   (e.g., `.filter(|s| s.labels["type"] == "spdx")`) is explicitly rejected because:
   - Production has hundreds of thousands of CycloneDX documents that would be loaded into
     memory unnecessarily.
   - For each loaded SBOM, the migration would also fetch the source document from the
     `source_document` table, multiplying the I/O waste.
   - The `labels` jsonb column already supports this filter at the database level, so there
     is no technical reason to defer filtering to application code.

2. **Reuse of `suppliers()` function:** The migration imports and calls the existing
   `suppliers()` function from the ingestor module rather than duplicating the SPDX supplier
   extraction logic. The `migration` crate already depends on `trustify-module-ingestor` in
   `migration/Cargo.toml`, so no new dependency is needed.

3. **Migration registration:** Register the new migration in `migration/src/lib.rs` by adding
   `mod m0042_backfill_suppliers;` and appending `Box::new(m0042_backfill_suppliers::Migration)`
   to the migration list. (This file is not in the task's "Files to Modify" scope, so it would
   be flagged in Step 9's scope containment check for user approval.)

---

## Registration (out-of-scope flag)

The new migration module must be registered in `migration/src/lib.rs`. This file is not listed
in "Files to Modify", so per Step 9 scope containment rules, this out-of-scope change would be
flagged for user approval before proceeding. The change is a single `mod` declaration and a
`Box::new(...)` entry in the migrations vector.

---

## Tests

### Test 1: SPDX supplier backfill

Create a test that:
1. Inserts an SPDX SBOM record with `labels: {"type": "spdx"}` and a corresponding
   source document containing SPDX package data with supplier fields.
2. Inserts `sbom_package` records with empty supplier values.
3. Runs the migration.
4. Asserts that the `sbom_package` records now have the correct supplier values populated.

### Test 2: CycloneDX documents unaffected

Create a test that:
1. Inserts a CycloneDX SBOM record with `labels: {"type": "cyclonedx"}` and `sbom_package`
   records with existing (or empty) supplier values.
2. Runs the migration.
3. Asserts that the CycloneDX `sbom_package` records are unchanged -- the migration did not
   load or process them.

---

## Database Query Strategy

The migration queries the database using a filtered SeaORM query:

```rust
sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(db)
    .await?
```

This translates to the SQL:

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx'
```

This approach loads only SPDX SBOMs from the database, avoiding the cost of loading hundreds
of thousands of CycloneDX documents that do not need re-processing.

---

## Acceptance Criteria Verification

| Criterion | How Satisfied |
|---|---|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | Filtered query selects all SPDX SBOMs; each is re-parsed and `sbom_package` records updated |
| CycloneDX documents are not loaded or processed | `WHERE labels->>'type' = 'spdx'` excludes CycloneDX at the database level |
| The `suppliers()` function in the ingestor is made public for reuse | Visibility changed from `fn` to `pub fn` |
| The migration follows the existing migration pattern from `m0001_initial` | Implements `MigrationTrait` with `up()` and `down()` methods, same structure as `m0001_initial/mod.rs` |
