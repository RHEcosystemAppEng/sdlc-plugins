# Implementation Plan: TC-9206 — Add SBOM supplier extraction to data migration

Simulated run of `/sdlc-workflow:implement-task TC-9206`. No repository files were changed
and no external tools were called (Jira, git, Serena). This document lists the steps the
skill would take.

---

## Step 0 – Validate Project Configuration

The mock CLAUDE.md contains:
- Repository Registry: `trustify-backend` -> Serena instance `serena_backend`, path `./` (OK)
- Jira Configuration: project key TC, Cloud ID, Feature issue type ID 10142, Git PR field
  `customfield_10875`, GitHub Issue field `customfield_10747` (OK)
- Code Intelligence: naming convention `mcp__<serena-instance>__<tool>`. Limitation:
  rust-analyzer needs 30–60 s to index on first use. (OK)

Result: the configuration is valid, so the run continues.

## Step 0.5 / 1 – Fetch and parse task (simulated)

Would call `jira.get_issue(TC-9206)` (MCP first, REST fallback only if the user agrees).
Parsed sections:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Files to Modify | `migration/src/m0002_supplier/mod.rs`, `modules/ingestor/src/graph/sbom/mod.rs` |
| Files to Create | `migration/src/m0002_supplier/test.rs` |
| API Changes | none |
| Target PR / Bookend Type / Review Context | absent, so the default flow applies |
| Dependencies | None |

All required sections are present. The GitHub Issue field (`customfield_10747`) would be read
from the issue. If it is empty, it is skipped silently.

## Step 1.5 – Description integrity

Would call `jira.get_issue_comments(TC-9206)`, find the latest comment starting with
`[sdlc-workflow] Description digest:`, and compare it with
`python3 scripts/sha256-digest.py /tmp/desc-TC-9206.txt`. If there is no digest, log a warning
and continue. If the digests do not match, stop and ask the user.

## Step 2 – Dependencies

None, so nothing to check.

## Step 3 – Assign and transition (simulated)

`jira.user_info()` -> `jira.edit_issue(TC-9206, assignee=<me>)` -> transition to **In Progress**.

## Step 4 – Understand the code (via `serena_backend`)

Planned inspections:
1. `mcp__serena_backend__get_symbols_overview` on `modules/ingestor/src/graph/sbom/mod.rs`:
   find `describing_packages`, `suppliers`, `PackageRef`, `SupplierInfo`, `Sbom`.
2. `mcp__serena_backend__find_symbol` (include_body=true) on `describing_packages` and
   `suppliers` to confirm the signatures match the Implementation Notes.
3. `mcp__serena_backend__find_referencing_symbols` on both functions to list the current
   ingestor callers, so I can confirm a visibility-only change does not break them.
4. `get_symbols_overview` on `modules/ingestor/src/lib.rs` and
   `modules/ingestor/src/graph/mod.rs` to check that `graph` and `sbom` are `pub mod`.
   The function is only reachable from the migration crate if the whole path is public.
5. Read `migration/Cargo.toml` to confirm the
   `trustify-module-ingestor = { path = "../modules/ingestor" }` dependency.
6. Sibling and convention analysis: `migration/src/m0001_initial/mod.rs` and
   `migration/src/lib.rs` for the migration struct pattern (`MigrationTrait`, `up`/`down`,
   `DeriveMigrationName`) and how migrations are registered in `Migrator::migrations()`.
7. Read `CONVENTIONS.md` at the repo root. Record the CI check commands (fmt, clippy, check,
   test) and any code-generation commands for Step 9.
8. Documentation files: `README.md`, `docs/architecture.md`. These probably need no update
   because no public API or endpoint changes.

### Discrepancies found in the provided repo structure (raise before implementing)

- **`migration/src/m0002_supplier/mod.rs` does not exist.** The repo tree only has
  `migration/src/m0001_initial/`, but the task lists the m0002 file under *Files to
  Modify*. I would ask the user whether this file is expected to come from a not-yet-merged
  change, or whether it should be treated as a file to create. Because of the Cross-section
  reference consistency rule, I would not just assume.
- **Migration registration.** A new `m0002_supplier` module must be declared
  (`mod m0002_supplier;`) and added to `Migrator::migrations()` in `migration/src/lib.rs`.
  That file is **not** in Files to Modify. If the registration is not already there, it
  needs user approval as an out-of-scope change.
- **`sbom_supplier` table/entity.** No `entity/src/sbom_supplier.rs` exists. The migration
  can create or insert into the table using SeaQuery `Table`/`Iden` definitions local to the
  migration, which is the usual SeaORM migration pattern and avoids depending on the entity
  crate. If a SeaORM entity is wanted, that is out of scope and must be flagged.
- **Module path visibility.** If `graph` or `graph::sbom` is private in the ingestor crate,
  making it public touches `lib.rs` / `graph/mod.rs`, which are out of scope. I would flag
  this for approval, or suggest a `pub use` re-export.

### Discovered conventions (binding for Steps 6–7)

- Error handling: `Result<T, AppError>`/`anyhow` with `.context()` wrapping. Migrations
  return `Result<(), DbErr>`, as in `m0001_initial`.
- Naming: `snake_case` verb_noun functions. Migration modules named `mNNNN_<topic>`.
- Tests: `assert_eq!` value-based checks. Integration tests use a real PostgreSQL test DB.

## Step 5 – Branch (simulated)

```
git checkout main && git pull && git checkout -b TC-9206
```

## Step 6 – Implement changes

### 6a. `modules/ingestor/src/graph/sbom/mod.rs` (modify)

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -> `pub fn describing_packages(...)`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -> `pub fn suppliers(...)`
- If `PackageRef` / `SupplierInfo` are defined in this file and are private, make them `pub`
  (and make their fields public or add accessors as the migration needs) so the public
  signatures do not expose private types.
- Add `///` doc comments to each newly-public function and type, for example:
  - `/// Returns the packages this SBOM declares it describes (its top-level subjects).`
  - `/// Extracts supplier information declared in the SBOM metadata.`
- The function bodies do not change. This is a visibility-only change.

### 6b. `migration/src/m0002_supplier/mod.rs` (modify)

- `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`
  (the exact path is confirmed in Step 4). **No copy of the extraction logic in the
  migration crate.**
- In `MigrationTrait::up`:
  1. Load ingested SBOMs, all of them, as the acceptance criterion says ("all ingested
     SBOMs"). Because the scope covers every SBOM, a broad query is intentional, and a code
     comment will say so (Step 9 query-scope rule). Load in pages or a stream to limit memory.
  2. Parse/reconstruct each SBOM into the `Sbom` type the helpers take.
  3. Call `describing_packages(&sbom)` and `suppliers(&sbom)`.
  4. Insert one `sbom_supplier` row per supplier (sbom_id + supplier fields, linked to the
     describing package where applicable). Use `ON CONFLICT DO NOTHING` so the migration can
     be re-run safely, which matches the ingestor's conflict handling (cross-module entity
     parity check).
  5. If an SBOM has no suppliers, insert no rows. Use `.unwrap_or_default()` / empty-vec
     guards on data that comes from the ingestor (defensive access across the crate
     boundary).
- `down`: delete the rows the migration added (or leave as a no-op, following the
  m0001 sibling).
- Add `#[cfg(test)] mod test;` to wire in the new test file.
- Use `.context()`-style error wrapping, mapped to `DbErr` where the migration API needs it.

### 6c. Documentation impact

There is no Documentation Updates section, and no public API, endpoint, or config changes.
No doc edits are expected.

## Step 7 – Tests: `migration/src/m0002_supplier/test.rs` (create)

Following sibling conventions, each test gets a `///` doc comment and given/when/then comments:

1. `/// Verifies the migration extracts the expected suppliers from a sample SBOM.`
   `test_extracts_suppliers_from_sample_sbom`. Given a sample SBOM fixture with known
   suppliers ingested into the test DB, when the m0002 `up` step runs, then the
   `sbom_supplier` rows match the expected supplier names and sbom_id values, asserted with
   `assert_eq!` on the actual values and not only the row count.
2. `/// Verifies an SBOM without supplier metadata produces no sbom_supplier rows.`
   `test_sbom_without_suppliers_produces_no_records`. Given an SBOM with no suppliers, when
   the migration runs, then the query returns an empty vec (`assert_eq!(rows, vec![])`).

These two cases differ in setup and assertions, so they stay as separate tests and are not
parameterized (Meszaros heuristic).

Run: `cargo test -p trustify-migration` and `cargo test -p trustify-module-ingestor`
(the package names come from `cargo metadata --no-deps --format-version 1`).

## Step 8 – Acceptance criteria

| Criterion | How it is met |
|---|---|
| Migration extracts suppliers from all ingested SBOMs | `up` goes through every SBOM and calls `suppliers()` |
| Extraction reuses existing ingestor logic | Imports the now-`pub` `describing_packages`/`suppliers`. No duplicate code |
| `sbom_supplier` table populated correctly | Covered by test 1 (value assertions) and test 2 (empty case) |

## Step 9 – Self-verification

- **Scope containment**: the expected diff is the 2 modified files and 1 new file. Any change
  to `migration/src/lib.rs`, `modules/ingestor/src/lib.rs`, `graph/mod.rs`, or `entity/` is
  flagged for explicit user approval.
- **Duplication check**: grep the migration crate for supplier/describing-package logic to
  confirm nothing was re-implemented.
- **Dead parameters**: none expected, because only visibility changes.
- **Sensitive patterns**: run the `git diff --cached | grep` check.
- **CI checks**: run every command from `CONVENTIONS.md` (for example `cargo fmt --check`,
  `cargo clippy -- -D warnings`, `cargo check`). Any non-zero exit is a hard stop.
- **Rust module tests**: `cargo test -p` for both the migration and ingestor crates.
- **Data flow**: stored SBOM -> parse to `Sbom` -> `describing_packages`/`suppliers` ->
  insert into `sbom_supplier` -> checked by tests. Every stage is connected.
- **Contract and sibling parity**: `MigrationTrait` `up`/`down` implemented. Same structure
  as m0001. Conflict handling matches the ingestor's inserts. The existing ingestor callers
  of the two helpers are unchanged.

## Step 10 – Commit and PR (simulated)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): extract SBOM suppliers in m0002 migration

Make describing_packages() and suppliers() in trustify-module-ingestor public
and reuse them in the m0002_supplier migration instead of duplicating the
logic. The migration crate already depends on trustify-module-ingestor, so no
new coupling is introduced.

Implements TC-9206"
```

Check for fork (`git remote get-url upstream`), then `gh pr create --base main`. The PR body
includes `Implements [TC-9206](<webUrl>)`, the reuse rationale, and `Closes <owner>/<repo>#<n>`
if the GitHub Issue field is set.

## Step 11 – Jira (simulated)

- Set `customfield_10875` to the PR URL (ADF inlineCard).
- Add a comment with the PR link, a summary, and deviations (for example the
  m0002/lib.rs/entity scope questions above), ending with the implement-task footnote.
- Transition to **In Review**.

## Private-function handling (summary)

Make `describing_packages()` and `suppliers()` `pub` in
`modules/ingestor/src/graph/sbom/mod.rs`, plus their argument and return types if needed,
and import them in the migration. The `migration -> trustify-module-ingestor` dependency
already exists, so duplicating them is not justified. See `reuse-decision.md`.
