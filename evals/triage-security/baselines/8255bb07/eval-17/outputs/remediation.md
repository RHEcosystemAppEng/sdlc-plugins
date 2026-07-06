# Step 8 -- Remediation

## Triage Outcome

### Issue stream (2.2.x) -- Already fixed in latest

The 2.2.x stream already ships the fix in versions 2.2.3+ (quinn-proto 0.11.14). The latest released versions are not affected. While earlier versions (2.2.0, 2.2.1, 2.2.2) shipped vulnerable code, the fix has already been picked up in the stream. No new remediation tasks are required for 2.2.x.

Affects Versions will be corrected to reflect 2.2.0, 2.2.1, 2.2.2 (removing the incorrect RHTPA 2.0.0).

### Cross-stream impact (2.1.x) -- Case B: Proactive remediation

All versions in the 2.1.x stream (2.1.0, 2.1.1) are affected. Since this stream is outside the issue's scope ([rhtpa-2.2]) and no stream-specific CVE Jira exists for 2.1.x, proactive (preemptive) remediation tasks will be created per Case B.

The ecosystem is Cargo (source dependency), so **two tasks** are created for the 2.1.x stream: an upstream backport task and a downstream propagation subtask.

---

## Remediation Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, preemptive -- originating CVE is from a different stream)

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
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

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, preemptive), Blocks (blocked by upstream backport task)

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Cross-Stream Impact Comment (for TC-8001)

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
lock file analysis. The 2.1.x stream has no stream-specific CVE Jira.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Post-Triage Summary

After all triage actions, the following would be applied to TC-8001:

1. **Label added**: `ai-cve-triaged`
2. **Affects Versions corrected**: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
3. **Triage outcome**: 2.2.x stream already fixed in versions 2.2.3+; 2.1.x stream requires preemptive remediation (2 tasks created)
4. **Remediation tasks**: Upstream backport (2.1.x) + Downstream propagation (2.1.x), linked as Related to TC-8001 with security-preemptive labels
5. **Reporter @mention**: Included in post-triage summary comment
