# Step 8 -- Remediation

## Triage Decision

### Stream 2.2.x (in scope -- Case B)

Only version **2.2.0** is affected. Versions 2.2.1 through 2.2.4 already ship h2 >= 0.4.8 and are NOT affected. Since 2.2.0 is affected and the upstream branch (release/0.4.z) already ships the fix (h2 0.4.9 at the latest tag), the remediation uses the **dependency bump** variant.

### Stream 2.1.x (cross-stream -- Case A)

All versions in stream 2.1.x (2.1.0, 2.1.1) are affected. Since this issue is scoped to `[rhtpa-2.2]` and stream 2.1.x does not have its own CVE Jira for CVE-2026-48901, proactive (preemptive) remediation tasks are created for stream 2.1.x with the `security-preemptive` label.

The upstream branch release/0.3.z does NOT ship the fix -- h2 remains at 0.4.5 at the latest tag. Therefore the upstream task uses the **upstream backport** variant (not dependency bump).

---

## Remediation Tasks -- Stream 2.2.x (Standard)

### Task 1: Dependency Bump (upstream fix already available)

**Summary**: Remediate CVE-2026-48901: update h2 to 0.4.8 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`

**Link type**: Depend (to TC-8030)

#### Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: bump h2 to 0.4.8 via dependency update.
The vulnerable dependency (h2 < 0.4.8) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0 (h2 0.4.5 at build tag v0.4.5)
Source commit(s): v0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (h2 is a Cargo dependency)
- **Remediation action**: run `cargo update -p h2` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add h2@0.4.8`
- Verify the lock file reflects >= 0.4.8 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)
```

### Task 2: Downstream Propagation (blocked by Task 1)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`

**Link type**: Depend (to TC-8030), Blocks (blocked by Task 1)

#### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-48901 fix from the dependency bump task.

The dependency bump task bumps h2 to 0.4.8 on release/0.4.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [dependency-bump-task-key] (dependency bump must merge first)
- Depends on: TC-8030 (parent tracking issue)
```

---

## Remediation Tasks -- Stream 2.1.x (Preemptive / Case A)

These tasks carry the `security-preemptive` label and use the "Related" link type to TC-8030 (the originating CVE Jira for stream 2.2.x), because no stream-specific CVE Jira exists for 2.1.x.

### Task 3: Upstream Backport (fix NOT available on release/0.3.z)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030 -- preemptive, cross-stream)

#### Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5 at v0.3.8), 2.1.1 (h2 0.4.5 at v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (h2 is a Cargo dependency)
- The upstream branch release/0.3.z does NOT currently ship the fix
  (h2 remains at 0.4.5 at latest tag v0.3.12)
- Update h2 dependency to >= 0.4.8 in Cargo.toml on release/0.3.z
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (originating CVE tracking issue, cross-stream)
```

### Task 4: Downstream Propagation for 2.1.x (blocked by Task 3)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link type**: Related (to TC-8030 -- preemptive), Blocks (blocked by Task 3)

#### Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-backport-task-key] (upstream backport must merge first)
- Depends on: TC-8030 (originating CVE tracking issue, cross-stream)
```

---

## Cross-Stream Impact Comment (for TC-8030)

```
Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
Stream 2.1.x ships h2 0.4.5 in all versions (2.1.0, 2.1.1).
This stream is not tracked by a companion CVE issue and may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-backport-task-key] (upstream backport, security-preemptive)
- 2.1.x: [downstream-propagation-task-key] (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Jira Linkage Summary

| Task | Link Type | Target | Direction |
|------|-----------|--------|-----------|
| Dependency bump (2.2.x) | Depend | TC-8030 | outward |
| Downstream propagation (2.2.x) | Depend | TC-8030 | outward |
| Downstream propagation (2.2.x) | Blocks | Dependency bump (2.2.x) | blocked by |
| Upstream backport (2.1.x) | Related | TC-8030 | preemptive |
| Downstream propagation (2.1.x) | Related | TC-8030 | preemptive |
| Downstream propagation (2.1.x) | Blocks | Upstream backport (2.1.x) | blocked by |

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8030
2. Post summary comment to TC-8030 documenting:
   - Version impact table (2.2.0 affected, 2.2.1+ not affected)
   - Affects Versions correction: RHTPA 2.2.0 (already correct for in-scope stream)
   - Triage outcome: remediation tasks created
   - Cross-stream impact on 2.1.x with preemptive tasks
3. Transition TC-8030 to In Progress
