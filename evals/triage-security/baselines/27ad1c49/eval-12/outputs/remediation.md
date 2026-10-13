# Step 8 -- Remediation

## Triage Decision Flow

1. **Any supported versions affected?** YES -- stream 2.1.x ships h2 0.4.5 (< 0.4.8)
2. **Issue scoped to a single stream?** YES -- scoped to 2.2.x via suffix `[rhtpa-2.2]`
3. **Other streams also affected?** YES -- stream 2.1.x is affected
4. **Flow**: Case A (cross-stream impact) followed by Case B (remediation for scoped stream)

## Scoped Stream Result (2.2.x)

**No remediation tasks needed for stream 2.2.x.** All versions in the scoped stream ship h2 >= 0.4.8 (the fix threshold). The scoped stream is not affected.

No remediation tasks are created within the issue's scope because no 2.2.x versions are vulnerable.

## Case A -- Cross-Stream Impact

Stream 2.1.x is affected (h2 0.4.5 < 0.4.8 in versions 2.1.0 and 2.1.1) but is outside this issue's scope. A cross-stream impact comment would be posted to TC-8030:

> Cross-stream impact: h2 (< 0.4.8) also affects stream 2.1.x based on lock file analysis.
> Versions affected: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5).
> This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

### Preemptive Remediation Tasks for Stream 2.1.x

Since stream 2.1.x is affected and (assuming) has no existing CVE Jira for CVE-2026-48901, preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type to the originating CVE Jira TC-8030.

h2 is a Cargo ecosystem (source dependency), so **2 tasks** are created for stream 2.1.x:

---

### Task 1: Upstream Backport -- Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
**Link**: Related to TC-8030 (originating CVE Jira, different stream)

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (tag v0.3.8, h2 0.4.5), RHTPA 2.1.1 (tag v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be determined via lock file / manifest inspection
- Update h2 dependency to >= 0.4.8 in Cargo.lock / Cargo.toml

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add h2@0.4.8` to add as a direct dependency,
  overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue -- Related link, preemptive)
```

---

### Task 2: Downstream Propagation -- Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
**Link**: Related to TC-8030 (originating CVE Jira, different stream)
**Blocked by**: Task 1 (upstream backport must merge first)

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

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
- Depends on: TC-8030 (parent tracking issue -- Related link, preemptive)
```

---

## Post-Triage Summary

### Triage Outcome

- **Scoped stream (2.2.x)**: NOT AFFECTED -- all versions ship h2 >= 0.4.8. No remediation tasks created within scope.
- **Cross-stream impact (2.1.x)**: AFFECTED -- versions 2.1.0 and 2.1.1 ship h2 0.4.5. Preemptive remediation tasks created (2 tasks: upstream backport + downstream propagation) with `security-preemptive` label.

### Affects Versions Correction

Current: RHTPA 2.2.0
Proposed: No change needed (or remove RHTPA 2.2.0 since 2.2.x is not affected). The PSIRT-assigned Affects Version of RHTPA 2.2.0 is incorrect -- version 2.2.0 ships h2 0.4.8, which is at the fix threshold and is NOT vulnerable.

### Recommended Actions

1. **Correct Affects Versions**: Remove RHTPA 2.2.0 from Affects Versions (2.2.x is not affected).
2. **Post cross-stream impact comment** noting 2.1.x is affected.
3. **Create preemptive remediation tasks** for stream 2.1.x (2 tasks as described above).
4. **Close TC-8030** as "Not a Bug" with VEX Justification "Component not Present" (the vulnerable version of h2 is not present in any 2.2.x release). The VEX Justification custom field (customfield_12345) would be set to "Component not Present".
5. **Add ai-cve-triaged label** to TC-8030.

### Jira Linkage Plan

- Preemptive upstream task --> TC-8030: Related (cross-stream, preemptive)
- Preemptive downstream task --> TC-8030: Related (cross-stream, preemptive)
- Preemptive upstream task --> preemptive downstream task: Blocks (upstream must merge first)
