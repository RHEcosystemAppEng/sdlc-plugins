<!-- SYNTHETIC TEST DATA — fictional Jira feature and repository paths for fail-open risk planning evals. -->
# Mock Jira Feature Issue

**Key**: TC-9008
**Summary**: Gate release verification on a linked tracker issue
**Status**: New
**Priority**: Major
**Fix Versions**: None
**Labels**: ai-generated-jira
**Linked Issues**: None

---

## Feature Overview

The release verifier runs on every pull request. Before running the expensive verification suite, it should look up the tracker issue linked to the pull request and only verify pull requests whose linked issue is in the "Ready for Verification" state. Pull requests with no matching issue are skipped.

Tracker access moves to a new service-account token sent through the tracker API gateway.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Search the tracker for the issue linked to the pull request | Uses the existing search client | Yes |
| Run verification only when a linked issue is "Ready for Verification" | Otherwise skip with a log message | Yes |
| Authenticate tracker calls with the service-account token via the gateway | Replaces the personal token | Yes |

## Known Risks

- The tracker gateway returns a successful, empty search response to an unauthenticated or under-privileged request. `search_issues` then exits 0 with `[]`, and the gate treats "no matching issue" as a normal skip — so a verifier run can finish green without ever verifying the pull request.
- The shell wrapper only reports an authentication failure when the client exits non-zero, which an empty `[]` never triggers.
- Suggested mitigation: a live run after merge confirms the token works.

## Acceptance Criteria

- Pull requests linked to a "Ready for Verification" issue are verified.
- Pull requests with no linked issue are skipped.
- Tracker calls use the service-account token through the gateway.

## Repository Structure: release-verifier

| Path | Existing behavior |
|---|---|
| `src/tracker/client.py` | Tracker HTTP client; `search_issues(jql)` returns a list of issues and exits non-zero only on HTTP 401/403 |
| `src/tracker/auth.py` | Builds the tracker `Authorization` header from the configured token |
| `src/gate/resolve_issue.py` | `resolve_gated_issue(pr_url)` calls `search_issues` and returns `None` (skip) when the result is empty |
| `scripts/pre-verify.sh` | Runs the gate before verification; greps client stderr for 401/403 to report auth failures |
| `tests/tracker/test_client.py` | Tracker client tests |
| `tests/gate/test_resolve_issue.py` | Gate resolution tests |
