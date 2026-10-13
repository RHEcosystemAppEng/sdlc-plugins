# Step 8 -- Remediation Task Descriptions: TC-8001

CVE-2026-31812: quinn-proto < 0.11.14 (DoS via excessive stream counts)

---

## Stream 2.2.x (In Scope -- Case B, Dependency Bump Variant)

Upstream fix is already available on release/0.4.z (v0.4.11+ ship quinn-proto 0.11.14).
Remediation is a dependency bump (no upstream backport needed) plus downstream propagation.

### Task 1: Dependency Bump -- quinn-proto (2.2.x)

**Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Issue Type**: Task

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation -- backend ref update (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-31812
**Issue Type**: Task

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

- Depends on: dependency bump task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### Jira Linkage for 2.2.x Tasks

1. Dependency bump task -> TC-8001: link type **Depend** (CVE inward, task outward)
2. Downstream propagation task -> TC-8001: link type **Depend** (CVE inward, task outward)
3. Dependency bump task -> downstream propagation task: link type **Blocks** (upstream inward, downstream outward)

---

## Stream 2.1.x (Out of Scope -- Case A, Preemptive Upstream Backport Variant)

Upstream fix is NOT available on release/0.3.z (latest v0.3.12 ships quinn-proto 0.11.9).
Remediation requires an upstream backport first, then downstream propagation.
These are preemptive tasks because no stream-specific CVE Jira exists for 2.1.x.

### Task 3: Preemptive Upstream Backport -- quinn-proto (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Issue Type**: Task
**Link Type**: Related (to originating CVE TC-8001, not Depend)

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 4: Preemptive Downstream Propagation -- backend ref update (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Issue Type**: Task
**Link Type**: Related (to originating CVE TC-8001, not Depend)

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

- Depends on: upstream backport task (upstream fix must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### Jira Linkage for 2.1.x Preemptive Tasks

1. Upstream backport task -> TC-8001: link type **Related** (preemptive, not Depend)
2. Downstream propagation task -> TC-8001: link type **Related** (preemptive, not Depend)
3. Upstream backport task -> downstream propagation task: link type **Blocks** (upstream inward, downstream outward)

---

## Summary of All Remediation Tasks

| # | Task | Stream | Type | Labels |
|---|------|--------|------|--------|
| 1 | Dependency bump: quinn-proto to 0.11.14 (rhtpa-2.2) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 |
| 2 | Downstream propagation: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 |
| 3 | Upstream backport: quinn-proto to 0.11.14 (rhtpa-2.1) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
| 4 | Downstream propagation: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |

Total: 4 remediation tasks (2 standard for 2.2.x + 2 preemptive for 2.1.x)
