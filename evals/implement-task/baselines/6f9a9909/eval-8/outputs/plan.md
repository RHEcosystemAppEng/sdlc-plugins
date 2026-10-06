# Implementation Plan: TC-9206 -- Add SBOM supplier extraction to data migration

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Serena with rust-analyzer for trustify-backend

Configuration is valid. Proceeding.

## Step 1 -- Parsed Task Description

| Field | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Bookend Type | (none) |
| Target PR | (none) |
| Dependencies | None |

**Description:** Add supplier information extraction during the SBOM data migration step. The migration crate needs to extract describing packages and supplier information from ingested SBOMs to populate the new `sbom_supplier` table.

**Files to Modify:**
1. `migration/src/m0002_supplier/mod.rs` -- add supplier extraction logic to the migration step
2. `modules/ingestor/src/graph/sbom/mod.rs` -- make `describing_packages()` and `suppliers()` public

**Files to Create:**
1. `migration/src/m0002_supplier/test.rs` -- unit tests for the supplier extraction migration

**Acceptance Criteria:**
- The migration step extracts supplier information from all ingested SBOMs
- The extraction reuses the existing ingestor logic rather than duplicating it
- The `sbom_supplier` table is populated correctly with supplier data

**Test Requirements:**
- Test that the migration step correctly extracts suppliers from a sample SBOM
- Test that SBOMs with no suppliers produce no supplier records

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 4 -- Understand the Code

### Files to inspect

1. **`modules/ingestor/src/graph/sbom/mod.rs`** -- Contains the two private helper functions:
   - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages an SBOM describes
   - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata
   - Use `get_symbols_overview` to see all symbols, then `find_symbol` with `include_body=true` on both functions to read their implementations.

2. **`migration/src/m0002_supplier/mod.rs`** -- The migration step file to modify. Inspect current structure and existing migration logic.

3. **`migration/src/m0001_initial/mod.rs`** -- Sibling migration module. Use `get_symbols_overview` to understand migration conventions (naming, structure, error handling, SeaORM patterns).

4. **`migration/Cargo.toml`** -- Verify that `trustify-module-ingestor` is already listed as a dependency. This is critical for the reuse decision.

5. **`CONVENTIONS.md`** -- Check at repository root for project conventions and CI check commands.

### Convention conformance analysis (from sibling migration)

Examine `m0001_initial/mod.rs` for:
- Migration function signature pattern (likely `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>`)
- Error handling (`.context()` wrapping or `?` propagation)
- Table creation and data population patterns
- Import organization

### Dependency verification

The task states that `migration/Cargo.toml` already contains:
```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```
This confirms the dependency exists and enables the reuse path.

### Reuse analysis

The implementation needs `describing_packages()` and `suppliers()` from the ingestor crate. These are currently private. Since the dependency already exists, the "Reuse over duplication" rule in the skill (Step 6) dictates: make the functions public and import them rather than duplicating the code.

### Backward compatibility check

Use `find_referencing_symbols` on both functions to verify no external code currently references them (they are private, so this should return only internal callers). Making them `pub` is additive and non-breaking -- existing internal callers are unaffected.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9206
```

## Step 6 -- Implementation Changes

### File 1: `modules/ingestor/src/graph/sbom/mod.rs`

**Change:** Make two private functions public.

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

**Rationale:** The migration crate already depends on `trustify-module-ingestor`. Making these functions public allows reuse without code duplication. This is the DRY-compliant approach per the skill's "Reuse over duplication" guidance.

**Also check:** Whether these functions are re-exported from the crate's `lib.rs`. If the module path `graph::sbom` is not publicly accessible, add `pub mod` declarations up the module tree so the migration crate can import them as `trustify_module_ingestor::graph::sbom::describing_packages` (or the appropriate path). Specifically:
- `modules/ingestor/src/lib.rs` must have `pub mod graph;`
- `modules/ingestor/src/graph/mod.rs` must have `pub mod sbom;`

### File 2: `migration/src/m0002_supplier/mod.rs`

**Changes:** Add supplier extraction logic to the migration step.

1. **Add imports:**
   ```rust
   use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
   ```
   Plus imports for the `sbom_supplier` table entity, database types, and error handling.

2. **Implement the migration `up()` function:**
   - Query all existing SBOMs from the database
   - For each SBOM, call `describing_packages(&sbom)` and `suppliers(&sbom)` to extract supplier data
   - Insert extracted supplier records into the `sbom_supplier` table
   - Use batch insert for performance if the ORM supports it
   - Follow error handling patterns from `m0001_initial` (likely `?` propagation with `.context()`)

3. **Implement the migration `down()` function:**
   - Truncate or drop data from `sbom_supplier` table (reversible migration)

4. **Add doc comments:**
   - Document the migration module explaining it populates `sbom_supplier` from existing SBOM data
   - Document any helper functions added within the migration

### File 3: `migration/src/m0002_supplier/test.rs` (new file)

**Create unit tests:**

1. **`test_migration_extracts_suppliers_from_sbom`:**
   - Doc comment: "Verifies that the migration correctly extracts supplier information from a sample SBOM."
   - Given: A sample SBOM with known supplier metadata
   - When: The migration supplier extraction logic runs
   - Then: The correct supplier records are produced with expected values (assert on specific field values, not just count)

2. **`test_migration_no_suppliers_produces_no_records`:**
   - Doc comment: "Verifies that an SBOM with no supplier information produces zero supplier records."
   - Given: An SBOM with no supplier metadata
   - When: The migration supplier extraction logic runs
   - Then: No supplier records are produced (assert empty result)

3. **Register the test module:** Add `#[cfg(test)] mod test;` in `migration/src/m0002_supplier/mod.rs`.

### Module registration

Ensure `migration/src/lib.rs` includes `pub mod m0002_supplier;` and that the migration is registered in the migration runner's list (following the pattern established by `m0001_initial`).

## Step 7 -- Write Tests

Implement the tests described above in `migration/src/m0002_supplier/test.rs`. Run:
```
cargo test -p trustify-migration
```
(Package name resolved via `cargo metadata`.)

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| Migration extracts supplier info from all ingested SBOMs | The `up()` function queries all SBOMs and processes each one |
| Extraction reuses existing ingestor logic | Functions are imported from `trustify_module_ingestor`, not duplicated |
| `sbom_supplier` table is populated correctly | Tests verify correct data extraction and insertion |

## Step 9 -- Self-Verification Checklist

- **Scope containment:** Only files listed in Files to Modify and Files to Create are changed, plus necessary module registration in `lib.rs` and potential `pub mod` additions in the ingestor module tree (flag for user approval if out-of-scope)
- **Sensitive-pattern check:** No credentials or secrets in the diff
- **Duplication check:** Confirmed reuse of existing functions rather than duplication
- **Dead parameter detection:** No parameters removed
- **CI checks:** Run CONVENTIONS.md CI commands if present, plus `cargo test -p trustify-migration`
- **Data-flow trace:** SBOM data (DB) -> `describing_packages()`/`suppliers()` extraction -> `sbom_supplier` table insert. Complete path.
- **Query-scope verification:** Migration queries all SBOMs (intentionally broad -- task says "all ingested SBOMs")

## Step 10 -- Commit and Push

```
git add modules/ingestor/src/graph/sbom/mod.rs migration/src/m0002_supplier/mod.rs migration/src/m0002_supplier/test.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add SBOM supplier extraction to data migration

Extract supplier information from ingested SBOMs during the m0002_supplier
migration step. Reuses the existing describing_packages() and suppliers()
functions from the ingestor crate by making them public, rather than
duplicating the extraction logic.

Implements TC-9206"
```

Then push and create PR targeting `main`.

## Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add comment with PR link and summary of changes
- Transition TC-9206 to In Review
