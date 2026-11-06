# Implementation Plan: TC-9206 — Add SBOM supplier extraction to data migration

## Step 0: Project Configuration check
The mock CLAUDE.md has a Repository Registry (trustify-backend, Serena instance
`serena_backend`, path `./`). It also has Jira Configuration (Project key TC, Cloud ID,
Feature issue type ID 10142) and Code Intelligence (naming convention
`mcp__<instance>__<tool>`). Validation passes.

## Step 1: Parsed task
| Field | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Target PR / Bookend Type | none (default flow) |
| Files to Modify | `migration/src/m0002_supplier/mod.rs`, `modules/ingestor/src/graph/sbom/mod.rs` |
| Files to Create | `migration/src/m0002_supplier/test.rs` |
| Dependencies | None |
| GitHub Issue (customfield_10747) | read from issue; if set, add `Closes <owner>/<repo>#<n>` to PR body |

All required sections are present, so the task can proceed.

## Steps 1.5–3: Jira steps (simulated, not executed)
- Fetch comments and check the `[sdlc-workflow] Description digest:` comment, if one exists.
- No dependencies to check.
- Assign TC-9206 to the current user and move it to In Progress.

## Step 4: Understand the code (planned Serena calls on `serena_backend`)
1. `get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")`: locate
   `describing_packages`, `suppliers`, `PackageRef`, `SupplierInfo`, and check their visibility.
2. `find_symbol("describing_packages", include_body=true)` and the same for `suppliers`:
   confirm the signatures match the Implementation Notes.
3. `find_referencing_symbols` on both: list the existing internal callers. A visibility
   change does not break them.
4. Check that the module path is public: `pub mod graph` in `modules/ingestor/src/lib.rs`,
   and `pub mod sbom` in `modules/ingestor/src/graph/mod.rs`.
5. Read `migration/Cargo.toml` to confirm the `trustify-module-ingestor` dependency.
6. Siblings for conventions: `migration/src/m0001_initial/mod.rs` and
   `migration/src/lib.rs` (the `Migrator` list). Check how migrations implement
   `MigrationTrait` (`up`/`down`), how they access the DB, and how they handle errors.
7. Look for a `sbom_supplier` entity or table definition. The repo listing has no
   `entity/src/sbom_supplier.rs`.
8. Read `CONVENTIONS.md` at the repo root for naming, test conventions, and its CI check
   commands, which Step 9 needs.
9. Docs to check: `README.md`, `docs/architecture.md`.

### Discrepancies to raise with the user before coding
- **`migration/src/m0002_supplier/mod.rs` is listed under Files to Modify, but it does not
  appear in the repo structure.** Only `m0001_initial/` exists. I would confirm with the
  user whether it already exists on `main` (from another task) or whether it should be
  created. If it must be created, it also has to be registered in `migration/src/lib.rs`
  (`mod m0002_supplier;` plus a `Box::new(m0002_supplier::Migration)` entry in
  `Migrator::migrations()`). That file is outside Files to Modify, so it needs approval.
- **No `sbom_supplier` table or entity exists in the listing.** I would ask whether
  table creation belongs to this migration or to another task. If it belongs here, the
  `up()` would create the table before populating it.
- **Module visibility in the ingestor.** If `graph` or `sbom` is not `pub`,
  making the functions `pub` is not enough. `lib.rs` or `graph/mod.rs` would also
  need changes, which are out of scope and need user approval.

## Step 5: Branch
`git checkout main && git pull && git checkout -b TC-9206` (simulated)

## Step 6: Changes

### 6.1 `modules/ingestor/src/graph/sbom/mod.rs` (modify)
- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` becomes `pub fn describing_packages(...)`.
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` becomes `pub fn suppliers(...)`.
- Add `///` doc comments to both, because they are now public API.
- If `PackageRef` or `SupplierInfo` (and their fields the migration reads) are private, make
  them `pub` as well and add doc comments. Otherwise the public functions cannot be used
  from outside the crate.
- No change to bodies or signatures. Internal callers are untouched.

### 6.2 `migration/src/m0002_supplier/mod.rs` (modify)
- Import the shared helpers. Do not copy them:
  `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`
- Implement the migration step, following the `m0001_initial` pattern (`MigrationTrait`):
  - `up()`: iterate over all ingested SBOMs. The task scope is "all ingested SBOMs", so a
    query that loads every SBOM is intentional; add a short comment saying so.
    Process in pages or batches, not by loading everything into memory. For each SBOM:
    load or parse the document into `Sbom`, call `describing_packages(&sbom)` and
    `suppliers(&sbom)`, map each `SupplierInfo` (linked to the SBOM id and the describing
    package where relevant) into `sbom_supplier` rows, and insert them. Use
    `ON CONFLICT DO NOTHING` so a re-run is idempotent and matches the ingestor's conflict
    handling for shared entities.
  - Skip SBOMs where `suppliers()` returns an empty `Vec`, which produces no rows.
  - Use defensive access on the SBOM data, because it comes from another module.
    For example, use `unwrap_or_default()` and `if let` for optional supplier name/URL fields.
  - Handle errors the way sibling migrations do (`DbErr` / `.context()` as used there).
  - `down()`: delete the populated `sbom_supplier` rows, or mirror whatever reversal the
    sibling migration uses.
- Split the pure mapping into a small helper so it can be unit tested without a DB,
  for example `fn supplier_rows(sbom_id, &Sbom) -> Vec<sbom_supplier::ActiveModel>`, built on the
  two imported functions. Give it a `///` doc comment.
- Add `#[cfg(test)] mod test;` to register the new test file.

### 6.3 `migration/src/m0002_supplier/test.rs` (create)
Follow the `CONVENTIONS.md` and sibling test conventions. Every test gets a `///` doc comment and
`// Given / // When / // Then` sections.
- `/// Verifies supplier rows are extracted from an SBOM that declares suppliers.`
  `test_extracts_suppliers_from_sample_sbom`: build a sample SBOM with known suppliers,
  then assert on the actual values (supplier names, the linked SBOM id, the describing package).
  A row count alone is not enough. For example, `assert_eq!(rows, vec![expected_a, expected_b])`.
- `/// Verifies an SBOM without supplier metadata produces no supplier records.`
  `test_sbom_without_suppliers_produces_no_records`: assert `rows.is_empty()` (or
  `assert_eq!(rows, vec![])`).
- If the project's migration tests use the test DB, add a test that runs `up()` against a
  seeded SBOM and checks the `sbom_supplier` table contents. This covers AC3.
- The two required tests differ in setup and assertions, so they stay separate tests
  rather than one parameterized test.

### Documentation impact
No public REST API changes. If `docs/architecture.md` or the README describe migrations or the
`sbom_supplier` schema, update them briefly. Otherwise no doc changes.

## Steps 7–8: Tests and acceptance criteria
- `cargo test -p trustify-migration` and `cargo test -p trustify-module-ingestor`. Resolve
  the crate names with `cargo metadata --no-deps --format-version 1`.
- AC1 (extracts from all ingested SBOMs): `up()` iterates every SBOM.
- AC2 (reuses ingestor logic): the imports come from `trustify_module_ingestor`, with no
  copied function bodies.
- AC3 (table populated correctly): the value-based assertions and the DB-backed test cover it.

## Step 9: Self-verification
- **Scope:** `git diff --name-only` must list only the three files above. Flag any change to
  `migration/src/lib.rs`, `modules/ingestor/src/lib.rs`, `modules/ingestor/src/graph/mod.rs`,
  `entity/src/*`, or `migration/Cargo.toml` for user approval.
- **Duplication check:** grep the migration crate for any re-implementation of supplier or
  describing-package parsing. There should be none.
- **Run the CI commands from `CONVENTIONS.md`** (e.g. `cargo fmt --check`, `cargo clippy`).
  Stop on any non-zero exit.
- **Contract and sibling parity:** `MigrationTrait` provides `up`/`down`. Compare with
  `m0001_initial` for parity. Use the same conflict handling as the ingestor when writing
  SBOM-related rows.
- **Data flow:** SBOM rows in the DB, then parse to `Sbom`, then `describing_packages`/`suppliers`,
  then map to `sbom_supplier` rows, then insert. Every stage connects.
- **Query scope:** the full SBOM scan is intended ("all ingested SBOMs"), and a comment says so.
- Check for sensitive patterns and for untracked files.

## Step 10: Commit and PR (simulated)
```
feat(migration): extract SBOM suppliers during data migration

Populate the sbom_supplier table by reusing the ingestor's
describing_packages() and suppliers() helpers, now made public.
migration already depends on trustify-module-ingestor, so the helpers
are imported rather than duplicated (no new crate coupling).

Implements TC-9206
```
Use `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.

Run `gh pr create --base main`. The PR body includes `Implements [TC-9206](<webUrl>)`, the
reuse rationale, and a `Closes` line if a GitHub issue is linked.

## Step 11: Jira (simulated)
- Set customfield_10875 to the PR URL in ADF inlineCard form.
- Add a comment with the PR link, a summary, and any deviations (for example, approved
  out-of-scope files), ending with the implement-task footnote.
- Move the issue to In Review.
