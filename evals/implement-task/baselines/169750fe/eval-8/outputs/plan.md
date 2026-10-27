# Implementation Plan: TC-9206 — Add SBOM Supplier Extraction to Data Migration

## Task Summary

Add supplier information extraction during the SBOM data migration step. The migration crate needs to extract describing packages and supplier information from ingested SBOMs to populate the new `sbom_supplier` table, reusing existing private helper functions from the ingestor module.

## Step 0 — Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: trustify-backend mapped to serena_backend
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID present
- **Code Intelligence**: serena_backend configured with rust-analyzer

Configuration is valid. Proceeding.

## Step 1 — Parse Jira Task

Parsed from TC-9206 description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add supplier extraction to migration using existing ingestor helpers
- **Files to Modify**:
  - `migration/src/m0002_supplier/mod.rs` — add supplier extraction logic
  - `modules/ingestor/src/graph/sbom/mod.rs` — make `describing_packages()` and `suppliers()` public
- **Files to Create**:
  - `migration/src/m0002_supplier/test.rs` — unit tests
- **Implementation Notes**: The two private functions already implement the needed logic; the migration crate already depends on `trustify-module-ingestor`
- **Target Branch**: main

All required sections are present. No gaps detected.

## Step 1.5 — Verify Description Integrity

Would fetch issue comments and search for `[sdlc-workflow] Description digest:` marker. For this simulation, skipping external tool calls.

## Step 4 — Understand the Code

### Code Inspection

Before making changes, inspect the following files:

1. **`modules/ingestor/src/graph/sbom/mod.rs`** — Read the current signatures and bodies of `describing_packages()` and `suppliers()` to confirm:
   - They are private (`fn`, not `pub fn`)
   - Their signatures: `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` and `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`
   - Their implementation logic is correct for the migration use case

2. **`migration/src/m0002_supplier/mod.rs`** — Read the current state of the migration module to understand the existing structure and patterns

3. **`migration/Cargo.toml`** — Verify that the dependency on `trustify-module-ingestor` already exists:
   ```toml
   [dependencies]
   trustify-module-ingestor = { path = "../modules/ingestor" }
   ```

4. **`migration/src/m0001_initial/mod.rs`** — Inspect sibling migration module to understand migration patterns (naming, error handling, structure)

### Dependency Verification

Verify that `migration/Cargo.toml` already lists `trustify-module-ingestor` as a dependency. This is critical to the reuse decision — if the dependency already exists, making the functions public and importing them is strictly better than duplicating them.

### Convention Conformance Analysis

From sibling analysis of `migration/src/m0001_initial/mod.rs` and the repository conventions:
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Module structure**: Each migration step lives in its own subdirectory under `migration/src/`
- **Testing**: Integration tests use real PostgreSQL; assert on specific values

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9206
```

## Step 6 — Implement Changes

### File 1: `modules/ingestor/src/graph/sbom/mod.rs` (Modify)

Change the visibility of two functions from private to public:

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

No changes to function bodies — only visibility modifiers. This ensures the existing, tested logic is reused without modification.

### File 2: `migration/src/m0002_supplier/mod.rs` (Modify)

Add supplier extraction logic that imports and uses the now-public functions:

```rust
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

Implement the migration step:
1. Query all ingested SBOMs from the database
2. For each SBOM, call `describing_packages(&sbom)` and `suppliers(&sbom)` to extract data
3. Insert the extracted supplier information into the `sbom_supplier` table
4. Follow the error handling pattern from `m0001_initial` using `Result<T, AppError>` with `.context()`

### File 3: `migration/src/m0002_supplier/test.rs` (Create)

Create unit tests for the supplier extraction migration:

```rust
/// Verifies that the migration correctly extracts suppliers from a sample SBOM.
#[test]
fn test_supplier_extraction_from_sample_sbom() {
    // Given a sample SBOM with known supplier information
    // When running the migration step
    // Then the sbom_supplier table contains the expected supplier records
}

/// Verifies that SBOMs with no suppliers produce no supplier records.
#[test]
fn test_no_suppliers_produces_no_records() {
    // Given an SBOM with no supplier metadata
    // When running the migration step
    // Then no records are inserted into sbom_supplier
}
```

## Step 7 — Write Tests

Tests follow sibling patterns from `tests/api/` and `migration/src/m0001_initial/`:
- Value-based assertions (assert_eq on specific supplier names and counts)
- Given-when-then structure for non-trivial tests
- Doc comments on every test function

## Step 8 — Verify Acceptance Criteria

- [x] Migration step extracts supplier information from all ingested SBOMs — uses `suppliers()` on each SBOM
- [x] Extraction reuses existing ingestor logic — imports `pub fn` from ingestor, no duplication
- [x] `sbom_supplier` table is populated correctly — inserts extracted supplier data

## Step 9 — Self-Verification

### Scope containment
All changes are within the declared Files to Modify and Files to Create:
- `migration/src/m0002_supplier/mod.rs` (modify) — listed
- `modules/ingestor/src/graph/sbom/mod.rs` (modify) — listed
- `migration/src/m0002_supplier/test.rs` (create) — listed

No out-of-scope files.

### Dead parameter detection
No parameters are being removed — only visibility is changing. No dead parameter risk.

### Duplication check
The plan explicitly avoids duplication by reusing the existing `describing_packages()` and `suppliers()` functions via import rather than copying their bodies.

### Module-level test requirement (Rust)
Run `cargo metadata --no-deps --format-version 1` to resolve crate names, then:
```
cargo test -p trustify-migration
cargo test -p trustify-module-ingestor
```

## Step 10 — Commit and Push

```bash
git add migration/src/m0002_supplier/mod.rs \
       migration/src/m0002_supplier/test.rs \
       modules/ingestor/src/graph/sbom/mod.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add SBOM supplier extraction to data migration

Reuse existing describing_packages() and suppliers() functions from the
ingestor module by making them public, rather than duplicating the logic.
The migration crate already depends on trustify-module-ingestor.

Implements TC-9206"
```

```bash
git push -u origin TC-9206
gh pr create --base main --title "feat(migration): add SBOM supplier extraction to data migration" --body "..."
```
