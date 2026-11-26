# Reuse Decision: TC-9206 — private ingestor helpers

## Decision

**Make `describing_packages()` and `suppliers()` public in the ingestor crate and import them
from the migration crate. Do NOT duplicate them.**

## Functions in question

Located in `modules/ingestor/src/graph/sbom/mod.rs` (crate `trustify-module-ingestor`):

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` — packages an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` — supplier info from SBOM metadata

Both are currently private (`fn`, not `pub fn`). The migration step in
`migration/src/m0002_supplier/mod.rs` needs exactly this logic.

## Rationale (implement-task Step 6, "Reuse over duplication")

1. **Check dependency relationship** — `migration/Cargo.toml` already declares:
   ```toml
   [dependencies]
   trustify-module-ingestor = { path = "../modules/ingestor" }
   ```
   (Stated in the task's Implementation Notes; in a live run I would confirm this by reading
   `migration/Cargo.toml` via `mcp__serena_backend__search_for_pattern` / Read before editing.)
2. **The dependency already exists** -> the skill rule says to make the function public and
   import it rather than duplicate it. No new cross-crate coupling is introduced, so the
   usual reason for duplication (avoiding a new dependency for a single utility) does not apply.
3. **DRY / single source of truth** — the migration must produce the same supplier data the
   ingestor produces at ingest time. If the logic were copied, a future bug fix in the
   ingestor would silently diverge from the migration, and backfilled `sbom_supplier` rows
   would differ from newly-ingested ones.
4. **Task alignment** — the task explicitly lists `modules/ingestor/src/graph/sbom/mod.rs` in
   Files to Modify ("make `describing_packages()` and `suppliers()` public"), its
   Implementation Notes say "make the functions public and import them rather than
   duplicating the code", and the Acceptance Criteria require "the extraction reuses the
   existing ingestor logic rather than duplicating it". So the change is in scope, and no
   convention conflict needs to go back to the user.

Duplication would only be acceptable if `migration` did **not** already depend on
`trustify-module-ingestor` and adding that dependency would bring in unwanted coupling.
That is not the case here.

## Things the change needs (to be checked during Step 4)

- **Visibility of the whole path**: `pub fn` alone is not enough. The modules on the way
  (`graph` in `modules/ingestor/src/lib.rs`, `sbom` in `modules/ingestor/src/graph/mod.rs`)
  must be `pub mod`, or the functions must be re-exported. I would check this with
  `mcp__serena_backend__get_symbols_overview` on `lib.rs` and `graph/mod.rs`. If either
  module is private, changing it means editing a file outside Files to Modify, so I would
  flag it for user approval (Step 9 scope containment) and not change it silently.
- **Visibility of the types**: `PackageRef` and `SupplierInfo` (and `Sbom` as used in the
  signatures) must also be public, or the now-public functions cannot be called from another
  crate (and rustc gives a `private_interfaces` warning). If they are defined in the same
  file, mark them `pub` too. That keeps the change inside the listed file.
- **Least visibility**: `pub(crate)` is not enough here because the caller is in another
  crate, so plain `pub` is needed.
- **No behaviour change**: only the visibility changes. The function bodies stay the same.
  I would run `mcp__serena_backend__find_referencing_symbols` to confirm the existing callers
  inside the ingestor are unaffected.
- **Documentation**: add a `///` doc comment to each newly-public function and type (Step 6
  code-quality rule for public symbols).

## How the decision will be shown to reviewers

As Step 6 item 4 requires, the commit message body and the PR description will say:

> Made `describing_packages()` and `suppliers()` in `trustify-module-ingestor` public and
> imported them in the m0002_supplier migration instead of duplicating them. `migration`
> already depends on `trustify-module-ingestor`, so no new coupling is added, and the
> migration and ingest-time extraction now share one implementation.
