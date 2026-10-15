# Step 8 -- Remediation

## Triage Outcome

- **Stream scope:** 2.2.x
- **Affected versions:** 2.2.0, 2.2.1, 2.2.2
- **Not affected:** 2.2.3, 2.2.4 (already ship h2 0.4.5)
- **Cross-stream impact:** None (2.1.x is not affected)
- **Case:** Case B -- affected versions exist, create remediation tasks
- **Ecosystem:** Cargo (source dependency)
- **Upstream fix available:** Yes (release/0.4.z already ships h2 0.4.5)
- **Remediation variant:** Dependency bump + downstream propagation (2 tasks)
- **Dependency type:** Transitive (3 levels deep)
- **Dependency chain:** `backend (workspace) -> reqwest -> hyper -> h2`

## Dependency Chain Summary

h2 is a **transitive** dependency, not directly declared in `backend/Cargo.toml`. The chain is:

```
backend (workspace)
  -> reqwest 0.12 (direct dependency, production profile)
    -> hyper 1.4.1
      -> h2 0.4.4 (VULNERABLE, 3 levels deep)
```

Because h2 is transitive, remediation uses a **two-tier approach**:

1. **Preferred: bump the direct dependency (reqwest)** to a version whose transitive closure includes h2 >= 0.4.5. Verify the bump does not introduce breaking API changes to reqwest.
2. **Fallback: pin h2 directly** via `cargo add h2@0.4.5` to override the transitive resolution, if bumping reqwest is not viable (breaking API changes, no compatible release available). Document why the direct dep bump was not viable in the PR description.

---

## Task 1: Dependency Bump Task (upstream)

**Proposed Jira action -- not executed.**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99010: update h2 to 0.4.5 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 < 0.4.5) is already fixed upstream --
a package manager update is sufficient.

The h2 crate before version 0.4.5 allows a remote attacker to cause
memory exhaustion by sending a large number of CONTINUATION frames
(denial of service).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.8 also covers 2.2.2 retag)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- **Dependency chain**: h2 is NOT a direct dependency of backend. It is pulled
  in transitively through reqwest (0.12) -> hyper (1.4.1) -> h2 (0.4.4).

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
intermediate packages. Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: **reqwest** (version 0.12)
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Run `cargo update -p h2` to pull in the latest compatible version of h2
- Verify the bump does not introduce breaking API changes to reqwest
- Check `Cargo.lock` after update to confirm h2 >= 0.4.5

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available
with the fix):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the
  transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

- **Remediation action**: run `cargo update -p h2` to pull in the latest
  compatible version. If the update pulls a version that still falls within
  the affected range, pin explicitly: `cargo add h2@0.4.5`
- Verify the lock file reflects h2 >= 0.4.5 after the update

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 (verified in Cargo.lock)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

### Proposed Jira linkage (Task 1)

- **Depend link:** TC-8060 (inward) -> Task 1 key (outward), type "Depend"

---

## Task 2: Downstream Propagation Task

**Proposed Jira action -- not executed.**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99010 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from the dependency bump task.

The dependency bump task updates h2 to 0.4.5 on release/0.4.z
(via reqwest/hyper transitive dependency chain). Once that PR merges,
update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: transitive -- carried forward from upstream task
- **Dependency chain**: backend -> reqwest -> hyper -> h2
- Update the backend reference to the merged commit or new release tag
  that includes h2 >= 0.4.5
- If the upstream fix pinned h2 directly (fallback approach), verify
  the pinning is reflected in the downstream build's Cargo.lock after
  the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix (h2 >= 0.4.5)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream dependency bump task key] (dependency bump must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

### Proposed Jira linkage (Task 2)

- **Depend link:** TC-8060 (inward) -> Task 2 key (outward), type "Depend"
- **Blocks link:** Task 1 key (inward) -> Task 2 key (outward), type "Blocks"
  (downstream propagation is blocked by the upstream dependency bump)

---

## Post-Creation Linkage Summary

All links are **proposed actions** -- not executed.

| Link Type | Inward Issue | Outward Issue | Purpose |
|-----------|-------------|---------------|---------|
| Depend | TC-8060 (CVE) | Task 1 (dep bump) | Remediation depends on CVE |
| Depend | TC-8060 (CVE) | Task 2 (propagation) | Remediation depends on CVE |
| Blocks | Task 1 (dep bump) | Task 2 (propagation) | Downstream blocked by upstream |

## Post-Triage Summary (proposed comment on TC-8060)

**Proposed Jira action -- not executed.**

The following summary comment would be posted to TC-8060:

```
CVE-2026-99010 triage complete for stream 2.2.x.

Version impact (h2 < 0.4.5):

| Version | h2 | Affected? | Notes |
|---------|-----|-----------|-------|
| 2.2.0 | 0.4.4 | YES | |
| 2.2.1 | 0.4.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.5 | NO | |
| 2.2.4 | 0.4.5 | NO | |

Dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep)
Upstream fix status: FIXED on release/0.4.z (shipped in 2.2.3+)

Affects Versions corrected: [RHTPA 2.2.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Remediation tasks created:
- [Task 1 key] (dependency bump: update h2 to 0.4.5 via reqwest/cargo update)
- [Task 2 key] (downstream propagation: update backend ref in rhtpa-release.0.4.z,
  blocked by [Task 1 key])

Cross-stream impact: 2.1.x is NOT affected (ships h2 0.4.5).

@psirt-analyst (reporter notification)
```

## Proposed Affects Versions Correction

**Proposed Jira action -- not executed.**

- Current: `[RHTPA 2.2.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- Rationale: Lock file analysis at pinned commits confirms h2 0.4.4 (vulnerable)
  in versions 2.2.0, 2.2.1, and 2.2.2. Version 2.2.2 is a retag of 2.2.1
  (same backend tag v0.4.8) and inherits the same vulnerable h2 version.
  Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

## Proposed Label Addition

**Proposed Jira action -- not executed.**

- Add label `ai-cve-triaged` to TC-8060 to mark the issue as triaged.
