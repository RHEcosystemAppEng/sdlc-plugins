# Task 2 — Make `search_issues` fail closed on unauthenticated or under-privileged empty results

**Summary:** TC-9008: Fail closed in search_issues when gateway authentication cannot be proven
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — TC-9008 has none)
**Parent:** none (Feature → Task hierarchy; Feature "Incorporates" this task)

## Repository
release-verifier

## Target Branch
main

## Description
TC-9008's Known Risks state that the tracker gateway answers an unauthenticated or under-privileged request with a successful, empty search response. Today `search_issues(jql)` exits non-zero only on HTTP 401/403, so in this case it exits 0 with `[]`. The result is indistinguishable from "no linked issue", and downstream the verifier finishes green without verifying the pull request.

This task makes the tracker client fail closed. `search_issues` may return an empty list only when the request is proven authenticated and authorized. Otherwise it raises a typed authentication error and the client CLI exits non-zero. The post-merge "live run" mitigation suggested in the feature is not enough on its own, so this task adds code-level coverage.

## Files to Modify
- `src/tracker/client.py` — add the authentication-proof check and a typed auth error. Make `search_issues` raise (and the CLI entry point exit non-zero) when the request isn't proven authenticated, rather than returning `[]`.
- `tests/tracker/test_client.py` — add degraded/empty-path tests

## Implementation Notes
- **Gate site:** `src/tracker/client.py::search_issues`. This is where an unauthenticated empty response currently becomes `[]` with exit 0. The guard belongs here, before the empty result is returned to callers.
- The existing behaviour only treats HTTP 401/403 as failures. Keep that, and add a second check because the gateway returns 200 + empty for unauthenticated requests. Options, in order of preference (confirm which signal the gateway supports):
  1. An authenticated-identity probe through the gateway, such as a "current user / session" endpoint, done once per client instance. If it doesn't confirm the service account, raise.
  2. Assert on a gateway response header or body field that indicates the authenticated principal. If it is absent or anonymous, raise.
- Define one typed exception (e.g. `TrackerAuthError`) in `src/tracker/client.py`. Raise it for both the existing 401/403 path and the new "auth unproven" path, so callers have one failure type to handle. Its message must clearly state that authentication or authorization could not be proven. Task 3's wrapper uses this to report the failure.
- The client's command-line entry point (the one `scripts/pre-verify.sh` invokes) must exit non-zero when `TrackerAuthError` is raised. It must never print `[]` and exit 0 on this path.
- An empty list remains a valid return value **only** after authentication has been positively confirmed.
- Constraints (docs/constraints.md):
  - §2.1–2.3: Jira key footer, Conventional Commits, `Assisted-by:` trailer.
  - §3.1–3.3: task-key branch, PR link posted to Jira, `--base main`.
  - §5.1–5.4: scoped files, inspect before modifying, follow these notes, reuse the existing 401/403 handling instead of duplicating it.

## Reuse Candidates
- `src/tracker/client.py::search_issues` — existing 401/403 non-zero-exit handling; extend it so the new auth-unproven path shares the same error type and exit behaviour
- `src/tracker/auth.py` (header builder updated in Task 1) — source of the service-account credentials the probe must confirm

## Acceptance Criteria
- [ ] When the gateway returns a successful (2xx) empty search for a request that can't be proven authenticated/authorized, `search_issues` raises `TrackerAuthError` instead of returning `[]`
- [ ] The client CLI exits non-zero, and does not print `[]` and exit 0, whenever authentication or authorization can't be proven. This applies whether the gateway returned 401/403 or a 2xx empty response.
- [ ] `search_issues` returns `[]` only when authentication has been positively confirmed and the search really matched nothing
- [ ] Existing HTTP 401/403 handling still results in a non-zero exit and now raises the same `TrackerAuthError` type

## Test Requirements
- [ ] Degraded-path test in `tests/tracker/test_client.py`: mock the gateway to return 200 with an empty result **and** a failed/anonymous auth proof (unauthenticated request). Assert that `search_issues` raises `TrackerAuthError` and does not return `[]`.
- [ ] Degraded-path test: mock an under-privileged service account (auth proof shows a principal without search permission, search returns 200 + empty). Assert that `TrackerAuthError` is raised.
- [ ] CLI test: invoke the client entry point against the unauthenticated-empty mock. Assert a non-zero exit code and that stdout does not contain `[]`.
- [ ] Positive test: with a confirmed-authenticated proof and an empty search, assert that `search_issues` returns `[]` and the CLI exits 0
- [ ] Regression test: an HTTP 401 and an HTTP 403 response each raise `TrackerAuthError` and give a non-zero CLI exit

## Dependencies
- Depends on: Task 1 — Authenticate tracker calls with the service-account token via the gateway
