# Step 8 -- Remediation: TC-8030 (CVE-2026-48901, h2)

## Triage Decision Summary

- **Issue**: TC-8030 -- CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2]
- **Scoped stream**: 2.2.x
- **Scoped stream impact**: NOT AFFECTED (all 2.2.x versions ship h2 >= 0.4.8)
- **Cross-stream impact**: 2.1.x IS AFFECTED (all 2.1.x versions ship h2 0.4.5 < 0.4.8)

## Case C: Scoped Stream (2.2.x) -- Close as Not a Bug

Since no versions in the scoped 2.2.x stream are affected:

**PROPOSAL**: Close TC-8030 as "Not a Bug" (not affected).

### Proposed Jira Mutations

1. **Affects Versions correction**: Remove RHTPA 2.2.0 (no 2.2.x versions are affected)
2. **VEX Justification** (customfield_12345): Set to **"Component not Present"**
   - Rationale: The vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version. All 2.2.x builds include h2 >= 0.4.8.
3. **Comment**: Post triage analysis documenting version impact evidence
4. **Resolution**: Close with resolution "Not a Bug"
5. **Label**: Add `ai-cve-triaged`

### Proposed Close Comment

```
No supported versions in stream 2.2.x ship a vulnerable version of h2.

Version impact analysis (fix threshold: h2 < 0.4.8, source: MITRE CVE API + OSV.dev):

| Version | h2 Version | Affected? |
|---------|------------|-----------|
| 2.2.0   | 0.4.8      | NO        |
| 2.2.1   | 0.4.8      | NO        |
| 2.2.2   | --         | NO (retag of 2.2.1) |
| 2.2.3   | 0.4.9      | NO        |
| 2.2.4   | 0.4.9      | NO        |

All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.
VEX Justification: Component not Present.

Cross-stream note: Stream 2.1.x IS affected (h2 0.4.5 < 0.4.8).
Preemptive remediation tasks created for 2.1.x -- see below.
```

---

## Case A: Cross-Stream Impact -- Preemptive Remediation for 2.1.x

The version impact analysis reveals that stream 2.1.x (outside the scoped stream 2.2.x) is affected. Since no sibling CVE Jira exists for 2.1.x (no companion issues found in mock data), preemptive remediation tasks are created.

### Cross-Stream Impact Comment (PROPOSAL)

```
Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
analysis. Stream 2.1.x versions ship h2 0.4.5 (affected).
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Ecosystem Classification

- Ecosystem: **Cargo** (source dependency)
- Fix availability: **Fix available upstream** (h2 0.4.8 published on crates.io)
- Task pattern: **Dependency bump + downstream propagation** (2 tasks)
- Labels: Include `security-preemptive` (preemptive task for stream without its own CVE Jira)
- Link type: **Related** to TC-8030 (not Depend, since TC-8030 belongs to a different stream)

---

### Preemptive Task 1: Dependency Bump (2.1.x)

**PROPOSAL**: Create Jira Task

**Summary**: Remediate CVE-2026-48901: update h2 to 0.4.8 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for stream 2.1.x. When PSIRT creates one, this task will be linked
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
- **Dependency type**: to be determined via Cargo.toml/Cargo.lock analysis
- **Remediation action**: run `cargo update -p h2` to pull in h2 >= 0.4.8
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`
- Verify the lock file reflects h2 >= 0.4.8 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira, different stream)
```

**Proposed Jira Link**: Related link from TC-8030 to this task (not Depend, since TC-8030 is scoped to a different stream)

---

### Preemptive Task 2: Downstream Propagation (2.1.x)

**PROPOSAL**: Create Jira Task

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for stream 2.1.x. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the dependency bump task.

The dependency bump task bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the h2 fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: [dependency bump task] (upstream fix must merge first)
- Related to: TC-8030 (originating CVE Jira, different stream)
```

**Proposed Jira Links**:
- Blocks link: dependency bump task (inward) blocks this downstream task (outward)
- Related link: TC-8030 (originating CVE) to this task

---

## Preemptive Task Comment (PROPOSAL)

Post comment on TC-8030:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [dependency-bump-task-key] (security-preemptive) -- bump h2 to 0.4.8
- 2.1.x: [downstream-propagation-task-key] (security-preemptive) -- propagate fix

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary (PROPOSAL)

**Label addition**: Add `ai-cve-triaged` to TC-8030

**Summary comment on TC-8030**:

```
Triage complete for CVE-2026-48901 (h2 HTTP/2 CONTINUATION flood).

Version impact (fix threshold: h2 < 0.4.8, cross-validated from MITRE + OSV.dev):

| Stream | Versions | h2 Version | Affected? |
|--------|----------|------------|-----------|
| 2.1.x  | 2.1.0, 2.1.1 | 0.4.5 | YES |
| 2.2.x  | 2.2.0--2.2.4 | 0.4.8--0.4.9 | NO |

Affects Versions correction: Removed RHTPA 2.2.0 (not affected in 2.2.x).

Triage outcome: Closed as Not a Bug -- no 2.2.x versions ship vulnerable h2.
VEX Justification: Component not Present.

Cross-stream impact: 2.1.x is affected (h2 0.4.5 < 0.4.8).
Preemptive remediation tasks created for 2.1.x:
- [dependency-bump-task-key]: bump h2 to 0.4.8 on release/0.3.z (security-preemptive)
- [downstream-propagation-task-key]: propagate fix to rhtpa-release.0.3.z (security-preemptive)
```

---

## All Proposed Jira Mutations (Summary)

These are PROPOSALS only -- not executed actions.

| # | Operation | Target | Details |
|---|-----------|--------|---------|
| 1 | Field edit | TC-8030 | Remove RHTPA 2.2.0 from Affects Versions |
| 2 | Field edit | TC-8030 | Set VEX Justification (customfield_12345) to "Component not Present" |
| 3 | Comment | TC-8030 | Cross-stream impact comment (2.1.x affected) |
| 4 | Create Task | (new) | Preemptive dependency bump: h2 to 0.4.8, stream 2.1.x |
| 5 | Create Task | (new) | Preemptive downstream propagation: update backend ref, stream 2.1.x |
| 6 | Link (Related) | TC-8030 <-> Task #4 | Preemptive task link (Related, not Depend) |
| 7 | Link (Related) | TC-8030 <-> Task #5 | Preemptive task link (Related, not Depend) |
| 8 | Link (Blocks) | Task #4 -> Task #5 | Upstream blocks downstream |
| 9 | Comment | TC-8030 | Preemptive task creation comment |
| 10 | Field edit | TC-8030 | Add label `ai-cve-triaged` |
| 11 | Comment | TC-8030 | Post-triage summary with version impact table |
| 12 | Status transition | TC-8030 | Close with resolution "Not a Bug" |
