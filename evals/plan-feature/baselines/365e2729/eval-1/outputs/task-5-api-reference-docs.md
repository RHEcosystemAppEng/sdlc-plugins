## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference to document the new advisory severity aggregation endpoint introduced by TC-9001.

- **What changed**: a new endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns aggregated counts of unique vulnerability advisories by severity for a given SBOM: `{ critical, high, medium, low, total }`. It returns 404 for unknown SBOM IDs, responses are cached for 5 minutes (invalidated when new advisories are correlated to the SBOM), and it supports an optional `?threshold=<critical|high|medium|low>` query parameter that returns only counts at or above the given severity.
- **Doc impact type**: Updates — add endpoint to REST API reference.
- **User purpose**: API consumers (frontend dashboard team, alerting integrations) need to know the endpoint path, parameters, and response shape.
- **Reference material**: existing SBOM advisory endpoints documentation (e.g., `GET /api/v2/sbom/{id}/advisories`) — follow its structure and style.
- **Feature**: TC-9001 — Add advisory severity aggregation endpoint.

## Acceptance Criteria
- [ ] The REST API reference includes `GET /api/v2/sbom/{id}/advisory-summary` alongside the existing SBOM advisory endpoints
- [ ] The path parameter `{id}`, optional `threshold` query parameter (allowed values and semantics), and response shape `{ critical, high, medium, low, total }` are documented
- [ ] Deduplication semantics (unique advisories by advisory ID), the 404 behavior, the 400 for invalid threshold values, and the 5-minute caching behavior are documented
- [ ] At least one example request/response is included for both the unfiltered and `?threshold=critical` cases

## Test Requirements
- [ ] Verify every documented field, parameter, and status code matches the implemented behavior (compare against the endpoint's integration tests)
- [ ] Verify the example requests return the documented responses against a running instance
- [ ] Verify the new section is consistent in format with the existing SBOM advisory endpoint documentation

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Invalidate advisory-summary cache on advisory ingestion
- Depends on: Task 4 — Add optional severity threshold filter to advisory-summary endpoint
