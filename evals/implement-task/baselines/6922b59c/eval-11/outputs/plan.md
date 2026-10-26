# Implementation Plan -- TC-9209

**Task**: Re-process all SPDX SBOMs to extract package supplier information

## Overview

This task creates a data migration that iterates over SPDX SBOM documents (only), re-parses
their source data, extracts the `supplier` field from SPDX package entries, and updates the
corresponding `sbom_package` records with the extracted supplier values. CycloneDX documents
are excluded entirely -- they already have supplier information populated.

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public.

The `suppliers()` function currently contains the SPDX supplier extraction logic and is
declared as `fn suppliers(...)` (private). Change the visibility to `pub fn suppliers(...)`
so the migration crate can import and reuse it.

This is a single-line change:

```rust
// Before
fn suppliers(...) -> ... {

// After
pub fn suppliers(...) -> ... {
```

**Rationale**: The migration crate already depends on `trustify-module-ingestor` in
`migration/Cargo.toml`, so making the function public is sufficient -- no new dependency
is needed. This follows the "reuse over duplication" principle: the function already
exists and does exactly what the migration needs.

**Backward compatibility**: Changing visibility from private to public is a non-breaking
change. Use `find_referencing_symbols` (or Grep) to confirm no existing callers are
affected by the signature remaining unchanged.

### 2. `migration/src/lib.rs`

**Change**: Register the new migration module.

Add a `mod m0042_backfill_suppliers;` declaration and include it in the migration list
(following the pattern established by `m0001_initial` and other existing migrations).

## Files to Create

### 1. `migration/src/m0042_backfill_suppliers/mod.rs`

**Purpose**: Data migration that re-processes SPDX SBOMs to backfill supplier information.

**Structure** (following the pattern from `m0001_initial/mod.rs`):

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

        // Query ONLY SPDX SBOMs using a filtered query on the labels JSONB column.
        // CycloneDX documents (hundreds of thousands in production) are excluded
        // at the database level to avoid unnecessary I/O.
        let spdx_sboms = Sbom::find()
            .filter(sbom::Column::Labels.contains(json!({"type": "spdx"})))
            .all(db)
            .await?;

        for sbom in spdx_sboms {
            // Fetch the raw source document for this SBOM
            let source = SourceDocument::find_by_sbom_id(sbom.id)
                .one(db)
                .await?;

            if let Some(source_doc) = source {
                // Re-parse the SPDX document and extract supplier information
                // using the now-public suppliers() function from the ingestor module
                let supplier_data = suppliers(&source_doc.data);

                // Update sbom_package records with extracted supplier values
                for (package_ref, supplier_value) in supplier_data {
                    SbomPackage::update_many()
                        .filter(sbom_package::Column::SbomId.eq(sbom.id))
                        .filter(sbom_package::Column::PackageRef.eq(package_ref))
                        .col_expr(sbom_package::Column::Supplier, Expr::value(supplier_value))
                        .exec(db)
                        .await?;
                }
            }
        }

        Ok(())
    }
}
```

**Key design decisions**:

1. **Filtered database query**: The migration uses `labels.contains(json!({"type": "spdx"}))`
   to filter at the database level. This is critical because production has hundreds of
   thousands of CycloneDX documents alongside a smaller number of SPDX documents. An
   unfiltered query (`Sbom::find().all(db)`) would load all records unnecessarily, wasting
   I/O, memory, and time. See `outputs/query-scope.md` for the full analysis.

2. **Reuse of `suppliers()` function**: Rather than duplicating the SPDX supplier extraction
   logic, the migration imports the now-public `suppliers()` function from
   `trustify_module_ingestor::graph::sbom`. This ensures consistency with the ingestion
   pipeline and avoids code duplication.

3. **Source document retrieval**: Uses `SourceDocument::find_by_sbom_id(id)` to fetch the
   raw SPDX document bytes for re-parsing, as documented in the Implementation Notes.

4. **Per-record updates**: Updates `sbom_package` records individually per SBOM, matching
   packages by their reference within the SBOM context.

## Database Query Strategy

**Query used**:
```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx'
```

**Rejected alternative**:
```sql
SELECT * FROM sbom  -- loads ALL documents, including hundreds of thousands of CycloneDX
```

The filtered query is used because:
- The task explicitly targets only SPDX SBOMs
- The `labels` JSONB column supports filtering by document type
- Production has hundreds of thousands of CycloneDX documents that would be loaded and
  immediately discarded
- The acceptance criteria require that "CycloneDX documents are not loaded or processed"

## Test Plan

### Test 1: SPDX supplier backfill

**File**: Test within the migration module or in `tests/` following project conventions.

**What it verifies**: The migration correctly extracts and populates supplier information
from an SPDX SBOM document.

**Approach**:
1. Insert a test SBOM record with `labels = {"type": "spdx"}` and a corresponding
   source document containing SPDX package entries with `supplier` fields
2. Insert `sbom_package` records with empty/null supplier values
3. Run the migration
4. Assert that the `sbom_package` records now have the correct supplier values
   (value-based assertions, not just non-null checks)

### Test 2: CycloneDX exclusion

**File**: Same test module as Test 1.

**What it verifies**: CycloneDX SBOM documents are not loaded or processed by the migration.

**Approach**:
1. Insert a test SBOM record with `labels = {"type": "cyclonedx"}` and a corresponding
   source document
2. Insert `sbom_package` records with existing supplier values
3. Run the migration
4. Assert that the CycloneDX `sbom_package` records remain unchanged (supplier values
   are identical to pre-migration state)

## Acceptance Criteria Verification

| Criterion | How satisfied |
|-----------|---------------|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | Filtered query loads all SPDX SBOMs; `suppliers()` extracts data; `sbom_package` records updated |
| CycloneDX documents are not loaded or processed | Database-level filter `labels->>'type' = 'spdx'` excludes CycloneDX at the query layer |
| `suppliers()` function in the ingestor is made public | Visibility changed from `fn` to `pub fn` |
| Migration follows existing pattern from `m0001_initial` | Implements `MigrationTrait` with `up()` method, same module structure |

## Data-Flow Trace

1. **Input**: Database query filtered to SPDX SBOMs via `labels->>'type' = 'spdx'`
2. **Source retrieval**: `SourceDocument::find_by_sbom_id(id)` fetches raw SPDX bytes
3. **Processing**: `suppliers()` function parses SPDX data and extracts supplier fields
4. **Output**: `sbom_package` records updated with extracted supplier values via
   `SbomPackage::update_many()`

All stages connect -- data flows from filtered query through source retrieval, parsing,
and back to database update. No disconnected stages.

## Scope Containment

Files in scope:
- `modules/ingestor/src/graph/sbom/mod.rs` (modify -- listed in Files to Modify)
- `migration/src/m0042_backfill_suppliers/mod.rs` (create -- listed in Files to Create)
- `migration/src/lib.rs` (modify -- required for module registration, would flag as
  out-of-scope for user approval in Step 9)

No other files are modified. The `migration/Cargo.toml` already depends on
`trustify-module-ingestor`, so no dependency changes are needed.
