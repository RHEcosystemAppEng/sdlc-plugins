# Step 8 -- Remediation

## Triage Outcome

### Stream 2.2.x (issue scope): Case C -- Not Affected

No supported versions in the 2.2.x stream ship a vulnerable version of h2. All versions ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

- Resolution: Not a Bug
- VEX Justification: **Component not Present** (the vulnerable version of h2 is not included in any 2.2.x release; all ship the fixed version 0.4.8+)
- VEX custom field: customfield_12345

**Close comment**:
> No supported versions in the 2.2.x stream ship a vulnerable version of h2. Version impact analysis shows all 2.2.x releases ship h2 >= 0.4.8, which is the fix threshold for CVE-2026-48901. All supported versions ship h2 0.4.8 or 0.4.9, which are outside the affected range (< 0.4.8).

### Stream 2.1.x (cross-stream): Case B -- Cross-Stream Impact

The version impact analysis reveals that the **2.1.x** stream is affected (h2 0.4.5 < 0.4.8 in versions 2.1.0 and 2.1.1). Since no companion CVE Jira exists for the 2.1.x stream, preemptive remediation tasks are created.

**Cross-stream impact comment** (posted to TC-8030):
> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis. Versions 2.1.0 and 2.1.1 ship h2 0.4.5, which is within the affected range. This stream may require a separate PSIRT triage or is covered by preemptive remediation tasks below.

---

## Preemptive Remediation Tasks (Stream 2.1.x)

Since h2 is a Cargo (source dependency) ecosystem, two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030 (originating CVE Jira, different stream)

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)
```

### Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030 (originating CVE Jira, different stream)

**Blocked by**: Task 1 (upstream backport must merge first)

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)
```

---

## Jira Operations Summary

### For TC-8030 (stream 2.2.x):

1. **Affects Versions Correction**: Current [RHTPA 2.2.0] -- no correction needed for the scoped stream since no 2.2.x versions are affected. Remove RHTPA 2.2.0 from Affects Versions (version is not actually affected).
2. **Close**: Transition to Closed with resolution "Not a Bug"
3. **VEX Justification**: Set customfield_12345 to "Component not Present"
4. **Label**: Add `ai-cve-triaged`
5. **Cross-stream comment**: Post cross-stream impact notice for 2.1.x
6. **Preemptive tasks comment**: List created preemptive tasks for 2.1.x

### For preemptive tasks (stream 2.1.x):

1. **Create** upstream backport task with `security-preemptive` label
2. **Create** downstream propagation subtask with `security-preemptive` label
3. **Link** both tasks to TC-8030 with "Related" link type
4. **Link** downstream task blocked by upstream task with "Blocks" link type
5. **Post** description digest comments on both tasks
