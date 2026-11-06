# Reuse Decision: TC-9206 — private ingestor helpers

## Functions in question

Both live in `modules/ingestor/src/graph/sbom/mod.rs` (crate `trustify-module-ingestor`):

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`: extracts the packages an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`: extracts supplier information from SBOM metadata

Both are private (`fn`, not `pub fn`). The `migration` crate needs exactly this logic.

## Decision: make them public and import them. Do not duplicate.

## Reasoning (implement-task Step 6, "Reuse over duplication")

1. **Is there already a dependency?** Yes. `migration/Cargo.toml` already declares
   `trustify-module-ingestor = { path = "../modules/ingestor" }` (stated in the task's
   Implementation Notes). Before editing, I would confirm this by reading
   `migration/Cargo.toml` with `mcp__serena_backend__search_for_pattern` or Read.
2. **Since it exists, reuse is the rule.** Making the functions `pub` adds no new
   coupling between crates, because migration -> ingestor is already a dependency.
   The only change is a wider API surface on the ingestor crate.
3. **DRY and keeping one source of truth.** Supplier and describing-package extraction
   is SBOM-format-specific logic (SPDX vs CycloneDX). If it were copied, a fix in one
   copy would not reach the other, and the migrated `sbom_supplier` data could drift
   from what new ingestion produces. One shared implementation keeps backfilled rows and
   newly ingested rows consistent.
4. **The task asks for it.** Implementation Notes say "make the functions public and
   import them rather than duplicating the code". Acceptance Criterion 2 says "The
   extraction reuses the existing ingestor logic rather than duplicating it".
   `modules/ingestor/src/graph/sbom/mod.rs` is listed in Files to Modify for this purpose.
5. **When duplication would have been acceptable:** only if `migration` did not
   already depend on `trustify-module-ingestor`. Adding a whole new cross-crate
   dependency for two small helpers might not be worth the coupling. That is not the
   case here.

## How it will be done

- Change `fn describing_packages` to `pub fn describing_packages` and `fn suppliers` to
  `pub fn suppliers`.
- Add a `///` doc comment to each, since they become public API. Each comment says what
  the function returns and how it handles SBOMs that lack the data (an empty `Vec`).
- Make sure the signature types (`PackageRef`, `SupplierInfo`, `Sbom`) are reachable
  from outside the crate. If they are private, make them `pub` too, because the
  functions cannot be used without them (Rust's `private_interfaces` lint would also
  flag this).
- Make sure the module path is reachable: `graph` must be `pub mod graph` in
  `modules/ingestor/src/lib.rs`, and `sbom` must be `pub mod sbom` in
  `modules/ingestor/src/graph/mod.rs`. I would check both with
  `mcp__serena_backend__get_symbols_overview`. If either is private, the fix
  touches files outside Files to Modify. I would flag that to the user for approval
  (Step 9 scope containment) and not change it silently.
- Choose `pub` over `pub(crate)`, because the caller is in another crate.
- Run `find_referencing_symbols` on both functions to confirm existing callers inside the
  ingestor are unaffected. Only visibility changes, not signature or behaviour, so
  nothing should break.
- In the migration: `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`

## Flagging for reviewers

The commit body and PR description will both say:

> Made `describing_packages()` and `suppliers()` in `trustify-module-ingestor` public
> and reused them from the `migration` crate instead of duplicating them. `migration`
> already depends on `trustify-module-ingestor`, so no new coupling is introduced, and
> migrated supplier data stays consistent with ingestion-time extraction.
