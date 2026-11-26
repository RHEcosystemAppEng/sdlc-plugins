# Implementation Plan — TC-9209

**Summary**: Re-process all SPDX SBOMs to extract package supplier information
**Repository**: trustify-backend (Serena instance: `serena_backend`)
**Target Branch**: `main` → task branch `TC-9209`

---

## Step 0 – Project Configuration Validation

Mock CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` → `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142 (plus Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`)
- Code Intelligence: tool naming convention `mcp__<serena-instance>__<tool>`; limitation: rust-analyzer indexing delay on first use

Validation passes.

## Step 1 – Task Parsing

All required sections present: Repository, Target Branch (`main`), Description, Files to Modify, Files to Create, API Changes (none), Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (none). No Target PR, no Bookend Type → default flow. GitHub Issue field would be read from the fetched issue (skipped silently if empty).

## Step 1.5 / 2 / 3 – (simulated)

- Digest check: would fetch comments and compare `[sdlc-workflow] Description digest:` (not executed — no external calls).
- Dependencies: none.
- Would assign to current user and transition to In Progress (not executed).

## Step 4 – Understand the Code (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")` — locate `suppliers()`.
- `mcp__serena_backend__find_symbol("suppliers", include_body=true)` — read signature/body.
- `mcp__serena_backend__find_referencing_symbols("suppliers")` — confirm visibility change does not break callers (making a private fn `pub` is backward compatible).
- `mcp__serena_backend__find_symbol("Migration", include_body=true)` in `migration/src/m0001_initial/mod.rs` — migration structure (`DeriveMigrationName`, `MigrationTrait::up/down`).
- Read `migration/src/lib.rs` — how migrations are registered in `Migrator::migrations()`.
- Read `entity/src/sbom.rs` — confirm `labels: Json` column (jsonb) and column enum name.
- Read `entity/src/sbom_package.rs` — confirm supplier column exists (or where supplier is stored).
- Locate `SourceDocument::find_by_sbom_id` (`search_for_pattern("find_by_sbom_id")`).
- Verify `migration/Cargo.toml` already depends on `trustify-module-ingestor` (stated in notes) — so making `suppliers()` public is the correct "reuse over duplication" choice (no new dependency).
- Symbol dedup: grep for any existing `backfill`/`supplier` helpers before writing new ones.
- Read `CONVENTIONS.md` at repo root — extract CI check commands (e.g. `cargo fmt --check`, `cargo clippy`, `cargo test`) for Step 9.

Conventions to follow (from repo-backend.md): SeaORM for DB, `Result<T, _>` with `.context()` error wrapping, integration tests against real PostgreSQL, `assert_eq!` value assertions.

## Step 6 – Changes

### File to Modify: `modules/ingestor/src/graph/sbom/mod.rs`

- Change `fn suppliers(...)` → `pub fn suppliers(...)`.
- Add/ensure a `///` doc comment describing what it does (extracts supplier values from SPDX package entries) and its parameters/return.
- No signature or behavior change; existing callers unaffected.
- If the parent module (`graph/mod.rs` / `lib.rs`) does not re-export `graph::sbom` publicly, the path must be reachable; check with Serena. If a re-export change is needed, that would be an out-of-scope file and would be flagged to the user (Step 9).

### File to Create: `migration/src/m0042_backfill_suppliers/mod.rs`

Structure following `m0001_initial`:

```rust
use sea_orm::{ConnectionTrait, EntityTrait, QueryFilter, QuerySelect, sea_query::Expr};
use sea_orm_migration::prelude::*;
use trustify_entity::{sbom, sbom_package};
use trustify_module_ingestor::graph::sbom::suppliers;

/// Data migration that backfills `sbom_package` supplier values by re-parsing
/// SPDX source documents. CycloneDX documents are excluded at the query level.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Re-processes every SPDX SBOM and updates supplier fields on its packages.
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // Query scope: only SPDX documents. Filtered at the DB via the jsonb
        // `labels` column so CycloneDX rows (hundreds of thousands in prod)
        // are never loaded.
        let mut pages = sbom::Entity::find()
            .filter(Expr::cust("labels->>'type' = 'spdx'"))
            .select_only()
            .column(sbom::Column::SbomId)
            .into_tuple::<Uuid>()
            .paginate(db, BATCH_SIZE);

        while let Some(ids) = pages.fetch_and_next().await? {
            for sbom_id in ids {
                // Fetch raw bytes for this SBOM only
                let Some(doc) = SourceDocument::find_by_sbom_id(sbom_id).one(db).await? else {
                    continue; // defensive: missing source document
                };
                let spdx = parse_spdx(&doc.data)?;        // re-parse source
                for (purl_or_pkg_ref, supplier) in suppliers(&spdx) {
                    // update matching sbom_package row(s) for this sbom
                    sbom_package::Entity::update_many()
                        .col_expr(sbom_package::Column::Supplier, Expr::value(supplier))
                        .filter(sbom_package::Column::SbomId.eq(sbom_id))
                        .filter(/* package identity match */)
                        .exec(db).await?;
                }
            }
        }
        Ok(())
    }

    /// Data-only backfill; nothing to revert structurally.
    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        Ok(())
    }
}
```

Key design points:
- **Database query**: `SELECT sbom_id FROM sbom WHERE labels->>'type' = 'spdx'` — expressed in SeaORM via `Expr::cust("labels->>'type' = 'spdx'")` (or `Expr::col(sbom::Column::Labels).cast_json_field("type").eq("spdx")`). Only IDs are selected, paginated in batches, so memory is bounded and CycloneDX rows are never read.
- Source bytes fetched per-SBOM via `SourceDocument::find_by_sbom_id(id)` (per Implementation Notes) — no bulk load of documents.
- Reuses `trustify_module_ingestor::graph::sbom::suppliers` (no duplicated extraction logic).
- Defensive handling: skip SBOMs with missing source document / null supplier rather than panicking; parse errors mapped to `DbErr::Custom` with context.
- Updates scoped by `sbom_id` so only the current SPDX SBOM's packages are touched.
- Doc comments on all new public items.

### Out-of-scope file needed (flag, do not silently modify)

- `migration/src/lib.rs` — the new migration must be registered (`mod m0042_backfill_suppliers;` and `Box::new(m0042_backfill_suppliers::Migration)` in `Migrator::migrations()`), otherwise it never runs. This file is not listed in Files to Modify; per the skill it would be flagged at Step 9 scope containment and require explicit user approval before committing.
- Tests: the Test Requirements call for two tests but no test file is listed in Files to Create. Plan: put them as `#[cfg(test)] mod tests` inside `migration/src/m0042_backfill_suppliers/mod.rs` (in-scope), or — if the project convention requires `tests/` — flag the new test file for user approval.

## Step 7 – Tests

In `migration/src/m0042_backfill_suppliers/mod.rs` (`#[cfg(test)]`), against the PostgreSQL test DB:

1. `/// Verifies the migration populates supplier for packages of an SPDX SBOM.`
   - Given: ingest an SPDX SBOM whose packages have `supplier` set, with `sbom_package.supplier` cleared (NULL).
   - When: run `Migration.up()`.
   - Then: `assert_eq!` each package's supplier equals the expected value (e.g. `"Organization: Red Hat"`) — value-based, not count-only.
2. `/// Verifies CycloneDX SBOMs are untouched by the migration.`
   - Given: a CycloneDX SBOM with known supplier values (and one with NULL supplier, to prove it is not processed).
   - When: run `Migration.up()`.
   - Then: `assert_eq!` supplier values identical before/after.

Different setup/assertions → separate tests (not parameterized). Given/When/Then comments in both.

## Step 8 – Acceptance Criteria

| Criterion | How satisfied |
|---|---|
| Migration re-processes all SPDX SBOMs and populates supplier | Paginated loop over all `labels->>'type' = 'spdx'` SBOMs; test 1 |
| CycloneDX not loaded or processed | DB-level filter; CycloneDX rows never selected; test 2 |
| `suppliers()` made public | `pub fn suppliers` in ingestor |
| Follows `m0001_initial` pattern | `DeriveMigrationName` + `MigrationTrait` `up`/`down` |

## Step 9 – Self-Verification

- Scope containment: expected diff = the 2 listed files + `migration/src/lib.rs` (flagged for approval).
- Query-scope verification: see `query-scope.md` — query filtered to SPDX at the data source; no mismatch.
- Dead parameters: none (no code removed).
- Sensitive patterns: none.
- CI checks from CONVENTIONS.md; then `cargo test -p trustify-migration` and `cargo test -p trustify-module-ingestor` (crate names resolved via `cargo metadata`). Hard stop on any failure.
- Data-flow trace: `sbom` (SPDX filter) → `source_document` bytes → SPDX parse → `suppliers()` → `sbom_package` update. Complete.
- Contract/sibling parity: `MigrationTrait` both `up` and `down` implemented; parity with `m0001_initial`; cross-module entity check on `sbom_package` writes (ingestor writes the same column — use same value format).

## Step 10 / 11 – (simulated)

- Commit: `feat(migration): backfill SPDX package suppliers` with `Implements TC-9209` footer and `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- PR: `gh pr create --base main`, body `Implements [TC-9209](<webUrl>)`; PR description notes the reuse decision (made `suppliers()` public since migration already depends on the ingestor crate).
- Jira: set `customfield_10875` (ADF inlineCard) to PR URL, add comment with footnote, transition to In Review.
