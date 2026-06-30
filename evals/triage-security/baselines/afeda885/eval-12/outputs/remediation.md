# Step 7 -- Remediation: CVE-2026-48901 (h2)

## Triage Outcome for Scoped Stream (2.2.x)

### Case C: No supported versions affected within issue scope

The version impact table shows **NO** for all 2.2.x versions. All versions in the 2.2.x stream ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as **Not a Bug** (not affected).

**Proposed actions** (pending engineer confirmation):

1. Add comment to TC-8030:
   > No supported 2.2.x versions ship a vulnerable version of h2.
   > Version impact analysis shows all 2.2.x versions ship h2 0.4.8 or later,
   > which is at or above the fix threshold (< 0.4.8) established by both
   > MITRE CVE API and OSV.dev.
   >
   > | Version | h2 Version | Affected? |
   > |---------|------------|-----------|
   > | 2.2.0   | 0.4.8      | NO        |
   > | 2.2.1   | 0.4.8      | NO        |
   > | 2.2.2   | --         | NO (retag of 2.2.1) |
   > | 2.2.3   | 0.4.9      | NO        |
   > | 2.2.4   | 0.4.9      | NO        |

2. Transition TC-8030 to **Closed** with resolution **Not a Bug**.

3. Set VEX Justification (customfield_12345) to **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version; all versions ship h2 at or above the fix threshold.

4. Add label `ai-cve-triaged` to TC-8030.

5. Assign TC-8030 to current user.

## Cross-Stream Impact (Case B): 2.1.x Stream

The version impact analysis reveals that stream **2.1.x** (outside this issue's scope) IS affected:

| Version | h2 Version | Affected? |
|---------|------------|-----------|
| 2.1.0   | 0.4.5      | YES       |
| 2.1.1   | 0.4.5      | YES       |

### Cross-Stream Impact Comment

Post to TC-8030:
> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> All 2.1.x versions ship h2 0.4.5, which is below the fix threshold.
> This stream is tracked by a companion issue (if one exists) or may require
> separate PSIRT triage.

### Preemptive Remediation Tasks for 2.1.x

If no companion CVE Jira exists for the 2.1.x stream (i.e., no sibling Vulnerability issue with label CVE-2026-48901 and suffix `[rhtpa-2.1]`), create preemptive remediation tasks:

#### Task 1: Upstream Backport (preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030

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

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

#### Task 2: Downstream Propagation (preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030; Blocked by upstream backport task

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

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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
