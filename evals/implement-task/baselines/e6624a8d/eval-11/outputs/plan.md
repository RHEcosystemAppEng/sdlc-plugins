# Implementation Plan: TC-9209

## Task Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously
ignored during ingestion. Create a data migration that iterates over SPDX SBOM documents,
re-parses the source data, extracts the `supplier` field from SPDX package entries, and
updates corresponding `sbom_package` records.

## Repository

trustify-backend (Serena instance: serena_backend)

## Target Branch

main

## Files to Modify

### `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public.

- Current signature: `fn suppliers(...)` (private)
- New signature: `pub fn suppliers(...)` (public)
- Rationale: The migration crate already depends on `trustify-module-ingestor` in
  `migration/Cargo.toml`, so no new dependency is needed. Making the function public
  allows the migration to reuse the existing SPDX supplier extraction logic rather
  than duplicating it (DRY principle, per Step 6 "Reuse over duplication" guidance).
- Add a documentation comment (`///`) explaining what the function does, since it is
  now part of the public API.

## Files to Create

### `migration/src/m0042_backfill_suppliers/mod.rs`

**Structure**: Follow the existing migration pattern from `migration/src/m0001_initial/mod.rs`.

The migration module implements `MigrationTrait` with an `up()` method containing the
following logic:

1. **Query SPDX SBOMs only**: Query the `sbom` table filtering by
   `labels->>'type' = 'spdx'` to select only SPDX documents. This is critical because
   production has hundreds of thousands of CycloneDX documents that already have supplier
   data and should not be loaded.

2. **Iterate over each SPDX SBOM**: For each SPDX SBOM record returned:
   a. Fetch the raw source document using `SourceDocument::find_by_sbom_id(id)` from
      the `source_document` table.
   b. Parse the raw document bytes as an SPDX document.
   c. Call the now-public `suppliers()` function from
      `trustify_module_ingestor::graph::sbom` to extract supplier information from
      the parsed SPDX package entries.
   d. Update the corresponding `sbom_package` records in the database with the
      extracted supplier values.

3. **Error handling**: Follow the error handling conventions from the existing migration
   pattern. Use `Result<T, AppError>` with `.context()` wrapping as per repository
   conventions.

### Registration in `migration/src/lib.rs`

The new migration module `m0042_backfill_suppliers` must be registered in
`migration/src/lib.rs` so it is discovered and executed by the migration runner.
This typically involves:
- Adding a `mod m0042_backfill_suppliers;` declaration
- Adding the migration to the ordered migration list/vector

## Database Query Strategy

### Primary query (SPDX SBOM selection)

```sql
SELECT id, labels FROM sbom WHERE labels->>'type' = 'spdx';
```

This query uses the `labels` JSONB column on the `sbom` entity to filter for SPDX
documents only. The `labels` column stores `{"type": "spdx"}` for SPDX documents
and `{"type": "cyclonedx"}` for CycloneDX documents.

**Why filtered query**: The task explicitly states "Only SPDX SBOMs need re-processing"
and production has hundreds of thousands of CycloneDX documents. Using an unfiltered
query (e.g., `Sbom::find()` / `SELECT * FROM sbom`) would load all documents and
require application-level filtering, causing unnecessary I/O and memory pressure.
The `labels->>'type'` filter pushes the subset restriction to the database level.

### Source document retrieval (per SBOM)

```
SourceDocument::find_by_sbom_id(sbom_id)
```

Fetches the raw SPDX document bytes for re-parsing. This is called once per SPDX
SBOM record, not in bulk, to avoid loading all source documents into memory at once.

### Supplier update (per SBOM package)

For each SPDX package with an extracted supplier value, update the corresponding
`sbom_package` record:

```sql
UPDATE sbom_package SET supplier = <extracted_value> WHERE sbom_id = <id> AND package_id = <pkg_id>;
```

Using the SeaORM equivalent update operation following existing patterns.

## Convention Conformance

Based on the repository conventions documented in repo-backend.md:

- **Framework**: SeaORM for database operations
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Migration pattern**: Follow `m0001_initial/mod.rs` structure with `MigrationTrait`
  and `up()` method
- **Testing**: Integration tests hit a real PostgreSQL test database

## Test Plan

### Test 1: SPDX supplier backfill

- Create a test SPDX SBOM with known supplier data in source document but empty
  supplier fields in `sbom_package` records
- Run the migration
- Assert that `sbom_package` records now have the correct supplier values
- Use value-based assertions (check actual supplier strings, not just non-null)

### Test 2: CycloneDX documents unaffected

- Create a CycloneDX SBOM with existing supplier data in `sbom_package` records
- Run the migration
- Assert that CycloneDX `sbom_package` records remain unchanged
- This verifies the query filter correctly excludes CycloneDX documents

Both tests should include `///` documentation comments and given-when-then section
comments as per the skill's test guidance.

## Acceptance Criteria Verification

1. Migration re-processes all SPDX SBOM documents and populates supplier fields --
   achieved by querying `sbom WHERE labels->>'type' = 'spdx'` and updating
   `sbom_package` with extracted suppliers
2. CycloneDX documents are not loaded or processed -- achieved by the filtered query
   excluding `{"type": "cyclonedx"}` records
3. The `suppliers()` function is made public for reuse -- achieved by changing
   `fn suppliers` to `pub fn suppliers` in `modules/ingestor/src/graph/sbom/mod.rs`
4. The migration follows the existing migration pattern -- achieved by implementing
   `MigrationTrait` following `m0001_initial/mod.rs`

## Data-Flow Trace

`sbom` table (filtered query) -> `source_document` table (raw bytes) ->
SPDX parser (re-parse) -> `suppliers()` function (extract) ->
`sbom_package` table (update) -- **COMPLETE**

All stages are connected: input (filtered SBOM query), processing (document
retrieval, parsing, supplier extraction), and output (database update).
