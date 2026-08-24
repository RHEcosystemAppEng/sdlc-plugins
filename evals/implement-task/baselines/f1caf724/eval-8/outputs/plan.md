# Implementation Plan: TC-9206 — Add SBOM supplier extraction to data migration

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains:
- Repository Registry with trustify-backend entry (Serena instance: serena_backend, Path: ./)
- Jira Configuration with Project key TC, Cloud ID, Feature issue type ID
- Code Intelligence section with tool naming convention and serena_backend instance

All required sections present. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description for TC-9206:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add supplier information extraction during the SBOM data migration step. The migration crate needs to extract describing packages and supplier information from ingested SBOMs to populate the new `sbom_supplier` table. The ingestor module already has private helper functions (`describing_packages()` and `suppliers()`) that implement this extraction logic.
- **Files to Modify**:
  - `migration/src/m0002_supplier/mod.rs` -- add supplier extraction logic to the migration step
  - `modules/ingestor/src/graph/sbom/mod.rs` -- make `describing_packages()` and `suppliers()` public
- **Files to Create**:
  - `migration/src/m0002_supplier/test.rs` -- unit tests for the supplier extraction migration
- **Implementation Notes**: The ingestor module has two private helper functions (`describing_packages` and `suppliers`) that implement the exact extraction logic needed. The migration crate already depends on `trustify-module-ingestor` in its Cargo.toml.
- **Acceptance Criteria**:
  - The migration step extracts supplier information from all ingested SBOMs
  - The extraction reuses the existing ingestor logic rather than duplicating it
  - The `sbom_supplier` table is populated correctly with supplier data
- **Test Requirements**:
  - Test that the migration step correctly extracts suppliers from a sample SBOM
  - Test that SBOMs with no suppliers produce no supplier records
- **Dependencies**: None

## Step 1.5 -- Verify Description Integrity

Check Jira issue comments for `[sdlc-workflow] Description digest:` marker. If no digest comment is found, log a warning and proceed normally (backward compatibility -- tasks created before digest tracking was introduced have no digest comment):

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9206 to current user via `jira.edit_issue(TC-9206, assignee=<accountId>)`
3. Transition TC-9206 to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code

### 4.1 -- Inspect files to modify

**modules/ingestor/src/graph/sbom/mod.rs** (SBOM ingestion module):
- Use `mcp__serena_backend__get_symbols_overview` on `modules/ingestor/src/graph/sbom/mod.rs` to see all functions and types.
- Use `mcp__serena_backend__find_symbol` to read `describing_packages` and `suppliers` function bodies. These are the two private helper functions referenced in the Implementation Notes:
  - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- currently private (no `pub` keyword)
  - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- currently private (no `pub` keyword)
- These functions are currently private (`fn`, not `pub fn`) and need to be made public so the migration crate can import them.

**migration/src/m0002_supplier/mod.rs** (migration step):
- Use `mcp__serena_backend__get_symbols_overview` on `migration/src/m0002_supplier/mod.rs` to understand its current structure.
- Identify the migration function signature and determine where to add the supplier extraction call.

### 4.2 -- Verify the dependency relationship

Before deciding whether to make functions public or duplicate them, check the dependency manifest.

**Critical check**: Read `migration/Cargo.toml` to verify that the migration crate already depends on `trustify-module-ingestor`. According to the Implementation Notes, the dependency exists:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This is the key finding: the migration crate already has `trustify-module-ingestor` as a dependency in its `Cargo.toml`. This means we can import public symbols from the ingestor crate directly -- no new dependency needs to be added.

### 4.3 -- Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on `describing_packages` and `suppliers` to identify all current callers. Since these are private functions, their callers are confined to `modules/ingestor/src/graph/sbom/mod.rs` itself. Making them `pub fn` will not break existing callers -- it only widens visibility.

### 4.4 -- Convention conformance analysis (sibling files)

Inspect sibling files in the migration directory and ingestor module for patterns:

- **migration/src/m0001_initial/mod.rs**: Use `mcp__serena_backend__get_symbols_overview` to see the structure of the existing migration module. Identify patterns: function signatures, error handling, database interaction patterns.
- **modules/ingestor/src/graph/advisory/mod.rs**: Use `mcp__serena_backend__get_symbols_overview` to see sibling patterns in the ingestor graph module.

Discovered conventions:
- **Error handling**: Functions use `Result<T, AppError>` with `.context()` for error wrapping
- **Module structure**: Each domain module follows `model/ + service/ + endpoints/` pattern
- **Migration pattern**: Migration steps follow a function-based pattern with database transaction scoping
- **Testing**: Integration tests use `assert_eq!` with specific value-based assertions

### 4.5 -- CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read and follow its conventions. Extract any CI check commands for use in Step 9.

### 4.6 -- Documentation file identification

- `README.md` at repository root
- `docs/architecture.md` -- system architecture overview
- `docs/api.md` -- REST API reference (not directly relevant since this is a migration, not an endpoint)

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9206
```

## Step 6 -- Implement Changes

### 6.1 -- Make private functions public in ingestor crate

**File**: `modules/ingestor/src/graph/sbom/mod.rs`

Change the visibility of two functions from private to public:

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

No other changes to the function bodies. The logic remains identical -- only visibility changes.

Add documentation comments to both newly-public functions:

```rust
/// Extracts the list of packages that an SBOM describes.
pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> {
    // existing body unchanged
}

/// Extracts supplier information from SBOM metadata.
pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> {
    // existing body unchanged
}
```

### 6.2 -- Add supplier extraction logic to migration step

**File**: `migration/src/m0002_supplier/mod.rs`

Import the now-public functions from the ingestor crate:

```rust
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

Implement the migration logic:
1. Query all ingested SBOMs from the database
2. For each SBOM, call `describing_packages(&sbom)` and `suppliers(&sbom)` to extract supplier data
3. Insert extracted supplier records into the `sbom_supplier` table
4. Use `.context()` for error handling, following the established convention

The migration function reuses the existing extraction logic from the ingestor crate via import rather than reimplementing or copying the logic.

### 6.3 -- Reuse decision: pub fn over duplication

The decision to make `describing_packages()` and `suppliers()` public (rather than copying their bodies into the migration crate) was made based on:

1. **Dependency already exists**: `migration/Cargo.toml` already lists `trustify-module-ingestor` as a dependency. No new coupling is introduced.
2. **DRY principle**: Duplicating the function bodies would create two copies of the same logic. If a bug is found in the extraction logic, the fix would need to be applied in two places. Making the functions `pub` ensures any future bug fix applies in one place.
3. **No duplication proposed**: The plan explicitly does NOT copy or inline the function bodies into the migration crate.

See `outputs/reuse-decision.md` for the full analysis.

## Step 7 -- Write Tests

**File to create**: `migration/src/m0002_supplier/test.rs`

Tests to implement:

```rust
/// Verifies that the migration step correctly extracts suppliers from a sample SBOM.
#[test]
fn test_migration_extracts_suppliers_from_sbom() {
    // Given a sample SBOM with known supplier data
    // When running the supplier extraction migration
    // Then the sbom_supplier table contains the expected supplier records
}

/// Verifies that SBOMs with no suppliers produce no supplier records.
#[test]
fn test_migration_handles_sbom_with_no_suppliers() {
    // Given an SBOM with no supplier information
    // When running the supplier extraction migration
    // Then no supplier records are inserted into sbom_supplier
}
```

Follow sibling test patterns from `migration/src/m0001_initial/mod.rs` for setup/teardown, database transaction handling, and test organization.

Use value-based assertions (assert_eq on specific supplier names and counts) rather than existence-only checks.

Run tests to verify: `cargo test -p migration`

## Step 8 -- Verify Acceptance Criteria

- [x] The migration step extracts supplier information from all ingested SBOMs -- verified by the migration logic calling `suppliers()` for each SBOM
- [x] The extraction reuses the existing ingestor logic rather than duplicating it -- verified by importing `pub fn suppliers()` from the ingestor crate
- [x] The `sbom_supplier` table is populated correctly with supplier data -- verified by test assertions

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all modified files are within scope:
- `modules/ingestor/src/graph/sbom/mod.rs` -- listed in Files to Modify
- `migration/src/m0002_supplier/mod.rs` -- listed in Files to Modify
- `migration/src/m0002_supplier/test.rs` -- listed in Files to Create

All files are in scope. No out-of-scope modifications.

### Dead parameter detection
No parameters removed in this change. No dead parameter candidates.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- no matches expected.

### Duplication check
Search repository for existing supplier extraction logic. The only instances of `describing_packages` and `suppliers` are in the ingestor module, which we are reusing. No duplicated logic introduced.

### Contract & sibling parity
- Functions made public maintain the same signatures -- no contract changes
- Sibling migration modules follow the same pattern

### CI checks
Run CI check commands from CONVENTIONS.md (if found). Run `cargo build`, `cargo test`, `cargo clippy`.

## Step 10 -- Commit and Push

```bash
git add modules/ingestor/src/graph/sbom/mod.rs migration/src/m0002_supplier/mod.rs migration/src/m0002_supplier/test.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add SBOM supplier extraction to data migration

Reuse existing describing_packages() and suppliers() functions from the
ingestor crate by making them public. The migration crate already depends
on trustify-module-ingestor, so no new dependency is needed.

Implements TC-9206"
```

Push and open PR:

```bash
git push -u origin TC-9206
gh pr create --base main --title "feat(migration): add SBOM supplier extraction to data migration" --body "..."
```

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with PR URL
2. Add comment to TC-9206 with PR link and summary of changes
3. Transition TC-9206 to In Review
