# Implementation Plan: TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously ignored during ingestion. This involves making an existing private function public for reuse and creating a new data migration that filters to SPDX documents only.

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public so the migration crate can import and reuse it.

- Locate the private function `fn suppliers(...)` in this module.
- Change the visibility from `fn suppliers(...)` to `pub fn suppliers(...)`.
- No logic changes are needed -- the extraction logic already works correctly; it was simply not exported.
- Before making the change, use `find_referencing_symbols` (or Grep) to verify no existing callers depend on it being private or would break with the visibility change. Since this is a visibility widening (private to public), it is backward-compatible -- no existing callers are affected.

**Rationale for reuse over duplication**: The `migration` crate already depends on `trustify-module-ingestor` in `migration/Cargo.toml`, so the dependency relationship exists. Making the function public follows the DRY principle and ensures any future bug fixes to supplier extraction logic apply in one place.

## Files to Create

### 2. `migration/src/m0042_backfill_suppliers/mod.rs`

**Change**: Create a new data migration module that re-processes SPDX SBOMs and populates supplier fields on `sbom_package` records.

**Structure** (following the pattern in `migration/src/m0001_initial/mod.rs`):

```rust
use sea_orm_migration::prelude::*;

/// Data migration that re-processes all SPDX SBOM documents to extract
/// and backfill package supplier information into sbom_package records.
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
        // records. Loading all documents would cause excessive I/O and memory
        // pressure for no benefit, since CycloneDX documents already have
        // supplier information populated during ingestion.
        let spdx_sboms = Entity::find()
            .filter(
                Expr::col(sbom::Column::Labels)
                    .cast_as(Alias::new("text"))
                    .like("%\"type\":\"spdx\"%")
            )
            // OR using SeaORM's JSON operator support:
            // .filter(
            //     Expr::cust_with_values(
            //         "labels->>'type' = $1",
            //         ["spdx"]
            //     )
            // )
            .all(db)
            .await?;

        for sbom_record in spdx_sboms {
            // Fetch the raw source document bytes for this SBOM
            let source_doc = SourceDocument::find_by_sbom_id(sbom_record.id)
                .one(db)
                .await?;

            let Some(source_doc) = source_doc else {
                // Source document missing -- skip this record, log warning
                tracing::warn!(
                    sbom_id = %sbom_record.id,
                    "No source document found for SPDX SBOM, skipping supplier backfill"
                );
                continue;
            };

            // Re-parse the SPDX document and extract supplier information
            // using the now-public suppliers() function from the ingestor
            let suppliers = trustify_module_ingestor::graph::sbom::suppliers(&source_doc.data);

            // Update each sbom_package record with the extracted supplier value
            for (package_ref, supplier_value) in suppliers {
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

1. **Filtered query at the database level**: The query uses `labels->>'type' = 'spdx'` (or equivalent SeaORM JSON filtering) to only load SPDX SBOM records. This is critical because production environments have hundreds of thousands of CycloneDX documents. Loading all documents with an unfiltered query (e.g., `Sbom::find()` or `Entity::all()`) and then filtering in application code would cause:
   - Massive unnecessary I/O reading hundreds of thousands of CycloneDX records from the database
   - Excessive memory consumption materializing all those records in the application
   - Significantly longer migration runtime with no benefit

2. **Reuse of `suppliers()` function**: The migration imports and calls the public `suppliers()` function from `trustify-module-ingestor` rather than duplicating the extraction logic. The dependency already exists in `migration/Cargo.toml`.

3. **Defensive handling**: The migration gracefully handles missing source documents (logs a warning and continues) rather than panicking. This protects against data inconsistencies in production.

### 3. `migration/src/lib.rs`

**Change**: Register the new migration module. Add the `m0042_backfill_suppliers` module declaration and include `Migration` in the migration runner's list. This follows the pattern established by `m0001_initial`.

```rust
mod m0042_backfill_suppliers;
// ... in the migration list:
Box::new(m0042_backfill_suppliers::Migration),
```

Note: This file is not listed in "Files to Modify" in the task. Per Step 9 scope containment, this would be flagged as an out-of-scope change for user approval. However, it is structurally required -- a migration module that is not registered in `lib.rs` will never run. The user should approve this addition.

## Database Query for the Migration

The migration queries the `sbom` table filtered by the `labels` jsonb column to select only SPDX documents:

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx';
```

In SeaORM, this translates to a filtered query using JSON path extraction on the `labels` column. The `labels` column stores metadata as `jsonb`, where SPDX documents have `{"type": "spdx"}` and CycloneDX documents have `{"type": "cyclonedx"}`.

This filtered query is essential. An unfiltered query (`SELECT * FROM sbom`) would load hundreds of thousands of CycloneDX records that do not need re-processing, causing:
- Unnecessary database I/O (reading rows that will be immediately discarded)
- Excessive application memory usage (materializing all records)
- Longer migration wall-clock time with zero benefit

## Tests

### Test 1: SPDX supplier backfill

Location: within the migration module or in `tests/`

```rust
/// Verifies that the migration extracts and populates supplier information
/// for SPDX SBOM documents.
#[tokio::test]
async fn test_migration_backfills_spdx_suppliers() {
    // Given an SPDX SBOM in the database with no supplier information
    // (insert test SBOM with labels = {"type": "spdx"} and associated
    // sbom_package records with null supplier fields, plus a source_document
    // containing SPDX data with supplier entries)

    // When the migration runs
    // (execute m0042_backfill_suppliers::Migration::up())

    // Then the sbom_package records should have supplier values populated
    // (assert_eq! on the supplier column values, verifying specific
    // supplier strings match the SPDX source data)
}
```

### Test 2: CycloneDX documents are unaffected

```rust
/// Verifies that CycloneDX SBOM documents are not loaded or processed
/// by the supplier backfill migration.
#[tokio::test]
async fn test_migration_skips_cyclonedx_documents() {
    // Given a CycloneDX SBOM in the database
    // (insert test SBOM with labels = {"type": "cyclonedx"} and associated
    // sbom_package records)

    // When the migration runs

    // Then the CycloneDX sbom_package records should remain unchanged
    // AND the source_document for the CycloneDX SBOM should not have been
    // fetched (verify no unnecessary I/O occurred)
}
```

## Acceptance Criteria Verification

| Criterion | How verified |
|-----------|-------------|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | Filtered query selects all SPDX SBOMs; for each, re-parses source and updates sbom_package supplier column. Test 1 validates. |
| CycloneDX documents are not loaded or processed | WHERE clause filters to `type = 'spdx'` only; CycloneDX records are never fetched from DB. Test 2 validates. |
| `suppliers()` function made public for reuse | Visibility changed from `fn` to `pub fn` in `modules/ingestor/src/graph/sbom/mod.rs`. |
| Migration follows existing pattern from `m0001_initial` | Implements `MigrationTrait` with `up()` method, same module structure. |
