# Repository Impact Map — TC-9008: Gate release verification on a linked tracker issue

```
release-verifier:
  changes:
    - Build the tracker Authorization header from a new service-account token instead of the personal token (src/tracker/auth.py)
    - Route tracker HTTP calls through the tracker API gateway (src/tracker/client.py)
    - Make tracker search fail closed when the request cannot be proven authenticated/authorized — an empty `[]` from the gateway must not be indistinguishable from "no matching issue" (src/tracker/client.py::search_issues)
    - Resolve the issue linked to a pull request and return it only when its state is "Ready for Verification"; skip with a log message otherwise (src/gate/resolve_issue.py::resolve_gated_issue)
    - Make the gate distinguish a proven-authenticated empty result (legitimate skip) from an unproven/degraded result (hard failure) (src/gate/resolve_issue.py::resolve_gated_issue)
    - Make the pre-verify shell wrapper fail on any non-zero gate exit and on an unproven-auth signal, instead of only grepping stderr for 401/403 (scripts/pre-verify.sh)
    - Add tests covering the fail-closed degraded/empty paths in the client, gate, and wrapper (tests/tracker/test_client.py, tests/gate/test_resolve_issue.py, new wrapper test)
```

## Known-risk coverage (fail-open)

| Risk (from Feature "Known Risks") | Gate site | Covered by | Coverage type |
|---|---|---|---|
| Gateway returns successful empty search to unauthenticated/under-privileged request; `search_issues` exits 0 with `[]` | `src/tracker/client.py::search_issues` | Task 2 | Fail-closed AC + test + implementation note |
| Gate treats "no matching issue" as a normal skip, so a run finishes green without verifying | `src/gate/resolve_issue.py::resolve_gated_issue` | Task 3 | Fail-closed AC + test + implementation note |
| Shell wrapper only reports auth failure on non-zero exit / 401-403 stderr grep, which `[]` never triggers | `scripts/pre-verify.sh` | Task 3 | Fail-closed AC + test + implementation note |

The Feature's suggested mitigation ("a live run after merge confirms the token works") is retained only as a **supplementary** operational check. It is NOT accepted as the coverage for these risks — each risk is lowered into a code-level fail-closed acceptance criterion and a test that drives the degraded/empty path.

## Excluded requirements

None. All three MVP requirements and all three acceptance criteria are planned.

## Assumptions (where the skill would prompt or query external systems)

- `release-verifier` is not listed in the Repository Registry of CLAUDE.md and has no Serena instance; repository analysis is based on the repository structure supplied in the Feature description (file paths and existing behavior). Paths listed are taken verbatim from that structure; the one new file is a new test.
- No CONVENTIONS.md, `docs/testing-readiness.md`, or documentation files are known for `release-verifier` → no convention enrichment, no testing tasks.
- Feature has no "Documentation Considerations" section → no documentation task.
- Impact map treated as approved by the user (non-interactive eval).

## Workflow mode decision

**Mode: `direct-to-main`**

Rationale — atomicity indicators evaluated:
1. Coordinated schema migrations — none (no database/data model changes).
2. Breaking API changes — none. Task 2 adds a new, additive failure signal (`TrackerAuthUnprovenError` / distinct exit code) to `search_issues`; existing callers keep working (they get a hard failure instead of a silent `[]`, which is the intended safer behavior).
3. Cross-cutting refactors — none.
4. Tightly coupled components — none. Each task leaves `main` working when merged in order (Task 1 → Task 2 → Task 3); dependencies are sequential, not all-or-nothing.

No atomicity indicators found → `direct-to-main`. All tasks target `main`; no bookend tasks.
