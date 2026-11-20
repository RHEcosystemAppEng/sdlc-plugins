# Reuse Decision: TC-9206 — `describing_packages()` and `suppliers()`

## Decision

**Make both functions public in the ingestor crate and import them from the migration crate. Do NOT duplicate them.**

- `modules/ingestor/src/graph/sbom/mod.rs`:
  - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` becomes `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
  - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` becomes `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`
- `migration/src/m0002_supplier/mod.rs`:
  - `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`

## How I decided (implement-task Step 6, "Reuse over duplication")

1. **Is the source crate already a dependency of the target crate?**
   Yes. The task's Implementation Notes quote `migration/Cargo.toml`:
   ```toml
   [dependencies]
   trustify-module-ingestor = { path = "../modules/ingestor" }
   ```
   In a real run I would check this directly in `migration/Cargo.toml` (Read or
   `mcp__serena_backend__search_for_pattern`) and not just trust the task text.
   Because the dependency already exists, making the functions public adds no new
   coupling between crates.

2. **The dependency exists, so make them public and import them.**
   - **DRY / one source of truth:** these functions are the logic that decides
     which packages an SBOM describes and who its suppliers are. If the migration
     had its own copy, the two could drift apart. A future fix to the ingestor
     (for example, CycloneDX vs SPDX supplier handling) would then not reach the
     migration, and the `sbom_supplier` rows backfilled by the migration would
     differ from the rows written at ingest time.
   - **Acceptance criterion:** "The extraction reuses the existing ingestor logic
     rather than duplicating it." Duplicating the code would fail this criterion.
   - **Task instruction:** the Implementation Notes say outright: "make the
     functions public and import them rather than duplicating the code." The
     Files to Modify section also lists the ingestor file for this change.

3. **When duplication would be acceptable (not the case here):** only if using
   the functions meant adding a new cross-crate dependency just for one utility.
   That is not the case here.

4. **Recording the decision:** the commit body and the PR description will say
   that the functions were made `pub` so the migration crate can reuse them, and
   that duplication was rejected because `trustify-module-ingestor` is already a
   dependency.

## Things to check so `pub` actually works across crates

Changing `fn` to `pub fn` is not enough on its own. I would check these with
`mcp__serena_backend__get_symbols_overview` / `find_symbol` before editing:

- **Module path visibility:** `modules/ingestor/src/lib.rs` must declare
  `pub mod graph;` and `graph/mod.rs` must declare `pub mod sbom;`. Otherwise the
  functions cannot be reached at `trustify_module_ingestor::graph::sbom::*`. If
  either module is private, changing it touches `lib.rs` or `graph/mod.rs`. Those
  files are outside the task's listed scope, so I would flag them in the Step 9
  scope check for user approval. The alternative is a narrow `pub use`
  re-export, which also needs approval.
- **Type visibility:** `Sbom`, `PackageRef` and `SupplierInfo` appear in the
  signatures and must also be `pub` and reachable from outside the crate.
  Otherwise the compiler reports `private type in public interface`, or the
  caller cannot name the types. If they are private, making them public is part
  of the same in-scope change to `graph/sbom/mod.rs`, as long as they are
  defined in that file.
- **Use the narrowest visibility that works:** `pub(crate)` is not enough
  because the caller is in another crate, so plain `pub` is needed. I would not
  widen visibility on anything else.
- **Callers inside the ingestor:** `find_referencing_symbols` on both functions
  to confirm the signature stays the same. Only visibility changes, so existing
  callers are unaffected.
- **Documentation:** add `///` doc comments to both functions, because they are
  now public API (Step 6, "Documentation on new symbols"/public functions).
- **Lints:** check whether the workspace enables `missing_docs` or
  `unreachable_pub`. The doc comments handle the first. The second does not apply
  once the functions are used from outside the crate.

## Trade-off I noted but did not act on

Migration crates are sometimes kept independent of application code, so that
old migrations keep producing the same result as the application changes. That
argues for freezing a copy of the logic inside the migration. Here, though, the
dependency already exists, and the task and acceptance criteria explicitly ask
for reuse. So I follow the skill rule and do not duplicate. I would mention this
in the PR description so reviewers can weigh it.
