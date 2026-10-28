# Implementation Plan for TC-9206: Add SBOM supplier extraction to data migration

## Task Summary

Add supplier information extraction during the SBOM data migration step so the new
`sbom_supplier` table is populated with supplier data extracted from ingested SBOMs.

## Project Configuration Validation

The project CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID present
- Code Intelligence: Tool naming convention documented, `serena_backend` configured with rust-analyzer

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Current state:** Contains two private helper functions:
- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata

**Changes:**
- Change `fn describing_packages(...)` to `pub fn describing_packages(...)` -- make the function public so it can be imported by the migration crate
- Change `fn suppliers(...)` to `pub fn suppliers(...)` -- make the function public so it can be imported by the migration crate
- Add documentation comments (`///`) to both functions describing their purpose, parameters, and return values, since they are now part of the public API

**Rationale:** The migration crate already depends on `trustify-module-ingestor` (see `migration/Cargo.toml`). Making these functions public and importing them follows the DRY principle and ensures that any future bug fixes or improvements to the extraction logic apply everywhere. See `outputs/reuse-decision.md` for the full analysis.

### 2. `migration/src/m0002_supplier/mod.rs`

**Current state:** Existing migration step module (structure to be confirmed via Serena/Read).

**Changes:**
- Add imports for the newly-public functions from the ingestor crate:
  ```rust
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- Implement the supplier extraction migration logic:
  1. Query all ingested SBOMs from the database
  2. For each SBOM, call `describing_packages(&sbom)` to get the packages the SBOM describes
  3. For each SBOM, call `suppliers(&sbom)` to extract supplier information
  4. Insert extracted supplier records into the `sbom_supplier` table
- Follow existing migration patterns from sibling `m0001_initial/mod.rs` for:
  - Error handling (use `Result<T, AppError>` with `.context()`)
  - Database transaction patterns
  - Logging conventions
- Add defensive guards on external data (null/empty checks on supplier fields using `.unwrap_or_default()` or similar Rust idioms)
- Add a documentation comment on the migration function explaining what it does

## Files to Create

### 3. `migration/src/m0002_supplier/test.rs`

**Changes:**
- Create unit tests for the supplier extraction migration step
- Follow test conventions from sibling test files in the migration crate

**Test cases:**

1. **`test_migration_extracts_suppliers_from_sbom`**
   - Doc comment: `/// Verifies that the migration step correctly extracts suppliers from a sample SBOM.`
   - Given: A sample SBOM with known supplier metadata
   - When: The migration step processes the SBOM
   - Then: The `sbom_supplier` table contains the expected supplier records with correct field values
   - Use value-based assertions (assert on specific supplier names/fields, not just count)

2. **`test_migration_handles_sbom_with_no_suppliers`**
   - Doc comment: `/// Verifies that SBOMs with no suppliers produce no supplier records.`
   - Given: An SBOM with no supplier information
   - When: The migration step processes the SBOM
   - Then: No records are inserted into `sbom_supplier` (assert empty result set)

- Register the test module in `mod.rs` with `#[cfg(test)] mod test;`

## Step-by-Step Execution Order

1. **Understand the code (Step 4):**
   - Use `serena_backend` to inspect `modules/ingestor/src/graph/sbom/mod.rs` via `get_symbols_overview` and `find_symbol` with `include_body=true` on `describing_packages` and `suppliers`
   - Inspect `migration/src/m0001_initial/mod.rs` as a sibling for convention analysis
   - Inspect `migration/src/m0002_supplier/mod.rs` to understand current state
   - Check `CONVENTIONS.md` at repo root for CI check commands and coding standards
   - Verify `migration/Cargo.toml` confirms the `trustify-module-ingestor` dependency

2. **Create branch (Step 5):**
   - `git checkout main && git pull && git checkout -b TC-9206`

3. **Implement changes (Step 6):**
   - Modify `modules/ingestor/src/graph/sbom/mod.rs`: change `fn` to `pub fn` on both functions, add doc comments
   - Modify `migration/src/m0002_supplier/mod.rs`: add imports and supplier extraction logic
   - Create `migration/src/m0002_supplier/test.rs`: write tests

4. **Write tests (Step 7):**
   - Implement the two test cases described above
   - Run `cargo test -p trustify-migration` (or whatever the crate name resolves to via `cargo metadata`)
   - Fix any failures

5. **Verify acceptance criteria (Step 8):**
   - Confirm migration extracts supplier information from all ingested SBOMs
   - Confirm extraction reuses existing ingestor logic (no duplication)
   - Confirm `sbom_supplier` table is populated correctly

6. **Self-verification (Step 9):**
   - Scope containment: verify only the three expected files are modified/created
   - Sensitive-pattern check on staged diff
   - Duplication check: confirm no duplicate extraction logic was introduced
   - Run CI checks from CONVENTIONS.md (if present)
   - Run `cargo test -p <crate-name>` for each modified crate (ingestor and migration)
   - Data-flow trace: SBOM input -> describing_packages/suppliers extraction -> sbom_supplier table insertion
   - Query-scope verification: confirm the migration queries the correct SBOM subset

7. **Commit and push (Step 10):**
   - Commit with message: `feat(migration): add SBOM supplier extraction to data migration`
   - Body: explain that `describing_packages()` and `suppliers()` were made public in the ingestor crate to enable reuse (DRY principle)
   - Footer: `Implements TC-9206`
   - Create PR targeting `main`

8. **Update Jira (Step 11):**
   - Set Git Pull Request custom field (`customfield_10875`) with PR URL
   - Add comment with PR link and summary of changes
   - Transition TC-9206 to In Review

## Handling the Private Functions

The private functions `describing_packages()` and `suppliers()` in the ingestor crate are the
central reuse decision in this task. Since `migration/Cargo.toml` already declares
`trustify-module-ingestor` as a dependency, the functions should be made public (`pub fn`)
and imported rather than duplicated. Full rationale is in `outputs/reuse-decision.md`.
