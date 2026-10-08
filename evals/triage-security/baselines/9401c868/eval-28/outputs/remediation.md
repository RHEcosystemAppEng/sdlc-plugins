# Step 8 -- Remediation: CVE-2026-99010

## Triage Outcome

**Case B: Affected -- create remediation tasks**

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship h2 0.4.4 which is within
the affected range (< 0.4.5). The upstream branch `release/0.4.z` already ships h2 0.4.5
(confirmed in Step 2.5), so this uses the **dependency bump** variant rather than the
upstream backport variant.

**Ecosystem:** Cargo (source dependency) -- 2 tasks per stream:
1. Dependency bump task (upstream source repo)
2. Downstream propagation task (Konflux release repo)

## Dependency Chain

```
backend (workspace) -> reqwest -> hyper -> h2
Type: transitive (3 levels deep)
Profile: production (reqwest is a runtime dependency)
```

h2 is NOT a direct dependency of the backend workspace. It enters the dependency tree
through the chain: reqwest (direct) -> hyper -> h2. This requires a **two-tier
remediation approach**.

## Task 1: Dependency Bump Task

**Summary:** Remediate CVE-2026-99010: update h2 to 0.4.5 (2.2.x)

**Labels:** ai-generated-jira, Security, CVE-2026-99010

### Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 < 0.4.5) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)
- **Remediation action**: use the two-tier approach below

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
the chain: backend -> reqwest -> hyper -> h2 (3 levels deep).

**Preferred: bump the direct dependency (reqwest)**
- Identify the direct dependency that pulls in h2: `reqwest` (version 0.12)
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Run `cargo update -p reqwest` to pull in the latest compatible reqwest version
- Verify the lock file reflects h2 >= 0.4.5 after the update
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available
with the fix):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the
  transitive resolution
- This forces h2 >= 0.4.5 regardless of what reqwest/hyper resolve
- Document why the reqwest bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation Task

**Summary:** Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels:** ai-generated-jira, Security, CVE-2026-99010

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010
fix from the dependency bump task.

The dependency bump task bumps h2 to 0.4.5 on release/0.4.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly as a transitive dependency override
  (fallback approach), verify the pinning is reflected in the downstream build's
  Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix (h2 >= 0.4.5)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Task 1 -- dependency bump task (upstream fix must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

1. **Task 1 (dependency bump)** -> TC-8060: link type **Depend**
2. **Task 2 (downstream propagation)** -> TC-8060: link type **Depend**
3. **Task 1** -> **Task 2**: link type **Blocks** (downstream is blocked by upstream)
4. **Task 1** -> release Task: link type **Blocks** (if release Jira active from Step 7.5)
5. **Task 2** -> release Task: link type **Blocks** (if release Jira active from Step 7.5)
6. **TC-8060** -> release Task: link type **Related** (if release Jira active from Step 7.5)

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x stream (matches Cargo ecosystem classification: dependency bump + downstream propagation)
- [x] **Cross-stream coverage**: 2.1.x stream is NOT affected (h2 0.4.5 at fix threshold) -- no preemptive tasks needed
- [x] **Link types**: "Depend" for tasks linked to TC-8060, "Blocks" for upstream -> downstream within stream
- [x] **Preemptive labels**: not applicable (no cross-stream preemptive tasks needed)
- [x] **Coordination guidance**: included -- deployment context is "upstream" (default)
- [x] **Release Jira linking**: planned (pending Step 7.5 execution)
- [x] **Dedup consistency**: no dedup detected (pending Step 7.5.3)
- [x] **Dependency chain documented**: full chain (backend -> reqwest -> hyper -> h2) included in both tasks
- [x] **Two-tier remediation approach**: documented with preferred (bump reqwest) and fallback (pin h2 directly) strategies

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8060
2. Post summary comment to TC-8060 with:
   - Version impact table
   - Affects Versions correction (2.2.0, 2.2.1, 2.2.2 are affected; PSIRT only listed 2.2.0)
   - Remediation task keys and links
   - @mention of reporter psirt-analyst (account ID: 557058:psirt-analyst-mock-id)
3. Transition TC-8060 to In Progress

## Affects Versions Correction (Step 3)

PSIRT set Affects Versions to: RHTPA 2.2.0
Lock file evidence shows affected versions: 2.2.0, 2.2.1, 2.2.2

**Correction needed:** Add RHTPA 2.2.1 and RHTPA 2.2.2 to Affects Versions. Versions
2.2.3 and 2.2.4 ship h2 0.4.5 (fixed) and should NOT be in Affects Versions.
