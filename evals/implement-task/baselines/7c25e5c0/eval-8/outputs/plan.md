# Implementation Plan — TC-9206: Add SBOM Supplier Extraction to Data Migration

## Step 0 — Validate Project Configuration

Verified CLAUDE.md contains all required sections:
- **Repository Registry**: trustify-backend mapped to Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID present, Feature issue type ID present
- **Code Intelligence**: `mcp__serena_backend__<tool>` naming convention documented

## Step 1 — Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Jira Issue**: TC-9206
- **Jira Web URL**: https://redhat.atlassian.net/browse/TC-9206

### Parsed Sections

- **Files to Modify**:
  1. `migration/src/m0002_supplier/mod.rs` — add supplier extraction logic
  2. `modules/ingestor/src/graph/sbom/mod.rs` — make private functions public

- **Files to Create**:
  1. `migration/src/m0002_supplier/test.rs` — unit tests for supplier extraction

- **Dependencies**: None

## Step 1.5 — Verify Description Integrity

No description digest comment found — skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 4 — Understand the Code

### Code Inspection

Before making any changes, inspect the relevant files:

1. **`modules/ingestor/src/graph/sbom/mod.rs`** — use `mcp__serena_backend__get_symbols_overview` to identify:
   - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` (private)
   - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` (private)
   - Confirm these are the exact functions referenced in Implementation Notes

2. **`migration/src/m0002_supplier/mod.rs`** — inspect existing migration step structure to understand patterns

3. **`migration/src/lib.rs`** — check how migration modules are registered

4. **`migration/Cargo.toml`** — verify the dependency on `trustify-module-ingestor`:
   ```toml
   [dependencies]
   trustify-module-ingestor = { path = "../modules/ingestor" }
   ```
   This dependency already exists, which is critical for the reuse decision.

### Sibling Analysis

Inspect `migration/src/m0001_initial/mod.rs` to understand migration step conventions:
- Module structure and naming
- How migration steps access data and write to tables
- Error handling patterns within migrations

### Convention Conformance

- **Migration module pattern**: Each migration is a submodule under `migration/src/`
- **Error handling**: Migrations use `Result<T, AppError>` with `.context()` wrapping
- **Test pattern**: Migration tests follow the integration test patterns from `tests/api/`

### CONVENTIONS.md Lookup

Check `CONVENTIONS.md` at the repository root for CI check commands and coding conventions. Extract any verification commands for use in Step 9.

## Step 5 — Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9206
```

## Step 6 — Implement Changes

### File 1: `modules/ingestor/src/graph/sbom/mod.rs` (Modify)

**Change**: Make `describing_packages()` and `suppliers()` public by changing `fn` to `pub fn`.

Before:
```rust
fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> { ... }
fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> { ... }
```

After:
```rust
/// Extracts the list of packages that an SBOM describes.
pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> { ... }

/// Extracts supplier information from SBOM metadata.
pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> { ... }
```

No changes to function bodies — only visibility modifier and documentation.

### File 2: `migration/src/m0002_supplier/mod.rs` (Modify)

**Change**: Add supplier extraction logic that imports and calls the now-public functions from the ingestor module.

```rust
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

Implement the migration step to:
1. Query all ingested SBOMs from the database
2. For each SBOM, call `describing_packages()` to get package references
3. Call `suppliers()` to extract supplier information
4. Insert supplier records into the `sbom_supplier` table

Follow the migration step pattern from `m0001_initial/mod.rs` for error handling and transaction management.

### File 3: `migration/src/m0002_supplier/test.rs` (Create)

**Change**: Create unit tests for the supplier extraction migration.

Tests to implement:
1. Test that the migration step correctly extracts suppliers from a sample SBOM
2. Test that SBOMs with no suppliers produce no supplier records

Follow test conventions discovered from sibling analysis.

## Step 7 — Write Tests

Tests in `migration/src/m0002_supplier/test.rs`:

```rust
/// Verifies that the migration correctly extracts supplier information from an SBOM.
#[test]
fn test_supplier_extraction() {
    // Given an SBOM with known supplier information
    // When the migration step processes it
    // Then the sbom_supplier table contains the expected supplier records
}

/// Verifies that SBOMs without supplier metadata produce no records.
#[test]
fn test_no_suppliers() {
    // Given an SBOM with no supplier information
    // When the migration step processes it
    // Then no records are inserted into sbom_supplier
}
```

## Step 9 — Self-Verification

### Scope Containment
- `git diff --name-only` should show only:
  - `modules/ingestor/src/graph/sbom/mod.rs` (modified)
  - `migration/src/m0002_supplier/mod.rs` (modified)
  - `migration/src/m0002_supplier/test.rs` (created)
- All files are within the scope defined by Files to Modify and Files to Create.

### Dead Parameter Detection
No parameters removed — not applicable.

### Duplication Check
No new utility functions created. The implementation reuses existing `describing_packages()` and `suppliers()` from the ingestor crate.

### Module-Level Tests (Rust)
Resolve crate names using `cargo metadata --no-deps --format-version 1`:
- `modules/ingestor/src/graph/sbom/mod.rs` → `trustify-module-ingestor`
- `migration/src/m0002_supplier/mod.rs` → `trustify-migration`

Run:
```bash
cargo test -p trustify-module-ingestor
cargo test -p trustify-migration
```

## Step 10 — Commit and Push

```bash
git add modules/ingestor/src/graph/sbom/mod.rs migration/src/m0002_supplier/mod.rs migration/src/m0002_supplier/test.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add SBOM supplier extraction to data migration

Reuse existing describing_packages() and suppliers() functions from
the ingestor module by making them public. The migration crate already
depends on trustify-module-ingestor, so reuse avoids code duplication
and ensures future fixes apply in one place.

Implements TC-9206"
```

Push and create PR:
```bash
git push -u origin TC-9206
gh pr create --base main --title "feat(migration): add SBOM supplier extraction to data migration" --body "..."
```

## Step 11 — Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL
- Add comment with PR link and summary of changes
- Transition TC-9206 to In Review
