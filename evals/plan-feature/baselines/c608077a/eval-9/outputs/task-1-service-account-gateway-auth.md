# Task 1 — Authenticate tracker calls with the service-account token via the gateway

**Summary:** TC-9008: Authenticate tracker calls with the service-account token via the API gateway
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — Feature has none)
**Epic:** TC-9008: Tracker gateway authentication

## Repository
release-verifier

## Target Branch
main

## Description
Tracker access moves from a personal token to a new service-account token, and tracker calls must be sent through the tracker API gateway (TC-9008, requirement "Authenticate tracker calls with the service-account token via the gateway"). This task switches the credential source used to build the `Authorization` header and points the tracker HTTP client at the gateway. It does not change search semantics — fail-closed handling of degraded/empty responses is owned by Task 2.

## Files to Modify
- `src/tracker/auth.py` — build the tracker `Authorization` header from the configured service-account token instead of the personal token
- `src/tracker/client.py` — send all tracker requests (including `search_issues`) through the tracker API gateway base URL using the header from `auth.py`
- `tests/tracker/test_client.py` — cover the new header source and gateway routing

## Implementation Notes
- `src/tracker/auth.py` already builds the `Authorization` header from "the configured token"; change the configured source to the service-account token (new config key, e.g. `TRACKER_SERVICE_ACCOUNT_TOKEN`) and remove use of the personal token. Keep header construction in `auth.py` so `client.py` continues to consume a single header-building function.
- If the service-account token is missing or empty, raise a configuration error at header-build time — do not send an unauthenticated request (an unauthenticated request to the gateway returns a successful empty response, see Feature "Known Risks"). This is the first line of the fail-closed defence; Task 2 adds the response-side guard.
- `src/tracker/client.py`: replace the tracker base URL with the gateway base URL (new config key, e.g. `TRACKER_GATEWAY_URL`); every request path in the client must use it.
- Do not log the token value.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules (Jira ID footer `Implements <task-key>`, Conventional Commits, `Assisted-by:` trailer); §3.1–3.3 PR rules (branch named after the task Jira ID, PR link posted to Jira, `gh pr create --base main`); §5.1–5.4 code change rules (scope to listed files, inspect before modifying, follow referenced patterns, no duplication); §1.4–1.5 implement-task scope rules.

## Reuse Candidates
- `src/tracker/auth.py` (header builder) — existing `Authorization` header construction; extend its token source rather than adding a second header builder
- `src/tracker/client.py::search_issues` — existing search client to be routed through the gateway; do not introduce a parallel client

## Acceptance Criteria
- [ ] Tracker requests carry an `Authorization` header built from the service-account token; the personal token is no longer read.
- [ ] All tracker requests made by `src/tracker/client.py` (including `search_issues`) are sent to the tracker API gateway base URL.
- [ ] When the service-account token is missing or empty, header construction raises an error and no request is sent (fail closed — never send an unauthenticated request).
- [ ] The token value is never written to logs.

## Test Requirements
- [ ] Test that the header built by `auth.py` uses the service-account token value.
- [ ] Test that `search_issues` issues its HTTP request against the gateway base URL with that header (mocked transport).
- [ ] Test that a missing/empty service-account token raises before any HTTP request is attempted (assert the mocked transport is never called).

## Dependencies
- None
