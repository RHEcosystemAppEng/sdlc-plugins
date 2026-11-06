# Implementation Plan — TC-9209

**Summary**: Re-process all SPDX SBOMs to extract package supplier information
**Repository**: trustify-backend (Serena instance: `serena_backend`)
**Target Branch**: `main` -> task branch `TC-9209`

> Simulated run: no repository files were modified and no external tools (Jira, git, Serena) were called.

## Step 0 – Project Configuration validation

The mock CLAUDE.md has all three required sections:
- Repository Registry: `trustify-backend | Rust backend service | serena_backend | ./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142
- Code Intelligence: `mcp__<serena-instance>__<tool>` naming convention, with `serena_backend` (rust-analyzer)

Validation passes.

## Step 1 – Task parsing

All required sections are present: Repository, Target Branch (`main`), Description, Files to Modify, Files to Create, API Changes (none), Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (none). There is no Target PR and no Bookend Type, so the default flow applies (new branch + new PR). The GitHub Issue custom field (`customfield_10747`) would be read and, if it has a value, a `Closes owner/repo#N` line added to the PR body.

## Steps 1.5 / 2 / 3 – Jira (simulated)

- Description digest check: fetch comments, find the `[sdlc-workflow] Description digest:` comment, and compare it to `python3 scripts/sha256-digest.py`. If no digest comment exists, warn and continue.
- Dependencies: none, so nothing to verify.
- Assign TC-9209 to the current user (`jira.user_info()` then `jira.edit_issue`) and transition it to In Progress.

## Step 4 – Understand the code (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")`: locate `suppliers()`.
- `mcp__serena_backend__find_symbol("suppliers", include_body=true)`: confirm the signature and what it returns.
- `mcp__serena_backend__find_referencing_symbols("suppliers")`: confirm that changing visibility only (private to `pub`) breaks no callers.
- `mcp__serena_backend__get_symbols_overview("migration/src/m0001_initial/mod.rs")` and `migration/src/lib.rs`: learn the `MigrationTrait` structure and how migrations are registered.
- `mcp__serena_backend__find_symbol("Model", relative_path="entity/src/sbom.rs")`: confirm `labels: Json` (jsonb) and the `sbom_id` primary key.
- `mcp__serena_backend__find_symbol("find_by_sbom_id")`: confirm the `SourceDocument::find_by_sbom_id(id)` signature and return type.
- `mcp__serena_backend__get_symbols_overview("entity/src/sbom_package.rs")`: find the supplier column and the key columns used to match packages.
- Check that `migration/Cargo.toml` already depends on `trustify-module-ingestor`, as the task states. That means making the function `pub` is the right reuse choice (no new dependency is introduced).
- Read `CONVENTIONS.md` at the repo root and extract its CI check commands for Step 9.
- Docs to check: `README.md`, `docs/architecture.md`. A data migration probably has no doc impact.

Expected conventions (from repo-backend.md): `Result<T, AppError>` with `.context()`, SeaORM, `verb_noun` naming, and integration tests against a real PostgreSQL database.

## Step 6 – Changes

### File to modify: `modules/ingestor/src/graph/sbom/mod.rs`

- Change `fn suppliers(...)` to `pub fn suppliers(...)`. Keep the signature and body as they are.
- Add a `///` doc comment, e.g. `/// Extracts supplier names from an SPDX package entry; shared with the m0042 supplier backfill migration.`
- Make sure the containing module path is reachable from the crate root, e.g. `trustify_module_ingestor::graph::sbom::suppliers`. If `graph` or `sbom` is not `pub` in `lib.rs` / `graph/mod.rs`, flag that instead of silently editing out-of-scope files (see the scope notes below).

### File to create: `migration/src/m0042_backfill_suppliers/mod.rs`

The structure follows `m0001_initial`:

```rust
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QueryOrder, QuerySelect, sea_query::Expr};
use sea_orm_migration::prelude::*;
use trustify_entity::{sbom, sbom_package};
use trustify_module_ingestor::graph::sbom::suppliers;

/// Data migration that backfills `sbom_package` supplier values by re-parsing SPDX SBOM source documents.
#[derive(DeriveMigrationName)]
pub struct Migration;

const BATCH_SIZE: u64 = 500;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();
        let mut last_id = None;
        loop {
            // Query scope: SPDX documents only. Filtered at the DB via labels->>'type'.
            // CycloneDX documents already have suppliers populated at ingestion, and there are
            // hundreds of thousands of them, so they are never loaded.
            let mut q = sbom::Entity::find()
                .select_only()
                .column(sbom::Column::SbomId)
                .filter(Expr::cust("labels->>'type' = 'spdx'"))
                .order_by_asc(sbom::Column::SbomId)
                .limit(BATCH_SIZE);
            if let Some(id) = last_id { q = q.filter(sbom::Column::SbomId.gt(id)); }
            let ids: Vec<Uuid> = q.into_tuple().all(db).await?;
            if ids.is_empty() { break; }

            for id in &ids {
                let Some(doc) = SourceDocument::find_by_sbom_id(*id).one(db).await? else { continue; };
                let spdx = parse_spdx(&doc.data)?;          // reuse the existing SPDX parser used by the ingestor
                for pkg in spdx.package_information.iter() {
                    let supplier = suppliers(pkg);           // reused, now-public helper
                    if supplier.is_empty() { continue; }
                    sbom_package::Entity::update_many()
                        .col_expr(sbom_package::Column::Supplier, Expr::value(supplier))
                        .filter(sbom_package::Column::SbomId.eq(*id))
                        .filter(sbom_package::Column::NodeId.eq(&pkg.package_spdx_identifier))
                        .exec(db).await?;
                }
            }
            last_id = ids.last().copied();
        }
        Ok(())
    }

    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        // Data-only backfill; nothing to revert (supplier values were previously absent).
        Ok(())
    }
}
```

Notes:
- Each batch's updates run in a transaction (`db.begin()` / `txn.commit()`), matching how the ingestor writes `sbom_package`. This is checked under cross-module entity parity.
- Defensive access: a missing source document is skipped and logged with `log::warn!`, not a panic. A package with no `supplier` field (an `Option`) is skipped.
- Exact column names (`Supplier`, `NodeId`) and the SPDX parser entry point will be confirmed in Step 4. If they differ, follow the real code.
- If a JSON-path helper exists in `common/src/db/query.rs`, reuse it instead of `Expr::cust`, and use a bound parameter for the `'spdx'` literal.

### How the database is queried for the migration

1. **Select candidate SBOMs, SPDX only, filtered in SQL**:
   ```sql
   SELECT sbom_id FROM sbom
   WHERE labels->>'type' = 'spdx' AND sbom_id > $last_id
   ORDER BY sbom_id LIMIT 500;
   ```
   Keyset pagination keeps memory flat and never touches CycloneDX rows. A `Document::all()` / `sbom::Entity::find().all()` followed by in-Rust filtering is explicitly rejected (see query-scope.md).
2. **Fetch raw bytes per SPDX SBOM** with `SourceDocument::find_by_sbom_id(id)`, which only runs for the filtered IDs.
3. **Update `sbom_package`** with `UPDATE sbom_package SET supplier = $1 WHERE sbom_id = $2 AND node_id = $3`, in one transaction per batch.
4. Optional, flagged rather than done: an expression index `CREATE INDEX ON sbom ((labels->>'type'))` would speed up the filter. It is out of scope for this task, so it is suggested to the user only.

## Step 7 – Tests

These go in a `#[cfg(test)] mod tests` block inside `migration/src/m0042_backfill_suppliers/mod.rs`, which keeps them in scope. They use the repo's PostgreSQL test DB bootstrap.

```rust
/// Verifies the backfill populates supplier values on sbom_package rows for an SPDX SBOM.
#[tokio::test]
async fn backfill_populates_spdx_suppliers() {
    // Given an ingested SPDX SBOM whose package rows have no supplier
    // When the m0042 migration runs
    // Then each package's supplier equals the SPDX `supplier` value
    assert_eq!(supplier_for(&db, sbom_id, "SPDXRef-pkg-a").await, Some("Organization: Acme".into()));
}

/// Verifies CycloneDX SBOMs are untouched by the backfill.
#[tokio::test]
async fn backfill_skips_cyclonedx() {
    // Given an ingested CycloneDX SBOM with known supplier values
    // When the m0042 migration runs
    // Then its sbom_package rows are identical (value comparison) to the pre-migration snapshot
    assert_eq!(rows_after, rows_before);
}
```

The assertions compare values, not just counts. The two tests have different setup and different assertions, so they are separate functions rather than parameterized.

Run: `cargo test -p <migration crate name resolved via cargo metadata>` and `cargo test -p trustify-module-ingestor`.

## Step 8 – Acceptance criteria

| Criterion | How it is met |
|---|---|
| Re-processes all SPDX SBOMs and populates suppliers | Keyset loop over every `labels->>'type' = 'spdx'` row; `sbom_package.supplier` is updated |
| CycloneDX not loaded or processed | The SQL filter excludes them at the source; `backfill_skips_cyclonedx` tests this |
| `suppliers()` made public | `pub fn suppliers` in the ingestor |
| Follows `m0001_initial` pattern | `DeriveMigrationName` + `MigrationTrait::up/down` |

## Step 9 – Self-verification notes

- **Scope containment and out-of-scope flags (need user approval, not added silently):**
  - `migration/src/lib.rs`: the new migration must be added with `mod m0042_backfill_suppliers;` and `Box::new(m0042_backfill_suppliers::Migration)` in `Migrator::migrations()`. Without this the migration never runs. This file is not listed in Files to Modify, so it is flagged for approval.
  - Possibly `modules/ingestor/src/lib.rs` / `graph/mod.rs`, if the `graph::sbom` module path is not already public.
  - The SPDX parser entry point, if it is also private.
- **Query-scope verification:** the task targets the SPDX subset and the query filters on `labels->>'type' = 'spdx'`, so there is no mismatch. Details are in `query-scope.md`.
- **Reuse:** `suppliers()` is reused, not duplicated. The dependency already exists, so making it `pub` is the correct option.
- **Data-flow trace:** `sbom` (SPDX filter) -> `source_document` bytes -> SPDX parse -> `suppliers()` -> `sbom_package.supplier` update. Every stage connects.
- **Contract & sibling parity:** `MigrationTrait` is implemented with both `up` and `down`. The migration matches m0001 structure. It uses the same transaction pattern as the ingestor's `sbom_package` writes. It calls `suppliers()` the same way the ingestor does.
- **CI:** run the commands extracted from `CONVENTIONS.md` (e.g. `cargo fmt --check`, `cargo clippy`, `cargo check`). Any failure is a hard stop.

## Steps 10–11 (simulated)

- Commit:
  ```
  git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): backfill SPDX package suppliers

  Makes ingestor suppliers() public and reuses it in m0042 migration,
  which re-processes only SPDX SBOMs (filtered via labels->>'type').

  Implements TC-9209"
  ```
- Create the PR with `gh pr create --base main`, with the body containing `Implements [TC-9209](<webUrl>)` (and `Closes ...` if the GitHub issue field is set).
- Jira: set `customfield_10875` to the PR URL as an ADF inlineCard. Add a comment covering the PR link, a summary, and deviations (the lib.rs registration flag), ending with the footer from `shared/comment-footnote.md`. Transition to In Review.
