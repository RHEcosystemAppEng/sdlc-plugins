# Step 8 -- Remediation

## Triage Outcome

**Case B: Affected -- create remediation tasks**

All 2.2.x versions ship criterion 0.5.1, which is within the affected range
(< 0.5.2). Remediation tasks are required.

**Ecosystem**: Cargo (source dependency) -- 2 tasks per stream:
1. Dependency bump task (upstream)
2. Downstream propagation task

**Dev-dependency override**: criterion is a dev-only dependency (declared in
`[dev-dependencies]`). Per the dependency scope decision tree:
- Label: `dev-dependency` added to all remediation tasks
- Priority: **Normal** (overrides CVE severity of Medium/CVSS 5.3)

## Task 1: Dependency Bump Task (2.2.x stream)

**Summary**: Remediate CVE-2026-99001: update criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: bump criterion to 0.5.2 via dependency update.
The vulnerable dependency (criterion versions before 0.5.2) allows path
traversal in benchmark output via crafted benchmark names containing path
separators.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) --
  NOT shipped in production builds, used for benchmarks only
- **Remediation action**: run `cargo update -p criterion` to pull in criterion
  0.5.2 (the fixed version)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add criterion@0.5.2 --dev`
- Verify the lock file reflects criterion >= 0.5.2 after the update

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

## Task 2: Downstream Propagation Task (2.2.x stream)

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the dependency bump task.

The dependency bump task bumps criterion to 0.5.2 on release/0.4.z. Once
that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Jira Linkage Plan

1. Link dependency bump task to TC-8050 (Depend)
2. Link downstream propagation task to TC-8050 (Depend)
3. Link downstream propagation task as blocked by dependency bump task (Blocks)
4. If release Jira orchestration is active (Step 7.5): link both tasks to the
   release Task (Blocks) and link TC-8050 to the release Task (Related)

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected (all versions ship criterion 0.5.1).
A cross-stream impact comment would be posted on TC-8050:

> Cross-stream impact: criterion versions before 0.5.2 also affects
> stream 2.1.x based on lock file analysis. These streams are tracked by
> companion issues (see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks for 2.1.x would be created with:
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`
- Priority: Normal (dev-dependency override)
- Link type: Related (not Depend) to TC-8050
