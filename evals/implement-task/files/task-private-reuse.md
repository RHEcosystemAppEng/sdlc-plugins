<!-- SYNTHETIC TEST DATA — task requiring reuse of private functions from a dependent crate for testing reuse-over-duplication behavior -->

# Mock Jira Task

**Key**: TC-9206
**Summary**: Add SBOM supplier extraction to data migration
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Target Branch
main

## Description
Add supplier information extraction during the SBOM data migration step. The migration
crate needs to extract describing packages and supplier information from ingested SBOMs
to populate the new `sbom_supplier` table. The ingestor module already has private helper
functions (`describing_packages()` and `suppliers()`) that implement this extraction logic.

## Files to Modify
- `migration/src/m0002_supplier/mod.rs` — add supplier extraction logic to the migration step
- `modules/ingestor/src/graph/sbom/mod.rs` — make `describing_packages()` and `suppliers()` public

## Files to Create
- `migration/src/m0002_supplier/test.rs` — unit tests for the supplier extraction migration

## Implementation Notes
- The `modules/ingestor/src/graph/sbom/mod.rs` file contains two private helper functions:
  - `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` — extracts the list of packages that an SBOM describes
  - `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` — extracts supplier information from SBOM metadata
- These functions implement the exact logic needed for the migration, but they are currently private (`fn`, not `pub fn`)
- The `migration` crate already depends on `trustify-module-ingestor` in its `Cargo.toml`:
  ```toml
  [dependencies]
  trustify-module-ingestor = { path = "../modules/ingestor" }
  ```
- Since the dependency already exists, make the functions public and import them rather than duplicating the code

## Acceptance Criteria
- [ ] The migration step extracts supplier information from all ingested SBOMs
- [ ] The extraction reuses the existing ingestor logic rather than duplicating it
- [ ] The `sbom_supplier` table is populated correctly with supplier data

## Test Requirements
- [ ] Test that the migration step correctly extracts suppliers from a sample SBOM
- [ ] Test that SBOMs with no suppliers produce no supplier records

## Dependencies
- Depends on: None
