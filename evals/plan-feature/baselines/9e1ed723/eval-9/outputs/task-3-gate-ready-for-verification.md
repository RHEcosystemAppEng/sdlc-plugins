# Task 3 — Gate verification on a "Ready for Verification" linked issue and fail closed in the gate and wrapper

**Summary:** TC-9008: Gate verification on "Ready for Verification" linked issue; fail closed in gate and pre-verify wrapper
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — TC-9008 has none)
**Parent:** none (Feature → Task hierarchy; Feature "Incorporates" this task)

## Repository
release-verifier

## Target Branch
main

## Description
Before running the expensive verification suite, the release verifier must look up the tracker issue linked to the pull request. It verifies only when that issue is in the "Ready for Verification" state, and it skips (with a log message) when there is no matching issue or the issue is in another state.

TC-9008's Known Risks also say the gate currently treats "no matching issue" as a normal skip, even when the empty result came from an unauthenticated request. On top of that, `scripts/pre-verify.sh` detects auth failures only by grepping client stderr for 401/403, which an empty `[]` never triggers. This task adds the state gating and makes both the gate and the wrapper fail closed, so a run can't finish green without verifying the PR. The feature's suggested "live run after merge" mitigation is kept only as an optional extra check, not as the coverage for this risk.

Covers acceptance criteria:
- Pull requests linked to a "Ready for Verification" issue are verified.
- Pull requests with no linked issue are skipped. This applies only after a proven-authenticated search.

## Files to Modify
- `src/gate/resolve_issue.py` — add the "Ready for Verification" state check in `resolve_gated_issue(pr_url)`. Return `None` (skip) only for a proven-authenticated empty result or a non-ready state, and let `TrackerAuthError` propagate so the gate exits non-zero.
- `scripts/pre-verify.sh` — fail the run on any non-zero gate/client exit (and on the explicit auth-error message) instead of relying only on grepping stderr for 401/403
- `tests/gate/test_resolve_issue.py` — add state-gating and fail-closed tests

## Implementation Notes
- **Gate site (skip logic):** `src/gate/resolve_issue.py::resolve_gated_issue`. Today it calls `search_issues` and returns `None` (skip) whenever the result is empty. Change it as follows:
  - Do not catch `TrackerAuthError` (added in Task 2) and turn it into a skip. Let it propagate, or re-raise it, so the gate process exits non-zero.
  - Return `None` with a log message such as "no linked tracker issue for <pr_url>; skipping verification" only when `search_issues` returned `[]` after confirmed authentication.
  - When a linked issue is found, compare its status to `"Ready for Verification"`. If it matches, return the issue (verify). If not, return `None` and log the actual state ("linked issue <key> is in state <state>; skipping verification").
  - Keep the state name in one module-level constant so it isn't duplicated.
- **Gate site (wrapper):** `scripts/pre-verify.sh`. Today it greps client stderr for 401/403 to report auth failures. Change it as follows:
  - Capture the gate's exit status explicitly (e.g. `set -euo pipefail`, or check `$?` directly). Treat **any** non-zero exit as a failure that stops verification and fails the job.
  - Keep the 401/403 grep only to make the error message friendlier, not to decide whether the run failed. Also recognise the `TrackerAuthError` message from Task 2 when reporting the reason.
  - A skip must come from the gate's explicit skip outcome (exit 0 with a skip signal/log), never from an empty search result alone.
- Use `search_issues` from `src/tracker/client.py` as-is. Don't add a second search path.
- Optional, supplementary only: after merge, a live run with the service-account token can further confirm the setup. That doesn't replace the tests below.
- Constraints (docs/constraints.md):
  - §2.1–2.3: Jira key footer, Conventional Commits, `Assisted-by:` trailer.
  - §3.1–3.3: task-key branch, PR link posted to Jira, `--base main`.
  - §5.1–5.4: scoped files, inspect before modifying, follow these notes, reuse `search_issues` and the existing gate structure.

## Reuse Candidates
- `src/tracker/client.py::search_issues` — the existing search client required by the feature ("Uses the existing search client")
- `src/gate/resolve_issue.py::resolve_gated_issue` — the existing gate entry point; extend it rather than adding a parallel resolver
- `scripts/pre-verify.sh` — the existing wrapper; harden its exit handling instead of adding a new wrapper

## Acceptance Criteria
- [ ] A PR whose linked tracker issue is in "Ready for Verification" is verified: `resolve_gated_issue` returns the issue and `pre-verify.sh` proceeds to verification
- [ ] A PR whose linked issue is in any other state is skipped, with a log message naming the issue key and its state
- [ ] A PR with no linked issue is skipped, with a log message, **only** when `search_issues` returned `[]` after confirmed authentication
- [ ] When the tracker source can't be proven authenticated (`TrackerAuthError`, from either a 2xx empty unauthenticated response or a 401/403), `resolve_gated_issue` does not return `None`. The gate exits non-zero instead of treating the empty result as a skip.
- [ ] `scripts/pre-verify.sh` exits non-zero and does not run or report a green verification whenever the gate exits non-zero, even when stderr contains no "401" or "403" text

## Test Requirements
- [ ] Test in `tests/gate/test_resolve_issue.py`: a mocked `search_issues` returns one issue in "Ready for Verification", and `resolve_gated_issue` returns that issue
- [ ] Test: a mocked issue in another state (e.g. "In Progress") makes `resolve_gated_issue` return `None` and log the state
- [ ] Test: a mocked authenticated empty result (`[]`) makes `resolve_gated_issue` return `None` and log the skip
- [ ] Degraded-path test: a mocked `search_issues` raising `TrackerAuthError` (simulating the gateway's unauthenticated 200 + empty response) makes `resolve_gated_issue` propagate the error, not return `None`. The gate entry point exits non-zero.
- [ ] Wrapper test (e.g. a shell test run from the test suite, or a pytest that invokes `scripts/pre-verify.sh` with a stubbed gate): the stubbed gate exits non-zero with stderr containing no "401"/"403". Assert that `pre-verify.sh` exits non-zero and the verification step is not invoked.
- [ ] Wrapper test: the stubbed gate exits 0 with an explicit skip outcome. Assert that `pre-verify.sh` exits 0 and the verification step is not invoked.

## Verification Commands
- `pytest tests/gate/test_resolve_issue.py tests/tracker/test_client.py` — all tests pass, including the fail-closed degraded-path tests

## Dependencies
- Depends on: Task 2 — Make `search_issues` fail closed on unauthenticated or under-privileged empty results
