# Implementation Plan — TC-9209

**Summary**: Re-process all SPDX SBOMs to extract package supplier information
**Repository**: trustify-backend
**Mode**: default (no Target PR, no Bookend Type) — branch `TC-9209` from `main`, PR -> `main`

> Simulated run. No repository files, git, Jira or Serena were touched. Each external
> operation below is described, not executed.

## Step 0 – Project Configuration validation

Checked against `claude-md-mock.md`:

- Repository Registry: present, `trustify-backend` -> Serena instance `serena_backend`, path `./`. **PASS**
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142` all present. **PASS**
- Code Intelligence: present, naming convention `mcp__<serena-instance>__<tool>`. **PASS**

## Step 1 – Parse task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Files to Modify | `modules/ingestor/src/graph/sbom/mod.rs` |
| Files to Create | `migration/src/m0042_backfill_suppliers/mod.rs` |
| API Changes | none |
| Target PR / Bookend Type | none, so mode is **default** |
| Dependencies | none |
| GitHub Issue (customfield_10747) | read from the issue; if it is empty, skip it |

All required sections are present. The task is well-formed.

## Steps 1.5 / 2 / 3 – Jira (simulated)

- 1.5: fetch comments and look for a `[sdlc-workflow] Description digest:` comment. If one exists, compare it with `python3 scripts/sha256-digest.py`. If none exists, warn and continue.
- 2: no dependencies.
- 3: `jira.user_info()`, then assign TC-9209 to the current user, then transition to **In Progress**.

## Step 4 – Understand the code (planned Serena calls on `serena_backend`)

- `get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")`, then `find_symbol("suppliers", include_body=true)` to read the signature and the SPDX supplier parsing logic.
- `find_referencing_symbols("suppliers")` to confirm that making it `pub` does not change any caller.
- `find_symbol` on `migration/src/m0001_initial/mod.rs` (the `Migration` struct, `MigrationName` and `MigrationTrait::up`) to get the migration pattern.
- `find_symbol` on `migration/src/lib.rs` (`Migrator::migrations()`) to see how migrations are registered.
- `get_symbols_overview("entity/src/sbom.rs")` to confirm the `labels: Json` column. Same for `entity/src/sbom_package.rs` to find the supplier column and the primary key (`sbom_id`, `package_id`/node id).
- `search_for_pattern("find_by_sbom_id")` to locate `SourceDocument::find_by_sbom_id`.
- `search_for_pattern("labels")` across `common/src/db/query.rs` and the services, to find any existing JSON label filter helper to reuse.
- Check `migration/Cargo.toml` to confirm it depends on `trustify-module-ingestor`, as the task says.
- Read `CONVENTIONS.md` at the repo root and extract its CI check commands for Step 9 check 14.
- Documentation candidates: `README.md`, `docs/architecture.md`. No public API changes, so these are unlikely to be affected.

Conventions recorded from repo-backend.md: SeaORM for DB access; `Result<T, AppError>` with `.context()` in app code (migrations use `DbErr`, as in `m0001_initial`); integration tests in `tests/` against a real PostgreSQL database.

## Step 5 – Branch (simulated)

```
git checkout main && git pull && git checkout -b TC-9209
```

## Step 6 – Changes

### Modify: `modules/ingestor/src/graph/sbom/mod.rs`

- Change `fn suppliers(...)` to `pub fn suppliers(...)` and leave the signature and body unchanged. This follows the Reuse rule "exists but not exported": the dependency already exists, so we export it and do not duplicate the logic.
- Add a `///` doc comment, e.g. `/// Extracts supplier names from the SPDX package entries of a parsed SPDX document.`
- If `graph::sbom` is not reachable from the crate root, it must also be re-exported or made `pub mod` in `modules/ingestor/src/graph/mod.rs` / `lib.rs`. That file is out of scope, so it would be flagged in Step 9 check 1 for user approval.

### Create: `migration/src/m0042_backfill_suppliers/mod.rs`

Structure follows `m0001_initial`:

```rust
//! Backfills `sbom_package` supplier values for SPDX SBOMs ingested before
//! supplier extraction was supported.

use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect, ConnectionTrait,
              sea_query::Expr, TransactionTrait};
use sea_orm_migration::prelude::*;
use trustify_entity::{sbom, sbom_package};
use trustify_module_ingestor::graph::sbom::suppliers;

#[derive(DeriveMigrationName)]
pub struct Migration;

const BATCH_SIZE: u64 = 500;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Re-parses every SPDX SBOM source document and writes extracted suppliers
    /// onto the matching `sbom_package` rows. CycloneDX documents are never loaded.
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();
        let mut last_id = None;
        loop {
            // Query scope: only SPDX SBOMs (labels->>'type' = 'spdx'), filtered in SQL,
            // keyset-paginated by id. Only the id column is selected.
            let mut q = sbom::Entity::find()
                .select_only()
                .column(sbom::Column::SbomId)
                .filter(Expr::cust(r#"labels @> '{"type":"spdx"}'::jsonb"#))
                .order_by_asc(sbom::Column::SbomId)
                .limit(BATCH_SIZE);
            if let Some(id) = last_id {
                q = q.filter(sbom::Column::SbomId.gt(id));
            }
            let ids: Vec<Uuid> = q.into_tuple().all(db).await?;
            if ids.is_empty() { break; }

            for id in &ids {
                let Some(doc) = SourceDocument::find_by_sbom_id(*id).one(db).await? else {
                    // Defensive: SBOM without a stored source document; skip it.
                    continue;
                };
                let spdx = parse_spdx(&doc.data)   // same parser the ingestor uses
                    .map_err(|e| DbErr::Migration(format!("sbom {id}: {e}")))?;
                let txn = db.begin().await?;
                for (package_ref, supplier) in suppliers(&spdx) {
                    sbom_package::Entity::update_many()
                        .col_expr(sbom_package::Column::Supplier, Expr::value(supplier))
                        .filter(sbom_package::Column::SbomId.eq(*id))
                        .filter(sbom_package::Column::NodeId.eq(package_ref))
                        .exec(&txn).await?;
                }
                txn.commit().await?;
            }
            last_id = ids.last().copied();
        }
        Ok(())
    }

    /// Data backfill only; no schema to revert. Supplier values are left in place.
    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        Ok(())
    }
}
```

Notes:
- Exact column names (`SbomId`, `NodeId`, `Supplier`), the parser entry point and the return shape of `suppliers()` will be confirmed in Step 4. The sketch adapts to what Serena reports.
- Each SBOM is updated in its own transaction, so a failure part-way leaves earlier SBOMs fully updated. The update is idempotent, so re-running the migration is safe.
- `labels @> '{"type":"spdx"}'` is used instead of `labels->>'type' = 'spdx'` because a GIN index on `labels` can serve containment. The two are semantically equivalent here (see query-scope.md).
- Guard: `find_by_sbom_id` returning `None` skips the SBOM instead of panicking. An SPDX package with no `supplier` field yields no update, so no NULLs are written over existing values.

### Registration: `migration/src/lib.rs` (out of scope, flagged)

The migration only runs if it is added to `Migrator::migrations()` (`Box::new(m0042_backfill_suppliers::Migration)`) and declared with `mod m0042_backfill_suppliers;`. This file is not in Files to Modify, so it is a Step 9 scope flag that needs explicit user approval. Without it the data-flow trace (check 11) is incomplete.

## Step 7 – Tests

Planned location: the migration crate's test module, or `tests/` following the repo's real-DB integration pattern (to be confirmed in Step 4). That location is not listed in the task's files either, so it is flagged under scope containment.

```rust
/// Verifies that the backfill populates supplier values for packages of an SPDX SBOM.
#[tokio::test]
async fn backfill_populates_spdx_suppliers() {
    // Given an SPDX SBOM ingested with supplier values stripped from sbom_package
    // When the m0042 migration runs
    // Then each package's supplier equals the value in the SPDX source,
    //   e.g. assert_eq!(pkg.supplier.as_deref(), Some("Organization: Red Hat"))
}

/// Verifies that CycloneDX SBOM packages are untouched by the backfill.
#[tokio::test]
async fn backfill_skips_cyclonedx() {
    // Given a CycloneDX SBOM with known sbom_package rows (snapshot before)
    // When the m0042 migration runs
    // Then the rows equal the snapshot: assert_eq!(after, before)
}
```

The assertions compare values, not lengths. There are two distinct behaviours, so these are separate tests rather than a parameterized one.

## Step 8 – Acceptance criteria

| Criterion | How it is met |
|---|---|
| Re-processes all SPDX SBOMs and populates suppliers | Keyset loop over every `labels @> {"type":"spdx"}` SBOM; test 1 |
| CycloneDX not loaded or processed | The SQL filter excludes them before any row or source document is fetched; test 2 |
| `suppliers()` made public | `pub fn suppliers` in the ingestor |
| Follows the `m0001_initial` pattern | `DeriveMigrationName` + `MigrationTrait::up/down` |

## Step 9 – Self-verification (expected results)

| # | Check | Result |
|---|---|---|
| 1 | Scope containment | FLAGGED: `migration/src/lib.rs` (registration), the test file location, and possibly the ingestor `graph/mod.rs` visibility. Each needs user approval |
| 3 | Sensitive patterns | PASS (expected) |
| 5 | Duplication | PASS: reuses `suppliers()` and does not reimplement it |
| 10 | Cross-section references | PASS: paths are consistent between Files to Modify/Create and Implementation Notes |
| 11 | Data-flow trace | source_document bytes -> SPDX parse -> `suppliers()` -> `sbom_package.supplier` UPDATE. Complete once lib.rs registration is approved |
| 12 | Query scope | PASS: the batch query filters to SPDX at the DB level (details in query-scope.md) |
| 13 | Contract & sibling parity | Contract: `MigrationTrait` up/down implemented. Sibling: matches m0001. Cross-module entity: `sbom_package` is written by the ingestor, so the plan matches its column semantics and uses plain updates (no inserts, no conflict handling needed). Caller-site: `suppliers()` is called the same way as in the ingestor |
| 14 | CI checks | Run the commands from CONVENTIONS.md (e.g. `cargo fmt --check`, `cargo clippy`). Hard stop on failure |
| 15 | Module tests (Rust) | Resolve crates via `cargo metadata`, then `cargo test -p trustify-module-ingestor` and `cargo test -p migration` (names as reported by metadata) |

## Steps 10–11 (simulated)

- Commit: `feat(migration): backfill SPDX package suppliers` with body `Implements TC-9209` and `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- Check for an `upstream` remote. Then `gh pr create --base main`, with the description `Implements [TC-9209](<webUrl>)` and `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.
- Jira: set `customfield_10875` to the PR URL (ADF inlineCard). Add a comment with the PR link, a summary and the deviations (the lib.rs registration), ending with the implement-task footnote. Transition to **In Review**.
