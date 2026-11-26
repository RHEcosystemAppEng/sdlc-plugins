# Implementation Plan — TC-9206: Add SBOM supplier extraction to data migration

Produced by following `plugins/sdlc-workflow/skills/implement-task/SKILL.md`. No repository files were changed and no external tools (Jira, git, Serena) were called. Where the skill would call one, this plan says what would be done instead.

## Step 0 – Project Configuration check (claude-md-mock.md)

| Section | Status |
|---|---|
| Repository Registry | Present: `trustify-backend`, Serena instance `serena_backend`, path `./` |
| Jira Configuration | Present: Project key TC, Cloud ID, Feature issue type 10142, PR field `customfield_10875`, GitHub Issue field `customfield_10747` |
| Code Intelligence | Present: `mcp__<instance>__<tool>` naming, `serena_backend` (rust-analyzer) |

The check passes, so I proceed.

## Step 1 – Parse task

| Field | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR / Bookend Type | none (default flow) |
| Files to Modify | `migration/src/m0002_supplier/mod.rs`, `modules/ingestor/src/graph/sbom/mod.rs` |
| Files to Create | `migration/src/m0002_supplier/test.rs` |
| API Changes | none |
| Dependencies | none |
| GitHub Issue (customfield_10747) | read from the issue. If set, add `Closes owner/repo#N` to the PR body only |

All required sections are present.

## Steps 1.5 – 3 (would run, simulated here)

- **1.5:** Fetch comments, find the latest `[sdlc-workflow] Description digest:` comment, compute the digest with `scripts/sha256-digest.py` and compare. If no digest comment exists, warn and continue.
- **2:** There are no dependencies to check.
- **3:** `jira.user_info()`, assign TC-9206 to the current user, then transition it to In Progress.

## Step 4 – Understand the code (`serena_backend`)

1. `get_symbols_overview` on `modules/ingestor/src/graph/sbom/mod.rs`. Then `find_symbol(include_body=true)` for `describing_packages`, `suppliers`, `Sbom`, `PackageRef` and `SupplierInfo`, to confirm their signatures and see where each type is defined.
2. `find_referencing_symbols` on `describing_packages` and `suppliers` to list existing internal callers. Widening visibility does not affect them, but this confirms nothing else changes.
3. Confirm the module path is public: check `modules/ingestor/src/lib.rs` for `pub mod graph;` and `graph/mod.rs` for `pub mod sbom;`.
4. Read `migration/Cargo.toml` to confirm `trustify-module-ingestor = { path = "../modules/ingestor" }`. This decides between reuse and duplication (see reuse-decision.md).
5. Convention analysis on sibling `migration/src/m0001_initial/mod.rs` and `migration/src/lib.rs`. Note the `MigrationTrait` / `DeriveMigrationName` structure, how `up`/`down` are written, how the `Migrator` registers migrations, and the error style (`DbErr`).
6. Read `CONVENTIONS.md` at the repo root and extract CI check commands (for example `cargo fmt --check`, `cargo clippy`) and any code generation commands, for Step 9.
7. Documentation files: `README.md`, `docs/architecture.md`. These need no changes unless they document migrations or the ingestor's public API.
8. Symbol deduplication: grep the workspace for `sbom_supplier`, `SupplierInfo` and `supplier`. This confirms there is no existing entity or helper for supplier extraction to reuse, and whether a `sbom_supplier` entity or table definition already exists.

### Discrepancies to flag to the user (repo-backend.md versus the task)

- **`migration/src/m0002_supplier/mod.rs` does not exist in the repository tree.** Only `m0001_initial/` exists, yet the task lists the file under *Files to Modify*. I would ask whether the module should be created from scratch (treating it as a create) or whether it exists on a newer `main`.
- **Registering the migration:** a new migration module must be added to `migration/src/lib.rs` (`mod m0002_supplier;` plus an entry in `Migrator::migrations()`). `lib.rs` is not in Files to Modify, so I would flag it under scope containment rather than edit it silently.
- **No `sbom_supplier` entity** exists in `entity/src/`. The plan defines the table inside the migration with a SeaQuery `Table::create()` / `Iden` enum, which keeps it in scope. If a SeaORM entity is wanted, that is a separate, out-of-scope file.
- If `pub mod graph` / `pub mod sbom` or the signature types are private in files outside scope, that needs user approval too (see reuse-decision.md).

## Step 5 – Branch

```
git checkout main && git pull && git checkout -b TC-9206
```

## Step 6 – Changes per file

### 1. `modules/ingestor/src/graph/sbom/mod.rs` (modify)

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(...)`.
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(...)`.
- Add `///` doc comments to both. For example: `/// Returns the packages this SBOM declares it describes (its top-level subjects).` and `/// Extracts supplier information declared in the SBOM metadata; returns an empty Vec if none.`
- If `Sbom`, `PackageRef` or `SupplierInfo` are defined in this file and are not `pub`, make them `pub` (with doc comments) to avoid `private type in public interface` errors.
- Function bodies and signatures do not change, so there is no behaviour change for the ingestor.
- Edit with Serena `replace_symbol_body`, or Edit on the signature line.

### 2. `migration/src/m0002_supplier/mod.rs` (modify, or create if confirmed missing)

Follow the `m0001_initial` sibling pattern:

```rust
use sea_orm_migration::prelude::*;
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};

/// Migration that creates `sbom_supplier` and backfills it from already-ingested SBOMs.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // 1. create sbom_supplier table (id, sbom_id FK -> sbom ON DELETE CASCADE, package_ref, supplier name/fields)
        // 2. backfill: for every stored SBOM, load + parse the document, then
        //    for each described package and each supplier from suppliers(&sbom),
        //    insert a row
        Ok(())
    }
    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // drop sbom_supplier
    }
}

/// Pure helper: maps one parsed SBOM to the supplier rows to insert (unit-testable without a DB).
pub(crate) fn supplier_rows(sbom_id: Uuid, sbom: &Sbom) -> Vec<SupplierRow> { ... }

#[cfg(test)]
mod test;
```

Key points:

- **Reuse:** `describing_packages()` and `suppliers()` are imported from `trustify_module_ingestor` and never reimplemented. This satisfies the acceptance criterion "reuses existing ingestor logic".
- **A pure `supplier_rows` helper** separates extraction from database I/O, so the unit tests in `test.rs` need no database.
- **Defensive access:** the parsed SBOM comes from another crate. An empty `Vec` from `suppliers()` produces no rows. If an SBOM document is missing or fails to parse, the plan follows the sibling migration's error style: propagate it as `DbErr::Custom` with context. That `DbErr::Custom` is a placeholder to confirm against m0001 and CONVENTIONS.md. Skipping with a `log::warn!` is the other option, and which one to use would be confirmed with the user.
- **Query scope:** the task says "all ingested SBOMs", so iterating every `sbom` row is intentional. The query pages or streams through rows instead of loading every document into memory, and a comment explains why it is broad.
- **Idempotency:** inserts use `ON CONFLICT DO NOTHING`, matching the ingestor's conflict handling (cross-module entity parity).
- **Docs:** every new struct and function gets a `///` comment.

### 3. `migration/src/m0002_supplier/test.rs` (create)

The tests follow the Test Requirements. They exercise the pure `supplier_rows` helper, which in turn calls the reused ingestor functions, so they need no database. Each test gets a `///` doc comment and Given/When/Then sections:

```rust
use super::*;

/// Verifies that suppliers declared in a sample SBOM are extracted into supplier rows.
#[test]
fn extracts_suppliers_from_sample_sbom() {
    // Given an SBOM describing one package with supplier "Acme Corp"
    // When computing supplier rows
    // Then rows contain exactly that sbom_id / package / "Acme Corp" (value-based assert_eq! on the row vector)
}

/// Verifies that an SBOM with no supplier metadata yields no supplier rows.
#[test]
fn sbom_without_suppliers_produces_no_rows() {
    // Given an SBOM with no supplier metadata
    // When computing supplier rows
    // Then the result is empty
    assert_eq!(rows, vec![]);
}
```

- The first test asserts on actual values (supplier name, package ref, sbom id), not only on length.
- The two cases differ in setup and expectation, so they stay separate tests rather than using `rstest`, which the repo does not appear to use.
- Optionally, an integration test against the real PostgreSQL test DB (the repo's convention in `tests/`) could check that the `sbom_supplier` table is populated. That lives in an out-of-scope file, so I would only propose it.

## Step 7 – Tests

`cargo test -p trustify-module-ingestor` and `cargo test -p <migration package name from cargo metadata>`.

## Step 8 – Acceptance criteria

| Criterion | How it is met |
|---|---|
| Extracts supplier info from all ingested SBOMs | `up()` backfill iterates every `sbom` row |
| Reuses ingestor logic | Imports `pub` `describing_packages` / `suppliers`, with no copies |
| `sbom_supplier` populated correctly | Table created and rows inserted in `up()`. Row mapping is covered by `test.rs` |

## Step 9 – Self-verification

- **Scope containment:** the expected diff touches the 3 listed files. `migration/src/lib.rs` (registering the migration) and any `pub mod` / type-visibility edits outside `graph/sbom/mod.rs` need explicit user approval.
- **Duplication check:** grep the migration crate for any reimplementation of the supplier or describing-package parsing. There should be none.
- **Sensitive patterns:** none expected.
- **CI:** run the CONVENTIONS.md checks (fmt, clippy, and so on). Any failure is a hard stop.
- **Rust module tests:** `cargo test -p` for both the ingestor and migration crates, resolving package names with `cargo metadata`.
- **Data-flow trace:** stored SBOM → parse to `Sbom` → `describing_packages` / `suppliers` → `supplier_rows` → INSERT into `sbom_supplier`.
- **Contract and sibling parity:** `MigrationTrait` `up` and `down` are both implemented. The structure matches m0001. Conflict handling matches the ingestor.

## Step 10 – Commit and PR

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): extract SBOM suppliers into sbom_supplier table

Make describing_packages() and suppliers() in trustify-module-ingestor
public and reuse them from the m0002_supplier migration instead of
duplicating the logic; migration already depends on the ingestor crate,
so no new dependency is introduced.

Implements TC-9206"
```

Do fork detection, then `gh pr create --base main`. The PR body includes `Implements [TC-9206](<webUrl>)`, a "Reuse decision" section, and `Closes …` if a GitHub issue is linked.

## Step 11 – Jira

Set `customfield_10875` to the PR URL as an ADF inlineCard. Add a comment covering the PR link, a summary, and the deviations or flags (m0002 module did not exist, `lib.rs` registration), ending with the implement-task footnote. Transition to In Review.
