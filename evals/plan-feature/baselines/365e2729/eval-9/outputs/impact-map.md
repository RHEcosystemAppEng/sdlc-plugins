# Repository Impact Map — TC-9008: Gate release verification on a linked tracker issue

```
release-verifier:
  changes:
    - Authenticate tracker calls with the service-account token routed through the tracker API gateway (replace the personal token)
    - Add a positive authentication proof to the tracker client so an empty search result can be distinguished from an unauthenticated / under-privileged "200 + []" gateway response
    - Make search_issues fail closed (non-zero / typed error) when the gateway response cannot be proven authenticated, not only on HTTP 401/403
    - Resolve the tracker issue linked to the pull request and run verification only when it is in "Ready for Verification"; skip with a log message otherwise
    - Make resolve_gated_issue fail closed instead of returning None (skip) when the empty search result comes from a source that cannot be proven authenticated
    - Make scripts/pre-verify.sh propagate the gate's exit status and fail on any non-zero/unverified-auth outcome, rather than only grepping stderr for 401/403
    - Add tests for the authenticated-empty (skip), unauthenticated-empty (fail closed), Ready / not-Ready, and wrapper exit-code paths
```

## Known-risk coverage (fail-open / silent-empty)

| Documented risk | Gate site | Covered by | Fail-closed AC + test? |
|---|---|---|---|
| Gateway returns successful empty `[]` to unauthenticated / under-privileged requests; `search_issues` exits 0 | `src/tracker/client.py::search_issues` | Task 1 | Yes — AC + test in Task 1 |
| Gate treats "no matching issue" as a normal skip, so a run can finish green without verifying | `src/gate/resolve_issue.py::resolve_gated_issue` | Task 2 | Yes — AC + test in Task 2 |
| Shell wrapper reports auth failure only when the client exits non-zero (greps stderr for 401/403) | `scripts/pre-verify.sh` | Task 3 | Yes — AC + test in Task 3 |
| Suggested mitigation "a live run after merge confirms the token works" | — | Retained as a supplementary post-merge check in Task 3 | Not accepted as sole coverage — code-level fail-closed ACs and tests above are the primary coverage |

## Shared-artifact analysis

Not applicable — no acceptance criterion depends on a shared record, manifest, index, or cache. The single consumer of `search_issues` named in the feature is `resolve_gated_issue`; the single caller of the gate is `scripts/pre-verify.sh`. Implementers should grep for any other `search_issues` callers at implementation time (cross-cutting signature change in Task 1).

## Excluded requirements

None. All three MVP requirements map to tasks.

Open item (does not block planning): the feature does not name the gateway's identity/"whoami" endpoint or the exact service-account configuration key. Task 1 instructs the implementer to confirm both against the gateway documentation; if no identity endpoint exists, a configured canary query (a known issue that the service account must be able to see) is the specified fallback proof of authentication.

## Workflow mode

**Selected mode: `direct-to-main`**

Rationale — no atomicity indicators found:
1. Coordinated schema migrations: none.
2. Breaking API changes: the `search_issues` change adds a fail-closed error path; existing callers continue to work, and Task 2/3 consume it after Task 1 lands. Each task merges independently without breaking `main` (Task 1 alone makes unauthenticated runs fail louder, which is the desired direction).
3. Cross-cutting refactors: none.
4. Tightly coupled frontend/backend: none (single repository).

Tasks land sequentially on `main` via their declared dependencies (Task 2 depends on Task 1; Task 3 depends on Task 2).

## Planning notes

- Issue-type discovery (Step 2.5) could not be executed offline; planned as Feature → Task (no Epic layer). If an Epic-level type exists, the configured strategy `by-sub-feature` would yield a single Epic "TC-9008: Fail-closed tracker-gated verification".
- No "Documentation Considerations" section in the feature → no documentation task.
- No `docs/testing-readiness.md` or `CONVENTIONS.md` known for `release-verifier` → no testing tasks, no convention enrichment.
- Priority `Major` will be propagated to all tasks; fixVersions is empty on the Feature → omitted.
