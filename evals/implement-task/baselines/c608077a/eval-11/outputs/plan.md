# Implementation Plan — TC-9209

**Summary**: Re-process all SPDX SBOMs to extract package supplier information
**Repository**: trustify-backend (Serena instance: `serena_backend`)
**Target Branch**: `main` -> task branch `TC-9209`

---

## Step 0 – Project Configuration validation

The mock CLAUDE.md contains every required section:
- Repository Registry: `trustify-backend | Rust backend service | serena_backend | ./`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142` (plus the Git PR field `customfield_10875` and the GitHub Issue field `customfield_10747`)
- Code Intelligence: the `mcp__<serena-instance>__<tool>` naming convention, with instance `serena_backend` (rust-analyzer)

Result: **PASS**. Execution continues.

## Step 1 – Task parsing

| Section | Present | Value |
|---|---|---|
| Repository | yes | trustify-backend |
| Target Branch | yes | main |
| Description | yes | Data migration that re-processes **SPDX** SBOMs only and backfills `sbom_package` supplier values |
| Files to Modify | yes | `modules/ingestor/src/graph/sbom/mod.rs` |
| Files to Create | yes | `migration/src/m0042_backfill_suppliers/mod.rs` |
| API Changes | yes | none |
| Implementation Notes | yes | `labels` jsonb with `{"type":"spdx"}` / `{"type":"cyclonedx"}`; reuse `suppliers()`; `m0001_initial` pattern; `SourceDocument::find_by_sbom_id` |
| Acceptance Criteria | yes | 4 items |
| Test Requirements | yes | 2 tests |
| Dependencies | yes | None |
| Target PR / Bookend Type | no | default flow |

- GitHub Issue field (`customfield_10747`): would be read from the issue. If it is empty, this step is skipped silently.
- Step 1.5 (digest check): would fetch comments and verify the `[sdlc-workflow] Description digest:` comment. Not run in this eval.
- Step 2: no dependencies to check.
- Step 3: would assign the issue to the current user and move it to In Progress. Not run in this eval.

## Step 4 – Code understanding (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")`: locate `fn suppliers`.
- `mcp__serena_backend__find_symbol("suppliers", include_body=true)`: confirm its signature (input: the parsed SPDX package/document; output: supplier strings).
- `mcp__serena_backend__find_referencing_symbols("suppliers")`: list the current callers. Making the function `pub` only widens visibility, so no caller breaks.
- `mcp__serena_backend__find_symbol("MigrationTrait")` in `migration/src/m0001_initial/mod.rs`, plus `migration/src/lib.rs`: learn the migration structure and how migrations are registered.
- `entity/src/sbom.rs`: confirm the `labels: Json` column. `entity/src/sbom_package.rs`: confirm the supplier column name and type.
- `search_for_pattern("find_by_sbom_id")`: confirm the `SourceDocument` helper exists.
- `search_for_pattern("labels")` across modules: check for an existing label-filter helper (for example in `common/src/db/query.rs`) to reuse before writing a new filter expression.
- Read `CONVENTIONS.md` at the repo root to get the CI check commands (fmt, clippy, check, test) for Step 9.
- Migration crate deps: `migration/Cargo.toml` already depends on `trustify-module-ingestor`, so making the function public is the right choice and duplicating it is not needed (see "Reuse over duplication").

## Step 6 – Changes

### 1. Modify `modules/ingestor/src/graph/sbom/mod.rs`
- Change `fn suppliers(...)` to `pub fn suppliers(...)`. Do not change its logic.
- Add a `///` doc comment, e.g. `/// Extracts supplier names from an SPDX package entry; reused by the m0042 supplier backfill migration.`
- If the enclosing `graph::sbom` module path is not publicly reachable from the crate root, the re-export is needed for the migration to import it. Check `lib.rs` / `graph/mod.rs` visibility. Those files are **out of scope**, so if a change is needed there, flag it for approval in Step 9 rather than editing silently.

### 2. Create `migration/src/m0042_backfill_suppliers/mod.rs`
Follow the `m0001_initial` structure:

```rust
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect, sea_query::Expr};
use sea_orm_migration::prelude::*;
use trustify_entity::{sbom, sbom_package};
use trustify_module_ingestor::graph::sbom::suppliers;

/// Backfills package supplier information for SPDX SBOMs that were ingested
/// before supplier extraction was supported.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // Query scope: only SPDX SBOMs. CycloneDX already has suppliers populated
        // at ingestion and vastly outnumbers SPDX in production, so filter at the DB.
        let spdx_ids: Vec<Uuid> = sbom::Entity::find()
            .select_only()
            .column(sbom::Column::SbomId)
            .filter(Expr::cust("labels->>'type' = 'spdx'"))
            .into_tuple()
            .all(db)
            .await?;

        for sbom_id in spdx_ids {
            // fetch raw bytes for this SBOM only
            let Some(doc) = SourceDocument::find_by_sbom_id(sbom_id, db).await? else {
                log::warn!("no source document for SPDX SBOM {sbom_id}; skipping");
                continue;
            };
            let spdx = parse_spdx(&doc.data)?; // existing SPDX parser used by ingestor
            for pkg in spdx.package_information.iter() {
                let supplier = suppliers(pkg); // reused, now-public helper
                // UPDATE sbom_package SET supplier = $1
                //  WHERE sbom_id = $2 AND <package id match>
                sbom_package::Entity::update_many()
                    .col_expr(sbom_package::Column::Supplier, Expr::value(supplier))
                    .filter(sbom_package::Column::SbomId.eq(sbom_id))
                    .filter(/* package identifier match from SPDX package ref */)
                    .exec(db)
                    .await?;
            }
        }
        Ok(())
    }

    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        // Data-only backfill; nothing to revert structurally.
        Ok(())
    }
}
```

Design notes:
- **Database query for the migration**: the SPDX subset is selected in SQL with `WHERE labels->>'type' = 'spdx'` on the `sbom` table. Only the `sbom_id` column is projected, and source documents are fetched one SBOM at a time with `SourceDocument::find_by_sbom_id`. CycloneDX rows are never loaded and their source documents are never fetched. Equivalent SQL:
  ```sql
  SELECT sbom_id FROM sbom WHERE labels->>'type' = 'spdx';
  ```
  If there are many SPDX ids, page through them (`ORDER BY sbom_id LIMIT/OFFSET`, or a keyset on `sbom_id`) so the result set is never held in memory at once. Updates touch only `sbom_package` rows whose `sbom_id` is in the SPDX set, so CycloneDX `sbom_package` rows are untouched.
- Matching the parse function, package identifier column, and supplier column names must be confirmed in Step 4 against `entity/src/sbom_package.rs` and the ingestor's SPDX parse path. Reuse the ingestor's parser and do not write a new one.
- Error handling and logging should match the migration siblings. Missing source documents are logged and skipped rather than aborting the whole migration (confirm against sibling conventions).
- Every new struct and function gets a `///` doc comment.

### Out-of-scope files that will likely need changes (flag in Step 9 and do not edit without approval)
- `migration/src/lib.rs`: the new `mod m0042_backfill_suppliers;` must be declared and `Box::new(m0042_backfill_suppliers::Migration)` added to the `Migrator::migrations()` vec. Without this the migration never runs. It is not listed in Files to Modify, so ask the user to approve it.
- Test location: the Test Requirements ask for 2 tests but no test file is listed. Option A is an inline `#[cfg(test)] mod tests` inside `m0042_backfill_suppliers/mod.rs`, which is in scope. Option B is a new file under `tests/` or `migration/tests/`, which is out of scope and would need approval. Prefer Option A if sibling migrations allow it.
- Possibly `modules/ingestor/src/graph/mod.rs` / `lib.rs`, if the `sbom` submodule is not publicly exported.

## Step 7 – Tests (in the migration module, using the test-DB pattern)

```rust
/// Verifies the migration populates supplier values on sbom_package rows of an SPDX SBOM.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn backfill_populates_spdx_suppliers(ctx: &TrustifyContext) -> anyhow::Result<()> {
    // Given an SPDX SBOM ingested with supplier values cleared
    // When the m0042 migration runs
    // Then each sbom_package row has the exact expected supplier (value-based assert_eq!)
}

/// Verifies CycloneDX SBOMs are untouched (not loaded/updated) by the migration.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn backfill_skips_cyclonedx(ctx: &TrustifyContext) -> anyhow::Result<()> {
    // Given a CycloneDX SBOM with known supplier values (and one with a sentinel/NULL value)
    // When the m0042 migration runs
    // Then its sbom_package supplier values are exactly unchanged (snapshot compare before/after)
}
```

- Assertions compare actual supplier values, not row counts.
- Each test has a `///` doc comment and given/when/then section comments.
- The two cases differ in setup and assertions, so they are separate tests, not a parameterized test.
- Run with `cargo test -p trustify-migration` and `cargo test -p trustify-module-ingestor`. Resolve the crate names with `cargo metadata`.

## Step 8 – Acceptance criteria mapping

| AC | Satisfied by |
|---|---|
| Re-processes all SPDX SBOMs and populates supplier fields | The `labels->>'type' = 'spdx'` query plus a loop over every result; test 1 |
| CycloneDX documents not loaded or processed | The DB-level filter means CycloneDX rows are never selected and their source docs are never fetched; test 2 |
| `suppliers()` made public | `pub fn suppliers` in the ingestor |
| Follows `m0001_initial` pattern | `DeriveMigrationName` + `MigrationTrait::up/down` |

## Step 9 – Self-verification highlights
- Scope containment: the expected diff is the 2 listed files plus `migration/src/lib.rs` (flagged for approval).
- Query-scope verification: see `query-scope.md`. Filtered at the source and **PASS**.
- Data flow: `sbom` (SPDX filter) -> `source_document` bytes -> SPDX parse -> `suppliers()` -> `UPDATE sbom_package`. All stages connect.
- Contract and sibling parity:
  - Contract: `MigrationTrait` gets both `up` and `down`.
  - Sibling parity: matches `m0001_initial`.
  - Cross-module entity: `sbom_package` is also written by the ingestor, so use the same column semantics and no conflicting inserts (update only).
  - Caller-site: `suppliers()` is called with the same argument types as the ingestor's existing caller.
- CI: run the CONVENTIONS.md checks (fmt, clippy, check, tests). Any failure is a hard stop.

## Steps 10–11 (not executed in eval)
- Commit: `feat(migration): backfill package suppliers for SPDX SBOMs` with footer `Implements TC-9209` and trailer `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- Run `gh pr create --base main` with `Implements [TC-9209](<webUrl>)` in the body.
- Set `customfield_10875` to the PR URL (ADF inlineCard), add a Jira comment with the summary and deviations (lib.rs registration), and transition the issue to In Review.
