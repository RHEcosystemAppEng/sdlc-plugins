# Repository Impact Map — TC-9008: Gate release verification on a linked tracker issue

```
release-verifier:
  changes:
    - Authenticate tracker calls with the service-account token routed through the tracker API gateway (replaces the personal token) — src/tracker/auth.py, src/tracker/client.py
    - Give the tracker client a positive authentication proof so an empty search result can be distinguished from an unauthenticated / under-privileged "successful empty" gateway response — src/tracker/client.py
    - Gate verification on the linked issue's state: verify only when the linked issue is "Ready for Verification", skip with a log message otherwise — src/gate/resolve_issue.py
    - Make the gate fail closed: an empty search result is only a "no linked issue" skip when the tracker session is proven authenticated; otherwise the gate errors (non-zero) instead of skipping — src/gate/resolve_issue.py
    - Make the pre-verify wrapper report auth failures from the client/gate exit status (not only from 401/403 text in stderr) and never treat an unproven-auth empty result as a green skip — scripts/pre-verify.sh
    - Add tests for the token/gateway auth, the authentication proof, the state gate and the fail-closed paths — tests/tracker/test_client.py, tests/gate/test_resolve_issue.py
```

## Known risk coverage (fail-open)

| Risk stated in the Feature | Code-level coverage | Owning task |
|---|---|---|
| Gateway returns a successful, empty search response to an unauthenticated / under-privileged request; `search_issues` exits 0 with `[]` and the gate treats it as a normal skip | `resolve_gated_issue` raises / exits non-zero when the result is empty and authentication has not been positively proven; fail-closed AC + test driving the unauthenticated-empty path | Task 2 (gate), with the auth-proof primitive from Task 1 |
| Client only exits non-zero on HTTP 401/403, so an empty `[]` never signals an auth problem | Client exposes an authentication proof (authenticated-identity check through the gateway) and a distinct error for "authentication not proven"; tested with a mocked 200 + `[]` unauthenticated response | Task 1 (client) |
| Shell wrapper only reports auth failure when the client exits non-zero / stderr contains 401/403 | `pre-verify.sh` propagates the gate's non-zero exit status and reports an auth failure for the dedicated "auth not proven" exit code; test drives the wrapper with a stubbed gate returning that code | Task 3 (wrapper) |

The Feature's suggested mitigation ("a live run after merge confirms the token works") is retained only as a supplementary operational check. It is NOT the coverage for these risks — each risk above has a fail-closed acceptance criterion and test in its owning task.

## Excluded requirements

None. All three MVP requirements are planned.

## Notes / assumptions

- release-verifier is not listed in the CLAUDE.md Repository Registry and has no Serena instance; repository structure is taken from the Feature description's "Repository Structure" table. File paths are limited to the paths documented there; the implementer must confirm exact symbol names (e.g. where the token is read from configuration) at implementation time.
- The concrete gateway endpoint for the authentication proof (e.g. an authenticated "current identity" endpoint) is not documented in the Feature; Task 1 asks the implementer to confirm it against the gateway API.
- No "Documentation Considerations" section in the Feature — no documentation task generated.
- No `docs/testing-readiness.md` discovered for release-verifier — no testing tasks generated.
- No CONVENTIONS.md discovered for release-verifier — no convention enrichment applied.

## Workflow Mode Decision

**Mode: `direct-to-main`**

Rationale — atomicity indicators evaluated:
1. Coordinated schema migrations — none (no data model / schema).
2. Breaking API changes — none. Task 1 adds an authentication-proof capability to the tracker client and switches the token source; the existing `search_issues(jql)` contract is preserved, so `resolve_gated_issue` keeps working when Task 1 merges alone. Task 2 consumes the new capability and is ordered after Task 1 via a dependency, not a co-merge requirement.
3. Cross-cutting refactors — none.
4. Tightly coupled components — none; Task 3 (wrapper) only reacts to an exit code that Task 2 introduces and is safe to merge after Task 2.

No atomicity indicator found; tasks are delivered incrementally to `main` in dependency order (Task 1 → Task 2 → Task 3).

## Epic grouping

Strategy: `by-sub-feature` (from CLAUDE.md Hierarchy Configuration). Suggested groupings (presented for approval):

- Epic A — "TC-9008: Tracker service-account authentication" → Task 1
- Epic B — "TC-9008: Fail-closed verification gate" → Task 2, Task 3
