# Repository Impact Map — TC-9008: Gate release verification on a linked tracker issue

## Analysis basis

- `release-verifier` is not listed in the CLAUDE.md Repository Registry and has no Serena instance. This plan uses the repository structure given in the Feature description (`feature-fail-open-risk.md`, section "Repository Structure: release-verifier"). Every file path below comes from that table. Paths for new test files follow the existing `tests/<package>/test_<module>.py` layout.
- No `CONVENTIONS.md`, `docs/testing-readiness.md`, or "Documentation Considerations" section was found or given. So the plan applies no convention enrichment, generates no testing tasks, and generates no documentation task.
- No Figma link was found, so Step 2 was skipped.

```
release-verifier:
  changes:
    - Build the tracker Authorization header from the new service-account token instead of the personal token (src/tracker/auth.py)
    - Send tracker calls through the tracker API gateway (src/tracker/client.py)
    - Make the tracker client fail closed: search_issues must raise / exit non-zero when it cannot prove the request was authenticated with sufficient privilege. An empty [] result from an unauthenticated or under-privileged gateway request must never be returned as a normal "no results" (src/tracker/client.py)
    - Gate resolution: find the linked issue for the PR, verify only when its state is "Ready for Verification", and otherwise skip with a log message (src/gate/resolve_issue.py)
    - Gate resolution fails closed: resolve_gated_issue returns None (skip) only for an empty result from a search that was proven authenticated. Any auth or unproven-auth condition propagates as an error (src/gate/resolve_issue.py)
    - The pre-verify wrapper fails the run on any non-zero client or gate exit, not only when stderr contains 401/403. It tells an explicit "skip" outcome apart from an error (scripts/pre-verify.sh)
    - Tests for the client, the gate, and the wrapper, covering the degraded/empty-auth path (tests/tracker/test_client.py, tests/gate/test_resolve_issue.py, new tests/scripts/test_pre_verify.py)
```

## Fail-open risk trace (from Feature "Known Risks")

| Stated risk | Gate / skip site that owns it | Fail-closed coverage |
|---|---|---|
| Gateway returns a successful empty search for an unauthenticated or under-privileged request, so `search_issues` exits 0 with `[]` | `src/tracker/client.py::search_issues` | Task 1: AC plus a test that the client raises / exits non-zero when authentication cannot be proven, even on HTTP 200 with `[]` |
| The gate treats "no matching issue" as a normal skip, so the run finishes green without verifying | `src/gate/resolve_issue.py::resolve_gated_issue` | Task 2: AC plus a test that an unproven-auth or auth-error condition is not turned into `None` (skip) |
| The shell wrapper reports auth failure only on a non-zero exit with 401/403 in stderr | `scripts/pre-verify.sh` | Task 3: AC plus a test that any non-zero gate exit fails the wrapper. Skip requires an explicit skip signal |
| Suggested mitigation: "a live run after merge confirms the token works" | — | Kept only as an extra post-merge check. It is **not** used as the coverage for any risk above |

## Excluded requirements

None. All three MVP requirements map to tasks below.

## Proposed tasks

1. Task 1: Authenticate tracker calls with the service-account token via the gateway and make `search_issues` fail closed
2. Task 2: Gate verification on a "Ready for Verification" linked issue, with fail-closed resolution
3. Task 3: Make `pre-verify.sh` fail on any non-zero gate exit instead of grepping for 401/403

## Workflow mode

**direct-to-main.** No atomicity indicator applies. There is no schema migration and no cross-cutting refactor. Task 1 changes the client's error behavior, and Task 2 consumes it through a direct dependency, so the tasks merge in order. Merging Task 1 alone fails closed (the new error propagates as a non-zero exit) and does not break `main`. Merging Task 3 after Task 2 only tightens the wrapper.
