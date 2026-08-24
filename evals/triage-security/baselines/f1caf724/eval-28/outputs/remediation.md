# Step 8 -- Remediation: TC-8060 (CVE-2026-99010)

## Triage Outcome

**Case B: Affected -- create remediation tasks**

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship h2 0.4.4, which is within the affected range (< 0.4.5). Versions 2.2.3+ already ship the fix. The 2.1.x stream is not affected (Case A cross-stream impact does not apply).

Ecosystem: Cargo (source dependency) -- requires **2 tasks** per stream:
1. Upstream backport task (fix in source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks (source dependency -- upstream backport + downstream propagation)
- [x] **Cross-stream coverage**: 2.1.x is not affected, no preemptive tasks needed
- [x] **Link types**: "Depend" for tasks linked to TC-8060, "Blocks" for upstream -> downstream
- [x] **Preemptive labels**: N/A (no preemptive tasks)
- [x] **Coordination guidance**: upstream deployment context -- coordinate with upstream maintainers

---

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 -- Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

h2 is a **transitive** dependency pulled in through the following chain:

```
backend (workspace) -> reqwest -> hyper -> h2
```

h2 is NOT a direct dependency -- it enters the dependency tree through reqwest (version 0.12), which depends on hyper (version 1.4.1), which depends on h2.

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2
Source commit tags: v0.4.5 (2.2.0), v0.4.8 (2.2.1, 2.2.2)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through intermediate packages. Use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- Identify that reqwest (version 0.12) is the direct dependency that ultimately pulls in h2
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- The dependency chain is: reqwest -> hyper -> h2
- Verify the bump does not introduce breaking API changes to reqwest
- After bumping, run `cargo update` and verify h2 >= 0.4.5 in Cargo.lock

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available with the fix):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the transitive resolution
- This forces Cargo to resolve h2 to >= 0.4.5 regardless of what hyper requests
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 in Cargo.lock
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.5 on release/0.4.z by addressing the transitive dependency chain (reqwest -> hyper -> h2). Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly as a transitive dependency override (fallback approach), verify the pinning is reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

1. Link upstream backport task to TC-8060 with type "Depend"
2. Link downstream propagation task to TC-8060 with type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with type "Blocks"
4. Transition TC-8060 to In Progress
5. Assign TC-8060 to current user
6. Add `ai-cve-triaged` label to TC-8060

## Post-Triage Summary Comment (for TC-8060)

Version impact analysis for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | |
| 2.2.1 | 0.4.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.5 | NO | |
| 2.2.4 | 0.4.5 | NO | |

Dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep, production)

Affects Versions correction: RHTPA 2.2.0 (current) -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (proposed, scoped to 2.2.x stream)

Cross-stream impact: 2.1.x is NOT affected (h2 0.4.5 in all versions).

Remediation tasks created:
- Upstream backport task: bump h2 to 0.4.5 via reqwest update on release/0.4.z (two-tier: prefer reqwest bump, fallback to pinning h2 directly)
- Downstream propagation task: update rhtpa-backend ref in rhtpa-release.0.4.z (blocked by upstream task)

@psirt-analyst (reporter notification)
