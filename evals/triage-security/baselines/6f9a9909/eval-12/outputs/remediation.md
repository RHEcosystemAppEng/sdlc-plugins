# Step 8 -- Remediation

## Triage Outcome

### In-scope stream (2.2.x): Case C -- No supported versions affected

The version impact table shows **NO** for all versions in the 2.2.x stream (the issue's scoped stream). All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as **Not a Bug** (not affected).

- Resolution: Not a Bug
- VEX Justification: **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version. All 2.2.x builds include h2 0.4.8 or later, which contains the fix for CVE-2026-48901.

Proposed closing comment:
> No supported 2.2.x versions ship a vulnerable version of h2. Version impact
> analysis: all 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which
> is outside the affected range (< 0.4.8). The fix for CVE-2026-48901 was
> included in h2 0.4.8, and the earliest 2.2.x release (2.2.0) already ships
> this version.

### Cross-stream impact (2.1.x): Case A -- Proactive remediation

The version impact analysis reveals that stream **2.1.x** (outside this issue's scope) IS affected: both 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold of 0.4.8.

**Cross-stream impact comment** (to post on TC-8030):
> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock
> file analysis. Stream 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5.
> These streams are tracked by companion issues (see Related links) or may
> require separate PSIRT triage.

Since no companion CVE Jira exists for the 2.1.x stream, **preemptive remediation tasks** are created:

---

## Preemptive Remediation Tasks for Stream 2.1.x

### Task 1: Upstream Backport (preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030, the originating CVE Jira from stream 2.2.x)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- h2 is a direct dependency of the backend workspace
- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update Cargo.lock
- If a direct bump to 0.4.8 introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog and PR #800)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira from stream 2.2.x)

---

### Task 2: Downstream Propagation (preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030); Blocks (blocked by upstream backport task above)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira from stream 2.2.x)

---

## Summary of Actions

1. **TC-8030 (2.2.x scope)**: Close as Not a Bug with VEX Justification "Component not Present"
   - All 2.2.x versions ship h2 >= 0.4.8 (not affected)
2. **Cross-stream notice**: Post comment on TC-8030 noting 2.1.x impact
3. **Preemptive upstream task (2.1.x)**: Bump h2 to >= 0.4.8 on release/0.3.z
   - Labels: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
   - Link: Related to TC-8030
4. **Preemptive downstream task (2.1.x)**: Update backend ref in rhtpa-release.0.3.z
   - Labels: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
   - Link: Related to TC-8030, Blocked by upstream task
5. **Add label**: `ai-cve-triaged` to TC-8030
