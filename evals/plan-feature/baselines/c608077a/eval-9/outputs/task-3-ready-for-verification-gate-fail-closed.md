# Task 3 — Gate verification on a "Ready for Verification" linked issue, failing closed on unproven tracker results

**Summary:** TC-9008: Gate verification on a "Ready for Verification" linked issue and fail closed in gate and pre-verify wrapper
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — Feature has none)
**Epic:** TC-9008: Verification gating

## Repository
release-verifier

## Target Branch
main

## Description
Before running the expensive verification suite, the release verifier must look up the tracker issue linked to the pull request and verify only pull requests whose linked issue is in the "Ready for Verification" state; pull requests with no matching issue are skipped with a log message (TC-9008 requirements 1 and 2, acceptance criteria 1 and 2).

TC-9008 "Known Risks" also identifies two fail-open gate sites:
- `resolve_gated_issue` treats an empty search result as a normal skip, so an unauthenticated empty `[]` makes the run finish green without verifying.
- `scripts/pre-verify.sh` only reports an authentication failure when it greps 401/403 in client stderr on a non-zero exit, which an empty `[]` never triggers.

This task implements the state gate and makes both gate sites fail closed: a skip is only allowed when the tracker client has proven authentication (Task 2); any auth-unproven or non-zero client outcome fails the pre-verify step.

## Files to Modify
- `src/gate/resolve_issue.py` — filter the linked issue by "Ready for Verification" state; skip with a log message for no linked issue / other states; propagate auth-unproven errors as hard failures instead of returning `None`
- `scripts/pre-verify.sh` — fail (non-zero) on any non-zero gate exit, specifically on the auth-unproven exit code, rather than relying only on a 401/403 stderr grep
- `tests/gate/test_resolve_issue.py` — add state-gate tests and degraded/empty-path tests

## Files to Create
- `tests/gate/test_pre_verify_wrapper.py` — tests that execute `scripts/pre-verify.sh` with a stubbed gate/client and assert its exit status on degraded paths

## Implementation Notes
- **Gate site 1:** `src/gate/resolve_issue.py::resolve_gated_issue(pr_url)`. Currently calls `search_issues` and returns `None` (skip) when the result is empty. Change to:
  - Call `search_issues` (from `src/tracker/client.py`, routed through the gateway by Task 1). Let `TrackerAuthUnprovenError` (Task 2) and 401/403 failures propagate (or convert into a distinct non-zero exit) — never catch them and return `None`.
  - Return `None` (skip, with an info log including the PR URL and reason "no linked issue") **only** when `search_issues` returned `[]` successfully, which after Task 2 implies authentication was proven.
  - When a linked issue exists but its state is not "Ready for Verification", return `None` with a log message stating the actual state.
  - When the linked issue's state is "Ready for Verification", return the issue so verification runs.
  - Do not add a broad `except Exception: return None`; that would reopen the fail-open path.
- **Gate site 2:** `scripts/pre-verify.sh`. Currently greps client stderr for 401/403 to report auth failures. Change to:
  - Capture the gate's exit status explicitly (`set -euo pipefail`, or check `$?` directly — ensure pipes such as `| grep` do not mask the exit status).
  - Treat any non-zero gate exit as a failure of the pre-verify step (exit non-zero), and report the auth-unproven exit code from Task 2 with a clear "tracker authentication could not be proven" message. Keep the 401/403 grep only as an additional diagnostic message, not as the failure condition.
  - Only a zero exit with an explicit "skip" outcome from the gate may skip verification.
- The post-merge live run suggested in the Feature is a supplementary check only; this task's tests are the required coverage.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.1–3.3 PR rules; §5.1–5.4 code change rules; §5.6 trace the data flow PR URL → search → state filter → wrapper exit; §5.8 parity with the client's auth-failure handling; §1.4–1.5 implement-task scope rules.

## Reuse Candidates
- `src/tracker/client.py::search_issues` — existing search client ("Uses the existing search client" per Feature requirement 1); reuse it, do not add a new search call
- `src/gate/resolve_issue.py::resolve_gated_issue` — existing gate function; extend it rather than adding a parallel resolver
- `scripts/pre-verify.sh` — existing auth-failure reporting; keep its messaging but change the failure condition

## Acceptance Criteria
- [ ] Pull requests whose linked issue is in "Ready for Verification" state are returned by `resolve_gated_issue` and verified.
- [ ] Pull requests with no linked issue are skipped with a log message — only when `search_issues` returned `[]` with proven authentication.
- [ ] Pull requests whose linked issue is in any other state are skipped with a log message naming the state.
- [ ] **Fail closed (gate):** when `search_issues` raises the auth-unproven error (or fails with 401/403), `resolve_gated_issue` does not return `None`/skip; the gate exits non-zero instead of treating the empty result as a skip.
- [ ] **Fail closed (wrapper):** `scripts/pre-verify.sh` exits non-zero whenever the gate exits non-zero — including the auth-unproven exit code with no 401/403 text in stderr — and never proceeds to a green "skipped" outcome in that case.
- [ ] `scripts/pre-verify.sh` skips verification only on a zero gate exit with an explicit skip outcome.

## Test Requirements
- [ ] Test: linked issue in "Ready for Verification" → `resolve_gated_issue` returns the issue.
- [ ] Test: linked issue in another state (e.g., "In Progress") → returns `None` and logs the state.
- [ ] Test: authenticated empty result (`search_issues` returns `[]`) → returns `None` and logs "no linked issue".
- [ ] Test (degraded path): `search_issues` mocked to raise `TrackerAuthUnprovenError` (simulating gateway 200 + `[]` without proven auth) → `resolve_gated_issue` raises / gate exits non-zero; assert it does NOT return `None`.
- [ ] Test (wrapper degraded path): run `scripts/pre-verify.sh` with a stubbed gate that exits with the auth-unproven code and writes no 401/403 text to stderr → assert the wrapper exits non-zero and does not report a skip.
- [ ] Test (wrapper): stubbed gate exits 0 with skip outcome → wrapper exits 0 and reports skip; stubbed gate returns ready issue → wrapper proceeds to verification.

## Verification Commands
- `pytest tests/gate/` — all gate and wrapper tests pass, including the fail-closed degraded-path tests

## Dependencies
- Depends on: Task 2 — Make tracker search fail closed when authentication cannot be proven
