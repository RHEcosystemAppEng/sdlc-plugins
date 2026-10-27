# Step 8 -- Remediation

## Triage Outcome

**Case B: Affected -- create remediation tasks**

All supported versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (versions before 0.5.2). Remediation tasks are required.

**Dev-dependency handling**: criterion is declared in `[dev-dependencies]` and is NOT shipped in production builds. Per the dependency scope decision tree:
- Remediation tasks are still created (supply chain risk)
- `dev-dependency` label added to all remediation tasks
- Priority overridden to **Normal** regardless of CVE severity
- Task descriptions include dev/build-only note

## Remediation Tasks (2.2.x stream)

Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

---

### Task 1: Upstream Dependency Bump

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (overridden -- dev-dependency, not shipped in production)

**Description**:

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: bump criterion to 0.5.2 via dependency update.
The vulnerable dependency (criterion versions before 0.5.2) allows an attacker to write benchmark output files to arbitrary paths via crafted benchmark names containing path separators.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production, used for benchmarks only
- **Remediation action**: run `cargo update -p criterion` to pull in criterion >= 0.5.2
- If the update pulls a version that still falls within the affected range, pin explicitly: `cargo add criterion@0.5.2 --dev`
- Verify the lock file reflects criterion >= 0.5.2 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (overridden -- dev-dependency, not shipped in production)

**Description**:

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001 fix from the upstream dependency bump task.

The upstream task bumps criterion to 0.5.2 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
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

- Depends on: upstream dependency bump task (upstream fix must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Jira Linkage Plan

1. Link upstream task to TC-8050 with type "Depend" (CVE inward, task outward)
2. Link downstream task to TC-8050 with type "Depend" (CVE inward, task outward)
3. Link downstream task as blocked by upstream task with type "Blocks" (upstream inward, downstream outward)

## Summary

| # | Task | Stream | Labels | Priority | Link to CVE |
|---|------|--------|--------|----------|-------------|
| 1 | Upstream: bump criterion to 0.5.2 | 2.2.x | ai-generated-jira, Security, CVE-2026-99001, dev-dependency | Normal | Depend |
| 2 | Downstream: propagate fix to rhtpa-release.0.4.z | 2.2.x | ai-generated-jira, Security, CVE-2026-99001, dev-dependency | Normal | Depend |

**Key points**:
- Both tasks carry the `dev-dependency` label because criterion is a dev-only dependency ([dev-dependencies])
- Priority is overridden to **Normal** regardless of CVE severity (CVSS 5.3 Medium) because the dependency is not shipped in production
- Both task descriptions include the note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
- Remediation is still performed despite dev-only status due to supply chain risk (compromised dev dependencies can inject malicious code during builds)
