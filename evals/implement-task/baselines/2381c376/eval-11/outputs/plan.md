# Implementation Plan for TC-9209

## Task Summary

**TC-9209**: Re-process all SPDX SBOMs to extract package supplier information.

Create a data migration that iterates over SPDX SBOM documents only, re-parses their source data, extracts the `supplier` field from SPDX package entries, and updates the corresponding `sbom_package` records with the extracted supplier values. CycloneDX documents already have supplier information and must not be loaded or processed.

---

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public.

The `suppliers()` function currently has private visibility (`fn suppliers(...)`). Change its visibility to `pub fn suppliers(...)` so the migration crate can import and reuse it. The migration crate (`migration/`) already depends on `trustify-module-ingestor` in `migration/Cargo.toml`, so no new dependency is needed.

This is a minimal, non-breaking change -- making a private function public adds no risk to existing callers since there are none outside the module today.

**Backward compatibility**: Use `find_referencing_symbols` (or Grep) to confirm no external callers exist before the change. Since the function is currently private, promoting it to `pub` cannot break existing code.

---

## Files to Create

### 2. `migration/src/m0042_backfill_suppliers/mod.rs`

**Change**: Create a new data migration module that backfills supplier information for SPDX SBOMs.

#### Migration structure

Follow the existing pattern from `migration/src/m0001_initial/mod.rs`:
- Implement `MigrationTrait` with an `up()` method (and a no-op `down()`).
- Register the migration in `migration/src/lib.rs`.

#### Database query -- filtered to SPDX only

The migration MUST query only SPDX documents using a filtered query on the `labels` JSONB column:

```sql
SELECT id FROM sbom WHERE labels->>'type' = 'spdx'
```

Or the SeaORM equivalent:

```rust
use sea_orm::{entity::prelude::*, Condition, JsonValue};

Sbom::find()
    .filter(
        Expr::cust_with_values(
            "labels->>'type' = $1",
            ["spdx"]
        )
    )
    .all(db)
    .await?
```

**This filtered query is critical.** The task description explicitly states "Only SPDX SBOMs need re-processing" and the acceptance criteria require that "CycloneDX documents are not loaded or processed by the migration." Loading all documents indiscriminately (e.g., `Sbom::find().all(db)` or `Document::all()`) and then filtering in application code would be a serious performance problem: production environments have hundreds of thousands of CycloneDX records alongside a smaller number of SPDX documents. Loading all records would cause unnecessary I/O, excessive memory consumption, and prolonged migration runtime -- all to discard the vast majority of loaded records. The `labels->>'type'` column supports filtering at the database level, so the subset restriction must be expressed in the query itself.

#### Processing logic

For each SPDX SBOM returned by the filtered query:

1. Fetch the raw source document using `SourceDocument::find_by_sbom_id(sbom_id)`.
2. Parse the source document bytes as SPDX.
3. Call the now-public `suppliers()` function from `trustify_module_ingestor::graph::sbom` to extract supplier information from the parsed SPDX packages.
4. Update each corresponding `sbom_package` record in the database with the extracted supplier value.
5. Use batch updates or transactions to maintain data consistency and avoid partial writes.

#### Error handling

- Follow the `Result<T, AppError>` pattern with `.context()` wrapping.
- If a single document fails to parse, log the error and continue processing the remaining documents (do not abort the entire migration for one malformed document).

#### Documentation

- Add a doc comment on the migration struct explaining what it does and why only SPDX documents are targeted.

### 3. Registration in `migration/src/lib.rs`

**Change**: Add `mod m0042_backfill_suppliers;` and register the new migration in the migration list so it runs as part of the migration sequence.

---

## Test Plan

Tests would be added within the migration module or in the `tests/` directory, depending on the project's test conventions.

### Test 1: SPDX SBOM supplier backfill

Verify the migration populates supplier information for an SPDX SBOM.

- **Given**: An SPDX SBOM record exists in the database with `labels = '{"type": "spdx"}'` and its `sbom_package` records have empty supplier fields. A corresponding `source_document` with valid SPDX content containing supplier information exists.
- **When**: The migration `up()` method runs.
- **Then**: The `sbom_package` records for that SBOM have their supplier fields populated with the values from the SPDX source data.

### Test 2: CycloneDX SBOMs are not affected

Verify CycloneDX documents are not loaded or processed.

- **Given**: A CycloneDX SBOM record exists with `labels = '{"type": "cyclonedx"}'` and its `sbom_package` records have supplier fields already populated.
- **When**: The migration `up()` method runs.
- **Then**: The CycloneDX `sbom_package` records remain unchanged. The migration query does not load the CycloneDX document or its source data (verifiable by checking that `SourceDocument::find_by_sbom_id` is never called for the CycloneDX SBOM's ID).

---

## Acceptance Criteria Verification

| Criterion | How satisfied |
|-----------|--------------|
| Migration re-processes all SPDX SBOM documents and populates supplier fields | The filtered query selects all SPDX SBOMs; each is re-parsed and updated |
| CycloneDX documents are not loaded or processed | The `WHERE labels->>'type' = 'spdx'` filter excludes CycloneDX at the database level |
| The `suppliers()` function in the ingestor is made public for reuse | Visibility changed from `fn` to `pub fn` |
| The migration follows the existing migration pattern from `m0001_initial` | Implements `MigrationTrait` with `up()` method, registered in `lib.rs` |

---

## Data-Flow Trace

1. **Input**: Database query fetches SPDX SBOM IDs from `sbom` table (filtered by `labels->>'type' = 'spdx'`).
2. **Processing**: For each SBOM ID, fetch raw bytes from `source_document` table, parse as SPDX, extract suppliers via the `suppliers()` function.
3. **Output**: Update `sbom_package` records with extracted supplier values.

All stages are connected. No external API calls or file system operations are involved beyond the database.

---

## Scope Containment

Files within scope:
- `modules/ingestor/src/graph/sbom/mod.rs` (modify -- make `suppliers()` public)
- `migration/src/m0042_backfill_suppliers/mod.rs` (create -- new migration)
- `migration/src/lib.rs` (modify -- register the new migration module)

The `migration/src/lib.rs` modification is an expected side-effect of creating a new migration module (it must be registered). This is standard practice per the migration pattern.
