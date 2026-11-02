## Repository
release-verifier

## Target Branch
main

## Description
Migrate the tracker HTTP client authentication from the personal token to the new service-account token routed through the tracker API gateway. This changes the authorization header construction and token source without altering the client's request/response behavior. The gateway endpoint URL replaces the direct tracker URL.

## Files to Modify
- `src/tracker/auth.py` — replace personal token lookup with service-account token; update the `Authorization` header format for gateway authentication
- `src/tracker/client.py` — update the base URL to point to the tracker API gateway instead of the direct tracker endpoint
- `tests/tracker/test_client.py` — update test fixtures to use the gateway URL and service-account token

## Implementation Notes
- `src/tracker/auth.py` currently builds the `Authorization` header from a configured token. Change the token source to the service-account token (e.g., environment variable or config key) and adjust the header format if the gateway requires a different scheme (e.g., `Bearer` vs custom).
- `src/tracker/client.py` has `search_issues(jql)` which uses the base URL. Update the base URL to the gateway endpoint. The response shape from the gateway is identical to the direct tracker API — no parsing changes needed.
- Preserve the existing non-zero exit behavior on HTTP 401/403 in `client.py` — this is consumed by `scripts/pre-verify.sh` and must remain intact.
- Per docs/constraints.md §5 (Code Change Rules): keep changes scoped to authentication migration only; do not refactor unrelated client behavior.

## Acceptance Criteria
- [ ] Tracker API calls use the service-account token through the gateway
- [ ] The `Authorization` header is constructed with the service-account token, not the personal token
- [ ] The base URL points to the tracker API gateway endpoint
- [ ] Existing `search_issues` behavior (return list of issues, exit non-zero on 401/403) is preserved

## Test Requirements
- [ ] Test that `auth.py` builds the correct `Authorization` header with the service-account token
- [ ] Test that `client.py` sends requests to the gateway URL
- [ ] Test that 401/403 responses from the gateway still cause non-zero exit

## Dependencies
- None
