# Impact Map — TC-9001: Advisory Severity Aggregation Endpoint

## Priority: Major
## Fix Versions: RHTPA 1.5.0

## Field Propagation

- **Priority**: Major — inherited from feature TC-9001, propagated to all tasks via additional_fields.
- **Fix Versions**: RHTPA 1.5.0 — inherited from feature TC-9001, propagated to all tasks via additional_fields (fixVersion scope defaults to 'both').

## Workflow Mode

Direct-to-main — single repository (trustify-backend), no atomicity constraints requiring feature-branch isolation. All tasks target `main`.

trustify-backend:
  changes:
    - Add `AdvisorySeveritySummary` response model struct in `modules/fundamental/src/sbom/model/` with fields: critical, high, medium, low, total (all u64)
    - Add `get_advisory_severity_summary` method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` that queries the `sbom_advisory` join table, joins to `advisory` entity, groups by severity, and returns deduplicated counts
    - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in `modules/fundamental/src/sbom/endpoints/` that validates SBOM existence (404 if missing), calls the service method, and returns the summary as JSON
    - Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes
    - Add 5-minute `tower-http` cache-control middleware to the advisory-summary route in the endpoint route builder
    - Add cache invalidation hook in `modules/ingestor/src/graph/advisory/mod.rs` to invalidate cached summaries when new advisories are linked to an SBOM
    - Add optional `threshold` query parameter support to filter severity counts (non-MVP, included for completeness)
    - Add integration tests in `tests/api/` covering: success with known SBOM, 404 for missing SBOM, correct severity counts, cache behavior, and threshold filtering

## Task Summary

| Task | Title | Dependencies |
|------|-------|-------------|
| 1 | Add AdvisorySeveritySummary response model | None |
| 2 | Add severity aggregation query to SbomService | Task 1 |
| 3 | Add advisory-summary endpoint with caching | Task 2 |
| 4 | Add cache invalidation on advisory ingestion | Task 3 |
| 5 | Add integration tests for advisory-summary endpoint | Task 3 |

## Description Digests

After each task was created, a description digest comment was posted:

- Task 1: `[sdlc-workflow] Description digest: sha256-md:196670169db30aa7c9792b5f3dba75e5329dc14c205701903194665ecf7ca200`
- Task 2: `[sdlc-workflow] Description digest: sha256-md:cbecf9d0be5259bce2367b0fc90ff3fd58c577685773ed205d2a790723bd1ea1`
- Task 3: `[sdlc-workflow] Description digest: sha256-md:f895045c0f751748a95f163755e3bb5123655aa753d1faa1bc8e6f4a33d44765`
- Task 4: `[sdlc-workflow] Description digest: sha256-md:909f26fec39c15b429ba827effa2ed3d5682dd7c744fb6b9b1162e535c92a3ec`
- Task 5: `[sdlc-workflow] Description digest: sha256-md:8361f2ec453cf2de6a4dd1023ff1a2095bfe691b2c1af36a75426025f750fc55`

## Summary Comment (Feature TC-9001 — Step 6c)

Implementation plan created for TC-9001 (Advisory Severity Aggregation Endpoint) with 5 tasks targeting trustify-backend, using direct-to-main workflow.

**Inherited fields propagated to all tasks:**
- **Priority**: Major — inherited from feature TC-9001, set on all 5 tasks via additional_fields.
- **Fix Versions**: RHTPA 1.5.0 — inherited from feature TC-9001, set on all 5 tasks via additional_fields (fixVersion scope defaults to 'both' per configuration).