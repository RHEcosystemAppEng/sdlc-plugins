## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference to document the new advisory severity aggregation endpoint introduced by TC-9001.

**What changed:** a new endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns counts of unique advisories (deduplicated by advisory ID) affecting an SBOM, bucketed by severity: `{ critical: N, high: N, medium: N, low: N, total: N }`. It returns 404 when the SBOM does not exist, responses are cached for 5 minutes and invalidated when new advisories are linked to the SBOM, and an optional `?threshold=<critical|high|medium|low>` query parameter restricts counts to severities at or above the threshold (400 on invalid values).

**Doc impact type:** Updates to existing content. Add the endpoint to the REST API reference.

**Details from Documentation Considerations:**
- User purpose: API consumers need to know the endpoint path, parameters, and response shape.
- Reference material: existing SBOM advisory endpoints documentation (e.g., `GET /api/v2/sbom/{id}/advisories`). Follow its structure and style.

Feature reference: TC-9001, "Add advisory severity aggregation endpoint".

## Acceptance Criteria
- [ ] REST API reference includes `GET /api/v2/sbom/{id}/advisory-summary` with path parameter, optional `threshold` query parameter, response schema, and example response
- [ ] Documents status codes: 200, 404 (unknown SBOM), 400 (invalid threshold)
- [ ] States that counts are unique advisories (deduplicated by advisory ID) and how `total` is computed
- [ ] Notes the 5-minute caching behavior and invalidation on advisory ingestion
- [ ] Placement and format are consistent with the existing SBOM advisory endpoint documentation

## Test Requirements
- [ ] Verify documented paths, parameters, response fields, and status codes match the implemented behavior (e.g., by calling the endpoint on a running instance)
- [ ] Verify example request/response snippets are valid and reproducible
- [ ] Verify links and cross-references to related SBOM/advisory endpoint docs resolve

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service aggregation
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate cached advisory summaries on advisory/SBOM ingestion
- Depends on: Task 4 — Support ?threshold query parameter on advisory-summary endpoint (non-MVP)
