## Repository
release-verifier

## Target Branch
main

## Description
Add a fail-closed guard to the issue resolution gate so that an empty search result from an unauthenticated or degraded gateway request causes a non-zero exit instead of silently skipping verification.

The tracker API gateway returns a successful (HTTP 200), empty search response `[]` to unauthenticated or under-privileged requests. The current implementation in `resolve_gated_issue` treats an empty result as "no matching issue" and returns `None`, which the caller interprets as a normal skip. The shell wrapper `pre-verify.sh` only detects authentication failures when the client exits non-zero, which an empty `[]` response never triggers. This creates a fail-open risk where a verifier run can finish green without ever verifying the pull request.

This task closes that gap by making the gate distinguish between a verified "no linked issue" result and a potentially degraded empty response, failing closed when the latter cannot be ruled out.

## Files to Modify
- `src/gate/resolve_issue.py` — modify `resolve_gated_issue` to validate that the tracker response is from an authenticated session before treating an empty result as a skip; raise an error or exit non-zero when the response cannot be proven authenticated
- `scripts/pre-verify.sh` — propagate the fail-closed exit from `resolve_gated_issue`; ensure that an error from the gate is surfaced as a non-zero exit code for the overall pre-verification step, not silently swallowed
- `tests/gate/test_resolve_issue.py` — add tests covering the fail-closed behavior on empty responses from unauthenticated or degraded sources

## Implementation Notes
- **Gate site:** `src/gate/resolve_issue.py`, function `resolve_gated_issue(pr_url)`. This is the specific location where the fail-closed guard must be inserted. Currently, this function calls `search_issues` and returns `None` when the result list is empty. The guard should verify that the search was performed with valid authentication before accepting an empty result as a legitimate "no linked issue" outcome.
- **Shell wrapper site:** `scripts/pre-verify.sh`. This script runs the gate before verification and currently only detects auth failures by grepping client stderr for 401/403. It must be updated to handle the new non-zero exit code from `resolve_gated_issue` when a fail-closed condition is detected.
- **Guard strategy options:** (a) Require the tracker client to return metadata (e.g., response headers, authentication status) alongside search results, so the gate can verify that the empty result came from an authenticated request. (b) Have the client validate its own authentication before executing the search (e.g., a pre-flight auth check or inspecting response headers for authentication confirmation). (c) Treat any empty result as suspicious and require explicit proof of authentication before skipping.
- The operational mitigation mentioned in the Feature's Known Risks ("a live run after merge confirms the token works") supplements this code-level guard but does not replace it.
- Per docs/constraints.md section 2 (Commit Rules): every commit must reference TC-9008 in the footer and follow Conventional Commits format.
- Per docs/constraints.md section 3 (PR Rules): the feature branch must be named after the Jira issue ID.
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to the files listed; inspect existing code before modifying.

## Acceptance Criteria
- [ ] `resolve_gated_issue` exits non-zero or raises an error when the tracker search returns an empty result from an unauthenticated or degraded source, instead of treating the empty result as a normal skip
- [ ] `resolve_gated_issue` continues to return `None` (skip) only when the empty result can be confirmed to come from an authenticated, fully privileged session
- [ ] `scripts/pre-verify.sh` surfaces the fail-closed exit from the gate as a non-zero exit code for the overall pre-verification step
- [ ] The verifier run does not finish green when the gateway returns an empty `[]` due to missing or invalid authentication

## Test Requirements
- [ ] Test that `resolve_gated_issue` raises an error or exits non-zero when `search_issues` returns an empty list from an unauthenticated or degraded session (simulated by mocking the tracker client to return `[]` without authentication proof)
- [ ] Test that `resolve_gated_issue` still returns `None` (skip) when `search_issues` returns an empty list from a confirmed authenticated session with no matching issues
- [ ] Test that `resolve_gated_issue` returns the resolved issue when `search_issues` returns a matching issue in an authenticated session
- [ ] Test that `scripts/pre-verify.sh` exits non-zero when the gate reports a fail-closed condition
- [ ] Test the end-to-end path: unauthenticated gateway request returning `[]` must cause the pre-verification step to fail, not silently skip

## Dependencies
- Depends on: Task 1 — Switch tracker authentication to the service-account token via the gateway
