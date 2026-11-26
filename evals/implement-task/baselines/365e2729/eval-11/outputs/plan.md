# Implementation Plan — TC-9209

**Summary:** Re-process all SPDX SBOMs to extract package supplier information
**Repository:** trustify-backend (Serena instance: `serena_backend`)
**Target Branch:** main
**Task Branch:** `TC-9209` (created from `main`)

---

## Step 0 – Project Configuration Validation

The mock CLAUDE.md contains everything the skill needs:
- Repository Registry: trustify-backend -> `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID, and Feature issue type ID 10142 (plus Git PR field `customfield_10875` and GitHub Issue field `customfield_10747`)
- Code Intelligence: tool naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer)

Validation passes.

## Step 1 – Task Parsing

All required sections are present: Repository, Target Branch (`main`), Description, Files to Modify, Files to Create, API Changes (none), Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (none).
- No Target PR, so this is the default flow (new branch and new PR).
- No Bookend Type, so the normal implementation steps apply.
- GitHub Issue field (`customfield_10747`): would be read from the issue. If it is empty, skip it.

## Steps 1.5 / 2 / 3 – Integrity, Dependencies, Jira Transition (simulated)

- Step 1.5: fetch the comments, find the `[sdlc-workflow] Description digest:` comment and compare digests. Not executed in this eval because external calls are not allowed.
- Step 2: Dependencies: None. Nothing to verify.
- Step 3: would assign TC-9209 to the current user and move it to In Progress. Not executed in this eval.

## Step 4 – Code Understanding (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")`: find `suppliers()` and see its signature.
- `mcp__serena_backend__find_symbol("suppliers", include_body=true)`: read the SPDX supplier extraction logic.
- `mcp__serena_backend__find_referencing_symbols("suppliers")`: confirm that making it `pub` does not break any caller. Widening visibility is backward compatible.
- `mcp__serena_backend__get_symbols_overview("migration/src/m0001_initial/mod.rs")` and `migration/src/lib.rs`: learn the `MigrationTrait` / `Migrator` registration pattern.
- `mcp__serena_backend__find_symbol("Model", relative_path="entity/src/sbom.rs")`: confirm the `labels: Json` column and the `sbom_id` primary key.
- `mcp__serena_backend__find_symbol("find_by_sbom_id")`: confirm the `SourceDocument::find_by_sbom_id` signature and return type.
- `mcp__serena_backend__find_symbol("Model", relative_path="entity/src/sbom_package.rs")`: confirm there is a `supplier` column, or the column the supplier should be written to.
- `migration/Cargo.toml`: confirm it already depends on `trustify-module-ingestor`, as the Implementation Notes say. If it does, making the function `pub` is the right reuse path ("Reuse over duplication", option 2). Do not duplicate the function.
- CONVENTIONS.md at the repo root: read it and record the CI check commands (for example `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) for Step 9.
- Documentation: README.md and `docs/architecture.md`. These are unlikely to need changes because the work is an internal data migration with no API change.

**Conventions found (binding for implementation):**
- Error handling: `Result<T, AppError>` / `.context()` in services. Migrations return `Result<(), DbErr>`, so any errors are mapped to `DbErr::Migration(...)` / `DbErr::Custom(...)`.
- Migration naming: `mNNNN_<snake_case>` module with `mod.rs`, `#[derive(DeriveMigrationName)] pub struct Migration;`, and `#[async_trait] impl MigrationTrait for Migration { async fn up(...); async fn down(...) }`.
- Tests: integration tests against a real PostgreSQL test DB, value-based assertions.

## Step 5 – Branch

```
git checkout main && git pull && git checkout -b TC-9209
```

## Step 6 – Changes

### File to Modify: `modules/ingestor/src/graph/sbom/mod.rs`

- Change `fn suppliers(...)` to `pub fn suppliers(...)`.
- Add a `///` doc comment, for example: `/// Extracts supplier names from an SPDX package entry; returns an empty vec when the supplier is absent or NOASSERTION.` (Match the wording to the actual behavior.)
- If `graph::sbom` is not already reachable from the crate root (`lib.rs` -> `pub mod graph;` -> `pub mod sbom;`), check the module visibility chain. If any parent module is private, that edit is still in `mod.rs` or `lib.rs`. Because `lib.rs` is not in Files to Modify, I would flag that change for approval in the Step 9 scope check rather than make it silently.
- No logic changes. The function keeps a single definition, so future fixes apply in one place.

### File to Create: `migration/src/m0042_backfill_suppliers/mod.rs`

Structure, following the `m0001_initial` pattern:

```rust
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect, ConnectionTrait, sea_query::Expr};
use sea_orm_migration::prelude::*;
use trustify_entity::{sbom, sbom_package};
use trustify_module_ingestor::graph::sbom::suppliers;

/// Backfills `sbom_package` supplier values by re-parsing SPDX source documents.
/// Only SPDX SBOMs are loaded; CycloneDX documents already carry supplier data.
#[derive(DeriveMigrationName)]
pub struct Migration;

const BATCH_SIZE: u64 = 500;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();
        let mut last_id = None;
        loop {
            // Query scope: SPDX only, filtered at the database by labels->>'type'.
            let mut q = sbom::Entity::find()
                .select_only()
                .column(sbom::Column::SbomId)
                .filter(Expr::cust("labels->>'type' = 'spdx'"))
                .order_by_asc(sbom::Column::SbomId)
                .limit(BATCH_SIZE);
            if let Some(id) = last_id {
                q = q.filter(sbom::Column::SbomId.gt(id));
            }
            let ids: Vec<Uuid> = q.into_tuple().all(db).await?;
            if ids.is_empty() { break; }

            for id in &ids {
                let Some(doc) = SourceDocument::find_by_sbom_id(*id, db).await? else { continue };
                let spdx = parse_spdx(&doc.data)
                    .map_err(|e| DbErr::Migration(format!("sbom {id}: {e}")))?;
                for pkg in spdx.package_information.iter() {
                    let supplier = suppliers(pkg);   // reused ingestor helper
                    if supplier.is_empty() { continue; }
                    sbom_package::Entity::update_many()
                        .col_expr(sbom_package::Column::Supplier, Expr::value(supplier.join(", ")))
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
        // Data-only backfill; values remain valid, nothing to revert.
        Ok(())
    }
}
```

The exact column names (`NodeId`, `Supplier`), the parser entry point, and the `suppliers()` return type would be confirmed in Step 4 with Serena before writing the code. The block above is the intended shape.

Design points:
- **SPDX-only query at the source.** The filter is `WHERE labels->>'type' = 'spdx'` on `sbom.labels` (jsonb). CycloneDX rows are never loaded. See `query-scope.md`.
- **Select only `sbom_id`** for the scan, so full sbom rows are not loaded.
- **Keyset pagination** (`sbom_id > last_id ORDER BY sbom_id LIMIT 500`) bounds memory and avoids OFFSET cost.
- **Per-SBOM source fetch** through the existing `SourceDocument::find_by_sbom_id`. This reuses the existing accessor and adds no new raw SQL against `source_document`.
- **Reuse** of `trustify_module_ingestor::graph::sbom::suppliers`. The existing crate dependency makes this the correct choice over duplication. The PR description records that decision.
- **Defensive access:** a missing source document is skipped (`continue`), and absent or `NOASSERTION` suppliers are skipped. A parse failure aborts the migration with a `DbErr::Migration` that includes the sbom id. Alternatively it could log and skip. Because this is a backfill of previously ignored data, I would confirm with the user which behavior they prefer. Default: fail loudly.
- **Doc comments** on the `Migration` struct and on the newly public `suppliers`.

### Registration (out-of-scope flag)

`migration/src/lib.rs` must add `mod m0042_backfill_suppliers;` and `Box::new(m0042_backfill_suppliers::Migration)` to `Migrator::migrations()`, or the migration never runs. `lib.rs` is **not** listed in Files to Modify or Files to Create. I would not add it to the plan silently. I would flag it in the Step 9 scope check and ask the user to approve it, since it is needed for acceptance criterion 1.

Test files (under `migration/tests/` or `tests/`) are also not listed in Files to Create, although Test Requirements need them. These would be flagged for approval the same way.

## Step 7 – Tests

Following the integration-test conventions (real PostgreSQL test DB), with `///` doc comments and given/when/then sections:

1. `/// Verifies the backfill populates supplier values for packages of an SPDX SBOM.`
   - Given: ingest an SPDX fixture whose packages have `supplier: Organization: Acme`, then null out `sbom_package.supplier` to simulate pre-fix data.
   - When: run `m0042_backfill_suppliers::Migration.up()`.
   - Then: `assert_eq!` the exact supplier value for each named package. Do not just count the rows.
2. `/// Verifies CycloneDX SBOMs are untouched by the backfill.`
   - Given: ingest a CycloneDX fixture and record its `sbom_package` rows (supplier values included).
   - When: run the migration.
   - Then: `assert_eq!` that the rows are identical before and after.

These two tests have different setup and assertions, so they stay as separate tests rather than being parameterized.

Run: `cargo test -p trustify-migration` and `cargo test -p trustify-module-ingestor`. The crate names would be resolved through `cargo metadata --no-deps`.

## Step 8 – Acceptance Criteria

| Criterion | How it is satisfied |
|---|---|
| Re-processes all SPDX SBOMs and populates suppliers | Keyset loop over every `labels->>'type'='spdx'` sbom, with an update per package |
| CycloneDX not loaded or processed | Filter applied in SQL, so CycloneDX rows never leave the DB (test 2) |
| `suppliers()` made public | `pub fn suppliers` in the ingestor |
| Follows `m0001_initial` pattern | `DeriveMigrationName` + `MigrationTrait` `up`/`down`, registered in `Migrator` |

## Step 9 – Self-Verification

- Scope containment: the expected diff is the 2 listed files plus `migration/src/lib.rs` and the test file(s). The extra files are flagged for approval.
- Query-scope verification: done. See `query-scope.md`. The scope matches the task (SPDX only, filtered at the source).
- Contract: `MigrationTrait` `up` and `down` are both implemented.
- Sibling parity: matches `m0001_initial` structure and naming.
- Cross-module entity: `sbom_package` is written by the ingestor. Check that it uses the same column semantics (supplier string format). A plain UPDATE is used, with no new inserts and so no conflict handling needed.
- Caller-site: `suppliers()` is called with the same argument type as the ingestor's existing call site.
- Data flow: `sbom` (SPDX ids) -> `source_document` bytes -> SPDX parse -> `suppliers()` -> `sbom_package.supplier` UPDATE. The chain is complete.
- Dead parameters: none (no removals).
- CI: run the CONVENTIONS.md commands. Any failure is a hard stop.

## Steps 10–11 – Commit, PR, Jira (simulated)

- Commit: `feat(migration): backfill SPDX package suppliers` with the body `Implements TC-9209` and `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- PR: `gh pr create --base main`. The body includes `Implements [TC-9209](<webUrl>)`, notes the reuse-over-duplication decision for `suppliers()`, and adds `Closes owner/repo#N` if the GitHub Issue field is set.
- Jira: set `customfield_10875` (ADF inlineCard with the PR URL), add a comment (PR link, summary, deviations: `lib.rs` registration and test files), with the footnote, and move the task to In Review.
