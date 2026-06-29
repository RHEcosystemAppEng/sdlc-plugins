# Step 7 -- Remediation

## Triage Outcome

Based on the version impact analysis:

- **Scoped stream (2.2.x)**: NOT AFFECTED -- all versions ship h2 >= 0.4.8
- **Cross-stream (2.1.x)**: AFFECTED -- all versions ship h2 0.4.5 (< 0.4.8)

This triggers two remediation paths:

1. **Case C** for the scoped stream: close TC-8030 as Not a Bug
2. **Case B** cross-stream impact: create preemptive remediation tasks for the 2.1.x stream

---

## Case C: Close TC-8030 as Not a Bug (scoped stream 2.2.x)

### Rationale

No supported versions in the 2.2.x stream ship a vulnerable version of h2. Version impact analysis shows all 2.2.x versions (2.2.0 through 2.2.4) ship h2 0.4.8 or 0.4.9, which are at or above the fix threshold of 0.4.8.

### Actions (pending engineer confirmation)

1. Add comment to TC-8030:
   > No supported versions in the 2.2.x stream ship a vulnerable version of h2.
   > Version impact analysis:
   >
   > | Version | h2 version | Affected? |
   > |---------|------------|-----------|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | -- | NO (retag of 2.2.1) |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |
   >
   > All supported versions ship h2 >= 0.4.8 which is outside the affected range (< 0.4.8).

2. Transition TC-8030 to Closed with resolution "Not a Bug"

3. Set VEX Justification field (customfield_12345) to **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not present in any 2.2.x release

4. Add label `ai-cve-triaged` to TC-8030

5. Assign TC-8030 to current user

---

## Case B: Cross-Stream Impact Notice and Preemptive Remediation (2.1.x stream)

### Cross-Stream Impact Comment

Post to TC-8030:

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> All 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5 which is below the fix threshold of 0.4.8.
> The 2.1.x stream is tracked by rhtpa-release.0.3.z and may require separate PSIRT triage.

### Preemptive Remediation Tasks for Stream 2.1.x

Since the 2.1.x stream does not have its own CVE Jira for CVE-2026-48901, create preemptive remediation tasks. h2 is a Cargo (source dependency) ecosystem, so two tasks are created.

#### Task 1: Upstream Backport Task (preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030 (not Depend, because this is cross-stream preemptive)

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
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

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)
```

#### Task 2: Downstream Propagation Subtask (preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030; Blocked by upstream backport task

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)
```

### Preemptive Tasks Comment on TC-8030

Post to TC-8030:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: [upstream-task-key] (upstream backport, security-preemptive)
> - 2.1.x: [downstream-task-key] (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.
