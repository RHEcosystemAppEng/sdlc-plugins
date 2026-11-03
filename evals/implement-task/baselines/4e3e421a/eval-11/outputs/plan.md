# Implementation Plan — TC-9209

**Summary**: Re-process all SPDX SBOMs to extract package supplier information
**Repository**: trustify-backend
**Target Branch**: `main` (task branch: `TC-9209`)
**Skill**: /sdlc-workflow:implement-task. This is a dry run, so no repo, Jira, git or Serena calls were made.

---

## Step 0: Project Configuration check

The mock CLAUDE.md (`claude-md-mock.md`) has all three required sections:
- Repository Registry: `trustify-backend`, Serena instance `serena_backend`, path `./`
- Jira Configuration: project key TC, Cloud ID, Feature issue type ID 10142, plus PR field `customfield_10875` and GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<instance>__<tool>`, instance `serena_backend` (rust-analyzer)

Result: valid. Execution continues.

## Step 1: Parse the task

All required sections are present: Repository, Target Branch, Description, Files to Modify, Files to Create, API Changes (none), Implementation Notes, Acceptance Criteria, Test Requirements and Dependencies.
- No Target PR, so this is the default new-branch/new-PR flow.
- No Bookend Type, so this is normal implementation.
- GitHub Issue field (`customfield_10747`): would be read from the fetched issue. If it is empty, skip it.

## Steps 1.5 to 3 (dry run, no calls made)
- 1.5: Fetch comments, find the `[sdlc-workflow] Description digest:` comment and compare digests.
- 2: Dependencies are "None", so there is nothing to check.
- 3: `jira.user_info()`, then assign to the current user, then transition to In Progress.

## Step 4: Understand the code (planned Serena calls on `serena_backend`)

| Call | Purpose |
|---|---|
| `get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")` | Find `fn suppliers(...)` and its neighbours |
| `find_symbol("suppliers", include_body=true)` | Get the exact signature: input type (SPDX package struct) and return type |
| `find_referencing_symbols("suppliers")` | Confirm that changing private to `pub` does not break callers (it only widens visibility) |
| `get_symbols_overview("migration/src/m0001_initial/mod.rs")` and `migration/src/lib.rs` | Learn the migration structure: `DeriveMigrationName`, `MigrationTrait`, `up`/`down`, and how the `Migrator` registers migrations |
| `get_symbols_overview("entity/src/sbom.rs")`, `entity/src/sbom_package.rs` | Confirm the `labels: Json` column, the `sbom_package` PK/FK and whether a `supplier` column exists |
| `search_for_pattern("find_by_sbom_id")` | Locate `SourceDocument::find_by_sbom_id` and its return type |
| `search_for_pattern("labels")` in `common/src/db/query.rs` and `modules/` | Check for an existing JSONB label-filter helper to reuse |
| Read `migration/Cargo.toml` | Check that `trustify-module-ingestor` is already a dependency (the notes say it is) |
| Read `CONVENTIONS.md` | Find naming rules and the CI check commands for Step 9 |

**Docs to check for impact**: `README.md`, `CONVENTIONS.md`, `docs/architecture.md`. I expect no doc change, because this is an internal migration with no API change.

**Conventions to follow (sibling analysis)**:
- Migration modules are named `mNNNN_<snake_name>/mod.rs`, contain `#[derive(DeriveMigrationName)] pub struct Migration;`, and implement `MigrationTrait` with `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>`.
- Errors: inside the migration, map to `DbErr::Custom(...)`, because `MigrationTrait` requires `DbErr`. Elsewhere the codebase uses `Result<T, AppError>` with `.context()`.
- Tests: integration tests run against a real PostgreSQL test database and use `assert_eq!`.

## Step 5: Branch
```
git checkout main && git pull && git checkout -b TC-9209
```

## Step 6: Changes

### 1. Modify `modules/ingestor/src/graph/sbom/mod.rs`
- Change `fn suppliers(...)` to `pub fn suppliers(...)`. The body stays as it is.
- Add a `///` doc comment, for example: `/// Extracts supplier names from an SPDX package entry. Public so data migrations (e.g. m0042_backfill_suppliers) can reuse it.`
- If the function sits in a private submodule, it also has to be reachable from the crate root, for example `pub use` or a `pub mod graph::sbom`. I would confirm the visibility path with `find_symbol`. If that needs a change to `lib.rs` or `graph/mod.rs`, I would raise it as a scope item rather than make the change silently.
- **Reuse over duplication decision**: `migration/Cargo.toml` already depends on `trustify-module-ingestor`, so the function is made `pub` and imported, not copied. This rationale goes in the commit/PR body.

### 2. Create `migration/src/m0042_backfill_suppliers/mod.rs`

Outline:

```rust
use sea_orm::{EntityTrait, QueryFilter, QuerySelect, ConnectionTrait, ActiveModelTrait, Set};
use sea_orm::sea_query::Expr;
use sea_orm_migration::prelude::*;
use trustify_entity::{sbom, sbom_package};
use trustify_module_ingestor::graph::sbom::suppliers;

/// Backfills `sbom_package` supplier values by re-parsing SPDX SBOM source documents.
#[derive(DeriveMigrationName)]
pub struct Migration;

/// Number of SPDX SBOM ids fetched per page, which keeps memory bounded.
const PAGE_SIZE: u64 = 500;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // Query scope: only SPDX SBOMs. CycloneDX documents already have suppliers
        // populated at ingestion, so we filter on labels->>'type' at the DB level
        // and never load them.
        let mut last_id = None;
        loop {
            let mut q = sbom::Entity::find()
                .select_only()
                .column(sbom::Column::SbomId)
                .filter(Expr::cust_with_values("labels->>'type' = $1", ["spdx"]))
                .order_by_asc(sbom::Column::SbomId)
                .limit(PAGE_SIZE);
            if let Some(id) = last_id {
                q = q.filter(sbom::Column::SbomId.gt(id));
            }
            let ids: Vec<Uuid> = q.into_tuple().all(db).await?;
            if ids.is_empty() { break; }

            for id in &ids {
                // Fetch the raw document only for this SPDX SBOM
                let Some(doc) = SourceDocument::find_by_sbom_id(*id, db).await? else {
                    log::warn!("no source document for SPDX sbom {id}; skipping");
                    continue;
                };
                let spdx = parse_spdx(&doc.data)
                    .map_err(|e| DbErr::Custom(format!("parse SPDX {id}: {e}")))?;
                let txn = db.begin().await?;
                for pkg in spdx.package_information.iter() {
                    let supplier = suppliers(pkg);   // reused ingestor logic
                    if supplier.is_empty() { continue; }
                    sbom_package::Entity::update_many()
                        .col_expr(sbom_package::Column::Supplier, Expr::value(supplier.join(", ")))
                        .filter(sbom_package::Column::SbomId.eq(*id))
                        .filter(sbom_package::Column::NodeId.eq(&pkg.package_spdx_identifier))
                        .exec(&txn).await?;
                }
                txn.commit().await?;
            }
            last_id = ids.last().copied();
        }
        Ok(())
    }

    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        // Data backfill only, so there is no schema to revert. Supplier values are
        // left in place because they are correct data.
        Ok(())
    }
}
```

The exact column names (`SbomId`, `NodeId`, `Supplier`), the `suppliers()` return type and the SPDX parse function would be confirmed in Step 4 and adjusted to match.

Guards:
- A missing source document is logged and skipped.
- A package with no supplier is skipped.
- A parse failure stops the migration with `DbErr::Custom`. This follows the sibling pattern. Skipping with a warning is the alternative; I would confirm which the team prefers.

### How the database is queried
1. **Selection (the key query)**: one paged query on `sbom` that filters on the JSONB label in SQL:
   ```sql
   SELECT sbom_id FROM sbom
   WHERE labels->>'type' = 'spdx' AND sbom_id > $last
   ORDER BY sbom_id LIMIT 500;
   ```
   - Only ids are selected, not whole rows. Keyset pagination keeps memory flat.
   - CycloneDX rows never come back to the application.
2. **Source fetch**: `SourceDocument::find_by_sbom_id(id)` is called once per SPDX id. It is never called for CycloneDX.
3. **Update**: `UPDATE sbom_package SET supplier = $1 WHERE sbom_id = $2 AND node_id = $3`, run in a transaction for each SBOM.
4. **Optional index**: an expression index such as `CREATE INDEX ON sbom ((labels->>'type'))` would speed up the filter. That would be a schema change in another file, so I would raise it with the user rather than add it.

### 3. Scope items to raise (not in Files to Modify/Create)
- `migration/src/lib.rs`: the new module has to be declared (`mod m0042_backfill_suppliers;`) and added to `Migrator::migrations()`. Without that, the migration never runs. This needs user approval in Step 9 scope containment.
- Test file location: the task asks for tests but lists no test file. Options are an inline `#[cfg(test)] mod tests` inside `m0042_backfill_suppliers/mod.rs` (in scope) or a new file under `tests/`. I would use the in-scope inline option unless the user prefers otherwise.
- If `sbom_package` has no `supplier` column, a schema change would be needed. The task implies the column exists ("update the corresponding `sbom_package` records"), and I would confirm this in Step 4.

## Step 7: Tests
Follow the integration-test convention: real PostgreSQL test DB, `assert_eq!` on values, a `///` doc comment on each test, and Given/When/Then comments.

```rust
/// Verifies the migration populates supplier values for packages of an SPDX SBOM.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn backfill_populates_spdx_suppliers(ctx: &TrustifyContext) -> anyhow::Result<()> {
    // Given an SPDX SBOM ingested with supplier values cleared
    // When the m0042 migration's up() runs
    // Then each sbom_package row has the expected supplier string
    assert_eq!(pkg.supplier.as_deref(), Some("Organization: Red Hat"));
}

/// Verifies CycloneDX SBOMs are neither loaded nor modified by the migration.
async fn backfill_skips_cyclonedx(ctx) {
    // Given a CycloneDX SBOM whose sbom_package suppliers are snapshotted
    // When the migration runs
    // Then the supplier values are unchanged (compare the full before/after vectors)
}
```

The two tests differ in setup and assertions, so they stay as separate functions rather than parameterized cases. Run `cargo test -p trustify-migration` and `cargo test -p trustify-module-ingestor`, with crate names resolved through `cargo metadata`.

## Step 8: Acceptance criteria
| Criterion | How it is met |
|---|---|
| Re-processes all SPDX SBOMs and populates suppliers | Paged loop over every `labels->>'type'='spdx'` row, then update of `sbom_package` |
| CycloneDX not loaded or processed | Filtered out in SQL; `find_by_sbom_id` is never called for them; covered by a test |
| `suppliers()` made public | `pub fn suppliers` in the ingestor |
| Follows the `m0001_initial` pattern | `DeriveMigrationName` + `MigrationTrait` `up`/`down` |

## Step 9: Self-verification
- Scope containment: the expected diff is the two listed files, plus `migration/src/lib.rs`, which is flagged for approval.
- Query-scope verification: done. See `query-scope.md`.
- Data flow: `sbom` (SPDX ids) → `source_document` bytes → SPDX parse → `suppliers()` → `sbom_package.supplier`. Every stage is connected.
- Contract: `MigrationTrait` requires `up` and `down`; both are implemented.
- Sibling parity: matches `m0001_initial`.
- Cross-module entity: the ingestor also writes `sbom_package`. Updates are transactional per SBOM and do not insert rows, so there are no conflict cases.
- Caller-site: `find_by_sbom_id` is used the same way as its existing callers.
- Run the CI commands from `CONVENTIONS.md` (for example `cargo fmt --check`, `cargo clippy`). Any failure is a hard stop.

## Steps 10 and 11
- Commit: `feat(migration): backfill SPDX package suppliers` with the body explaining the reuse decision and the footer `Implements TC-9209`, plus `--trailer="Assisted-by: Claude Code"`.
- PR: `gh pr create --base main`, with `Implements [TC-9209](<webUrl>)` in the description.
- Jira: set `customfield_10875` to the PR URL as an ADF inlineCard, add a comment with the footnote and transition to In Review.
