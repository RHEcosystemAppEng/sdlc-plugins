## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The feature TC-9001 adds a severity aggregation endpoint that API consumers need documented.

Documentation considerations from the feature:
- **Doc impact type:** Updates to existing content
- **User purpose:** API consumers need to know the endpoint path, parameters, and response shape
- **Reference material:** Existing SBOM advisory endpoints documentation

The documentation should cover:
- Endpoint path and HTTP method
- Path parameters (SBOM ID)
- Optional query parameters (`threshold` for severity filtering)
- Response body shape with field descriptions
- Error responses (404 for missing SBOM, 400 for invalid threshold)
- Cache behavior (5-minute cache with invalidation on advisory ingestion)

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation describes the response shape: `{ critical, high, medium, low, total }`
- [ ] Documentation describes the optional `?threshold` query parameter and its valid values
- [ ] Documentation describes error responses (404, 400)
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the endpoint's actual behavior
- [ ] Verify request/response examples match the implementation
- [ ] Verify documentation is consistent with existing SBOM endpoint documentation style

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
- Depends on: Task 5 — Add optional threshold query parameter for severity filtering
