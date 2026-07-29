# Step 8 -- Remediation

## Triage Outcome

### In-Scope Stream (2.2.x): Case C -- No Supported Versions Affected

No versions in the 2.2.x stream ship a vulnerable version of h2. All versions
ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as **Not a Bug** (not affected).

- **Resolution**: Not a Bug
- **VEX Justification**: Component not Present (the vulnerable h2 version
  < 0.4.8 is not included in any 2.2.x release)

**Proposed Jira comment for TC-8030**:

> No supported versions in the 2.2.x stream ship a vulnerable version of h2.
> Version impact analysis:
>
> | Version | h2 version | Affected? |
> |---------|------------|-----------|
> | 2.2.0 | 0.4.8 | NO |
> | 2.2.1 | 0.4.8 | NO |
> | 2.2.2 | 0.4.8 | NO (retag of 2.2.1) |
> | 2.2.3 | 0.4.9 | NO |
> | 2.2.4 | 0.4.9 | NO |
>
> All 2.2.x versions ship h2 0.4.8+, which is outside the affected range
> (< 0.4.8). Fix threshold validated against MITRE CVE API and OSV.dev
> (both confirm fixed at 0.4.8).

### Cross-Stream Impact: Case A -- Stream 2.1.x Is Affected

The version impact analysis reveals that stream **2.1.x** (outside this issue's
scope) is affected:

| Version | h2 version | Affected? |
|---------|------------|-----------|
| 2.1.0 | 0.4.5 | YES |
| 2.1.1 | 0.4.5 | YES |

**Proposed cross-stream impact comment for TC-8030**:

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock
> file analysis. Both 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5.
> This stream is tracked by companion issues (see Related links)
> or may require separate PSIRT triage.

Since no sibling CVE Jira exists for stream 2.1.x (no companion issue found),
**preemptive remediation tasks** are created for the 2.1.x stream.

---

## Preemptive Remediation Tasks for Stream 2.1.x

The h2 library is in the **Cargo** ecosystem (source dependency category),
which produces **2 tasks** per affected stream: an upstream backport task and
a downstream propagation subtask.

### Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030 -- preemptive, originating CVE is in a different stream)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version
(0.4.8+).

Affected versions: 2.1.0 (backend v0.3.8), 2.1.1 (backend v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (backend workspace -> h2)
- Fix threshold validated against MITRE CVE API (lessThan 0.4.8) and OSV.dev
  (fixed 0.4.8) -- both sources agree

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog and PR #800)

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

- Related to: TC-8030 (originating CVE Jira, stream 2.2.x -- preemptive)

---

### Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030 -- preemptive)

**Blocked by**: Task 1 (upstream backport must merge first)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira, stream 2.2.x -- preemptive)

---

## Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8030
2. **Post summary comment** to TC-8030 documenting:
   - Version impact table (2.2.x not affected, 2.1.x affected)
   - Cross-stream impact notice (2.1.x)
   - Preemptive remediation tasks created for 2.1.x
   - Close recommendation for TC-8030 (Not a Bug, VEX: Component not Present)
3. **Close TC-8030** as Not a Bug with VEX Justification "Component not Present"
   (pending engineer confirmation)

## Preemptive Task Summary Comment for TC-8030

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: [upstream-task-key] (upstream backport, security-preemptive)
> - 2.1.x: [downstream-task-key] (downstream propagation, security-preemptive, blocked by upstream)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.
