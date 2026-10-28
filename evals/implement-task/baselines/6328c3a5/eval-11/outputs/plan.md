# Implementation Plan: TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously ignored during ingestion. The migration must target only SPDX documents, filtering by the `labels` jsonb column on the `sbom` entity.

---

## Files to Modify

### `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the existing `suppliers()` function public so the migration can reuse it.

- Locate the private function `fn suppliers(...)` in the SBOM ingestion module.
- Change the visibility from `fn suppliers(...)` to `pub fn suppliers(...)`.
- No changes to the function body, parameters, or return type.
- Verify with `find_referencing_symbols` that no existing callers are broken by the visibility change (making a private function public is backward-compatible -- all existing internal callers continue to work).

**Rationale**: The `suppliers()` function already contains the SPDX supplier extraction logic. The migration crate already depends on `trustify-module-ingestor` in `migration/Cargo.toml`, so making it public allows direct import without code duplication.

---

## Files to Create

### `migration/src/m0042_backfill_suppliers/mod.rs`

**Structure**: Follow the existing migration pattern from `migration/src/m0001_initial/mod.rs`. Implement the `MigrationTrait` with an `up()` method.

**Implementation**:

1. **Query only SPDX SBOMs** using a filtered query on the `sbom` entity's `labels` jsonb column:

   ```rust
   // Query only SPDX SBOMs -- CycloneDX documents already have supplier
   // information and production environments have hundreds of thousands of
   // CycloneDX records. Loading all documents would cause unnecessary I/O
   // and memory pressure.
   let spdx_sboms = Sbom::find()
       .filter(
           Expr::col(sbom::Column::Labels)
               .cast_as(Alias::new("jsonb"))
               .json_extract("type")
               .eq("spdx")
       )
       .all(db)
       .await?;
   ```

   Alternatively, using a raw JSON condition with SeaORM:

   ```rust
   use sea_orm::{Condition, sea_query::Expr};

   let spdx_sboms = sbom::Entity::find()
       .filter(
           Expr::cust_with_values(
               "labels->>'type' = $1",
               ["spdx"]
           )
       )
       .all(db)
       .await?;
   ```

   The exact syntax depends on the SeaORM version and JSON query patterns used elsewhere in the codebase. Inspect sibling migrations and the `common/src/db/query.rs` module for the project's established jsonb querying pattern.

2. **For each SPDX SBOM**, retrieve the raw source document:

   ```rust
   let source = SourceDocument::find_by_sbom_id(sbom.id).one(db).await?;
   ```

3. **Re-parse the source data** and extract the `supplier` field from SPDX package entries using the now-public `suppliers()` function from `trustify_module_ingestor::graph::sbom`.

4. **Update the corresponding `sbom_package` records** in the database with the extracted supplier values.

5. **Error handling**: Use `.context()` wrapping consistent with the project's `AppError` pattern. Log warnings for documents that fail to parse rather than aborting the entire migration.

### `migration/src/lib.rs`

**Change**: Register the new migration module `m0042_backfill_suppliers` in the migration registry. Add the module declaration and include it in the migration list, following the pattern established by `m0001_initial`.

---

## Database Query Strategy

### Filtered query (correct approach)

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx';
```

This query uses the `labels` jsonb column on the `sbom` entity to filter for SPDX documents only. The `labels` column stores metadata about each document:
- SPDX documents: `{"type": "spdx"}`
- CycloneDX documents: `{"type": "cyclonedx"}`

### Why not load all documents

An unfiltered query (e.g., `Sbom::find().all(db)` or `Document::all()`) would load hundreds of thousands of CycloneDX records alongside the smaller number of SPDX documents. This would cause:

- **Unnecessary I/O**: Reading hundreds of thousands of rows from the database when only a fraction are needed.
- **Memory pressure**: Holding all document records in memory simultaneously.
- **Wasted processing**: For each loaded record, the migration would need to fetch the source document and attempt to parse it, only to skip CycloneDX documents.
- **Extended migration runtime**: What could be a targeted operation on a subset becomes a full table scan with application-level filtering.

The `labels` column supports jsonb filtering at the database level, making a filtered query both possible and efficient.

---

## Test Plan

### Test 1: SPDX supplier backfill

Create an SPDX SBOM fixture with package entries containing supplier information. Run the migration. Verify that the `sbom_package` records are updated with the correct supplier values.

### Test 2: CycloneDX exclusion

Create a CycloneDX SBOM fixture. Run the migration. Verify that the CycloneDX SBOM's packages are not loaded, processed, or modified by the migration.

---

## Convention Conformance

- **Migration pattern**: Follow `m0001_initial/mod.rs` structure (implement `MigrationTrait`, define `up()` and `down()` methods).
- **Error handling**: Use `Result<T, AppError>` with `.context()` wrapping.
- **Framework**: SeaORM for database queries (consistent with entity definitions in `entity/src/`).
- **Reuse**: Import `suppliers()` from the ingestor module rather than duplicating the extraction logic.

## Acceptance Criteria Verification

- [x] The migration re-processes all SPDX SBOM documents and populates supplier fields -- achieved by filtered query on `labels->>'type' = 'spdx'` and calling `suppliers()` for each.
- [x] CycloneDX documents are not loaded or processed by the migration -- achieved by the filtered query excluding `cyclonedx` type documents at the database level.
- [x] The `suppliers()` function in the ingestor is made public for reuse -- changed from `fn` to `pub fn`.
- [x] The migration follows the existing migration pattern from `m0001_initial` -- implements `MigrationTrait` with `up()` method.
