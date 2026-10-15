# Implementation Plan: TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously
ignored during ingestion. This is a data migration that iterates over SPDX SBOM documents,
re-parses the source data, extracts the `supplier` field from SPDX package entries, and
updates the corresponding `sbom_package` records with the extracted supplier values.

## Task Parsing (Step 1)

- **Jira Key**: TC-9209
- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: (none)
- **Target PR**: (none)
- **Dependencies**: None

## Files to Modify

### `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public.

- Current signature: `fn suppliers(...)` (private)
- New signature: `pub fn suppliers(...)` (public)
- This is the only change to this file. The function body remains unchanged.
- **Rationale**: The migration crate (`migration/`) already depends on
  `trustify-module-ingestor` in `migration/Cargo.toml`, so making the function public
  allows the migration to import and reuse the existing SPDX supplier extraction logic
  without duplicating it. This follows the "Reuse over duplication" principle from the
  skill: when the dependency already exists, make the function public rather than
  duplicating code.

## Files to Create

### `migration/src/m0042_backfill_suppliers/mod.rs`

**Purpose**: Data migration that re-processes all SPDX SBOM documents to backfill
supplier information on `sbom_package` records.

**Structure** (following the pattern from `migration/src/m0001_initial/mod.rs`):

```rust
use sea_orm_migration::prelude::*;

/// Backfills supplier information on sbom_package records by re-processing
/// all SPDX SBOM documents. CycloneDX documents are skipped because they
/// already have supplier information populated during ingestion.
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

        // Step 1: Query only SPDX SBOMs using the labels jsonb column filter.
        // This avoids loading hundreds of thousands of CycloneDX documents
        // that already have supplier information.
        let spdx_sboms = sbom::Entity::find()
            .filter(
                Expr::cust("labels->>'type' = 'spdx'")
            )
            .all(db)
            .await?;

        // Step 2: For each SPDX SBOM, fetch the source document and re-parse
        for sbom in spdx_sboms {
            // Fetch raw document bytes from source_document table
            let source_doc = SourceDocument::find_by_sbom_id(sbom.id)
                .one(db)
                .await?;

            let Some(source_doc) = source_doc else {
                // Skip SBOMs with no source document (defensive guard)
                continue;
            };

            // Step 3: Parse the SPDX document and extract suppliers
            // using the now-public suppliers() function from the ingestor
            let suppliers = trustify_module_ingestor::graph::sbom::suppliers(
                &source_doc.data
            )?;

            // Step 4: Update sbom_package records with extracted supplier values
            for (package_ref, supplier_value) in suppliers {
                sbom_package::Entity::update_many()
                    .filter(sbom_package::Column::SbomId.eq(sbom.id))
                    .filter(sbom_package::Column::PackageRef.eq(package_ref))
                    .col_expr(
                        sbom_package::Column::Supplier,
                        Expr::value(supplier_value),
                    )
                    .exec(db)
                    .await?;
            }
        }

        Ok(())
    }

    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        // Backfill migrations are not reversible — supplier data would need
        // to be cleared, but there is no safe way to distinguish backfilled
        // values from values set during normal ingestion.
        Ok(())
    }
}
```

**Key design decisions**:

1. **Database-level filtering**: The query uses `labels->>'type' = 'spdx'` to filter
   at the database level, ensuring CycloneDX documents (hundreds of thousands in
   production) are never loaded into memory. This is critical for performance — see
   `outputs/query-scope.md` for the full query-scope analysis.

2. **Reuse of `suppliers()` function**: Instead of duplicating the SPDX supplier
   extraction logic, the migration imports the existing function from the ingestor
   module. The dependency already exists in `migration/Cargo.toml`.

3. **Defensive null handling**: Uses `let Some(source_doc) = source_doc else { continue; }`
   to skip SBOMs whose source documents may have been deleted, following the skill's
   "Defensive property access on external data" guidance.

4. **Migration pattern conformance**: Follows the existing migration pattern from
   `m0001_initial/mod.rs` with `MigrationTrait`, `up()`, and `down()` methods.

### `migration/src/lib.rs` (registration)

**Change**: Register the new migration module in the migration library's module
declarations and migration list:

- Add `mod m0042_backfill_suppliers;` to the module declarations
- Add `Box::new(m0042_backfill_suppliers::Migration)` to the migration vec/list

## Database Query Strategy

The migration queries the database as follows:

1. **Primary query** — fetch all SPDX SBOMs:
   ```sql
   SELECT * FROM sbom WHERE labels->>'type' = 'spdx';
   ```
   This uses the jsonb extraction operator (`->>`) to filter on the `type` key within
   the `labels` column. Only SPDX documents are returned.

2. **Per-SBOM source document fetch**:
   ```sql
   SELECT * FROM source_document WHERE sbom_id = ?;
   ```
   Fetches the raw document bytes for parsing via `SourceDocument::find_by_sbom_id()`.

3. **Per-package supplier update**:
   ```sql
   UPDATE sbom_package
   SET supplier = ?
   WHERE sbom_id = ? AND package_ref = ?;
   ```
   Updates each package record with the extracted supplier value.

## Tests to Write

### Test 1: Migration populates supplier for SPDX SBOM

- **Setup**: Insert a test SPDX SBOM with `labels = '{"type": "spdx"}'`, a corresponding
  source document containing SPDX package data with supplier fields, and `sbom_package`
  records with null supplier values.
- **Action**: Run the migration.
- **Assertion**: Verify the `sbom_package` records now have the correct supplier values
  populated from the SPDX source data. Assert on specific supplier string values, not
  just non-null.

### Test 2: Migration does not affect CycloneDX SBOMs

- **Setup**: Insert a CycloneDX SBOM with `labels = '{"type": "cyclonedx"}'`, a
  corresponding source document, and `sbom_package` records with null supplier values.
- **Action**: Run the migration.
- **Assertion**: Verify the `sbom_package` records for the CycloneDX SBOM still have
  null supplier values (unchanged).

## Acceptance Criteria Verification

| Criterion | How verified |
|---|---|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | Test 1 + code review of query filter |
| CycloneDX documents are not loaded or processed | Test 2 + query uses `labels->>'type' = 'spdx'` filter |
| The `suppliers()` function is made public for reuse | Code change: `fn` to `pub fn` |
| Migration follows existing pattern from `m0001_initial` | Structural comparison with `m0001_initial/mod.rs` |

## Scope Containment

All changes are within the declared scope:

- **Files to Modify**: `modules/ingestor/src/graph/sbom/mod.rs` (visibility change only)
- **Files to Create**: `migration/src/m0042_backfill_suppliers/mod.rs`
- **Additional**: `migration/src/lib.rs` needs module registration — this is an
  out-of-scope file that would be flagged in Step 9 for user approval (necessary for
  the migration to be discoverable by the migration runner)

## Data-Flow Trace

1. **Input**: SPDX SBOM records from `sbom` table (filtered by `labels->>'type' = 'spdx'`)
2. **Processing**: For each SBOM, fetch raw document from `source_document`, parse with
   `suppliers()` to extract supplier fields from SPDX package entries
3. **Output**: Updated `sbom_package` records with populated `supplier` column

All stages are connected. The pipeline is complete within the migration's `up()` method.
