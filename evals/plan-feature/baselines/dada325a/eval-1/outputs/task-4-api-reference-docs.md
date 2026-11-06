## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to cover the new advisory severity summary endpoint delivered under Feature TC-9001 ("Add advisory severity aggregation endpoint").

**What changed**: a new endpoint, `GET /api/v2/sbom/{id}/advisory-summary`, returns aggregated advisory severity counts for an SBOM as `{ critical, high, medium, low, total }`. Each advisory is counted once (deduplicated by advisory ID). The endpoint returns 404 for an unknown SBOM ID. Responses are cached for 5 minutes, and the cache is invalidated when the advisory ingestion pipeline links new advisories to the SBOM. An optional `?threshold=<critical|high|medium|low>` parameter limits the response to severities at or above the given level (non-MVP; document it only if Task 3 has shipped).

**Doc impact type**: Updates. Add the endpoint to the existing REST API reference.

**From Documentation Considerations**:
- User purpose: API consumers need to know the endpoint path, parameters, and response shape.
- Reference material: the existing documentation for the SBOM advisory endpoints.

Feature reference: TC-9001.

## Acceptance Criteria
- [ ] The REST API reference lists `GET /api/v2/sbom/{id}/advisory-summary` next to the existing SBOM advisory endpoints
- [ ] The documented response shape matches the implemented JSON (`critical`, `high`, `medium`, `low`, `total`, all integers), including how `total` treats advisories with unknown severity
- [ ] The 404 behavior for unknown SBOM IDs is documented
- [ ] The 5-minute caching and the invalidation-on-ingestion behavior are described so consumers know how fresh the data is
- [ ] The `threshold` query parameter (accepted values, at-or-above semantics, 400 on invalid values) is documented if Task 3 has shipped, and omitted otherwise
- [ ] A request/response example is included, consistent with the style of the existing SBOM advisory endpoint docs

## Test Requirements
- [ ] Run each documented example request against a running build and confirm the response matches the documented shape and status codes
- [ ] Review the documented parameters, status codes, and caching behavior against the merged implementation (Tasks 1–3) for accuracy and completeness
- [ ] Confirm the new section follows the formatting and terminology of the existing SBOM advisory endpoint documentation

## Dependencies
- Depends on: Task 1 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 2 — Cache advisory summary for 5 minutes with ingestion-driven invalidation
- Depends on: Task 3 — Add optional threshold filter to advisory summary endpoint
