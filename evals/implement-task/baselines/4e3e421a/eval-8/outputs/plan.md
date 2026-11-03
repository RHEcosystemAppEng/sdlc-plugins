# Implementation Plan — TC-9206: Add SBOM supplier extraction to data migration

## Step 0 — Project Configuration validation

The project CLAUDE.md (claude-md-mock.md) has everything the skill needs:
- Repository Registry: `trustify-backend`, Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: `mcp__<instance>__<tool>` naming convention, `serena_backend` (rust-analyzer)

Validation passes, so execution continues.

## Step 1 — Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none (default flow) |
| Bookend Type | none |
| Dependencies | None |
| Files to Modify | `migration/src/m0002_supplier/mod.rs`, `modules/ingestor/src/graph/sbom/mod.rs` |
| Files to Create | `migration/src/m0002_supplier/test.rs` |

All required sections are present. The GitHub Issue field (`customfield_10747`) would be read from the issue. It is empty in the mock, so no `Closes` line gets added.

## Steps 1.5–3 — Jira (simulated, no calls made)

- 1.5: Fetch comments and look for `[sdlc-workflow] Description digest:`. If there is no digest, log a warning and continue.
- 2: There are no dependencies, so nothing to verify.
- 3: `jira.user_info()`, assign TC-9206 to that user, then transition it to In Progress.

## Step 4 — Understand the code (planned Serena calls on `serena_backend`)

1. `mcp__serena_backend__get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")` to confirm that `describing_packages` and `suppliers` exist and are private.
2. `mcp__serena_backend__find_symbol("describing_packages", include_body=true)` and the same for `suppliers`, to confirm the signatures:
   - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
   - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`
3. `find_symbol` on `PackageRef`, `SupplierInfo` and `Sbom`, to check that these types are reachable from outside the crate. They must be `pub` and re-exported through a `pub mod` path. Otherwise, making the functions `pub` would trigger a `private type in public interface` error or warning.
4. `find_referencing_symbols` on both functions to list the current in-crate callers. Changing only the visibility is backward compatible, so the callers stay as they are.
5. Read `migration/Cargo.toml` to confirm `trustify-module-ingestor = { path = "../modules/ingestor" }` (see reuse-decision.md).
6. Check that `modules/ingestor/src/lib.rs` and `modules/ingestor/src/graph/mod.rs` declare `pub mod graph` and `pub mod sbom`. Without that, the path `trustify_module_ingestor::graph::sbom::suppliers` cannot be reached.
7. Sibling and convention analysis: `get_symbols_overview` on `migration/src/m0001_initial/mod.rs` and `migration/src/lib.rs`, to learn the `MigrationTrait`/`Migrator` registration pattern and naming (`m000N_<name>`).
8. Read `CONVENTIONS.md` at the repo root. Extract the CI check commands (likely `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) and any codegen commands.
9. Docs: `README.md` and `docs/architecture.md`. These are not expected to need changes because no public API or endpoint changes.

### Discovered conventions (expected, confirmed in Step 4)
- Errors: `Result<T, AppError>` / `DbErr` with `.context()` wrapping. Migrations return `Result<(), DbErr>`.
- Naming: `snake_case` and `verb_noun` functions. Migration modules are named `m000N_<topic>`.
- Module structure: each migration lives in its own directory with a `mod.rs`, and tests go in a sibling `test.rs` included via `#[cfg(test)] mod test;`.
- Tests: `assert_eq!` with concrete values.

### Cross-section / codebase consistency flags (to raise with the user)
- `repo-backend.md` shows only `migration/src/m0001_initial/`. The directory `migration/src/m0002_supplier/` and its `mod.rs` are listed under **Files to Modify**, but they do not appear in the tree. If Step 4 confirms the file does not exist, I would ask the user whether to create it. That would also mean adding the module to the migrator list in `migration/src/lib.rs`, a file that is not in scope.
- No `entity/src/sbom_supplier.rs` exists, and the migration that creates the `sbom_supplier` table is not visible. The task assumes the table is "new". If it is not created elsewhere, inserting into it needs either a table-creation step in `m0002_supplier/mod.rs` or an out-of-scope entity file.
- Because of the rule against adding out-of-scope files to the plan, the two items above are **flagged for user approval** and are not planned edits.

## Step 5 — Branch

```
git checkout main
git pull
git checkout -b TC-9206
```

## Step 6 — Changes per file

### 1. `modules/ingestor/src/graph/sbom/mod.rs` (modify)
- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(...)`.
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(...)`.
- Add a `///` doc comment to each, since they are now public API:
  - `/// Returns the packages that the given SBOM declares it describes (its top-level subjects).`
  - `/// Extracts supplier information from the SBOM's metadata; returns an empty Vec when none is declared.`
- Leave function bodies and existing callers unchanged.
- If `PackageRef` or `SupplierInfo` turn out to be private, make them `pub` in this same file. This stays in scope only if they are defined here. If they are defined elsewhere, flag it.
- Tooling: `mcp__serena_backend__replace_symbol_body`, or an Edit on just the signature lines.

### 2. `migration/src/m0002_supplier/mod.rs` (modify)
- Import the reused logic instead of duplicating it:
  ```rust
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- Inside the migration's `up()`:
  1. Iterate over ingested SBOMs, querying all rows of the `sbom` table. Query scope: the task says "all ingested SBOMs", so a full scan is intended. Process the rows in pages or batches to bound memory, and add a comment explaining why the query is broad.
  2. For each SBOM, load or parse the stored document into the ingestor's `Sbom` type.
  3. Call `describing_packages(&sbom)` and `suppliers(&sbom)`.
  4. Insert one `sbom_supplier` row per (SBOM, supplier) pair. Use `ON CONFLICT DO NOTHING` so the migration can be re-run and matches the ingestor's conflict handling (cross-module entity parity check). If the extraction returns an empty `Vec`, insert nothing.
  5. Guard against missing or partial data from the ingestor, for example by skipping and logging SBOMs whose document cannot be parsed. Use `.context()` wrapping per convention.
- `down()`: delete the rows inserted into `sbom_supplier`, following whatever pattern `m0001_initial` uses for `down`.
- Add a doc comment on the migration struct and on any new helper, for example a private helper `fn supplier_rows(sbom_id, &Sbom) -> Vec<sbom_supplier::ActiveModel>` that is a pure mapping and easy to unit test.
- Add `#[cfg(test)] mod test;` to wire in the new test file.

### 3. `migration/src/m0002_supplier/test.rs` (create)
Each test gets a `///` doc comment and `// Given / // When / // Then` sections. Assertions are value-based.
- `/// Verifies that suppliers are extracted from a sample SBOM and mapped to sbom_supplier rows.`
  `test_extracts_suppliers_from_sample_sbom`: build a sample SBOM with two known suppliers, run the extraction helper, then `assert_eq!` on the actual supplier names and SBOM id of the rows, not just the count.
- `/// Verifies that an SBOM with no supplier metadata produces no sbom_supplier records.`
  `test_sbom_without_suppliers_yields_no_records`: `assert_eq!(rows, vec![])`.
- These are two different behaviors with different setup and assertions, so they stay as separate tests (Meszaros heuristic) and are not parameterized.
- If the crate's test harness provides a test DB, add one DB-backed check that runs `up()` and queries `sbom_supplier` for the expected rows. This covers "table populated correctly".

### Documentation impact
There are no endpoint, config or CLI changes, so no doc updates are expected. The two newly public functions get doc comments.

## Step 7 — Tests
`cargo test -p <migration-crate>` and `cargo test -p trustify-module-ingestor`. Resolve the package names via `cargo metadata --no-deps --format-version 1`.

## Step 8 — Acceptance Criteria mapping
- Supplier extraction runs for all ingested SBOMs: `up()` iterates over every SBOM.
- Reuses the ingestor logic: the migration imports `describing_packages` and `suppliers`, and no copy of the logic exists in the migration crate.
- `sbom_supplier` populated correctly: covered by the value-based tests and the DB-backed test.

## Step 9 — Self-verification
- Scope: `git diff --name-only` must equal exactly the three listed files. `migration/src/lib.rs`, an `entity` file, or a type made `pub` in another file would each need explicit user approval.
- Duplication check: grep the migration crate for any re-implementation of supplier or describing-package parsing. There should be none.
- Run the CONVENTIONS.md CI checks (fmt, clippy, check). Any failure is a hard stop.
- Run `cargo test -p` for both modified crates (the ingestor crate and the migration crate). Any failure is a hard stop.
- Data-flow trace: `sbom` rows → parse to `Sbom` → `describing_packages` / `suppliers` → `sbom_supplier` rows → insert.
- Contract/sibling parity: `MigrationTrait` `up`/`down` both implemented, matching `m0001_initial`. Conflict handling matches the ingestor.

## Step 10 — Commit and PR
```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): extract SBOM suppliers during data migration

Make ingestor's describing_packages() and suppliers() public and reuse
them from the m0002_supplier migration instead of duplicating the logic.
The migration crate already depends on trustify-module-ingestor, so no
new cross-crate dependency is introduced.

Implements TC-9206"
```
- No `upstream` remote, so `gh pr create --base main`.
- The PR body includes `Implements [TC-9206](<webUrl>)` and a "Reuse decision" section with the rationale from reuse-decision.md.

## Step 11 — Jira (simulated)
- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Add a comment with the PR link, a summary, and deviations (for example, if `m0002_supplier` had to be created or `lib.rs` registration was approved). End it with the implement-task footnote.
- Transition to In Review.
