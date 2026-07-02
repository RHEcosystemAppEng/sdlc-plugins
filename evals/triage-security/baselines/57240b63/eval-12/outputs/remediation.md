# Step 8 -- Remediation: TC-8030

## Triage Outcome: Case C -- No Supported Versions Affected (in scoped stream)

TC-8030 is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`).

The version impact analysis shows that **no 2.2.x versions are affected**:
- All 2.2.x versions ship h2 >= 0.4.8, which is at or above the enriched fix threshold (0.4.8) from Step 1.5 cross-validation (MITRE CVE API + OSV.dev).
- No remediation tasks are needed for the 2.2.x stream.

## PROPOSAL: Close TC-8030 as Not a Bug

**Rationale**: No supported versions in the 2.2.x stream ship a vulnerable version of h2. Version impact analysis confirms all 2.2.x releases include h2 >= 0.4.8, which is at or above the fix threshold.

### Proposed Jira Mutations (require engineer confirmation)

1. **Add comment** to TC-8030:

   > No supported versions in the 2.2.x stream ship a vulnerable version of h2.
   > Version impact analysis:
   >
   > | Version | h2 version | Affected? |
   > |---------|-----------|-----------|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | -- | NO (retag of 2.2.1) |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |
   >
   > All 2.2.x versions ship h2 0.4.8+, which is outside the affected range (< 0.4.8).
   > Fix threshold sourced from MITRE CVE API (lessThan 0.4.8) and OSV.dev (fixed 0.4.8).

2. **Transition** TC-8030 to Closed with resolution **"Not a Bug"**.

3. **Set VEX Justification** (customfield_12345) to **"Component not Present"** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version. All 2.2.x versions include h2 at or above the fix threshold.

4. **Add label** `ai-cve-triaged` to TC-8030.

## Cross-Stream Impact: 2.1.x IS Affected

While the 2.2.x stream is not affected, the version impact analysis reveals that the **2.1.x stream IS affected**:

| Version | Backend Tag | h2 version | Affected? |
|---------|-------------|------------|-----------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** |

Both 2.1.x versions ship h2 0.4.5, which is below the fix threshold (0.4.8).

### PROPOSAL: Post cross-stream impact comment on TC-8030

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> - 2.1.0 ships h2 0.4.5 (affected)
> - 2.1.1 ships h2 0.4.5 (affected)
>
> The 2.1.x stream is tracked separately. If a companion CVE Jira exists for stream 2.1.x,
> it should be triaged independently. If no companion issue exists, PSIRT should be notified
> that stream 2.1.x requires a tracking issue for CVE-2026-48901.

### Remediation Tasks for 2.1.x (if a companion CVE Jira exists or preemptive tasks are warranted)

If Case B applies (proactive remediation for streams without their own CVE Jira), the following tasks would be created with the `security-preemptive` label and "Related" link to TC-8030:

#### Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists yet
> for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

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
- Check for pinned versions or transitive dependency constraints that might prevent the bump
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

#### Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists yet
> for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)
