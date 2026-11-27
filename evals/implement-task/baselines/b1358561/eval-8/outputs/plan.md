# Implementation Plan: TC-9206 — Add SBOM supplier extraction to data migration

## Step 0 – Project Configuration validation
`claude-md-mock.md` has all three required sections:
- Repository Registry: `trustify-backend`, Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142 (plus PR field `customfield_10875` and GitHub Issue field `customfield_10747`)
- Code Intelligence: naming convention `mcp__<instance>__<tool>`, with `serena_backend` (rust-analyzer)

Result: PASS. The skill continues.

## Step 1 – Parsed task
| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Target PR | none |
| Bookend Type | none |
| **Mode** | **default** (branch `TC-9206` from `main`, PR → `main`) |
| Dependencies | None |
| GitHub Issue (customfield_10747) | I would read this from the fetched issue. It is not in the mock, so I would skip it without comment. |

Every required section is present, so the skill continues.

## Step 1.5 – Description integrity
I would fetch the comments and look for `[sdlc-workflow] Description digest:`. If one exists, I would run `scripts/sha256-digest.py` on the description and compare the two digests. If none exists, I would log a warning and continue. (Not executed: no external calls in this eval.)

## Step 2 – Dependencies
"Depends on: None", so there is nothing to check.

## Step 3 – Jira
`jira.user_info()`, then assign TC-9206 to the current user, then move it to **In Progress**. (Not executed.)

## Step 4 – Understand the code (planned Serena calls on `serena_backend`)
1. `get_symbols_overview("modules/ingestor/src/graph/sbom/mod.rs")`: confirm that `describing_packages` and `suppliers` exist and are private.
2. `find_symbol("describing_packages", include_body=true)` and `find_symbol("suppliers", include_body=true)`: confirm the signatures
   `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` and `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`.
3. `find_symbol("PackageRef")`, `find_symbol("SupplierInfo")`, `find_symbol("Sbom")`: check whether the parameter and return types are public. A `pub fn` cannot expose a private type (`private type in public interface`), so these may need `pub` too.
4. `get_symbols_overview("modules/ingestor/src/lib.rs")` and `("modules/ingestor/src/graph/mod.rs")`: check that the module path `graph::sbom` can be reached from outside the crate (`pub mod graph;` and `pub mod sbom;`).
5. `find_referencing_symbols` on both functions: list the current callers inside the ingestor. Changing visibility does not break callers, but I need the list for parity.
6. `search_for_pattern("trustify-module-ingestor", paths="migration/Cargo.toml")`: confirm the dependency exists. The task says it already does.
7. Check whether `migration/src/m0002_supplier/` exists. The repo snapshot shows only `migration/src/m0001_initial/mod.rs`, and the task lists `m0002_supplier/mod.rs` under "Files to Modify". I would look at `migration/src/lib.rs` (the migrator registration list) and `m0001_initial/mod.rs` as the sibling pattern.
8. Look for an entity or table definition for `sbom_supplier` (`entity/src/`). The snapshot has none.
9. Read `CONVENTIONS.md` at the repo root: get the CI check commands for Step 9 and the naming and test conventions.
10. Duplication search: `search_for_pattern("supplier")` and `("describing")` across the workspace, to confirm there is no other copy of this logic.

### Conventions to apply (from the repo-backend summary; I would confirm against siblings)
- Error handling: `Result<T, _>` with `.context()` wrapping. In migrations this becomes `DbErr` mapping, following `m0001_initial`.
- SeaORM for DB access. Migrations implement `MigrationTrait` (`up`/`down`), following `m0001_initial`.
- Naming: snake_case, `mNNNN_<name>` migration modules.
- Tests: assert on values, put a `///` doc comment on every test, and use given/when/then comments.

## Step 5 – Branch
```
git checkout main && git pull && git checkout -b TC-9206
```

## Step 6 – Changes

### 1. `modules/ingestor/src/graph/sbom/mod.rs` (modify, in scope)
- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` becomes `pub fn describing_packages(...)`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` becomes `pub fn suppliers(...)`
- Add a `///` doc comment to each, because they are now public API:
  - `/// Returns the packages that the given SBOM declares it describes (its top-level subjects).`
  - `/// Extracts supplier information from the SBOM's metadata; returns an empty vec when no supplier is declared.`
- Leave the function bodies unchanged. This is a visibility-only change, made with Serena `replace_symbol_body` or a one-token Edit.
- If Step 4 shows that `PackageRef` / `SupplierInfo` (or their fields the migration reads) are private, make them `pub` in the same file. This stays within the listed file.

### 2. `migration/src/m0002_supplier/mod.rs` (modify per task; may need creating, see flags)
Add the supplier extraction step, reusing the ingestor helpers:
```rust
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```
Logic in `up()`:
1. Create the `sbom_supplier` table, if this migration owns its schema. Follow how `m0001_initial` builds tables (columns such as `sbom_id` FK → `sbom.id`, supplier name, and package ref if needed).
2. Read every ingested SBOM in pages or batches. This must not be limited to one subset (query-scope check #12).
3. For each SBOM, load or parse it into the `Sbom` type the helpers expect, then call `describing_packages(&sbom)` and `suppliers(&sbom)`.
4. Map each `SupplierInfo` to an `sbom_supplier` row and insert in batches. If `suppliers()` returns empty, insert nothing for that SBOM.
5. Guard against missing data at the module boundary: skip SBOMs whose document cannot be loaded (log or warn, matching sibling style), and use `unwrap_or_default()` on optional supplier fields.
- `down()`: drop the `sbom_supplier` table, or delete its rows.
- Extract a small pure function, such as `fn supplier_rows(sbom_id, &Sbom) -> Vec<sbom_supplier::ActiveModel>` (or a plain struct), that wraps the two imported helpers. Unit tests can then call it without a DB. It only maps data and does not reimplement the extraction.
- Add `#[cfg(test)] mod test;` to register the new test file.
- Doc comments go on the migration struct and on the new helper.

### 3. `migration/src/m0002_supplier/test.rs` (create)
```rust
/// Verifies that supplier rows are produced for each supplier declared in a sample SBOM.
#[test]
fn extracts_suppliers_from_sample_sbom() {
    // Given an SBOM whose metadata declares suppliers "Acme Corp" and "Example Ltd"
    // When building supplier rows for the migration
    // Then the rows contain exactly those supplier names linked to the SBOM id
    //   (assert_eq! on the collected names/ids, not just the length)
}

/// Verifies that an SBOM without supplier metadata yields no supplier records.
#[test]
fn sbom_without_suppliers_produces_no_records() {
    // Given an SBOM with no supplier metadata
    // When building supplier rows
    // Then the result is empty
}
```
- The two tests set up different inputs and assert different things, so they stay as separate tests and are not parameterized.
- If the siblings or CONVENTIONS show that migration tests run against a DB (the `tests/` crate uses a real PostgreSQL), add an async DB-backed test that runs the migration and checks the contents of `sbom_supplier`. That covers the acceptance criterion "table is populated correctly".

### Reuse decision (summary; full rationale in reuse-decision.md)
**Make the functions public and import them. Do not duplicate them.** `migration/Cargo.toml` already depends on `trustify-module-ingestor`, so this is rule 2 of the skill's Reuse section ("Exists but is not exported, and its package is already a dependency: make it public and import it"). No new cross-crate dependency is added. I would record this choice in the commit body and the PR description.

## Step 7 – Tests
Run `cargo test -p <crate>` for each modified crate (see Step 9 #15).

## Step 8 – Acceptance criteria
- Extracts suppliers from **all** ingested SBOMs: the batch loop covers the full `sbom` table.
- Reuses existing ingestor logic: imports `describing_packages` / `suppliers` and adds no copied code.
- `sbom_supplier` populated correctly: covered by the value-based tests and an optional DB test.

## Step 9 – Self-verification (planned)
| # | Check | Expected result |
|---|---|---|
| 1 | Scope containment | Possible FLAGGED items: `migration/src/lib.rs` (registering `m0002_supplier::Migration` in the `Migrator` list), `entity/src/sbom_supplier.rs` and `entity/src/lib.rs` (if a SeaORM entity is needed), and `modules/ingestor/src/lib.rs` / `graph/mod.rs` (if `pub mod` is needed to reach the functions). Each would be listed for user approval before commit. |
| 2 | Untracked files | Only `m0002_supplier/test.rs` and possibly `mod.rs`, both expected. |
| 3 | Sensitive patterns | PASS |
| 4 | Dead parameters | Not triggered (nothing removed) |
| 5 | Duplication | PASS. The extraction logic is imported, not rewritten. A grep for `supplier` should find only the ingestor definition and the migration call site. |
| 6 | Doc currency | Public API added to the ingestor (two `pub fn`). Doc comments are added. Check whether `docs/architecture.md` mentions ingestor internals; if so, flag it rather than edit it. |
| 10 | Cross-section refs | The task's file paths match the plan. Flag that `m0002_supplier/` is missing from the snapshot. |
| 11 | Data-flow trace | SBOM row → `Sbom` → `suppliers()` → `sbom_supplier` rows → insert |
| 12 | Query scope | Iterate all SBOMs with pagination, not a filtered subset |
| 13 | Sibling parity | Migration structure matches `m0001_initial`, and the existing ingestor callers are unchanged |
| 14 | CI checks | Commands from CONVENTIONS.md (for example `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`). Clippy may warn about now-public items that lack docs; the doc comments cover that. |
| 15 | Module tests | `cargo metadata --no-deps --format-version 1` maps the files to crates, then `cargo test -p trustify-module-ingestor` and `cargo test -p <migration crate name from metadata>` |

## Step 10 – Commit and PR
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(migration): extract SBOM suppliers into sbom_supplier table

Add m0002_supplier migration step that populates sbom_supplier for all
ingested SBOMs. Reuses the ingestor's describing_packages() and
suppliers() helpers, made public, instead of duplicating them; the
migration crate already depends on trustify-module-ingestor, so no new
dependency is introduced.

Implements TC-9206"
```
- Fork detection: `git remote get-url upstream`
- `gh pr create --base main`. The body has `Implements [TC-9206](<webUrl>)`, the reuse rationale, and a `Closes owner/repo#N` line only if the GitHub Issue field is set.

## Step 11 – Jira
- Set `customfield_10875` to the PR URL as an ADF inlineCard.
- Comment with the PR link, a summary, and deviations (any approved out-of-scope files such as `migration/src/lib.rs`), ending with the implement-task footnote.
- Transition to **In Review**.

## Open questions / flags for the user
1. `migration/src/m0002_supplier/mod.rs` is listed under "Files to Modify", but the snapshot has no such directory. I would confirm whether to create it, and approve registering it in `migration/src/lib.rs`.
2. The snapshot has no `sbom_supplier` entity or table. I need to know whether this migration creates the table or an earlier change does.
3. If the ingestor's `graph` / `graph::sbom` modules or the `PackageRef` / `SupplierInfo` types are not public, more visibility changes are needed.
