# Implementation Plan: TC-9206 -- Add SBOM supplier extraction to data migration

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- Repository Registry: lists `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: has Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: configured with `serena_backend` using rust-analyzer

Validation passes. Proceed.

## Step 1 -- Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add supplier information extraction during the SBOM data migration step. The migration crate needs to extract describing packages and supplier information from ingested SBOMs to populate the new `sbom_supplier` table. The ingestor module already has private helper functions that implement this extraction logic.
- **Files to Modify**:
  - `migration/src/m0002_supplier/mod.rs` -- add supplier extraction logic
  - `modules/ingestor/src/graph/sbom/mod.rs` -- make private functions public
- **Files to Create**:
  - `migration/src/m0002_supplier/test.rs` -- unit tests for supplier extraction
- **Dependencies**: None
- **Target PR**: None
- **Bookend Type**: None

## Step 2 -- Verify Dependencies

No dependencies declared. Proceed.

## Step 4 -- Understand the Code

### Files to inspect

1. **`modules/ingestor/src/graph/sbom/mod.rs`** -- Contains the two private helper functions:
   - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts packages an SBOM describes
   - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier info from SBOM metadata
   - Both are currently private (`fn`, not `pub fn`).

2. **`migration/src/m0001_initial/mod.rs`** -- Sibling migration module; inspect for migration step conventions (function signatures, error handling, database interaction patterns).

3. **`migration/src/lib.rs`** -- Module registration; need to understand how migration steps are registered and how `m0002_supplier` should be declared.

4. **`migration/Cargo.toml`** -- Verify that `trustify-module-ingestor` is already a dependency (the task description asserts this).

5. **`common/src/error.rs`** -- Understand `AppError` for error handling patterns.

6. **`entity/src/sbom.rs`** -- Understand the SBOM entity struct, since the migration reads from it.

### Convention conformance analysis

Based on the repository conventions documented in repo-backend.md:
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Framework**: SeaORM for database operations
- **Module pattern**: `model/ + service/ + endpoints/` structure for domain modules
- **Testing**: Integration tests hit real PostgreSQL; assertion pattern: `assert_eq!(...)`
- **Naming**: Rust standard snake_case for functions and variables

### Documentation files

- `CONVENTIONS.md` at the repo root
- `docs/architecture.md`
- `docs/api.md` (unlikely to be affected since this is a migration, not an API change)

### CONVENTIONS.md

Would read `CONVENTIONS.md` to extract CI check commands (formatting, linting, clippy, tests) for use in Step 9.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9206
```

## Step 6 -- Implement Changes

### File 1: `modules/ingestor/src/graph/sbom/mod.rs` (Modify)

**Change**: Make two private functions public by changing their visibility from `fn` to `pub fn`.

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

**Rationale**: The migration crate already depends on `trustify-module-ingestor` (confirmed in `migration/Cargo.toml`). Per SKILL.md Step 6 "Reuse over duplication" guidance, when the dependency relationship already exists, the correct approach is to make the functions public and import them rather than duplicating the code. See `outputs/reuse-decision.md` for the full decision analysis.

No other changes to this file. The function bodies remain unchanged.

### File 2: `migration/src/m0002_supplier/mod.rs` (Modify)

**Changes**:

1. **Add imports**: Import the newly-public functions from the ingestor crate:
   ```rust
   use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
   ```
   Also import any required types (`PackageRef`, `SupplierInfo`, `Sbom`) that these functions use.

2. **Implement supplier extraction migration step**: Following the pattern established in `m0001_initial/mod.rs`:
   - Define the migration step function (matching the naming and signature convention from sibling `m0001_initial`)
   - Query all ingested SBOMs from the database
   - For each SBOM, call `describing_packages(&sbom)` and `suppliers(&sbom)` to extract supplier information
   - Insert extracted supplier records into the `sbom_supplier` table using SeaORM
   - Use `Result<T, AppError>` with `.context()` for error handling, consistent with repo conventions

3. **Add documentation comment**: Every new public function gets a `///` doc comment explaining what it does.

### File 3: `migration/src/lib.rs` (In-scope note)

This file needs to be checked: the new `m0002_supplier` module must be declared here (e.g., `mod m0002_supplier;`) so it is compiled and registered as part of the migration sequence. If this file is not listed in Files to Modify, it would be flagged in Step 9's scope containment check for user approval.

**Note**: `migration/src/m0002_supplier/mod.rs` is listed as "Files to Modify" which implies the module directory already exists. However, if `lib.rs` does not already declare this module, it must be added. This is an expected out-of-scope change that would be flagged for user approval.

### File 4: `migration/src/m0002_supplier/test.rs` (Create)

**Changes**:

1. **Test: migration extracts suppliers from a sample SBOM**
   ```rust
   /// Verifies that the migration step correctly extracts supplier records from an SBOM with known supplier data.
   #[test]
   fn test_extract_suppliers_from_sbom() {
       // Given an SBOM with known supplier information
       // (construct a test SBOM with suppliers populated)

       // When the migration supplier extraction runs
       // (call the extraction logic on the test SBOM)

       // Then the correct supplier records are produced
       // (assert_eq! on specific supplier names/values, not just count)
   }
   ```

2. **Test: SBOMs with no suppliers produce no records**
   ```rust
   /// Verifies that an SBOM with no supplier metadata produces zero supplier records.
   #[test]
   fn test_no_suppliers_produces_empty_result() {
       // Given an SBOM with no supplier information
       // (construct a test SBOM with empty/absent supplier fields)

       // When the migration supplier extraction runs

       // Then no supplier records are produced
       // (assert_eq!(result.len(), 0) or assert!(result.is_empty()))
   }
   ```

Both tests follow the repo's assertion pattern (`assert_eq!`), include `///` doc comments (per SKILL.md Step 7), and use given-when-then section comments for non-trivial tests.

## Step 7 -- Write Tests

Write the tests described above in `migration/src/m0002_supplier/test.rs`. Run:

```
cargo test -p trustify-migration
```

(The crate name is resolved via `cargo metadata --no-deps --format-version 1`, not derived from the nearest `Cargo.toml`.)

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. **The migration step extracts supplier information from all ingested SBOMs** -- Verified by the implementation iterating over all SBOMs and calling `suppliers()` on each.
2. **The extraction reuses the existing ingestor logic rather than duplicating it** -- Verified by making the existing private functions public and importing them, rather than copying the function bodies.
3. **The `sbom_supplier` table is populated correctly with supplier data** -- Verified by the migration inserting the extracted data via SeaORM, confirmed by unit tests.

## Step 9 -- Self-Verification

### Scope containment
- `modules/ingestor/src/graph/sbom/mod.rs` -- listed in Files to Modify (in scope)
- `migration/src/m0002_supplier/mod.rs` -- listed in Files to Modify (in scope)
- `migration/src/m0002_supplier/test.rs` -- listed in Files to Create (in scope)
- `migration/src/lib.rs` -- NOT listed; flag for user approval (module declaration needed)

### Duplication check
Search for existing `describing_packages` and `suppliers` function names across the repo. The only instances should be in `modules/ingestor/src/graph/sbom/mod.rs`. Confirm no duplication was introduced.

### Dead parameter detection
No parameters were removed from existing functions. Only visibility was changed (`fn` to `pub fn`).

### CI checks
Run all CI check commands from `CONVENTIONS.md` (formatting, clippy, tests). Hard stop on any failure.

### Module-level test (Rust)
Run `cargo test -p trustify-migration` and `cargo test -p trustify-module-ingestor` since both crates had files modified.

### Data-flow trace
- **Input**: SBOM records from the database (read via SeaORM query)
- **Processing**: `describing_packages()` and `suppliers()` extract structured supplier data from each SBOM
- **Output**: Supplier records inserted into `sbom_supplier` table via SeaORM
- All stages connected; data flow is complete.

## Step 10 -- Commit and Push

```
git add modules/ingestor/src/graph/sbom/mod.rs migration/src/m0002_supplier/mod.rs migration/src/m0002_supplier/test.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add SBOM supplier extraction to data migration

Make describing_packages() and suppliers() public in the ingestor crate
and reuse them in the new m0002_supplier migration step. The migration
queries all ingested SBOMs and populates the sbom_supplier table using
the existing extraction logic.

Reuse decision: made existing private functions public rather than
duplicating them, since migration already depends on
trustify-module-ingestor.

Implements TC-9206"
```

Then push and create a PR against `main`.

## Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL
- Add comment summarizing changes and linking to the PR
- Transition TC-9206 to In Review
