# Implementation Plan — TC-9209

**Summary**: Re-process all SPDX SBOMs to extract package supplier information
**Repository**: trustify-backend (Serena instance: `serena_backend`)
**Target Branch**: `main` -> task branch `TC-9209`

## Step 0 — Project Configuration validation

The mock CLAUDE.md contains `# Project Configuration` with:
- Repository Registry (trustify-backend, `serena_backend`, `./`)
- Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142, PR field `customfield_10875`, GitHub Issue field `customfield_10747`)
- Code Intelligence (naming convention `mcp__<serena-instance>__<tool>`; limitation: rust-analyzer indexing delay)

Validation passes.

## Step 1 — Task parsing

All required sections are present (Repository, Target Branch, Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies). No Target PR, no Bookend Type -> default flow. GitHub Issue field would be read from `customfield_10747` (skipped if empty).

## Steps 1.5 / 2 / 3 — (simulated, not executed)

- Step 1.5: would fetch comments, look for `[sdlc-workflow] Description digest:` and compare via `scripts/sha256-digest.py`.
- Step 2: Dependencies = None -> nothing to verify.
- Step 3: would assign to current user and transition to In Progress.

## Step 4 — Code understanding (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `modules/ingestor/src/graph/sbom/mod.rs`
- `mcp__serena_backend__find_symbol(name_path_pattern="suppliers", include_body=true)` — confirm signature, inputs (SPDX package type) and return type
- `mcp__serena_backend__find_referencing_symbols` on `suppliers` — confirm the visibility change does not affect existing callers (making something `pub` is backward compatible)
- `mcp__serena_backend__find_symbol(name_path_pattern="MigrationTrait")` and read `migration/src/m0001_initial/mod.rs` — sibling migration pattern (`DeriveMigrationName`, `#[async_trait] impl MigrationTrait for Migration { async fn up(...); async fn down(...) }`)
- Read `migration/src/lib.rs` to see how migrations are registered in `Migrator::migrations()`
- Read `entity/src/sbom.rs` to confirm the `labels: Json` column and `entity/src/sbom_package.rs` to confirm the supplier column name
- `search_for_pattern("find_by_sbom_id")` to confirm the `SourceDocument::find_by_sbom_id` helper and its return type
- Read `migration/Cargo.toml` to confirm the `trustify-module-ingestor` dependency (per Implementation Notes)
- Read `CONVENTIONS.md` at repo root and extract CI check commands (e.g. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) for Step 9
- Symbol deduplication: grep the migration crate and ingestor for any existing SPDX label filter helper (e.g. `is_spdx`, `labels->>'type'`, `Expr::cust`) before writing a new one

Conventions to follow (from repo-backend.md): SeaORM for DB access, `Result<T, _>` with `.context()` error wrapping, integration tests against a real PostgreSQL DB with `assert_eq!` style.

## Step 6 — Changes

### File to modify: `modules/ingestor/src/graph/sbom/mod.rs`

- Change `fn suppliers(...)` to `pub fn suppliers(...)`.
- Add a `///` doc comment describing what it does (extracts supplier values from SPDX package entries) since it is now part of the public API.
- No logic changes. Reuse-over-duplication rule: the migration crate already depends on `trustify-module-ingestor`, so the function is made public and imported rather than duplicated.
- If `graph::sbom` is not itself publicly reachable from the crate root, that would require a re-export in `modules/ingestor/src/lib.rs` / `graph/mod.rs` — that would be out of scope and flagged for approval (see Scope notes).

### File to create: `migration/src/m0042_backfill_suppliers/mod.rs`

Follows the `m0001_initial` pattern:

```rust
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect, sea_query::Expr};
use sea_orm_migration::prelude::*;
use trustify_entity::{sbom, sbom_package, source_document::SourceDocument};
use trustify_module_ingestor::graph::sbom::suppliers;

/// Backfills `sbom_package` supplier values by re-parsing SPDX SBOM source documents.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Re-processes SPDX SBOMs only; CycloneDX documents already have suppliers populated.
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // Query scope: SPDX only. Filtering at the database via the jsonb `labels`
        // column avoids loading the (much larger) CycloneDX population.
        let spdx_ids: Vec<Uuid> = sbom::Entity::find()
            .select_only()
            .column(sbom::Column::SbomId)
            .filter(Expr::cust("labels->>'type' = 'spdx'"))
            .into_tuple()
            .all(db)
            .await?;

        for sbom_id in spdx_ids {
            let Some(doc) = SourceDocument::find_by_sbom_id(sbom_id, db).await? else {
                // log + skip: missing source document should not abort the migration
                continue;
            };
            let spdx = parse_spdx(&doc.data)?;           // re-parse raw bytes
            for (package_ref, supplier) in suppliers(&spdx) {
                sbom_package::Entity::update_many()
                    .col_expr(sbom_package::Column::Supplier, Expr::value(supplier))
                    .filter(sbom_package::Column::SbomId.eq(sbom_id))
                    .filter(sbom_package::Column::NodeId.eq(package_ref))
                    .exec(db)
                    .await?;
            }
        }
        Ok(())
    }

    /// Data-only backfill; no schema change to revert.
    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        Ok(())
    }
}
```

Notes:
- Exact column names (`SbomId`, `Supplier`, `NodeId`) and `suppliers()` signature will be confirmed in Step 4 before writing.
- Iteration is by ID list then per-document fetch, so only one raw document is held in memory at a time. For very large SPDX sets, page the ID query (`.paginate(db, 1000)`) rather than `.all()`.
- Each SBOM's updates run in a transaction (`db.begin()`), matching cross-module entity handling for `sbom_package` writes in the ingestor.
- Defensive access: SPDX packages without a `supplier` field (or `NOASSERTION`) are skipped rather than unwrapped.
- An equivalent SeaORM-native filter, if the project has a JSON helper, is `Expr::cust_with_values("labels ->> 'type' = $1", ["spdx"])`; the bound-value form is preferred.

## How the database is queried for the migration

```sql
-- ID selection (only SPDX rows are read)
SELECT sbom_id FROM sbom WHERE labels->>'type' = 'spdx';

-- Per SBOM: raw document
SELECT * FROM source_document WHERE sbom_id = $1;   -- via SourceDocument::find_by_sbom_id

-- Per package with a supplier
UPDATE sbom_package SET supplier = $1 WHERE sbom_id = $2 AND node_id = $3;
```

CycloneDX rows (`labels->>'type' = 'cyclonedx'`) are never selected, so their source documents are never fetched or parsed. If no index exists on `(labels->>'type')`, a sequential scan of `sbom` (metadata only, not documents) is still cheap relative to loading documents; an expression index could be suggested in the PR description but is not added here (out of scope).

## Step 7 — Tests

Location: tests for the migration in the migration crate (or `tests/` per CONVENTIONS.md), against the real PostgreSQL test DB.

1. `/// Verifies the migration populates supplier values for packages of an SPDX SBOM.`
   - Given: ingest an SPDX fixture with known package suppliers, then null out `sbom_package.supplier`
   - When: run `m0042_backfill_suppliers::Migration.up()`
   - Then: `assert_eq!` on the specific supplier strings for specific packages (value-based, not count-only)
2. `/// Verifies CycloneDX SBOMs are untouched by the migration.`
   - Given: a CycloneDX SBOM with a sentinel supplier value (and an SPDX SBOM alongside)
   - When: run the migration
   - Then: `assert_eq!` CycloneDX package suppliers equal the sentinel values exactly as before

Both tests use given/when/then comments. Run `cargo test -p <crate>` for the migration crate and the ingestor crate (crate names resolved via `cargo metadata`).

## Step 8 — Acceptance criteria mapping

| Criterion | How satisfied |
|---|---|
| Re-processes all SPDX SBOMs and populates supplier | ID query over `labels->>'type' = 'spdx'`, update loop; test 1 |
| CycloneDX not loaded or processed | Filter at the DB query; CycloneDX IDs never selected; test 2 |
| `suppliers()` made public | `pub fn suppliers` in ingestor |
| Follows `m0001_initial` pattern | `DeriveMigrationName` + `MigrationTrait` `up()`/`down()` |

## Step 9 — Self-verification

- **Scope containment**: in-scope files are `modules/ingestor/src/graph/sbom/mod.rs` and `migration/src/m0042_backfill_suppliers/mod.rs`. **Flag**: a new migration must be registered in `migration/src/lib.rs` (`mod m0042_backfill_suppliers;` + `Box::new(m0042_backfill_suppliers::Migration)` in `Migrator::migrations()`), otherwise it never runs. This file is not listed in Files to Modify, so it would be presented to the user for explicit approval before committing. Test files likewise would be flagged if they fall outside the listed paths.
- **Query-scope verification**: see `query-scope.md` — query is filtered to SPDX at the data source.
- **Data-flow trace**: `sbom` (SPDX IDs) -> `source_document` bytes -> SPDX parse -> `suppliers()` -> `sbom_package.supplier` update. Complete, provided the migration is registered in `lib.rs` (flagged above).
- **Contract & sibling parity**: Contract: `MigrationTrait` needs `up()` (and `down()` matching sibling). Sibling parity: same structure/naming as `m0001_initial`. Cross-module entity: `sbom_package` writes are compared with the ingestor's write path (transaction usage, conflict handling). Caller-site: `suppliers()` is called with the same input type as the ingestor's existing call site.
- **Dead parameter / duplication / sensitive patterns**: no code removed; supplier logic reused, not duplicated; no secrets.
- **CI**: run CONVENTIONS.md CI commands and `cargo test -p` for both crates; hard stop on any failure.

## Steps 10–11 — (simulated)

- Commit: `feat(migration): backfill package suppliers for SPDX SBOMs` with body, `Implements TC-9209`, `--trailer="Assisted-by: Claude Code"`.
- PR: `gh pr create --base main` (or fork flags if `upstream` exists); body includes `Implements [TC-9209](<webUrl>)` and `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.
- Jira: set `customfield_10875` with ADF inlineCard of the PR URL, add comment (PR link, summary, deviation: `migration/src/lib.rs` registration) ending with the skill footnote, transition to In Review.
