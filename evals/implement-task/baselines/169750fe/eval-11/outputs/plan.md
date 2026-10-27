# Implementation Plan: TC-9209

## Summary

Re-process all SPDX SBOMs to extract package supplier information by creating a data migration and making the existing `suppliers()` helper public for reuse.

## Step 0 — Validate Project Configuration

Verified CLAUDE.md contains:
- **Repository Registry**: trustify-backend with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: Serena with rust-analyzer

All required sections present — proceeding.

## Step 1 — Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Create a data migration that re-processes all SPDX SBOMs to extract package supplier information. Only SPDX SBOMs need re-processing — CycloneDX documents already have supplier information populated during ingestion.
- **Files to Modify**: `modules/ingestor/src/graph/sbom/mod.rs`
- **Files to Create**: `migration/src/m0042_backfill_suppliers/mod.rs`
- **API Changes**: None
- **Dependencies**: None
- **Bookend Type**: Not present
- **Target PR**: Not present

## Step 4 — Understand the Code

### Code inspection

Before modifying any files, inspect the following:

1. **`modules/ingestor/src/graph/sbom/mod.rs`** — use `get_symbols_overview` to understand the module structure, then `find_symbol` with `include_body=true` on the `suppliers()` function to read its implementation. Confirm it is currently `fn suppliers(...)` (private) and understand its signature, parameters, and return type.

2. **`migration/src/m0001_initial/mod.rs`** — read this file to understand the existing migration pattern. Identify the `MigrationTrait` implementation, the `up()` method structure, and how database operations are performed within migrations.

3. **`entity/src/sbom.rs`** — use `get_symbols_overview` to inspect the SBOM entity definition. Verify the `labels` column exists and is of type `jsonb`. Confirm that SPDX documents store `{"type": "spdx"}` in labels.

4. **`migration/src/lib.rs`** — read to understand how migrations are registered and discover the module registration pattern.

5. **`migration/Cargo.toml`** — verify that `trustify-module-ingestor` is already listed as a dependency, confirming that the migration crate can import from the ingestor without adding a new dependency.

### Convention conformance analysis

Examine sibling migrations (e.g., `m0001_initial/mod.rs`) for:
- **Naming**: Migration modules use `m<NNNN>_<description>/mod.rs` pattern
- **Structure**: Each migration implements `MigrationTrait` with `up()` and `down()` methods
- **Error handling**: Migrations use `Result<(), DbErr>` return types with `?` operator
- **Database access**: Migrations use SeaORM's `DatabaseConnection` for queries

### Documentation files identified

- `docs/api.md` — no API changes, no update needed
- `docs/architecture.md` — no structural changes, no update needed
- `CONVENTIONS.md` — will check for CI verification commands

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9209
```

## Step 6 — Implement Changes

### File 1: Modify `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the `suppliers()` function public by changing `fn suppliers(...)` to `pub fn suppliers(...)`.

This is a minimal change — only the visibility modifier is added. The function signature, parameters, body, and return type remain unchanged. This allows the migration crate to import and reuse the existing supplier extraction logic rather than duplicating it.

### File 2: Create `migration/src/m0042_backfill_suppliers/mod.rs`

**Change**: Create a new migration module that:

1. **Queries only SPDX SBOMs using a filtered database query**:
   ```rust
   // Query only SPDX documents using the labels jsonb column
   let spdx_sboms = sbom::Entity::find()
       .filter(Expr::cust("labels->>'type' = 'spdx'"))
       .all(&db)
       .await?;
   ```
   This filters at the database level using `labels->>'type' = 'spdx'` on the `sbom` entity's `labels` jsonb column. This is critical because production environments have hundreds of thousands of CycloneDX documents — loading all documents indiscriminately and filtering in application code would cause excessive, unnecessary I/O and memory consumption. The database index on the jsonb column enables efficient filtering.

2. **For each SPDX SBOM**:
   - Fetch the source document using `SourceDocument::find_by_sbom_id(id)`
   - Parse the SPDX document to extract package entries
   - Call the now-public `suppliers()` function from `trustify_module_ingestor::graph::sbom` to extract supplier information
   - Update the corresponding `sbom_package` records with the extracted supplier values

3. **Implements `MigrationTrait`** following the pattern from `m0001_initial/mod.rs`:
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
           
           // Query only SPDX SBOMs — CycloneDX already has supplier data
           let spdx_sboms = sbom::Entity::find()
               .filter(Expr::cust("labels->>'type' = 'spdx'"))
               .all(db)
               .await?;
           
           for sbom in spdx_sboms {
               let source = SourceDocument::find_by_sbom_id(sbom.id)
                   .one(db)
                   .await?;
               
               if let Some(doc) = source {
                   let parsed = parse_spdx(&doc.data)?;
                   let supplier_map = suppliers(&parsed);
                   
                   for (pkg_id, supplier) in supplier_map {
                       sbom_package::Entity::update_many()
                           .filter(sbom_package::Column::SbomId.eq(sbom.id))
                           .filter(sbom_package::Column::PackageId.eq(pkg_id))
                           .set(sbom_package::ActiveModel {
                               supplier: Set(Some(supplier)),
                               ..Default::default()
                           })
                           .exec(db)
                           .await?;
                   }
               }
           }
           
           Ok(())
       }
   }
   ```

### File 3: Register migration in `migration/src/lib.rs`

Add `mod m0042_backfill_suppliers;` and register the migration in the migration list. Note: `migration/src/lib.rs` is not listed in Files to Modify — this would be flagged as an out-of-scope change in Step 9's scope containment check, requiring user approval before proceeding.

## Step 7 — Write Tests

Following the Test Requirements:

1. **Test: SPDX SBOM supplier backfill** — insert a test SPDX SBOM with known package entries missing supplier information, run the migration, and verify the `sbom_package` records are updated with the correct supplier values. Use value-based assertions (`assert_eq!` on specific supplier strings) rather than just checking non-null.

2. **Test: CycloneDX SBOMs unaffected** — insert both an SPDX SBOM and a CycloneDX SBOM (with `labels: {"type": "cyclonedx"}`), run the migration, and verify that only the SPDX SBOM's packages were processed. The CycloneDX document's packages should remain unchanged.

## Step 8 — Verify Acceptance Criteria

- [x] The migration re-processes all SPDX SBOM documents and populates supplier fields — verified by the filtered query on `labels->>'type' = 'spdx'` and the `suppliers()` call
- [x] CycloneDX documents are not loaded or processed by the migration — verified by the database-level filter excluding `cyclonedx` type documents
- [x] The `suppliers()` function in the ingestor is made public for reuse — visibility changed from `fn` to `pub fn`
- [x] The migration follows the existing migration pattern from `m0001_initial` — implements `MigrationTrait` with `up()` method

## Step 9 — Self-Verification

### Scope containment
- `modules/ingestor/src/graph/sbom/mod.rs` — in scope (Files to Modify)
- `migration/src/m0042_backfill_suppliers/mod.rs` — in scope (Files to Create)
- `migration/src/lib.rs` — OUT OF SCOPE: needed for migration registration but not listed in Files to Modify. Would flag this for user approval.

### Query-scope verification
See `query-scope.md` for detailed analysis. The migration uses a filtered query targeting only SPDX SBOMs via `labels->>'type' = 'spdx'`, avoiding loading hundreds of thousands of CycloneDX documents.

### Dead parameter detection
No parameters are being removed — not applicable.

### Symbol deduplication
The `suppliers()` function is reused from the ingestor module rather than redeclared. No new constants or type aliases are introduced.

### Module-level test requirement (Rust)
Would run `cargo metadata --no-deps --format-version 1` from the workspace root to resolve the crate names for the modified files:
- `modules/ingestor/src/graph/sbom/mod.rs` → resolve to the ingestor crate name (e.g., `trustify-module-ingestor`)
- `migration/src/m0042_backfill_suppliers/mod.rs` → resolve to the migration crate name (e.g., `trustify-migration`)

Then run:
```
cargo test -p trustify-module-ingestor
cargo test -p trustify-migration
```

## Step 10 — Commit and Push

```bash
git add modules/ingestor/src/graph/sbom/mod.rs migration/src/m0042_backfill_suppliers/mod.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): backfill SPDX SBOM supplier information

Add data migration m0042 that re-processes SPDX SBOMs to extract
package supplier data. Makes the ingestor's suppliers() function
public so the migration can reuse existing extraction logic.

Uses filtered query on sbom.labels jsonb column to target only
SPDX documents, avoiding unnecessary I/O on CycloneDX records.

Implements TC-9209"
```

Create PR:
```bash
gh pr create --base main --title "feat(migration): backfill SPDX SBOM supplier information" --body "..."
```
