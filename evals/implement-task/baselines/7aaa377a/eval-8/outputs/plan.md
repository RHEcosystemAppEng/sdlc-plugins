# Implementation Plan for TC-9206: Add SBOM Supplier Extraction to Data Migration

## Task Summary

Add supplier information extraction during the SBOM data migration step. The migration crate needs to extract describing packages and supplier information from ingested SBOMs to populate the new `sbom_supplier` table. The ingestor module already has private helper functions that implement this extraction logic.

## Step-by-step Plan

### 1. Validate Project Configuration

Read CLAUDE.md and verify:
- Repository Registry contains `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration has Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence section lists `serena_backend` with `rust-analyzer`

All sections are present and complete. Proceed.

### 2. Fetch and Parse Jira Task (TC-9206)

Parsed fields:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add supplier information extraction during the SBOM data migration step
- **Files to Modify**: `migration/src/m0002_supplier/mod.rs`, `modules/ingestor/src/graph/sbom/mod.rs`
- **Files to Create**: `migration/src/m0002_supplier/test.rs`
- **Acceptance Criteria**: 3 items (supplier extraction, reuse of existing logic, correct table population)
- **Test Requirements**: 2 items (correct extraction, empty supplier handling)
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None

### 3. Transition to In Progress and Assign

- Retrieve current user via `jira.user_info()`
- Assign TC-9206 to current user
- Transition TC-9206 to "In Progress"

### 4. Understand the Code

#### 4a. Inspect files to modify

**`modules/ingestor/src/graph/sbom/mod.rs`** (via `mcp__serena_backend__get_symbols_overview`):
- Contains SBOM ingestion logic: parse, store, link packages
- Contains two private helper functions:
  - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
  - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata
- Use `mcp__serena_backend__find_symbol` with `include_body=true` to read the full implementation of both functions

**`migration/src/m0002_supplier/mod.rs`** (via `mcp__serena_backend__get_symbols_overview`):
- Inspect existing migration step structure
- Understand how migrations interact with the database and how they import from other crates

#### 4b. Check dependency relationship

Inspect `migration/Cargo.toml` to verify the dependency on `trustify-module-ingestor`:
```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```
Confirmed: the dependency already exists.

#### 4c. Inspect sibling migration files

Use `mcp__serena_backend__get_symbols_overview` on `migration/src/m0001_initial/mod.rs` to understand:
- Migration step structure and naming conventions
- How migrations import external types and functions
- Error handling patterns in migrations
- Database interaction patterns (SeaORM usage)

#### 4d. Convention conformance analysis

- Identify patterns from `m0001_initial/mod.rs` (naming, error handling, imports)
- Check for `CONVENTIONS.md` at the repository root
- Record discovered conventions for use during implementation

#### 4e. Test convention analysis

- Inspect sibling test files in the migration crate or nearby modules
- Record assertion patterns, test naming, and setup/teardown conventions

#### 4f. Documentation file identification

- Check for README files in `migration/` directory
- Note the repository root `README.md` and `CONVENTIONS.md`

#### 4g. Check for referencing symbols

Use `mcp__serena_backend__find_referencing_symbols` on `describing_packages` and `suppliers` to understand if anything else calls these functions. Changing their visibility from private to public is a backward-compatible change (no existing callers break).

### 5. Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9206
```

### 6. Implement Changes

#### File 1: `modules/ingestor/src/graph/sbom/mod.rs` (MODIFY)

**Change**: Make two private functions public by changing `fn` to `pub fn`:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` becomes `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` becomes `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

**Rationale**: The migration crate already depends on `trustify-module-ingestor`. Making these functions public allows direct import, avoiding code duplication. This follows the "reuse over duplication" principle in the skill's Step 6 guidance: "If the dependency already exists: make the function public and import it rather than duplicating the code."

**Documentation**: Add or update doc comments on both functions since they are now part of the public API:
```rust
/// Extracts the list of packages that an SBOM describes.
///
/// Returns a vector of package references found in the SBOM's
/// describing relationships.
pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> { ... }

/// Extracts supplier information from SBOM metadata.
///
/// Returns a vector of supplier information entries found in the
/// SBOM's component and document metadata.
pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> { ... }
```

Also verify that the types `PackageRef` and `SupplierInfo` are publicly exported from the ingestor crate. If they are private, make them public as well (they are return types of now-public functions and must be accessible to callers).

#### File 2: `migration/src/m0002_supplier/mod.rs` (MODIFY)

**Changes**:
1. Add imports for the newly-public functions from the ingestor crate:
   ```rust
   use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
   ```
2. Add supplier extraction logic to the migration step:
   - Iterate over all ingested SBOMs in the database
   - For each SBOM, call `describing_packages()` and `suppliers()` to extract supplier data
   - Insert extracted supplier records into the `sbom_supplier` table
   - Follow the migration patterns observed in `m0001_initial/mod.rs` (error handling, transaction usage, SeaORM patterns)

**Pattern**: Follow the same structure as existing migration steps (from sibling analysis of `m0001_initial`), including:
- Error handling with `Result<T, AppError>` and `.context()` wrapping
- Transaction handling consistent with how other migrations interact with the database
- Logging at appropriate levels

#### File 3: `migration/src/m0002_supplier/test.rs` (CREATE)

**Changes**:
1. Create unit tests following the test conventions discovered in Step 4
2. Include two test cases as specified in Test Requirements:

```rust
/// Verifies that the migration step correctly extracts suppliers from a sample SBOM.
#[test]
fn test_supplier_extraction_from_sbom() {
    // Given an SBOM with known supplier information
    let sbom = create_test_sbom_with_suppliers(vec![
        SupplierInfo { name: "Acme Corp".into(), url: Some("https://acme.example.com".into()) },
    ]);

    // When the migration extracts suppliers
    let result = extract_suppliers(&sbom);

    // Then supplier records should be populated correctly
    assert_eq!(result.len(), 1);
    assert_eq!(result[0].name, "Acme Corp");
    assert_eq!(result[0].url, Some("https://acme.example.com".into()));
}

/// Verifies that SBOMs with no suppliers produce no supplier records.
#[test]
fn test_no_suppliers_produces_empty_result() {
    // Given an SBOM with no supplier information
    let sbom = create_test_sbom_with_suppliers(vec![]);

    // When the migration extracts suppliers
    let result = extract_suppliers(&sbom);

    // Then no supplier records should be produced
    assert!(result.is_empty());
}
```

3. Add module registration: ensure `test.rs` is registered as `#[cfg(test)] mod test;` in `migration/src/m0002_supplier/mod.rs`
4. Each test function has a doc comment explaining what it verifies
5. Non-trivial tests use given-when-then section comments

### 7. Run Tests

```bash
cargo test -p trustify-migration
```

Fix any failures before proceeding.

### 8. Verify Acceptance Criteria

- [x] The migration step extracts supplier information from all ingested SBOMs -- verified by the supplier extraction logic in `m0002_supplier/mod.rs`
- [x] The extraction reuses the existing ingestor logic rather than duplicating it -- verified by the `pub fn` change and import in migration
- [x] The `sbom_supplier` table is populated correctly with supplier data -- verified by tests

### 9. Self-Verification

#### Scope containment
- `git diff --name-only` should show only:
  - `modules/ingestor/src/graph/sbom/mod.rs` (in Files to Modify)
  - `migration/src/m0002_supplier/mod.rs` (in Files to Modify)
  - `migration/src/m0002_supplier/test.rs` (in Files to Create)
- If any types (e.g., `PackageRef`, `SupplierInfo`) needed visibility changes, those files would be out-of-scope and require user approval

#### Sensitive-pattern check
- Scan staged diff for passwords, API keys, secrets

#### Duplication check
- Verify no duplicate supplier extraction logic exists elsewhere in the codebase

#### Data-flow trace
- SBOM data (input) -> `describing_packages()` + `suppliers()` extraction (processing) -> `sbom_supplier` table insertion (output) -- COMPLETE

#### Contract & sibling parity
- Compare migration step structure with `m0001_initial` for parity
- Verify transaction and error handling patterns match

### 10. Commit and Push

```bash
git add modules/ingestor/src/graph/sbom/mod.rs migration/src/m0002_supplier/mod.rs migration/src/m0002_supplier/test.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add SBOM supplier extraction to data migration

Make describing_packages() and suppliers() public in the ingestor crate
and import them in the migration step to populate the sbom_supplier table.
Reuses existing extraction logic rather than duplicating it.

Implements TC-9206"
```

Then push and create PR:
```bash
git push -u origin TC-9206
gh pr create --base main --title "feat(migration): add SBOM supplier extraction to data migration" --body "..."
```

PR description includes:
- Summary of changes
- Implements [TC-9206](https://redhat.atlassian.net/browse/TC-9206) link
- Note about the reuse decision (making private functions public vs. duplicating)

### 11. Update Jira

- Set Git Pull Request custom field (`customfield_10875`) to the PR URL (ADF format)
- Add comment summarizing changes made, including the reuse decision
- Transition TC-9206 to "In Review"
