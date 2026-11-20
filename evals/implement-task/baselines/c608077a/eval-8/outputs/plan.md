# Implementation Plan: TC-9206 — Add SBOM supplier extraction to data migration

## Step 0 – Project Configuration validation

The mock CLAUDE.md has every section this skill requires:
- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142 (plus Git PR field `customfield_10875` and GitHub Issue field `customfield_10747`)
- Code Intelligence: naming convention `mcp__<instance>__<tool>` and instance `serena_backend` (rust-analyzer; first indexing may take 30-60 s)

Validation passes, so the skill continues.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR / Bookend Type | none (default flow) |
| Dependencies | None (Step 2 has nothing to check) |
| Files to Modify | `migration/src/m0002_supplier/mod.rs`, `modules/ingestor/src/graph/sbom/mod.rs` |
| Files to Create | `migration/src/m0002_supplier/test.rs` |

All required sections are present. Step 1.5 (digest check), Step 3 (assign, In Progress) and the Jira steps would normally run. They are skipped here because this eval does not allow external calls.

## Step 4 – Code understanding (what I would inspect with `serena_backend`)

- `get_symbols_overview` on `modules/ingestor/src/graph/sbom/mod.rs`, then `find_symbol(include_body=true)` on `describing_packages`, `suppliers`, `Sbom`, `PackageRef` and `SupplierInfo`. This confirms the signatures and shows whether the types are already `pub`.
- `find_referencing_symbols` on `describing_packages` and `suppliers` to list callers inside the ingestor. Only visibility changes, so these callers are not affected.
- Check module visibility in `modules/ingestor/src/lib.rs` (`pub mod graph`) and `graph/mod.rs` (`pub mod sbom`).
- Read `migration/Cargo.toml` to confirm the dependency on `trustify-module-ingestor`.
- Siblings for conventions: `migration/src/lib.rs` (the `Migrator` list of migrations) and `migration/src/m0001_initial/mod.rs` (the `MigrationTrait` impl, `up`/`down` style, error type).
- `CONVENTIONS.md` at the repo root: read it, and extract the CI check commands and any codegen commands for Step 9.
- Search the `entity/` crate for an `sbom_supplier` entity (`search_for_pattern "sbom_supplier"`).

### Discrepancies found while parsing (to raise with the user)

1. **`migration/src/m0002_supplier/mod.rs` is listed under Files to Modify, but it does not exist** in the repository tree. Only `m0001_initial/` exists. I would point this out (Step 9, cross-section consistency) and treat the file as new. Either the step was created by another task that is not yet merged, or the task means "create".
2. **Migration registration:** a new `m0002_supplier` module must be declared and added to the `Migrator` in `migration/src/lib.rs`. That file is not in scope, so I would flag it for user approval.
3. **`sbom_supplier` table/entity:** there is no `entity/src/sbom_supplier.rs`. If this migration also creates the table, I would write it with the SeaQuery schema builder inside the migration, which needs no entity. If the task expects a SeaORM entity, that file is out of scope and I would flag it.
4. **Ingestor module visibility:** if `graph` or `sbom` are not `pub` modules, then `lib.rs` or `graph/mod.rs` also need a change. That is out of scope, so I would flag it.

## Step 5 – Branch

`git checkout main && git pull && git checkout -b TC-9206` (not run in this eval).

## Step 6 – Changes per file

### 1. `modules/ingestor/src/graph/sbom/mod.rs` (modify)
- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` becomes `pub fn ...`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` becomes `pub fn ...`
- Add `///` doc comments to both functions, because they are now public API. For example: "Returns the packages this SBOM declares it describes (its top-level subjects)." and "Extracts supplier information from the SBOM metadata; returns an empty vec when none is declared."
- Make sure `Sbom`, `PackageRef` and `SupplierInfo` are `pub`. If they are defined in this file, I change them here.
- The bodies and signatures stay as they are. This is a visibility change only.

### 2. `migration/src/m0002_supplier/mod.rs` (modify, or create if missing as noted above)
- Imports:
  ```rust
  use sea_orm_migration::prelude::*;
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- `#[derive(DeriveMigrationName)] pub struct Migration;` with a `MigrationTrait` impl that follows the style of `m0001_initial`.
- `up()`:
  1. Create the `sbom_supplier` table, if this step owns its creation, with columns such as `sbom_id` (FK to `sbom.id`, ON DELETE CASCADE), `package_ref` and `supplier`, and a unique key on `(sbom_id, package_ref, supplier)`.
  2. Load every ingested SBOM. The task says "all ingested SBOMs", so a full scan is intended (Step 9 query-scope check). Process them in pages or batches so the whole table is never in memory at once, and add a comment explaining why the query is broad.
  3. For each SBOM, build the ingestor's `Sbom` value and call the **imported** `describing_packages(&sbom)` and `suppliers(&sbom)`. No extraction logic is written again in the migration.
  4. Map the result to `sbom_supplier` rows and insert them with `ON CONFLICT DO NOTHING`, so a re-run is idempotent and matches how the ingestor writes. Write nothing when `suppliers()` returns an empty vec.
  5. Treat data from the other crate defensively: skip SBOMs whose documents fail to parse or have no metadata, and log them instead of panicking (`if let` / `unwrap_or_default()`).
- `down()`: drop the `sbom_supplier` table (or delete the backfilled rows if another step owns the table).
- Put the row-building logic in a small helper such as `fn supplier_rows(sbom_id, &Sbom) -> Vec<SupplierRow>` (with a `///` doc comment). Unit tests can call it without a database. It only calls the imported ingestor functions.
- Add `#[cfg(test)] mod test;` to wire in the new test file.

### 3. `migration/src/m0002_supplier/test.rs` (create)
Tests follow the Step 7 rules: a `///` doc comment on every test, `// Given / // When / // Then` sections, and assertions on actual values rather than only lengths.
- `/// Verifies that suppliers declared in a sample SBOM are extracted into sbom_supplier rows.`
  `test_extracts_suppliers_from_sample_sbom`: build a fixture SBOM with known describing packages and suppliers (for example "Acme Corp" and "Red Hat"). Assert `assert_eq!` on the exact `(package_ref, supplier)` rows, not just the count.
- `/// Verifies that an SBOM without supplier metadata produces no supplier records.`
  `test_sbom_without_suppliers_produces_no_records`: assert `assert_eq!(rows, vec![])` (or `is_empty()` on a typed vec).
- The two cases use different setups and assertions, so they stay separate tests rather than one parameterized test. The repo shows no use of `rstest`, so I would not introduce it.
- If the repo's test DB harness can be used from the migration crate, add an integration-style check that `up()` fills `sbom_supplier` for SBOMs already in the database. This covers the acceptance criterion "table is populated correctly".

### Documentation impact
No public REST API changes. If `CONVENTIONS.md` or `docs/architecture.md` lists migrations or ingestor internals, I would add a short note there. Otherwise no documentation changes.

## Step 7/8 – Tests and acceptance criteria
- `cargo test -p <migration crate>` and `cargo test -p trustify-module-ingestor`. Get the crate names from `cargo metadata --no-deps`.
- AC1 (all SBOMs processed): covered by the full, batched scan in `up()`.
- AC2 (reuse, no duplication): covered by importing `describing_packages` and `suppliers`. See reuse-decision.md.
- AC3 (table populated correctly): covered by the value-based unit tests and the optional DB test.

## Step 9 – Self-verification plan
- **Scope containment:** the expected diff is the 3 listed files. Possible out-of-scope files, each needing user approval: `migration/src/lib.rs` (registration), `modules/ingestor/src/lib.rs` or `graph/mod.rs` (module visibility), and an `entity/src/sbom_supplier.rs` entity if one is needed.
- **Duplication check:** grep the migration crate for supplier or describing-package parsing logic to confirm that none was re-implemented.
- **CI checks:** run the commands from `CONVENTIONS.md` (for example `cargo fmt --check`, `cargo clippy -- -D warnings`). Stop on any failure.
- **Data-flow trace:** stored SBOM, then load and parse, then `describing_packages` / `suppliers` (ingestor), then map to rows, then insert into `sbom_supplier`. Every stage connects to the next.
- **Cross-module entity parity:** if the ingestor also writes `sbom_supplier` at ingest time, use the same conflict handling and column semantics.
- Also: the sensitive-pattern check and the untracked-file check (for example, a test.rs that is not yet staged).

## Step 10/11 – Commit, PR and Jira (not run in this eval)
- Commit: `feat(migration): extract SBOM suppliers during data migration`. The body says that `describing_packages()` and `suppliers()` in `trustify-module-ingestor` were made `pub` and imported instead of duplicated, because the migration crate already depends on the ingestor. Footer `Implements TC-9206`, plus the trailer `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- PR: `gh pr create --base main`. The description states the same reuse rationale and contains `Implements [TC-9206](<webUrl>)`.
- Jira: set `customfield_10875` to the PR URL (ADF inlineCard), add a comment with the footnote, and transition to In Review.
