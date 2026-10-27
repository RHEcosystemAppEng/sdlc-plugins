# Step 8 -- Remediation

## Triage Outcome

**Case B: Affected -- create remediation tasks**

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship h2 0.4.4, which is within the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4 already ship h2 0.4.5 (the fixed version).

Since the upstream branch `release/0.4.z` already ships the fix (confirmed by versions 2.2.3+ having h2 0.4.5), the remediation uses the **dependency bump** variant (not upstream backport).

Since h2 is a **Cargo source dependency**, two tasks are created for the 2.2.x stream:
1. Dependency bump task (upstream source repo)
2. Downstream propagation task (Konflux release repo)

---

## Task 1: Dependency Bump Task

**Summary**: Remediate CVE-2026-99010: update h2 to 0.4.5 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 versions before 0.4.5) is already fixed upstream --
a package manager update is sufficient.

h2 before version 0.4.5 allows a remote attacker to cause memory exhaustion by
sending a large number of CONTINUATION frames (DoS). CVSS: 7.5 (High).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1), v0.4.8 (2.2.2, retag of 2.2.1)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- **Remediation action**: This is a transitive dependency. h2 is not declared
  directly in backend/Cargo.toml -- it enters the dependency tree through
  reqwest -> hyper -> h2 (3 levels deep).

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
intermediate packages. Use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- reqwest is the direct dependency that ultimately pulls in h2 via
  reqwest -> hyper -> h2
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Check reqwest's changelog/release notes for a version that depends on
  hyper with h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest
- Run `cargo update -p reqwest` to pull in the latest compatible version,
  then verify h2 >= 0.4.5 in the resolved Cargo.lock

**Fallback: pin h2 directly**
If bumping reqwest is not viable (breaking API changes, no release available
with the fix):
- Cargo: `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding
  the transitive resolution
- This forces Cargo to resolve h2 to at least 0.4.5 regardless of what
  reqwest/hyper request
- Document why the reqwest bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation Task

**Summary**: Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the dependency bump task.

The dependency bump task bumps h2 to 0.4.5 on release/0.4.z (via reqwest
update or direct h2 pin). Once that PR merges, update the source pinning
in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2) -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach via `cargo add h2@0.4.5`),
  verify the pinning is reflected in the downstream build's Cargo.lock after the
  source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

1. Link dependency bump task to TC-8060 with type "Depend"
2. Link downstream propagation task to TC-8060 with type "Depend"
3. Link downstream propagation task as blocked by dependency bump task with type "Blocks"
4. Transition TC-8060 to In Progress
5. Add `ai-cve-triaged` label to TC-8060

## Cross-Stream Impact

The issue is scoped to stream 2.2.x. The 2.1.x stream shows h2 at version 0.4.5
for all versions (v0.3.8 and v0.3.12), which is at or above the fix threshold.
The 2.1.x stream is **not affected** -- no cross-stream remediation required.

## Key Transitive Dependency Context

- **h2 is transitive, not direct**: It is not declared in backend/Cargo.toml.
  The full chain is: backend -> reqwest -> hyper -> h2 (3 levels deep).
- **Two-tier remediation approach**:
  - **Preferred**: Bump reqwest (the direct dependency) to a version whose
    dependency tree includes h2 >= 0.4.5
  - **Fallback**: Pin h2 directly via `cargo add h2@0.4.5` if the reqwest
    bump is not viable (e.g., breaking API changes, no compatible release)
- **Cargo ecosystem**: The fallback uses `cargo add h2@0.4.5` which adds h2
  as an explicit dependency in Cargo.toml, overriding the transitive resolution
