# Reuse Decision — TC-9206: private ingestor helpers

## Functions in question

Both live in `modules/ingestor/src/graph/sbom/mod.rs` (crate `trustify-module-ingestor`) and are currently private:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`: extracts the packages an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`: extracts supplier information from SBOM metadata

The consumer is the `migration` crate (`migration/src/m0002_supplier/mod.rs`).

## Decision: **make them public (`pub fn`) and import them. Do NOT duplicate them.**

## Rationale (following the implement-task skill's "Reuse over duplication" rule)

1. **Check the dependency relationship.** The skill says to check the dependency manifest first. The task's Implementation Notes quote `migration/Cargo.toml`:
   ```toml
   [dependencies]
   trustify-module-ingestor = { path = "../modules/ingestor" }
   ```
   During Step 4 I would confirm this directly by reading `migration/Cargo.toml` (via Serena `search_for_pattern` on `serena_backend`, or Read). The edge `migration -> trustify-module-ingestor` **already exists**.
2. **The dependency already exists, so promote and import.** Making the functions `pub` adds no new crate coupling, no new build edge and no risk of a dependency cycle. Duplicating them would create two copies of the SBOM supplier and describing-package extraction logic. Those copies would drift apart, and future bug fixes (for example to SPDX/CycloneDX supplier parsing) would have to be applied twice. If they were not applied twice, migrated data would differ from freshly ingested data, which is a real correctness risk.
3. **When duplication would be acceptable (and why that case does not apply).** Inlining is only justified when using the function would mean adding a *new* cross-crate dependency just for one utility. That is not the case here.
4. **The task agrees.** The Implementation Notes say "make the functions public and import them rather than duplicating the code". The Acceptance Criteria require "The extraction reuses the existing ingestor logic rather than duplicating it". `modules/ingestor/src/graph/sbom/mod.rs` is listed in Files to Modify for exactly this purpose.

## Visibility details

- Use `pub`, not `pub(crate)`. `pub(crate)` would still be invisible to the `migration` crate.
- Add a `///` doc comment to each newly public function. The skill requires docs on public functions, and these now form part of the ingestor crate's API.
- **Check the whole path is reachable (Step 4).** A `pub fn` is only importable if every module on the path is public: `lib.rs` must declare `pub mod graph;` and `graph/mod.rs` must declare `pub mod sbom;`. Its signature types (`Sbom`, `PackageRef`, `SupplierInfo`) must also be `pub`, or the compiler raises `private type in public interface` errors.
  - If `Sbom`, `PackageRef` or `SupplierInfo` are defined in `graph/sbom/mod.rs`, making them `pub` is in scope.
  - If the module chain or the types live in `lib.rs`, `graph/mod.rs` or another file outside Files to Modify, I would **not** silently edit those files. I would flag them under Step 9 scope containment and ask the user to approve the extra `pub mod` / `pub struct` change. The alternative is a `pub use` re-export, but that also needs an out-of-scope file.
- Check backward compatibility with `find_referencing_symbols` on both functions. Widening visibility never breaks existing callers inside the ingestor crate, so there are no signature changes and no caller updates.

## Commit / PR disclosure

As the skill requires, the decision is stated for reviewers. Commit body:

> Make `describing_packages()` and `suppliers()` in trustify-module-ingestor public and
> reuse them from the m0002_supplier migration instead of duplicating the logic. The
> migration crate already depends on trustify-module-ingestor, so no new dependency
> is introduced.

The PR description gets a matching "Reuse decision" section.
