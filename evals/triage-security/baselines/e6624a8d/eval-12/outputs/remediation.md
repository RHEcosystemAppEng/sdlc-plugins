# Step 8 -- Remediation

## Triage Decision

### Scoped Stream (2.2.x): Case C -- Not Affected

No versions in the 2.2.x stream ship a vulnerable version of h2. All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

- **Resolution**: Not a Bug
- **VEX Justification** (customfield_12345): **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x release
- **Closing comment**: "No supported 2.2.x versions ship a vulnerable version of h2. Version impact analysis shows all 2.2.x releases ship h2 >= 0.4.8 (fix threshold from MITRE CVE API and OSV.dev). The vulnerability (CVE-2026-48901, h2 HTTP/2 CONTINUATION flood, < 0.4.8) does not apply to this stream."

### Cross-Stream Impact (2.1.x): Case A -- Preemptive Remediation

Stream 2.1.x is affected (h2 0.4.5 < 0.4.8 at all versions) but has no stream-specific CVE Jira for CVE-2026-48901. Preemptive remediation tasks are created.

**Cross-stream impact comment** (posted to TC-8030):
```
Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
All 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5, which is within the affected range.
Stream 2.1.x is tracked by preemptive remediation tasks (see Related links)
and may require separate PSIRT triage.
```

---

## Remediation Tasks for Stream 2.1.x (Preemptive)

Ecosystem: Cargo (source dependency) -- 2 tasks required per stream.
Labels include `security-preemptive` since no 2.1.x-scoped CVE Jira exists.
Link type: "Related" to TC-8030 (originating CVE from a different stream).

### Task 1: Upstream Backport (rhtpa-backend, release/0.3.z)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Description**:

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

Affected versions: 2.1.0 (v0.3.8, h2 0.4.5), 2.1.1 (v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (h2 is a direct Cargo dependency)
- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)

---

### Task 2: Downstream Propagation (rhtpa-release.0.3.z)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Blocked by**: Task 1 (upstream backport must merge first)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

- Blocked by: upstream backport task (must merge first)
- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)

---

## Jira Linkage Summary

| Task | Type | Link to TC-8030 | Additional Links |
|------|------|-----------------|------------------|
| Upstream backport (2.1.x) | Task | Related | -- |
| Downstream propagation (2.1.x) | Task | Related | Blocked by upstream backport task |

## Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8030
2. **Post summary comment** to TC-8030 documenting:
   - Version impact table (2.2.x not affected, 2.1.x affected)
   - Affects Versions correction (RHTPA 2.2.0 should be removed since 2.2.x is not affected)
   - Triage outcome: 2.2.x closed as Not a Bug; preemptive remediation created for 2.1.x
   - Links to preemptive remediation tasks
   - @mention of the issue reporter (PSIRT analyst)
3. **Close TC-8030** with resolution "Not a Bug" and VEX justification "Component not Present" (after engineer confirmation)
