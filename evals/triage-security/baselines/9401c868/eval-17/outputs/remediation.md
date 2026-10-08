# Step 8 -- Remediation

## Triage Outcome

**Case B** applies: supported versions within the issue's scoped stream (2.2.x) are affected (2.2.0, 2.2.1, 2.2.2).

**Case A** also applies: the issue is scoped to 2.2.x, but the 2.1.x stream is also affected. Cross-stream impact comment and preemptive remediation tasks are needed for 2.1.x.

## Remediation Tasks for Stream 2.2.x (Case B -- Scoped Stream)

Ecosystem: Cargo (source dependency). Upstream fix is available on release/0.4.z (Step 2.5 confirmed). Remediation uses the **dependency bump** variant: 2 tasks.

### Task 1: Dependency Bump (2.2.x)

```
Summary: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)
Labels: ai-generated-jira, Security, CVE-2026-31812

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the
  latest compatible version (>= 0.11.14)
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Task 2: Downstream Propagation (2.2.x)

```
Summary: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
Labels: ai-generated-jira, Security, CVE-2026-31812

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Task 1 (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage (2.2.x)

- Task 1 (dependency bump) -> TC-8001: **Depend**
- Task 2 (downstream) -> TC-8001: **Depend**
- Task 1 -> Task 2: **Blocks** (upstream blocks downstream)

---

## Preemptive Remediation Tasks for Stream 2.1.x (Case A -- Cross-Stream Impact)

The 2.1.x stream is affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9) but has no CVE Jira of its own. Preemptive remediation tasks are created with the `security-preemptive` label.

Ecosystem: Cargo (source dependency). Upstream fix is **not** available on release/0.3.z. Remediation uses the **upstream backport** variant: 2 tasks.

### Preemptive Task 1: Upstream Backport (2.1.x)

```
Summary: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Preemptive Task 2: Downstream Propagation (2.1.x)

```
Summary: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Preemptive Task 1 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage (2.1.x -- Preemptive)

- Preemptive Task 1 (upstream backport) -> TC-8001: **Related** (not Depend -- preemptive, different stream)
- Preemptive Task 2 (downstream) -> TC-8001: **Related** (not Depend -- preemptive, different stream)
- Preemptive Task 1 -> Preemptive Task 2: **Blocks** (upstream blocks downstream)

---

## Cross-Stream Impact Comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
based on lock file analysis. These streams are tracked by companion issues
(see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-backport-task-key] + [downstream-propagation-task-key] (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Summary of All Remediation Tasks

| # | Task | Stream | Type | Variant | Labels |
|---|------|--------|------|---------|--------|
| 1 | Dependency bump: quinn-proto to 0.11.14 | 2.2.x | upstream | dependency bump (fix available) | ai-generated-jira, Security, CVE-2026-31812 |
| 2 | Downstream propagation: update backend ref in rhtpa-release.0.4.z | 2.2.x | downstream | standard | ai-generated-jira, Security, CVE-2026-31812 |
| 3 | Upstream backport: quinn-proto to 0.11.14 | 2.1.x | upstream | backport (fix not available) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
| 4 | Downstream propagation: update backend ref in rhtpa-release.0.3.z | 2.1.x | downstream | preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |

Total: 4 tasks (2 per affected stream, consistent with Cargo source dependency ecosystem classification).
