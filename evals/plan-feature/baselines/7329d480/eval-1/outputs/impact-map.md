# Repository Impact Map — TC-9001

## Feature
Add advisory severity aggregation endpoint

## Repositories Affected

### trustify-backend
**Role**: Primary backend service — all changes land here.

**Changes needed**:
- **New response model**: `AdvisorySeveritySummary` struct in `modules/fundamental/src/sbom/model/`
- **New service method**: Aggregation query in `modules/fundamental/src/sbom/service/sbom.rs` joining `sbom_advisory` table, grouping by severity, deduplicating by advisory ID
- **New endpoint**: `GET /api/v2/sbom/{id}/advisory-summary` in `modules/fundamental/src/sbom/endpoints/` with 5-minute cache
- **Cache invalidation**: Update advisory ingestion in `modules/ingestor/src/graph/advisory/mod.rs` to invalidate cached summaries when new advisories are linked to an SBOM
- **Integration tests**: New test module in `tests/api/` covering success, 404, and cache behavior
- **Documentation**: REST API reference updates for the new endpoint

## Workflow Mode

**Direct-to-main**

This is a single-repository, backend-only feature with no cross-repo atomicity constraints. All tasks target `main` directly. No feature branch bookend tasks are needed.
