# Implementation Plan for TC-9209

## Task Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously
ignored during ingestion. The migration iterates over SPDX SBOM documents only, re-parses
their source data, extracts the `supplier` field from SPDX package entries, and updates
corresponding `sbom_package` records with supplier values.

## Project Configuration Validation (Step 0)

The mock CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID present
- Code Intelligence: tool naming convention documented (`mcp__serena_backend__<tool>`)

Configuration is valid. Proceed.

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public.

- Current: `fn suppliers(...)` (private function)
- Changed: `pub fn suppliers(...)` (public function)

This is a visibility-only change. The function signature, parameters, and return type
remain identical. The migration crate already depends on `trustify-module-ingestor` in
`migration/Cargo.toml`, so no dependency changes are needed.

**Backward compatibility**: Use `find_referencing_symbols` (or Grep) to verify all
existing callers of `suppliers()` within the ingestor module are unaffected by the
visibility change. Making a private function public is additive and does not break
existing callers.

## Files to Create

### 2. `migration/src/m0042_backfill_suppliers/mod.rs`

**Pattern**: Follow the existing migration pattern from `migration/src/m0001_initial/mod.rs`.
Implement `MigrationTrait` with an `up()` method.

**Implementation**:

```rust
use sea_orm_migration::prelude::*;
use sea_orm::{EntityTrait, QueryFilter, ColumnTrait, ActiveModelTrait, Set};
use trustify_entity::sbom;
use trustify_module_ingestor::graph::sbom::suppliers;

/// Data migration that re-processes all SPDX SBOM documents to extract and
/// backfill package supplier information into sbom_package records.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // Query ONLY SPDX SBOMs using the labels jsonb column filter.
        // CycloneDX documents already have supplier info and are excluded
        // to avoid unnecessary I/O (hundreds of thousands of records).
        let spdx_sboms = sbom::Entity::find()
            .filter(Expr::cust("labels->>'type' = 'spdx'"))
            .all(db)
            .await?;

        for sbom_record in spdx_sboms {
            // Fetch the raw source document for this SBOM
            let source_doc = SourceDocument::find_by_sbom_id(sbom_record.id)
                .one(db)
                .await?;

            let Some(source_doc) = source_doc else {
                // Skip SBOMs with no source document (defensive guard)
                continue;
            };

            // Re-parse the SPDX document and extract supplier information
            // using the now-public suppliers() function from the ingestor
            let supplier_data = suppliers(&source_doc.data);

            // Update each sbom_package record with the extracted supplier
            for (package_ref, supplier_value) in supplier_data {
                // Find the sbom_package by sbom_id and package reference,
                // then update the supplier field
                // ... (update logic using SeaORM ActiveModel pattern)
            }
        }

        Ok(())
    }
}
```

### 3. `migration/src/lib.rs` (modification)

Register the new migration module in the migration library's module list and migration
registry. Add:

```rust
mod m0042_backfill_suppliers;
```

and add `m0042_backfill_suppliers::Migration` to the migration list returned by the
`Migrator` struct.

**Note**: This file is not listed in "Files to Modify" in the task description. Per the
skill's scope containment rules (Step 9), this would be flagged as an out-of-scope file
requiring user approval. However, it is necessary for the migration to be discoverable
by the migration runner. The user should be asked to approve this change.

## Database Query for the Migration

### Filtered query (required)

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx';
```

SeaORM equivalent:

```rust
sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(db)
    .await?
```

This query uses the `labels` jsonb column on the `sbom` entity to select only SPDX
documents. The `labels` column stores `{"type": "spdx"}` for SPDX documents and
`{"type": "cyclonedx"}` for CycloneDX documents, as documented in the task's
Implementation Notes.

### Why not an unfiltered query

An unfiltered query (`sbom::Entity::find().all(db)`) would load all SBOM records
including hundreds of thousands of CycloneDX documents that do not need processing.
This would cause:

- Unnecessary database I/O loading records that will be skipped
- Unnecessary memory consumption holding CycloneDX records
- Unnecessary source document fetches for documents that already have supplier data
- Significantly longer migration runtime in production environments

The filtered query avoids all of this by selecting only the SPDX subset at the
database level.

## Tests

### Test file location

Tests would be added within `migration/src/m0042_backfill_suppliers/mod.rs` (as a
`#[cfg(test)]` module) or in a dedicated test file depending on the project's test
conventions observed in `m0001_initial`.

### Test 1: SPDX SBOM supplier backfill

```rust
/// Verifies that the migration extracts and populates supplier information
/// from an SPDX SBOM document's package entries.
#[tokio::test]
async fn test_migration_populates_spdx_suppliers() {
    // Given an SPDX SBOM with packages containing supplier fields
    // ... (set up test DB with an SPDX SBOM record, source document, and
    //      sbom_package records with empty supplier fields)

    // When the migration runs
    // ... (execute Migration::up)

    // Then the sbom_package records should have supplier values populated
    // ... (assert_eq on specific supplier values, not just non-null checks)
}
```

### Test 2: CycloneDX SBOMs unaffected

```rust
/// Verifies that CycloneDX SBOM documents are not loaded or processed
/// by the migration, preserving their existing supplier data.
#[tokio::test]
async fn test_migration_skips_cyclonedx_sboms() {
    // Given a CycloneDX SBOM with existing supplier data
    // ... (set up test DB with a CycloneDX SBOM record with
    //      labels = {"type": "cyclonedx"} and pre-populated supplier fields)

    // When the migration runs
    // ... (execute Migration::up)

    // Then the CycloneDX sbom_package records should be unchanged
    // ... (assert_eq on original supplier values to verify no modification)
}
```

## Acceptance Criteria Verification

| Criterion | How verified |
|-----------|-------------|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | Test 1 + filtered query targeting `labels->>'type' = 'spdx'` |
| CycloneDX documents are not loaded or processed | Test 2 + filtered query excludes CycloneDX by design |
| `suppliers()` function made public for reuse | Visibility change from `fn` to `pub fn` in `mod.rs` |
| Migration follows existing pattern from `m0001_initial` | Implements `MigrationTrait` with `up()` method per convention |

## Self-Verification Checklist

- [ ] Scope containment: flag `migration/src/lib.rs` as out-of-scope (required but not listed)
- [ ] Query-scope verification: filtered query using `labels->>'type' = 'spdx'` (see query-scope.md)
- [ ] Dead parameter detection: no parameters removed, not applicable
- [ ] Sensitive-pattern check: no secrets or credentials in migration code
- [ ] Duplication check: reuses existing `suppliers()` function rather than duplicating logic
- [ ] Data-flow trace: source_document -> re-parse -> extract supplier -> update sbom_package
- [ ] Contract & sibling parity: migration implements `MigrationTrait` per `m0001_initial` pattern
