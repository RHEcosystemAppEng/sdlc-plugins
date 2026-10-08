# Step 8 -- Remediation

## Triage Outcome Summary

### 2.2.x stream (scoped stream)

**No new remediation tasks required.** The fix for CVE-2026-31812 (quinn-proto >= 0.11.14) is already present in released versions 2.2.3 (build v0.4.11) and 2.2.4 (build v0.4.12). The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14. There is no outstanding work to remediate this stream.

The Affects Versions have been corrected to [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] to accurately reflect which historical versions shipped the vulnerable dependency.

### 2.1.x stream (Case A -- Cross-stream impact, preemptive remediation)

**Cross-stream impact detected.** The version impact analysis reveals that the 2.1.x stream (outside this issue's scope of 2.2.x) is also affected. Both 2.1.0 (quinn-proto 0.11.9) and 2.1.1 (quinn-proto 0.11.9) ship a vulnerable version.

The upstream branch `release/0.3.z` does NOT yet ship the fix (latest tag v0.3.12 has quinn-proto 0.11.9). This requires an upstream backport.

Since no sibling CVE Jira exists for the 2.1.x stream, **preemptive remediation tasks** are created with the `security-preemptive` label and linked to TC-8001 via "Related" (not "Depend").

---

## Cross-Stream Impact Comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto (< 0.11.14) also affects stream 2.1.x based
on lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9.
This stream is not tracked by a companion issue and may require separate PSIRT triage.
```

---

## Preemptive Remediation Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001 (originating CVE Jira, different stream)

### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE from stream rhtpa-2.2)

---

## Preemptive Remediation Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001 (originating CVE Jira, different stream)

**Blocked by**: Upstream backport task (Task 1 above)

### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (must merge first)
- Related to: TC-8001 (originating CVE from stream rhtpa-2.2)

---

## Preemptive Task Comment (posted to TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive, blocked by upstream task)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Pre-Creation Checklist Verification

- [x] **Task count per stream**: 2.1.x has 2 tasks (source dependency Cargo: upstream backport + downstream propagation). 2.2.x has 0 tasks (fix already present in 2.2.3+).
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created. No sibling CVE Jira exists for 2.1.x.
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8001 (different stream's CVE). "Blocks" for upstream -> downstream within the 2.1.x stream.
- [x] **Preemptive labels**: Both 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Both tasks include upstream deployment context guidance.
