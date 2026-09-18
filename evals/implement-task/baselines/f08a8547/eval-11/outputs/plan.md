# Implementation Plan: TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously
ignored during ingestion. This involves making an existing private helper public for
reuse and creating a new data migration module.

---

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change:** Make the `suppliers()` function public.

- Locate the existing private function: `fn suppliers(...)`
- Change the visibility to `pub fn suppliers(...)`
- No changes to the function body, parameters, or return type -- only the visibility modifier.
- Verify with `find_referencing_symbols` that no existing callers are broken by the visibility change (making a private function public is always backward-compatible for existing callers within the same module).

---

## Files to Create

### 2. `migration/src/m0042_backfill_suppliers/mod.rs`

**Purpose:** Data migration that iterates over SPDX SBOM documents, re-parses them,
extracts the `supplier` field from SPDX package entries, and updates the corresponding
`sbom_package` records in the database.

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
        // 1. Query ONLY SPDX SBOMs using a filtered database query:
        //    SELECT id FROM sbom WHERE labels->>'type' = 'spdx'
        //
        //    CRITICAL: Do NOT use an unfiltered query like Sbom::find().all().
        //    The labels column has a 'type' key that distinguishes SPDX from
        //    CycloneDX documents. Production has hundreds of thousands of
        //    CycloneDX documents -- loading them would cause unnecessary I/O
        //    and the migration would process records it should skip.
        //
        // 2. For each SPDX SBOM:
        //    a. Fetch the raw source document using SourceDocument::find_by_sbom_id(id)
        //    b. Parse the SPDX document from the raw bytes
        //    c. Call the now-public `suppliers()` function from
        //       trustify_module_ingestor::graph::sbom to extract supplier info
        //    d. Update the corresponding sbom_package records with the extracted
        //       supplier values
        //
        // 3. Process in batches to manage memory for large datasets

        let db = manager.get_connection();

        // Query filtered to SPDX documents only
        let spdx_sboms = db.query_all(Statement::from_string(
            DbBackend::Postgres,
            "SELECT id FROM sbom WHERE labels->>'type' = 'spdx'".to_string(),
        )).await?;

        for row in spdx_sboms {
            let sbom_id: i64 = row.try_get("", "id")?;

            // Fetch source document
            // Parse SPDX data
            // Extract suppliers using the public suppliers() function
            // Update sbom_package records with supplier values
        }

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Reverse: set supplier fields back to NULL for SPDX sbom_package records
        let db = manager.get_connection();
        db.execute(Statement::from_string(
            DbBackend::Postgres,
            "UPDATE sbom_package SET supplier = NULL WHERE sbom_id IN (SELECT id FROM sbom WHERE labels->>'type' = 'spdx')".to_string(),
        )).await?;
        Ok(())
    }
}
```

**Key design decisions:**

1. **Database-level filtering**: The query uses `WHERE labels->>'type' = 'spdx'` to
   filter at the database level. This ensures CycloneDX documents are never loaded
   into memory, satisfying both the acceptance criteria ("CycloneDX documents are not
   loaded or processed") and the performance constraint (avoiding I/O for hundreds of
   thousands of irrelevant records).

2. **Reuse of `suppliers()` function**: The migration imports and calls the now-public
   `suppliers()` function from `trustify_module_ingestor::graph::sbom` rather than
   duplicating the extraction logic. The `migration/Cargo.toml` already declares a
   dependency on `trustify-module-ingestor`, so no new dependency is needed.

3. **Follows existing migration pattern**: The module structure mirrors `m0001_initial/mod.rs`
   with `MigrationTrait` implementation and `up()`/`down()` methods.

### 3. `migration/src/lib.rs` (registration)

**Change:** Register the new migration module in the migration registry.

- Add `mod m0042_backfill_suppliers;` to the module declarations
- Add `Box::new(m0042_backfill_suppliers::Migration)` to the migrations vec/list

---

## Database Query Strategy

The migration queries the database as follows:

```sql
-- Step 1: Get all SPDX SBOM IDs (filtered at the database level)
SELECT id FROM sbom WHERE labels->>'type' = 'spdx';

-- Step 2: For each SPDX SBOM, fetch its source document
SELECT * FROM source_document WHERE sbom_id = $1;

-- Step 3: After extracting suppliers, update the sbom_package records
UPDATE sbom_package SET supplier = $1 WHERE sbom_id = $2 AND package_id = $3;
```

The filtering is done in Step 1 at the SQL level using the `labels` JSONB column,
not in application code after loading all records.

---

## Tests

### Test 1: Migration populates supplier for SPDX SBOM

- Set up a test database with an SPDX SBOM record (`labels = {"type": "spdx"}`),
  a corresponding source document with SPDX content containing supplier fields,
  and associated `sbom_package` records with NULL supplier values.
- Run the migration `up()` method.
- Assert that the `sbom_package` records now have the correct supplier values
  extracted from the SPDX source data.
- Use value-based assertions on the actual supplier string, not just a non-NULL check.

### Test 2: Migration does not affect CycloneDX SBOMs

- Set up a test database with a CycloneDX SBOM record (`labels = {"type": "cyclonedx"}`)
  and associated `sbom_package` records.
- Run the migration `up()` method.
- Assert that the CycloneDX `sbom_package` records remain unchanged (supplier still NULL
  or whatever their original value was).
- Verify the source document for the CycloneDX SBOM was never fetched (this confirms
  the database-level filtering is working).

---

## Acceptance Criteria Verification

| Criterion | How Satisfied |
|-----------|---------------|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | The `up()` method queries all SPDX SBOMs via `labels->>'type' = 'spdx'`, fetches their source docs, extracts suppliers, and updates `sbom_package` records |
| CycloneDX documents are not loaded or processed | The SQL WHERE clause filters to SPDX only at the database level; CycloneDX records are never fetched |
| The `suppliers()` function in the ingestor is made public for reuse | Visibility changed from `fn` to `pub fn` in `modules/ingestor/src/graph/sbom/mod.rs` |
| The migration follows the existing migration pattern from `m0001_initial` | Module structure, `MigrationTrait` implementation, and `up()`/`down()` methods follow the same pattern |

---

## Self-Verification Notes

### Scope containment
- Only files listed in Files to Modify and Files to Create are touched, plus the
  necessary registration in `migration/src/lib.rs` (flagged as out-of-scope for user
  approval since the migration module must be registered but `lib.rs` is not listed
  in the task).

### Data-flow trace
- Input: SPDX SBOM records from the `sbom` table (filtered by labels)
- Processing: Source document fetch, SPDX parsing, supplier extraction via `suppliers()`
- Output: Updated `sbom_package` records with supplier field populated
- All stages connect; no incomplete paths.

### Contract & sibling parity
- The migration implements `MigrationTrait` matching the contract from SeaORM migration.
- Follows the same pattern as `m0001_initial/mod.rs` (sibling migration).
