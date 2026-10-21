# Step 8 -- Remediation: TC-8001

## Triage Decision

- **Any supported versions affected?** YES
- **Issue scoped?** YES (scoped to 2.2.x stream)
- **Other streams also affected?** YES (2.1.x is also affected)
- **Decision path**: Case A (cross-stream impact) + Case B (create remediation tasks)

## Case A: Cross-Stream Impact

The issue is scoped to **2.2.x**, but version impact analysis shows that **2.1.x** is also affected (all versions ship quinn-proto 0.11.9 < 0.11.14). Since no stream-specific CVE Jira exists for 2.1.x, preemptive remediation tasks are created for that stream.

### Cross-stream impact comment (posted to TC-8001):

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based
on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto
0.11.9 which is within the affected range.

These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

---

## Case B: Remediation Tasks for 2.2.x Stream (Scoped)

### Ecosystem and Remediation Path

- Ecosystem: **Cargo** (source dependency)
- Upstream fix status: **Fixed** on release/0.4.z (quinn-proto 0.11.14 at branch HEAD)
- Remediation variant: **Dependency bump** (fix is already available upstream)
- Tasks per stream: **2** (dependency bump + downstream propagation)

### Task 1: Dependency Bump Task (2.2.x)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
**Link**: Depend (inward: TC-8001, outward: this task)

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation Task (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
**Link**: Depend (inward: TC-8001, outward: this task)
**Blocked by**: Task 1 (dependency bump must merge first)

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Link Topology (2.2.x)

1. Dependency bump task -- Depend --> TC-8001
2. Downstream propagation task -- Depend --> TC-8001
3. Downstream propagation task -- Blocks (blocked by) --> dependency bump task

---

## Case A: Preemptive Remediation Tasks for 2.1.x Stream

Since no CVE Jira exists for the 2.1.x stream, preemptive remediation tasks are created with the `security-preemptive` label and linked to TC-8001 via "Related" (not "Depend").

### Upstream Fix Status for 2.1.x

- Upstream branch: release/0.3.z
- quinn-proto at HEAD: 0.11.9
- Fix available upstream? **NO**
- Remediation variant: **Upstream backport** (fix must be applied to release/0.3.z first)

### Task 3: Upstream Backport Task (2.1.x, Preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related (inward: TC-8001, outward: this task)

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue -- cross-stream)
```

### Task 4: Downstream Propagation Task (2.1.x, Preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related (inward: TC-8001, outward: this task)
**Blocked by**: Task 3 (upstream backport must merge first)

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue -- cross-stream)
```

### Link Topology (2.1.x Preemptive)

1. Upstream backport task -- Related --> TC-8001 (Related, not Depend, because preemptive)
2. Downstream propagation task -- Related --> TC-8001
3. Downstream propagation task -- Blocks (blocked by) --> upstream backport task

---

## Preemptive Task Comment (posted to TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: upstream backport task (security-preemptive)
- 2.1.x: downstream propagation task (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x has 2 tasks (dependency bump + downstream propagation); 2.1.x has 2 tasks (upstream backport + downstream propagation). Matches ecosystem classification table for Cargo (source dependency).
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created (no existing sibling CVE Jira).
- [x] **Link types**: "Depend" for tasks linked to their own CVE Jira (2.2.x tasks to TC-8001), "Related" for preemptive tasks linked to another stream's CVE Jira (2.1.x tasks to TC-8001), "Blocks" for upstream-to-downstream within a stream.
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Each task includes guidance for "upstream" deployment context.
- [x] **Release Jira linking**: Release Jira orchestration (Step 7.5) would link non-preemptive remediation tasks to the release Task (not executed in this eval).
- [x] **Dedup consistency**: No dedup detected -- all streams receive new remediation tasks.

## Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Transition**: TC-8001 to In Progress
3. **Post summary comment** to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 removed; RHTPA 2.2.0, 2.2.1, 2.2.2 added)
   - Remediation tasks created (4 total: 2 for 2.2.x, 2 preemptive for 2.1.x)
   - Cross-stream impact on 2.1.x
