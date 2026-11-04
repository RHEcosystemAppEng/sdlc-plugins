**Summary:** TC-9008: Make tracker search fail closed when authentication cannot be proven
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Epic:** TC-9008: Fail-closed tracker gating

## Repository
release-verifier

## Target Branch
main

## Description
The tracker gateway returns a successful, empty search response (`[]`, HTTP 200) to unauthenticated or under-privileged requests. Today `search_issues(jql)` in the tracker client exits non-zero only on HTTP 401/403. A degraded request is therefore indistinguishable from "no matching issue", and the release gate can skip verification and finish green without ever verifying the pull request (TC-9008, Known Risks).

This task makes the tracker client fail closed. It should return an empty list only when the caller's authentication and search permission have been proven. Otherwise it raises a dedicated error and the CLI entry point exits non-zero. This is the building block that the gate (Task 2) relies on, and it must land before tracker auth is switched to the gateway (Task 3).

## Files to Modify
- `src/tracker/client.py`: add an authentication proof (authenticated-identity probe and/or response validation) used by `search_issues`. Raise a dedicated error and exit non-zero when an empty result cannot be proven authenticated.
- `tests/tracker/test_client.py`: add tests for the degraded/empty fail-closed path and the proven-authenticated empty path.

## Implementation Notes
- **Gate/skip site:** `src/tracker/client.py::search_issues`. This is where `[]` is returned today. Add the guard here so that no caller can mistake an unauthenticated empty response for "no match".
- Introduce a dedicated exception, for example `TrackerAuthUnprovenError` (subclass of the client's existing error type if one exists). Raise it when:
  - the result is empty **and** the authenticated-identity check has not succeeded for this client/session, or
  - the response is missing the fields a real authenticated search returns (for example a `total` count or similar metadata). Inspect the actual gateway response shape at implementation time.
- Authenticated-identity check: make one lightweight call to the gateway's current-user / "myself" endpoint, or the equivalent. Confirm the exact endpoint against the gateway. Cache the result per client instance. If that call returns no identity, an anonymous identity, or a non-2xx status, treat the client as unauthenticated.
- Keep the existing 401/403 → non-zero exit behavior. Map `TrackerAuthUnprovenError` to its own **distinct non-zero exit code** in the client's CLI entry point, so `scripts/pre-verify.sh` (Task 2) can tell it apart from success.
- Do not change the header construction in `src/tracker/auth.py` in this task. The token switch is Task 3.
- Constraints (docs/constraints.md):
  - §2: Conventional Commits, Jira ID in the footer (`Implements TC-xxxx`), and the `Assisted-by: Claude Code` trailer.
  - §3: branch named after the task's Jira ID, `gh pr create --base main`, and the PR link posted to Jira.
  - §5: change only the listed files, inspect before modifying, and reuse existing client error handling rather than duplicating it.

## Reuse Candidates
- `src/tracker/client.py::search_issues`: existing HTTP call and 401/403 handling. Extend it rather than adding a parallel search function.
- `src/tracker/auth.py`: existing `Authorization` header builder. Reuse it for the identity probe request.

## Acceptance Criteria
- [ ] When the tracker returns an empty search result and the client cannot prove it is authenticated (identity probe fails, returns anonymous, or the response is missing authenticated-search metadata), `search_issues` raises `TrackerAuthUnprovenError` instead of returning `[]`.
- [ ] The client CLI exits with a distinct non-zero code (not 0) in that case, so an empty `[]` from a degraded request can never surface as success.
- [ ] When authentication is proven and the search genuinely matches nothing, `search_issues` returns `[]` and exits 0.
- [ ] Existing HTTP 401/403 handling still exits non-zero.

## Test Requirements
- [ ] Test: mock the gateway to return HTTP 200 with `[]` for the search and an unauthenticated/anonymous identity probe. Assert `search_issues` raises `TrackerAuthUnprovenError` and does not return `[]`.
- [ ] Test: mock HTTP 200 with `[]` and missing authenticated-search metadata. Assert the fail-closed error.
- [ ] Test: run the client CLI entry point on the degraded/empty path. Assert a non-zero exit code equal to the dedicated auth-unproven code.
- [ ] Test: proven-authenticated identity plus empty search returns `[]` with exit 0.
- [ ] Test: the existing 401/403 test cases still exit non-zero (regression).

## Verification Commands
- `pytest tests/tracker/test_client.py`: all tests pass, including the new fail-closed cases.

## Dependencies
- None
