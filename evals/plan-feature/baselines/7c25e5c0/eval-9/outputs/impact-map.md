# Repository Impact Map — TC-9008

## release-verifier

### Changes

- Migrate tracker authentication from personal token to service-account token via the API gateway (`src/tracker/auth.py`)
- Add fail-closed guard in `resolve_gated_issue` so that an empty search result from an unverified/unauthenticated source raises an error instead of returning `None` (skip) (`src/gate/resolve_issue.py`)
- Update `scripts/pre-verify.sh` to propagate the non-zero exit from the fail-closed gate and report the failure reason
- Update `src/tracker/client.py` to expose an authentication-health signal (e.g., a lightweight authenticated probe) so the gate can distinguish "genuinely no matching issue" from "search returned empty because the token is invalid or the gateway is degraded"
- Add and update tests for the fail-closed gate, the new auth probe, and the shell wrapper behavior under degraded/unauthenticated conditions

### Fail-open risk analysis

**Documented risk (from Known Risks):**
The tracker gateway returns a successful, empty search response (`[]`) to an unauthenticated or under-privileged request. `search_issues` exits 0, and `resolve_gated_issue` treats "no matching issue" as a normal skip. The shell wrapper `pre-verify.sh` only reports auth failures when the client exits non-zero — which an empty `[]` never triggers. Result: the verifier run finishes green without ever verifying the pull request.

**Risk classification:** Silent-empty / fail-open. The gate silently succeeds (skip) when it should fail (cannot prove the search was authenticated).

**Required coverage:**
- A code-level, testable fail-closed Acceptance Criterion on the gate-owning task
- A Test Requirement that drives the unauthenticated/degraded/empty-search path and asserts the fail-closed outcome
- Implementation Notes pointing at the specific gate site: `src/gate/resolve_issue.py` (`resolve_gated_issue`) and `scripts/pre-verify.sh`

**Suggested mitigation disposition:**
The feature description suggests "a live run after merge confirms the token works" as mitigation. This is insufficient as sole coverage — it is an operational check, not a code-level guard. The plan includes a fail-closed Acceptance Criterion and test as primary coverage; a live post-merge run may supplement but does not replace them.

### Excluded requirements

None — all requirements can be planned with the available repository structure.

### Workflow mode decision

**Selected mode:** `direct-to-main`
**Rationale:** No atomicity indicators detected. The authentication migration, fail-closed gate, and shell wrapper updates can each be merged independently without leaving main in a broken state. The existing gate behavior (skip on empty) is preserved until the fail-closed guard lands, and each task is backward-compatible.

### Inherited field propagation

- **Priority:** Major (inherited from Feature TC-9008; will be propagated to all created tasks)
- **fixVersions:** None on the Feature — fixVersion inheritance is skipped
