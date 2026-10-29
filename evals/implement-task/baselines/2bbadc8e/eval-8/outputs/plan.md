# Implementation Plan for TC-9206

## Task Summary

Add SBOM supplier extraction to the data migration step. The migration crate needs to
extract describing packages and supplier information from ingested SBOMs to populate the
new `sbom_supplier` table, reusing existing private helper functions from the ingestor crate.

## Project Configuration Validation (Step 0)

Verified from CLAUDE.md:
- Repository Registry: present, contains `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: present with Project key TC, Cloud ID, Feature issue type ID
- Code Intelligence: present with tool naming convention `mcp__serena_backend__<tool>`

## Parsed Task Structure (Step 1)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add supplier extraction to migration using existing ingestor helpers
- **Files to Modify**:
  - `migration/src/m0002_supplier/mod.rs`
  - `modules/ingestor/src/graph/sbom/mod.rs`
- **Files to Create**:
  - `migration/src/m0002_supplier/test.rs`
- **Acceptance Criteria**: 3 items (supplier extraction, reuse over duplication, correct table population)
- **Test Requirements**: 2 items (correct extraction, empty-supplier handling)
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None

## Branch (Step 5)

```
git checkout main
git pull
git checkout -b TC-9206
```

## Code Understanding (Step 4)

### Files to inspect

1. **`modules/ingestor/src/graph/sbom/mod.rs`** -- Inspect using `mcp__serena_backend__get_symbols_overview` to see the structure, then `mcp__serena_backend__find_symbol` with `include_body=true` on `describing_packages` and `suppliers` to read their implementations. Confirm they are currently private (`fn`, not `pub fn`), understand their signatures, and verify their logic matches the migration's needs.

2. **`migration/src/m0002_supplier/mod.rs`** (to modify) -- Inspect current state to understand how the migration step is structured and where the supplier extraction logic should be added. Look at sibling migration `migration/src/m0001_initial/mod.rs` for conventions.

3. **`migration/Cargo.toml`** -- Verify that `trustify-module-ingestor` is already listed as a dependency. This is critical for the reuse decision.

4. **`migration/src/lib.rs`** -- Check how migration modules are registered (e.g., `mod m0002_supplier;`).

### Sibling convention analysis

- Inspect `migration/src/m0001_initial/mod.rs` for migration step patterns (naming, error handling, transaction usage).
- Inspect existing tests in the `migration` crate (if any) for test patterns.
- Inspect `modules/ingestor/src/graph/sbom/mod.rs` for code style around the target functions.

### Documentation files

- `README.md` at repo root
- `docs/architecture.md`
- `CONVENTIONS.md` at repo root -- read for CI check commands and project conventions

## Implementation Changes (Step 6)

### File 1: `modules/ingestor/src/graph/sbom/mod.rs` (modify)

**Change**: Make `describing_packages()` and `suppliers()` public.

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

**Rationale**: The migration crate already depends on `trustify-module-ingestor`. Making these functions public follows the "Reuse over duplication" principle from Step 6 of the skill. No new dependency is introduced, so reuse is strictly preferred over duplication. See `outputs/reuse-decision.md` for full analysis.

**Backward compatibility**: Use `mcp__serena_backend__find_referencing_symbols` on both functions to confirm that no existing callers are affected by the visibility change. Changing `fn` to `pub fn` is a purely additive change -- it cannot break any existing call site within the ingestor crate. External callers did not exist before (the functions were private), so there are no callers to break.

**Documentation**: Add a doc comment to each newly-public function explaining its purpose, since the skill requires documentation on all public/exported functions:

```rust
/// Extracts the list of packages that an SBOM describes.
///
/// Parses the SBOM document to identify top-level packages referenced
/// as the subject of the bill of materials.
pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> {
    // ... existing body unchanged ...
}

/// Extracts supplier information from SBOM metadata.
///
/// Returns supplier records derived from the SBOM's creation info
/// and package supplier fields.
pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> {
    // ... existing body unchanged ...
}
```

### File 2: `migration/src/m0002_supplier/mod.rs` (modify)

**Change**: Add supplier extraction logic that imports and calls the now-public functions from the ingestor crate.

- Add import: `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`
- In the migration step function, for each ingested SBOM:
  1. Call `describing_packages(&sbom)` to get the described packages
  2. Call `suppliers(&sbom)` to get supplier information
  3. Insert supplier records into the `sbom_supplier` table
- Follow the migration patterns observed in `m0001_initial/mod.rs` (error handling with `.context()`, transaction usage, SeaORM patterns)
- Add defensive guards on the returned data (e.g., handle empty vectors, null supplier names) per the "Defensive property access on external data" guidance

### File 3: `migration/src/m0002_supplier/test.rs` (create)

**Change**: Create unit tests for the supplier extraction migration step.

- **Test 1: `test_migration_extracts_suppliers_from_sbom`**
  - Doc comment: `/// Verifies that the migration step correctly extracts supplier information from a sample SBOM.`
  - Given: A sample SBOM with known supplier data
  - When: The migration step processes the SBOM
  - Then: The `sbom_supplier` table contains the expected supplier records with correct values (value-based assertions, not just count)

- **Test 2: `test_migration_handles_sbom_with_no_suppliers`**
  - Doc comment: `/// Verifies that SBOMs with no supplier metadata produce no supplier records.`
  - Given: A sample SBOM with no supplier information
  - When: The migration step processes the SBOM
  - Then: No records are inserted into `sbom_supplier` (assert empty result set)

- Follow test patterns from sibling tests (assertion style, test database setup/teardown if applicable)
- Use `assert_eq!` with specific values per skill guidance on value-based assertions

### Module registration

- Verify `migration/src/lib.rs` includes `mod m0002_supplier;` -- if the module declaration already exists (since the file is listed under Files to Modify, not Files to Create), no change is needed. If it is missing, flag as out-of-scope per Step 9 scope containment.

## Verification (Step 9)

### Scope containment
- Run `git diff --name-only` and verify only the three files listed above are modified/created
- If `migration/src/lib.rs` needed a module declaration, flag it for user approval

### CI checks
- Read `CONVENTIONS.md` and run all CI check commands extracted from it
- Run `cargo test -p trustify-migration` (module-level test requirement for Rust)
- Run `cargo test -p trustify-module-ingestor` (since we modified a file in that crate)

### Duplication check
- Grep for `describing_packages` and `suppliers` across the repo to confirm no duplicate implementations exist

### Data-flow trace
- Input: Ingested SBOMs in the database
- Processing: Migration step reads SBOMs, calls `describing_packages()` and `suppliers()` to extract data
- Output: Records inserted into `sbom_supplier` table
- All stages connected through the migration step function

## Commit and PR (Step 10)

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add SBOM supplier extraction to data migration

Import and reuse describing_packages() and suppliers() from the ingestor
crate (made public) rather than duplicating the extraction logic. The
migration step processes all ingested SBOMs and populates the sbom_supplier
table with extracted supplier information.

The dependency on trustify-module-ingestor already existed in migration/Cargo.toml,
so making the functions pub and importing them is preferred over code duplication
per the DRY principle.

Implements TC-9206"
```

PR base: `main`
PR description includes:
- Summary of changes (3 files, reuse decision)
- Implements [TC-9206](https://redhat.atlassian.net/browse/TC-9206)

## Jira Update (Step 11)

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add comment with PR link, summary of changes, and note about the reuse decision
- Transition TC-9206 to In Review
