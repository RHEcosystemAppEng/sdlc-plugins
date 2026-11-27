**Summary:** Authenticate tracker calls with the service-account token via the gateway and make search_issues fail closed
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Parent:** Epic "TC-9008: Fail-closed tracker-gated release verification"

## Repository
release-verifier

## Target Branch
main

## Description
Move tracker access from the personal token to the new service-account token, sent through the tracker API gateway (TC-9008 requirement: "Authenticate tracker calls with the service-account token via the gateway").

The Feature's Known Risks say the gateway returns a **successful, empty** search response to an unauthenticated or under-privileged request. Today `search_issues(jql)` exits non-zero only on HTTP 401/403. On that degraded path it exits 0 with `[]`, and downstream callers cannot tell "not authenticated" apart from "no matching issue". This task makes the client fail closed: `search_issues` must return a result list only when the request is proven to have been authenticated with the service-account identity. In every other case it raises a dedicated authentication error and exits non-zero.

## Files to Modify
- `src/tracker/auth.py` — build the `Authorization` header from the configured service-account token instead of the personal token, and raise when the service-account token is missing or empty (do not send an unauthenticated request)
- `src/tracker/client.py` — route requests through the tracker API gateway. Add an authentication proof to `search_issues` so it raises / exits non-zero when authentication cannot be proven, including on HTTP 200 with an empty result
- `tests/tracker/test_client.py` — add tests for the service-account header, gateway routing, and the fail-closed degraded/empty-auth path

## Implementation Notes
- **Fail-closed gate site:** `src/tracker/client.py::search_issues`. The current check (non-zero exit only on HTTP 401/403) is the fail-open site. Do not treat a 2xx response as proof of authentication.
- **Authentication proof:** before `search_issues` returns, establish that the gateway authenticated the service-account identity, for example with a call to the gateway's authenticated-identity / current-user endpoint, cached per client instance, which must return the expected service-account principal. Another option is a gateway response signal that confirms the authenticated principal. Confirm the exact endpoint or header against the gateway API at implementation time; it is not listed in the repository structure. If the proof is missing, anonymous, or names a different principal, raise a new `TrackerAuthError` (or extend the client's existing error type, if there is one) instead of returning `[]`.
- **Keep the existing 401/403 handling.** Have it raise the same `TrackerAuthError` so callers handle a single auth-failure type.
- `src/tracker/auth.py`: read the service-account token from configuration (new setting name, e.g. `TRACKER_SERVICE_ACCOUNT_TOKEN`; follow the existing configured-token pattern in this module). Remove the use of the personal token. A missing or empty token must raise at header-build time; never send an empty `Authorization` header.
- The CLI / entry point of the client must exit non-zero on `TrackerAuthError`, so `scripts/pre-verify.sh` (Task 3) sees a failure exit.
- An operational check after merge (a live run confirming the token works) is a welcome addition, but it is not this task's coverage for the fail-open risk. The tests below are.
- Constraints (docs/constraints.md): commits follow Conventional Commits, reference TC-9008's task key in the footer, and include an `Assisted-by:` trailer (§2.1–2.3). The PR targets `main` with `--base main`, and the PR link is posted to the Jira task (§3.2–3.3). Changes stay within Files to Modify, inspect code before changing it, reuse existing helpers, and every new test gets a doc comment plus given-when-then comments for non-trivial tests (§5.1–5.4, §5.11–5.12). implement-task stays scoped to this task (§1.4–1.5).

## Reuse Candidates
- `src/tracker/auth.py` — existing `Authorization` header builder. Extend it for the service-account token rather than writing a new builder
- `src/tracker/client.py::search_issues` — existing search client with 401/403 handling. Extend it with the auth proof rather than wrapping it in a new client

## Acceptance Criteria
- [ ] Tracker requests carry an `Authorization` header built from the service-account token and are sent to the tracker API gateway. The personal token is no longer used
- [ ] With a missing or empty service-account token, the client raises `TrackerAuthError` and exits non-zero without sending a request
- [ ] **Fail-closed:** when the gateway returns HTTP 200 with an empty result (`[]`) but the request cannot be proven authenticated as the service account, `search_issues` raises `TrackerAuthError` and the client exits non-zero. It does not return `[]`
- [ ] When the gateway authenticates a different or under-privileged principal, `search_issues` raises `TrackerAuthError` and exits non-zero
- [ ] HTTP 401/403 responses still raise and exit non-zero, now as `TrackerAuthError`
- [ ] When authentication is proven, `search_issues` returns the issue list, including a legitimate empty list

## Test Requirements
- [ ] Test that the built `Authorization` header uses the service-account token and that requests target the gateway base URL
- [ ] Test that a missing or empty service-account token raises `TrackerAuthError` before any HTTP call
- [ ] **Degraded-path test:** mock the gateway to return HTTP 200 with `[]` while the auth proof is anonymous or missing. Assert that `search_issues` raises `TrackerAuthError` and the client entry point exits non-zero (not 0 with `[]`)
- [ ] Test that an authenticated proof naming the wrong or under-privileged principal raises `TrackerAuthError`
- [ ] Test that 401 and 403 responses raise `TrackerAuthError` and exit non-zero (regression)
- [ ] Test that a proven-authenticated empty result returns `[]` without raising

## Dependencies
- None
