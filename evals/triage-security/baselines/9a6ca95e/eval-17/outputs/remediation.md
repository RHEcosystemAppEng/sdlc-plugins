# Step 8 -- Remediation

## Triage Outcome

### In-scope stream (2.2.x): Already Fixed

The 2.2.x stream already ships the fixed version of quinn-proto (0.11.14) in versions 2.2.3 and 2.2.4. No new remediation tasks are needed for this stream. The Affects Versions should be corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, and the issue can note that the fix was picked up in build 0.4.11 (version 2.2.3).

### Out-of-scope stream (2.1.x): Case B -- Cross-Stream Proactive Remediation

The version impact analysis reveals that the 2.1.x stream (outside this issue's scope) is also affected. All versions in the 2.1.x stream (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the vulnerable range (< 0.11.14).

**Cross-stream impact comment** (posted to TC-8001):
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
lock file analysis. The 2.1.x stream ships quinn-proto 0.11.9 in all versions
(2.1.0, 2.1.1). This stream is tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

Since the 2.1.x stream does not have its own CVE Jira for CVE-2026-31812, preemptive remediation tasks are created.

---

## Preemptive Remediation Tasks for Stream 2.1.x

Since quinn-proto is a Cargo (source dependency) ecosystem package, two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task (Preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001)

**Description**:

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

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
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

### Task 2: Downstream Propagation Subtask (Preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001), Blocked by upstream backport task

**Description**:

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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
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

## Post-Triage Summary

The following actions would be taken on TC-8001:

1. **Add label**: `ai-cve-triaged`
2. **Correct Affects Versions**: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
3. **Post summary comment** documenting:
   - Version impact table (all streams)
   - Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, 2.2.1, 2.2.2)
   - In-scope triage outcome: already fixed in 2.2.3+ (quinn-proto 0.11.14)
   - Cross-stream impact: 2.1.x affected, preemptive remediation tasks created
   - Links to preemptive tasks created for stream 2.1.x
   - @mention of the issue reporter (PSIRT analyst)
4. **Preemptive remediation comment** listing tasks created for 2.1.x stream with `security-preemptive` label
