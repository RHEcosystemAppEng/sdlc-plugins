## Repository
release-verifier

## Target Branch
main

## Description
Add a fail-closed guard to the gating flow so that an empty search result from a source that cannot be proven authenticated or healthy causes the gate to fail (exit non-zero / raise an error) instead of silently skipping verification.

The documented risk is that the tracker gateway returns a successful, empty search response (`[]`) to an unauthenticated or under-privileged request. Currently, `resolve_gated_issue` in `src/gate/resolve_issue.py` treats an empty result as "no matching issue" and returns `None`, causing the verifier to skip — finishing green without verifying. The shell wrapper `scripts/pre-verify.sh` only reports auth failures on non-zero exit, which an empty `[]` never triggers.

This task introduces an authentication-health probe before the search, and modifies the gate to fail closed when the probe indicates the search source is not proven authentic.

## Files to Modify
- `src/gate/resolve_issue.py` — modify `resolve_gated_issue` to fail closed when the search returns empty and the source cannot be proven authenticated; add pre-search auth health check
- `src/tracker/client.py` — add an `is_authenticated()` or `verify_auth()` method that performs a lightweight authenticated probe (e.g., fetching the current user) to confirm the token is valid before the search
- `scripts/pre-verify.sh` — update to propagate the non-zero exit code from the fail-closed gate and report the failure reason (not just 401/403 grep)
- `tests/gate/test_resolve_issue.py` — add tests for the fail-closed behavior
- `tests/tracker/test_client.py` — add tests for the auth health probe

## Implementation Notes
- **Gate site:** `src/gate/resolve_issue.py`, function `resolve_gated_issue(pr_url)`. This is where the fail-closed guard must be added. Currently it calls `search_issues` and returns `None` when the result is empty. The new behavior: before returning `None` on an empty result, call the auth health probe. If the probe fails or returns unhealthy, raise an error (or return a sentinel that causes non-zero exit) instead of `None`.
- **Shell wrapper site:** `scripts/pre-verify.sh`. Currently greps client stderr for 401/403 to report auth failures. This must be updated to check the exit code from the gate (not just grep for specific error strings), since the fail-closed gate will exit non-zero with a different error message.
- **Auth probe in client:** `src/tracker/client.py` has `search_issues(jql)` which exits non-zero only on HTTP 401/403. Add a `verify_auth()` method that makes a lightweight authenticated request (e.g., `GET /myself` or `GET /serverInfo`) and returns a boolean indicating whether the token is valid. This decouples auth verification from the search result.
- **Decision logic in the gate:**
  ```
  results = search_issues(jql)
  if results:
      return find_ready_issue(results)
  # Empty result — is the source proven authenticated?
  if not client.verify_auth():
      raise GateError("Search returned empty but token is not proven valid — failing closed")
  # Source is authenticated, empty result is genuine
  return None  # legitimate skip
  ```
- Per docs/constraints.md §5 (Code Change Rules): the fail-closed behavior is the core change; do not refactor unrelated gate logic.

## Acceptance Criteria
- [ ] When `search_issues` returns an empty result and the source cannot be proven authenticated or healthy, `resolve_gated_issue` raises an error (or exits non-zero) instead of returning `None`
- [ ] When `search_issues` returns an empty result and the source IS proven authenticated (auth probe succeeds), `resolve_gated_issue` returns `None` (legitimate skip) as before
- [ ] `scripts/pre-verify.sh` exits non-zero and reports a meaningful error message when the gate fails closed
- [ ] The fail-closed guard is a code-level, testable mechanism — not solely an operational or post-merge check. A live run after merge may supplement but does not replace this guard
- [ ] Pull requests linked to a "Ready for Verification" issue are still verified (no regression)
- [ ] Pull requests with no linked issue and a proven-authenticated source are still skipped with a log message (no regression)

## Test Requirements
- [ ] Test that `resolve_gated_issue` raises an error when `search_issues` returns `[]` and `verify_auth()` returns `False` (unauthenticated/degraded path — fail-closed assertion)
- [ ] Test that `resolve_gated_issue` returns `None` when `search_issues` returns `[]` and `verify_auth()` returns `True` (authenticated, genuinely no matching issue — legitimate skip)
- [ ] Test that `resolve_gated_issue` returns the matching issue when `search_issues` returns a non-empty result with a "Ready for Verification" issue
- [ ] Test that `scripts/pre-verify.sh` exits non-zero when the gate fails closed (not just on 401/403)
- [ ] Test that `verify_auth()` returns `False` when the gateway returns an empty response to an unauthenticated request
- [ ] Test that `verify_auth()` returns `True` when the gateway returns a valid response to an authenticated request

## Dependencies
- Depends on: Task 1 — Service-account auth migration (the auth probe uses the same token and gateway)
