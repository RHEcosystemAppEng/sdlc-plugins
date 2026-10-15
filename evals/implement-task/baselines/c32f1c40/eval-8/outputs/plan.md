# Implementation Plan for TC-9206: Add SBOM supplier extraction to data migration

## Task Summary

Add supplier information extraction during the SBOM data migration step. The migration
crate needs to extract describing packages and supplier information from ingested SBOMs
to populate the new `sbom_supplier` table, reusing existing private helper functions from
the ingestor crate.

## Repository

trustify-backend

## Target Branch

main

## Step-by-Step Plan

### Step 1: Validate and Parse Task

- Repository: trustify-backend
- Target Branch: main
- No Target PR (new branch/PR flow)
- No Bookend Type (standard implementation)
- No dependencies to verify

### Step 2: Branch Creation

```
git checkout main
git pull
git checkout -b TC-9206
```

### Step 3: Code Understanding (Step 4 of Skill)

Inspect the following files using Serena (`serena_backend`) or Read/Grep fallback:

1. **`modules/ingestor/src/graph/sbom/mod.rs`** -- understand the private functions:
   - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
   - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata
   - Inspect their signatures, bodies, and types to understand what they return and how they work.

2. **`migration/src/m0001_initial/mod.rs`** -- sibling migration module; understand the existing migration pattern (struct layout, trait implementations, `up`/`down` methods, error handling) to replicate the same conventions.

3. **`migration/Cargo.toml`** -- verify the `trustify-module-ingestor` dependency exists (the task states it does).

4. **`migration/src/lib.rs`** -- understand how migration modules are registered so the new `m0002_supplier` module can be added.

5. **Check for `CONVENTIONS.md`** at repository root for CI checks and coding standards.

#### Convention Conformance

Examine `m0001_initial/mod.rs` as a sibling to discover:
- Migration struct naming and trait implementation pattern
- Error handling conventions within migrations
- Import organization
- How migrations iterate over database records

### Step 4: Implementation Changes

#### File to Modify: `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make `describing_packages()` and `suppliers()` public.

- Change `fn describing_packages(` to `pub fn describing_packages(`
- Change `fn suppliers(` to `pub fn suppliers(`
- Add documentation comments to both functions (required by skill's code quality practices for all public symbols):
  - `/// Extracts the list of packages that an SBOM describes.`
  - `/// Extracts supplier information from SBOM metadata.`

**Rationale**: The migration crate already depends on `trustify-module-ingestor`, so making these functions public enables direct reuse without introducing new coupling. See `outputs/reuse-decision.md` for the full decision analysis.

#### File to Modify: `migration/src/m0002_supplier/mod.rs`

**Change**: Add supplier extraction logic to the migration step.

- Import `describing_packages` and `suppliers` from `trustify_module_ingestor::graph::sbom` (the exact module path depends on the crate's `lib.rs` re-exports; verify during implementation).
- Create a migration struct (e.g., `M0002Supplier`) following the pattern from `m0001_initial/mod.rs`.
- Implement the migration trait (likely SeaORM's `MigrationTrait` with `up` and `down` methods).
- In the `up` method:
  1. Query all ingested SBOMs from the database.
  2. For each SBOM, call `describing_packages(&sbom)` and `suppliers(&sbom)` to extract supplier data.
  3. Insert extracted supplier records into the `sbom_supplier` table.
- In the `down` method: drop or truncate the `sbom_supplier` table (reversibility).
- Apply defensive property access on SBOM data (`.unwrap_or_default()` for optional fields).
- Follow error handling conventions from sibling migration (`Result<T, AppError>` with `.context()` if applicable).

#### File to Modify: `migration/src/lib.rs`

**Change**: Register the new `m0002_supplier` module.

- Add `mod m0002_supplier;` declaration.
- Add the new migration to the migration registry/vector (following the pattern used by `m0001_initial`).

#### File to Create: `migration/src/m0002_supplier/test.rs`

**Change**: Unit tests for the supplier extraction migration.

- Add `#[cfg(test)] mod test;` to `migration/src/m0002_supplier/mod.rs`.
- Implement tests per Test Requirements:

```rust
/// Verifies that the migration correctly extracts suppliers from a sample SBOM.
#[test]
fn test_extract_suppliers_from_sbom() {
    // Given an SBOM with known supplier information
    // When the migration processes the SBOM
    // Then the sbom_supplier table contains the expected supplier records
}

/// Verifies that SBOMs with no suppliers produce no supplier records.
#[test]
fn test_no_suppliers_produces_empty_records() {
    // Given an SBOM with no supplier metadata
    // When the migration processes the SBOM
    // Then no records are inserted into sbom_supplier
}
```

- Use value-based assertions (assert on specific supplier names/fields, not just counts).
- Add doc comments on every test function.
- Use given-when-then section comments for non-trivial tests.
- Follow test patterns from sibling migration tests (if they exist).

### Step 5: Verification (Step 9 of Skill)

1. **Scope containment**: Verify `git diff --name-only` only touches the four files listed above (plus `migration/src/lib.rs` for module registration, which should be flagged as out-of-scope per the task's Files to Modify and approved by user).
2. **Sensitive-pattern check**: Scan staged diff for secrets.
3. **Duplication check**: Verify no other copy of `describing_packages` or `suppliers` logic exists elsewhere.
4. **CI checks**: Run commands from `CONVENTIONS.md` if present, otherwise `cargo check` and `cargo fmt --check`.
5. **Module-level test**: Run `cargo test -p <migration-crate-name>` and `cargo test -p trustify-module-ingestor`.
6. **Data-flow trace**: Input (SBOM records from DB) -> Processing (describing_packages + suppliers extraction) -> Output (sbom_supplier table rows). All stages connected.
7. **Query-scope verification**: The migration should process all SBOMs (task says "all ingested SBOMs"), so a broad query is intentional and correct.

### Step 6: Commit and PR

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add SBOM supplier extraction to data migration

Add m0002_supplier migration step that extracts supplier information from
ingested SBOMs and populates the sbom_supplier table. Reuses existing
describing_packages() and suppliers() functions from the ingestor crate
by making them public, avoiding code duplication.

Implements TC-9206"
```

Create PR targeting `main` with description referencing the Jira issue.

### Step 7: Update Jira

- Update `customfield_10875` (Git Pull Request) with PR URL.
- Add comment with PR link and summary of changes.
- Transition TC-9206 to In Review.

## Files Summary

| File | Action | Description |
|------|--------|-------------|
| `modules/ingestor/src/graph/sbom/mod.rs` | Modify | Make `describing_packages()` and `suppliers()` public, add doc comments |
| `migration/src/m0002_supplier/mod.rs` | Modify | Add supplier extraction logic using imported ingestor functions |
| `migration/src/lib.rs` | Modify | Register `m0002_supplier` module (out-of-scope per task, needs user approval) |
| `migration/src/m0002_supplier/test.rs` | Create | Unit tests for supplier extraction |
