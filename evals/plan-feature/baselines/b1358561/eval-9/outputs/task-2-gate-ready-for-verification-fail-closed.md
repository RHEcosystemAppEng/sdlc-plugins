**Summary:** Gate verification on a "Ready for Verification" linked issue with fail-closed resolution
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Parent:** Epic "TC-9008: Fail-closed tracker-gated release verification"

## Repository
release-verifier

## Target Branch
main

## Description
Before the expensive verification suite runs, look up the tracker issue linked to the pull request. Verify the PR only when the linked issue is in the "Ready for Verification" state. Otherwise, skip with a log message (TC-9008 requirements 1 and 2).

Today `resolve_gated_issue(pr_url)` returns `None` (skip) whenever `search_issues` returns an empty result. The Feature's Known Risks note that an unauthenticated gateway request produces exactly that empty result, so "no matching issue" can turn a failed authentication into a green skip. This task makes the gate fail closed: a skip is allowed only after an authenticated search (as guaranteed by Task 1) has run. Any authentication failure, or unproven authentication, propagates as an error that stops the run with a non-zero exit.

## Files to Modify
- `src/gate/resolve_issue.py` — add the "Ready for Verification" state check, keep the logged skip for "no linked issue" / "not ready", and stop converting auth or unproven-auth conditions into `None`
- `tests/gate/test_resolve_issue.py` — add tests for verify, skip, and the fail-closed degraded path

## Implementation Notes
- **Fail-closed gate site:** `src/gate/resolve_issue.py::resolve_gated_issue`. The empty-result → `None` branch is the skip site that can fail open. It must not catch `TrackerAuthError` (from Task 1, raised by `src/tracker/client.py::search_issues`). Also do not add any broad `except Exception` that returns `None`.
- Return values: (a) a linked issue in "Ready for Verification" → return the issue (verify). (b) A linked issue in any other state → return `None` and log the issue key and its current state. (c) An empty result from an authenticated search → return `None` and log "no linked issue". (d) `TrackerAuthError` or any other tracker error → propagate so the process exits non-zero. If the call site needs to tell "skip" apart from "verify" without relying on `None`, consider an explicit result (e.g. a small enum or `GateDecision` with `VERIFY` / `SKIP` plus a reason). Task 3 uses this so the wrapper can treat skip as an explicit signal.
- Compare the state against the literal "Ready for Verification" using the same status field `search_issues` already returns. Do not use a substring match.
- Keep the existing JQL lookup of the PR-linked issue unchanged; this task only changes how the result is interpreted.
- An operational post-merge live run can be an extra check, but it does not replace the fail-closed test below.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules (Conventional Commits, Jira key footer, `Assisted-by:` trailer). §3.2–3.3 PR rules (`--base main`, PR link on the Jira task). §5.1–5.4 and §5.11–5.12 code-change and test-documentation rules. §1.4–1.5 implement-task scope.

## Reuse Candidates
- `src/tracker/client.py::search_issues` — existing search used by the gate. After Task 1 it guarantees authenticated results or raises `TrackerAuthError`. Reuse it; do not add a second lookup
- `src/gate/resolve_issue.py::resolve_gated_issue` — extend the existing function instead of adding a parallel gate

## Acceptance Criteria
- [ ] A PR whose linked issue is "Ready for Verification" resolves to "verify"
- [ ] A PR whose linked issue is in any other state resolves to "skip" and logs the issue key and state
- [ ] A PR with no linked issue (an empty result from an authenticated search) resolves to "skip" and logs "no linked issue"
- [ ] **Fail-closed:** when `search_issues` raises `TrackerAuthError` (including the case where the gateway returned an empty `[]` without proven authentication), `resolve_gated_issue` does not return a skip. The error propagates and the gate exits non-zero
- [ ] Any other tracker or client error also propagates instead of becoming a skip

## Test Requirements
- [ ] Test that a linked issue in "Ready for Verification" yields "verify"
- [ ] Test that a linked issue in a different state (e.g. "In Progress") yields "skip" with a log message containing the issue key and state
- [ ] Test that an authenticated empty result yields "skip" with a "no linked issue" log message
- [ ] **Degraded-path test:** stub `search_issues` to raise `TrackerAuthError` (simulating the unauthenticated gateway returning `[]`). Assert that `resolve_gated_issue` raises, never returns `None`/skip, and the gate entry point exits non-zero
- [ ] Test that a generic tracker error propagates and is not converted into a skip

## Dependencies
- Depends on: Task 1 — Authenticate tracker calls with the service-account token via the gateway and make search_issues fail closed
