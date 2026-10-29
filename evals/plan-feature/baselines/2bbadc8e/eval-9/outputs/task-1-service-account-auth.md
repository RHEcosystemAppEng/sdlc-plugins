## Repository
release-verifier

## Target Branch
main

## Description
Replace the personal token authentication with a service-account token routed through the tracker API gateway. The tracker HTTP client currently builds an `Authorization` header from a configured personal token. This task switches the token source to the new service-account credential and updates the client to route all tracker API requests through the gateway endpoint.

## Files to Modify
- `src/tracker/auth.py` — replace personal token lookup with service-account token configuration; update the `Authorization` header builder to use the new credential
- `src/tracker/client.py` — update the base URL or request routing to send tracker API calls through the gateway endpoint instead of the direct tracker URL
- `tests/tracker/test_client.py` — update existing tests to use the service-account token and gateway routing; add tests for token configuration errors

## Implementation Notes
- `src/tracker/auth.py` currently builds the `Authorization` header from a configured token. Change the token source to read the service-account token (e.g., from an environment variable or configuration file). Preserve the same header format expected by the gateway.
- `src/tracker/client.py` contains the HTTP client with `search_issues(jql)`. Update the base URL to point at the tracker API gateway. Ensure that the gateway-routed requests still return the same response shape as direct tracker calls.
- The gateway returns a successful, empty response `[]` for unauthenticated or under-privileged requests (see Known Risks in TC-9008). This task focuses on the auth switch only; the fail-closed guard for empty responses is handled in Task 2.
- Per docs/constraints.md section 2 (Commit Rules): every commit must reference TC-9008 in the footer and follow Conventional Commits format.
- Per docs/constraints.md section 3 (PR Rules): the feature branch must be named after the Jira issue ID.

## Acceptance Criteria
- [ ] Tracker API calls use the service-account token instead of the personal token
- [ ] Tracker API calls are routed through the gateway endpoint
- [ ] The `Authorization` header is built from the service-account token credential
- [ ] Existing `search_issues` functionality is preserved (same interface, same response shape)

## Test Requirements
- [ ] Test that `auth.py` builds the `Authorization` header from the service-account token
- [ ] Test that `client.py` routes requests to the gateway endpoint URL
- [ ] Test that `search_issues` returns the expected response through the gateway
- [ ] Test error handling when the service-account token is missing or misconfigured

## Dependencies
- None
