# Step 8 -- Remediation for TC-8060

## Triage Outcome

**Case B: Affected -- create remediation tasks**

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream ship h2 0.4.4, which is within the affected range (< 0.4.5). The 2.1.x stream is not affected (ships h2 0.4.5), so Case A (cross-stream impact) does not apply.

Since the upstream branch `release/0.4.z` already ships h2 >= 0.4.5 (confirmed by 2.2.3+ versions), the **dependency bump** variant applies. This produces two tasks for the 2.2.x stream:

1. **Task 1**: Dependency bump -- update h2 via reqwest in the backend source repo
2. **Task 2**: Downstream propagation -- update backend ref in the Konflux release repo

## Task 1: Dependency Bump (upstream source repository)

**Jira summary**: `Remediate CVE-2026-99010: update h2 to 0.4.5 (2.2.x)`
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`
**Link**: Depend -- TC-8060 (parent Vulnerability issue)

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 < 0.4.5) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest 0.12.5 -> hyper 1.4.1 -> h2 0.4.4)

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
intermediate packages (3 levels deep). Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: `reqwest`
- Full dependency chain: backend (workspace) -> reqwest -> hyper -> h2
- Bump `reqwest` to a version whose transitive closure
  includes h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to
  reqwest (check reqwest changelog for the target version)
- After bumping, verify with: `cargo tree -p h2` to confirm
  h2 >= 0.4.5 in the resolved dependency tree

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes,
no release available with the fix):
- Run: `cargo add h2@0.4.5` to add h2 as a direct dependency,
  overriding the transitive resolution
- This forces Cargo to resolve h2 to >= 0.4.5 regardless of
  what reqwest/hyper request
- Document why the reqwest bump was not viable in the PR description

- **Remediation action**: run the appropriate package manager update command:
  - `cargo update -p h2` to pull in the latest compatible version
  - If the update pulls a version that still falls within the affected range,
    pin explicitly: `cargo add h2@0.4.5`
  - Verify the lock file reflects h2 >= 0.4.5 after the update

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

## Task 2: Downstream Propagation (Konflux release repository)

**Jira summary**: `Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)`
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`
**Link**: Depend -- TC-8060 (parent Vulnerability issue)
**Blocked by**: Task 1 (dependency bump must merge first)

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the upstream dependency bump task.

The upstream dependency bump task bumps h2 to 0.4.5
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive -- carried forward from upstream task
- Full dependency chain: backend -> reqwest -> hyper -> h2
- Update the backend reference to the merged commit or new release tag
  that includes h2 >= 0.4.5
- If the upstream fix pinned h2 directly (fallback approach), verify the
  pinning is reflected in the downstream build's Cargo.lock after the
  source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the h2 >= 0.4.5 fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Task 1 (upstream dependency bump must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

## Jira Linkage Plan

After creating the remediation tasks:

1. **Link Task 1 (dependency bump) to TC-8060**: type `Depend` (inward: TC-8060, outward: Task 1)
2. **Link Task 2 (downstream propagation) to TC-8060**: type `Depend` (inward: TC-8060, outward: Task 2)
3. **Link Task 2 blocked by Task 1**: type `Blocks` (inward: Task 1, outward: Task 2)
4. **Release Jira linking** (if Step 7.5 produced a release Task): link both remediation tasks to the release Task (Blocks), link TC-8060 to the release Task (Related)
5. **Transition** TC-8060 to In Progress
6. **Add `ai-cve-triaged` label** to TC-8060
7. **Post summary comment** to TC-8060 with version impact table, remediation task links, and @mention of reporter (557058:psirt-analyst-mock-id)

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x (source dependency ecosystem: dependency bump + downstream propagation)
- [x] **Cross-stream coverage**: 2.1.x stream is NOT affected -- no preemptive tasks needed
- [x] **Link types**: "Depend" for tasks linked to TC-8060; "Blocks" for upstream -> downstream within stream
- [x] **Preemptive labels**: not applicable (no streams without CVE Jira need preemptive tasks)
- [x] **Coordination guidance**: omitted (Source Repositories table has no Deployment Context column)
- [x] **Dedup consistency**: no dedup applies (no prior remediation tasks exist for this component)

## Transitive Dependency Summary

| Aspect | Detail |
|--------|--------|
| Vulnerable library | h2 |
| Dependency type | Transitive (3 levels deep) |
| Full chain | backend -> reqwest 0.12.5 -> hyper 1.4.1 -> h2 0.4.4 |
| Direct dependency to bump | reqwest |
| Fallback approach | `cargo add h2@0.4.5` (pin transitive dep directly) |
| Profile | Production (reqwest is a runtime dependency) |
| Affected versions | 2.2.0, 2.2.1, 2.2.2 |
| Fixed in | 2.2.3+ (h2 0.4.5) |
| Upstream branch status | Fixed (release/0.4.z ships h2 >= 0.4.5) |
