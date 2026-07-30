<!-- SYNTHETIC TEST DATA — data migration task targeting a subset of records to test query-scope verification -->

# Mock Jira Task

**Key**: TC-9209
**Summary**: Re-process all SPDX SBOMs to extract package supplier information
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Target Branch
main

## Description
Create a data migration that re-processes all SPDX SBOMs to extract package supplier
information that was previously ignored during ingestion. The migration should iterate
over each SPDX SBOM document, re-parse the source data, extract the `supplier` field
from SPDX package entries, and update the corresponding `sbom_package` records in the
database with the extracted supplier values.

Only SPDX SBOMs need re-processing — CycloneDX documents already have supplier
information populated during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/sbom/mod.rs` — extract the `suppliers()` helper into a public function so the migration can reuse it

## Files to Create
- `migration/src/m0042_backfill_suppliers/mod.rs` — the data migration that re-processes SPDX SBOMs

## API Changes
- (none)

## Implementation Notes
- The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores
  metadata about each document. SPDX documents have `{"type": "spdx"}` in their labels,
  while CycloneDX documents have `{"type": "cyclonedx"}`.
- The `suppliers()` function in `modules/ingestor/src/graph/sbom/mod.rs` already contains the
  SPDX supplier extraction logic. It is currently private (`fn suppliers(...)`) — make it
  `pub fn suppliers(...)` so the migration can import and reuse it. The migration crate already
  depends on `trustify-module-ingestor` in `migration/Cargo.toml`.
- Existing migration pattern: see `migration/src/m0001_initial/mod.rs` for the migration
  structure. Each migration implements the `MigrationTrait` with an `up()` method.
- The source SBOM data is stored in the `source_document` table and can be fetched by
  `sbom_id`. Use `SourceDocument::find_by_sbom_id(id)` to retrieve the raw document bytes.
- Production environments have hundreds of thousands of CycloneDX documents alongside
  a smaller number of SPDX documents. The migration should only load and process SPDX
  documents to avoid unnecessary I/O.

## Acceptance Criteria
- [ ] The migration re-processes all SPDX SBOM documents and populates supplier fields
- [ ] CycloneDX documents are not loaded or processed by the migration
- [ ] The `suppliers()` function in the ingestor is made public for reuse
- [ ] The migration follows the existing migration pattern from `m0001_initial`

## Test Requirements
- [ ] Add a test that verifies the migration populates supplier information for an SPDX SBOM
- [ ] Add a test that verifies CycloneDX SBOMs are not affected by the migration

## Dependencies
- Depends on: None
