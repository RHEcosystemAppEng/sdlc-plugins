# Step 8 -- Remediation

## Decision Tree Evaluation

1. **Any supported versions affected?** YES -- 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5 < 0.4.8.
2. **Issue scoped to a single stream?** YES -- scoped to 2.2.x via `[rhtpa-2.2]` suffix.
3. **Other streams also affected?** YES -- 2.1.x is affected (cross-stream impact).

This triggers:
- **Case A**: Post cross-stream impact comment and create preemptive remediation tasks for 2.1.x
- **Case B**: Create remediation tasks for affected streams within the issue's scope (2.2.x). However, since the scoped stream (2.2.x) is NOT affected, no standard remediation tasks are created for 2.2.x.
- **Case C consideration**: For the scoped stream (2.2.x), no versions are affected. Recommend closing TC-8030 as "Not a Bug" with VEX Justification "Component not Present" (the vulnerable version of h2 is not shipped in any 2.2.x version). The vulnerable h2 < 0.4.8 is not present -- all 2.2.x versions ship h2 >= 0.4.8.

## Case A: Cross-Stream Impact Comment

The following comment would be posted to TC-8030:

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> Versions 2.1.0 and 2.1.1 both ship h2 0.4.5, which is below the fix threshold of 0.4.8.
> This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

## Case A: Preemptive Remediation Tasks for 2.1.x

Since the 2.1.x stream does not have its own CVE Jira for CVE-2026-48901, preemptive remediation tasks are created. These carry the `security-preemptive` label and use "Related" link type (not "Depend") to the originating CVE Jira TC-8030.

Ecosystem: Cargo (source dependency) -- two tasks per stream.

### Task 1: Upstream Backport (2.1.x -- preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

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

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update h2 dependency to >= 0.4.8 in Cargo.lock
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

- Related to: TC-8030 (originating CVE Jira -- different stream)

---

### Task 2: Downstream Propagation (2.1.x -- preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

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

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira -- different stream)

---

## Close Recommendation for TC-8030 (scoped stream 2.2.x)

**Recommendation**: Close TC-8030 as **Not a Bug** (not affected).

**Rationale**: No supported versions in the 2.2.x stream ship a vulnerable version of h2. All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold established by cross-validated MITRE and OSV.dev data.

**VEX Justification**: Component not Present (the vulnerable h2 version < 0.4.8 is not present in any 2.2.x release)

**VEX Justification custom field**: customfield_12345

**Proposed comment for TC-8030**:

> No supported 2.2.x versions ship a vulnerable version of h2.
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
> All 2.2.x versions ship h2 >= 0.4.8, which is outside the affected range (< 0.4.8).
> Fix threshold source: MITRE CVE API and OSV.dev (cross-validated agreement).
>
> Cross-stream impact: 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5, which IS affected.
> Preemptive remediation tasks have been created for the 2.1.x stream.

**Proposed actions**:
1. Set VEX Justification (customfield_12345) to "Component not Present"
2. Add comment with version impact table and cross-stream impact notice
3. Transition TC-8030 to Closed with resolution "Not a Bug"
4. Add label: ai-cve-triaged
