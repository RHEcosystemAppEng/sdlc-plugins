# Repository Impact Map — TC-9008: Gate release verification on a linked tracker issue

## Planning context and non-interactive decisions

- **Feature source**: `feature-fail-open-risk.md` (mock of Jira TC-9008). No Figma URL in arguments or description, so Step 2 was skipped.
- **Priority**: Major (propagated to all tasks). **fixVersions**: none on the Feature, so fixVersions are omitted from tasks (scope setting `both` is irrelevant).
- **Parent link (Step 1.5)**: no parent set; prompt defaulted to *skip*.
- **Issue type discovery (Step 2.5)**: Jira was not contacted (offline eval). No level-1 type could be confirmed, so the plan uses the graceful-degradation Feature → Task hierarchy. No Epics are created, and the configured `by-sub-feature` strategy is recorded but not applied.
- **Repository analysis**: `release-verifier` is not in the CLAUDE.md Repository Registry and has no Serena instance. The analysis therefore uses the repository structure table in the Feature description. No `CONVENTIONS.md`, `docs/testing-readiness.md` or documentation files are known for this repository, so the plan has no convention enrichment, testing tasks or Documentation Updates sections.
- **Documentation signals**: the Feature has no "Documentation Considerations" section, so no documentation task is generated.
- **Impact map approval**: auto-approved (non-interactive run).

## Impact map

```
release-verifier:
  changes:
    - Build the tracker Authorization header from the new service-account token and route tracker calls through the tracker API gateway (src/tracker/auth.py, src/tracker/client.py)
    - Give the tracker client a way to prove a request was authenticated and authorized, so callers can tell an authenticated empty search apart from a gateway "successful empty" response to an unauthenticated or under-privileged request (src/tracker/client.py)
    - Make the gate verify only PRs whose linked issue is "Ready for Verification" and skip other PRs with a log message (src/gate/resolve_issue.py)
    - Make the gate fail closed: an empty search result counts as "no linked issue, skip" only when authentication is proven; otherwise the gate raises and exits non-zero (src/gate/resolve_issue.py)
    - Make the pre-verify wrapper fail closed on any non-zero gate or client exit, instead of only grepping stderr for 401/403 (scripts/pre-verify.sh)
    - Add tests for each of the above (tests/tracker/test_client.py, tests/gate/test_resolve_issue.py, plus a new wrapper test)
```

## Known-risk coverage (fail-open risks → fail-closed coverage)

| Stated risk | Owning gate site | Coverage |
|---|---|---|
| Gateway returns a successful empty `[]` to unauthenticated or under-privileged requests, and the gate treats that as a normal skip | `src/gate/resolve_issue.py::resolve_gated_issue`, backed by the auth proof in `src/tracker/client.py` | Task 1: AC, test and note for the client auth proof. Task 2: fail-closed AC, test and note at the skip site |
| Shell wrapper reports auth failure only when the client exits non-zero (empty `[]` never triggers it) | `scripts/pre-verify.sh` (stderr grep for 401/403) | Task 3: fail-closed AC, test and note |
| Suggested mitigation "a live run after merge confirms the token works" | — | Kept only as a supplementary operational check. It is **not** the coverage for either risk (constraint §1.107) |

## Excluded requirements

None. All three MVP requirements map to tasks:

- Search the tracker for the linked issue → Task 2 (reuses the existing `search_issues`)
- Verify only "Ready for Verification" issues, otherwise skip with a log → Task 2
- Service-account token via the gateway → Task 1

## Shared-artifact analysis

Not applicable. No acceptance criterion depends on a shared artifact (record, manifest, index or cache) that has more than one producer.

## Workflow mode decision (Step 4.5)

- **Selected mode**: `direct-to-main`
- **Rationale**: no atomicity indicators were found.
  - No schema migrations.
  - No breaking API contract between tasks. Task 1 adds the auth proof as a new client capability, and Task 2 consumes it afterwards. Merging Task 1 alone leaves `main` working.
  - No cross-cutting rename or refactor.
  - No frontend/backend pair that cannot work alone.
  - Tasks are ordered with Depends-on links (1 → 2 → 3), and each merge leaves `main` working.
- All tasks target `main`. No bookend tasks are generated.

## Task list

1. `task-1-service-account-gateway-auth.md`: Authenticate tracker calls with the service-account token through the API gateway, and expose an auth proof
2. `task-2-ready-for-verification-fail-closed-gate.md`: Gate verification on a "Ready for Verification" linked issue, and fail closed on an unproven-auth empty search
3. `task-3-pre-verify-fail-closed-wrapper.md`: Make `scripts/pre-verify.sh` fail closed on any non-zero gate exit
