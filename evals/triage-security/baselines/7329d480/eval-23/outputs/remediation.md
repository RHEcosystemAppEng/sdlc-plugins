# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome Summary

- **Scoped stream (2.2.x)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. However, the fix is already incorporated in versions 2.2.3+ (quinn-proto 0.11.14 shipped starting with build 0.4.11). The upstream branch `release/0.4.z` already contains the fix. No new upstream backport task is needed for 2.2.x.
- **Cross-stream (2.1.x)**: All versions (2.1.0, 2.1.1) are affected. The upstream branch `release/0.3.z` does NOT contain the fix. Preemptive remediation tasks are needed (Case B).

## Case B: Cross-Stream Impact

The 2.1.x stream is also affected but has no stream-specific CVE Jira. Preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

---

## Remediation Task 1: Upstream Backport (2.1.x stream -- preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related to TC-8001

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

quinn-proto before version 0.11.14 allows a remote attacker to cause a denial of
service (DoS) by sending a QUIC transport frame that creates an excessive number
of streams. The server panics when the allocation exceeds internal limits.

Affected versions: 2.1.0 (ships quinn-proto 0.11.9), 2.1.1 (ships quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (2.1.x stream -- preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related to TC-8001
**Blocked by**: Upstream backport task (Task 1 above)

### Task Description

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

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Post-Triage Actions

### Affects Versions Correction (Step 3)

Remove `RHTPA 2.0.0` and add `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2` to reflect the actual affected versions based on lock file evidence.

### Cross-Stream Impact Comment (Step 8, Case B)

Post to TC-8001:

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9. This stream does not have a companion CVE Jira -- preemptive remediation tasks have been created.

### Preemptive Tasks Comment

Post to TC-8001:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: [upstream-task-key] (security-preemptive, upstream backport)
> - 2.1.x: [downstream-task-key] (security-preemptive, downstream propagation)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.

### 2.2.x Stream Status

For the scoped 2.2.x stream, the fix is already present in versions 2.2.3+ (quinn-proto 0.11.14 shipped starting with build 0.4.11). No remediation tasks are needed for this stream. The Affects Versions correction documents which older versions were affected.

### Label Addition

Add `ai-cve-triaged` label to TC-8001 to mark triage as complete.
