# Task 1 — Authenticate tracker calls with the service-account token via the gateway, and expose a positive auth check

**Summary:** TC-9008: Use service-account token through tracker gateway and add positive auth verification to tracker client
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted, because TC-9008 has none)
**Epic group (by-sub-feature):** TC-9008: Tracker authentication

## Repository
release-verifier

## Target Branch
main

## Description
Tracker access moves from the personal token to a new service-account token, sent through the tracker API gateway. This task changes the auth header construction and the client base URL to use the gateway.

It also closes the client-side half of a known fail-open risk. The gateway returns a successful, empty search response (HTTP 200, `[]`) to unauthenticated or under-privileged requests. Today `search_issues` exits non-zero only on HTTP 401/403, so callers can't tell "authenticated, no matching issue" apart from "not authenticated at all". This task adds a positive authentication check, so callers can prove that the session is authenticated and has permission to search before they trust an empty result.

## Files to Modify
- `src/tracker/auth.py`: build the `Authorization` header from the configured service-account token instead of the personal token. Fail fast with a clear error when the service-account token is missing or empty.
- `src/tracker/client.py`: route calls through the tracker API gateway. Add a positive auth check (for example `verify_authenticated()`) that confirms the session's identity and search permission. Raise a dedicated auth error, which gives a non-zero exit, when that can't be proven, including when the gateway responds 200.
- `tests/tracker/test_client.py`: add tests for the gateway, the service-account header and the auth check, including the degraded 200 + `[]` path.

## Implementation Notes
- `src/tracker/auth.py`: the existing header builder reads the configured token. Switch its source to the service-account token config key. Do not keep a silent fallback to the personal token: if the service-account token is absent, raise an error. Don't send an unauthenticated request.
- `src/tracker/client.py::search_issues(jql)`: today it exits non-zero only on HTTP 401/403. Keep that behavior, and stop treating a 2xx response as proof of authentication.
- Add a positive auth check in `src/tracker/client.py` that calls a gateway endpoint whose answer proves identity and permission. Examples are an authenticated "myself"/whoami endpoint, or a known-existing canary issue or project the service account must be able to see. If the response is 200 but anonymous, empty or missing the expected identity, the session is **unauthenticated**. Raise a dedicated exception (for example `TrackerAuthError`) and exit non-zero with a stable, greppable message such as `tracker auth unverified`.
- Keep the 401/403 handling in `search_issues`. The new check adds to it and does not replace it.
- Per docs/constraints.md §2: commits must follow Conventional Commits, reference TC-9008 in the footer (for example `Implements TC-9008`), and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §3: branch named after the Jira task key. `gh pr create --base main`. Post the PR link on the Jira task.
- Per docs/constraints.md §5: limit changes to the files listed above, inspect the code before editing, reuse the existing header builder and HTTP client, and don't duplicate them.

## Reuse Candidates
- `src/tracker/auth.py` (the existing `Authorization` header builder): extend it for the service-account token rather than writing a second builder.
- `src/tracker/client.py::search_issues`: reuse its HTTP session, base-URL handling and 401/403 error path for the new auth check.

## Acceptance Criteria
- [ ] All tracker calls send the service-account token in the `Authorization` header, through the tracker API gateway.
- [ ] The personal token is no longer used. A missing or empty service-account token raises an error and no unauthenticated request is sent.
- [ ] The client exposes a positive auth check that succeeds only when the gateway confirms an authenticated identity with search permission.
- [ ] **Fail-closed:** when the gateway answers an unauthenticated or under-privileged request with a successful (2xx) empty response, the auth check raises an auth error and the client exits non-zero. An empty `[]` is never treated as proof of authentication.
- [ ] Existing behavior is kept: `search_issues` still exits non-zero on HTTP 401/403.

## Test Requirements
- [ ] Test that the `Authorization` header is built from the service-account token and that requests go to the gateway base URL.
- [ ] Test that a missing or empty service-account token raises an error before any HTTP request is sent.
- [ ] Test that the auth check passes when the mocked gateway returns an authenticated identity with search permission.
- [ ] **Degraded-path test:** the mocked gateway returns HTTP 200 with an anonymous or empty identity and `[]` for search, for invalid or no credentials. Assert that the auth check raises the auth error and the CLI exits non-zero.
- [ ] Test that HTTP 401/403 still gives a non-zero exit (regression).

## Verification Commands
- `pytest tests/tracker/test_client.py`: all tests pass.

## Dependencies
- None
