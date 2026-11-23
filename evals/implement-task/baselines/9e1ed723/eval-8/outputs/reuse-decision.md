# Reuse Decision — TC-9206: Private ingestor helpers

## Decision

**Make `describing_packages()` and `suppliers()` public (`pub fn`) in
`modules/ingestor/src/graph/sbom/mod.rs` and import them from the `migration` crate.
Do NOT duplicate them.**

## Functions in question

| Function | Location | Current visibility | Purpose |
|---|---|---|---|
| `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` | `modules/ingestor/src/graph/sbom/mod.rs` | private | Extracts the packages an SBOM describes |
| `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` | `modules/ingestor/src/graph/sbom/mod.rs` | private | Extracts supplier info from SBOM metadata |

## Rationale (following implement-task Step 6, "Reuse over duplication")

1. **Check dependency relationship** — The source package is `trustify-module-ingestor`;
   the target package is `migration`. Per the task's Implementation Notes,
   `migration/Cargo.toml` already declares:
   ```toml
   [dependencies]
   trustify-module-ingestor = { path = "../modules/ingestor" }
   ```
   In a real run I would confirm this by reading `migration/Cargo.toml`
   (`mcp__serena_backend__search_for_pattern` / Read) before editing.

2. **Dependency already exists → make public and import.** Because no new cross-crate
   dependency (and therefore no new coupling or dependency-cycle risk) is introduced,
   the skill's rule is to expose the function rather than copy it. Benefits:
   - DRY: one implementation of the extraction logic.
   - Bug fixes / format support changes (e.g. new SPDX/CycloneDX supplier fields)
     apply to both ingestion and migration automatically.
   - Guarantees the migration populates `sbom_supplier` with data identical to what
     fresh ingestion produces — a correctness property, not just style.
   - Directly satisfies Acceptance Criterion "The extraction reuses the existing
     ingestor logic rather than duplicating it".

3. **Duplication rejected** — duplication is only acceptable when reuse would require
   adding a *new* dependency. That is not the case here, so duplication would be
   unjustified code drift risk.

4. **The task explicitly agrees** — Files to Modify includes
   `modules/ingestor/src/graph/sbom/mod.rs` with "make `describing_packages()` and
   `suppliers()` public", and Implementation Notes say "make the functions public and
   import them rather than duplicating the code". No convention conflict exists.

## Supporting visibility changes

- The return/parameter types `PackageRef`, `SupplierInfo` (and `Sbom`, if it is local)
  must also be reachable from outside the crate, otherwise `pub fn` triggers the
  `private_interfaces` lint / cannot be used. Before editing I would run
  `mcp__serena_backend__find_symbol` on each type; any that are private get `pub`
  (these edits are in the same file, i.e. within scope). If a type lives in another
  file, that would be flagged as out-of-scope for user approval.
- The `graph::sbom` module path must be reachable: verify `modules/ingestor/src/lib.rs`
  has `pub mod graph;` and `graph/mod.rs` has `pub mod sbom;`. If either is private,
  that is an out-of-scope file and would be flagged for user approval (alternatively a
  `pub use` re-export could be proposed).
- Prefer `pub` over `pub(crate)` — `pub(crate)` would not be visible to `migration`.
- Add `///` doc comments to both newly public functions (skill requires docs on
  public symbols), describing inputs, return value, and that they are shared by the
  ingestor and the m0002 migration.
- Run `mcp__serena_backend__find_referencing_symbols` on both functions to confirm
  existing in-crate callers are unaffected (visibility widening is backward compatible;
  signatures remain unchanged).

## Flagging the decision for reviewers

Commit message body and PR description will state:

> `describing_packages()` and `suppliers()` in the ingestor's `graph::sbom` module were
> made public and are reused by the m0002_supplier migration instead of being
> duplicated. The `migration` crate already depends on `trustify-module-ingestor`, so
> no new dependency was introduced.
