# Step 8 — Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome Summary

### Stream 2.2.x (scoped stream) — Already Fixed

The scoped stream (2.2.x) has already incorporated the fix starting in version 2.2.3.
The latest version (2.2.4) ships quinn-proto 0.11.14, which is the fixed version.
No remediation tasks are needed for stream 2.2.x.

Affected versions (historical): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Fixed versions: RHTPA 2.2.3, RHTPA 2.2.4

### Stream 2.1.x (cross-stream impact) — Case B: Preemptive Remediation

Stream 2.1.x is affected in all versions (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9).
No stream-specific CVE Jira exists for 2.1.x. Preemptive remediation tasks are created
with the `security-preemptive` label.

Since quinn-proto is a Cargo (source dependency) ecosystem, two tasks are needed:
an upstream backport task and a downstream propagation subtask.

---

## Preemptive Remediation Task 1: Upstream Backport (Stream 2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (originating CVE from stream 2.2.x)

### Description

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
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
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

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Preemptive Remediation Task 2: Downstream Propagation (Stream 2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (originating CVE from stream 2.2.x)

**Blocked by**: Upstream backport task (Task 1 above)

### Description

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
