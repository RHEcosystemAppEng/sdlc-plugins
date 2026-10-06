# Step 8 -- Remediation

## Triage Decision

Based on the version impact analysis:

1. **Scoped stream (2.2.x)**: No versions affected -- all ship h2 >= 0.4.8
2. **Cross-stream (2.1.x)**: All versions affected -- both ship h2 0.4.5 (< 0.4.8)

### Case C (scoped stream 2.2.x): Close as Not a Bug

No supported versions in the 2.2.x stream ship a vulnerable version of h2.

- **Resolution**: Not a Bug
- **VEX Justification**: Component not Present (the vulnerable version of h2 is not present in any 2.2.x release; all versions ship h2 >= 0.4.8)
- **Comment**: "No supported 2.2.x versions ship a vulnerable version of h2. Version impact analysis shows all 2.2.x versions ship h2 0.4.8 or later, which is at or above the fix threshold (< 0.4.8). Closing as Not a Bug."

### Case A (cross-stream impact): 2.1.x Preemptive Remediation

The 2.1.x stream is affected (h2 0.4.5 < 0.4.8 in both 2.1.0 and 2.1.1). Since the issue TC-8030 is scoped to 2.2.x, preemptive remediation tasks should be created for the 2.1.x stream.

#### Cross-stream impact comment (posted to TC-8030):

```
Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
analysis. Both 2.1.0 and 2.1.1 ship h2 0.4.5 (vulnerable).
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

---

## Preemptive Remediation Tasks for 2.1.x

Since h2 is a Cargo (source dependency) ecosystem package, two tasks are created per the ecosystem classification table: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
**Link type**: Related (to TC-8030, since TC-8030 belongs to a different stream)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update h2 dependency to >= 0.4.8 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira, scoped to 2.2.x)

---

### Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
**Link type**: Related (to TC-8030); Blocks (blocked by upstream backport task)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
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

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira, scoped to 2.2.x)
