# Step 8 -- Remediation

## Triage Decision

### Scoped Stream Assessment (2.2.x)

The issue TC-8030 is scoped to stream **2.2.x**. The version impact analysis shows that **no versions in the 2.2.x stream are affected**:

- All 2.2.x versions ship h2 >= 0.4.8, which is at or above the enriched fix threshold
- h2 0.4.8 is the first fixed version (from MITRE CVE API and OSV.dev cross-validation)

**Outcome for scoped stream: Case C -- No supported versions affected**

Recommendation: Close TC-8030 as **Not a Bug** (not affected).

- Resolution: Not a Bug
- VEX Justification (customfield_12345): **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version
- Comment: "No supported versions in the 2.2.x stream ship a vulnerable version of h2. Version impact analysis shows all 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold (< 0.4.8). The vulnerability does not affect this stream."
- Label to add: `ai-cve-triaged`

### Cross-Stream Impact Assessment (Case A)

The version impact analysis reveals that stream **2.1.x** (outside TC-8030's scope) **is affected**:

- 2.1.0: h2 0.4.5 (affected, < 0.4.8)
- 2.1.1: h2 0.4.5 (affected, < 0.4.8)

**Cross-stream impact comment** (to be posted on TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> Versions 2.1.0 and 2.1.1 both ship h2 0.4.5, which is within the affected range.
> This stream is tracked by a companion issue (see Related links) or may require
> separate PSIRT triage.

### Preemptive Remediation Tasks for 2.1.x

Since stream 2.1.x is affected but does not have its own CVE Jira for CVE-2026-48901, create **preemptive** remediation tasks. The ecosystem is Cargo (source dependency), so **2 tasks** are created for the 2.1.x stream.

---

## Remediation Task 1: Upstream Backport (2.1.x -- preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to originating CVE TC-8030, since this is a preemptive task for a different stream)

### Task Description

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: source dependency (Cargo crate)
- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Run `cargo update -p h2` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`
- Verify the lock file reflects h2 >= 0.4.8 after the update

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

- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)
```

---

## Remediation Task 2: Downstream Propagation (2.1.x -- preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to originating CVE TC-8030)

**Blocked by**: Remediation Task 1 (upstream backport must merge first)

### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: source dependency (carried forward from upstream task)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the h2 >= 0.4.8 fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream fix must merge first)
- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)
```

---

## Jira Linkage Summary

| Link Type | From | To | Purpose |
|-----------|------|----|---------|
| Related | TC-8030 (CVE) | Upstream backport task | Preemptive remediation (different stream) |
| Related | TC-8030 (CVE) | Downstream propagation task | Preemptive remediation (different stream) |
| Blocks | Upstream backport task | Downstream propagation task | Downstream is blocked by upstream |

## Post-Triage Summary

### Actions on TC-8030:

1. **Add label**: `ai-cve-triaged`
2. **Close as Not a Bug**: The 2.2.x stream (scoped stream) is not affected -- all versions ship h2 >= 0.4.8
3. **Set VEX Justification** (customfield_12345): Component not Present
4. **Post cross-stream impact comment**: 2.1.x is affected (h2 0.4.5 < 0.4.8)
5. **Post preemptive task comment**:
   > Preemptive remediation tasks created for streams without CVE Jiras:
   > - 2.1.x: upstream backport task + downstream propagation task (security-preemptive)
   >
   > These tasks use the "Related" link type and carry the security-preemptive
   > label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   > reconciliation will link them and remove the label.
6. **Post summary comment** with version impact table, Affects Versions correction, and triage outcome
