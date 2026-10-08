# Implementation Plan -- TC-9206: Add SBOM supplier extraction to data migration

## Task Summary

Add supplier information extraction during the SBOM data migration step. The migration crate needs to extract describing packages and supplier information from ingested SBOMs to populate the new `sbom_supplier` table. The ingestor module already has private helper functions that implement this extraction logic.

## Project Configuration Validation

The mock CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Serena instance `serena_backend` with rust-analyzer

## Parsed Task Fields

- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None

## Step 4 -- Code Understanding

### Files to Modify

#### 1. `modules/ingestor/src/graph/sbom/mod.rs`

This file contains the SBOM ingestion logic: parse, store, and link packages. It contains two private helper functions that are central to this task:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata

These functions are currently private (no `pub` keyword). They need to be made public so the migration crate can import and reuse them.

**Action**: Change `fn describing_packages(...)` to `pub fn describing_packages(...)` and `fn suppliers(...)` to `pub fn suppliers(...)`. Add documentation comments to both functions explaining their purpose, since they are becoming part of the public API.

**Backward compatibility check**: Use `find_referencing_symbols` on both functions to confirm all existing callers within the ingestor crate continue to compile after the visibility change. Making a private function public is a non-breaking change for existing callers -- it only widens access.

#### 2. `migration/src/m0002_supplier/mod.rs`

This is the migration step module where the supplier extraction logic must be added.

**Action**: Import `describing_packages` and `suppliers` from `trustify_module_ingestor::graph::sbom` (using the crate name from the Cargo.toml dependency). Implement the migration logic that:
1. Iterates over all ingested SBOMs
2. Calls `describing_packages()` on each SBOM to get the packages it describes
3. Calls `suppliers()` on each SBOM to extract supplier information
4. Inserts the extracted supplier data into the `sbom_supplier` table

Follow error handling patterns from the existing migration `m0001_initial/mod.rs` (use `Result<T, AppError>` with `.context()` wrapping). Follow the SeaORM patterns used elsewhere in the project for database operations.

### Files to Create

#### 1. `migration/src/m0002_supplier/test.rs`

Unit tests for the supplier extraction migration.

**Action**: Create test module with the following tests:

- `test_migration_extracts_suppliers_from_sbom` -- Verifies that the migration step correctly extracts suppliers from a sample SBOM. Set up a test SBOM with known supplier data, run the migration logic, and assert that the `sbom_supplier` table contains the expected supplier records with correct field values.

- `test_migration_handles_sbom_with_no_suppliers` -- Verifies that SBOMs with no suppliers produce no supplier records. Set up a test SBOM with no supplier metadata, run the migration logic, and assert the result set is empty.

Each test will have:
- A `///` documentation comment explaining what it verifies
- Given/When/Then section comments inside the test body
- Value-based assertions (assert on specific supplier names, not just counts)

Register the test module in `migration/src/m0002_supplier/mod.rs` with `#[cfg(test)] mod test;`.

### Dependency Verification

The `migration/Cargo.toml` already contains:
```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

Since the dependency already exists, no new dependency needs to be added. The private functions can be made public and imported directly.

### Convention Conformance

Conventions to follow (derived from the repository structure and key conventions):
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Framework**: SeaORM for database operations
- **Module pattern**: Follow the existing migration module structure (`m0001_initial/mod.rs` as the sibling reference)
- **Testing**: Use the project's integration test patterns; assert on specific values

### Documentation Impact

- Both `describing_packages()` and `suppliers()` need doc comments added when made public
- No existing documentation files appear to cover migration internals, so no doc updates needed beyond the code-level comments

## Step 5 -- Branch

Create branch from main:
```
git checkout main
git pull
git checkout -b TC-9206
```

## Step 6 -- Implementation Sequence

1. **Make helper functions public** in `modules/ingestor/src/graph/sbom/mod.rs`:
   - Change `fn describing_packages(...)` to `pub fn describing_packages(...)`
   - Change `fn suppliers(...)` to `pub fn suppliers(...)`
   - Add `///` doc comments to both functions

2. **Implement migration logic** in `migration/src/m0002_supplier/mod.rs`:
   - Add import: `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`
   - Implement the migration step that iterates SBOMs, extracts suppliers, and inserts into `sbom_supplier`
   - Follow SeaORM patterns and error handling from `m0001_initial`

3. **Write tests** in `migration/src/m0002_supplier/test.rs`:
   - Two test functions as described above
   - Register test module in `mod.rs`

4. **Register the migration module** in `migration/src/lib.rs`:
   - Add `mod m0002_supplier;` to include the new migration step

## Step 9 -- Self-Verification Checklist

- **Scope containment**: Only files in Files to Modify and Files to Create are changed
- **Sensitive-pattern check**: No credentials or secrets involved
- **Duplication check**: Confirmed no duplication -- reusing existing functions rather than duplicating
- **CI checks**: Run `cargo check`, `cargo fmt --check`, `cargo clippy`, and `cargo test -p migration` and `cargo test -p trustify-module-ingestor`
- **Data-flow trace**: SBOM data (input) -> `describing_packages()` + `suppliers()` (processing) -> `sbom_supplier` table INSERT (output) -- complete path
- **Query-scope verification**: Migration should process all ingested SBOMs (the task says "all ingested SBOMs"), so a full-table scan is intentional and correct

## Step 10 -- Commit and PR

Commit message:
```
feat(migration): add SBOM supplier extraction to data migration

Reuse existing describing_packages() and suppliers() helper functions
from the ingestor crate by making them public, rather than duplicating
the extraction logic in the migration module.

Implements TC-9206
```

PR targets `main` branch with a description referencing TC-9206.
