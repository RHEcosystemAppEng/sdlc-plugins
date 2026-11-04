**Summary:** TC-9008: Authenticate tracker calls with the service-account token through the tracker API gateway
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Epic:** TC-9008: Service-account gateway authentication

## Repository
release-verifier

## Target Branch
main

## Description
Tracker access moves from the personal token to a new service-account token sent through the tracker API gateway (TC-9008 MVP requirement 3).

This is the change that exposes the gateway's silent-empty behavior for bad or under-privileged tokens. It must land only after the fail-closed client (Task 1) and gate (Task 2) are on `main`, so a misconfigured service-account token fails the run rather than producing a green, unverified run.

## Files to Modify
- `src/tracker/auth.py`: build the `Authorization` header from the configured service-account token instead of the personal token.
- `src/tracker/client.py`: route tracker requests (search and the Task 1 identity probe) through the tracker API gateway base URL.
- `tests/tracker/test_client.py`: cover gateway routing, the service-account header, and the fail-closed behavior with an under-privileged service-account token.

## Implementation Notes
- `src/tracker/auth.py`: replace the personal-token source with the service-account token config, for example `TRACKER_SERVICE_ACCOUNT_TOKEN`. Use the header scheme the gateway expects. If the service-account token is missing or empty, raise at startup. Do not fall back to an anonymous request, because an anonymous gateway request is exactly the silent-empty case.
- `src/tracker/client.py`: point the base URL at the gateway through configuration. The identity probe added in Task 1 must also go through the gateway with the same header, so it proves the service account's authentication on the same path the search uses.
- Remove any fallback to the personal token so that the auth source cannot become ambiguous.
- **Fail-open guard dependency:** the code-level fail-closed guards live in `src/tracker/client.py::search_issues` (Task 1) and `src/gate/resolve_issue.py::resolve_gated_issue` / `scripts/pre-verify.sh` (Task 2). This task must not weaken them. The tests below re-assert them with the service-account configuration.
- Post-merge live run: after merge, run one live verifier pass against a PR linked to a "Ready for Verification" issue to confirm the service-account token works through the gateway. This is an **extra operational check only**. The authoritative coverage for the silent-empty risk is the fail-closed ACs and tests in this task and in Tasks 1–2.
- Constraints (docs/constraints.md):
  - §2: Conventional Commits, Jira ID footer, and the `Assisted-by: Claude Code` trailer.
  - §3: branch named after the task Jira ID, `--base main`, and the PR link posted to Jira.
  - §5: change only the listed files, inspect before modifying, and reuse the existing header builder.

## Reuse Candidates
- `src/tracker/auth.py`: existing `Authorization` header builder. Change its token source rather than adding a second builder.

## Acceptance Criteria
- [ ] All tracker calls (search and identity probe) go through the tracker API gateway with the service-account token in the `Authorization` header.
- [ ] The personal token is no longer read or used.
- [ ] A missing/empty service-account token makes the client fail at startup with a non-zero exit. It never sends an unauthenticated request.
- [ ] **Fail-closed:** with a service-account token the gateway treats as unauthenticated or under-privileged (search returns HTTP 200 `[]`), the gate exits non-zero and the run fails. It does not skip verification.

## Test Requirements
- [ ] Test: the request built by the client targets the gateway base URL and carries the service-account token in `Authorization`.
- [ ] Test: missing/empty service-account token → startup error, non-zero exit, and no HTTP request sent.
- [ ] Test (degraded/empty path): gateway mocked to return HTTP 200 `[]` for search and an unauthenticated identity for the service-account token → `search_issues` raises `TrackerAuthUnprovenError` and the client exits non-zero (fail closed, not a skip).
- [ ] Post-merge (supplementary, not a replacement for the tests above): one live verifier run confirms the service-account token works through the gateway.

## Verification Commands
- `pytest tests/tracker/test_client.py tests/gate/test_resolve_issue.py`: all tests pass.

## Documentation Updates
- Repository README / configuration docs (if present): document the service-account token setting and gateway base URL, and remove the personal-token instructions.

## Dependencies
- Depends on: Task 1 — Make tracker search fail closed when authentication cannot be proven
- Depends on: Task 2 — Gate verification on a "Ready for Verification" linked issue, failing closed on unproven tracker results
