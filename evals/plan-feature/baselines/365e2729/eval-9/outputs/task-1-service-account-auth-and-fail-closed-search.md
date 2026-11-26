# Task 1 — Authenticate tracker calls with the service-account token via the gateway and fail closed on unproven authentication

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — TC-9008 has none)

## Repository
release-verifier

## Target Branch
main

## Description
TC-9008 moves tracker access from a personal token to a new service-account token sent through the tracker API gateway. The gateway has a known fail-open behavior: it returns a successful (HTTP 200), empty search response to an unauthenticated or under-privileged request, so `search_issues(jql)` currently exits 0 with `[]` and only treats HTTP 401/403 as an error.

This task (a) switches `src/tracker/auth.py` and `src/tracker/client.py` to the service-account token and gateway base URL, and (b) gives the client a positive proof of authentication so an empty result can be trusted only when the caller is provably authenticated with the expected service account. When authentication cannot be proven, the client must fail closed (raise a typed error / exit non-zero) instead of returning `[]`.

## Files to Modify
- `src/tracker/auth.py` — build the `Authorization` header from the service-account token (replacing the personal token); fail with a clear error when the token is missing or empty instead of sending an unauthenticated request
- `src/tracker/client.py` — route requests through the tracker API gateway; add `verify_authenticated()` and make `search_issues(jql)` fail closed when authentication is not proven
- `tests/tracker/test_client.py` — cover the service-account header, gateway routing, and the unauthenticated-empty fail-closed path

## Implementation Notes
- **Auth header** (`src/tracker/auth.py`): replace the personal-token source with the service-account token setting. If the configured token is absent or blank, raise a configuration error immediately — never fall through to building a request without `Authorization`, since the gateway would answer it with a green `[]`.
- **Positive auth proof** (`src/tracker/client.py`): add `verify_authenticated()` that calls the gateway's identity endpoint (e.g. a "myself"/whoami route — confirm the exact path against gateway docs at implementation time) and asserts that the response is non-empty and identifies the configured service account. If the gateway exposes no identity endpoint, use a configured canary JQL query for an issue the service account is known to be able to see, and treat an empty canary result as unauthenticated. Cache the result per client instance so the probe runs once per verifier run.
- **Fail-closed search** (`src/tracker/client.py::search_issues`): today it exits non-zero only on HTTP 401/403. Keep that behavior, and additionally raise a dedicated `TrackerAuthError` (or exit non-zero when run as a CLI) when `verify_authenticated()` fails, so `[]` is only ever returned from a proven-authenticated session. Do not convert this error into an empty list anywhere in the client.
- Emit the auth failure to stderr with a stable marker (e.g. `TRACKER_AUTH_UNVERIFIED`) so downstream consumers (Task 2's gate, Task 3's wrapper) can identify it; the exit code, not the marker, is the authoritative signal.
- Cross-cutting: `search_issues` gains a new error path. Grep for all callers of `search_issues` (known: `src/gate/resolve_issue.py::resolve_gated_issue`) and confirm none swallow exceptions into `[]`; any additional callers found must be listed in the PR.
- Constraints (docs/constraints.md): commits follow Conventional Commits, reference the Jira task in the footer, include an `Assisted-by:` trailer (§2.1–2.3); branch named after the task ID, PR opened with `--base main`, PR link posted on the Jira task (§3.1–3.3); keep changes scoped to the listed files, inspect code before modifying, reuse existing client/auth code rather than duplicating it (§5.1–5.4). Tests require doc comments and given-when-then comments for non-trivial cases (§5.11–5.12).

## Reuse Candidates
- `src/tracker/auth.py` — existing `Authorization` header builder; extend it to read the service-account token instead of writing a parallel builder
- `src/tracker/client.py::search_issues` — existing HTTP 401/403 non-zero exit handling; reuse the same error path for the unproven-auth case
- `tests/tracker/test_client.py` — existing client test fixtures / HTTP mocking for new cases

## Acceptance Criteria
- [ ] Tracker requests carry an `Authorization` header built from the service-account token and are sent to the tracker API gateway; the personal token is no longer used.
- [ ] When the service-account token is missing or blank, the client raises a configuration error before sending any request (no unauthenticated request is issued).
- [ ] **Fail-closed:** when the gateway returns HTTP 200 with an empty search result and `verify_authenticated()` cannot prove the session is authenticated as the configured service account (empty/anonymous identity response or empty canary), `search_issues` raises `TrackerAuthError` / exits non-zero instead of returning `[]`.
- [ ] `search_issues` continues to exit non-zero on HTTP 401/403.
- [ ] When authentication is proven, `search_issues` returns `[]` for a genuinely empty search (no false failure).

## Test Requirements
- [ ] Test that the request `Authorization` header uses the service-account token and the gateway base URL.
- [ ] Test that a missing/blank service-account token raises a configuration error and no HTTP request is made.
- [ ] **Fail-closed test:** mock the gateway to return HTTP 200 with `[]` for the search and an empty/anonymous identity response (unauthenticated/under-privileged path); assert `search_issues` raises `TrackerAuthError` (or exits non-zero) and does not return `[]`.
- [ ] Test that HTTP 401 and 403 still produce a non-zero exit / error.
- [ ] Test that with a valid identity response for the service account, an empty search returns `[]` without error.

## Verification Commands
- `pytest tests/tracker/test_client.py` — all tests pass, including the unauthenticated-empty fail-closed case

## Documentation Updates
- Configuration/setup docs for release-verifier (if present) — document the new service-account token setting and gateway URL, and that the personal token is no longer used

## Dependencies
- None
