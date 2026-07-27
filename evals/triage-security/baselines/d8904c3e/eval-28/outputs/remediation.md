# Step 8 -- Remediation

## Triage Decision

**Case B: Affected -- create remediation tasks**

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship h2 0.4.4, which is within the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4 already ship h2 0.4.5 (the fixed version). The 2.1.x stream is not affected (all versions ship h2 >= 0.4.5), so no cross-stream remediation (Case A) is needed.

**Ecosystem**: Cargo (source dependency) -- requires **two tasks** per stream:
1. Upstream backport task (fix in the source repo rhtpa-backend)
2. Downstream propagation subtask (update the reference in rhtpa-release.0.4.z)

## Dependency Chain

```
backend (workspace) -> reqwest -> hyper -> h2
Type: transitive (3 levels deep)
Profile: production (reqwest is a runtime dependency)
```

h2 is a **transitive** dependency, not directly declared in Cargo.toml. The two-tier remediation approach applies:
- **Preferred**: bump the direct dependency (reqwest) to a version whose transitive closure includes h2 >= 0.4.5
- **Fallback**: pin h2 directly via `cargo add h2@0.4.5` to override the transitive resolution

---

## Task 1: Upstream Backport (2.2.x stream)

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

h2 is a **transitive** dependency pulled in through the chain:
`backend (workspace) -> reqwest -> hyper -> h2`

Affected versions: 2.2.0 (backend tag v0.4.5), 2.2.1 (backend tag v0.4.8), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency (pulled in through reqwest -> hyper -> h2). Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: `reqwest` (version 0.12.5 in affected versions)
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest
- Note: versions 2.2.3+ already ship h2 0.4.5, confirming that a compatible reqwest version exists

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available with the fix):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the transitive resolution
- Document why the reqwest bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] Full dependency chain verified: reqwest -> hyper -> h2 all resolve to non-vulnerable versions
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation (2.2.x stream)

**Summary**: Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

**Blocked by**: Task 1 (upstream backport must merge first)

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.5 (via the transitive dependency chain: reqwest -> hyper -> h2) on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive -- carried forward from upstream task
- **Dependency chain**: backend -> reqwest -> hyper -> h2
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the h2 >= 0.4.5 fix
- [ ] Konflux rebuild triggers new container image
- [ ] Rebuilt container image contains h2 >= 0.4.5 in its dependency tree

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

1. Link upstream backport task to TC-8060 with link type **Depend**
2. Link downstream propagation task to TC-8060 with link type **Depend**
3. Link downstream propagation task as **blocked by** upstream backport task (link type: **Blocks**)
4. Transition TC-8060 to In Progress
5. Add `ai-cve-triaged` label to TC-8060

## Post-Triage Summary Comment

The following summary would be posted to TC-8060:

> **Triage summary for CVE-2026-99010 (h2 < 0.4.5)**
>
> **Version impact (2.2.x stream):**
>
> | Version | h2 Version | Affected? | Notes |
> |---------|-----------|-----------|-------|
> | 2.2.0   | 0.4.4     | YES       |       |
> | 2.2.1   | 0.4.4     | YES       |       |
> | 2.2.2   | --        | YES       | retag of 2.2.1 |
> | 2.2.3   | 0.4.5     | NO        | fixed version |
> | 2.2.4   | 0.4.5     | NO        | fixed version |
>
> **Dependency chain**: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep, production profile)
>
> **Cross-stream check**: 2.1.x stream is NOT affected (all versions ship h2 >= 0.4.5).
>
> **Affects Versions correction**: RHTPA 2.2.0 confirmed affected. Versions RHTPA 2.2.1 and RHTPA 2.2.2 should also be added to Affects Versions.
>
> **Remediation tasks created**:
> - Upstream backport task: bump h2 to >= 0.4.5 via reqwest on release/0.4.z
> - Downstream propagation task: update rhtpa-backend ref in rhtpa-release.0.4.z (blocked by upstream task)
>
> **Two-tier remediation approach** (transitive dependency):
> 1. Preferred: bump reqwest to pull in h2 >= 0.4.5 transitively
> 2. Fallback: pin h2 directly via `cargo add h2@0.4.5`
>
> @psirt-analyst -- triage complete.
