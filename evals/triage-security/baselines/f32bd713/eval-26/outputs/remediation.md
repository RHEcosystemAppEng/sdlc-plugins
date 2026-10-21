# Step 8 -- Remediation: TC-8050

## Triage Outcome

**Case B** (Affected -- create remediation tasks) for the scoped 2.2.x stream.
**Case A** (Cross-stream impact) for the 2.1.x stream, which is also affected but outside the issue scope.

criterion is a **dev-only dependency** (declared in `[dev-dependencies]`). It is NOT shipped in production builds. Per the dependency scope decision tree, all remediation tasks carry the `dev-dependency` label and priority is overridden to **Normal** regardless of CVE severity.

---

## Case B: Remediation Tasks for 2.2.x (scoped stream)

Ecosystem: Cargo (source dependency, fix NOT available upstream) -- 2 tasks.

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (dev-dependency override -- not inherited from CVE severity)

**Description**:

```
## Repository

backend

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

Upstream fix: (no upstream PR link available)
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) --
  NOT shipped in production builds. Used for benchmarks only.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

**Link**: Depend (TC-8050 inward, this task outward)

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (dev-dependency override)

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

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

- Depends on: [upstream-backport-task-key] (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

**Link**: Blocks (upstream task inward, this task outward)
**Link**: Depend (TC-8050 inward, this task outward)

---

## Case A: Cross-Stream Impact -- Preemptive Remediation for 2.1.x

Stream 2.1.x is also affected (criterion 0.5.1 < 0.5.2 in versions 2.1.0 and 2.1.1) but is outside the issue scope of TC-8050.

No existing sibling CVE Jira was found for CVE-2026-99001 scoped to stream 2.1.x.

Preemptive remediation tasks are created with `security-preemptive` label and "Related" link type.

### Preemptive Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`

**Priority**: Normal (dev-dependency override)

**Description**:

```
## Repository

backend

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

Upstream fix: (no upstream PR link available)
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) --
  NOT shipped in production builds. Used for benchmarks only.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (originating CVE Jira, cross-stream)
```

**Link**: Related (TC-8050 inward, this task outward -- preemptive, not Depend)

---

### Preemptive Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`

**Priority**: Normal (dev-dependency override)

**Description**:

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

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

The upstream backport bumps criterion to 0.5.2 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

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

- Depends on: [preemptive-upstream-backport-task-key] (upstream backport must merge first)
- Depends on: TC-8050 (originating CVE Jira, cross-stream)
```

**Link**: Blocks (preemptive upstream task inward, this task outward)
**Link**: Related (TC-8050 inward, this task outward -- preemptive, not Depend)

---

## Cross-Stream Impact Comment (to be posted on TC-8050)

```
Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on
lock file analysis. This stream is tracked by companion issues (see Related
links) or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (security-preemptive), [downstream-task-key] (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation
will link them and remove the label.
```

---

## Summary

| Stream | Task Type | Task Count | Labels | Priority | Link to TC-8050 |
|--------|-----------|------------|--------|----------|-----------------|
| 2.2.x | Standard upstream backport | 1 | ai-generated-jira, Security, CVE-2026-99001, dev-dependency | Normal | Depend |
| 2.2.x | Standard downstream propagation | 1 | ai-generated-jira, Security, CVE-2026-99001, dev-dependency | Normal | Depend |
| 2.1.x | Preemptive upstream backport | 1 | ai-generated-jira, Security, CVE-2026-99001, security-preemptive, dev-dependency | Normal | Related |
| 2.1.x | Preemptive downstream propagation | 1 | ai-generated-jira, Security, CVE-2026-99001, security-preemptive, dev-dependency | Normal | Related |

**Total tasks**: 4 (2 standard for 2.2.x + 2 preemptive for 2.1.x)

All tasks have:
- `dev-dependency` label (criterion is a dev-only dependency, not shipped in production)
- **Normal** priority (overridden from CVE severity due to dev-dependency status)
- Note in description: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
