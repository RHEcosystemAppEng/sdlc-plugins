# Step 8 -- Remediation

## Triage Decision

### Scoped stream (2.2.x): Case C -- No supported versions affected

The version impact table shows **NO** for all versions in the issue-scoped stream (2.2.x). All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

- Resolution: Not a Bug
- VEX Justification: **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x release. All 2.2.x versions ship h2 0.4.8 or later.
- VEX Justification field: customfield_12345

**Proposed Jira comment:**
> No supported versions in stream 2.2.x ship a vulnerable version of h2. Version impact analysis shows all 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold (< 0.4.8). Closing as Not a Bug.

### Cross-stream impact: Case A -- Stream 2.1.x affected

The version impact analysis reveals that stream **2.1.x** (outside the issue's scope) is affected. Both 2.1.x versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.

**Proposed cross-stream impact comment on TC-8030:**
> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis. Both 2.1.0 (h2 0.4.5) and 2.1.1 (h2 0.4.5) are affected. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

## Preemptive Remediation Tasks for Stream 2.1.x

Since the 2.1.x stream is affected but has no stream-specific CVE Jira (no sibling issue with `[rhtpa-2.1]` suffix found), create preemptive remediation tasks.

Ecosystem: Cargo (source dependency, fix available upstream) -> 2 tasks: dependency bump + downstream propagation

### Task 1: Dependency Bump (upstream)

**Summary**: Remediate CVE-2026-48901: update h2 to 0.4.8 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030, the originating CVE Jira -- preemptive variant)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: bump h2 to 0.4.8 via dependency update.
The vulnerable dependency (h2 < 0.4.8) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p h2` to pull in the latest compatible version (>= 0.4.8)
- If the update pulls a version that still falls within the affected range, pin explicitly: `cargo add h2@0.4.8`
- Verify the lock file reflects >= 0.4.8 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030 -- preemptive variant), Blocks (blocked by Task 1)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream dependency bump task.

The dependency bump task bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

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

- Depends on: Task 1 (dependency bump must merge first)
- Depends on: TC-8030 (parent tracking issue)

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency, fix available) -> 2 tasks (dependency bump + downstream propagation) for 2.1.x stream. Matches ecosystem classification table.
- [x] **Cross-stream coverage**: The 2.1.x stream (affected, outside issue scope) has preemptive tasks created. The 2.2.x stream (scoped, not affected) has Case C closure recommendation.
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8030 (another stream's CVE Jira). "Blocks" for Task 1 -> Task 2 within the stream.
- [x] **Preemptive labels**: Both tasks carry the `security-preemptive` label (2.1.x has no stream-specific CVE Jira).
- [x] **Coordination guidance**: Each task includes upstream coordination guidance (deployment context: upstream).

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8030
2. Post summary comment to TC-8030 documenting:
   - Version impact table (2.2.x: not affected; 2.1.x: affected)
   - Scoped stream (2.2.x) closure as Not a Bug with VEX justification
   - Cross-stream impact notice for 2.1.x
   - Preemptive remediation tasks created for 2.1.x
3. @mention the reporter of TC-8030
