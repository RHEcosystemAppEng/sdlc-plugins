# Implementation Plan — TC-9206: Add SBOM supplier extraction to data migration

This is a simulated run of `/sdlc-workflow:implement-task`. No repository files were changed, and no calls were made to Jira, git, GitHub or Serena. Each step below says what would happen in a live run.

## Step 0: Validate Project Configuration

The project CLAUDE.md (`claude-md-mock.md`) has all three required sections:
- **Repository Registry**: `trustify-backend` uses the Serena instance `serena_backend` at path `./`.
- **Jira Configuration**: the project key (TC), Cloud ID and Feature issue type ID (10142) are all set. The Git Pull Request field is `customfield_10875` and the GitHub Issue field is `customfield_10747`.
- **Code Intelligence**: it gives the naming convention `mcp__<serena-instance>__<tool>`. The instance is `serena_backend`, which uses rust-analyzer. Its listed limitation is that indexing takes 30-60 seconds on first use.

Result: the configuration is valid, so the run continues.

## Step 1: Parse the task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Description | Extract describing packages and suppliers from ingested SBOMs during migration, and use them to fill the `sbom_supplier` table |
| Files to Modify | `migration/src/m0002_supplier/mod.rs`, `modules/ingestor/src/graph/sbom/mod.rs` |
| Files to Create | `migration/src/m0002_supplier/test.rs` |
| API Changes | None (there is no such section, and no endpoints are involved) |
| Implementation Notes | Make `describing_packages()` and `suppliers()` public and import them. The `migration` crate already depends on `trustify-module-ingestor` |
| Acceptance Criteria | 3 items (see Step 8) |
| Test Requirements | 2 items (see Step 7) |
| Target PR / Bookend Type / Review Context | None. This uses the default flow |
| Dependencies | None |
| GitHub Issue (`customfield_10747`) | Read from the issue fields. If it is empty, it is skipped without comment |

All required sections are present, so the run continues.

## Step 1.5: Description integrity

The run would fetch the comments on TC-9206 with `jira.get_issue_comments`. It would then look for the most recent `[sdlc-workflow] Description digest:` comment and compare that digest with the output of `python3 scripts/sha256-digest.py`. If the digest matches, the run continues. If it does not match, the run stops and asks the user what to do. If there is no digest comment, the run logs a warning and continues.

## Step 2: Dependencies

There are none, so nothing needs checking.

## Step 3: Jira status

1. Call `jira.user_info()` to get the current user's account ID.
2. Call `jira.edit_issue(TC-9206, assignee=<id>)` to assign the task to that user.
3. Call `jira.transition_issue(TC-9206, "In Progress")`.

## Step 4: Understand the code (using `serena_backend`)

These are the checks a live run would make before editing anything:

1. Run `mcp__serena_backend__get_symbols_overview` on `modules/ingestor/src/graph/sbom/mod.rs`. This confirms that `describing_packages` and `suppliers` exist with the signatures given in the task:
   - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
   - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`
2. Run `find_symbol(include_body=true)` on both functions to read how they work. Then find where their parameter and return types (`Sbom`, `PackageRef`, `SupplierInfo`) are defined and check those types' visibility. If any of them is private, making the functions `pub` will raise a `private type in public interface` error. Those types would also need to be `pub`, or re-exported from the same file (see the reuse decision for details).
3. Run `find_referencing_symbols` on both functions to list the callers that exist today inside the ingestor. Making a function more visible does not break existing callers, but the list confirms how much is affected.
4. Check the module path from the crate root. That means checking `modules/ingestor/src/lib.rs` (`mod graph` / `pub mod graph`) and `graph/mod.rs` (`mod sbom` / `pub mod sbom`). If either module is private, `pub fn` alone does not make the functions reachable. In that case the plan is to add a `pub use` re-export, preferably inside `graph/sbom/mod.rs` so it stays in scope (more below).
5. **Check the dependency.** Read `migration/Cargo.toml` and confirm it contains `trustify-module-ingestor = { path = "../modules/ingestor" }`, as the Implementation Notes say. This check matters because the reuse decision depends on it.
6. **Discrepancy: the target directory is missing.** The repository structure (`repo-backend.md`) lists only `migration/src/lib.rs` and `migration/src/m0001_initial/mod.rs`. There is no `m0002_supplier/` directory, even though the task lists `migration/src/m0002_supplier/mod.rs` under **Files to Modify**. There is also no `sbom_supplier` entity in `entity/src/`. In a live run I would check this with `list_dir`. If it is confirmed, I would **raise it with the user before implementing**, because of the next point.
   - If `m0002_supplier/mod.rs` does not exist, it would also need to be registered in the migrator in `migration/src/lib.rs`, and the `sbom_supplier` table would need a schema and entity. Neither `migration/src/lib.rs` nor any `entity/` file is listed in Files to Modify or Files to Create, so I would not add them to the plan. I would flag them for scope approval in Step 9.
7. **Sibling conventions.** Run `get_symbols_overview` on `migration/src/m0001_initial/mod.rs` and `migration/src/lib.rs` to learn the migration pattern. This is SeaORM `MigrationTrait`, with `up`/`down` and `#[async_trait]`, plus the `DeriveMigrationName` naming. Also look at another ingestor graph module (`graph/advisory/mod.rs`) to see how its helpers are exposed.
8. **CONVENTIONS.md.** The file is at the repository root (`./CONVENTIONS.md`). Read it and record the CI check commands it lists (for example `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`) and any code generation commands. These are used in Step 9.
9. **Related documentation.** Candidates are `README.md`, `docs/architecture.md` and any migration docs. No public API or endpoint changes are expected, so no documentation updates are expected either.

**Conventions found (these bind the implementation):**
- Errors: use `Result<T, _>` with `.context()` wrapping. In migrations, use `DbErr` as SeaORM requires.
- Naming: functions use `verb_noun` or lowercase noun names. Migration modules use `mNNNN_<name>`.
- Database: SeaORM. Writes to shared entities should follow the ingestor's conflict handling (for example `ON CONFLICT DO NOTHING` / `DO UPDATE`).
- Tests: use `assert_eq!` on concrete values and a real PostgreSQL test database where one is needed.

## Step 5: Create the branch

```
git checkout main
git pull
git checkout -b TC-9206
```

## Step 6: Implement the changes

### 6.1 `modules/ingestor/src/graph/sbom/mod.rs` (modify)

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(...)`.
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(...)`.
- Do not change either function body. The only change is visibility.
- Add `///` doc comments to both functions, because they become part of the crate's public API:
  - `/// Returns the packages that the given SBOM declares it describes (its top-level subjects).`
  - `/// Extracts the supplier entries declared in the given SBOM's metadata. Returns an empty Vec when no supplier is declared.`
- If `PackageRef` or `SupplierInfo` is defined in this file and is private, make it `pub` too, with a doc comment. A public function cannot expose private types.
- If the module path (`graph` or `graph::sbom`) is private at the crate root, add `pub use` re-exports, but only after checking with the user, since `lib.rs` and `graph/mod.rs` are outside the listed scope. `pub(crate)` would **not** work, because the caller lives in a different crate (`migration`).

### 6.2 `migration/src/m0002_supplier/mod.rs` (modify)

Add the extraction step to the migration's `up()`:

```rust
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};

/// Collects the supplier rows to insert for one SBOM: one row per supplier.
/// Rows are linked to the SBOM and to the packages it describes.
fn supplier_rows(sbom_id: Uuid, sbom: &Sbom) -> Vec<SbomSupplierRow> {
    let _described = describing_packages(sbom); // used to link suppliers to described packages
    suppliers(sbom)
        .into_iter()
        .map(|s| SbomSupplierRow::new(sbom_id, s /* , described-package link */))
        .collect()
}
```

- `up()` iterates over **all** ingested SBOMs, as Acceptance Criterion 1 requires. The SBOMs are read in pages, or streamed, so they are not all loaded into memory at once. A full scan is intended in this case because the task covers every SBOM, and I would note that in a code comment (this is the query-scope check).
- For each SBOM, parse or load the stored document, call `supplier_rows`, and bulk-insert the rows into `sbom_supplier`. The insert uses an `ON CONFLICT DO NOTHING` style, following the ingestor's conflict handling for shared tables, so that re-running the migration is idempotent.
- When an SBOM has no suppliers, `suppliers()` returns an empty `Vec`. Skip the insert for that SBOM so that no records are produced (Test Requirement 2).
- Be defensive with stored data: if a stored SBOM document is missing or fails to parse, log it and skip it with `.context()`/`map_err` rather than panicking.
- Errors are wrapped with `.context()` or converted to `DbErr`, matching the m0001 convention.
- `down()` deletes the rows the migration inserted from `sbom_supplier`, or leaves them alone if the m0001 sibling uses a no-op pattern for data migrations.
- Add `#[cfg(test)] mod test;` so that the new test file is compiled.
- None of the extraction logic is duplicated. The migration only calls the ingestor's functions.

### 6.3 `migration/src/m0002_supplier/test.rs` (create)

See Step 7.

### Documentation impact

No public HTTP API, CLI or configuration changes, so no documentation updates. The only new public items are the two functions, and their `///` doc comments cover them.

## Step 7: Tests (`migration/src/m0002_supplier/test.rs`)

The two cases have different setup and different assertions, so they are written as separate tests rather than one parameterized test.

```rust
/// Verifies that suppliers declared in a sample SBOM are extracted into sbom_supplier rows.
#[test]
fn test_extracts_suppliers_from_sample_sbom() {
    // Given an SBOM describing one package with two declared suppliers
    let sbom = sample_sbom_with_suppliers(&["Acme Corp", "Red Hat"]);
    let sbom_id = Uuid::new_v4();

    // When computing supplier rows for the migration
    let rows = supplier_rows(sbom_id, &sbom);

    // Then each supplier is present with the correct SBOM link
    let names: Vec<_> = rows.iter().map(|r| r.supplier_name.as_str()).collect();
    assert_eq!(names, vec!["Acme Corp", "Red Hat"]);
    assert!(rows.iter().all(|r| r.sbom_id == sbom_id));
}

/// Verifies that an SBOM with no supplier metadata produces no sbom_supplier rows.
#[test]
fn test_sbom_without_suppliers_produces_no_records() {
    // Given an SBOM with no supplier metadata
    let sbom = sample_sbom_with_suppliers(&[]);

    // When computing supplier rows
    let rows = supplier_rows(Uuid::new_v4(), &sbom);

    // Then no records are produced
    assert_eq!(rows, vec![]);
}
```

- The assertions check actual values (supplier names and SBOM IDs), not just how many rows came back.
- If the sibling tests use a real PostgreSQL test database, add a database-backed variant. It runs `up()` against a seeded SBOM and then compares the `sbom_supplier` contents by value, which covers Acceptance Criterion 3.
- Run `cargo test -p <migration crate>` and `cargo test -p trustify-module-ingestor`. The crate names come from `cargo metadata --no-deps --format-version 1`.

## Step 8: Acceptance criteria

| Criterion | How it is satisfied |
|---|---|
| Extract suppliers from all ingested SBOMs | `up()` iterates over every SBOM in pages and calls `suppliers()` on each |
| Reuse existing ingestor logic, no duplication | `describing_packages` and `suppliers` become `pub` and are imported. No logic is copied |
| `sbom_supplier` filled correctly | Rows are built per supplier and linked to the SBOM. The database-backed test checks the contents by value |

## Step 9: Self-verification

- **Scope:** the expected diff is the three listed files. Possible files outside the listed scope, each to be **flagged for user approval rather than changed without asking**:
  - `migration/src/lib.rs`, if `m0002_supplier` is not already registered.
  - The `sbom_supplier` entity or schema in `entity/src/`, if it does not exist yet.
  - `modules/ingestor/src/lib.rs` or `graph/mod.rs`, if the module path to the functions is private.
- **Untracked files:** `test.rs` is new and is referenced through `mod test;`, so stage it.
- **Duplication check:** grep for `fn suppliers` and `fn describing_packages` across the workspace. The only definitions should be the ones in the ingestor.
- **Dead parameters:** none expected, because no code is removed.
- **Sensitive patterns:** none expected.
- **CI checks:** run every command extracted from CONVENTIONS.md. Any non-zero exit stops the run.
- **Rust tests:** run `cargo test -p` for both the migration crate and the ingestor crate.
- **Data flow:** stored SBOM, then parse into `Sbom`, then `describing_packages` + `suppliers`, then `supplier_rows`, then insert into `sbom_supplier`. The chain is complete as long as the entity and table exist (see the Step 4 discrepancy).
- **Query scope:** a full SBOM scan is intended, because the task says "all ingested SBOMs". It uses paging, and the reason is noted in a code comment.
- **Contract and sibling parity:**
  - The migration implements `MigrationTrait`, including `up`/`down`.
  - Its structure matches m0001.
  - Inserts follow the ingestor's conflict handling for the shared table.
  - The migration calls `suppliers()` the same way the ingestor's existing callers do.

## Step 10: Commit, push and open the PR

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): extract SBOM suppliers into sbom_supplier

Make describing_packages() and suppliers() in the ingestor's graph::sbom
module public and reuse them from the m0002_supplier migration instead of
duplicating the extraction logic. The migration crate already depends on
trustify-module-ingestor, so no new cross-crate dependency is introduced.

Implements TC-9206"
```

Check whether an `upstream` remote exists, which would mean this is a fork. Then run `gh pr create --base main` (with `-R`/`--head` if it is a fork). The PR description includes:
- `Implements [TC-9206](<webUrl>)`
- The reuse rationale, as the skill requires for reuse versus duplication decisions
- `Closes <owner>/<repo>#<n>`, if the GitHub Issue field is set.

## Step 11: Update Jira

- Set `customfield_10875` to the PR URL using an ADF `inlineCard`.
- Add a comment with the PR link, a summary of the changes, and any deviations, such as the scope flags from Step 4/9. The comment ends with the implement-task footnote.
- Transition the issue to **In Review**.
