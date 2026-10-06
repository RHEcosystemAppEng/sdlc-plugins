# Implementation Plan for TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information that was previously
ignored during ingestion. The migration must target only SPDX documents, leaving CycloneDX
documents untouched.

---

## Files to Modify

### `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public so the migration can reuse it.

- Locate the existing `fn suppliers(...)` function (currently private).
- Change the visibility from `fn suppliers(...)` to `pub fn suppliers(...)`.
- No logic changes to the function body -- only the visibility modifier changes.
- Before making this change, use `find_referencing_symbols` on `suppliers` to confirm
  that no existing callers depend on it being private and that the new public signature
  is safe.

**Rationale**: The migration crate already depends on `trustify-module-ingestor` in
`migration/Cargo.toml`, so making the function public allows direct import without
duplicating the extraction logic. This follows the "Reuse over duplication" principle
from the skill guidance.

---

## Files to Create

### `migration/src/m0042_backfill_suppliers/mod.rs`

**Structure**: Follow the existing migration pattern from `migration/src/m0001_initial/mod.rs`.
Implement `MigrationTrait` with an `up()` method.

**Database query for the migration**:

```rust
// Query ONLY SPDX SBOMs using the labels jsonb column as a filter.
// The sbom entity's labels column stores {"type": "spdx"} for SPDX documents
// and {"type": "cyclonedx"} for CycloneDX documents.
//
// CRITICAL: Do NOT use Sbom::find() or an unfiltered query like
// sbom::Entity::find().all(). Production environments have hundreds of
// thousands of CycloneDX documents. Loading all documents and filtering
// in application code would cause massive unnecessary I/O, memory
// consumption, and processing time.

let spdx_sboms = sbom::Entity::find()
    .filter(
        Expr::col(sbom::Column::Labels)
            .cast_as(Alias::new("jsonb"))
            .json_extract("$.type")
            .eq("spdx")
    )
    .all(&db)
    .await?;
```

Alternatively, using SeaORM's `Condition` with a raw JSON operator:

```rust
use sea_orm::{entity::*, query::*, sea_query::*};

let spdx_sboms = sbom::Entity::find()
    .filter(
        Expr::cust_with_values(
            "labels->>'type' = $1",
            ["spdx"]
        )
    )
    .all(&db)
    .await?;
```

**Migration `up()` method logic**:

1. Query all SPDX SBOM records using a filtered query on `labels->>'type' = 'spdx'`.
2. For each SPDX SBOM record:
   a. Fetch the raw source document using `SourceDocument::find_by_sbom_id(id)`.
   b. Parse the source document as SPDX format.
   c. Call the now-public `suppliers()` function from the ingestor module to extract
      supplier information from the parsed SPDX package entries.
   d. Update the corresponding `sbom_package` records in the database with the
      extracted supplier values.
3. Log progress (e.g., number of documents processed) for observability during
   long-running migrations.

**Error handling**: Follow the existing migration pattern -- use `Result<T, AppError>`
with `.context()` wrapping for meaningful error messages. If a single document fails
to parse, log the error and continue processing remaining documents (do not abort the
entire migration for one corrupt document).

### `migration/src/lib.rs`

**Change**: Register the new migration module. Add:

```rust
mod m0042_backfill_suppliers;
```

And add the migration to the migration list/registry following the pattern established
by existing migrations (e.g., `m0001_initial`).

---

## Files NOT Modified (Scope Containment)

The following files are explicitly out of scope per the task description:

- No API endpoint changes.
- No entity definition changes (the `sbom_package` table already has a supplier column).
- No changes to CycloneDX ingestion paths.

---

## Test Plan

### Test file: `migration/src/m0042_backfill_suppliers/mod.rs` (inline tests) or `tests/` directory

1. **Test: SPDX SBOM supplier backfill works correctly**
   - Set up a test database with an SPDX SBOM document (labels = `{"type": "spdx"}`).
   - Insert a source document with known SPDX package entries containing supplier fields.
   - Insert corresponding `sbom_package` records with empty/null supplier values.
   - Run the migration.
   - Assert that the `sbom_package` records now contain the correct supplier values
     extracted from the SPDX source data.

2. **Test: CycloneDX SBOMs are not affected**
   - Set up a test database with a CycloneDX SBOM document (labels = `{"type": "cyclonedx"}`).
   - Insert corresponding `sbom_package` records with existing supplier values.
   - Run the migration.
   - Assert that the CycloneDX `sbom_package` records are unchanged -- their supplier
     values must remain exactly as they were before the migration.
   - Verify (via query logging or mock) that no `SourceDocument::find_by_sbom_id` call
     was made for the CycloneDX document's ID.

---

## Acceptance Criteria Verification

| Criterion | How verified |
|-----------|-------------|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | Test 1: assert supplier values populated after migration |
| CycloneDX documents are not loaded or processed | Filtered query (`labels->>'type' = 'spdx'`) excludes them at the database level; Test 2 confirms no side effects |
| The `suppliers()` function is made public | Code change: `fn` -> `pub fn`; compilation confirms visibility |
| Migration follows existing pattern from `m0001_initial` | Implements `MigrationTrait` with `up()` method |
