# Task 1 — Authenticate tracker calls with the service-account token via the API gateway

**Summary**: TC-9008: Authenticate tracker calls with service-account token via gateway and expose auth proof
**Issue type**: Task | **Labels**: ai-generated-jira | **Priority**: Major (inherited) | **fixVersions**: omitted (Feature has none)
**Links**: TC-9008 incorporates this task

---

## Repository
release-verifier

## Target Branch
main

## Description
Tracker access moves from a personal token to a new service-account token sent through the tracker API gateway (TC-9008, requirement 3). This task changes the `Authorization` header construction and the client's target so that every tracker call goes through the gateway with the service-account token.

The gateway has a known fail-open behavior: it returns a successful, **empty** search response to unauthenticated or under-privileged requests instead of 401/403. Because of this, the client must also give callers a way to prove that a request was authenticated and authorized. An empty `[]` alone cannot be trusted. The gate (Task 2) relies on this proof to fail closed.

## Files to Modify
- `src/tracker/auth.py` — build the `Authorization` header from the configured service-account token instead of the personal token, and raise a clear error when the token is missing or empty
- `src/tracker/client.py` — send requests to the tracker API gateway base URL. Add an auth-proof capability (for example `verify_authenticated()`, or an authenticated-search result type) that raises a dedicated `TrackerAuthError` when the gateway cannot confirm an authenticated, authorized principal
- `tests/tracker/test_client.py` — add tests for the gateway or service-account wiring and for the auth-proof failure path

## Implementation Notes
- `src/tracker/auth.py` currently builds the tracker `Authorization` header from "the configured token". Keep that function as the single place the header is built. Swap its token source to the service-account token setting rather than adding a second header builder.
- `src/tracker/client.py::search_issues(jql)` currently exits non-zero **only** on HTTP 401/403. This is the root of the fail-open risk: the gateway answers unauthenticated or under-privileged requests with 200 and `[]`. Do not depend on 401/403 alone.
- **Auth proof (fail-closed guard, client side)**: add a client function that proves the current credentials resolve to an authenticated principal with search permission. One example is a gateway identity or permission check made with the same headers as `search_issues`. It must raise `TrackerAuthError` (non-zero exit when the client runs as a CLI) when the response is anonymous, unauthenticated, under-privileged or empty. Confirm the gateway's exact identity endpoint or auth-indicator header with the gateway owners at implementation time. Do not hard-code a guessed path without checking it.
- Missing or empty service-account token configuration must fail closed: raise before any request is sent, never send an unauthenticated request.
- Keep the existing return contract of `search_issues` (a list of issues) so existing callers keep working. Task 2 changes the gate to call the auth proof.
- Constraints (docs/constraints.md):
  - §1.4/§5.1: keep changes to the listed files.
  - §5.2: inspect `client.py`/`auth.py` before editing.
  - §5.4: reuse the existing header builder and HTTP client, no duplicate HTTP stack.
  - §5.8: error-handling parity with the existing 401/403 handling.
  - §2.1–2.3: commits use Conventional Commits, an `Implements <task-key>` footer and an `Assisted-by:` trailer.
  - §3.1–3.3: branch named after the task key, PR `--base main`, PR link posted to Jira.

## Reuse Candidates
- `src/tracker/auth.py` (Authorization header builder) — extend its token source rather than writing a new builder
- `src/tracker/client.py::search_issues` — reuse its request and session setup and its existing 401/403 error path for the new auth proof
- `tests/tracker/test_client.py` — follow the existing client test structure and HTTP mocking approach

## Acceptance Criteria
- [ ] Every tracker request carries an `Authorization` header built from the service-account token. The personal token is no longer read.
- [ ] Tracker requests go to the tracker API gateway base URL.
- [ ] If the service-account token is missing or empty, the client raises an error and exits non-zero without sending a request.
- [ ] The client exposes an auth proof that **fails closed**: when the gateway cannot confirm an authenticated, authorized principal (anonymous, under-privileged, or a successful-but-empty response to an unauthenticated request), it raises `TrackerAuthError` and exits non-zero. It never returns success or an empty result.
- [ ] Existing HTTP 401/403 handling in `search_issues` still exits non-zero.

## Test Requirements
- [ ] A test asserts the `Authorization` header is built from the service-account token and the request targets the gateway base URL.
- [ ] A test with a missing or empty service-account token asserts an error is raised (non-zero exit) and no HTTP request is made.
- [ ] **Fail-closed test**: mock the gateway to return HTTP 200 with an empty body or `[]` for an unauthenticated or under-privileged request. Assert the auth proof raises `TrackerAuthError` (non-zero exit) and does not report success.
- [ ] A test asserts the auth proof succeeds when the gateway confirms an authenticated principal.
- [ ] The existing 401/403 tests still pass.

## Verification Commands
- `pytest tests/tracker/test_client.py` — all tests pass

## Dependencies
- None
