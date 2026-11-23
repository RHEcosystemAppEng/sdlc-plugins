# Implementation Plan — TC-9206: Add SBOM supplier extraction to data migration

## Step 0 – Project Configuration validation
CLAUDE.md (claude-md-mock.md) contains Repository Registry (trustify-backend →
`serena_backend`, path `./`), Jira Configuration (project key TC, Cloud ID, Feature
issue type ID 10142, PR field `customfield_10875`, GitHub Issue field
`customfield_10747`), and Code Intelligence. Validation passes.

## Step 1 – Parsed task
- Repository: trustify-backend
- Target Branch: `main` (no Target PR, no Bookend Type → default flow)
- Files to Modify:
  - `migration/src/m0002_supplier/mod.rs`
  - `modules/ingestor/src/graph/sbom/mod.rs`
- Files to Create:
  - `migration/src/m0002_supplier/test.rs`
- Dependencies: none (Step 2 is a no-op)
- All required sections present.

Steps 1.5 / 3 (digest check, assign, transition to In Progress) would be done via
Jira MCP — skipped in this eval (no external calls).

## Step 4 – Code understanding (what I would inspect with `serena_backend`)
- `get_symbols_overview` on `modules/ingestor/src/graph/sbom/mod.rs`; `find_symbol`
  with body for `describing_packages`, `suppliers`, `PackageRef`, `SupplierInfo`, `Sbom`.
- `find_referencing_symbols` on both functions to list existing in-crate callers.
- Read `migration/Cargo.toml` to confirm the `trustify-module-ingestor` dependency.
- Verify module visibility chain: `modules/ingestor/src/lib.rs` (`pub mod graph`),
  `graph/mod.rs` (`pub mod sbom`).
- Sibling conventions: `migration/src/m0001_initial/mod.rs` and `migration/src/lib.rs`
  (SeaORM `MigrationTrait` impl, `DeriveMigrationName`, `up`/`down` structure).
- Read `CONVENTIONS.md` at repo root and extract CI check commands (e.g. `cargo fmt
  --check`, `cargo clippy`, etc.) for Step 9.
- Search for an `sbom_supplier` entity / table definition (`search_for_pattern
  "sbom_supplier"`).

### Discrepancies found against repo-backend.md (to flag)
1. `migration/src/m0002_supplier/mod.rs` is listed under **Files to Modify**, but the
   repository tree shows only `migration/src/m0001_initial/`. If it truly does not
   exist, it must be created; I would ask the user to confirm (cross-section reference
   consistency check) rather than silently re-scope.
2. Registering a new migration requires adding it to the `Migrator::migrations()` list
   in `migration/src/lib.rs`, which is **not** in Files to Modify → flag as
   out-of-scope for user approval if needed.
3. No `entity/src/sbom_supplier.rs` exists in the tree. If the `sbom_supplier` table is
   not created by an earlier migration, table creation must happen inside m0002
   (within scope) or an entity file is needed (out of scope → flag).
4. `test.rs` must be wired with `#[cfg(test)] mod test;` in `m0002_supplier/mod.rs`
   (within scope).

## Step 5 – Branch
`git checkout main && git pull && git checkout -b TC-9206` (not executed).

## Step 6 – Changes per file

### `modules/ingestor/src/graph/sbom/mod.rs` (modify)
- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` → `pub fn ...`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` → `pub fn ...`
- Make `PackageRef` and `SupplierInfo` (and their fields the migration reads) `pub`
  if they are currently private, so the public signatures are usable externally.
- Add `///` doc comments to both functions (and types if newly public).
- No signature or behavior changes — existing callers unaffected.

### `migration/src/m0002_supplier/mod.rs` (modify / create-if-missing, see flag 1)
- `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`
- In `MigrationTrait::up`:
  1. Ensure `sbom_supplier` table exists (if this migration owns its creation:
     columns e.g. `sbom_id` FK → `sbom.id`, `supplier` name, plus PK/unique on
     `(sbom_id, supplier)`).
  2. Iterate all ingested SBOMs (query scope: all SBOMs — the description says
     "from all ingested SBOMs", so a broad query is intentional; document with a
     comment; page through in batches to bound memory).
  3. For each SBOM: load/parse the stored document into `Sbom`, call
     `describing_packages(&sbom)` and `suppliers(&sbom)`, and insert one
     `sbom_supplier` row per supplier using `ON CONFLICT DO NOTHING` to stay
     idempotent and consistent with ingestor insert semantics (cross-module entity
     parity).
  4. SBOMs with no suppliers → no rows inserted.
  5. Defensive handling: use `.unwrap_or_default()` / skip on missing metadata;
     propagate DB errors as `DbErr`.
- In `down`: delete the rows (or drop the table if created here).
- Factor the per-SBOM mapping into a small pure helper
  (`fn supplier_rows(sbom_id, &Sbom) -> Vec<...>`, with `///` doc) so it can be
  unit-tested without a DB. This helper only maps the ingestor outputs to rows — it
  does not re-implement extraction.
- `#[cfg(test)] mod test;`

### `migration/src/m0002_supplier/test.rs` (create)
Following sibling test conventions, with `///` doc comment on every test and
given/when/then comments:
- `test_extracts_suppliers_from_sample_sbom` — Given a sample SBOM with two suppliers;
  When running extraction/`supplier_rows`; Then `assert_eq!` on the exact supplier
  names and `sbom_id` values (value-based, not length-only).
- `test_sbom_without_suppliers_produces_no_records` — Given an SBOM with no supplier
  metadata; When extracting; Then `assert_eq!(rows, vec![])`.
- If the project's migration tests use a test DB, an additional DB-backed test
  verifies `sbom_supplier` contents after `up`.
- Two cases differ in assertions/setup, so separate tests (no parameterization).

### Documentation impact
None expected beyond doc comments; check README/CONVENTIONS for migration lists.

## Step 7–8 – Tests & acceptance criteria
- `cargo test -p trustify-module-ingestor` and `cargo test -p <migration crate name
  from cargo metadata>`.
- AC1: all SBOMs iterated in `up` ✔. AC2: imports ingestor functions, no duplicated
  logic ✔. AC3: rows inserted per supplier, verified by tests ✔.

## Step 9 – Self-verification
- Scope containment: diff should contain only the 3 listed files; `migration/src/lib.rs`
  (and any visibility change in `lib.rs`/`graph/mod.rs` or entity file) flagged for
  approval if required.
- Duplication check: grep for any supplier-extraction logic in `migration/` to ensure
  none was copied.
- Run CONVENTIONS.md CI checks (hard stop on failure) and per-crate `cargo test`.
- Contract & sibling parity: `MigrationTrait` up/down implemented like m0001;
  insert conflict handling matches ingestor.
- Data flow: stored SBOM → parse → `describing_packages`/`suppliers` → rows →
  `sbom_supplier` table — complete.

## Step 10–11 – Commit, PR, Jira (not executed)
- Commit: `feat(migration): extract SBOM suppliers in m0002 migration` with body
  explaining the reuse decision, footer `Implements TC-9206`, and
  `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- PR `--base main`, body includes `Implements [TC-9206](<webUrl>)`, the reuse
  rationale, and `Closes owner/repo#N` if the GitHub Issue field is set.
- Jira: set `customfield_10875` (ADF inlineCard), add comment with footnote,
  transition to In Review.

## Handling of the private ingestor functions (summary)
Make `describing_packages()` and `suppliers()` `pub` and import them in the migration,
because `migration` already depends on `trustify-module-ingestor` — see
`reuse-decision.md`.
