# Step 8 -- Remediation

## Triage Outcome for TC-8030

### Case C: Scoped Stream 2.2.x -- Close as Not a Bug

The version impact analysis shows that **no versions** in the scoped stream (2.2.x) ship a vulnerable version of h2. All 2.2.x versions include h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

- Resolution: Not a Bug
- VEX Justification: Component not Present (the vulnerable version of h2, i.e., < 0.4.8, is not shipped in any 2.2.x version)
- VEX Justification custom field: customfield_12345

**Close comment**:

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
> All 2.2.x versions ship h2 0.4.8 or later, which is outside the affected range (< 0.4.8).
> Fix threshold source: MITRE CVE API and OSV.dev (cross-validated, both report fixed at 0.4.8).

### Case B: Cross-Stream Impact -- 2.1.x Affected

The version impact analysis reveals that the **2.1.x** stream (outside TC-8030's scope) IS affected. All 2.1.x versions ship h2 0.4.5, which is below the fix threshold of 0.4.8.

**Cross-stream impact comment** (to post on TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> The 2.1.x stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

## Preemptive Remediation Tasks for 2.1.x Stream

Since the 2.1.x stream lacks its own CVE Jira for CVE-2026-48901, preemptive remediation tasks should be created. The ecosystem is Cargo (source dependency), so two tasks are required: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task (Preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030 -- preemptive, not Depend)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5 at v0.3.8), 2.1.1 (h2 0.4.5 at v0.3.12)
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

---

### Task 2: Downstream Propagation Subtask (Preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030 -- preemptive, not Depend)

**Blocked by**: Task 1 (upstream backport must merge first)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

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
- Depends on: TC-8030 (parent tracking issue)
