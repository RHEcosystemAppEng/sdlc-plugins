# Step 8 -- Remediation: CVE-2026-48901

## Triage Outcome

**Case B: Cross-stream impact with proactive remediation**

The issue is scoped to stream 2.2.x ([rhtpa-2.2]). Within the scoped stream, only version 2.2.0 is affected (versions 2.2.1+ already ship the fix). Cross-stream analysis reveals that stream 2.1.x is also affected (both 2.1.0 and 2.1.1 ship h2 0.4.5).

Since the fix is already present in the 2.2.x stream starting from version 2.2.1, no upstream backport task is needed for the 2.2.x stream -- the vulnerability was already remediated by the h2 bump in build v0.4.8. However, stream 2.1.x still ships the vulnerable version and needs remediation.

---

## Remediation Tasks for Stream 2.1.x (Cross-Stream / Preemptive)

Since stream 2.1.x has no CVE Jira of its own for CVE-2026-48901, proactive remediation tasks are created with the `security-preemptive` label.

### Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030 (originating CVE Jira)

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

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

### Remediation approach (direct dependency)

The vulnerable package h2 is a direct dependency of the backend workspace:

- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
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

- Depends on: TC-8030 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030 (originating CVE Jira); Blocked by upstream backport task (Task 1)

#### Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (Task 1) -- upstream backport must merge first
- Depends on: TC-8030 (parent tracking issue)

---

## Cross-Stream Impact Comment (to be posted on TC-8030)

```
Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
Stream 2.1.x ships h2 0.4.5 in all versions (2.1.0 and 2.1.1).
No stream-specific CVE Jira exists for 2.1.x -- preemptive remediation tasks created.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (security-preemptive), [downstream-task-key] (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them
and remove the label.
```

## Note on Stream 2.2.x (Issue Scope)

Within the scoped stream 2.2.x, version 2.2.0 is the only affected version. However, the fix was already incorporated in version 2.2.1 (build v0.4.8, released 2026-02-05), and all subsequent versions (2.2.2 through 2.2.4) also carry the fix. No new remediation tasks are needed for stream 2.2.x -- the vulnerability was already remediated by the natural dependency update in the v0.4.8 build.

The Affects Versions field (RHTPA 2.2.0) is correct and does not need correction.

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8030
2. Post summary comment to TC-8030 with version impact table, Affects Versions confirmation, triage outcome, and links to all remediation tasks created
3. @mention the reporter of TC-8030 in the summary comment
