# Step 8 -- Remediation

## Triage Decision

### In-scope stream (2.2.x): Case C -- No supported versions affected

The version impact table shows **NO** for all 2.2.x versions. Every version in the
2.2.x stream ships h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

**Rationale**: No supported versions in the 2.2.x stream ship a vulnerable version
of h2. Version impact analysis shows all 2.2.x versions ship h2 0.4.8 or later,
which is outside the affected range (< 0.4.8).

**VEX Justification**: Component not Present (the vulnerable version of h2 is not
shipped in any 2.2.x release -- all 2.2.x versions ship h2 >= 0.4.8, which is the
fixed version).

**Close comment** (to be posted on TC-8030):

> No supported versions in stream 2.2.x ship a vulnerable version of h2.
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
> All 2.2.x versions ship h2 >= 0.4.8 which is outside the affected range (< 0.4.8).
> Fix threshold determined from cross-validated MITRE CVE API and OSV.dev data.
>
> VEX Justification: Component not Present

### Out-of-scope stream (2.1.x): Case B -- Cross-stream impact

The version impact analysis reveals that the 2.1.x stream (outside this issue's
scope) is affected: versions 2.1.0 and 2.1.1 both ship h2 0.4.5 (< 0.4.8).

**Cross-stream impact comment** (to be posted on TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
> analysis. Versions 2.1.0 and 2.1.1 ship h2 0.4.5. This stream is tracked by
> a companion issue (see Related links) or may require separate PSIRT triage.

**Preemptive remediation tasks for 2.1.x** (no CVE Jira exists for this stream):

Since the 2.1.x stream has no stream-specific CVE Jira for CVE-2026-48901, create
preemptive remediation tasks with the `security-preemptive` label.

---

## Preemptive Remediation Tasks (2.1.x stream)

### Task 1: Upstream backport task

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030, the originating CVE Jira from stream 2.2.x)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
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

- Target branch: release/0.3.z
- **Dependency type**: to be determined during implementation (inspect Cargo.toml to determine if h2 is direct or transitive)
- Update h2 dependency to >= 0.4.8 in Cargo.lock
- If h2 is a transitive dependency, prefer bumping the direct dependency that pulls it in; fall back to `cargo add h2@0.4.8` to pin the transitive dep directly

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (originating CVE tracking issue)

---

### Task 2: Downstream propagation subtask

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030); Blocks (blocked by upstream backport task)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901
fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (originating CVE tracking issue)

---

## Post-Triage Actions Summary

1. **Close TC-8030** as Not a Bug with VEX Justification "Component not Present" --
   no 2.2.x versions ship a vulnerable version of h2
2. **Post cross-stream impact comment** on TC-8030 noting 2.1.x is affected
3. **Create preemptive upstream backport task** for 2.1.x stream (security-preemptive label)
4. **Create preemptive downstream propagation subtask** for 2.1.x stream (security-preemptive label, blocked by upstream task)
5. **Link preemptive tasks** to TC-8030 with "Related" link type
6. **Post preemptive task comment** on TC-8030 listing the created tasks
7. **Add ai-cve-triaged label** to TC-8030
8. **Post summary comment** on TC-8030 with version impact table, triage outcome, and reporter @mention
