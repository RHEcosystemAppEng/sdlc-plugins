# Step 8 -- Remediation

## Triage Outcome

- **Case determination**: Case B -- Affected versions exist within the scoped stream (2.2.x)
- **Cross-stream impact (Case A)**: Not applicable -- the 2.1.x stream ships h2 0.4.5 (not affected)
- **Ecosystem**: Cargo (source dependency) -- 2 tasks required per stream
- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Fixed versions**: 2.2.3, 2.2.4 (already ship h2 0.4.5)
- **Upstream fix status**: Already fixed on release/0.4.z branch

## Dependency Chain

h2 is a **transitive** dependency (3 levels deep):

```
backend (workspace) -> reqwest -> hyper -> h2
```

- h2 is NOT a direct dependency of the backend workspace
- reqwest is the direct dependency that transitively pulls in h2 via hyper
- Profile: production (reqwest is a runtime dependency)
- Present in all versions since initial project setup

## Remediation Approach (Two-Tier for Transitive Dependencies)

Since h2 is transitive, the remediation uses a two-tier approach:

1. **Preferred -- bump the direct dependency**: Update `reqwest` (the direct dependency) to a version whose dependency tree includes h2 >= 0.4.5. This is the cleanest approach because it keeps the dependency resolution natural.

2. **Fallback -- pin the transitive dependency directly**: If no compatible reqwest version pulls in h2 >= 0.4.5 (due to breaking API changes or no available release), add h2 as a direct dependency to override transitive resolution:
   - Cargo: `cargo add h2@0.4.5`
   - Document why the direct dep bump was not viable in the PR description

---

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 via reqwest update (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames.
The vulnerable transitive dependency (h2 < 0.4.5) must be updated
to the fixed version (0.4.5+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- The upstream fix is already present on release/0.4.z -- versions 2.2.3+
  (built from tags v0.4.11 and v0.4.12) ship h2 0.4.5. This task confirms
  the fix is in place and no further action is needed on the upstream branch.

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
the chain: reqwest -> hyper -> h2. Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: `reqwest`
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest
- The dependency chain is: reqwest (0.12.5) -> hyper (1.4.1) -> h2 (0.4.4)
- A newer reqwest or hyper version that resolves h2 >= 0.4.5 is needed

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release
available with the fix):
- Cargo: `cargo add h2@0.4.5` to add as a direct dependency,
  overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 (verified in Cargo.lock)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

**Linkage**: Depend link from TC-8060 to this task

---

## Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.5 (via reqwest/hyper update or
direct h2 pin) on release/0.4.z. Once that PR merges, update the source
pinning in this Konflux release repo so the next build ships the fix.

Note: Versions 2.2.3+ (tags v0.4.11, v0.4.12) already ship h2 0.4.5.
This task ensures any future builds for the 2.2.x stream continue to
include the fix and that the Konflux release repo source pinning reflects
the remediated state.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
  -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release
  tag that includes the h2 fix
- Since h2 is a transitive dependency fixed via reqwest/hyper update (or
  direct h2 pin as fallback), verify the pinning is reflected in the
  downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the h2 >= 0.4.5 fix
- [ ] Cargo.lock in the built image contains h2 >= 0.4.5
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-task-key] (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

**Linkage**:
- Depend link from TC-8060 to this task
- Blocks link from the upstream task to this task (downstream is blocked by upstream)

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for the 2.2.x stream (Cargo = source dependency ecosystem -- upstream backport + downstream propagation). Matches the ecosystem classification table.
- [x] **Cross-stream coverage**: The 2.1.x stream is NOT affected (ships h2 0.4.5). No preemptive tasks needed. No sibling CVE Jiras required for other streams.
- [x] **Link types**: "Depend" for both tasks linked to TC-8060 (their CVE Jira). "Blocks" for upstream -> downstream within the 2.2.x stream.
- [x] **Preemptive labels**: Not applicable -- no streams without their own CVE Jira are affected.
- [x] **Coordination guidance**: Each task's Implementation Notes includes guidance for the `upstream` deployment context.
- [x] **Dependency chain documented**: Both tasks include the full transitive dependency chain (backend -> reqwest -> hyper -> h2) and the two-tier remediation approach.
- [x] **Two-tier remediation approach**: Both tasks document the preferred approach (bump reqwest) and the fallback approach (pin h2 directly).

## Post-Triage Summary

After engineer confirmation, the following actions would be taken:

1. **Affects Versions correction**: Current `[RHTPA 2.2.0]` -> Proposed `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (scoped to 2.2.x stream per issue suffix)
2. **Create upstream backport task** with Depend link to TC-8060
3. **Create downstream propagation subtask** with Depend link to TC-8060 and Blocks link from the upstream task
4. **Add `ai-cve-triaged` label** to TC-8060
5. **Post summary comment** to TC-8060 with version impact table, Affects Versions correction, task links, and @mention of reporter (557058:psirt-analyst-mock-id)
6. **Transition** TC-8060 to In Progress
