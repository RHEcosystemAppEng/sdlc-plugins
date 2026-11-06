# Task 1 — Authenticate tracker calls with the service-account token via the gateway and expose an authentication proof

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — Feature has none)
**Parent Epic:** TC-9008: Tracker service-account authentication

## Repository
release-verifier

## Target Branch
main

## Description
Tracker access moves from a personal token to a new service-account token sent through the tracker API gateway (TC-9008, requirement 3). In addition, the Feature's Known Risks state that the gateway returns a successful, empty search response to an unauthenticated or under-privileged request, and that `search_issues` only exits non-zero on HTTP 401/403. That means the client today cannot tell "no matching issue" apart from "the request was never authorized". This task switches the credential and adds a positive authentication proof to the client so callers (the gate, Task 2) can refuse to trust an empty result unless the session is proven authenticated.

## Files to Modify
- `src/tracker/auth.py` — build the `Authorization` header from the service-account token instead of the personal token; fail with a clear error when the service-account token is missing/empty instead of sending an unauthenticated request
- `src/tracker/client.py` — send requests through the tracker API gateway using the service-account header; add an authentication-proof call (e.g. `verify_authenticated()` against the gateway's authenticated-identity endpoint) and a dedicated `TrackerAuthNotProvenError` (or equivalent) raised when authentication cannot be positively confirmed
- `tests/tracker/test_client.py` — tests for the new auth header, gateway routing and authentication proof

## Implementation Notes
- `src/tracker/auth.py` currently builds the tracker `Authorization` header from the configured token — keep that single construction point and change only its token source to the service-account token; do not add a second header builder.
- `src/tracker/client.py::search_issues(jql)` currently exits non-zero only on HTTP 401/403. Keep that behavior, but do NOT rely on it as the only auth signal: the gateway answers unauthenticated/under-privileged requests with HTTP 200 and an empty result.
- Add a positive proof of authentication: a call that only succeeds with a non-empty authenticated identity (e.g. the gateway's "current user / myself" endpoint, or an equivalent the gateway documents). A 200 response without an identity, or any 401/403, must be reported as "authentication not proven" (`TrackerAuthNotProvenError`), never as success. Confirm the exact gateway endpoint against the gateway API at implementation time — it is not specified in the Feature.
- Missing service-account token configuration must raise immediately in `auth.py` (fail closed) rather than producing a request without an `Authorization` header.
- The existing `search_issues(jql)` signature and return type must stay unchanged so `src/gate/resolve_issue.py::resolve_gated_issue` keeps working when this task merges on its own (direct-to-main).
- Constraints (docs/constraints.md): §2 commit rules — Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer; §3 PR rules — branch named after the task issue ID, `gh pr create --base main`, post PR link to the Jira task; §5 code change rules — scope changes to the files listed above (§5.1), inspect code before modifying (§5.2), no duplicate header/auth logic (§5.4), compare new client method against `search_issues` for parity on error handling and logging (§5.8), doc comments on every new test (§5.11).

## Reuse Candidates
- `src/tracker/auth.py` (Authorization header builder) — existing single point that builds the header; switch its token source rather than writing a new builder
- `src/tracker/client.py::search_issues` — existing HTTP request / 401-403 error handling to reuse for the new authentication-proof call

## Acceptance Criteria
- [ ] All tracker calls are sent through the tracker API gateway with an `Authorization` header built from the service-account token; the personal token is no longer used
- [ ] When the service-account token is not configured, the client fails with a non-zero / raised error before sending any request (no unauthenticated request is sent)
- [ ] The client exposes an authentication proof that succeeds only when the gateway confirms an authenticated identity
- [ ] Fail-closed: when the gateway returns HTTP 200 with an empty/identity-less response for an unauthenticated or under-privileged request, the authentication proof raises `TrackerAuthNotProvenError` (or equivalent) instead of reporting success
- [ ] HTTP 401/403 continue to produce a non-zero exit / error from `search_issues`
- [ ] `search_issues(jql)` signature and return type are unchanged

## Test Requirements
- [ ] Test that the request `Authorization` header is built from the service-account token and the request targets the gateway base URL
- [ ] Test that a missing/empty service-account token raises before any HTTP call is made (assert no request was sent)
- [ ] Test that the authentication proof succeeds when the gateway returns an authenticated identity
- [ ] Fail-closed test: mock the gateway returning HTTP 200 with an empty body / no identity (the unauthenticated "successful empty" response) and assert the authentication proof raises `TrackerAuthNotProvenError` — it must not return success
- [ ] Test that HTTP 401 and 403 from `search_issues` still result in a non-zero exit / error

## Verification Commands
- `pytest tests/tracker/test_client.py` — all tests pass

## Dependencies
- None
