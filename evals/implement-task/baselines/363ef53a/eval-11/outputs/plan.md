# Implementation Plan: TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously ignored during ingestion. This requires making an existing private function public for reuse and creating a new data migration that iterates only over SPDX documents using a filtered database query.

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change:** Make the `suppliers()` function public.

**Current state:** The function is declared as `fn suppliers(...)` (private).

**Planned change:** Change the visibility to `pub fn suppliers(...)`.

**Rationale:** The migration crate (`migration/`) already depends on `trustify-module-ingestor` in its `Cargo.toml`. By making the function public, the migration can import and call it directly, reusing the existing SPDX supplier extraction logic rather than duplicating it. This follows the "Reuse over duplication" principle -- the dependency relationship already exists, so exporting the function is the correct approach.

**Backward compatibility:** Use `find_referencing_symbols` (or Grep) to verify that no existing callers are affected by the visibility change. Making a private function public is a non-breaking change -- all existing internal call sites continue to work.

## Files to Create

### 2. `migration/src/m0042_backfill_suppliers/mod.rs`

**Purpose:** A data migration that re-processes SPDX SBOMs to extract and persist supplier information for each package.

**Structure:** Follow the existing migration pattern from `migration/src/m0001_initial/mod.rs`. Implement the `MigrationTrait` with an `up()` method.

**Database query -- filtered, not unfiltered:**

The migration MUST query only SPDX documents using a filtered query on the `sbom` entity's `labels` jsonb column:

```rust
// Correct: filtered query targeting only SPDX documents
let spdx_sboms = Sbom::find()
    .filter(
        Expr::cust("labels->>'type' = 'spdx'")
    )
    .all(db)
    .await?;
```

**The migration MUST NOT use an unfiltered query such as:**

```rust
// WRONG: loads all documents including hundreds of thousands of CycloneDX records
let all_sboms = Sbom::find().all(db).await?;
for sbom in all_sboms {
    if sbom.labels["type"] == "spdx" {
        // process
    }
    // else skip -- but we already loaded and deserialized the row for nothing
}
```

Production environments have hundreds of thousands of CycloneDX documents that do not need re-processing. Loading them all into memory to filter in application code would cause severe performance degradation: excessive database I/O, high memory consumption, and unnecessarily long migration runtime. The `labels` jsonb column supports database-level filtering (`labels->>'type' = 'spdx'`), so the filtering must be pushed down to PostgreSQL.

**Processing logic for each SPDX SBOM:**

1. For each SPDX SBOM returned by the filtered query, fetch the source document using `SourceDocument::find_by_sbom_id(sbom.id)`.
2. Parse the raw SPDX document bytes to extract package entries.
3. Call the now-public `suppliers()` function (imported from `trustify_module_ingestor::graph::sbom`) to extract the `supplier` field from each SPDX package entry.
4. Update the corresponding `sbom_package` records in the database with the extracted supplier values.

**Batch processing considerations:**

- Process documents in batches (e.g., 100 at a time) to limit memory usage.
- Use transactions per batch so that partial progress is preserved on failure.
- Log progress (e.g., number of documents processed) for observability during long-running migrations.

**Error handling:**

- If a source document cannot be fetched or parsed, log a warning with the SBOM ID and continue to the next document. Do not abort the entire migration for a single corrupt record.
- Use `.context()` wrapping consistent with the project's error handling conventions.

### 3. Module registration

Register the new migration module in `migration/src/lib.rs` so it is discovered and executed by the migration runner. Add the module declaration and include it in the migration list, following the pattern established by `m0001_initial`.

## Tests

### Test file location

Add tests alongside the migration or in the existing test infrastructure, following the project's test conventions.

### Test 1: SPDX supplier backfill

Verify that the migration correctly extracts and populates supplier information for an SPDX SBOM document.

- **Given:** An SPDX SBOM with `labels = {"type": "spdx"}` and associated `sbom_package` records with empty supplier fields, plus a source document containing SPDX package entries with supplier data.
- **When:** The migration `up()` method runs.
- **Then:** The `sbom_package` records are updated with the extracted supplier values. Assert on the specific supplier values, not just that they are non-null.

### Test 2: CycloneDX documents unaffected

Verify that CycloneDX SBOM documents are not loaded or processed by the migration.

- **Given:** A CycloneDX SBOM with `labels = {"type": "cyclonedx"}` and associated `sbom_package` records with existing supplier fields.
- **When:** The migration `up()` method runs.
- **Then:** The CycloneDX `sbom_package` records remain unchanged. The migration query should not have loaded this document at all (verify via query count or absence of processing logs for this document).

## Acceptance Criteria Verification

| Criterion | How verified |
|-----------|-------------|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | Test 1 confirms supplier extraction and persistence for SPDX documents |
| CycloneDX documents are not loaded or processed | Filtered query (`labels->>'type' = 'spdx'`) excludes them at the database level; Test 2 confirms no side effects |
| The `suppliers()` function is made public for reuse | Visibility change from `fn` to `pub fn` in `mod.rs` |
| Migration follows existing migration pattern from `m0001_initial` | Implements `MigrationTrait` with `up()`, same module structure |

## Query-Scope Summary

See `query-scope.md` for the full analysis. In brief: the task targets SPDX SBOMs only (a subset), the `labels` jsonb column supports database-level filtering by document type, and the implementation uses a filtered query (`labels->>'type' = 'spdx'`) to avoid loading hundreds of thousands of non-target CycloneDX records.
