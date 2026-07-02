# Step 8 -- Remediation

## Triage Outcome

**Issue**: TC-8030 -- CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2]
**Scoped stream**: 2.2.x
**Enriched fix threshold**: h2 0.4.8 (from MITRE CVE API + OSV.dev)

### Decision Path

1. **Any supported versions affected?** YES -- stream 2.1.x is affected (h2 0.4.5 < 0.4.8)
2. **Scoped stream (2.2.x) affected?** NO -- all 2.2.x versions ship h2 >= 0.4.8
3. **Other streams affected?** YES -- stream 2.1.x (both 2.1.0 and 2.1.1)

This triggers **Case C** for the scoped stream (close as Not a Bug) combined with **Case B** (cross-stream impact on 2.1.x).

---

## Case C: Close TC-8030 as Not a Bug

**Recommendation**: Close TC-8030 with resolution "Not a Bug" (not affected).

**Rationale**: No supported versions in the 2.2.x stream ship a vulnerable version of h2. All 2.2.x releases (2.2.0 through 2.2.4) include h2 >= 0.4.8, which is at or above the fix threshold.

**VEX Justification**: Component not Present (the vulnerable version of h2 is not shipped in any 2.2.x release)

Note: The VEX Justification custom field (customfield_12345) is configured in Security Configuration and should be set when closing.

**Proposed Jira comment**:
> No supported 2.2.x versions ship a vulnerable version of h2. Version impact analysis shows all 2.2.x releases include h2 >= 0.4.8, which is outside the affected range (< 0.4.8).
>
> | Version | h2 version | Affected? |
> |---------|------------|-----------|
> | 2.2.0 | 0.4.8 | NO |
> | 2.2.1 | 0.4.8 | NO |
> | 2.2.2 | -- | NO (retag of 2.2.1) |
> | 2.2.3 | 0.4.9 | NO |
> | 2.2.4 | 0.4.9 | NO |
>
> Cross-stream impact: h2 0.4.5 (< 0.4.8) affects stream 2.1.x (versions 2.1.0, 2.1.1). See preemptive remediation tasks below.

**Affects Versions correction**: Remove RHTPA 2.2.0 (lock file evidence shows 2.2.0 ships h2 0.4.8, which is not affected).

---

## Case B: Cross-Stream Impact -- Preemptive Remediation for 2.1.x

Stream 2.1.x is affected but has no CVE Jira of its own for this CVE (TC-8030 is scoped to 2.2.x only). Preemptive remediation tasks should be created for stream 2.1.x using the preemptive variant templates.

### Preemptive Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

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

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

### Preemptive Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030)

**Blocked by**: Preemptive Task 1 (upstream backport)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

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

---

## Post-Triage Summary

### Actions to take on TC-8030:

1. **Correct Affects Versions**: Remove RHTPA 2.2.0 (not affected per lock file evidence)
2. **Post cross-stream impact comment**: Note that 2.1.x is affected
3. **Create preemptive remediation tasks** for 2.1.x stream (2 tasks: upstream backport + downstream propagation) with `security-preemptive` label and "Related" link type
4. **Add ai-cve-triaged label** to TC-8030
5. **Close TC-8030** as "Not a Bug" with VEX Justification "Component not Present" (customfield_12345)
6. **Post summary comment** documenting version impact table, Affects Versions correction, triage outcome, and preemptive task links
