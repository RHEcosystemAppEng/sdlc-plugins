# Implementation Plan for TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously
ignored during ingestion. This involves making an existing private helper function public
and creating a data migration that selectively processes only SPDX documents.

## Files to Modify

### `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Change the visibility of the `suppliers()` function from private to public.

- Locate the existing `fn suppliers(...)` function definition.
- Change the signature from `fn suppliers(...)` to `pub fn suppliers(...)`.
- No other changes to this file. The function's logic, parameters, and return type
  remain unchanged.
- Before making this change, use `find_referencing_symbols` (or Grep) on `suppliers` to
  confirm all existing callers are within the same module (since it is currently private)
  and that making it public does not create naming conflicts.

**Rationale for reuse over duplication**: The migration crate already depends on
`trustify-module-ingestor` in `migration/Cargo.toml`, so making the function public
allows direct import without introducing a new dependency. This follows the DRY
principle — the supplier extraction logic lives in one place, and future bug fixes
apply everywhere.

## Files to Create

### `migration/src/m0042_backfill_suppliers/mod.rs`

**Purpose**: A SeaORM data migration that iterates over all SPDX SBOM documents,
re-parses their source data to extract supplier information, and updates the
corresponding `sbom_package` records.

**Structure** (following the pattern from `migration/src/m0001_initial/mod.rs`):

```rust
use sea_orm_migration::prelude::*;

/// Backfills supplier information for all SPDX SBOM packages by re-processing
/// the original SPDX source documents.
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

        // 1. Query only SPDX SBOMs using the labels jsonb column filter.
        //    This avoids loading hundreds of thousands of CycloneDX documents.
        //    Filter: WHERE labels->>'type' = 'spdx'
        let spdx_sboms = Sbom::find()
            .filter(
                Expr::cust("labels->>'type' = 'spdx'")
            )
            .all(db)
            .await?;

        // 2. For each SPDX SBOM, retrieve the source document and extract suppliers.
        for sbom in spdx_sboms {
            let source_doc = SourceDocument::find_by_sbom_id(sbom.id)
                .one(db)
                .await?;

            let Some(source_doc) = source_doc else {
                // No source document found — skip this SBOM.
                log::warn!("No source document found for SBOM {}", sbom.id);
                continue;
            };

            // 3. Parse the SPDX document and extract supplier information
            //    using the now-public suppliers() helper from the ingestor module.
            let raw_bytes = source_doc.data;
            let spdx_doc = serde_json::from_slice(&raw_bytes)?;
            let supplier_map = trustify_module_ingestor::graph::sbom::suppliers(&spdx_doc);

            // 4. Update each sbom_package record with the extracted supplier value.
            for (package_ref, supplier_value) in supplier_map {
                SbomPackage::update_many()
                    .filter(sbom_package::Column::SbomId.eq(sbom.id))
                    .filter(sbom_package::Column::PackageRef.eq(&package_ref))
                    .set(sbom_package::ActiveModel {
                        supplier: Set(Some(supplier_value)),
                        ..Default::default()
                    })
                    .exec(db)
                    .await?;
            }
        }

        Ok(())
    }

    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        // Data migration — down() clears supplier fields for SPDX packages,
        // but this is a lossy rollback. In practice, re-running ingestion
        // would be preferred.
        Ok(())
    }
}
```

**Key design decisions**:

1. **Filtered query**: Use `labels->>'type' = 'spdx'` to query only SPDX SBOMs at the
   database level. Production has hundreds of thousands of CycloneDX documents that do not
   need processing. Loading all documents and filtering in application code would cause
   unnecessary I/O and memory pressure. The `labels` jsonb column supports this filter
   directly.

2. **Reuse `suppliers()` function**: Import the now-public `suppliers()` function from
   `trustify_module_ingestor::graph::sbom` rather than duplicating the extraction logic.
   The dependency already exists in `migration/Cargo.toml`.

3. **Graceful handling of missing source documents**: Use `if let` / `Option` handling
   to skip SBOMs that have no source document rather than panicking. Log a warning for
   observability.

4. **Batch updates per SBOM**: For each SPDX SBOM, extract all suppliers and update
   the corresponding `sbom_package` records. Use `update_many()` with filters on
   `sbom_id` and `package_ref` to target the correct rows.

### `migration/src/lib.rs` (registration)

**Change**: Register the new migration module in the migration library's module
declarations and migration list. Add:

```rust
mod m0042_backfill_suppliers;
```

And add `m0042_backfill_suppliers::Migration` to the migration vec returned by
the `migrations()` function (or equivalent registration mechanism, following the
pattern established by `m0001_initial`).

**Note**: This file is not listed in "Files to Modify" in the task description,
but registering the migration is mechanically required for the new migration file
to be discovered. This would be flagged in Step 9's scope containment check for
user approval.

## Database Query Strategy

The critical query in this migration filters SBOMs by document type:

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx';
```

This leverages the `labels` jsonb column on the `sbom` entity (`entity/src/sbom.rs`).
SPDX documents are tagged with `{"type": "spdx"}` and CycloneDX documents with
`{"type": "cyclonedx"}`.

**Why filter at the database level**: The task explicitly states that production
environments have hundreds of thousands of CycloneDX documents alongside a smaller
number of SPDX documents. Loading all SBOMs and filtering in application code would:
- Fetch hundreds of thousands of unnecessary rows
- Consume significant memory for records that will be immediately discarded
- Increase migration runtime substantially

A GIN index on `labels` (if present) or a btree index on the expression
`(labels->>'type')` would further optimize this query, but index creation is
outside the scope of this task.

## Tests to Write

### Test 1: SPDX supplier backfill

**Location**: Within the migration test module or `tests/` directory, following
existing migration test patterns.

- Set up a test SPDX SBOM with known package entries that have supplier information
  in the source document but no supplier values in `sbom_package` records.
- Run the migration's `up()` method.
- Assert that the `sbom_package` records now have the correct supplier values
  populated (value-based assertions on specific supplier strings, not just
  non-null checks).

### Test 2: CycloneDX documents unaffected

- Set up a test CycloneDX SBOM with `{"type": "cyclonedx"}` labels.
- Set the supplier field to a known value (or null).
- Run the migration's `up()` method.
- Assert that the CycloneDX SBOM's `sbom_package` records are unchanged — the
  migration should not have loaded or processed this document.

## Acceptance Criteria Verification

| Criterion | How verified |
|-----------|-------------|
| Migration re-processes all SPDX SBOMs and populates supplier fields | Test 1 + query uses `labels->>'type' = 'spdx'` filter |
| CycloneDX documents are not loaded or processed | Test 2 + query filter excludes `cyclonedx` type |
| `suppliers()` function made public | Visibility change from `fn` to `pub fn` in `mod.rs` |
| Migration follows existing pattern from `m0001_initial` | Structure mirrors `m0001_initial/mod.rs` with `MigrationTrait` implementation |

## Data-Flow Trace

1. **Input**: Database query fetches SPDX SBOM records from `sbom` table (filtered by labels).
2. **Source retrieval**: For each SBOM, `SourceDocument::find_by_sbom_id()` fetches raw document bytes from `source_document` table.
3. **Processing**: Raw bytes are deserialized into SPDX document structure, then `suppliers()` extracts package-to-supplier mappings.
4. **Output/Persistence**: Each extracted supplier value is written back to the corresponding `sbom_package` record via `update_many()`.

The data flow is complete — every stage connects to the next, and the output
(updated `sbom_package` records) is the intended deliverable of the migration.
