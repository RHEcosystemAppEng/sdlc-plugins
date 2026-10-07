# Step 8 -- Remediation

## Triage Outcome

**Case B: Affected -- create remediation tasks**

The scoped stream (2.2.x) has affected versions: 2.2.0, 2.2.1, 2.2.2
(all ship h2 0.4.4, which is within the vulnerable range < 0.4.5).

Cross-stream impact: 2.1.x is NOT affected (h2 0.4.5 in all versions).
Case A (cross-stream proactive remediation) does not apply -- no other streams are affected.

Ecosystem: **Cargo** (source dependency, fix available upstream per Step 2.5).
Task count: **2 tasks** -- dependency bump + downstream propagation.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)
```

h2 is a **transitive** dependency. It is NOT a direct dependency of any workspace
member. The full chain is: `reqwest -> hyper -> h2`. This requires a **two-tier
remediation approach** rather than a simple version bump.

---

## Task 1: Dependency Bump (upstream source fix)

**Summary**: Remediate CVE-2026-99010: update h2 to 0.4.5 (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-99010

### Repository

backend

### Target Branch

release/0.4.z

### Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 < 0.4.5) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1, 2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

### Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- **Remediation action**: use two-tier approach for transitive dependency

#### Two-tier remediation approach (transitive dependency)

h2 is a transitive dependency pulled in through the chain:
`reqwest -> hyper -> h2` (3 levels deep).

**Preferred: bump the direct dependency (reqwest)**

- Identify whether a newer version of reqwest (currently 0.12.5) pulls in
  hyper with h2 >= 0.4.5 in its transitive closure
- Run `cargo update -p reqwest` to pull in the latest compatible version
- Verify after update: `cargo tree -i h2` should show h2 >= 0.4.5
- If reqwest 0.12.x does not transitively pull h2 >= 0.4.5, check whether
  bumping hyper directly resolves it: `cargo update -p hyper`
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin h2 directly**

If bumping reqwest (or hyper) is not viable (breaking API changes, no
compatible release available with h2 >= 0.4.5):

- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding
  the transitive resolution
- This pins h2 to >= 0.4.5 regardless of what reqwest/hyper resolve
- Document why the direct dependency bump was not viable in the PR description

#### Verification

After either approach, confirm the fix:
```
cargo tree -i h2
# Should show h2 v0.4.5 (or higher)
# Full chain: backend -> reqwest -> hyper -> h2 v0.4.5
```

### Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

### Test Requirements

- [ ] Existing test suite passes with the updated dependency

### Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-99010

### Repository

rhtpa-release.0.4.z

### Target Branch

main

### Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the dependency bump task (Task 1).

The dependency bump task bumps h2 to 0.4.5 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

### Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
  that includes h2 >= 0.4.5
- If the upstream fix pinned h2 directly (fallback approach), verify the
  pinning is reflected in the downstream build's Cargo.lock after the
  source reference update
- Verify the Konflux build pipeline triggers successfully

### Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

### Test Requirements

- [ ] Container image builds successfully with the updated reference

### Dependencies

- Depends on: Task 1 (dependency bump must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

After task creation, the following links would be established:

1. **TC-8060 -> Task 1** (Depend): CVE depends on upstream dependency bump
2. **TC-8060 -> Task 2** (Depend): CVE depends on downstream propagation
3. **Task 1 -> Task 2** (Blocks): upstream bump must merge before downstream propagation
4. **Task 1 -> Release Task** (Blocks): remediation blocks release (if release Jira active)
5. **Task 2 -> Release Task** (Blocks): propagation blocks release (if release Jira active)
6. **Release Task -> TC-8060** (Related): traceability link from release to CVE

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for Cargo ecosystem (dependency bump + downstream propagation) -- matches classification table
- [x] **Cross-stream coverage**: 2.1.x is NOT affected -- no preemptive tasks needed
- [x] **Link types**: "Depend" for tasks linked to TC-8060, "Blocks" for upstream -> downstream
- [x] **Preemptive labels**: not applicable -- no streams without their own CVE Jira need coverage
- [x] **Coordination guidance**: Deployment Context column absent from Source Repositories table -- coordination guidance subsection omitted
- [x] **Dedup consistency**: no prior dedup detected -- new tasks to be created
