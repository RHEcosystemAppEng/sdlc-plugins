# Step 8 -- Remediation: CVE-2026-99001

## Triage Outcome: Case B (Affected) with Case A (Cross-Stream Impact)

All supported versions in the 2.2.x stream (issue scope) are affected. The 2.1.x stream is also affected (cross-stream). criterion is a **dev-only dependency** -- remediation tasks carry the `dev-dependency` label and priority is overridden to **Normal**.

---

## Case A: Cross-Stream Impact Comment

The following comment would be posted to TC-8050:

> Cross-stream impact: criterion (versions before 0.5.2) also affects stream 2.1.x based on lock file analysis.
> These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.
>
> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: (see preemptive tasks below)

---

## Case B: Remediation Tasks for Stream 2.2.x (Issue Scope)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (overridden -- dev-only dependency, not shipped in production)

**Link**: Depend on TC-8050

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production builds, used for benchmarks only

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (overridden -- dev-only dependency, not shipped in production)

**Link**: Depend on TC-8050; Blocked by upstream task (Task 1)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

---

## Case A: Preemptive Remediation Tasks for Stream 2.1.x

These tasks are created proactively because the 2.1.x stream is affected but has no stream-specific CVE Jira for criterion.

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`

**Priority**: Normal (overridden -- dev-only dependency, not shipped in production)

**Link**: Related to TC-8050 (not Depend -- preemptive, different stream)

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8050 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production builds, used for benchmarks only

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue -- cross-stream)
```

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`

**Priority**: Normal (overridden -- dev-only dependency, not shipped in production)

**Link**: Related to TC-8050 (not Depend -- preemptive, different stream); Blocked by upstream preemptive task (Task 3)

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8050 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

The upstream backport bumps criterion to 0.5.2 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream preemptive backport task (must merge first)
- Depends on: TC-8050 (parent tracking issue -- cross-stream)
```

---

## Summary of Remediation Tasks

| # | Stream | Type | Summary | Labels | Priority | Link to TC-8050 |
|---|--------|------|---------|--------|----------|-----------------|
| 1 | 2.2.x | Upstream backport | Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x) | ai-generated-jira, Security, CVE-2026-99001, dev-dependency | Normal | Depend |
| 2 | 2.2.x | Downstream propagation | Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x) | ai-generated-jira, Security, CVE-2026-99001, dev-dependency | Normal | Depend |
| 3 | 2.1.x | Upstream backport (preemptive) | Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.1.x) | ai-generated-jira, Security, CVE-2026-99001, security-preemptive, dev-dependency | Normal | Related |
| 4 | 2.1.x | Downstream propagation (preemptive) | Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x) | ai-generated-jira, Security, CVE-2026-99001, security-preemptive, dev-dependency | Normal | Related |

### Key Decisions

- **dev-dependency label**: Applied to all tasks because criterion is declared in `[dev-dependencies]` and is not shipped in production builds.
- **Normal priority override**: All tasks set to Normal priority regardless of CVE severity (5.3 Medium), per the dependency scope decision tree for dev-only dependencies.
- **Supply chain risk note**: All task descriptions include the note that the dependency is dev/build-only and not shipped in production, with remediation priority set to Normal (supply chain risk only).
- **Preemptive tasks for 2.1.x**: Created because the issue is scoped to 2.2.x but cross-stream analysis shows 2.1.x is also affected. These carry the `security-preemptive` label and use "Related" link type instead of "Depend".
