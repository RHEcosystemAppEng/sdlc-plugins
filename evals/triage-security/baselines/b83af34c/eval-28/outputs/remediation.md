# Step 8 -- Remediation: CVE-2026-99010 (h2)

## Triage Outcome

**Case B: Affected -- create remediation tasks** for the 2.2.x stream.

Versions 2.2.0, 2.2.1, and 2.2.2 are affected (ship h2 0.4.4, which is below the fix threshold 0.4.5).

Ecosystem: Cargo (source dependency) -- requires **2 tasks** per stream (upstream backport + downstream propagation).

---

## Task 1: Upstream Backport Task (2.2.x stream)

### Repository

backend

### Target Branch

release/0.4.z

### Description

Remediate CVE-2026-99010: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (retag v0.4.9)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

### Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)

#### Dependency chain

```
backend (workspace) -> reqwest -> hyper -> h2
Type: transitive (3 levels deep)
Profile: production (reqwest is a runtime dependency)
```

h2 is NOT a direct dependency of the backend workspace. It is pulled in transitively through the chain: reqwest -> hyper -> h2. The direct dependency that brings h2 into the tree is **reqwest**.

#### Remediation approach (transitive dependency)

Since h2 is a **transitive** dependency (pulled in through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- Identify that reqwest is the direct dependency that pulls in h2 (via reqwest -> hyper -> h2)
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest
- Check reqwest release notes for a version that ships with hyper containing h2 >= 0.4.5

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available with the fix):
- Cargo: `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the transitive resolution
- Document why the direct dep bump (reqwest) was not viable in the PR description

### Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

### Test Requirements

- [ ] Existing test suite passes with the updated dependency

### Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask (2.2.x stream)

### Repository

rhtpa-release.0.4.z

### Target Branch

main

### Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.5 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

### Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive -- carried forward from upstream task
- **Dependency chain**: backend -> reqwest -> hyper -> h2 (3 levels deep)
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach using `cargo add h2@0.4.5`), verify the pinning is reflected in the downstream build's lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

### Test Requirements

- [ ] Container image builds successfully with the updated reference

### Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)
