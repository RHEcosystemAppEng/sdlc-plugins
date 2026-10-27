# Remediation Tasks for TC-8001 (CVE-2026-31812)

## Overview

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: >= 0.11.14
- **Ecosystem**: Cargo (source dependency)
- **Issue scope**: Stream 2.2.x

### Stream 2.2.x -- Already Fixed

Stream 2.2.x does not require remediation tasks. The fix is already present in versions 2.2.3+ (backend tag v0.4.11 onward ships quinn-proto 0.11.14). The upstream branch `release/0.4.z` already contains the fix.

### Stream 2.1.x -- Preemptive Remediation Required

Stream 2.1.x is affected (all versions ship quinn-proto 0.11.9) and has no stream-specific CVE Jira. Preemptive remediation tasks are created per Case A (cross-stream impact). These tasks carry the `security-preemptive` label and use the "Related" link type to the originating CVE TC-8001.

---

## Task 1: Upstream Backport (Stream 2.1.x, Preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001 (originating CVE, stream 2.2.x)

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

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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

## Task 2: Downstream Propagation (Stream 2.1.x, Preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001 (originating CVE, stream 2.2.x)

**Blocked by**: Task 1 (upstream backport)

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Linkage Summary

| Link Type | From | To | Purpose |
|-----------|------|----|---------|
| Related | TC-8001 | Task 1 (upstream backport) | Preemptive task to originating CVE |
| Related | TC-8001 | Task 2 (downstream propagation) | Preemptive task to originating CVE |
| Blocks | Task 1 (upstream backport) | Task 2 (downstream propagation) | Upstream must merge before downstream |

## Notes

- **No Coordination Guidance**: The Source Repositories table in CLAUDE.md does not include a Deployment Context column. Per backward-compatibility rules, all repositories default to `upstream`, but the Coordination Guidance subsection is omitted entirely from all task descriptions.
- **Preemptive tasks**: Both tasks carry the `security-preemptive` label and use "Related" (not "Depend") link type because they are created proactively for a stream (2.1.x) that does not have its own CVE Jira. When PSIRT creates a stream-specific CVE Jira for 2.1.x, Step 4.4 reconciliation will link and remove the `security-preemptive` label.
- **Stream 2.2.x**: No remediation tasks created. The vulnerability is already fixed in versions 2.2.3+ (quinn-proto 0.11.14 ships starting from backend tag v0.4.11). Affects Versions correction is the only action needed for this stream.
