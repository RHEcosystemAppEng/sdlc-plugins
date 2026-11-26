# Implementation Plan — TC-9209

**Summary**: Re-process all SPDX SBOMs to extract package supplier information
**Repository**: trustify-backend (Serena instance: `serena_backend`)
**Target Branch**: `main` (task branch: `TC-9209`)
**Dependencies**: None (Step 2 passes trivially)

## Step 0 — Project Configuration validation

The mock CLAUDE.md contains `## Repository Registry` (trustify-backend / serena_backend / `./`),
`## Jira Configuration` (Project key TC, Cloud ID, Feature issue type ID 10142), and
`## Code Intelligence` (tool naming convention `mcp__<serena-instance>__<tool>`). Validation passes.

## Step 1 — Task parsing

All required sections are present: Repository, Target Branch, Description, Files to Modify,
Files to Create, API Changes (none), Implementation Notes, Acceptance Criteria, Test
Requirements, Dependencies. No Target PR, no Bookend Type → default flow.
GitHub Issue custom field `customfield_10747` would be read; if empty, skipped.

## Steps 1.5 / 3 (simulated — no external calls)

- Would fetch comments and verify the `[sdlc-workflow] Description digest:` comment.
- Would assign to current user and transition TC-9209 to In Progress.

## Step 4 — Understand the code (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")`
- `mcp__serena_backend__find_symbol("suppliers", include_body=true)` — confirm signature and SPDX logic
- `mcp__serena_backend__find_referencing_symbols("suppliers")` — confirm callers are unaffected by a visibility change
- `mcp__serena_backend__get_symbols_overview("migration/src/m0001_initial/mod.rs")` and `migration/src/lib.rs` — migration structure + `Migrator::migrations()` registration
- `mcp__serena_backend__find_symbol("Model", relative_path="entity/src/sbom.rs")` — confirm `labels: Json` column
- `mcp__serena_backend__find_symbol("find_by_sbom_id")` — confirm `SourceDocument::find_by_sbom_id` signature
- `mcp__serena_backend__find_symbol("Model", relative_path="entity/src/sbom_package.rs")` — confirm supplier column on `sbom_package`
- Verify `migration/Cargo.toml` already depends on `trustify-module-ingestor` (per Implementation Notes)
- Read `CONVENTIONS.md` at repo root; extract CI check commands for Step 9
- Search for existing JSONB label-filter helpers in `common/src/db/query.rs` to reuse rather than hand-writing the filter

Convention notes (from repo-backend.md): SeaORM for DB access, `Result<T, AppError>` with
`.context()`, integration tests against real PostgreSQL, `assert_eq!` style assertions.

## Step 6 — Changes

### File to Modify: `modules/ingestor/src/graph/sbom/mod.rs`

- Change `fn suppliers(...)` to `pub fn suppliers(...)` (no behavior change).
- Add a `///` doc comment describing it: extracts supplier values from SPDX package entries.
- Ensure it is reachable from the crate root (re-export via `graph::sbom` module path if
  `graph`/`sbom` modules are not already `pub`; verify with `get_symbols_overview` on
  `modules/ingestor/src/lib.rs` and `graph/mod.rs`). If making the modules public would
  require touching files outside scope, flag in Step 9 scope containment for user approval.
- Reuse-over-duplication rationale: migration crate already depends on
  `trustify-module-ingestor`, so make public and import instead of duplicating.

### File to Create: `migration/src/m0042_backfill_suppliers/mod.rs`

Following `m0001_initial` pattern:

```rust
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, Condition};
use sea_orm::sea_query::Expr;
use sea_orm_migration::prelude::*;
use trustify_entity::{sbom, sbom_package};
use trustify_module_ingestor::graph::sbom::suppliers;

/// Data migration that backfills package supplier information for SPDX SBOMs only.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Re-parses each SPDX SBOM's source document and updates `sbom_package` supplier values.
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // Query scope: only SPDX documents. CycloneDX already has suppliers populated
        // at ingestion, and production holds far more CycloneDX than SPDX documents,
        // so filtering at the database avoids loading hundreds of thousands of rows.
        let spdx_sboms = sbom::Entity::find()
            .filter(Expr::cust(r#"labels->>'type' = 'spdx'"#))
            .select_only()
            .column(sbom::Column::SbomId)
            .into_tuple::<Uuid>()
            .stream(db)            // stream / paginate in batches rather than .all()
            .await?;

        while let Some(sbom_id) = spdx_sboms.try_next().await? {
            let Some(doc) = SourceDocument::find_by_sbom_id(sbom_id, db).await? else {
                // Defensive: source missing — log and skip
                continue;
            };
            let spdx = parse_spdx(&doc.data)?;             // existing SPDX parser
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

    /// Data backfill is not reversible; down is a no-op.
    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        Ok(())
    }
}
```

Notes:
- Exact column names (`sbom_id`, `node_id`, `supplier`) and the parser entry point will be
  confirmed via Serena in Step 4 before writing.
- Prefer the JSONB containment form `labels @> '{"type":"spdx"}'` if a GIN index exists on
  `labels` (index-friendly); otherwise `labels->>'type' = 'spdx'`. If `common/src/db/query.rs`
  provides a label filter helper, reuse it.
- Process in batches (stream or paginated `.paginate(db, 500)`) so memory stays bounded;
  wrap each SBOM's updates in a transaction for consistency.
- Registration: the new migration must be added to `Migrator::migrations()` in
  `migration/src/lib.rs` (`mod m0042_backfill_suppliers;` + `Box::new(m0042_backfill_suppliers::Migration)`).
  `migration/src/lib.rs` is NOT listed in Files to Modify, so this will be flagged in the
  Step 9 scope containment check for user approval (without it the migration never runs).

### How the database is queried for the migration

1. **Select SPDX SBOM IDs only**:
   ```sql
   SELECT sbom_id FROM sbom WHERE labels->>'type' = 'spdx';
   -- or, index-friendly: WHERE labels @> '{"type": "spdx"}'
   ```
   Streamed / paginated, never `sbom::Entity::find().all()`.
2. **Per SPDX SBOM, fetch raw bytes**: `SourceDocument::find_by_sbom_id(sbom_id)`.
3. **Extract suppliers** with the now-public `suppliers()` helper.
4. **Update**: `UPDATE sbom_package SET supplier = $1 WHERE sbom_id = $2 AND node_id = $3;`
   CycloneDX rows are never selected, loaded, or updated.

## Step 7 — Tests

Located alongside migration tests (or `tests/` per CONVENTIONS.md), using a real PostgreSQL test DB:

```rust
/// Verifies the migration populates supplier values for packages in an SPDX SBOM.
#[tokio::test]
async fn backfill_populates_spdx_suppliers() {
    // Given an ingested SPDX SBOM whose sbom_package rows have NULL supplier
    // When running m0042_backfill_suppliers::Migration::up
    // Then each package's supplier equals the value from the SPDX document
    //   (assert_eq! on specific package -> supplier pairs, not just counts)
}

/// Verifies CycloneDX SBOMs are untouched by the migration.
#[tokio::test]
async fn backfill_does_not_touch_cyclonedx() {
    // Given an ingested CycloneDX SBOM with known supplier values (and a sentinel value)
    // When running the migration
    // Then its sbom_package supplier values are byte-for-byte unchanged
}
```

Two tests have different setup/assertions → separate tests, not parameterized.
Run `cargo test -p trustify-migration` and `cargo test -p trustify-module-ingestor`
(crate names resolved via `cargo metadata`).

## Step 8 — Acceptance criteria mapping

| Criterion | Satisfied by |
|---|---|
| Re-processes all SPDX SBOMs and populates suppliers | Filtered SPDX query + per-SBOM update loop; test 1 |
| CycloneDX not loaded or processed | `labels->>'type' = 'spdx'` filter at the DB; test 2 |
| `suppliers()` made public | `pub fn suppliers` in ingestor |
| Follows `m0001_initial` pattern | `DeriveMigrationName` + `MigrationTrait::up/down` |

## Step 9 — Self-verification (planned)

- **Scope containment**: expected diff = `modules/ingestor/src/graph/sbom/mod.rs`,
  `migration/src/m0042_backfill_suppliers/mod.rs`, plus test file(s). Flag
  `migration/src/lib.rs` (registration) for user approval.
- **Query-scope verification**: see `query-scope.md` — query restricted to SPDX via `labels`.
- **Data-flow trace**: `sbom` (SPDX filter) → `source_document` bytes → SPDX parse →
  `suppliers()` → `sbom_package.supplier` update. Complete once registered in `Migrator`.
- **Contract & sibling parity**: `MigrationTrait` fully implemented (up + down); parity
  with `m0001_initial`; cross-module entity check on `sbom_package` writes (ingestor uses
  the same table — match its conflict/transaction handling); caller-site check on
  `SourceDocument::find_by_sbom_id` usage.
- **CI checks** from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`), hard stop on failure.
- **Sensitive pattern check** on staged diff.

## Steps 10–11 (simulated)

- Commit: `feat(migration): backfill package suppliers for SPDX SBOMs` with footer
  `Implements TC-9209` and `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- `gh pr create --base main`, body `Implements [TC-9209](<webUrl>)`.
- Set `customfield_10875` (ADF inlineCard with PR URL), add Jira comment with summary
  and footnote, transition to In Review.
